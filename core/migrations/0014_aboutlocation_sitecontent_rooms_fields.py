from django.db import migrations, models


def seed_about_locations(apps, schema_editor):
    AboutLocation = apps.get_model("core", "AboutLocation")
    if AboutLocation.objects.exists():
        return

    AboutLocation.objects.bulk_create(
        [
            AboutLocation(
                title="Butwal Chauraha",
                distance="3.5 km",
                travel_time="About 6 min",
                description="Ideal for guests who want quick access to the city center while returning to a stay that feels calmer at the end of the day.",
                icon="city",
                sort_order=1,
            ),
            AboutLocation(
                title="Tansen / Rampur Palpa",
                distance="44 km",
                travel_time="About 1 hr 55 min",
                description="A scenic onward connection for hill drives, heritage outings, and guests extending their trip beyond the immediate city area.",
                icon="mountain-city",
                sort_order=2,
            ),
            AboutLocation(
                title="Lumbini",
                distance="38 km",
                travel_time="About 55 min",
                description="A practical base for cultural and spiritual visitors who want comfort and easy reach without staying right in the main pilgrimage zone.",
                icon="landmark",
                sort_order=3,
            ),
            AboutLocation(
                title="Sunauli Border",
                distance="22 km",
                travel_time="About 34 min",
                description="Useful for transit schedules, cross-border movement, and travelers looking for a smoother overnight stop before the next leg.",
                icon="road",
                sort_order=4,
            ),
            AboutLocation(
                title="Gautam Buddha Airport",
                distance="12 km",
                travel_time="About 29 min",
                description="Close enough to make arrivals, departures, and planned pickups easier for short stays and timed travel plans.",
                icon="plane-departure",
                sort_order=5,
            ),
            AboutLocation(
                title="Events & Gatherings",
                distance="Flexible setting",
                travel_time="Family-friendly",
                description="A relaxed setting for private functions, family gatherings, and smaller celebrations that benefit from a more personal atmosphere.",
                icon="calendar-check",
                sort_order=6,
            ),
        ]
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_sitecontent"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitecontent",
            name="rooms_hero_body",
            field=models.TextField(default="Each stay option at Sirupata is shaped around a slightly different mood, from greener farmhouse calm to more polished suite comfort. Browse the collection, compare the atmosphere, and choose the room that fits your kind of escape."),
        ),
        migrations.AddField(
            model_name="sitecontent",
            name="rooms_hero_title",
            field=models.CharField(default="Rooms designed for comfort, calm, and a memorable night away.", max_length=220),
        ),
        migrations.CreateModel(
            name="AboutLocation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("distance", models.CharField(blank=True, max_length=40)),
                ("travel_time", models.CharField(blank=True, max_length=60)),
                ("description", models.TextField()),
                ("icon", models.CharField(choices=[("city", "City"), ("mountain-city", "Mountain City"), ("landmark", "Landmark"), ("road", "Road"), ("plane-departure", "Airport"), ("calendar-check", "Events")], default="city", max_length=40)),
                ("sort_order", models.PositiveIntegerField(default=1)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "About Location",
                "verbose_name_plural": "About Locations",
                "ordering": ["sort_order", "title"],
            },
        ),
        migrations.RunPython(seed_about_locations, migrations.RunPython.noop),
    ]
