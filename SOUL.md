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

## Checkpoint — 2026-07-21 — Hardening de sesión frontend HU-002

- Avance verificado: sesión extraída a un módulo dedicado, contrato `200` exacto, sincronización multitab y reevaluación al recuperar visibilidad; `authenticatedFetch` permanece explícitamente pendiente.
- Alcance/HU: solo HU-002 frontend y su documentación; HU-005 y llamadas privadas no fueron iniciadas.
- Evidencia RED: 8 fallos focalizados de contrato/multitab/visibilidad/cleanup, fallo inicial por ausencia del módulo y 2 RED adicionales para JSON `200` inválido/campos de sesión extra.
- Evidencia de suites: frontend 41 passed; backend PostgreSQL 16 real 76 passed; Playwright registro/login 2 passed; build Vite, audit, lock, Compose config, CSP/cabeceras, escaneo de secretos y `git diff --check` en verde.
- Recuperación validada: la prueba de downgrade dejó una sola tabla de control; `alembic upgrade head` restauró `users` y `alembic_version` antes del E2E.
- Limpieza: contenedores, red, volumen, env efímero, script temporal y artefactos Playwright eliminados por trap.
- Riesgos: continúan el riesgo XSS residual de `localStorage`, la ausencia de revocación inmediata y el rate limiting pendiente.
- Próximo paso: crear y publicar el commit `fix: harden frontend authentication session` en el PR #4, sin merge.

## Checkpoint — 2026-07-21 — HU-005 perfil propio privado

- Alcance: exclusivamente HU-005 como primer incremento privado React → FastAPI → PostgreSQL; ninguna otra HU fue iniciada.
- Contrato: `GET /api/v1/users/me`, perfil exacto `id`/`email`/`created_at`, identidad únicamente desde `AuthenticatedPrincipal.user_id`, usuario eliminado como `401 invalid_token` y headers privados en todas las respuestas.
- Arquitectura: `GetOwnProfile` y `OwnProfile` permanecen en aplicación, `UserRepository.get_by_id` abstrae persistencia y dominio/aplicación continúan sin frameworks ni infraestructura.
- Persistencia: consulta UUID parametrizada por primary key con cierre/rollback seguros; tabla `users`, migración y JWT permanecen sin cambios.
- UI/sesión: `/profile`, `AuthSessionProvider`, `RequireAuth`, `authenticatedFetch` same-origin, login con `replace`, logout/`401` hacia `/login` y perfil únicamente en memoria.
- RED observado: ausencia de caso de uso, 3 fallos de repositorio, 5 fallos de API, import ausente y 8 fallos iniciales frontend; la regresión detectó además 2 expectativas obsoletas. El primer E2E integral encontró 1 fallo de harness por no entregar `TEST_DATABASE_URL` a la prueba heredada y motivó repetición completa.
- Evidencia final fresca: backend PostgreSQL 16 real 89 passed; frontend 58 passed; build Vite PASS; Playwright registro/login/perfil 3 passed; esquema `20260721_0001 (head)`.
- Seguridad/calidad: aislamiento adversarial, token alterado, usuario eliminado, respuesta exacta, no-store/no-cache/Vary, CSP, audit 0, lock, Compose config, frontera hexagonal, secretos y `git diff --check` en verde.
- Limpieza: credenciales/JWT y puertos efímeros; trap eliminó contenedores, red, volumen, env y artefactos Playwright.
- Riesgos: `localStorage` conserva riesgo XSS residual, logout no revoca JWT y rate limiting continúa pendiente antes de producción.
- Revisión independiente posterior: el hallazgo alto de traversal ya estaba resuelto mediante canonicalización y pruebas; se resolvieron además la normalización UTC de `created_at`, el `TEST_DATABASE_URL` faltante en el README E2E y la descripción inexacta del estado `unauthorized`. La validación afectada terminó backend unitario/API 82 passed, frontend 58 passed y build PASS.
- Estado: cambios en `feat/hu-005-own-profile`, pendientes de revisión mediante PR; sin merge.

## Checkpoint — 2026-07-21 — Pausa tras HU-005

### Estado real verificado
- PR #1 y #2 fusionados: estructura limpia y refinamiento del backlog, respectivamente.
- HU-001 completada y fusionada mediante PR #3; merge `f1a82ef`.
- HU-002 completada y fusionada mediante PR #4; merge `34f25f2`.
- HU-005 completada y fusionada mediante PR #5; merge `940da47`.
- `main` local se verificó limpia, sincronizada con `origin/main` y en `940da47a0b9d887e0593b153685c540515ff7790` inmediatamente antes de crear `docs/project-pause-checkpoint`.
- El producto implementado comprende registro, login JWT y consulta del perfil propio; backend, frontend, PostgreSQL 16 y Docker Compose quedaron operativos en la validación integral final.
- No se inició ninguna HU adicional. En particular, el análisis y la implementación de HU-003 permanecen pendientes.

### Validaciones finales conocidas
- Suite backend completa contra PostgreSQL 16 real desde volumen vacío: 90 passed.
- Suite frontend completa: 58 passed; Playwright conjunto registro/login/perfil: 3 passed.
- Build Vite, `npm audit`, `uv lock --check`, Compose config, CSP, headers privados, frontera hexagonal, escaneo de secretos y `git diff --check`: PASS.
- Alembic fue restaurado a `20260721_0001 (head)` después de las pruebas con downgrade.
- La limpieza automática eliminó contenedores, red, volumen, env, script temporal, `dist` y artefactos Playwright; una comprobación posterior confirmó cero recursos o temporales HU-005 restantes.

### Riesgos vigentes
- Riesgo XSS residual por persistir el JWT en `localStorage`.
- Logout local sin revocación inmediata del token.
- Rate limiting pendiente antes de producción.
- Advertencia Starlette/TestClient no bloqueante.

### Respaldo y siguiente acción
- Se conserva `backup/repository-structure-a0dfd0a` en `a0dfd0a5250fadd372d8c4d8e3a32a0504710f70` para preservar el checkpoint de la estructura limpia inicial.
- Al reanudar: analizar HU-003 y confirmar el dataset y el contrato de SECOP II. No implementar HU-003 sin una nueva instrucción de Codex.

## Checkpoint — 2026-07-22 — Análisis documental HU-003 SECOP II

- Alcance: análisis técnico/documental previo a implementación de HU-003; no se modificó `06-code/` ni se inició ninguna HU.
- Estado Git previo: PR #6 fusionado mediante GitHub, `main` sincronizada por fast-forward y rama `docs/project-pause-checkpoint` eliminada local/remotamente después de verificar que `00d3dc9cace43273a7914d13ee6f522b1dc776c8` quedó como ancestro de `main`.
- Fuente recomendada: datos.gov.co `SECOP II - Procesos de Contratación` (`p6dx-8zbt`), consultado por el backend mediante `https://www.datos.gov.co/resource/p6dx-8zbt.json`.
- Definición propuesta de vigencia: `estado_de_apertura_del_proceso = 'Abierto'` y `fecha_de_recepcion_de >= fecha actual`; registros sin fecha de recepción confiable quedan fuera del browse inicial.
- Contrato propuesto: `GET /api/v1/opportunities`, privado con Bearer JWT, paginado (`page=1`, `page_size=20`, máximo 50), timeout externo inicial de 5 segundos, orden por cierre ascendente y DTO normalizado con `id_del_proceso` como clave estable propuesta.
- Estados UI definidos: `loading`, `empty`, `external_error` y `success`; frontend consume únicamente API propia y no llama directamente a datos.gov.co.
- Riesgos documentados: disponibilidad/rate limits de datos.gov.co, cambios de esquema, datos incompletos, semántica de vigencia, duplicados y monto COP sin conversión a centavos en el listado.
- Decisiones pendientes: ratificar dataset, clave estable, fecha de vigencia, endpoint/DTO, privacidad, paginación/orden/timeout antes de autorizar implementación TDD.

## Checkpoint — 2026-07-23 — HU-003 exploración de convocatorias vigentes

- Alcance: exclusivamente HU-003 browse/listado inicial de convocatorias vigentes SECOP II. No se iniciaron HU-004 filtros, HU-010 detalle, favoritos, búsquedas guardadas ni dashboard.
- Fuente externa implementada: datos.gov.co `SECOP II - Procesos de Contratación` (`p6dx-8zbt`) vía `https://www.datos.gov.co/resource/p6dx-8zbt.json`; `SECOP_BASE_URL` queda como override opcional para stubs determinísticos.
- Contrato backend: `GET /api/v1/opportunities?page=1&page_size=20`, privado con Bearer JWT, headers `Cache-Control: no-store`, `Pragma: no-cache`, `Vary: Authorization`, `401` sin sesión válida, `422` por paginación inválida, `503 external_service_unavailable` para fallos SECOP y `200` con página normalizada.
- Vigencia implementada: fecha actual de Colombia calculada en backend; SoQL acotado con `estado_de_apertura_del_proceso='Abierto'`, `fecha_de_recepcion_de >= YYYY-MM-DDT00:00:00`, `id_del_proceso` obligatorio, orden por `fecha_de_recepcion_de`, `fecha_de_publicacion_del` e `id_del_proceso`.
- DTO final: `id`, `reference`, `entity_name`, `title`, `description`, `status`, `summary_status`, `opening_status`, `published_at`, `closing_at`, `estimated_amount_cop`, `source_url`; `estimated_amount_cop` permanece en COP sin conversión a centavos.
- Frontend: ruta privada `/opportunities`, navegación mínima desde `/profile`, `authenticatedFetch`, parser estricto, estados `loading`, `empty`, `external_error` y `success`, sin persistir oportunidades en `localStorage`.
- TDD: RED observado para imports/route ausente en backend y frontend antes de GREEN; GREEN con backend unitario/API HU-003, suite frontend, build y E2E determinístico con stub SECOP.
- Evidencia final: backend completo contra PostgreSQL 16 real `107 passed`; frontend `64 passed`; Playwright registro/login/perfil/oportunidades `4 passed`; build Vite PASS; `npm audit` 0 vulnerabilidades; `uv lock --check`, Compose config y consulta viva SECOP acotada PASS.
- Persistencia: no se crearon migraciones, no se modificó la tabla `users` y no se persisten oportunidades.
- Riesgos residuales: disponibilidad/rate limits/cambios de esquema de datos.gov.co, unicidad futura de `id_del_proceso` antes de favoritos, y riesgo XSS residual por JWT en `localStorage` ya conocido.

## Checkpoint — 2026-07-23 — Correcciones revisión Codex HU-003

- Alcance: corrección exclusiva de hallazgos HU-003 sobre validación `422` de `/api/v1/opportunities` y configuración SECOP. No se iniciaron HU-004, HU-010 ni otras HUs.
- API: los errores de query inválida en `GET /api/v1/opportunities` devuelven `422 validation_error` con mensaje `Opportunity query is invalid.`, no invocan el caso de uso y conservan headers privados.
- Configuración: `SECOP_BASE_URL` y `SECOP_TIMEOUT_SECONDS` quedan integrados al flujo `Settings`/`.env`; `bootstrap.py` ya no lee `os.getenv()` directamente.
- Defaults: `SECOP_BASE_URL=https://www.datos.gov.co/resource/p6dx-8zbt.json` y `SECOP_TIMEOUT_SECONDS=5`.
- Adaptador SECOP: recibe timeout configurable y lo aplica a la solicitud HTTP externa.
- Persistencia y alcance: no se agregaron migraciones, tablas ni persistencia de oportunidades.

## Checkpoint — 2026-07-22 — Análisis documental HU-004 filtros

- Alcance: análisis/microplan documental de HU-004 — Filtrar convocatorias. No se modificó `06-code/`, no se crearon pruebas productivas ni E2E y no se inició HU-010, HU-006, HU-007, HU-008, HU-009, HU-011 ni otra HU.
- Estado base: HU-003 fusionada en `main` mediante PR #8; merge commit `44a915acd905dadd562279202dd4c71ea5c1a4f0`; `main` sincronizada con `origin/main` antes de crear `docs/hu-004-filter-contract-analysis`.
- Contrato propuesto: extender `GET /api/v1/opportunities` con query params opcionales `entity`, `closing_from`, `closing_to` y `status`, preservando Bearer JWT, paginación, DTO, headers privados y errores de HU-003.
- Semántica propuesta: `entity` usa coincidencia parcial case-insensitive sobre `entidad` con normalización 3..120 caracteres; fechas `YYYY-MM-DD` inclusivas sobre `fecha_de_recepcion_de` en fecha civil Colombia; `status` inicial recomendado como `presentation` mapeado a `estado_resumen='Presentación de oferta'` sin relajar `estado_de_apertura_del_proceso='Abierto'`.
- Validaciones: filtros inválidos devuelven `422 validation_error` con mensaje `Opportunity query is invalid.`, fields por parámetro y garantía de no consultar SECOP; filtros válidos sin coincidencias producen `empty`, no error externo.
- Frontend propuesto: formulario accesible con entidad, rango, estado, aplicar y limpiar; conserva resultados ante errores de validación, reinicia a página 1 al aplicar y no persiste filtros hasta HU-008/HU-009.
- Riesgos: SoQL/encoding, rate limits, campos SECOP inconsistentes, ambigüedad de estado, paginación con filtros y bordes de fecha.
- Decisiones pendientes: ratificar endpoint extendido, nombres de query params, enum de estado, uso de `upper(entidad) like`, rechazo de parámetros desconocidos y short-circuit para rangos imposibles antes de autorizar código.
