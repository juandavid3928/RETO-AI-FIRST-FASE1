from concurrent.futures import ThreadPoolExecutor
import base64

import psycopg
from fastapi.testclient import TestClient

from app.bootstrap import build_app


JWT_SECRET = base64.urlsafe_b64encode(b"0123456789abcdef0123456789abcdef").decode().rstrip("=")


def build_test_app(database_url: str):
    return build_app(database_url, JWT_SECRET)


def test_registration_persists_canonical_email_and_argon2id_hash(migrated_database: str) -> None:
    api = TestClient(build_test_app(migrated_database), raise_server_exceptions=False)
    password = "correct horse battery"

    response = api.post(
        "/api/v1/auth/register",
        json={"email": "  Person@EXAMPLE.com ", "password": password},
    )

    assert response.status_code == 201
    with psycopg.connect(migrated_database) as connection:
        email, password_hash = connection.execute(
            "SELECT email, password_hash FROM users"
        ).fetchone()
    assert email == "person@example.com"
    assert password_hash.startswith("$argon2id$")
    assert password not in password_hash


def test_canonical_email_is_unique(migrated_database: str) -> None:
    api = TestClient(build_test_app(migrated_database), raise_server_exceptions=False)
    first = api.post(
        "/api/v1/auth/register", json={"email": "case@example.com", "password": "a" * 12}
    )
    duplicate = api.post(
        "/api/v1/auth/register", json={"email": " CASE@EXAMPLE.COM ", "password": "b" * 12}
    )
    assert (first.status_code, duplicate.status_code) == (201, 409)
    with psycopg.connect(migrated_database) as connection:
        assert connection.execute("SELECT count(*) FROM users").fetchone()[0] == 1


def test_concurrent_requests_yield_exactly_one_201_and_one_409(migrated_database: str) -> None:
    app = build_test_app(migrated_database)

    def submit(email: str) -> int:
        with TestClient(app, raise_server_exceptions=False) as api:
            return api.post(
                "/api/v1/auth/register", json={"email": email, "password": "a" * 12}
            ).status_code

    with ThreadPoolExecutor(max_workers=2) as executor:
        statuses = list(executor.map(submit, ["race@example.com", " RACE@EXAMPLE.COM "]))

    assert sorted(statuses) == [201, 409]
    with psycopg.connect(migrated_database) as connection:
        assert connection.execute("SELECT count(*) FROM users").fetchone()[0] == 1


def test_registered_user_can_login_and_wrong_password_is_uniform(migrated_database: str) -> None:
    api = TestClient(build_test_app(migrated_database), raise_server_exceptions=False)
    registration = api.post(
        "/api/v1/auth/register",
        json={"email": "login@example.com", "password": "correct horse battery"},
    )
    assert registration.status_code == 201

    success = api.post(
        "/api/v1/auth/login",
        json={"email": " LOGIN@EXAMPLE.COM ", "password": "correct horse battery"},
    )
    wrong = api.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "wrong"},
    )
    missing = api.post(
        "/api/v1/auth/login",
        json={"email": "missing@example.com", "password": "wrong"},
    )

    assert success.status_code == 200
    assert success.json()["token_type"] == "bearer"
    assert wrong.status_code == missing.status_code == 401
    assert wrong.json() == missing.json()
