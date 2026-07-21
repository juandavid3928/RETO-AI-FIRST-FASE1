from datetime import UTC, datetime
from uuid import UUID

import pytest

from app.application.errors import InvalidCredentials
from app.application.use_cases.authenticate_user import AuthenticateUser
from app.domain.user import Email, User, UserId


USER = User(
    UserId(UUID("8bb45e10-84cb-4b89-8f75-c27bbb319fe8")),
    Email("person@example.com"),
    "$argon2id$real",
    datetime(2026, 7, 21, tzinfo=UTC),
    datetime(2026, 7, 21, tzinfo=UTC),
)


class RepositoryStub:
    def __init__(self, found: User | None) -> None:
        self.found = found
        self.emails: list[str] = []

    def get_by_email(self, email: str) -> User | None:
        self.emails.append(email)
        return self.found


class VerifierStub:
    def __init__(self, valid: bool) -> None:
        self.valid = valid
        self.calls: list[tuple[str, str]] = []

    def verify(self, password: str, password_hash: str) -> bool:
        self.calls.append((password, password_hash))
        return self.valid


class IssuerStub:
    def issue(self, subject: str) -> str:
        return f"token:{subject}"


def test_authenticates_canonical_email_and_issues_token() -> None:
    repository = RepositoryStub(USER)
    verifier = VerifierStub(True)

    token = AuthenticateUser(repository, verifier, IssuerStub(), "$argon2id$dummy").execute(
        " Person@Example.com ", " secret "
    )

    assert token == "token:8bb45e10-84cb-4b89-8f75-c27bbb319fe8"
    assert repository.emails == ["person@example.com"]
    assert verifier.calls == [(" secret ", "$argon2id$real")]


def test_missing_user_runs_dummy_verification_then_returns_uniform_error() -> None:
    verifier = VerifierStub(False)

    with pytest.raises(InvalidCredentials):
        AuthenticateUser(RepositoryStub(None), verifier, IssuerStub(), "$argon2id$dummy").execute(
            "missing@example.com", "secret"
        )

    assert verifier.calls == [("secret", "$argon2id$dummy")]


def test_wrong_password_returns_uniform_error() -> None:
    with pytest.raises(InvalidCredentials):
        AuthenticateUser(RepositoryStub(USER), VerifierStub(False), IssuerStub(), "$argon2id$dummy").execute(
            "person@example.com", "wrong"
        )
