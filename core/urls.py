from django.urls import path
from . import views
from .views import restaurant_view

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path('submit-review/', views.submit_review, name='submit_review'),

    path("bookings/", views.booking_form, name="booking"),
    path("hotel/", views.hotel, name="hotel"),
    path('restaurant/', views.restaurant_view, name='restaurant'),
    path("contact/", views.contact, name="contact"),
]

