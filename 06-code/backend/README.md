# Backend HU-001

Python 3.12, FastAPI, psycopg y `pwdlib[argon2]`, gestionados con `uv`. Dominio y aplicación no importan frameworks ni infraestructura. Los puertos abstraen repositorio, hashing, reloj e IDs.

Ejecución local con una URL suministrada por entorno:

```bash
uv sync --frozen
DATABASE_URL='postgresql://...' uv run alembic upgrade head
DATABASE_URL='postgresql://...' uv run uvicorn app.main:app
```

Pruebas unitarias y de contrato API, sin PostgreSQL externo:

```bash
uv run pytest tests/unit tests/api -q
```

Suite completa con PostgreSQL 16 real disponible y migrable:

```bash
TEST_DATABASE_URL='postgresql://...' uv run pytest -q
```

Compose no construye URLs con credenciales: entrega `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` y `DB_PASSWORD` por separado para admitir caracteres reservados de forma segura.

Contrato implementado: `POST /api/v1/auth/register`. Usa UUID4, correo canónico y hash Argon2id; no entrega JWT. Alembic usa SQL explícito y el runtime no usa ORM.
