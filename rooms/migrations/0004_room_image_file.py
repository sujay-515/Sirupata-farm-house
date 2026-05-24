from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0003_alter_room_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="image_file",
            field=models.ImageField(blank=True, upload_to="rooms/"),
        ),
    ]
