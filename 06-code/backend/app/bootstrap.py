from app.application.use_cases.authenticate_user import AuthenticateUser
from app.application.use_cases.get_own_profile import GetOwnProfile
from app.application.use_cases.list_current_opportunities import ListCurrentOpportunities
from app.application.use_cases.register_user import RegisterUser
from app.application.use_cases.validate_access_token import ValidateAccessToken
from app.infrastructure.database.postgres_user_repository import PostgresUserRepository
from app.infrastructure.external.secop_opportunity_source import DEFAULT_BASE_URL, SecopOpportunitySource
from app.infrastructure.jwt_access_token import JwtAccessTokenService, decode_secret
from app.infrastructure.password_hasher import Argon2PasswordHasher
from app.infrastructure.system import ColombiaDateProvider, SystemClock, Uuid4Generator
from app.interfaces.api.app import create_app


def build_app(
    database_url: str,
    jwt_secret: str,
    *,
    secop_base_url: str = DEFAULT_BASE_URL,
    secop_timeout_seconds: float = 5.0,
):
    password_adapter = Argon2PasswordHasher()
    dummy_password_hash = password_adapter.dummy_hash()
    clock = SystemClock()
    token_service = JwtAccessTokenService(decode_secret(jwt_secret), clock)
    users = PostgresUserRepository(database_url)
    register_user = RegisterUser(
        users,
        password_adapter,
        clock,
        Uuid4Generator(),
    )
    authenticate_user = AuthenticateUser(users, password_adapter, token_service, dummy_password_hash)
    app = create_app(
        register_user=register_user,
        authenticate_user=authenticate_user,
        validate_access_token=ValidateAccessToken(token_service),
        get_own_profile=GetOwnProfile(users),
        list_current_opportunities=ListCurrentOpportunities(
            SecopOpportunitySource(base_url=secop_base_url, timeout_seconds=secop_timeout_seconds),
            ColombiaDateProvider(),
        ),
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
