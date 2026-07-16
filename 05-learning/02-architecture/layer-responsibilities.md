# Responsabilidades por capa

## Backend hexagonal

- `domain/`: reglas y tipos puros; no depende de FastAPI, psycopg, HTTP ni configuración.
- `application/ports/`: contratos para persistencia e integraciones.
- `application/use_cases/`: orquestación de comportamiento aprobado; depende de dominio y puertos.
- `infrastructure/database/`: futuros adaptadores PostgreSQL con psycopg.
- `infrastructure/external/`: futuros adaptadores externos, incluido SECOP.
- `interfaces/api/v1/`: futuros routers y schemas HTTP de FastAPI.
- `core/`: configuración y composición transversal, sin reglas de negocio.

Las dependencias apuntan hacia dominio y aplicación. Los routers no ejecutarán SQL y los casos de uso no importarán adaptadores concretos.

## Frontend

Presentación, navegación y estado de interfaz. Consume exclusivamente backend; no consume PostgreSQL ni SECOP.

## Database

Persistencia, constraints, índices, migraciones y datos controlados una vez aprobada la HU correspondiente.

## Dirección permitida

```text
frontend -> backend -> database
frontend -> backend -> SECOP
```
