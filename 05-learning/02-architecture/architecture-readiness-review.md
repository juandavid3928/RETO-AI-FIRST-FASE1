# Architecture readiness review

Estado actual: arquitectura productiva de HU-001 fusionada y HU-002 implementada localmente; cualquier ampliación permanece sujeta a aprobación incremental.

## Incremento productivo disponible

- Separación frontend/backend/DB.
- Dominio y aplicación hexagonales de HU-001/HU-002 con puertos explícitos y sin imports de frameworks o infraestructura.
- Dependencias backend y frontend bloqueadas mediante herramientas oficiales.
- PostgreSQL 16, backend FastAPI y frontend nginx como servicios Docker Compose con healthchecks.
- Configuración sensible por entorno.
- Integración SECOP reservada para un adaptador backend futuro.
- Capacidades productivas: registro y login en `POST /api/v1/auth/{register,login}`, pantallas `/register` y `/login`, emisión/validación JWT y dependencia Bearer reutilizable. No existe una ruta privada de producto; HU-003 a HU-011 permanecen sin implementación.

## Decisiones resueltas para HU-001/HU-002

- Contratos de registro, login, JWT y Bearer aprobados en `auth-api-contract.md`.
- Dominio/aplicación aislados mediante puertos de repositorio, hash, reloj e ID.
- PostgreSQL 16, psycopg runtime y Alembic SQL explícito adoptados para persistencia.
- Estrategia TDD cubre unidad, aplicación, API, PostgreSQL real, migración, concurrencia, componentes, build, Compose y E2E.

HU-002 está implementada y validada localmente, pendiente de publicación y revisión mediante PR. HU-005 no está iniciada.
