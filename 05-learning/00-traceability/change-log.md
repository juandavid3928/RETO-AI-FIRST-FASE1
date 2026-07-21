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
