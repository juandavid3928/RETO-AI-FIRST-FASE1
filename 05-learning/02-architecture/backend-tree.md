# Árbol backend aprobado

```text
backend/
├── Dockerfile
├── README.md
├── pyproject.toml
├── uv.lock
├── .python-version
├── .env.example
├── app/
│   ├── __init__.py
│   ├── domain/
│   │   └── __init__.py
│   ├── application/
│   │   ├── __init__.py
│   │   ├── ports/
│   │   │   └── __init__.py
│   │   └── use_cases/
│   │       └── __init__.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── database/
│   │   │   └── __init__.py
│   │   └── external/
│   │       └── __init__.py
│   ├── interfaces/
│   │   ├── __init__.py
│   │   └── api/
│   │       ├── __init__.py
│   │       └── v1/
│   │           └── __init__.py
│   └── core/
│       └── __init__.py
└── tests/
    └── .gitkeep
```

Todos los paquetes están vacíos de comportamiento productivo.
