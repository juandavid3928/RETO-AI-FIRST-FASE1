from psycopg.conninfo import conninfo_to_dict

from app.infrastructure.database.config import build_database_conninfo


def test_builds_safe_conninfo_for_reserved_postgres_credentials() -> None:
    conninfo = build_database_conninfo(
        None,
        host="db",
        port=5432,
        database="portal/db",
        user="portal@service",
        password="p@ss:word/with?chars and spaces",
    )

    parsed = conninfo_to_dict(conninfo)
    assert parsed == {
        "dbname": "portal/db",
        "host": "db",
        "password": "p@ss:word/with?chars and spaces",
        "port": "5432",
        "user": "portal@service",
    }


def test_explicit_database_url_takes_precedence() -> None:
    url = "postgresql://explicit.example/database"
    assert build_database_conninfo(url) == url
