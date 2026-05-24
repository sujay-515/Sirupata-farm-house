from django.db import migrations, models


def backfill_hotel_gallery_links(apps, schema_editor):
    GalleryImage = apps.get_model("gallery", "GalleryImage")
    GalleryCategory = apps.get_model("gallery", "GalleryCategory")
    Hotel = apps.get_model("core", "Hotel")

    for hotel in Hotel.objects.all():
        category = GalleryCategory.objects.filter(name__iexact=hotel.name).first()
        if category:
            GalleryImage.objects.filter(category=category, hotel__isnull=True).update(hotel=hotel)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_booking_status"),
        ("gallery", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="galleryimage",
            name="hotel",
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE, related_name="gallery_images", to="core.hotel"),
        ),
        migrations.RunPython(backfill_hotel_gallery_links, migrations.RunPython.noop),
    ]
