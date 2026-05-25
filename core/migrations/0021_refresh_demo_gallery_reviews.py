from django.db import migrations


def refresh_demo_content(apps, schema_editor):
    GalleryCategory = apps.get_model("gallery", "GalleryCategory")
    GalleryImage = apps.get_model("gallery", "GalleryImage")
    HomeWelcomeVideo = apps.get_model("core", "HomeWelcomeVideo")
    Review = apps.get_model("core", "Review")

    HomeWelcomeVideo.objects.update_or_create(
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

    category, _ = GalleryCategory.objects.update_or_create(
        name="Sirupata Farm House",
        defaults={
            "description": "A glimpse of the farmhouse surroundings, gatherings, and guest spaces.",
        },
    )

    gallery_images = [
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

    for image in gallery_images:
        GalleryImage.objects.update_or_create(
            category=category,
            title=image["title"],
            defaults={
                "image": image["image"],
                "is_featured": image["is_featured"],
                "sort_order": image["sort_order"],
            },
        )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0020_seed_home_video_reviews"),
        ("gallery", "0005_gallerycategory_description"),
    ]

    operations = [
        migrations.RunPython(refresh_demo_content, noop_reverse),
    ]
