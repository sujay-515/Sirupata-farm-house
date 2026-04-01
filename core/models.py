from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import datetime
from textblob import TextBlob


# =========================
# BOOKING
# =========================
class Booking(models.Model):
    ROOM_CHOICES = [
        ("Farmhouse Suite", "Farmhouse Suite"),
        ("Deluxe Room", "Deluxe Room"),
        ("Luxury Suite", "Luxury Suite"),
    ]

    name = models.CharField(max_length=100, blank=True, null=True)
    checkin = models.DateField()
    checkout = models.DateField()
    guests = models.CharField(max_length=20)
    room = models.CharField(max_length=50, choices=ROOM_CHOICES, db_index=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def clean(self):
        if self.checkin < datetime.date.today():
            raise ValidationError("Check-in date cannot be in the past.")
        if self.checkout < datetime.date.today():
            raise ValidationError("Check-out date cannot be in the past.")
        if self.checkout <= self.checkin:
            raise ValidationError("Checkout date must be after check-in date")

    def __str__(self):
        return f"{self.room} | {self.checkin}"


# =========================
# HOTEL
# =========================
class Hotel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    hero_image = models.ImageField(upload_to="hotel/hero/")
    location = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# =======================
class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    hero_image = models.ImageField(upload_to="restaurant/hero/")
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

    def __str__(self):
        return self.title
    
class HomeWelcomeVideo(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='media/welcome.mp4')
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

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
            blob = TextBlob(self.review_text)
            text_sentiment = blob.sentiment.polarity
            # Combine text sentiment with rating (normalized to -1 to 1)
            rating_normalized = (self.rating - 3) / 2  # 1-> -1, 5->1
            self.sentiment_score = (text_sentiment + rating_normalized) / 2
        super().save(*args, **kwargs)
    
    def get_sentiment_label(self):
        if self.sentiment_score > 0.1:
            return "Loved it! 😊"
        elif self.sentiment_score < -0.1:
            return "Not great"
        else:
            return "It was okay"