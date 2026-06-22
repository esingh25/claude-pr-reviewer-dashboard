from app.database import _normalize_database_url


def test_normalize_leaves_sqlite_untouched():
    assert _normalize_database_url("sqlite:///./dev.db") == "sqlite:///./dev.db"


def test_normalize_rewrites_plain_postgresql_to_psycopg_driver():
    url = "postgresql://user:pass@host/db?sslmode=require"

    result = _normalize_database_url(url)

    assert result == "postgresql+psycopg://user:pass@host/db?sslmode=require"


def test_normalize_leaves_explicit_driver_untouched():
    url = "postgresql+psycopg://user:pass@host/db"

    assert _normalize_database_url(url) == url
