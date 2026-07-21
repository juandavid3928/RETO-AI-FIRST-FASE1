import psycopg
from psycopg import sql
from psycopg.conninfo import conninfo_to_dict, make_conninfo
import pytest
from alembic import command
from alembic.config import Config
from uuid import uuid4


def test_users_migration_up_and_down(database_url: str) -> None:
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", database_url)
    command.downgrade(config, "base")
    command.upgrade(config, "head")

    with psycopg.connect(database_url) as connection:
        table = connection.execute("SELECT to_regclass('public.users')").fetchone()[0]
        constraint = connection.execute(
            "SELECT conname FROM pg_constraint WHERE conname = 'uq_users_email_canonical'"
        ).fetchone()[0]
        timestamp_columns = connection.execute(
            """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = 'users'
              AND column_name IN ('created_at', 'updated_at')
            ORDER BY column_name
            """
        ).fetchall()
    assert table == "users"
    assert constraint == "uq_users_email_canonical"
    assert timestamp_columns == [
        ("created_at", "timestamp with time zone"),
        ("updated_at", "timestamp with time zone"),
    ]

    command.downgrade(config, "base")
    with psycopg.connect(database_url) as connection:
        assert connection.execute("SELECT to_regclass('public.users')").fetchone()[0] is None


def test_alembic_db_environment_supports_reserved_password_characters(
    database_url: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    admin_settings = conninfo_to_dict(database_url)
    suffix = uuid4().hex[:12]
    role = f"alembic_role_{suffix}"
    database = f"alembic_db_{suffix}"
    password = "test@value:with/reserved?chars and spaces%"

    with psycopg.connect(database_url, autocommit=True) as admin:
        admin.execute(
            sql.SQL("CREATE ROLE {} LOGIN PASSWORD {}").format(
                sql.Identifier(role), sql.Literal(password)
            )
        )
        admin.execute(
            sql.SQL("CREATE DATABASE {} OWNER {}").format(
                sql.Identifier(database), sql.Identifier(role)
            )
        )
        try:
            monkeypatch.delenv("DATABASE_URL", raising=False)
            monkeypatch.setenv("DB_HOST", str(admin_settings["host"]))
            monkeypatch.setenv("DB_PORT", str(admin_settings["port"]))
            monkeypatch.setenv("DB_NAME", database)
            monkeypatch.setenv("DB_USER", role)
            monkeypatch.setenv("DB_PASSWORD", password)

            config = Config("alembic.ini")
            command.upgrade(config, "head")

            reserved_credential_conninfo = make_conninfo(
                host=admin_settings["host"],
                port=admin_settings["port"],
                dbname=database,
                user=role,
                password=password,
            )
            with psycopg.connect(reserved_credential_conninfo) as connection:
                row = connection.execute("SELECT to_regclass('public.users')").fetchone()
                assert row is not None
                assert row[0] == "users"

            command.downgrade(config, "base")
        finally:
            admin.execute(
                "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = %s",
                (database,),
            )
            admin.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(database)))
            admin.execute(sql.SQL("DROP ROLE IF EXISTS {}").format(sql.Identifier(role)))
