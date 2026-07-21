# Backend HU-001

Python 3.12, FastAPI, psycopg y `pwdlib[argon2]`, gestionados con `uv`. Dominio y aplicación no importan frameworks ni infraestructura. Los puertos abstraen repositorio, hashing, reloj e IDs.

```bash
uv sync --frozen
DATABASE_URL='postgresql://...' uv run alembic upgrade head
DATABASE_URL='postgresql://...' uv run uvicorn app.main:app
uv run pytest -q
```

Contrato implementado: `POST /api/v1/auth/register`. Usa UUID4, correo canónico y hash Argon2id; no entrega JWT. Alembic usa SQL explícito y el runtime no usa ORM.
