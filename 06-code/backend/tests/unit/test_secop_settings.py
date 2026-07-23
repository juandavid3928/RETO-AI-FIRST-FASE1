import importlib
import sys


def reload_main(monkeypatch, **env):
    for key in [
        "DATABASE_URL",
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
        "JWT_SECRET",
        "SECOP_BASE_URL",
        "SECOP_TIMEOUT_SECONDS",
    ]:
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("DATABASE_URL", "postgresql://portal:local@localhost:5432/portal")
    monkeypatch.setenv("JWT_SECRET", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    sys.modules.pop("app.main", None)
    return importlib.import_module("app.main")


def test_secop_settings_default_to_official_dataset_and_five_second_timeout(monkeypatch) -> None:
    main = reload_main(monkeypatch)

    settings = main.Settings()

    assert settings.secop_base_url == "https://www.datos.gov.co/resource/p6dx-8zbt.json"
    assert settings.secop_timeout_seconds == 5.0


def test_secop_settings_accept_env_overrides(monkeypatch) -> None:
    main = reload_main(
        monkeypatch,
        SECOP_BASE_URL="http://127.0.0.1:9000/secop",
        SECOP_TIMEOUT_SECONDS="2.5",
    )

    settings = main.Settings()

    assert settings.secop_base_url == "http://127.0.0.1:9000/secop"
    assert settings.secop_timeout_seconds == 2.5
