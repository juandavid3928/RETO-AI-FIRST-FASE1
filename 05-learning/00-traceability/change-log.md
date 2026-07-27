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

## 2026-07-21 — Complete backlog functional coverage

**Tipo:** requisitos | trazabilidad | documentación

**Motivo:** Resolver el único bloqueo funcional del PR #2 mediante cobertura explícita de detalle de convocatoria y dashboard resumen.

**Acciones:**
- Se conservaron HU-001 a HU-009.
- Se agregaron HU-010 para el detalle mínimo y HU-011 para un dashboard limitado a información ya respaldada.
- AP-07 registra la instrucción aprobada; IN-10 e IN-11 documentan las decisiones observables sin elevar referencias visuales a requisito oficial.
- Se añadieron 9 criterios Dado/Cuando/Entonces y se actualizaron orden, grafo, matrices, conteos, riesgos y decisiones pendientes.
- Se retiró del checkpoint el bloqueo por ausencia de HU-010/HU-011.

**Validaciones observadas:**
- Verificación documental ad hoc: 11 HU, 43 criterios únicos, fuentes y campos completos, matrices consistentes y 0 ciclos.
- Alcance Git: solo 7 documentos dentro de las rutas autorizadas; `06-code/` y archivos protegidos sin cambios.
- Búsqueda enfocada de secretos y datos heredados en el diff: 0 coincidencias.
- `git diff --check`: PASS.

**Límites:** No se implementó código, no se aprobó el inicio de ninguna HU y no se hizo merge.

**Pendiente:** Revisión de Codex y aprobación humana del PR #2.

## 2026-07-21 — Implement HU-001 user registration

**Tipo:** requisitos | backend | persistencia | frontend | pruebas | contenedores

**Alcance:** se aprobó e implementó únicamente HU-001. HU-002 no fue iniciada.

**Resultados:**
- Contrato y seis criterios de HU-001 fijan payload, normalización, límites, respuestas y errores estables.
- Caso de uso hexagonal con `Email`, `UserId`, `User` y puertos de repositorio, hash, reloj e ID; límites de imports verificados.
- PostgreSQL 16 con migración Alembic SQL reversible, UUID4, hash Argon2id, `created_at`/`updated_at` con zona y unicidad canónica autoritativa.
- FastAPI expone solo registro y health técnico; React expone `/register` con estados accesibles y protección de doble envío.
- Compose incorpora DB, backend y frontend con healthchecks, orden por salud, locks y credenciales suministradas por variables separadas para admitir caracteres reservados.

**Evidencia fresca:**
- Backend: `TEST_DATABASE_URL='postgresql://...' uv run pytest -q` → 32 passed contra PostgreSQL real.
- Frontend: `npm test` → 8 passed; `npm run build` → build exitoso.
- PostgreSQL real: 5 pruebas de integración incluidas en backend, con migración up/down, credenciales reservadas y carrera 201/409.
- Browser E2E: con stack saludable, `E2E_BASE_URL='http://...' TEST_DATABASE_URL='postgresql://...' npm run test:e2e` → 1 passed, verificando browser→API→PostgreSQL y hash Argon2id.
- Compose: build de ambos entrypoints y arranque saludable de los tres servicios; prueba de configuración exitosa.

Los fallos RED observados antes de cada segmento quedaron fuera del repositorio en `/tmp/hu001-red-evidence.txt`.

## 2026-07-21 — Implement HU-002 user login with JWT

**Tipo:** requisitos | backend | seguridad | frontend | pruebas | documentación

**Alcance:** HU-002 implementada localmente sobre HU-001 en `feat/hu-002-user-login`, sin iniciar HU-005 ni crear una ruta privada productiva.

**Resultados:**
- `POST /api/v1/auth/login` recibe JSON estricto con email canónico y password opaca, responde JWT Bearer temporal y mantiene idéntico `401 invalid_credentials` para cuenta inexistente o password incorrecta.
- Argon2id verifica hashes reales y ejecuta un hash dummy equivalente cuando no existe la cuenta; PostgreSQL se consulta con SQL parametrizado.
- JWT PyJWT HS256 fija algoritmo, `sub` UUID4, issuer, audience, `iat`, `exp`, TTL de 1800 segundos y leeway de validación de 30 segundos; el secreto base64url de mínimo 32 bytes es obligatorio al arrancar.
- La dependencia Bearer productiva diferencia token ausente e inválido, pero solo se conecta a una ruta protegida dentro de tests.
- `/login` cubre validación, doble envío, errores, persistencia mínima `portal.auth.session`, restauración, expiración y logout cliente; Nginx añade CSP y cabeceras de hardening.

**Evidencia vigente:**
- RED reproducido para `aud` no string, TTL distinto y `exp < iat`; GREEN posterior: `tests/unit/test_jwt_access_token.py` → 25 passed.
- Backend unitario/API posterior al correctivo JWT: 70 passed; advertencia no bloqueante de Starlette/TestClient.
- Frontend posterior a los ajustes de storage/contrato: 27 passed y build Vite exitoso.
- Verificación ad hoc: locks, frontera hexagonal, seguridad estática y `git diff --check` en verde.
- PostgreSQL 16 sobre volumen vacío aplicó Alembic `20260721_0001`; backend completo contra esa instancia → 76 passed.
- La primera corrida E2E conjunta produjo RED porque la prueba de downgrade de la suite backend dejó el esquema desmontado para el proceso externo. Se reaplicó `alembic upgrade head` y la repetición conjunta registro/login → 2 passed.
- El E2E de login verificó usuario realmente persistido, firma HS256, claims/TTL, storage exacto, restauración, expiración controlada, reautenticación y logout con limpieza.
- Frontend → 27 passed; build Vite exitoso; audit 0 vulnerabilidades; Compose config y CSP en verde.

**Revisión independiente:** el primer veredicto fue FAIL por ventana temporal JWT, `aud` no tipado y documentación obsoleta. Tras los correctivos TDD y documentales, una segunda revisión estable del snapshot emitió PASS sin bloqueantes; verificó adversarialmente audience, TTL y orden temporal, además del manejo frontend de storage y respuestas `200` malformadas.

**Límites y riesgos:** `localStorage` conserva riesgo residual XSS pese a CSP; logout no revoca un token robado antes de `exp`; rate limiting permanece como hardening pendiente aprobado fuera del incremento. No se hizo commit, push ni merge.

## 2026-07-21 — Harden HU-002 frontend authentication session

**Alcance:** correctivo frontend de HU-002 sobre el PR #4; no se añadió cliente autenticado, llamada privada ni capacidad de HU-005.

**Cambios:**
- `auth/authSession.ts` centraliza clave, contrato exacto, persistencia, restauración, expiración y limpieza segura.
- La respuesta `200` exige exactamente JWT estructural, `token_type: "bearer"` y `expires_in: 1800`; una respuesta malformada limpia sesión y contraseña.
- `LoginPage` sincroniza login, logout y expiración mediante `storage`, reevalúa al recuperar visibilidad y desmonta listeners/temporizador.
- `authenticatedFetch` queda documentado como pendiente hasta la primera capacidad privada autorizada.

**Evidencia RED:** la suite focalizada produjo 8 fallos reproducibles para contrato, multitab, visibilidad y cleanup; el test del módulo falló inicialmente porque el módulo todavía no existía. Una revisión posterior añadió 2 RED para JSON `200` inválido y campos extra en la sesión persistida.

**Evidencia GREEN fresca:** frontend 41 passed y build Vite exitoso; backend completo contra PostgreSQL 16 real 76 passed; esquema restaurado con `alembic upgrade head` después de la prueba de downgrade; E2E conjunto registro/login 2 passed; audit 0, lock, Compose config, CSP/cabeceras, escaneo de secretos y `git diff --check` en verde. La infraestructura usó puertos efímeros libres y fue eliminada junto con volumen, red, temporales y artefactos Playwright.

## 2026-07-21 — Implement HU-005 own profile

**Tipo:** requisitos | backend | autorización | frontend | pruebas | documentación

**Alcance:** primera capacidad privada completa sobre HU-001/HU-002. No se modificaron JWT, claims, tabla `users` ni migraciones; HU-003 y las demás historias no fueron iniciadas.

**Resultados:**
- `GET /api/v1/users/me` deriva la identidad únicamente de `AuthenticatedPrincipal.user_id`, proyecta exactamente `id`, `email`, `created_at` y aplica `no-store`, `no-cache` y `Vary: Authorization` en éxito y error.
- `UserRepository.get_by_id` consulta el UUID parametrizado por primary key; `GetOwnProfile` no devuelve la entidad completa y un usuario eliminado se presenta como `401 invalid_token` sin enumeración.
- La inyección de otro `user_id` por query, body o headers no cambia el principal ni permite exponer otra cuenta.
- `AuthSessionProvider` centraliza restauración, expiración, `storage`, visibilidad y logout; `RequireAuth` solo controla UX.
- `authenticatedFetch` restringe el destino a rutas relativas `/api/`, impide override de `Authorization`, clasifica errores y limpia sesión ante `401` sin navegar.
- Login navega con `replace` a `/profile`; el perfil exacto se valida y mantiene solo en memoria, con estados loading, success, unauthorized, network, server y storage error.

**Evidencia RED observada:**
- Caso de uso: colección falló antes de existir `get_own_profile`; después quedó en 3 passed.
- Repositorio: 3 fallos por ausencia de `get_by_id`; después quedó en 3 passed.
- API: 5 fallos porque `create_app` no aceptaba el nuevo caso de uso; después quedaron verdes los contratos de perfil/login.
- Frontend: la suite nueva produjo import ausente de `authenticatedFetch` y 8 fallos por ruta `/profile` inexistente; una regresión completa detectó 2 expectativas incompatibles con la navegación aprobada y la prioridad del mensaje de storage.
- La primera validación E2E ejecutó 2 escenarios nuevos correctamente y detectó 1 fallo de harness por omitir `TEST_DATABASE_URL` al E2E heredado; el harness se corrigió y se repitió todo desde infraestructura nueva.

**Evidencia GREEN reproducible:**
- PostgreSQL 16 sobre volumen vacío, Compose completo y Alembic: servicios saludables; esquema final `20260721_0001 (head)`.
- Backend completo contra PostgreSQL real: 89 passed; única advertencia no bloqueante de deprecación Starlette/TestClient.
- Frontend unitario/componente: 58 passed; build TypeScript/Vite exitoso.
- Playwright conjunto registro/login/perfil: 3 passed, incluido reload, logout, almacenamiento mínimo y token alterado.
- `npm audit`: 0 vulnerabilidades; `uv lock --check`, Compose config, CSP, headers privados, frontera hexagonal, escaneo de secretos y `git diff --check`: PASS.
- Puertos, credenciales y secreto JWT fueron efímeros; contenedores, red, volumen, env y artefactos Playwright se eliminaron mediante trap.

**Revisión independiente resuelta:** la validación canónica de dot-segments de `authenticatedFetch` y sus pruebas ya estaban incorporadas antes de recibir el hallazgo; se normalizó `created_at` explícitamente a UTC con una prueba RED/GREEN para zona `-05:00`, se añadió `TEST_DATABASE_URL` al comando E2E documentado y se corrigió la descripción de estados de `ProfilePage`. Validación afectada posterior: backend unitario/API 82 passed, frontend 58 passed y build PASS.

**Estado:** implementación en `feat/hu-005-own-profile`, pendiente de revisión mediante PR y sin merge.

## 2026-07-21 — Project pause checkpoint after HU-005

**Estado fusionado:** PR #1 estructura, PR #2 backlog, HU-001/PR #3 (`f1a82ef`), HU-002/PR #4 (`34f25f2`) y HU-005/PR #5 (`940da47`) están fusionados. Antes de crear la rama documental, `main` estaba limpia y sincronizada con `origin/main` en `940da47a0b9d887e0593b153685c540515ff7790`.

**Producto disponible:** registro, login JWT y perfil propio; PostgreSQL 16, backend, frontend y Docker Compose operativos. La validación integral final observó backend 90 passed, frontend 58 passed, Playwright 3 passed y PASS en build, audit, lock, Compose, CSP, arquitectura, secretos y diff. Alembic terminó en `20260721_0001 (head)` y la infraestructura/temporales de validación fueron eliminados.

**Pausa:** no se inició otra HU. HU-003 continúa pendiente de análisis; al retomar se debe confirmar dataset y contrato SECOP II antes de cualquier implementación y esperar una nueva instrucción de Codex. Se conserva `backup/repository-structure-a0dfd0a` como respaldo de la estructura limpia inicial.

**Riesgos vigentes:** XSS residual por JWT en `localStorage`, logout sin revocación, rate limiting pendiente y advertencia Starlette/TestClient no bloqueante.

## 2026-07-22 — Analyze HU-003 SECOP II contract

**Tipo:** requisitos | arquitectura | integración externa | documentación

**Alcance:** análisis documental para HU-003. No se implementó backend, frontend, migraciones, pruebas productivas ni E2E; HU-004, HU-010 y demás HU no fueron iniciadas.

**Fuentes inspeccionadas:**
- `SOUL.md`.
- `05-learning/03-requirements/`.
- `05-learning/02-architecture/`.
- Documentación vigente de `06-code/`.
- Metadata y consulta pública acotada del dataset oficial datos.gov.co `SECOP II - Procesos de Contratación` (`p6dx-8zbt`).

**Resultados:**
- Se recomendó `https://www.datos.gov.co/resource/p6dx-8zbt.json` como fuente SECOP II oficial para HU-003.
- Se definió “convocatoria vigente” como proceso con `estado_de_apertura_del_proceso = 'Abierto'` y `fecha_de_recepcion_de` no vencida.
- Se propuso el endpoint privado `GET /api/v1/opportunities` con paginación, timeout y DTO normalizado.
- Se ajustaron criterios AC-HU-003-01 a AC-HU-003-05 para reflejar backend-only, DTO, estados UI y fallos externos.
- Se documentó microplan TDD para una iteración posterior sin crear código.

**Áreas afectadas:**
- `SOUL.md`
- `05-learning/00-traceability/change-log.md`
- `05-learning/03-requirements/`

**Pendiente:** Codex y el humano deben ratificar dataset, clave estable, definición de vigencia, contrato, privacidad y límites antes de autorizar implementación.

## 2026-07-23 — Implement HU-003 opportunity browse

**Tipo:** backend | frontend | integración externa | pruebas | documentación

**Alcance:** HU-003 — exploración privada de convocatorias vigentes. No se implementaron filtros HU-004, detalle HU-010, favoritos, búsquedas guardadas ni dashboard.

**Resultados:**
- Backend hexagonal: puerto/caso de uso `ListCurrentOpportunities`, DTO interno, fecha actual de Colombia inyectable y adaptador SECOP en `app/infrastructure/external/`.
- Integración SECOP: dataset `p6dx-8zbt`, endpoint `https://www.datos.gov.co/resource/p6dx-8zbt.json`, SoQL acotado, timeout 5s, normalización estricta y fallos externos controlados.
- API: `GET /api/v1/opportunities?page=1&page_size=20`, privada con Bearer JWT, paginación 1..50, headers privados, `401`/`422`/`503`/`200` estables.
- Frontend: `/opportunities` privada, navegación desde `/profile`, `authenticatedFetch`, parser estricto, estados loading/empty/external_error/success y sin persistencia de oportunidades.
- Dependencias: `httpx` pasó a dependencia runtime porque el adaptador SECOP productivo lo usa; `uv.lock` actualizado.
- Compose: `SECOP_BASE_URL` opcional y `host.docker.internal` para E2E determinístico con stub local.

**Evidencia RED observada:**
- Backend HU-003 focalizado falló por imports ausentes de `InvalidPagination`, `ExternalOpportunitySourceUnavailable`, caso de uso y adaptador.
- Frontend HU-003 focalizado falló por servicio/ruta `/opportunities` inexistentes.

**Evidencia GREEN final:**
- Backend focalizado HU-003: 17 passed.
- Backend unitario/API: 99 passed.
- Backend completo con PostgreSQL 16 real: 107 passed.
- Frontend completo: 64 passed.
- Build Vite: PASS.
- Playwright registro/login/perfil/oportunidades con SECOP stub: 4 passed.
- `npm audit --audit-level=high`: 0 vulnerabilidades.
- `uv lock --check`: PASS.
- Docker Compose config: PASS.
- Consulta viva SECOP de solo lectura con `$limit=1`: PASS como evidencia externa no determinística.

**Limpieza:** contenedores, red, volumen, env temporal, script temporal, `dist`, `test-results` y `playwright-report` eliminados.

**Riesgos residuales:** disponibilidad/rate limits/cambios de esquema de datos.gov.co, necesidad de revalidar unicidad de `id_del_proceso` antes de favoritos y riesgo XSS residual por `localStorage` ya conocido.

## 2026-07-23 — Address HU-003 Codex review findings

**Tipo:** backend | configuración | pruebas | documentación

**Alcance:** corrección de HU-003 únicamente. No se implementaron filtros HU-004, detalle HU-010, favoritos, búsquedas guardadas, dashboard, migraciones, nuevas tablas ni persistencia de oportunidades.

**Hallazgos corregidos:**
- `GET /api/v1/opportunities?page=0&page_size=51` ahora responde `422 validation_error` con mensaje `Opportunity query is invalid.`, conserva headers privados y no invoca el caso de uso.
- `SECOP_BASE_URL` y `SECOP_TIMEOUT_SECONDS` pasan por `Settings`/`.env`; `bootstrap.py` no lee `os.getenv()`.
- `SecopOpportunitySource` recibe timeout configurable y lo usa en la solicitud externa. Defaults: dataset oficial `p6dx-8zbt` y timeout `5` segundos.

**Evidencia RED observada:**
- La prueba de query inválida falló porque devolvía `Registration data is invalid.`.
- Las pruebas de settings SECOP fallaron porque `Settings` no exponía `secop_base_url` ni `secop_timeout_seconds`.
- La prueba de timeout configurable falló porque `SecopOpportunitySource` no aceptaba `timeout_seconds`.

## 2026-07-22 — Analyze HU-004 filter contract

**Tipo:** requisitos | integración externa | frontend | documentación

**Alcance:** análisis/microplan documental para HU-004. No se modificó `06-code/`, no se implementaron backend, frontend, pruebas productivas ni E2E, y no se iniciaron HU-010, HU-006, HU-007, HU-008, HU-009, HU-011 ni otras HUs.

**Estado base verificado:** PR #8 cerrado/fusionado, HU-003 integrada en `main` con merge commit `44a915acd905dadd562279202dd4c71ea5c1a4f0`, `main` sincronizada con `origin/main`, rama `feat/hu-003-explore-opportunities` eliminada local/remotamente y respaldo `backup/repository-structure-a0dfd0a` conservado.

**Resultados:**
- Se creó `05-learning/03-requirements/hu-004-filter-contract-analysis.md`.
- Se propone extender `GET /api/v1/opportunities` con query params opcionales `entity`, `closing_from`, `closing_to` y `status`; no endpoint nuevo.
- `entity` se define como coincidencia parcial case-insensitive sobre `entidad`, con trim, colapso de espacios y longitud 3..120.
- `closing_from`/`closing_to` se definen como fechas `YYYY-MM-DD` inclusivas sobre `fecha_de_recepcion_de`, interpretadas como fecha civil de Colombia y combinadas con la vigencia HU-003.
- `status` se recomienda inicialmente como enum `presentation`, mapeado a `estado_resumen='Presentación de oferta'`, manteniendo fijo `estado_de_apertura_del_proceso='Abierto'`.
- Los filtros inválidos deben responder `422 validation_error`, mensaje `Opportunity query is invalid.`, fields por parámetro y no consultar SECOP.
- El frontend futuro debe agregar controles accesibles, aplicar/limpiar filtros, preservar resultados ante validación inválida y no persistir criterios hasta HU-008/HU-009.
- El E2E futuro debe usar stub SECOP determinístico sin Internet para registro, login, perfil y oportunidades filtradas.

**Corrección documental:** `user-stories.md`, `acceptance-criteria.md`, `scope-coverage.md` y `README.md` fueron actualizados para reflejar que HU-003 está fusionada en `main` mediante PR #8.

**Decisiones cerradas:** endpoint extendido `GET /api/v1/opportunities`, query params `entity`/`closing_from`/`closing_to`/`status`, entidad 3..120 con `upper(entidad) like`, estado inicial único `presentation`, rechazo de parámetros desconocidos, short-circuit local para `closing_to` anterior a hoy Colombia y no persistencia de filtros hasta HU-008/HU-009.

## 2026-07-22 — Record pause after HU-004 contract

**Tipo:** documentación | pausa | trazabilidad

**Alcance:** checkpoint de pausa posterior al cierre documental de HU-004. No se modificó `06-code/`, no se implementó HU-004 y no se inició HU-010 ni otra HU.

**Estado real registrado:**
- PR #8/HU-003 está fusionado en `main` mediante merge commit `44a915acd905dadd562279202dd4c71ea5c1a4f0`.
- PR #9/análisis HU-004 está fusionado en `main` mediante merge commit `a77aed42946de596e733413f5d8857757bb2b410`.
- `main` local y `origin/main` se verificaron sincronizadas en `a77aed42946de596e733413f5d8857757bb2b410` antes de crear la rama de pausa.
- Las ramas previas de HU-003 y HU-004 documental están eliminadas local/remotamente; `backup/repository-structure-a0dfd0a` permanece conservada.

**Pendiente:** reanudar con implementación HU-004 solo bajo nueva autorización, en rama nueva, sin iniciar HU-010, favoritos, búsquedas guardadas ni dashboard.
