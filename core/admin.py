from django.contrib import admin
from .models import (
    Booking,
    AboutLocation,
    ContactSubmission,
    Hotel,
    Restaurant,
    RestaurantImage,
    SpecialDish,
    RestaurantOffer,
    HomeWelcomeVideo,
    SiteContent,
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
        "status",
        "name",
        "checkin",
        "checkout",
        "guests",
        "room",
        "phone",
        "email",
        "received_email_sent_at",
        "confirmed_email_sent_at",
        "created_at",
    )
    list_filter = ("status", "room", "checkin", "checkout", "created_at")
    search_fields = ("phone", "email", "room")
    list_editable = ("status",)
    actions = ("mark_confirmed", "mark_checked_in", "mark_checked_out", "mark_cancelled")
    readonly_fields = ("received_email_sent_at", "confirmed_email_sent_at", "created_at")
    fieldsets = (
        ("Guest Details", {
            "fields": ("name", "email", "phone"),
        }),
        ("Stay Details", {
            "fields": ("room", "guests", "checkin", "checkout", "status"),
        }),
        ("Notification History", {
            "fields": ("received_email_sent_at", "confirmed_email_sent_at", "created_at"),
        }),
    )

    @admin.action(description="Mark selected bookings as Confirmed")
    def mark_confirmed(self, request, queryset):
        updated = 0
        for booking in queryset.exclude(status="confirmed"):
            booking.status = "confirmed"
            booking.save()
            updated += 1
        self.message_user(request, f"{updated} booking(s) marked as confirmed.", level=messages.SUCCESS)

    @admin.action(description="Mark selected bookings as Checked In")
    def mark_checked_in(self, request, queryset):
        updated = queryset.exclude(status="checked_in").update(status="checked_in")
        self.message_user(request, f"{updated} booking(s) marked as checked in.", level=messages.SUCCESS)

    @admin.action(description="Mark selected bookings as Checked Out")
    def mark_checked_out(self, request, queryset):
        updated = queryset.exclude(status="checked_out").update(status="checked_out")
        self.message_user(request, f"{updated} booking(s) marked as checked out.", level=messages.SUCCESS)

    @admin.action(description="Mark selected bookings as Cancelled")
    def mark_cancelled(self, request, queryset):
        updated = queryset.exclude(status="cancelled").update(status="cancelled")
        self.message_user(request, f"{updated} booking(s) marked as cancelled.", level=messages.SUCCESS)


# =========================
# HOTEL ADMIN
# =========================
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "check_in_time", "check_out_time", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "location")
    fieldsets = (
        ("Core Details", {
            "fields": ("name", "description", "hero_image", "location", "is_active"),
        }),
        ("Practical Stay Details", {
            "fields": ("check_in_time", "check_out_time", "parking_info", "wifi_info", "dining_info", "ideal_for"),
        }),
    )




@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
    list_display = ("restaurant", "title", "sort_order", "is_active")
    list_filter = ("is_active", "restaurant")
    list_editable = ("sort_order", "is_active")
    ordering = ("restaurant", "sort_order", "id")


@admin.register(SpecialDish)
class SpecialDishAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "price", "sort_order", "is_active")
    list_filter = ("is_active", "restaurant")
    search_fields = ("name",)
    list_editable = ("sort_order", "is_active")
    ordering = ("restaurant", "sort_order", "id")


@admin.register(RestaurantOffer)
class RestaurantOfferAdmin(admin.ModelAdmin):
    list_display = ("title", "restaurant", "price", "sort_order", "is_active")
    list_filter = ("is_active", "restaurant")
    list_editable = ("sort_order", "is_active")
    ordering = ("restaurant", "sort_order", "id")

 

@admin.register(HomeWelcomeVideo)
class HomeWelcomeVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'uploaded_at')
    list_filter = ('is_active',)


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Homepage Intro", {
            "fields": ("home_intro_title", "home_intro_body", "home_intro_cta_label", "home_intro_cta_url"),
        }),
        ("Rooms Intro", {
            "fields": ("rooms_hero_title", "rooms_hero_body"),
        }),
        ("About Hero", {
            "fields": ("about_hero_title", "about_hero_body", "about_highlight_title", "about_highlight_body"),
        }),
        ("About Story", {
            "fields": ("about_story_title", "about_story_body"),
        }),
        ("Guest Expectations", {
            "fields": (
                "about_expectation_title",
                "about_expectation_1_title",
                "about_expectation_1_body",
                "about_expectation_2_title",
                "about_expectation_2_body",
                "about_expectation_3_title",
                "about_expectation_3_body",
            ),
        }),
        ("Location Intro", {
            "fields": ("about_locations_title", "about_locations_intro"),
        }),
    )

    def has_add_permission(self, request):
        return not SiteContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AboutLocation)
class AboutLocationAdmin(admin.ModelAdmin):
    list_display = ("title", "distance", "travel_time", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description")


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "email", "status", "emailed_at", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_editable = ("status",)
    readonly_fields = ("emailed_at", "created_at")

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
