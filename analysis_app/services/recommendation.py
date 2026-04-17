"""
Recommendation service using TF-IDF cosine similarity.
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .data_loader import get_dataframe

_model_cache = None


def _build_model():
    global _model_cache
    if _model_cache is not None:
        return _model_cache

    df = get_dataframe().copy()
    df = df.reset_index(drop=True)

    # Build feature text: genres + director + cast
    def build_soup(row):
        parts = []
        if row.get('listed_in'):
            genres = ' '.join(row['listed_in'].replace(',', ' ').split())
            parts.append(genres)
        if row.get('director'):
            parts.append(row['director'].replace(' ', '_'))
        if row.get('cast'):
            actors = ' '.join([a.strip().replace(' ', '_') for a in row['cast'].split(',')[:5]])
            parts.append(actors)
        if row.get('description'):
            parts.append(row['description'])
        return ' '.join(parts)

    df['soup'] = df.apply(build_soup, axis=1)

    tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
    tfidf_matrix = tfidf.fit_transform(df['soup'])

    _model_cache = {
        'df': df,
        'tfidf_matrix': tfidf_matrix,
    }
    return _model_cache


def get_recommendations(title: str, n: int = 6) -> list:
    """Return top-n similar titles."""
    try:
        model = _build_model()
        df = model['df']
        matrix = model['tfidf_matrix']

        # Find matching title (case-insensitive)
        mask = df['title'].str.lower() == title.lower()
        if not mask.any():
            mask = df['title'].str.lower().str.contains(title.lower(), na=False)

        if not mask.any():
            return []

        idx = mask.idxmax()
        sim_scores = cosine_similarity(matrix[idx], matrix).flatten()
        sim_indices = sim_scores.argsort()[::-1][1:n+10]

        results = []
        seen_titles = set()
        for i in sim_indices:
            row = df.iloc[i]
            t = row['title']
            if t not in seen_titles and len(results) < n:
                seen_titles.add(t)
                results.append({
                    'title': t,
                    'type': row.get('type', ''),
                    'listed_in': row.get('listed_in', ''),
                    'release_year': int(row.get('release_year', 0)),
                    'rating': row.get('rating', ''),
                    'score': round(float(sim_scores[i]), 3),
                })
        return results
    except Exception as e:
        return []


def invalidate_cache():
    global _model_cache
    _model_cache = None
