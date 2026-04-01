from django.core.management.base import BaseCommand
from core.models import Review
from textblob import TextBlob

class Command(BaseCommand):
    help = 'Compute sentiment scores for all reviews'

    def handle(self, *args, **options):
        reviews = Review.objects.all()
        for review in reviews:
            if review.review_text:
                blob = TextBlob(review.review_text)
                text_sentiment = blob.sentiment.polarity
                rating_normalized = (review.rating - 3) / 2
                review.sentiment_score = (text_sentiment + rating_normalized) / 2
                review.save(update_fields=['sentiment_score'])
                self.stdout.write(f'Updated {review.user_name}: {review.sentiment_score}')
        self.stdout.write('Sentiment computation completed.')