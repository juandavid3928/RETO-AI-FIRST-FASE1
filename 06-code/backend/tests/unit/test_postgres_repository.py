from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any, cast
from uuid import uuid4

import pytest
import psycopg
from psycopg.errors import UniqueViolation

from app.application.errors import DatabaseUnavailable, DuplicateEmail
from app.domain.user import Email, User, UserId
from app.infrastructure.database.postgres_user_repository import PostgresUserRepository


class ConstraintViolation(UniqueViolation):
    def __init__(self, constraint_name: str) -> None:
        super().__init__(constraint_name)
        self._constraint_name = constraint_name

    @property
    def diag(self):
        return SimpleNamespace(constraint_name=self._constraint_name)


class ConnectionStub:
    def __init__(self, constraint_name: str) -> None:
        self.constraint_name = constraint_name
        self.rollback_count = 0
        self.close_count = 0

    def execute(self, *_args):
        raise ConstraintViolation(self.constraint_name)

    def rollback(self) -> None:
        self.rollback_count += 1

    def close(self) -> None:
        self.close_count += 1


class BrokenConnectionStub:
    def __init__(self) -> None:
        self.close_count = 0

    def execute(self, *_args) -> None:
        raise psycopg.OperationalError("connection lost")

    def rollback(self) -> None:
        raise psycopg.OperationalError("cannot rollback broken connection")

    def close(self) -> None:
        self.close_count += 1


def user() -> User:
    now = datetime.now(UTC)
    return User(
        UserId(uuid4()),
        Email("person@example.com"),
        "$argon2id$hash",
        now,
        now,
    )


def test_translates_only_email_constraint_and_rolls_back() -> None:
    connection = ConnectionStub("uq_users_email_canonical")
    repository = PostgresUserRepository("unused", connect=lambda _: connection)
    with pytest.raises(DuplicateEmail):
        repository.add(user())
    assert connection.rollback_count == 1
    assert connection.close_count == 1


def test_other_unique_constraint_remains_unexpected_after_rollback() -> None:
    connection = ConnectionStub("some_other_constraint")
    repository = PostgresUserRepository("unused", connect=lambda _: connection)
    with pytest.raises(UniqueViolation):
        repository.add(user())
    assert connection.rollback_count == 1
    assert connection.close_count == 1


def test_broken_rollback_does_not_mask_database_unavailable() -> None:
    connection = BrokenConnectionStub()
    repository = PostgresUserRepository("unused", connect=cast(Any, lambda _: connection))

    with pytest.raises(DatabaseUnavailable):
        repository.add(user())

    assert connection.close_count == 1


class LookupConnectionStub:
    def __init__(self, row):
        self.row = row
        self.query = None
        self.parameters = None
        self.close_count = 0

    def execute(self, query, parameters):
        self.query = query
        self.parameters = parameters
        return self

    def fetchone(self):
        return self.row

    def close(self):
        self.close_count += 1


def test_get_by_email_uses_parameterized_query_and_maps_user() -> None:
    identifier = uuid4()
    now = datetime.now(UTC)
    connection = LookupConnectionStub((identifier, "person@example.com", "$argon2id$hash", now, now))
    repository = PostgresUserRepository("unused", connect=cast(Any, lambda _: connection))

    found = repository.get_by_email("person@example.com")

    assert found == User(UserId(identifier), Email("person@example.com"), "$argon2id$hash", now, now)
    assert connection.parameters == ("person@example.com",)
    assert "%s" in connection.query
    assert connection.close_count == 1


def test_get_by_email_returns_none_when_absent() -> None:
    connection = LookupConnectionStub(None)
    repository = PostgresUserRepository("unused", connect=cast(Any, lambda _: connection))
    assert repository.get_by_email("missing@example.com") is None
