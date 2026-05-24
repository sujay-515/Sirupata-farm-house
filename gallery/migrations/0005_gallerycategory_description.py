from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gallery", "0004_single_featured_per_hotel"),
    ]

    operations = [
        migrations.AddField(
            model_name="gallerycategory",
            name="description",
            field=models.TextField(blank=True),
        ),
    ]
