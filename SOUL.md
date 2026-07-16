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
- La estructura fue integrada mediante PR; todo cambio posterior mantiene prohibidos la integración local y el push directo a `main`.

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
- Se separaron requisitos oficiales, decisiones aprobadas, nueve inferencias y dudas.
- Backlog propuesto: nueve HU para registro, login, browse SECOP, filtros, perfil, favoritos y búsquedas guardadas.
- Se definieron criterios observables, fuentes, valor, prioridad y dependencias sin ciclos.
- Las tareas técnicas permanecen separadas de las historias de usuario.
- Estado: propuesta documental pendiente de revisión; no se creó código ni se inició HU-001.

## Evidencias de producto

Sin pruebas funcionales, builds de aplicación ni flujos E2E: todavía no existe implementación productiva nueva.

## Checkpoint — 2026-07-16 — Pausa antes de completar la cobertura del backlog

### Estado real verificado

- Fase alcanzada: estructura base fusionada y backlog documental refinado; revisión funcional todavía abierta.
- El PR #1 fue fusionado en `main` mediante GitHub; su merge commit es `d374d39c14628b30f6ff84612324eb35603c9daf`.
- `main` local y `origin/main` quedaron sincronizadas en `d374d39c14628b30f6ff84612324eb35603c9daf`.
- Rama activa: `feat/refine-user-stories`, sincronizada con su rama remota antes de redactar este checkpoint.
- Commits documentales previos del PR #2:
  - `35f8f44598fb519c021d5f4c6d222c926795c3d2` — `docs: refine project user stories`.
  - `3448966ff2739460937514e78c7a30562e299159` — `docs: clarify backlog assumptions`.
- El presente checkpoint se añade a la misma rama con el mensaje `docs: record project pause checkpoint`.
- PR #2: abierto hacia `main`, no fusionado y destinado a revisión de Codex y aprobación humana.
- Working tree: limpio antes de iniciar la edición de este checkpoint.
- Diff funcional del PR #2 antes del checkpoint: siete documentos autorizados; `06-code/` sin cambios.
- Backlog existente: 9 HU (`HU-001` a `HU-009`) y 34 criterios de aceptación únicos.
- No existe implementación productiva, prueba funcional, build de aplicación ni flujo E2E.
- Ninguna HU ha comenzado; HU-001 tampoco está autorizada para implementación.

### Avances completados

- Estructura técnica base creada sin comportamiento de producto y fusionada mediante PR #1.
- Problema, actores, flujo, requisitos oficiales, decisiones, inferencias, dudas y límites documentados.
- Nueve HU propuestas con valor, prioridad, dependencias, fuentes, estado y criterios observables.
- Matriz de trazabilidad y tareas técnicas separadas del backlog funcional.
- Revisión independiente incorporada para marcar el acceso privado a browse/filtros como IN-09.

### Validaciones ya observadas

- 9 HU y 34 criterios de aceptación únicos.
- Requisitos obligatorios trazados en la matriz vigente.
- Dependencias circulares: 0; duplicados detectados: 0.
- Secretos o datos personales detectados en el diff documental: 0.
- `git diff --check`: PASS antes de este checkpoint.
- Alcance del PR verificado: solo documentación autorizada; código y archivos protegidos sin cambios.

### Decisiones aprobadas vigentes

- Track DEV, dominio Portal de Convocatorias Públicas y flujo Git mediante PR.
- Stack, arquitectura hexagonal, PostgreSQL 16 e integración SECOP mediante adaptador backend.
- El frontend consume únicamente la API propia.
- Docker Compose permanece limitado a PostgreSQL hasta aprobar entrypoints.
- Ninguna implementación comienza sin aprobación de HU, criterios, contrato y microplan.

### Decisiones e instrucciones pendientes

- Resolver campos de perfil/registro, política de contraseña y ciclo de vida JWT.
- Ratificar si browse/filtros serán privados o públicos.
- Definir dataset, clave estable, DTO, fechas, estados, paginación y orden SECOP.
- Resolver persistencia de bookmarks, búsquedas guardadas y políticas de resiliencia/calidad.
- El backlog actual no contiene `HU-010` ni `HU-011`; por instrucción de pausa, todavía debe resolverse la cobertura funcional de detalle de convocatoria y dashboard.
- No asumir que detalle y dashboard son requisitos oficiales: deben trazarse a fuente verificable o clasificarse explícitamente como inferencia/decisión antes de agregarlos, combinarlos o justificar su cobertura en HU existentes.
- No fusionar el PR #2 hasta completar esa cobertura, repetir las validaciones y obtener revisión de Codex y aprobación humana.
- No iniciar HU-001 ni modificar `06-code/` durante esta pausa.

### Riesgos e inconsistencias conocidas

- El PR #2 presenta el backlog de nueve HU como completo, pero la instrucción de pausa introduce una revisión pendiente sobre detalle y dashboard; esa inconsistencia debe resolverse antes del merge.
- Las referencias visuales incluyen dashboard y detalle, pero por sí solas no tienen autoridad de requisito oficial.
- Búsquedas guardadas son obligatorias en persistencia, aunque su flujo funcional oficial está menos especificado.
- Permanecen abiertos contratos, umbrales no funcionales y semántica de integración SECOP.

### Siguiente acción exacta al reanudar

Revisar el diff y comentarios del PR #2; contrastar detalle de convocatoria y dashboard con las fuentes oficiales y referencias visuales; decidir si corresponden a `HU-010`/`HU-011`, a una división/combinación de HU existentes o a fuera de alcance; actualizar backlog, criterios y trazabilidad; repetir los gates documentales; solicitar revisión de Codex y aprobación humana. No fusionar ni implementar antes de esa decisión.
