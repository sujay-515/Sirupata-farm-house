from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gallery", "0002_galleryimage_hotel"),
    ]

    operations = [
        migrations.AddField(
            model_name="galleryimage",
            name="sort_order",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterModelOptions(
            name="galleryimage",
            options={"ordering": ["-is_featured", "sort_order", "-created_at"]},
        ),
    ]
