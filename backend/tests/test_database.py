import sqlalchemy as sa
import pytest

from backend.db.session import engine
from backend.db.seeds.load_processed import load_processed


@pytest.fixture(scope="module", autouse=True)
def seed_once():
    """Ensure the database has the processed data before tests run."""
    load_processed()


@pytest.fixture
def table_counts():
    """Return a function that fetches genre/movie counts."""
    def _counts():
        with engine.connect() as conn:
            movies = conn.execute(sa.text("SELECT COUNT(*) FROM movies")).scalar_one()
            genres = conn.execute(sa.text("SELECT COUNT(*) FROM genres")).scalar_one()
        return movies, genres

    return _counts


def test_database_connectivity(table_counts):
    movies, genres = table_counts()
    assert movies == 4803
    assert genres == 20

def test_seeding_idempotent(table_counts):
    first = table_counts()
    load_processed()
    second = table_counts()
    assert first == second
