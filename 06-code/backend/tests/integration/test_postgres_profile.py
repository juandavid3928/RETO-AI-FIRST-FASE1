import base64
from uuid import UUID

import psycopg
from fastapi.testclient import TestClient

from app.bootstrap import build_app
from app.domain.user import UserId
from app.infrastructure.database.postgres_user_repository import PostgresUserRepository


JWT_SECRET = base64.urlsafe_b64encode(b"0123456789abcdef0123456789abcdef").decode().rstrip("=")


def test_real_postgres_profile_is_selected_only_by_authenticated_subject(migrated_database: str) -> None:
    api = TestClient(build_app(migrated_database, JWT_SECRET), raise_server_exceptions=False)
    first = api.post(
        "/api/v1/auth/register",
        json={"email": "profile@example.com", "password": "correct horse battery"},
    ).json()
    other = api.post(
        "/api/v1/auth/register",
        json={"email": "other@example.com", "password": "correct horse battery"},
    ).json()
    login = api.post(
        "/api/v1/auth/login",
        json={"email": "profile@example.com", "password": "correct horse battery"},
    )
    token = login.json()["access_token"]

    response = api.request(
        "GET",
        f"/api/v1/users/me?user_id={other['id']}",
        headers={"authorization": f"Bearer {token}", "x-user-id": other["id"]},
        json={"user_id": other["id"]},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": first["id"],
        "email": "profile@example.com",
        "created_at": first["created_at"],
    }
    stored = PostgresUserRepository(migrated_database).get_by_id(UserId(UUID(first["id"])))
    assert stored is not None
    assert stored.email.value == "profile@example.com"


def test_deleted_authenticated_user_is_uniformly_rejected(migrated_database: str) -> None:
    api = TestClient(build_app(migrated_database, JWT_SECRET), raise_server_exceptions=False)
    registration = api.post(
        "/api/v1/auth/register",
        json={"email": "deleted@example.com", "password": "correct horse battery"},
    ).json()
    token = api.post(
        "/api/v1/auth/login",
        json={"email": "deleted@example.com", "password": "correct horse battery"},
    ).json()["access_token"]
    with psycopg.connect(migrated_database) as connection:
        connection.execute("DELETE FROM users WHERE id = %s", (UUID(registration["id"]),))
        connection.commit()

    response = api.get("/api/v1/users/me", headers={"authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json() == {"error": {"code": "invalid_token", "message": "Access token is invalid."}}
    assert response.headers["www-authenticate"] == "Bearer"
