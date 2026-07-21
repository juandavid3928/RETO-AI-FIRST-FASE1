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
- Backlog funcional propuesto para revisión: HU-001 a HU-011; no autoriza implementación.
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
- Se separaron requisitos oficiales, decisiones aprobadas, once inferencias y dudas.
- Backlog propuesto: once HU para registro, login, browse SECOP, filtros, perfil, favoritos, búsquedas guardadas, detalle mínimo y dashboard resumen.
- Se definieron 43 criterios observables, fuentes, valor, prioridad y dependencias sin ciclos.
- Las tareas técnicas permanecen separadas de las historias de usuario.
- Estado: propuesta documental pendiente de revisión; no se creó código ni se inició HU-001.

## Evidencias de producto

HU-001 es el primer incremento productivo nuevo. Las evidencias anteriores al 2026-07-21 siguen siendo históricas; la evidencia vigente está en el checkpoint final de este archivo.

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
- Backlog vigente: 11 HU (`HU-001` a `HU-011`) y 43 criterios de aceptación únicos.
- No existe implementación productiva, prueba funcional, build de aplicación ni flujo E2E.
- Ninguna HU ha comenzado; HU-001 tampoco está autorizada para implementación.

### Avances completados

- Estructura técnica base creada sin comportamiento de producto y fusionada mediante PR #1.
- Problema, actores, flujo, requisitos oficiales, decisiones, inferencias, dudas y límites documentados.
- Once HU propuestas con valor, prioridad, dependencias, fuentes, estado y criterios observables.
- HU-010 cubre únicamente el detalle mínimo; HU-011 resume información ya respaldada sin analítica, recomendaciones ni métricas externas.
- Matriz de trazabilidad y tareas técnicas separadas del backlog funcional.
- Revisión independiente incorporada para marcar el acceso privado a browse/filtros como IN-09.

### Validaciones ya observadas

- 11 HU y 43 criterios de aceptación únicos.
- HU-010 aporta 4 criterios y HU-011 aporta 5 criterios observables.
- Requisitos obligatorios y la decisión AP-07 están trazados en las matrices vigentes.
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
- La cobertura de detalle y dashboard quedó resuelta por AP-07, HU-010, HU-011, IN-10 e IN-11; ya no bloquea el PR #2 por ausencia funcional.
- La clasificación se mantiene explícita: AP-07 es la instrucción aprobada; las referencias visuales no son requisitos oficiales.
- El PR #2 queda pendiente de revisión de Codex y aprobación humana, no de nuevas HU.
- No iniciar HU-001 ni modificar `06-code/` sin la aprobación posterior correspondiente.

### Riesgos e inconsistencias conocidas

- La inconsistencia de cobertura del PR #2 quedó resuelta con once HU; debe evitarse que la descripción remota conserve conteos o bloqueos anteriores.
- Las referencias visuales incluyen dashboard y detalle, pero por sí solas no tienen autoridad de requisito oficial; AP-07 acota ambas capacidades.
- Búsquedas guardadas son obligatorias en persistencia, aunque su flujo funcional oficial está menos especificado.
- Permanecen abiertos contratos, umbrales no funcionales y semántica de integración SECOP.

### Siguiente acción exacta al reanudar

Revisar en Codex el diff completo del PR #2 con HU-010/HU-011 y sus 43 criterios; aprobar o solicitar ajustes. No fusionar ni implementar durante esta iteración.

## Checkpoint — 2026-07-21 — Cobertura funcional completa del backlog

- Avance verificado: se conservaron HU-001 a HU-009 y se incorporaron HU-010 — Consultar detalle de convocatoria y HU-011 — Visualizar dashboard resumen.
- Alcance: únicamente `05-learning/03-requirements/`, `05-learning/00-traceability/change-log.md` y `SOUL.md`.
- Evidencia documental:
  - 11 HU únicas y numeradas de HU-001 a HU-011.
  - 43 criterios únicos: 4 nuevos para HU-010 y 5 nuevos para HU-011.
  - Grafo de dependencias dirigido sin ciclos.
  - Matrices requisito→HU y HU→fuente/dependencia actualizadas.
  - `git diff --check`: PASS.
  - Verificación documental ad hoc y revisión de rutas/secretos: PASS.
- Decisión: AP-07 registra la instrucción aprobada; HU-010 queda limitada al detalle mínimo y HU-011 al resumen de convocatorias visibles, favoritos y búsquedas guardadas, sin analítica, recomendaciones ni métricas externas.
- Riesgos/Bloqueos: se retiró el bloqueo por ausencia de HU-010/HU-011; permanecen decisiones de contrato y la revisión humana normal del PR.
- Producto funcional: inexistente; no se modificó `06-code/` ni se implementó ninguna HU.
- Próximo paso: revisión de Codex sobre el PR #2; no hacer merge ni iniciar implementación en esta iteración.

## Checkpoint — 2026-07-21 — HU-001 registro end-to-end

- Alcance: exclusivamente creación de cuenta; HU-002 sigue pendiente y no se implementaron login, JWT, roles, verificación, recuperación ni perfil editable.
- Decisiones: email recortado y canónico, password de 12..128 sin composición, UUID4, Argon2id, PostgreSQL como autoridad de concurrencia y errores HTTP estables.
- Arquitectura: `Email`, `UserId`, `User` y caso de uso hexagonal con puertos de repositorio, hash, reloj e ID; FastAPI, Pydantic, psycopg y pwdlib permanecen fuera de dominio/aplicación.
- Persistencia: migración Alembic SQL reversible con UUID primary key, email canónico único, hash no nulo y `created_at`/`updated_at` con zona.
- UI: única ruta `/register`, confirmación solo local, siete estados observables, doble envío bloqueado, permanencia en página y limpieza de campos sensibles al éxito.
- Runtime: PostgreSQL 16, backend y frontend en Compose; migración al arrancar, healthchecks, dependencias saludables y credenciales DB separadas que admiten caracteres reservados.
- RED: fallos de importación/colección del backend, ausencia de Alembic, ausencia de Vitest/Playwright y Compose sin servicios fueron observados antes de GREEN; evidencia auxiliar en `/tmp/hu001-red-evidence.txt`.
- Evidencia GREEN fresca: backend `32 passed`; frontend `8 passed`; build Vite exitoso; Playwright E2E `1 passed`; `npm audit` sin vulnerabilidades; `uv lock --check` y Compose válidos.
- Seguridad: SQL parametrizado, rollback/close de mejor esfuerzo sin ocultar indisponibilidad, Argon2id, errores sin detalles internos, límite real de 4 KiB y ausencia de password/hash/JWT en respuestas o almacenamiento frontend.
- Estado: implementación pendiente de revisión mediante PR; no se hizo merge y HU-002 no fue iniciada.

## Checkpoint — 2026-07-21 — HU-002 login JWT local

- Alcance: login como segundo incremento vertical sobre HU-001; HU-005, perfil y demás recursos privados no fueron iniciados.
- Contrato: JSON estricto `email`/`password`, password opaca de 1..128, respuesta Bearer con TTL 1800, errores uniformes y cuerpo máximo de 4 KiB.
- Arquitectura: casos de uso de autenticación/validación dependen de puertos; FastAPI, Pydantic, psycopg, pwdlib y PyJWT permanecen fuera de dominio/aplicación.
- Seguridad: Argon2id y hash dummy, HS256 fijo, UUID4/issuer/audience/`iat`/`exp` tipados, TTL exacto, leeway 30, secreto runtime base64url mínimo 32 bytes, headers no-store y Bearer sin OAuth2 form.
- UI: `/login` persiste únicamente `{ accessToken, expiresAt }` bajo `portal.auth.session`, valida estructura, restaura/expira, limpia estado y temporizadores, y realiza logout exclusivamente cliente.
- TDD: RED/GREEN cubrió credenciales uniformes, JWT alterado/claims/ventana, configuración fail-fast, API, PostgreSQL, storage, contrato 200 y UI accesible.
- Evidencia actual: backend unitario/API 70 passed; JWT focalizado 25 passed; frontend 27 passed; build Vite, locks, audit, frontera hexagonal y `git diff --check` en verde.
- Validación integral: PostgreSQL 16 vacío + Alembic; backend 76 passed; frontend 27 passed; build/audit; y Playwright conjunto registro/login 2 passed después de restaurar el esquema desmontado por la prueba explícita de downgrade.
- Revisión: un primer FAIL independiente detectó TTL/audience y documentación; tras los correctivos, una segunda revisión independiente emitió PASS sin bloqueantes sobre un snapshot estable.
- Riesgos: `localStorage` mantiene riesgo XSS residual, logout no revoca JWT y rate limiting queda como hardening previo a producción.
- Estado Git: cambios locales en `feat/hu-002-user-login`; sin commit, push ni merge.
