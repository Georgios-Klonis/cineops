
import csv
import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv, find_dotenv
import sqlalchemy as sa

load_dotenv(find_dotenv())

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError('DATABASE_URL not found')

ENGINE = sa.create_engine(DATABASE_URL, future=True)
PROCESSED_DIR = Path(__file__).resolve().parent / 'processed'


def _parse_date(value: str | None):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None


def _parse_float(value: str | None):
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def read_genres():
    path = PROCESSED_DIR / 'tmdb_genres_clean.csv'
    if not path.exists():
        raise FileNotFoundError(f'Genres CSV not found: {path}')

    with path.open(newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            yield {
                'id': int(row['id']),
                'name': row['name'],
            }


def read_movies():
    path = PROCESSED_DIR / 'tmdb_movies_clean.csv'
    if not path.exists():
        raise FileNotFoundError(f'Movies CSV not found: {path}')

    with path.open(newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            genre_ids = row['genre_ids']
            genre_ids_list = json.loads(genre_ids) if genre_ids else []

            yield {
                'tmdb_id': int(row['tmdb_id']),
                'title': row['title'],
                'overview': row['overview'] or None,
                'release_date': _parse_date(row['release_date']),
                'runtime': _parse_float(row['runtime']),
                'poster_url': row['poster_url'] or None,
                'genre_ids': genre_ids_list,
            }


def load_processed() -> None:
    metadata = sa.MetaData()
    metadata.reflect(bind=ENGINE, only=['genres', 'movies'])
    genres_table = metadata.tables['genres']
    movies_table = metadata.tables['movies']

    genres = list(read_genres())
    movies = list(read_movies())

    with ENGINE.begin() as conn:
        conn.execute(sa.text('TRUNCATE TABLE user_favorites, list_items, reviews, lists, movies, genres RESTART IDENTITY CASCADE'))

        if genres:
            conn.execute(genres_table.insert(), genres)
        if movies:
            conn.execute(movies_table.insert(), movies)

    with ENGINE.connect() as conn:
        genre_count = conn.execute(sa.text('SELECT COUNT(*) FROM genres')).scalar_one()
        movie_count = conn.execute(sa.text('SELECT COUNT(*) FROM movies')).scalar_one()

    print(f'Loaded {genre_count} genres and {movie_count} movies.')


def main() -> None:
    load_processed()


if __name__ == '__main__':
    main()
