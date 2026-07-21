# Database

PostgreSQL 16 persiste las cuentas de HU-001. La migración ejecutable reside junto al backend en `backend/alembic/`, de modo que el mismo artefacto que inicia la API la aplica antes de servir tráfico.

Alembic ejecuta SQL explícito para crear y retirar `users`; el runtime utiliza psycopg sin ORM. No existen seeds ni datos personales de ejemplo.
