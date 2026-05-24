import tempfile
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from core.models import Booking, ContactSubmission, HomeWelcomeVideo, Hotel, Restaurant, Review, SiteContent
from gallery.models import GalleryCategory, GalleryImage
from rooms.models import Room


TEST_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(
    MEDIA_ROOT=TEST_MEDIA_ROOT,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="noreply@example.com",
    SITE_NAME="Sirupata R Star",
)
class CoreFlowTests(TestCase):
    def setUp(self):
        self.room = Room.objects.create(
            name="Farmhouse Suite",
            price=7500,
            description="Room description",
            capacity="2-4 guests",
            amenities="Wi-Fi\nBreakfast",
            sort_order=1,
            is_available=True,
        )

    def test_homepage_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_homepage_renders_active_video(self):
        HomeWelcomeVideo.objects.create(
            title="Welcome",
            video=SimpleUploadedFile("welcome.mp4", b"video-content", content_type="video/mp4"),
            is_active=True,
        )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "video/mp4")

    def test_booking_form_submission_creates_booking(self):
        today = timezone.localdate()
        response = self.client.post(
            reverse("booking"),
            {
                "name": "Test Guest",
                "checkin": today + timedelta(days=1),
                "checkout": today + timedelta(days=2),
                "guests": "2",
                "room": self.room.name,
                "phone": "123456789",
                "email": "guest@example.com",
            },
        )
        self.assertRedirects(response, reverse("booking_success"))
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.first().status, "new")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("received your booking request", mail.outbox[0].subject.lower())
        self.assertEqual(Booking.objects.first().received_email_sent_at is not None, True)

    def test_booking_confirmation_sends_email_once(self):
        today = timezone.localdate()
        booking = Booking.objects.create(
            name="Test Guest",
            checkin=today + timedelta(days=1),
            checkout=today + timedelta(days=2),
            guests="2",
            room=self.room.name,
            phone="123456789",
            email="guest@example.com",
        )

        booking.status = "confirmed"
        booking.save()

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("booking is confirmed", mail.outbox[0].subject.lower())
        booking.refresh_from_db()
        self.assertIsNotNone(booking.confirmed_email_sent_at)

        booking.phone = "999999999"
        booking.save()
        self.assertEqual(len(mail.outbox), 1)

    def test_admin_dashboard_loads_for_superuser(self):
        user = get_user_model().objects.create_superuser("admin", "admin@example.com", "password123")
        self.client.force_login(user)
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)

    def test_hotel_page_uses_model_data(self):
        hotel = Hotel.objects.create(
            name="R-Asad Hotel",
            description="Hotel description",
            hero_image=SimpleUploadedFile("hotel.jpg", b"hotel-image", content_type="image/jpeg"),
            check_in_time="2:00 PM",
            check_out_time="12:00 PM",
            is_active=True,
        )
        category = GalleryCategory.objects.create(name=hotel.name)
        GalleryImage.objects.create(
            category=category,
            hotel=hotel,
            title="Lobby",
            image=SimpleUploadedFile("lobby.jpg", b"lobby-image", content_type="image/jpeg"),
        )
        response = self.client.get(reverse("hotel"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, hotel.name)
        self.assertContains(response, "2:00 PM")

    def test_restaurant_page_handles_missing_restaurant(self):
        response = self.client.get(reverse("restaurant"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Restaurant Coming Soon")

    def test_homepage_review_list_uses_admin_approved_reviews(self):
        Review.objects.create(
            user_name="Guest",
            rating=5,
            review_title="Great",
            review_text="Wonderful stay and service.",
            status="approved",
        )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Guest")

    def test_homepage_uses_admin_managed_intro_content(self):
        SiteContent.objects.create(
            home_intro_title="Custom Welcome",
            home_intro_body="Custom homepage copy for guests.",
            home_intro_cta_label="Explore More",
            home_intro_cta_url="/about/",
        )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Custom Welcome")
        self.assertContains(response, "Custom homepage copy for guests.")

    def test_about_page_uses_admin_managed_copy(self):
        SiteContent.objects.create(
            about_hero_title="Custom About Hero",
            about_hero_body="A more specific story about the property.",
            about_story_title="Custom Story",
            about_story_body="Custom long-form about copy.",
        )
        response = self.client.get(reverse("about"))
        self.assertContains(response, "Custom About Hero")
        self.assertContains(response, "Custom Story")

    def test_contact_form_saves_submission_and_sends_email(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Interested Guest",
                "email": "guest@example.com",
                "subject": "Event inquiry",
                "message": "I want to ask about a family event.",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactSubmission.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertContains(response, "saved successfully")
