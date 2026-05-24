from textblob import TextBlob


POSITIVE_THRESHOLD = 0.1
NEGATIVE_THRESHOLD = -0.1


def normalize_rating_to_sentiment(rating):
    return (rating - 3) / 2


def compute_review_sentiment(review_text, rating):
    rating_normalized = normalize_rating_to_sentiment(rating)
    if not review_text:
        return rating_normalized

    text_sentiment = TextBlob(review_text).sentiment.polarity
    return (text_sentiment + rating_normalized) / 2


def get_sentiment_label(score):
    if score > POSITIVE_THRESHOLD:
        return "Loved it! 😊"
    if score < NEGATIVE_THRESHOLD:
        return "Not great"
    return "It was okay"
