from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.views.generic import TemplateView
from django.contrib import messages
from django.db.models import Avg, Count
from django.db.models.functions import ExtractMonth
from django.core.mail import send_mail
from django.conf import settings

from .models import Booking, Review, HomeWelcomeVideo
from .models import Restaurant, SpecialDish, RestaurantOffer, RestaurantImage
from .forms import ReviewForm
from .utils import send_review_notification
from gallery.models import GalleryImage, GalleryCategory

def home(request):
    """Home page view with fake reviews"""
    # Get video
    video = HomeWelcomeVideo.objects.filter(is_active=True).order_by("-uploaded_at").first()
    
    # Pick independent sort modes from query string
    date_sort = request.GET.get('date_sort', 'newest')      # newest or oldest
    experience_sort = request.GET.get('overall_sort', 'best')  # best or worst

    # Build review queryset, apply sort by experience then date secondarily
    qs = Review.objects.filter(status='approved')
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

    # Find analytical top/bottom reviews for highlight
    # If no reviews in database, create fake ones for display
    if not reviews:
        reviews = [
            {
                'user_name': 'Gita Gurung',
                'rating': 5,
                'review_title': 'Wonderful Stay',
                'review_text': 'The rooms were spacious and clean. Great value for money. Highly recommended!',
                'created_at': '2024-03-12',
                'sentiment': 'Loved it! 😊',
                'stars': range(5),
            },
            {
                'user_name': 'Bikram Thapa',
                'rating': 5,
                'review_title': 'Best in Town',
                'review_text': 'Exceptional service and beautiful views. The restaurant serves delicious food.',
                'created_at': '2024-03-11',
                'sentiment': 'Loved it! 😊',
                'stars': range(5),
            },
            {
                'user_name': 'Sunita Rai',
                'rating': 5,
                'review_title': 'Perfect Getaway',
                'review_text': 'A perfect place to relax and unwind. The staff was very attentive and courteous.',
                'created_at': '2024-03-10',
                'sentiment': 'Loved it! 😊',
                'stars': range(5),
            },
        ]
    else:
        # For real reviews, add stars
        reviews = list(reviews)  # evaluate queryset
        for r in reviews:
            r.stars = range(r.rating)
    
    context = {
        "video": video,
        "reviews": reviews,
        "review_form": ReviewForm(),
        "date_sort": date_sort,
        "overall_sort": experience_sort,
    }

    # Demand forecasting: top busy months based on bookings
    busy_periods = Booking.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).order_by('-count')[:3]
    context['busy_periods'] = busy_periods

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
    return render(request, "core/about.html")


# -------------------------
# HOTEL PAGE
# -------------------------
def hotel(request):
    category = GalleryCategory.objects.filter(name__iexact="R-Asad Hotel").first()

    if category:
        gallery = GalleryImage.objects.filter(category=category)
    else:
        gallery = []

    return render(request, "core/hotel.html", {
        "gallery": gallery
    })


# -------------------------
# CONTACT PAGE
# -------------------------
def contact(request):
    success = False

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        full_message = f"""
        New Contact Message

        Name: {name}
        Email: {email}

        Message:
        {message}
        """

        send_mail(
            subject=f"Contact Form: {subject}",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        success = True

    return render(request, "core/contact.html", {"success": success})


# -------------------------
# BOOKING FORM
# -------------------------
def booking_form(request):
    context = {}

    if request.method == "POST":
        try:
            # Create booking object (NOT saved yet)
            booking = Booking(
                name=request.POST.get("name"),
                checkin=request.POST.get("checkin"),
                checkout=request.POST.get("checkout"),
                guests=request.POST.get("guests"),
                room=request.POST.get("room"),
                phone=request.POST.get("phone"),
                email=request.POST.get("email"),
            )

            # Run model validation (clean method)
            booking.full_clean()

            # Save to database
            booking.save()

            context["success"] = True

        except ValidationError as e:
            # Validation failed
            context["error"] = e.messages

    # Works for both GET and POST
    return render(request, "core/booking_form.html", context)


# -------------------------
# RESTAURANT PAGE
# -------------------------
def restaurant_view(request):
    restaurant = Restaurant.objects.filter(is_active=True).first()
    dishes = SpecialDish.objects.filter(is_active=True)
    offers = RestaurantOffer.objects.filter(is_active=True)
    images = RestaurantImage.objects.filter(is_active=True)

    context = {
        'restaurant': restaurant,
        'dishes': dishes,
        'offers': offers,
        'images': images,
    }
    return render(request, 'core/restaurant.html', context)