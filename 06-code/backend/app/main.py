from pydantic_settings import BaseSettings, SettingsConfigDict

from app.bootstrap import build_app
from app.infrastructure.database.config import build_database_conninfo


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str | None = None
    db_host: str | None = None
    db_port: int | None = None
    db_name: str | None = None
    db_user: str | None = None
    db_password: str | None = None
    jwt_secret: str

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
app = build_app(settings.database_conninfo(), settings.jwt_secret)
