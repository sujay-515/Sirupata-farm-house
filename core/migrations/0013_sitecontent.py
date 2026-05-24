from django.db import migrations, models


def create_site_content(apps, schema_editor):
    SiteContent = apps.get_model("core", "SiteContent")
    if not SiteContent.objects.exists():
        SiteContent.objects.create()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_booking_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="SiteContent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("home_intro_title", models.CharField(default="Welcome to Sirupata R-Star", max_length=200)),
                ("home_intro_body", models.TextField(default="A premium eco farm stay combined with modern hotel luxury. Relax, dine, and stay in harmony with nature. Discover our hilltop resort, woven into the fabric of a working farm ecosystem.")),
                ("home_intro_cta_label", models.CharField(default="Learn More About Us", max_length=80)),
                ("home_intro_cta_url", models.CharField(default="/about/", max_length=200)),
                ("about_hero_title", models.CharField(default="Nature-led stays with the comfort of a modern retreat.", max_length=220)),
                ("about_hero_body", models.TextField(default="Set around Butwal with easy access to Lumbini, Palpa routes, the airport, and the border corridor, Sirupata is designed for guests who want more than a standard overnight stop. It brings together the calm of a farm-led setting and the ease of a comfortable hotel stay, so the experience can feel both practical and restorative.")),
                ("about_highlight_title", models.CharField(default="Farm calm, hotel comfort", max_length=120)),
                ("about_highlight_body", models.TextField(default="Fresh surroundings, warm hospitality, and a stay style that feels both restful and welcoming.")),
                ("about_story_title", models.CharField(default="The Story Behind The Stay", max_length=160)),
                ("about_story_body", models.TextField(default="Sirupata grew from a simple but useful idea for this area: many guests are traveling for mixed reasons. Some are passing through Butwal. Some are visiting family. Some want a quieter base before heading toward Lumbini, Palpa, or nearby routes. Others simply want a greener, slower setting for a short escape. The property is shaped to support all of those rhythms without feeling cold, hurried, or overly formal.")),
                ("about_expectation_title", models.CharField(default="What Guests Can Expect", max_length=160)),
                ("about_expectation_1_title", models.CharField(default="Quiet with character", max_length=120)),
                ("about_expectation_1_body", models.TextField(default="A stay environment that feels open, peaceful, and personal instead of anonymous or strictly businesslike.")),
                ("about_expectation_2_title", models.CharField(default="Comfort that still feels local", max_length=120)),
                ("about_expectation_2_body", models.TextField(default="Modern essentials paired with greenery, local warmth, and a stronger sense of place than a typical city hotel.")),
                ("about_expectation_3_title", models.CharField(default="Flexible for real travel needs", max_length=120)),
                ("about_expectation_3_body", models.TextField(default="Useful for stopovers, family visits, small gatherings, scenic stays, and food-led weekends without changing its core identity.")),
                ("about_locations_title", models.CharField(default="Well placed for local travel", max_length=160)),
                ("about_locations_intro", models.TextField(default="Sirupata is close enough to key routes and destinations to stay convenient, while still feeling separate from the pace and noise of the everyday city.")),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Site Content",
                "verbose_name_plural": "Site Content",
            },
        ),
        migrations.RunPython(create_site_content, migrations.RunPython.noop),
    ]
