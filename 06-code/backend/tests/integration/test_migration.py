import psycopg
from alembic import command
from alembic.config import Config


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
