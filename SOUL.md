# SOUL — Reto AI-First Fase 1

## Identidad

- Track: DEV.
- Estado: estructura técnica base completada; producto funcional pendiente.
- Evidencia válida: únicamente la generada desde el onboarding aprobado del 2026-07-16.

## Reglas operativas

- No atribuir código ni evidencia heredada al proceso actual.
- No modificar `1-docs/`, `2-workshops/`, `3-challenge/` ni `4-internal/`.
- No almacenar ni exponer secretos.
- No ejecutar commit, push, PR o merge sin autorización explícita.
- Flujo Git obligatorio: rama de trabajo → cambios → validaciones → commit → push de la rama → PR hacia `main` → revisión → merge mediante GitHub.
- El push directo a `main` queda prohibido después de la excepción única usada para publicar la base inicial.
- Trabajar incrementalmente con HU aprobadas.

## Decisiones vigentes

- Track DEV confirmado.
- Stack base aprobado: Python 3.12, FastAPI, Uvicorn, psycopg, pydantic-settings, PostgreSQL 16, React 18, React Router DOM 6, Zustand, TypeScript, Vite, Tailwind CSS 4 y Docker Compose.
- Backend organizado mediante arquitectura hexagonal.
- Docker Compose contiene únicamente PostgreSQL hasta disponer de entrypoints aprobados.
- Backlog funcional propuesto para revisión: HU-001 a HU-009; no autoriza implementación.
- La estructura se integra mediante PR; no se permite integración local ni push directo a `main`.

## Checkpoint — 2026-07-16 — Reinicio aprobado del repositorio

- Avance verificado: se retiró la implementación heredada y se creó una base documental y estructural limpia.
- Alcance: `05-learning/`, `06-code/` y `SOUL.md`.
- Evidencia:
  - 53 archivos heredados retirados de `05-learning/`.
  - 9 PNG preservados como referencia visual no ejecutable.
  - 109 archivos heredados retirados de `06-code/`.
  - Esqueleto creado sin endpoints, schema SQL ni pantallas.
- Decisión: la ejecución fue autorizada explícitamente después del reporte de clasificación.

## Checkpoint — 2026-07-16 — Estructura técnica base

- Se completó la separación hexagonal obligatoria del backend.
- Se completaron las carpetas frontend aprobadas sin crear bootstrap ni comportamiento.
- Se conservaron vacías las carpetas DB.
- Se crearon Dockerfiles, nginx y Docker Compose sin servicios backend/frontend.
- Los locks fueron generados exclusivamente por `uv` y npm.
- Validaciones observadas:
  - `uv lock --check`: PASS.
  - `npm install`: PASS; 0 vulnerabilidades reportadas.
  - `npm ls --depth=0`: PASS.
  - Build frontend: no aplicable por ausencia deliberada de bootstrap.
  - `docker compose config --quiet`: PASS.
  - Verificación estructural ad hoc: PASS.
  - Búsqueda enfocada de secretos hardcodeados: 0 coincidencias.
- Producto funcional: inexistente.
- Próximo paso: revisar y aprobar el backlog; después, aprobar contrato y microplan de HU-001.

## Checkpoint — 2026-07-16 — Refinamiento integral del backlog

- Se contrastó el alcance inicial con el enunciado oficial Track DEV, la guía del programa y la documentación vigente.
- Se separaron requisitos oficiales, decisiones aprobadas, inferencias y dudas.
- Backlog propuesto: nueve HU para registro, login, browse SECOP, filtros, perfil, favoritos y búsquedas guardadas.
- Se definieron criterios observables, fuentes, valor, prioridad y dependencias sin ciclos.
- Las tareas técnicas permanecen separadas de las historias de usuario.
- Estado: propuesta documental pendiente de revisión; no se creó código ni se inició HU-001.

## Evidencias de producto

Sin pruebas funcionales, builds de aplicación ni flujos E2E: todavía no existe implementación productiva nueva.
