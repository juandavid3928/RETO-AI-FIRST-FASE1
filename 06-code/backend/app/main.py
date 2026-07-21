from pydantic_settings import BaseSettings, SettingsConfigDict

from app.bootstrap import build_app


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str


app = build_app(Settings().database_url)
