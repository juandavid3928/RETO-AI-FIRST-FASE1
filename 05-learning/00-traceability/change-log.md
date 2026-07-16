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

## 2026-07-16 — Refine complete product backlog

**Tipo:** requisitos | trazabilidad | documentación

**Motivo:** Contrastar las tres historias iniciales con el alcance funcional completo del Track DEV y preparar un backlog verificable para revisión.

**Fuentes inspeccionadas:**
- Enunciado oficial Track DEV y guía oficial del programa.
- `README.md`, `CLAUDE.md`, workshops de Spec Engineering y documentación vigente de `05-learning/`.
- El documento Track QA se clasificó como fuera de autoridad para el producto DEV.

**Acciones:**
- Se separaron requisitos oficiales, decisiones aprobadas, inferencias y dudas.
- Se definieron problema, actores, flujo principal, reglas y límites.
- Se conservaron y refinaron HU-001 y HU-002.
- Se refinó HU-003 y se dividió el alcance de búsqueda con HU-004.
- Se agregaron HU-005 a HU-009 para cubrir perfil, favoritos y búsquedas guardadas.
- Se documentaron criterios observables, dependencias sin ciclos, prioridad P0 y matriz de trazabilidad.
- Se separaron ocho tareas técnicas habilitadoras de las historias de usuario.

**Validaciones observadas:**
- Verificación documental ad hoc inicial: 7 rutas autorizadas, 9 HU, 34 criterios, 9 requisitos oficiales, 8 inferencias y 8 tareas técnicas; 0 ciclos y 0 fallos.
- `git diff --check`: PASS.
- El primer intento del verificador produjo falsos negativos al no aceptar las flexiones «Dada/Dados»; se corrigió únicamente el harness temporal y se repitió con resultado PASS.
- Una revisión independiente posterior confirmó la cobertura y detectó que el acceso privado a browse/filtros debía marcarse como IN-09; también separó las restricciones AI-First de las HU.

**Áreas afectadas:**
- `05-learning/03-requirements/`
- `05-learning/00-traceability/change-log.md`
- `SOUL.md`

**Límites:** No se modificó `06-code/`, no se implementó ninguna HU y el backlog permanece pendiente de revisión y aprobación.

**Pendiente:** Resolver las decisiones abiertas y aprobar criterios, contrato y microplan de HU-001 antes de crear código.
