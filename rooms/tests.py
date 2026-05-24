from django.test import TestCase
from django.urls import reverse

from rooms.models import Room


class RoomPageTests(TestCase):
    def test_rooms_page_loads_with_admin_room(self):
        Room.objects.create(
            name="Deluxe Room",
            price=4500,
            description="A comfortable room",
            capacity="1-2 guests",
            amenities="Wi-Fi\nBreakfast",
            sort_order=1,
            is_available=True,
        )
        response = self.client.get(reverse("rooms:rooms"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Deluxe Room")
