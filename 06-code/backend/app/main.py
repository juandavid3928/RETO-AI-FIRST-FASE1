from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.bootstrap import build_app
from app.infrastructure.database.config import build_database_conninfo
from app.infrastructure.external.secop_opportunity_source import DEFAULT_BASE_URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str | None = None
    db_host: str | None = None
    db_port: int | None = None
    db_name: str | None = None
    db_user: str | None = None
    db_password: str | None = None
    jwt_secret: str
    secop_base_url: str = DEFAULT_BASE_URL
    secop_timeout_seconds: float = Field(default=5.0, gt=0)

    def database_conninfo(self) -> str:
        return build_database_conninfo(
            self.database_url,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            user=self.db_user,
            password=self.db_password,
        )


settings = Settings()
app = build_app(
    settings.database_conninfo(),
    settings.jwt_secret,
    secop_base_url=settings.secop_base_url,
    secop_timeout_seconds=settings.secop_timeout_seconds,
)
