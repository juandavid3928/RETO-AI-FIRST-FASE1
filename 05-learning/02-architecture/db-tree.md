# Persistencia vigente

```text
06-code/
├── backend/
│   ├── alembic.ini
│   └── alembic/
│       ├── env.py
│       └── versions/20260721_0001_create_users.py
└── db/
    ├── README.md
    ├── migrations/
    ├── seeds/
    ├── schemas/
    ├── indexes/
    ├── scripts/
    └── test-data/
```

La migración ejecutable de HU-001 vive junto al backend para quedar dentro de su contexto de build. Crea y revierte `users` mediante Alembic con SQL explícito. Las carpetas `db/` restantes continúan reservadas y no contienen seeds, roles, sesiones, tokens ni datos personales.
