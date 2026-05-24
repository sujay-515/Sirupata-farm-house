from django.core.management.base import BaseCommand
from core.models import Review

from ml_engine.services.sentiment import compute_review_sentiment

class Command(BaseCommand):
    help = 'Compute sentiment scores for all reviews'

    def handle(self, *args, **options):
        reviews = Review.objects.all()
        for review in reviews:
            if review.review_text:
                review.sentiment_score = compute_review_sentiment(review.review_text, review.rating)
                review.save(update_fields=['sentiment_score'])
                self.stdout.write(f'Updated {review.user_name}: {review.sentiment_score}')
        self.stdout.write('Sentiment computation completed.')
