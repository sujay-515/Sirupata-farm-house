from django.urls import path
from .views import booking_form, booking_success

app_name = "bookings"

urlpatterns = [
    path("", booking_form, name="booking_form"),
    path("success/", booking_success, name="booking_success"),
]
