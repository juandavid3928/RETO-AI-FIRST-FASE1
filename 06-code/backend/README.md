# Backend HU-001/HU-002/HU-005

Python 3.12, FastAPI, psycopg y `pwdlib[argon2]`, gestionados con `uv`. Dominio y aplicación no importan frameworks ni infraestructura. Los puertos abstraen repositorio, hashing, reloj e IDs.

Ejecución local con una URL suministrada por entorno:

```bash
uv sync --frozen
DATABASE_URL='postgresql://...' uv run alembic upgrade head
DATABASE_URL='postgresql://...' JWT_SECRET='<base64url-32-byte-minimum>' uv run uvicorn app.main:app
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

Contratos implementados: `POST /api/v1/auth/register`, `POST /api/v1/auth/login` y `GET /api/v1/users/me`. Login verifica Argon2id —incluido hash dummy para cuentas inexistentes— y emite JWT HS256 de 1800 segundos con `sub`, `iss`, `aud`, `iat` y `exp`. Perfil reutiliza la validación Bearer, deriva el lookup exclusivamente de `AuthenticatedPrincipal.user_id` y devuelve exactamente `id`, `email` y `created_at` con headers privados. `JWT_SECRET` es obligatorio, base64url y de al menos 32 bytes decodificados. Alembic usa SQL explícito, HU-005 no añade migraciones y el runtime no usa ORM.
