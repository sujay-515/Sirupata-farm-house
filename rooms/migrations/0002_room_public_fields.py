from django.db import migrations, models


def seed_default_rooms(apps, schema_editor):
    Room = apps.get_model("rooms", "Room")

    defaults = [
        {
            "name": "Deluxe Room",
            "price": 4500,
            "description": "Comfortable and spacious room with modern amenities and scenic mountain views.",
            "image": "core/sections/hill1.jpg",
            "capacity": "1-2 guests",
            "amenities": "King Bed\nFree Wi-Fi\nBreakfast\nMountain View",
            "sort_order": 1,
            "is_available": True,
        },
        {
            "name": "Luxury Suite",
            "price": 9000,
            "description": "Premium suite with panoramic views, separate living area, and luxury amenities.",
            "image": "core/sections/hill3.jpg",
            "capacity": "2-4 guests",
            "amenities": "Living Area\nFree Wi-Fi\nBathtub\nPanoramic View\nMini Bar",
            "sort_order": 2,
            "is_available": True,
        },
        {
            "name": "Farmhouse Suite",
            "price": 7500,
            "description": "Experience the charm of farmhouse living with garden views and private balcony access.",
            "image": "core/sections/farm1.jpg",
            "capacity": "2-4 guests",
            "amenities": "Garden View\nPrivate Balcony\nFree Wi-Fi\nBreakfast",
            "sort_order": 3,
            "is_available": True,
        },
    ]

    for data in defaults:
        Room.objects.update_or_create(name=data["name"], defaults=data)


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="amenities",
            field=models.TextField(blank=True, help_text="Enter one amenity per line or separate them with commas."),
        ),
        migrations.AddField(
            model_name="room",
            name="capacity",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="room",
            name="image",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="room",
            name="sort_order",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.RunPython(seed_default_rooms, migrations.RunPython.noop),
    ]
