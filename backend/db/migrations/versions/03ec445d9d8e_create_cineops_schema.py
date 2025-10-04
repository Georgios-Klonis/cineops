"""create cineops schema

Revision ID: 03ec445d9d8e
Revises: 
Create Date: 2025-10-04 18:17:40.458093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '03ec445d9d8e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

status_enum = postgresql.ENUM('active', 'deleted', 'suspended', name='status', create_type=False)
visibility_enum = postgresql.ENUM('public', 'private', name='visibility', create_type=False)


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    status_enum.create(bind, checkfirst=True)
    visibility_enum.create(bind, checkfirst=True)

    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('firebase_id', sa.String(), nullable=False, unique=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('display_name', sa.String(length=120), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False, unique=True),
        sa.Column('avatar_url', sa.String(length=512), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('preferences_genres', postgresql.ARRAY(sa.Integer), nullable=True, server_default=sa.text("'{}'::integer[]")),
        sa.Column('status', status_enum, nullable=True, server_default=sa.text("'active'::status")),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    )

    op.create_table(
        'genres',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False, unique=True),
    )

    op.create_table(
        'movies',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('tmdb_id', sa.Integer, nullable=False, unique=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('overview', sa.Text(), nullable=True),
        sa.Column('release_date', sa.Date(), nullable=True),
        sa.Column('runtime', sa.Float(), nullable=True),
        sa.Column('poster_url', sa.String(), nullable=True),
        sa.Column('genre_ids', postgresql.ARRAY(sa.Integer), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    )

    op.create_table(
        'user_favorites',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('movie_id', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
        sa.UniqueConstraint('user_id', 'movie_id', name='uq_user_favorites_user_movie'),
    )

    op.create_table(
        'lists',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('visibility', visibility_enum, nullable=True, server_default=sa.text("'private'::visibility")),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    )

    op.create_table(
        'reviews',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('movie_id', sa.Integer, nullable=False),
        sa.Column('rating', sa.Float(), nullable=False),
        sa.Column('body', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
        sa.UniqueConstraint('user_id', 'movie_id', name='uq_reviews_user_movie'),
    )

    op.create_table(
        'list_items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('list_id', sa.Integer, nullable=False),
        sa.Column('movie_id', sa.Integer, nullable=False),
        sa.Column('position', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['list_id'], ['lists.id'], ),
        sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
        sa.UniqueConstraint('list_id', 'movie_id', name='uq_list_items_list_movie'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('list_items')
    op.drop_table('reviews')
    op.drop_table('lists')
    op.drop_table('user_favorites')
    op.drop_table('movies')
    op.drop_table('genres')
    op.drop_table('users')

    bind = op.get_bind()
    visibility_enum.drop(bind, checkfirst=True)
    status_enum.drop(bind, checkfirst=True)
