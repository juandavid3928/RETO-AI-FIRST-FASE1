from datetime import UTC, datetime, timedelta, timezone
from uuid import UUID

from fastapi.testclient import TestClient

from app.application.errors import (
    AuthenticatedUserNotFound,
    DatabaseUnavailable,
    InvalidAccessToken,
)
from app.application.use_cases.get_own_profile import OwnProfile
from app.application.use_cases.validate_access_token import AuthenticatedPrincipal
from app.interfaces.api.app import create_app


USER_ID = UUID("8bb45e10-84cb-4b89-8f75-c27bbb319fe8")
OTHER_USER_ID = UUID("83dd9c47-f7f0-4db4-9af6-c54ffeba3154")
CREATED_AT = datetime(2026, 7, 21, 15, tzinfo=UTC)


class RegisterStub:
    def execute(self, email: str, password: str):
        raise AssertionError("registration is out of this test")


class ValidateStub:
    def execute(self, token: str) -> AuthenticatedPrincipal:
        if token != "valid.jwt":
            raise InvalidAccessToken
        return AuthenticatedPrincipal(USER_ID)


class ProfileStub:
    def __init__(self, error: Exception | None = None, created_at: datetime = CREATED_AT) -> None:
        self.error = error
        self.created_at = created_at
        self.principals: list[AuthenticatedPrincipal] = []

    def execute(self, principal: AuthenticatedPrincipal) -> OwnProfile:
        self.principals.append(principal)
        if self.error:
            raise self.error
        return OwnProfile(USER_ID, "person@example.com", self.created_at)


def client(profile: ProfileStub | None = None) -> tuple[TestClient, ProfileStub]:
    profile = profile or ProfileStub()
    app = create_app(
        register_user=RegisterStub(),
        validate_access_token=ValidateStub(),
        get_own_profile=profile,
    )
    return TestClient(app, raise_server_exceptions=False), profile


def assert_private(response) -> None:
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["pragma"] == "no-cache"
    assert response.headers["vary"] == "Authorization"


def test_returns_exact_own_profile_without_secrets() -> None:
    api, profile = client()

    response = api.get("/api/v1/users/me", headers={"authorization": "Bearer valid.jwt"})

    assert response.status_code == 200
    assert response.json() == {
        "id": str(USER_ID),
        "email": "person@example.com",
        "created_at": "2026-07-21T15:00:00Z",
    }
    assert profile.principals == [AuthenticatedPrincipal(USER_ID)]
    assert "password" not in response.text
    assert "token" not in response.text
    assert_private(response)


def test_normalizes_created_at_to_utc() -> None:
    source_timezone = timezone(timedelta(hours=-5))
    api, _ = client(ProfileStub(created_at=datetime(2026, 7, 21, 10, tzinfo=source_timezone)))

    response = api.get("/api/v1/users/me", headers={"authorization": "Bearer valid.jwt"})

    assert response.status_code == 200
    assert response.json()["created_at"] == "2026-07-21T15:00:00Z"


def test_client_supplied_user_ids_never_change_the_authenticated_identity() -> None:
    api, profile = client()

    response = api.request(
        "GET",
        f"/api/v1/users/me?user_id={OTHER_USER_ID}",
        headers={"authorization": "Bearer valid.jwt", "x-user-id": str(OTHER_USER_ID)},
        json={"user_id": str(OTHER_USER_ID)},
    )

    assert response.status_code == 200
    assert response.json()["id"] == str(USER_ID)
    assert profile.principals == [AuthenticatedPrincipal(USER_ID)]


def test_missing_and_invalid_bearer_keep_the_approved_contract() -> None:
    api, profile = client()

    missing = api.get("/api/v1/users/me")
    invalid = api.get("/api/v1/users/me", headers={"authorization": "Bearer expired.jwt"})

    assert missing.status_code == invalid.status_code == 401
    assert missing.json() == {"error": {"code": "authentication_required", "message": "Authentication is required."}}
    assert invalid.json() == {"error": {"code": "invalid_token", "message": "Access token is invalid."}}
    assert missing.headers["www-authenticate"] == invalid.headers["www-authenticate"] == "Bearer"
    assert_private(missing)
    assert_private(invalid)
    assert profile.principals == []


def test_missing_authenticated_user_is_an_invalid_token_without_enumeration() -> None:
    api, _ = client(ProfileStub(AuthenticatedUserNotFound()))

    response = api.get("/api/v1/users/me", headers={"authorization": "Bearer valid.jwt"})

    assert response.status_code == 401
    assert response.json() == {"error": {"code": "invalid_token", "message": "Access token is invalid."}}
    assert response.headers["www-authenticate"] == "Bearer"
    assert_private(response)


def test_database_and_unexpected_failures_are_private_and_generic() -> None:
    cases = [
        (DatabaseUnavailable(), 503, "database_unavailable"),
        (RuntimeError("private detail"), 500, "internal_error"),
    ]
    for error, status, code in cases:
        api, _ = client(ProfileStub(error))

        response = api.get("/api/v1/users/me", headers={"authorization": "Bearer valid.jwt"})

        assert response.status_code == status
        assert response.json()["error"]["code"] == code
        assert "private detail" not in response.text
        assert_private(response)
