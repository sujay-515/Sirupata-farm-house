from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0018_booking_email_tracking"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurantimage",
            name="sort_order",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="restaurantoffer",
            name="sort_order",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="specialdish",
            name="sort_order",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterModelOptions(
            name="restaurantimage",
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.AlterModelOptions(
            name="restaurantoffer",
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.AlterModelOptions(
            name="specialdish",
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.CreateModel(
            name="ContactSubmission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("subject", models.CharField(max_length=200)),
                ("message", models.TextField()),
                ("status", models.CharField(choices=[("new", "New"), ("reviewed", "Reviewed"), ("resolved", "Resolved")], default="new", max_length=20)),
                ("emailed_at", models.DateTimeField(blank=True, editable=False, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                "verbose_name": "Contact Submission",
                "verbose_name_plural": "Contact Submissions",
                "ordering": ["-created_at"],
            },
        ),
    ]
