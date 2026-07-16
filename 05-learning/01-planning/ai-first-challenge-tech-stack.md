# Stack técnico aprobado

## Backend

- Python 3.12.
- FastAPI y Uvicorn.
- `uv` para resolución, lock y ejecución del entorno Python.
- PostgreSQL mediante `psycopg`.
- `pydantic-settings` para configuración.
- pytest, pytest-asyncio y httpx para pruebas.

## Frontend

- React 18 y React DOM 18.
- TypeScript y Vite.
- Tailwind CSS 4 con `@tailwindcss/vite`.
- React Router DOM 6.
- Zustand.

## Infraestructura

- Docker Compose.
- PostgreSQL 16 como único servicio inicial.
- Backend y frontend no serán servicios Compose hasta disponer de entrypoints aprobados.
- Configuración mediante variables de entorno sin secretos versionados.

## Límites

- Arquitectura hexagonal en backend.
- Frontend consume exclusivamente backend.
- Frontend no consume SECOP ni PostgreSQL directamente.
- No existe funcionalidad productiva en la estructura base.
