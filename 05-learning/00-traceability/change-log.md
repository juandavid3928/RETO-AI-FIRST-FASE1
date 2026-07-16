# Change log

Bitácora técnica iniciada después del onboarding y la aprobación de reconstrucción. No contiene historial heredado.

## 2026-07-16 — Reset inherited implementation and evidence

**Tipo:** onboarding | documentación | reconstrucción

**Motivo:** El usuario aprobó retirar implementación y evidencia heredadas, conservar conocimiento reutilizable y crear una base vacía.

**Áreas afectadas:**
- `05-learning/`
- `06-code/`
- `SOUL.md`

**Acciones verificadas:**
- Se retiraron 53 archivos heredados de `05-learning/`.
- Se conservaron 9 imágenes PNG como referencia visual no ejecutable.
- Se retiraron 109 archivos de implementación heredada de `06-code/`.
- Se creó documentación neutral y un esqueleto sin funcionalidad.

**Protección:** `1-docs/`, `2-workshops/`, `3-challenge/`, `4-internal/` y archivos raíz fuera de `SOUL.md` permanecieron fuera del alcance.

**Pendiente:** Obtener aprobación de la primera HU antes de implementar código.

## 2026-07-16 — Establish clean project structure

**Tipo:** estructura | tooling | documentación

**Motivo:** Completar la estructura base aprobada antes de iniciar historias de usuario.

**Áreas afectadas:**
- `05-learning/`
- `06-code/`
- `SOUL.md`

**Acciones verificadas:**
- Se completaron los paquetes hexagonales de backend con `__init__.py` y se retiraron cuatro `.gitkeep` innecesarios.
- Se añadieron `app/` y `features/` al esqueleto frontend; permanecen sin código fuente.
- Se declararon las dependencias backend y frontend aprobadas.
- `uv.lock` fue generado por `uv 0.11.29` y validado con `uv lock --check`.
- `package-lock.json` fue generado por npm; `npm install` y `npm ls --depth=0` finalizaron correctamente con 0 vulnerabilidades reportadas.
- El build frontend no fue aplicable porque no existe bootstrap funcional.
- Docker Compose quedó limitado a PostgreSQL 16 y pasó `docker compose config --quiet`.
- La verificación estructural ad hoc comprobó 25 rutas, 12 módulos Python sin comportamiento, 0 fuentes frontend, 0 archivos productivos DB y 9 referencias visuales.
- La búsqueda enfocada de credenciales o secretos hardcodeados produjo 0 coincidencias.

**Límites:** No se crearon endpoints, entidades, casos de uso, tablas, SQL, pantallas, rutas de producto, stores, autenticación ni integración SECOP.

**Pendiente:** Aprobar contrato y microplan de HU-001 antes de implementar comportamiento.
