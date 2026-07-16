# Estructura técnica base

Esqueleto limpio del Track DEV. Declara el stack y los límites arquitectónicos, pero no implementa HU-001, HU-002 ni HU-003.

- `backend/`: paquetes hexagonales vacíos y dependencias bloqueadas con `uv`.
- `frontend/`: dependencias React/Vite declaradas, sin bootstrap ni UI funcional.
- `db/`: directorios vacíos, sin SQL.
- `docker-compose.yml`: PostgreSQL 16 como único servicio inicial.

Backend y frontend no están incluidos como servicios Compose porque no existen entrypoints aprobados.
