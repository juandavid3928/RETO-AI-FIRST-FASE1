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
│   │   └── use_cases/{authenticate_user,register_user,validate_access_token}.py
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

Los paquetes usan `__init__.py`. HU-001 y HU-002 son la lógica productiva vigente: dominio y aplicación no importan FastAPI, Pydantic, psycopg, pwdlib, PyJWT ni infraestructura. SECOP, HU-005 y las demás historias permanecen sin implementar.
