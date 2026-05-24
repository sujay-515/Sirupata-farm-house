from django.db import migrations, models


def seed_default_hotel(apps, schema_editor):
    Hotel = apps.get_model("core", "Hotel")
    if not Hotel.objects.exists():
        Hotel.objects.create(
            name="Sirupata R-Star Hotel",
            description=(
                "A stay designed for comfort, easy access, and a more polished hospitality experience "
                "for guests visiting Butwal and nearby destinations."
            ),
            location="Butwal, Nepal",
            check_in_time="2:00 PM",
            check_out_time="12:00 PM",
            parking_info="Please confirm parking availability directly with the property.",
            wifi_info="Available for guest use.",
            dining_info="Restaurant access available as part of the wider Sirupata experience.",
            ideal_for="Family stays, stopovers, regional travel, and guests who want a more comfortable base.",
            is_active=True,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("gallery", "0002_galleryimage_hotel"),
        ("core", "0015_hotel_practical_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hotel",
            name="hero_image",
            field=models.ImageField(blank=True, upload_to="hotel/hero/"),
        ),
        migrations.RunPython(seed_default_hotel, migrations.RunPython.noop),
    ]
