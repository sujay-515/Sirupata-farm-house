from django.db import migrations


def seed_home_video_and_reviews(apps, schema_editor):
    HomeWelcomeVideo = apps.get_model("core", "HomeWelcomeVideo")
    Review = apps.get_model("core", "Review")

    HomeWelcomeVideo.objects.get_or_create(
        title="Welcome to Sirupata",
        defaults={
            "video": "home/videos/WhatsApp_Video_2026-01-30_at_8.56.26_PM.mp4",
            "is_active": True,
        },
    )

    reviews = [
        {
            "user_name": "Aarav Sharma",
            "rating": 5,
            "review_title": "Peaceful and welcoming",
            "review_text": "A calm place with warm service, fresh food, and a beautiful farmhouse feeling. We really enjoyed the quiet surroundings.",
            "sentiment_score": 0.95,
        },
        {
            "user_name": "Sita Gurung",
            "rating": 5,
            "review_title": "Beautiful family stay",
            "review_text": "The rooms were comfortable and the staff made everything easy for our family. The farm setting felt relaxing and memorable.",
            "sentiment_score": 0.92,
        },
        {
            "user_name": "Bikash Thapa",
            "rating": 4,
            "review_title": "Great food and location",
            "review_text": "The restaurant food was fresh and the location was convenient while still feeling away from the busy city.",
            "sentiment_score": 0.82,
        },
    ]

    for review in reviews:
        Review.objects.get_or_create(
            user_name=review["user_name"],
            review_title=review["review_title"],
            defaults={
                "user_email": "",
                "rating": review["rating"],
                "review_text": review["review_text"],
                "status": "approved",
                "is_featured": False,
                "sentiment_score": review["sentiment_score"],
            },
        )


def unseed_home_video_and_reviews(apps, schema_editor):
    HomeWelcomeVideo = apps.get_model("core", "HomeWelcomeVideo")
    Review = apps.get_model("core", "Review")

    HomeWelcomeVideo.objects.filter(title="Welcome to Sirupata").delete()
    Review.objects.filter(
        user_name__in=["Aarav Sharma", "Sita Gurung", "Bikash Thapa"],
        review_title__in=[
            "Peaceful and welcoming",
            "Beautiful family stay",
            "Great food and location",
        ],
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0019_contact_submission_and_restaurant_sorting"),
    ]

    operations = [
        migrations.RunPython(seed_home_video_and_reviews, unseed_home_video_and_reviews),
    ]
