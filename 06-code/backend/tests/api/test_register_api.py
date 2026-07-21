from datetime import UTC, datetime
from typing import cast
from uuid import UUID

from fastapi.testclient import TestClient
import pytest
from starlette.types import Message, Scope

from app.application.errors import DatabaseUnavailable, DuplicateEmail
from app.domain.errors import InvalidEmail
from app.domain.user import Email, User, UserId
from app.interfaces.api.app import create_app


class RegisterStub:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error
        self.calls: list[tuple[str, str]] = []

    def execute(self, email: str, password: str) -> User:
        self.calls.append((email, password))
        if self.error:
            raise self.error
        return User(
            id=UserId(UUID("8bb45e10-84cb-4b89-8f75-c27bbb319fe8")),
            email=Email.parse(email),
            password_hash="$argon2id$hidden",
            created_at=datetime(2026, 7, 21, 15, 0, tzinfo=UTC),
            updated_at=datetime(2026, 7, 21, 15, 0, tzinfo=UTC),
        )


def client(stub: RegisterStub) -> TestClient:
    return TestClient(create_app(register_user=stub), raise_server_exceptions=False)


def test_register_contract_returns_201_without_sensitive_data_or_jwt() -> None:
    stub = RegisterStub()
    response = client(stub).post(
        "/api/v1/auth/register",
        json={"email": " Me@Example.com ", "password": "a secure password"},
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": "8bb45e10-84cb-4b89-8f75-c27bbb319fe8",
        "email": "me@example.com",
        "created_at": "2026-07-21T15:00:00Z",
    }
    assert stub.calls == [("Me@Example.com", "a secure password")]
    assert "password" not in response.text.lower()
    assert "token" not in response.text.lower()


def test_unknown_field_uses_stable_422_envelope() -> None:
    response = client(RegisterStub()).post(
        "/api/v1/auth/register",
        json={"email": "me@example.com", "password": "a" * 12, "role": "admin"},
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"
    assert "role" in response.json()["error"]["fields"]


def test_malformed_json_uses_stable_422_envelope() -> None:
    response = client(RegisterStub()).post(
        "/api/v1/auth/register", content=b'{"email":', headers={"content-type": "application/json"}
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_body_over_4_kib_uses_stable_422_envelope() -> None:
    response = client(RegisterStub()).post(
        "/api/v1/auth/register",
        content=b"x" * 4097,
        headers={"content-type": "application/json"},
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_actual_body_size_is_enforced_when_content_length_is_misleading() -> None:
    response = client(RegisterStub()).post(
        "/api/v1/auth/register",
        content=b"x" * 4097,
        headers={"content-type": "application/json", "content-length": "1"},
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


@pytest.mark.asyncio
async def test_body_limit_stops_reading_as_soon_as_4_kib_is_exceeded() -> None:
    app = create_app(register_user=RegisterStub())
    chunks: list[Message] = [
        {"type": "http.request", "body": b"x" * 4096, "more_body": True},
        {"type": "http.request", "body": b"x", "more_body": True},
        {"type": "http.request", "body": b"x" * 100_000, "more_body": False},
    ]
    received = 0
    sent: list[Message] = []

    async def receive() -> Message:
        nonlocal received
        message = chunks[received]
        received += 1
        return message

    async def send(message: Message) -> None:
        sent.append(message)

    await app(
        cast(Scope, {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": "POST",
            "scheme": "http",
            "path": "/api/v1/auth/register",
            "raw_path": b"/api/v1/auth/register",
            "query_string": b"",
            "headers": [(b"content-type", b"application/json")],
            "client": ("127.0.0.1", 1234),
            "server": ("testserver", 80),
        }),
        receive,
        send,
    )

    assert received == 2
    assert next(message["status"] for message in sent if message["type"] == "http.response.start") == 422


def test_domain_validation_uses_field_error() -> None:
    response = client(RegisterStub(InvalidEmail())).post(
        "/api/v1/auth/register", json={"email": "bad@example.com", "password": "a" * 12}
    )
    assert response.status_code == 422
    assert response.json()["error"]["fields"] == {"email": ["Enter a valid email address."]}


def test_duplicate_uses_stable_409_envelope() -> None:
    response = client(RegisterStub(DuplicateEmail())).post(
        "/api/v1/auth/register", json={"email": "me@example.com", "password": "a" * 12}
    )
    assert response.status_code == 409
    assert response.json() == {
        "error": {"code": "email_already_registered", "message": "Email is already registered."}
    }


def test_database_unavailable_uses_stable_503_envelope() -> None:
    response = client(RegisterStub(DatabaseUnavailable())).post(
        "/api/v1/auth/register", json={"email": "me@example.com", "password": "a" * 12}
    )
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "database_unavailable"


def test_unexpected_error_uses_stable_500_envelope() -> None:
    with client(RegisterStub(RuntimeError("must stay private"))) as api:
        response = api.post(
            "/api/v1/auth/register", json={"email": "me@example.com", "password": "a" * 12}
        )
    assert response.status_code == 500
    assert response.json()["error"]["code"] == "internal_error"
    assert "must stay private" not in response.text
