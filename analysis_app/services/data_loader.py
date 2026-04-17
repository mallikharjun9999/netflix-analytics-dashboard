"""
Data loader service - loads and caches the Netflix dataset.
"""
import os
import pandas as pd
from django.conf import settings


_df_cache = None


def get_dataframe() -> pd.DataFrame:
    """Load and cache the Netflix dataframe."""
    global _df_cache
    if _df_cache is None:
        _df_cache = _load_and_clean()
    return _df_cache


def _load_and_clean() -> pd.DataFrame:
    path = settings.DATASET_PATH
    df = pd.read_csv(path)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Clean string columns
    for col in ['title', 'director', 'cast', 'country', 'rating', 'listed_in', 'description', 'type']:
        if col in df.columns:
            df[col] = df[col].fillna('').str.strip()

    # Parse date_added
    if 'date_added' in df.columns:
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
        df['year_added'] = df['date_added'].dt.year
        df['month_added'] = df['date_added'].dt.month

    # Ensure release_year is int
    if 'release_year' in df.columns:
        df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce').fillna(0).astype(int)

    # Parse duration
    if 'duration' in df.columns:
        df['duration_value'] = df['duration'].str.extract(r'(\d+)').astype(float)
        df['duration_unit'] = df['duration'].str.extract(r'(\D+)').fillna('').apply(
            lambda x: x[0].strip().lower() if x[0] else ''
        )

    return df


def reload_dataframe():
    """Force reload from disk."""
    global _df_cache
    _df_cache = None
    return get_dataframe()
