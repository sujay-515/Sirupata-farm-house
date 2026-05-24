from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0017_seed_restaurant"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="confirmed_email_sent_at",
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="booking",
            name="received_email_sent_at",
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]
