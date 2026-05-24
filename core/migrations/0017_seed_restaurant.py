from django.db import migrations, models


def seed_default_restaurant(apps, schema_editor):
    Restaurant = apps.get_model("core", "Restaurant")
    if not Restaurant.objects.exists():
        Restaurant.objects.create(
            name="Sirupata Restaurant",
            description=(
                "A comfortable dining space for guests, families, and small gatherings, with a focus on warm service "
                "and dishes that fit the wider Sirupata experience."
            ),
            is_active=True,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0016_seed_hotel_and_gallery_ordering"),
    ]

    operations = [
        migrations.AlterField(
            model_name="restaurant",
            name="hero_image",
            field=models.ImageField(blank=True, upload_to="restaurant/hero/"),
        ),
        migrations.RunPython(seed_default_restaurant, migrations.RunPython.noop),
    ]
