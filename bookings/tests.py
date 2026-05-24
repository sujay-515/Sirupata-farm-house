from django.test import TestCase
from django.urls import reverse


class BookingRouteTests(TestCase):
    def test_bookings_app_routes_to_shared_booking_page(self):
        response = self.client.get(reverse("bookings:booking_form"))
        self.assertEqual(response.status_code, 200)
