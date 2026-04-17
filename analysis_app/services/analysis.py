"""
Analysis service - computes all statistics and chart data.
"""
import json
from collections import Counter
from .data_loader import get_dataframe


def get_summary_stats() -> dict:
    df = get_dataframe()
    movies = df[df['type'] == 'Movie']
    tv = df[df['type'] == 'TV Show']

    top_country = (
        df[df['country'] != '']['country']
        .value_counts().index[0]
        if not df[df['country'] != ''].empty else 'N/A'
    )

    all_genres = []
    for g in df['listed_in']:
        all_genres.extend([x.strip() for x in g.split(',') if x.strip()])
    top_genre = Counter(all_genres).most_common(1)[0][0] if all_genres else 'N/A'

    return {
        'total_titles': len(df),
        'total_movies': len(movies),
        'total_tv_shows': len(tv),
        'top_country': top_country,
        'most_popular_genre': top_genre,
    }


def get_type_distribution() -> dict:
    df = get_dataframe()
    counts = df['type'].value_counts()
    return {
        'labels': counts.index.tolist(),
        'values': counts.values.tolist(),
    }


def get_content_by_year() -> dict:
    df = get_dataframe()
    df_valid = df[(df['release_year'] > 1990) & (df['release_year'] <= 2022)]
    grouped = df_valid.groupby(['release_year', 'type']).size().unstack(fill_value=0)

    years = sorted(grouped.index.tolist())
    movies = [int(grouped.loc[y, 'Movie']) if 'Movie' in grouped.columns else 0 for y in years]
    tv = [int(grouped.loc[y, 'TV Show']) if 'TV Show' in grouped.columns else 0 for y in years]

    return {'years': years, 'movies': movies, 'tv_shows': tv}


def get_top_countries(n: int = 10) -> dict:
    df = get_dataframe()
    countries = df[df['country'] != '']['country'].value_counts().head(n)
    return {
        'labels': countries.index.tolist(),
        'values': countries.values.tolist(),
    }


def get_top_genres(n: int = 10) -> dict:
    df = get_dataframe()
    all_genres: list = []
    for g in df['listed_in']:
        all_genres.extend([x.strip() for x in g.split(',') if x.strip()])
    counts = Counter(all_genres).most_common(n)
    return {
        'labels': [c[0] for c in counts],
        'values': [c[1] for c in counts],
    }


def get_ratings_distribution() -> dict:
    df = get_dataframe()
    ratings = df[df['rating'] != '']['rating'].value_counts()
    return {
        'labels': ratings.index.tolist(),
        'values': ratings.values.tolist(),
    }


def get_top_directors(n: int = 10) -> dict:
    df = get_dataframe()
    directors = df[df['director'] != '']['director'].value_counts().head(n)
    return {
        'labels': directors.index.tolist(),
        'values': directors.values.tolist(),
    }


def get_duration_distribution() -> dict:
    df = get_dataframe()
    movies = df[(df['type'] == 'Movie') & df['duration_value'].notna()]
    bins = list(range(60, 200, 15))
    labels = [f'{b}-{b+15}' for b in bins[:-1]]
    counts = []
    for i in range(len(bins) - 1):
        cnt = int(((movies['duration_value'] >= bins[i]) & (movies['duration_value'] < bins[i+1])).sum())
        counts.append(cnt)
    return {'labels': labels, 'values': counts}


def get_monthly_additions() -> dict:
    df = get_dataframe()
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_valid = df[df['month_added'].notna()]
    monthly = df_valid['month_added'].value_counts().sort_index()
    values = [int(monthly.get(i, 0)) for i in range(1, 13)]
    return {'labels': month_names, 'values': values}


def get_all_chart_data() -> dict:
    return {
        'type_distribution': get_type_distribution(),
        'content_by_year': get_content_by_year(),
        'top_countries': get_top_countries(),
        'top_genres': get_top_genres(),
        'ratings_distribution': get_ratings_distribution(),
        'top_directors': get_top_directors(),
        'duration_distribution': get_duration_distribution(),
        'monthly_additions': get_monthly_additions(),
    }
