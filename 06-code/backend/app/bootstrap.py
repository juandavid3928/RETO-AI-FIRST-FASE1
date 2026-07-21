from app.application.use_cases.register_user import RegisterUser
from app.infrastructure.database.postgres_user_repository import PostgresUserRepository
from app.infrastructure.password_hasher import Argon2PasswordHasher
from app.infrastructure.system import SystemClock, Uuid4Generator
from app.interfaces.api.app import create_app


def build_app(database_url: str):
    register_user = RegisterUser(
        PostgresUserRepository(database_url),
        Argon2PasswordHasher(),
        SystemClock(),
        Uuid4Generator(),
    )
    app = create_app(register_user=register_user)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
