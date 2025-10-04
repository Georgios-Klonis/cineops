"""SQLAlchemy ORM models for the CineOps database schema."""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import List, Optional

import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""


class UserStatus(str, Enum):
    ACTIVE = "active"
    DELETED = "deleted"
    SUSPENDED = "suspended"


class ListVisibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False
    )


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    firebase_id: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(sa.String(255), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(sa.String(120), nullable=False)
    username: Mapped[str] = mapped_column(sa.String(50), unique=True, nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(sa.String(512))
    bio: Mapped[Optional[str]] = mapped_column(sa.Text)
    preferences_genres: Mapped[List[int]] = mapped_column(
        sa.ARRAY(sa.Integer),
        nullable=False,
        server_default=sa.text("'{}'::integer[]"),
        default=list,
    )
    status: Mapped[UserStatus] = mapped_column(
        sa.Enum(UserStatus, name="status"),
        nullable=False,
        server_default=sa.text("'active'::status"),
        default=UserStatus.ACTIVE,
    )

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    favorites: Mapped[list["UserFavorite"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    lists: Mapped[list["List"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(100), unique=True, nullable=False)


class Movie(Base, TimestampMixin):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    tmdb_id: Mapped[int] = mapped_column(sa.Integer, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    overview: Mapped[Optional[str]] = mapped_column(sa.Text)
    release_date: Mapped[Optional[date]] = mapped_column(sa.Date)
    runtime: Mapped[Optional[float]] = mapped_column(sa.Float)
    poster_url: Mapped[Optional[str]] = mapped_column(sa.String)
    genre_ids: Mapped[Optional[List[int]]] = mapped_column(sa.ARRAY(sa.Integer))

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="movie", cascade="all, delete-orphan"
    )
    favorites: Mapped[list["UserFavorite"]] = relationship(
        back_populates="movie", cascade="all, delete-orphan"
    )
    list_items: Mapped[list["ListItem"]] = relationship(
        back_populates="movie", cascade="all, delete-orphan"
    )


class UserFavorite(Base):
    __tablename__ = "user_favorites"
    __table_args__ = (
        sa.UniqueConstraint("user_id", "movie_id", name="uq_user_favorites_user_movie"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False
    )

    user: Mapped[User] = relationship(back_populates="favorites")
    movie: Mapped[Movie] = relationship(back_populates="favorites")


class Review(Base, TimestampMixin):
    __tablename__ = "reviews"
    __table_args__ = (
        sa.UniqueConstraint("user_id", "movie_id", name="uq_reviews_user_movie"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    rating: Mapped[float] = mapped_column(sa.Float, nullable=False)
    body: Mapped[Optional[str]] = mapped_column(sa.Text)

    user: Mapped[User] = relationship(back_populates="reviews")
    movie: Mapped[Movie] = relationship(back_populates="reviews")


class List(Base, TimestampMixin):
    __tablename__ = "lists"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(sa.Text)
    visibility: Mapped[ListVisibility] = mapped_column(
        sa.Enum(ListVisibility, name="visibility"),
        nullable=False,
        server_default=sa.text("'private'::visibility"),
        default=ListVisibility.PRIVATE,
    )

    user: Mapped[User] = relationship(back_populates="lists")
    items: Mapped[list["ListItem"]] = relationship(
        back_populates="list", cascade="all, delete-orphan"
    )


class ListItem(Base):
    __tablename__ = "list_items"
    __table_args__ = (
        sa.UniqueConstraint("list_id", "movie_id", name="uq_list_items_list_movie"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    list_id: Mapped[int] = mapped_column(ForeignKey("lists.id", ondelete="CASCADE"), nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    position: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False
    )

    list: Mapped[List] = relationship(back_populates="items")
    movie: Mapped[Movie] = relationship(back_populates="list_items")
