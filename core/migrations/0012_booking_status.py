from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_alter_homewelcomevideo_video"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="status",
            field=models.CharField(
                choices=[
                    ("new", "New"),
                    ("confirmed", "Confirmed"),
                    ("checked_in", "Checked In"),
                    ("checked_out", "Checked Out"),
                    ("cancelled", "Cancelled"),
                ],
                db_index=True,
                default="new",
                max_length=20,
            ),
        ),
    ]
