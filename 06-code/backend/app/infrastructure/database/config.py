from psycopg.conninfo import make_conninfo


def build_database_conninfo(
    database_url: str | None,
    *,
    host: str | None = None,
    port: int | None = None,
    database: str | None = None,
    user: str | None = None,
    password: str | None = None,
) -> str:
    if database_url:
        return database_url

    values = {
        "host": host,
        "port": port,
        "database": database,
        "user": user,
        "password": password,
    }
    missing = [name for name, value in values.items() if value is None]
    if missing:
        raise ValueError(f"Missing database settings: {', '.join(missing)}")

    return make_conninfo(
        host=host,
        port=port,
        dbname=database,
        user=user,
        password=password,
    )
