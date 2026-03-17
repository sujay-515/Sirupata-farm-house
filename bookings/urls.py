from django.urls import path
from .views import booking_form

app_name = "bookings"

urlpatterns = [
    path("", booking_form, name="booking_form"),
]
