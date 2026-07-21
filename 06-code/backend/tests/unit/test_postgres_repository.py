from datetime import UTC, datetime
from types import SimpleNamespace
from uuid import uuid4

import pytest
from psycopg.errors import UniqueViolation

from app.application.errors import DuplicateEmail
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
