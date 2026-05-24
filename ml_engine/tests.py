from django.test import SimpleTestCase, TestCase

from core.models import Booking
from ml_engine.services.analytics import (
    get_booking_trend_data,
    get_room_booking_breakdown,
    get_room_popularity_map,
    get_stay_month_trend_data,
)
from ml_engine.services.recommendations import recommend_similar_items
from ml_engine.services.sentiment import (
    compute_review_sentiment,
    get_sentiment_label,
)


class SentimentServiceTests(SimpleTestCase):
    def test_compute_review_sentiment_uses_text_and_rating(self):
        score = compute_review_sentiment("Wonderful peaceful stay", 5)
        self.assertGreater(score, 0.5)

    def test_get_sentiment_label_matches_thresholds(self):
        self.assertEqual(get_sentiment_label(0.3), "Loved it! 😊")
        self.assertEqual(get_sentiment_label(-0.3), "Not great")
        self.assertEqual(get_sentiment_label(0.0), "It was okay")


class RecommendationServiceTests(SimpleTestCase):
    def test_recommend_similar_items_returns_related_rooms(self):
        items = [
            {"name": "Deluxe", "description": "garden view breakfast cozy wooden room"},
            {"name": "Family", "description": "large family garden breakfast wooden room"},
            {"name": "Hill", "description": "mountain panorama quiet private balcony"},
        ]
        recommendations = recommend_similar_items(items, seed_name="Deluxe", limit=2)
        self.assertEqual(recommendations[0]["name"], "Family")


class AnalyticsServiceTests(TestCase):
    def setUp(self):
        Booking.objects.create(
            name="Guest 1",
            checkin="2030-01-10",
            checkout="2030-01-11",
            guests="2",
            room="Deluxe",
            status="new",
            phone="123",
            email="guest1@example.com",
        )
        Booking.objects.create(
            name="Guest 2",
            checkin="2030-01-12",
            checkout="2030-01-13",
            guests="2",
            room="Deluxe",
            status="confirmed",
            phone="456",
            email="guest2@example.com",
        )
        Booking.objects.create(
            name="Guest 3",
            checkin="2030-01-14",
            checkout="2030-01-15",
            guests="2",
            room="Hill View",
            status="cancelled",
            phone="789",
            email="guest3@example.com",
        )

    def test_room_popularity_map_counts_bookings(self):
        popularity = get_room_popularity_map()
        self.assertEqual(popularity["Deluxe"], 2)

    def test_room_booking_breakdown_excludes_cancelled(self):
        breakdown = get_room_booking_breakdown(top_n=8)
        self.assertEqual(breakdown["labels"], ["Deluxe"])
        self.assertEqual(breakdown["data"], [2])

    def test_booking_trend_data_returns_period_length(self):
        chart = get_booking_trend_data(period=3)
        self.assertEqual(len(chart["labels"]), 3)
        self.assertEqual(len(chart["data"]), 3)

    def test_stay_month_trend_uses_checkin_months_and_skips_cancelled(self):
        stay_trend = get_stay_month_trend_data()
        self.assertEqual(stay_trend["data"][0], 2)
        self.assertEqual(stay_trend["data"][11], 0)
        self.assertEqual(stay_trend["peak_month_label"], "Jan")
