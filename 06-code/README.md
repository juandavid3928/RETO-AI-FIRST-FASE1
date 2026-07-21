# HU-001 — Registro de usuarios

Incremento ejecutable del Portal de Convocatorias con registro de usuarios únicamente.

- `backend/`: FastAPI y caso de uso hexagonal; persistencia SQL mediante psycopg y migración Alembic explícita.
- `frontend/`: React/Vite/Tailwind con la única ruta `/register`.
- `docker-compose.yml`: PostgreSQL 16, backend y frontend con healthchecks y orden por salud.

Ejecución local:

```bash
POSTGRES_DB=portal POSTGRES_USER=portal POSTGRES_PASSWORD='<local-only>' docker compose up --build --wait
```

Abrir `http://localhost:8080/register`. Ningún secreto debe guardarse en archivos versionados.

HU-002 y las capacidades de login/JWT permanecen fuera de alcance.
