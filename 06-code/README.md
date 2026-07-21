# HU-001/HU-002 — Registro e inicio de sesión

Incremento ejecutable del Portal de Convocatorias con registro e inicio de sesión JWT.

- `backend/`: FastAPI y caso de uso hexagonal; persistencia SQL mediante psycopg y migración Alembic explícita.
- `frontend/`: React/Vite/Tailwind con rutas `/register` y `/login`; la sesión JWT se conserva en `localStorage` bajo `portal.auth.session`.
- `docker-compose.yml`: PostgreSQL 16, backend y frontend con healthchecks y orden por salud.

Ejecución local:

```bash
POSTGRES_DB=portal POSTGRES_USER=portal POSTGRES_PASSWORD='<local-only>' JWT_SECRET='<base64url-32-byte-minimum>' docker compose up --build --wait
```

Abrir `http://localhost:8080/register` o `http://localhost:8080/login`. Ningún secreto debe guardarse en archivos versionados.

HU-005 y los recursos privados permanecen fuera de alcance. HU-002 incorpora únicamente emisión/validación JWT, dependencia Bearer reutilizable y logout cliente; no agrega una ruta privada productiva.
