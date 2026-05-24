from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_sync_index_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homewelcomevideo",
            name="video",
            field=models.FileField(upload_to="home/videos/"),
        ),
    ]
