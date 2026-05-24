from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0002_room_public_fields"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="room",
            options={"ordering": ("sort_order", "name")},
        ),
    ]
