"""SQLAlchemy engine/session setup. Reads DATABASE_URL (Neon Postgres in production, falls
back to a local SQLite file for development when unset)."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


def _normalize_database_url(url: str) -> str:
    """Neon (and most providers) hand out plain postgresql:// URLs, but SQLAlchemy defaults
    that scheme to the psycopg2 driver — we install psycopg (v3) instead, so rewrite it."""
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url[len("postgresql://") :]
    return url


DATABASE_URL = _normalize_database_url(os.environ.get("DATABASE_URL", "sqlite:///./dev.db"))

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
