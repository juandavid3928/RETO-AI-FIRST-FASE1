# Stack técnico aprobado

## Backend

- Python 3.12.
- FastAPI y Uvicorn.
- `uv` para resolución, lock y ejecución del entorno Python.
- PostgreSQL mediante `psycopg`.
- `pydantic-settings` para configuración.
- `pwdlib[argon2]` para hashing Argon2id y Alembic para migraciones SQL explícitas.
- pytest, pytest-asyncio y httpx para pruebas.

## Frontend

- React 18 y React DOM 18.
- TypeScript y Vite.
- Tailwind CSS 4 con `@tailwindcss/vite`.
- React Router DOM 6.
- Zustand.

## Infraestructura

- Docker Compose.
- PostgreSQL 16, backend y frontend como servicios desde HU-001, con entrypoints aprobados y healthchecks.
- Configuración mediante variables de entorno sin secretos versionados.

## Límites

- Arquitectura hexagonal en backend.
- Frontend consume exclusivamente backend.
- Frontend no consume SECOP ni PostgreSQL directamente.
- HU-001 es la única funcionalidad productiva; las demás historias permanecen pendientes.
