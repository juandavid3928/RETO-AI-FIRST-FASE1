import os

import psycopg
import pytest
from alembic import command
from alembic.config import Config


TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")


def database_available(database_url: str) -> bool:
    try:
        with psycopg.connect(database_url, connect_timeout=1):
            return True
    except psycopg.OperationalError:
        return False


@pytest.fixture(scope="session")
def database_url() -> str:
    if TEST_DATABASE_URL is None:
        pytest.fail("TEST_DATABASE_URL is required for real PostgreSQL integration tests")
    if not database_available(TEST_DATABASE_URL):
        pytest.fail("Real PostgreSQL is unavailable at TEST_DATABASE_URL")
    return TEST_DATABASE_URL


@pytest.fixture()
def migrated_database(database_url: str) -> str:
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", database_url)
    command.downgrade(config, "base")
    command.upgrade(config, "head")
    yield database_url
    command.downgrade(config, "base")
