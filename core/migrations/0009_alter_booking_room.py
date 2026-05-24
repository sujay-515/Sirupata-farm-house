from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_review_sentiment_score"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="room",
            field=models.CharField(db_index=True, max_length=100),
        ),
    ]
