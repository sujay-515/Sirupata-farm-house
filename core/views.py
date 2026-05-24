from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.views.generic import TemplateView
from django.contrib import messages
from django.db.models import Avg, Count
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_date

from ml_engine.services.analytics import get_stay_month_trend_data
from .models import AboutLocation, Booking, ContactSubmission, Review, HomeWelcomeVideo
from .models import Hotel, Restaurant, SiteContent, SpecialDish, RestaurantOffer, RestaurantImage
from .emails import send_booking_received_email, send_contact_submission_notification
from .forms import ContactForm, ReviewForm
from .utils import send_review_notification
from gallery.models import GalleryImage, GalleryCategory
from rooms.catalog import get_public_rooms


def get_site_content():
    return SiteContent.objects.order_by("id").first()


def home(request):
    """Home page view."""
    # Get video
    video = HomeWelcomeVideo.objects.filter(is_active=True).order_by("-uploaded_at").first()
    site_content = get_site_content()
    
    # Pick independent sort modes from query string
    date_sort = request.GET.get('date_sort', 'newest')      # newest or oldest
    experience_sort = request.GET.get('overall_sort', 'best')  # best or worst

    qs = Review.objects.filter(status='approved')
    review_summary = qs.aggregate(
        average_rating=Avg("rating"),
        total_reviews=Count("id"),
    )

    # Build review queryset, apply sort by experience then date secondarily
    if experience_sort == 'best':
        if date_sort == 'oldest':
            reviews = qs.order_by('-sentiment_score', 'created_at')[:6]
        else:
            reviews = qs.order_by('-sentiment_score', '-created_at')[:6]
    else:
        if date_sort == 'oldest':
            reviews = qs.order_by('sentiment_score', 'created_at')[:6]
        else:
            reviews = qs.order_by('sentiment_score', '-created_at')[:6]

    reviews = list(reviews)
    for r in reviews:
        r.stars = range(r.rating)
    
    context = {
        "video": video,
        "reviews": reviews,
        "review_form": ReviewForm(),
        "date_sort": date_sort,
        "overall_sort": experience_sort,
        "stay_trend": get_stay_month_trend_data(),
        "site_content": site_content,
        "review_average": round(review_summary["average_rating"], 1) if review_summary["average_rating"] else None,
        "review_count": review_summary["total_reviews"],
    }

    if request.GET.get('ajax') == '1':
        return render(request, "core/reviews_grid.html", context)

    return render(request, "core/home.html", context)

def submit_review(request):
    """Handle review submission"""
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.status = 'pending'  # New reviews need approval
            review.save()
            messages.success(request, 'Thank you for your review! It will be published after admin approval.')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    return redirect('home')
# -------------------------
# ABOUT PAGE
# -------------------------
def about(request):
    return render(
        request,
        "core/about.html",
        {
            "site_content": get_site_content(),
            "about_locations": AboutLocation.objects.filter(is_active=True),
        },
    )


# -------------------------
# HOTEL PAGE
# -------------------------
def hotel(request):
    hotel_obj = Hotel.objects.filter(is_active=True).first()
    gallery = []
    lead_gallery_image = None
    supporting_images = []
    if hotel_obj:
        gallery = list(hotel_obj.gallery_images.all())
        if not gallery:
            category = GalleryCategory.objects.filter(name__iexact=hotel_obj.name).first()
            if category:
                gallery = list(GalleryImage.objects.filter(category=category))

    if gallery:
        featured_gallery = [image for image in gallery if image.is_featured]
        non_featured_gallery = [image for image in gallery if not image.is_featured]

        if featured_gallery:
            lead_gallery_image = featured_gallery[0]
            supporting_images = featured_gallery[1:5] + non_featured_gallery[:4]
        else:
            lead_gallery_image = gallery[0]
            supporting_images = gallery[1:5]

    return render(request, "core/hotel.html", {
        "hotel": hotel_obj,
        "gallery": gallery,
        "lead_gallery_image": lead_gallery_image,
        "supporting_gallery_images": supporting_images,
    })


# -------------------------
# CONTACT PAGE
# -------------------------
def contact(request):
    form = ContactForm(request.POST or None)
    success = False
    mail_sent = False

    if request.method == "POST":
        if form.is_valid():
            submission = form.save()
            if send_contact_submission_notification(submission):
                submission.emailed_at = timezone.now()
                submission.save(update_fields=["emailed_at"])
                mail_sent = True
            success = True
            form = ContactForm()
        else:
            messages.error(request, "Please correct the highlighted contact form fields.")

    return render(
        request,
        "core/contact.html",
        {
            "success": success,
            "mail_sent": mail_sent,
            "contact_form": form,
        },
    )


# -------------------------
# BOOKING FORM
# -------------------------
def booking_form(request):
    context = {}
    all_rooms = get_public_rooms()
    selected_room = request.GET.get('room') or request.POST.get("room")
    room_lookup = {room["name"]: room for room in all_rooms}

    room_data = room_lookup.get(selected_room)
    if room_data is None and all_rooms:
        room_data = all_rooms[0]
        selected_room = room_data["name"]

    context['selected_room'] = selected_room
    context['room_data'] = room_data
    context['all_rooms'] = all_rooms

    if request.method == "POST":
        try:
            checkin_raw = request.POST.get("checkin")
            checkout_raw = request.POST.get("checkout")
            checkin_date = parse_date(checkin_raw or "")
            checkout_date = parse_date(checkout_raw or "")

            if not checkin_date or not checkout_date:
                raise ValidationError("Please enter valid check-in and check-out dates.")

            # Create booking object (NOT saved yet)
            booking = Booking(
                name=request.POST.get("name"),
                checkin=checkin_date,
                checkout=checkout_date,
                guests=request.POST.get("guests"),
                room=request.POST.get("room"),
                phone=request.POST.get("phone"),
                email=request.POST.get("email"),
            )

            today = timezone.localdate()
            if booking.checkin < today:
                raise ValidationError("Check-in date cannot be in the past.")
            if booking.checkout < today:
                raise ValidationError("Check-out date cannot be in the past.")

            # Run model validation (clean method)
            booking.full_clean()

            # Save to database
            booking.save()
            if send_booking_received_email(booking):
                booking.received_email_sent_at = timezone.now()
                booking.save(update_fields=["received_email_sent_at"])

            messages.success(request, "Booking submitted successfully! We'll contact you shortly.")
            return redirect("booking_success")

        except ValidationError as e:
            # Validation failed
            context["error"] = e.messages

    # Works for both GET and POST
    return render(request, "core/booking_form.html", context)


def booking_success(request):
    return render(request, "core/booking_success.html")


# -------------------------
# RESTAURANT PAGE
# -------------------------
def restaurant_view(request):
    restaurant = Restaurant.objects.filter(is_active=True).first()
    dishes = SpecialDish.objects.filter(is_active=True, restaurant=restaurant) if restaurant else []
    offers = RestaurantOffer.objects.filter(is_active=True, restaurant=restaurant) if restaurant else []
    images = RestaurantImage.objects.filter(is_active=True, restaurant=restaurant) if restaurant else []

    lead_image = None
    supporting_images = []
    if images:
        lead_image = images[0]
        supporting_images = list(images[1:5])

    context = {
        'restaurant': restaurant,
        'dishes': dishes,
        'offers': offers,
        'images': images,
        'lead_restaurant_image': lead_image,
        'supporting_restaurant_images': supporting_images,
    }
    return render(request, 'core/restaurant.html', context)
