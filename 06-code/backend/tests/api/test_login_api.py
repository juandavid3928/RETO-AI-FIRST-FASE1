from uuid import UUID

from fastapi import Depends
from fastapi.testclient import TestClient

from app.application.errors import DatabaseUnavailable, InvalidAccessToken, InvalidCredentials
from app.application.use_cases.validate_access_token import AuthenticatedPrincipal
from app.interfaces.api.app import create_app


class RegisterStub:
    def execute(self, email: str, password: str):
        raise AssertionError("registration is out of this test")


class AuthenticateStub:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error
        self.calls: list[tuple[str, str]] = []

    def execute(self, email: str, password: str) -> str:
        self.calls.append((email, password))
        if self.error:
            raise self.error
        return "signed.jwt"


class ValidateStub:
    def execute(self, token: str) -> AuthenticatedPrincipal:
        if token != "valid.jwt":
            raise InvalidAccessToken
        return AuthenticatedPrincipal(UUID("8bb45e10-84cb-4b89-8f75-c27bbb319fe8"))


def client(authenticate: AuthenticateStub | None = None) -> tuple[TestClient, AuthenticateStub]:
    authenticate = authenticate or AuthenticateStub()
    app = create_app(register_user=RegisterStub(), authenticate_user=authenticate, validate_access_token=ValidateStub())

    @app.get("/_test/protected")
    def protected(principal=Depends(app.state.require_principal)):
        return {"user_id": str(principal.user_id)}

    return TestClient(app, raise_server_exceptions=False), authenticate


def assert_no_store(response) -> None:
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["pragma"] == "no-cache"


def test_login_returns_bearer_token_contract_without_trimming_password() -> None:
    api, authenticate = client()
    response = api.post("/api/v1/auth/login", json={"email": " Person@Example.com ", "password": " secret "})
    assert response.status_code == 200
    assert response.json() == {"access_token": "signed.jwt", "token_type": "bearer", "expires_in": 1800}
    assert authenticate.calls == [("Person@Example.com", " secret ")]
    assert_no_store(response)


def test_login_forbids_extra_fields_and_enforces_password_bounds() -> None:
    api, _ = client()
    for body in (
        {"email": "person@example.com", "password": "", "role": "admin"},
        {"email": "person@example.com", "password": "x" * 129},
    ):
        response = api.post("/api/v1/auth/login", json=body)
        assert response.status_code == 422
        assert response.json()["error"]["code"] == "validation_error"
        assert_no_store(response)


def test_login_rejects_malformed_email_as_validation_error() -> None:
    api, authenticate = client()

    response = api.post("/api/v1/auth/login", json={"email": "not-an-email", "password": "x"})

    assert response.status_code == 422
    assert response.json() == {
        "error": {
            "code": "validation_error",
            "message": "Login data is invalid.",
            "fields": {"email": ["Enter a valid email address."]},
        }
    }
    assert authenticate.calls == []
    assert_no_store(response)


def test_registration_keeps_its_specific_validation_message() -> None:
    api, _ = client()

    response = api.post("/api/v1/auth/register", json={})

    assert response.status_code == 422
    assert response.json()["error"]["message"] == "Registration data is invalid."


def test_login_rejects_body_over_4_kib_with_no_store_headers() -> None:
    api, _ = client()
    response = api.post("/api/v1/auth/login", content=b"x" * 4097, headers={"content-type": "application/json"})
    assert response.status_code == 422
    assert_no_store(response)


def test_login_uses_uniform_invalid_credentials_response() -> None:
    api, _ = client(AuthenticateStub(InvalidCredentials()))
    response = api.post("/api/v1/auth/login", json={"email": "nobody@example.com", "password": "wrong"})
    assert response.status_code == 401
    assert response.json() == {"error": {"code": "invalid_credentials", "message": "Email or password is incorrect."}}
    assert response.headers["www-authenticate"] == "Bearer"
    assert_no_store(response)


def test_login_maps_database_and_unexpected_failures() -> None:
    cases = [
        (DatabaseUnavailable(), 503, "database_unavailable"),
        (RuntimeError("private"), 500, "internal_error"),
    ]
    for error, status, code in cases:
        api, _ = client(AuthenticateStub(error))
        response = api.post("/api/v1/auth/login", json={"email": "person@example.com", "password": "secret"})
        assert response.status_code == status
        assert response.json()["error"]["code"] == code
        assert "private" not in response.text
        assert_no_store(response)


def test_bearer_dependency_returns_principal_for_valid_token() -> None:
    api, _ = client()
    response = api.get("/_test/protected", headers={"authorization": "Bearer valid.jwt"})
    assert response.status_code == 200
    assert response.json() == {"user_id": "8bb45e10-84cb-4b89-8f75-c27bbb319fe8"}


def test_bearer_dependency_distinguishes_missing_and_invalid_token() -> None:
    api, _ = client()
    missing = api.get("/_test/protected")
    invalid = api.get("/_test/protected", headers={"authorization": "Bearer invalid.jwt"})
    assert missing.status_code == invalid.status_code == 401
    assert missing.json()["error"]["code"] == "authentication_required"
    assert invalid.json()["error"]["code"] == "invalid_token"
    assert missing.headers["www-authenticate"] == invalid.headers["www-authenticate"] == "Bearer"
