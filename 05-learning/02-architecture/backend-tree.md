# Árbol backend vigente

```text
backend/
├── Dockerfile
├── README.md
├── pyproject.toml
├── uv.lock
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/20260721_0001_create_users.py
├── app/
│   ├── main.py
│   ├── bootstrap.py
│   ├── domain/
│   │   ├── errors.py
│   │   └── user.py
│   ├── application/
│   │   ├── errors.py
│   │   ├── ports/{access_token,clock,id_generator,password_hasher,password_verifier,user_repository}.py
│   │   └── use_cases/{authenticate_user,get_own_profile,register_user,validate_access_token}.py
│   ├── infrastructure/
│   │   ├── database/postgres_user_repository.py
│   │   ├── jwt_access_token.py
│   │   ├── password_hasher.py
│   │   └── system.py
│   └── interfaces/api/app.py
└── tests/
    ├── unit/
    ├── api/
    └── integration/
```

HU-001, HU-002 y HU-005 son la lógica productiva vigente en la rama de perfil. Dominio y aplicación no importan FastAPI, Pydantic, psycopg, pwdlib, PyJWT ni infraestructura. `GetOwnProfile` consume `AuthenticatedPrincipal`, consulta `UserRepository.get_by_id` y devuelve únicamente la proyección `OwnProfile`; no existe endpoint para consultar otro usuario. La migración original de `users` permanece sin cambios. SECOP y las demás historias no están implementadas.
