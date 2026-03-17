from django.contrib import admin
from .models import (
    Booking,
    Hotel,
    Restaurant,
    RestaurantImage,
    SpecialDish,
    RestaurantOffer,
    HomeWelcomeVideo,
)
from django.utils.html import format_html
from .models import Review
from .utils import send_review_status_notification
from django.utils import timezone
from django.contrib import messages
# =========================
# BOOKING ADMIN
# =========================
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "checkin",
        "checkout",
        "guests",
        "room",
        "phone",
        "email",
        "created_at",
    )
    list_filter = ("room", "checkin")
    search_fields = ("phone", "email", "room")


# =========================
# HOTEL ADMIN
# =========================
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "location")




@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
    list_display = ("restaurant", "title", "is_active")
    list_filter = ("is_active", "restaurant")


@admin.register(SpecialDish)
class SpecialDishAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "price", "is_active")
    list_filter = ("is_active", "restaurant")
    search_fields = ("name",)


@admin.register(RestaurantOffer)
class RestaurantOfferAdmin(admin.ModelAdmin):
    list_display = ("title", "restaurant", "price", "is_active")
    list_filter = ("is_active", "restaurant")

 

@admin.register(HomeWelcomeVideo)
class HomeWelcomeVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'uploaded_at')
    list_filter = ('is_active',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'rating_display', 'review_short', 'status', 'created_at']
    list_filter = ['rating', 'status', 'created_at']
    search_fields = ['user_name', 'review_text']
    list_editable = ['status']
    list_per_page = 20
    
    def rating_display(self, obj):
        return '⭐' * obj.rating
    rating_display.short_description = 'Rating'
    
    def review_short(self, obj):
        return obj.review_text[:50] + '...' if len(obj.review_text) > 50 else obj.review_text
    review_short.short_description = 'Review'