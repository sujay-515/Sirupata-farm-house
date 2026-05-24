from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0014_aboutlocation_sitecontent_rooms_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="hotel",
            name="check_in_time",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="hotel",
            name="check_out_time",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="hotel",
            name="dining_info",
            field=models.CharField(blank=True, max_length=160),
        ),
        migrations.AddField(
            model_name="hotel",
            name="ideal_for",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name="hotel",
            name="parking_info",
            field=models.CharField(blank=True, max_length=160),
        ),
        migrations.AddField(
            model_name="hotel",
            name="wifi_info",
            field=models.CharField(blank=True, max_length=160),
        ),
    ]
