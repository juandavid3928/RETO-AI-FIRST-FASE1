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
│   │   ├── ports/{clock,id_generator,password_hasher,user_repository}.py
│   │   └── use_cases/register_user.py
│   ├── infrastructure/
│   │   ├── database/postgres_user_repository.py
│   │   ├── password_hasher.py
│   │   └── system.py
│   └── interfaces/api/app.py
└── tests/
    ├── unit/
    ├── api/
    └── integration/
```

Los paquetes usan `__init__.py`. HU-001 es la única lógica productiva: dominio y aplicación no importan FastAPI, Pydantic, psycopg, pwdlib ni infraestructura. HU-002, SECOP y las demás historias permanecen sin implementar.
