# Architecture readiness review

Estado actual: estructura técnica base validada; arquitectura productiva pendiente de aprobación incremental por HU.

## Base estructural disponible

- Separación frontend/backend/DB.
- Paquetes hexagonales backend completos y vacíos.
- Dependencias backend y frontend bloqueadas mediante herramientas oficiales.
- PostgreSQL 16 como único servicio inicial de Docker Compose.
- Configuración sensible por entorno.
- Integración SECOP reservada para un adaptador backend futuro.
- Sin endpoints, entidades, tablas, pantallas ni lógica productiva.

## Pendiente antes de HU-001

- Aprobar contrato de registro.
- Aprobar modelo mínimo de usuario.
- Aprobar estrategia de pruebas del primer comportamiento.
- Aprobar estrategia de persistencia e integridad para la HU.
