from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import datetime

from ml_engine.services.sentiment import compute_review_sentiment, get_sentiment_label


# =========================
# BOOKING
# =========================
class Booking(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("confirmed", "Confirmed"),
        ("checked_in", "Checked In"),
        ("checked_out", "Checked Out"),
        ("cancelled", "Cancelled"),
    ]

    name = models.CharField(max_length=100, blank=True, null=True)
    checkin = models.DateField()
    checkout = models.DateField()
    guests = models.CharField(max_length=20)
    room = models.CharField(max_length=100, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new", db_index=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    received_email_sent_at = models.DateTimeField(blank=True, null=True, editable=False)
    confirmed_email_sent_at = models.DateTimeField(blank=True, null=True, editable=False)

    def clean(self):
        # Historical bookings should remain editable in admin; only the
        # public booking flow blocks past dates before a record is created.
        if self.checkout <= self.checkin:
            raise ValidationError("Checkout date must be after check-in date")

    def __str__(self):
        return f"{self.room} | {self.checkin}"

    def save(self, *args, **kwargs):
        previous_status = None
        previous_confirmed_email_sent_at = None
        if self.pk:
            previous = Booking.objects.filter(pk=self.pk).values("status", "confirmed_email_sent_at").first()
            if previous:
                previous_status = previous["status"]
                previous_confirmed_email_sent_at = previous["confirmed_email_sent_at"]

        super().save(*args, **kwargs)

        if (
            self.status == "confirmed"
            and previous_status != "confirmed"
            and not self.confirmed_email_sent_at
            and not previous_confirmed_email_sent_at
        ):
            from .emails import send_booking_confirmed_email

            if send_booking_confirmed_email(self):
                sent_at = timezone.now()
                Booking.objects.filter(pk=self.pk, confirmed_email_sent_at__isnull=True).update(
                    confirmed_email_sent_at=sent_at
                )
                self.confirmed_email_sent_at = sent_at


# =========================
# HOTEL
# =========================
class Hotel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    hero_image = models.ImageField(upload_to="hotel/hero/", blank=True)
    location = models.CharField(max_length=200, blank=True)
    check_in_time = models.CharField(max_length=80, blank=True)
    check_out_time = models.CharField(max_length=80, blank=True)
    parking_info = models.CharField(max_length=160, blank=True)
    wifi_info = models.CharField(max_length=160, blank=True)
    dining_info = models.CharField(max_length=160, blank=True)
    ideal_for = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# =======================
class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    hero_image = models.ImageField(upload_to="restaurant/hero/", blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="gallery_images"
    )
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="restaurant/gallery/")
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title or "Gallery Image"


class SpecialDish(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="special_dishes"
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="restaurant/dishes/")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.name


class RestaurantOffer(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="offers"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title


class ContactSubmission(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("reviewed", "Reviewed"),
        ("resolved", "Resolved"),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    emailed_at = models.DateTimeField(blank=True, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
class HomeWelcomeVideo(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='home/videos/')
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SiteContent(models.Model):
    home_intro_title = models.CharField(max_length=200, default="Welcome to Sirupata R-Star")
    home_intro_body = models.TextField(
        default=(
            "A premium eco farm stay combined with modern hotel luxury. Relax, dine, and stay in harmony "
            "with nature. Discover our hilltop resort, woven into the fabric of a working farm ecosystem."
        )
    )
    home_intro_cta_label = models.CharField(max_length=80, default="Learn More About Us")
    home_intro_cta_url = models.CharField(max_length=200, default="/about/")
    rooms_hero_title = models.CharField(
        max_length=220,
        default="Rooms designed for comfort, calm, and a memorable night away.",
    )
    rooms_hero_body = models.TextField(
        default=(
            "Each stay option at Sirupata is shaped around a slightly different mood, from greener farmhouse calm "
            "to more polished suite comfort. Browse the collection, compare the atmosphere, and choose the room "
            "that fits your kind of escape."
        )
    )

    about_hero_title = models.CharField(max_length=220, default="Nature-led stays with the comfort of a modern retreat.")
    about_hero_body = models.TextField(
        default=(
            "Set around Butwal with easy access to Lumbini, Palpa routes, the airport, and the border corridor, "
            "Sirupata is designed for guests who want more than a standard overnight stop. It brings together "
            "the calm of a farm-led setting and the ease of a comfortable hotel stay, so the experience can feel "
            "both practical and restorative."
        )
    )
    about_highlight_title = models.CharField(max_length=120, default="Farm calm, hotel comfort")
    about_highlight_body = models.TextField(
        default="Fresh surroundings, warm hospitality, and a stay style that feels both restful and welcoming."
    )
    about_story_title = models.CharField(max_length=160, default="The Story Behind The Stay")
    about_story_body = models.TextField(
        default=(
            "Sirupata grew from a simple but useful idea for this area: many guests are traveling for mixed reasons. "
            "Some are passing through Butwal. Some are visiting family. Some want a quieter base before heading toward "
            "Lumbini, Palpa, or nearby routes. Others simply want a greener, slower setting for a short escape. "
            "The property is shaped to support all of those rhythms without feeling cold, hurried, or overly formal."
        )
    )
    about_expectation_title = models.CharField(max_length=160, default="What Guests Can Expect")
    about_expectation_1_title = models.CharField(max_length=120, default="Quiet with character")
    about_expectation_1_body = models.TextField(
        default="A stay environment that feels open, peaceful, and personal instead of anonymous or strictly businesslike."
    )
    about_expectation_2_title = models.CharField(max_length=120, default="Comfort that still feels local")
    about_expectation_2_body = models.TextField(
        default="Modern essentials paired with greenery, local warmth, and a stronger sense of place than a typical city hotel."
    )
    about_expectation_3_title = models.CharField(max_length=120, default="Flexible for real travel needs")
    about_expectation_3_body = models.TextField(
        default="Useful for stopovers, family visits, small gatherings, scenic stays, and food-led weekends without changing its core identity."
    )
    about_locations_title = models.CharField(max_length=160, default="Well placed for local travel")
    about_locations_intro = models.TextField(
        default=(
            "Sirupata is close enough to key routes and destinations to stay convenient, while still feeling separate "
            "from the pace and noise of the everyday city."
        )
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Content"
        verbose_name_plural = "Site Content"

    def __str__(self):
        return "Site Content"


class AboutLocation(models.Model):
    ICON_CHOICES = [
        ("city", "City"),
        ("mountain-city", "Mountain City"),
        ("landmark", "Landmark"),
        ("road", "Road"),
        ("plane-departure", "Airport"),
        ("calendar-check", "Events"),
    ]

    title = models.CharField(max_length=120)
    distance = models.CharField(max_length=40, blank=True)
    travel_time = models.CharField(max_length=60, blank=True)
    description = models.TextField()
    icon = models.CharField(max_length=40, choices=ICON_CHOICES, default="city")
    sort_order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "title"]
        verbose_name = "About Location"
        verbose_name_plural = "About Locations"

    def __str__(self):
        return self.title

class Review(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user_name = models.CharField(max_length=100, verbose_name="Your Name")
    user_email = models.EmailField(blank=True, null=True, verbose_name="Your Email (optional)")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Rating"
    )
    review_title = models.CharField(max_length=200, blank=True, verbose_name="Review Title")
    review_text = models.TextField(verbose_name="Your Review")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='approved')  # Default to approved for fake reviews
    is_featured = models.BooleanField(default=False, verbose_name="Featured Review")
    sentiment_score = models.FloatField(default=0.0, verbose_name="Sentiment Score", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
    
    def __str__(self):
        return f"{self.user_name} - {self.rating} Stars"
    
    def save(self, *args, **kwargs):
        if self.review_text:
            self.sentiment_score = compute_review_sentiment(self.review_text, self.rating)
        super().save(*args, **kwargs)
    
    def get_sentiment_label(self):
        return get_sentiment_label(self.sentiment_score)
