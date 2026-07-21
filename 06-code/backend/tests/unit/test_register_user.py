from datetime import UTC, datetime
from uuid import UUID

import pytest

from app.application.errors import DuplicateEmail
from app.application.use_cases.register_user import RegisterUser
from app.domain.errors import InvalidEmail, InvalidPassword
from app.domain.user import Email, User, UserId


class RepositoryStub:
    def __init__(self, *, duplicate: bool = False) -> None:
        self.duplicate = duplicate
        self.saved: User | None = None

    def add(self, user: User) -> User:
        if self.duplicate:
            raise DuplicateEmail
        self.saved = user
        return user


class HashStub:
    def hash(self, password: str) -> str:
        return f"hashed::{len(password)}"


class IdStub:
    def new(self) -> UserId:
        return UserId(UUID("8bb45e10-84cb-4b89-8f75-c27bbb319fe8"))


class ClockStub:
    def now(self) -> datetime:
        return datetime(2026, 7, 21, 15, 0, tzinfo=UTC)


def use_case(repository: RepositoryStub | None = None) -> tuple[RegisterUser, RepositoryStub]:
    repository = repository or RepositoryStub()
    return RegisterUser(repository, HashStub(), ClockStub(), IdStub()), repository


def test_registers_canonical_email_without_retaining_plaintext_password() -> None:
    register, repository = use_case()

    user = register.execute("  Person.Name@EXAMPLE.COM ", "correct horse battery")

    assert isinstance(user.email, Email)
    assert user.email.value == "person.name@example.com"
    assert isinstance(user.id, UserId)
    assert user.id.version == 4
    assert user.created_at == datetime(2026, 7, 21, 15, 0, tzinfo=UTC)
    assert user.updated_at == user.created_at
    assert repository.saved == user
    assert user.password_hash == "hashed::21"
    assert not hasattr(user, "password")


def test_email_is_a_domain_value_object() -> None:
    assert Email.parse("  Person@EXAMPLE.COM ") == Email("person@example.com")

    with pytest.raises(InvalidEmail):
        Email.parse("not-an-email")

    with pytest.raises(InvalidEmail):
        Email.parse("person..dots@example.com")

    for invalid in ("a,b@example.com", "a()@example.com", "<x>@example.com"):
        with pytest.raises(InvalidEmail):
            Email.parse(invalid)


def test_user_id_requires_uuid4() -> None:
    with pytest.raises(ValueError, match="UUID4"):
        UserId(UUID("00000000-0000-0000-0000-000000000000"))


@pytest.mark.parametrize("email", ["", "not-an-email", "a@", "@example.com", "a b@example.com"])
def test_rejects_invalid_email(email: str) -> None:
    register, repository = use_case()
    with pytest.raises(InvalidEmail):
        register.execute(email, "a" * 12)
    assert repository.saved is None


@pytest.mark.parametrize("password", ["a" * 11, "a" * 129])
def test_rejects_password_outside_12_to_128_characters(password: str) -> None:
    register, repository = use_case()
    with pytest.raises(InvalidPassword):
        register.execute("valid@example.com", password)
    assert repository.saved is None


def test_propagates_duplicate_email_from_repository() -> None:
    register, _ = use_case(RepositoryStub(duplicate=True))
    with pytest.raises(DuplicateEmail):
        register.execute("valid@example.com", "a" * 12)
