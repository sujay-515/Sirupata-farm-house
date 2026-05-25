import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.models import HomeWelcomeVideo, Review
from gallery.models import GalleryCategory, GalleryImage


class Command(BaseCommand):
    help = "Seed demo content needed for a fresh Docker checkout."

    def handle(self, *args, **options):
        self.seed_admin()
        self.seed_home_video()
        self.seed_reviews()
        self.seed_gallery()
        self.stdout.write(self.style.SUCCESS("Demo content is ready."))

    def seed_admin(self):
        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin12345")
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write("Created admin user.")

    def seed_home_video(self):
        HomeWelcomeVideo.objects.update_or_create(
            title="Welcome to Sirupata",
            defaults={
                "video": "home/videos/WhatsApp_Video_2026-01-30_at_8.56.26_PM.mp4",
                "is_active": True,
            },
        )

    def seed_reviews(self):
        reviews = [
            {
                "user_name": "Aarav Sharma",
                "rating": 5,
                "review_title": "Peaceful and welcoming",
                "review_text": "A calm place with warm service, fresh food, and a beautiful farmhouse feeling. We really enjoyed the quiet surroundings.",
                "sentiment_score": 1.0,
            },
            {
                "user_name": "Sita Gurung",
                "rating": 5,
                "review_title": "Beautiful family stay",
                "review_text": "The rooms were comfortable and the staff made everything easy for our family. The farm setting felt relaxing and memorable.",
                "sentiment_score": 0.99,
            },
            {
                "user_name": "Bikash Thapa",
                "rating": 4,
                "review_title": "Great food and location",
                "review_text": "The restaurant food was fresh and the location was convenient while still feeling away from the busy city.",
                "sentiment_score": 0.98,
            },
        ]

        for review in reviews:
            obj, _ = Review.objects.update_or_create(
                user_name=review["user_name"],
                review_title=review["review_title"],
                defaults={
                    "user_email": "",
                    "rating": review["rating"],
                    "review_text": review["review_text"],
                    "status": "approved",
                    "is_featured": True,
                    "sentiment_score": review["sentiment_score"],
                },
            )
            Review.objects.filter(pk=obj.pk).update(sentiment_score=review["sentiment_score"])

    def seed_gallery(self):
        category, _ = GalleryCategory.objects.update_or_create(
            name="Sirupata Farm House",
            defaults={
                "description": "A glimpse of the farmhouse surroundings, gatherings, and guest spaces.",
            },
        )

        images = [
            {
                "title": "Farm House View",
                "image": "gallery/sirupata.jpg",
                "is_featured": True,
                "sort_order": 1,
            },
            {
                "title": "Event Space",
                "image": "gallery/event2.jpg",
                "is_featured": False,
                "sort_order": 2,
            },
        ]

        for image in images:
            GalleryImage.objects.update_or_create(
                category=category,
                title=image["title"],
                defaults={
                    "image": image["image"],
                    "is_featured": image["is_featured"],
                    "sort_order": image["sort_order"],
                },
            )
