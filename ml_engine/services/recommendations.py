import logging

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


logger = logging.getLogger(__name__)


def recommend_similar_items(items, seed_name=None, *, text_key="description", name_key="name", limit=3):
    if len(items) < 2:
        return []

    descriptions = [item.get(text_key, "") for item in items]
    if not any(descriptions):
        return []

    try:
        tfidf = TfidfVectorizer().fit_transform(descriptions)
        similarity_matrix = cosine_similarity(tfidf)
    except Exception:
        logger.exception("Failed to build similarity matrix for recommendations.")
        return []

    if seed_name:
        seed_idx = next((idx for idx, item in enumerate(items) if item.get(name_key) == seed_name), 0)
    else:
        seed_idx = 0

    ranked = [
        (idx, score)
        for idx, score in enumerate(similarity_matrix[seed_idx])
        if idx != seed_idx
    ]
    ranked.sort(key=lambda item: item[1], reverse=True)
    return [items[idx] for idx, _ in ranked[:limit]]
