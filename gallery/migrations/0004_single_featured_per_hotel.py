from django.db import migrations


def normalize_featured_images(apps, schema_editor):
    GalleryImage = apps.get_model("gallery", "GalleryImage")
    hotel_ids = (
        GalleryImage.objects.filter(hotel__isnull=False, is_featured=True)
        .values_list("hotel_id", flat=True)
        .distinct()
    )

    for hotel_id in hotel_ids:
        featured_images = list(
            GalleryImage.objects.filter(hotel_id=hotel_id, is_featured=True)
            .order_by("sort_order", "-created_at", "id")
        )
        for image in featured_images[1:]:
            image.is_featured = False
            image.save(update_fields=["is_featured"])


class Migration(migrations.Migration):

    dependencies = [
        ("gallery", "0003_galleryimage_sort_order"),
    ]

    operations = [
        migrations.RunPython(normalize_featured_images, migrations.RunPython.noop),
    ]
