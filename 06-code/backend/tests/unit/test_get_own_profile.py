from datetime import datetime, timezone
from uuid import UUID

import pytest

from app.application.errors import AuthenticatedUserNotFound, DatabaseUnavailable
from app.application.use_cases.get_own_profile import GetOwnProfile, OwnProfile
from app.application.use_cases.validate_access_token import AuthenticatedPrincipal
from app.domain.user import Email, User, UserId


USER_ID = UUID("8bb45e10-84cb-4b89-8f75-c27bbb319fe8")
CREATED_AT = datetime(2026, 7, 21, 15, tzinfo=timezone.utc)


class UserRepositoryStub:
    def __init__(self, user: User | None = None, error: Exception | None = None) -> None:
        self.user = user
        self.error = error
        self.requested_ids: list[UserId] = []

    def get_by_id(self, user_id: UserId) -> User | None:
        self.requested_ids.append(user_id)
        if self.error:
            raise self.error
        return self.user


def user() -> User:
    return User(UserId(USER_ID), Email("person@example.com"), "private-hash", CREATED_AT, CREATED_AT)


def test_returns_only_the_authenticated_principals_public_profile() -> None:
    repository = UserRepositoryStub(user())
    principal = AuthenticatedPrincipal(USER_ID)

    profile = GetOwnProfile(repository).execute(principal)

    assert profile == OwnProfile(USER_ID, "person@example.com", CREATED_AT)
    assert repository.requested_ids == [UserId(USER_ID)]
    assert not hasattr(profile, "password_hash")


def test_rejects_a_principal_whose_user_no_longer_exists() -> None:
    repository = UserRepositoryStub()

    with pytest.raises(AuthenticatedUserNotFound):
        GetOwnProfile(repository).execute(AuthenticatedPrincipal(USER_ID))


def test_propagates_repository_unavailability_without_exposing_a_user() -> None:
    repository = UserRepositoryStub(error=DatabaseUnavailable())

    with pytest.raises(DatabaseUnavailable):
        GetOwnProfile(repository).execute(AuthenticatedPrincipal(USER_ID))
