from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_alter_booking_room"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="review",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="review",
            name="sentiment_score",
            field=models.FloatField(db_index=True, default=0.0, verbose_name="Sentiment Score"),
        ),
    ]
