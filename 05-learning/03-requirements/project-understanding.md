# Entendimiento del producto

## Estado y jerarquía de fuentes

Este documento propone el alcance funcional completo para revisión. No autoriza implementación.

Orden usado para resolver contradicciones:

1. Enunciado oficial Track DEV: `3-challenge/2a-reto-ai-first-fase1.pdf`.
2. Guía oficial del programa: `1-docs/1a-guia-ai-first.pdf`.
3. `README.md` y `CLAUDE.md` protegidos como resumen operativo del reto.
4. Decisiones nuevas verificables en `05-learning/` y `SOUL.md`.
5. Inferencias explícitas necesarias para convertir requisitos en comportamiento observable.
6. Referencias visuales heredadas, únicamente como apoyo de diseño y nunca como fuente funcional.

El documento del Track QA y `3-challenge/gestor-inventario/` no definen el producto DEV.

## Problema del producto

Contratistas y proveedores necesitan identificar oportunidades de contratación pública colombiana sin depender de una experiencia fragmentada o difícil de interpretar. El Portal de Convocatorias debe ofrecer una experiencia autenticada para explorar información vigente de SECOP, aplicar filtros relevantes y conservar oportunidades o búsquedas para retomarlas después.

## Actores

| Actor | Necesidad | Alcance |
|---|---|---|
| Visitante | Crear una cuenta e iniciar una sesión segura. | Registro y autenticación. |
| Usuario registrado | Explorar, filtrar y organizar oportunidades relacionadas con su actividad. | Perfil propio, convocatorias, favoritos y búsquedas guardadas. |
| datos.gov.co / SECOP | Proveer datos públicos vigentes. | Sistema externo; no es un usuario ni recibe valor directo del portal. |
| Evaluador del reto | Comprobar una aplicación coherente y reproducible. | Actor de entrega, no actor funcional; sus necesidades se cubren con tareas técnicas y evidencia. |

## Flujo principal

1. Un visitante crea una cuenta.
2. El usuario inicia sesión y obtiene acceso a las capacidades privadas.
3. Puede consultar su perfil propio.
4. Explora convocatorias obtenidas en vivo desde SECOP por medio del backend.
5. Aplica filtros por entidad, rango de fechas y estado, de forma individual o combinada.
6. Consulta el detalle mínimo de una convocatoria seleccionada.
7. Guarda una convocatoria como favorita y luego puede consultarla o retirarla.
8. Guarda un conjunto útil de filtros y posteriormente puede consultarlo, ejecutarlo de nuevo o eliminarlo.
9. Visualiza un dashboard que resume convocatorias visibles, favoritos y búsquedas guardadas ya respaldadas.
10. El portal informa estados de carga, resultados, ausencia de resultados y error sin exponer detalles internos.

## Catálogo de requisitos oficiales

| ID | Requisito | Fuente | Tipo |
|---|---|---|---|
| OF-01 | Usuarios registrados pueden explorar, filtrar y guardar convocatorias públicas colombianas. | Enunciado DEV, §3. | Funcional oficial. |
| OF-02 | Registro e inicio de sesión con JWT; cada usuario tiene perfil propio. | Enunciado DEV, tabla de requisitos mínimos. | Funcional oficial. |
| OF-03 | API REST con búsqueda, filtros y gestión de bookmarks. | Enunciado DEV, tabla de requisitos mínimos. | Funcional oficial. |
| OF-04 | Interfaz web funcional para browse de convocatorias, favoritos y perfil. | Enunciado DEV, tabla de requisitos mínimos. | Funcional oficial. |
| OF-05 | Persistencia para usuarios, bookmarks y búsquedas guardadas. | Enunciado DEV y guía del programa, componentes obligatorios. | Funcional oficial. |
| OF-06 | Consulta en vivo a datos.gov.co/SECOP por entidad, fecha y estado. | Enunciado DEV, tabla de requisitos mínimos. | Integración oficial. |
| OF-07 | El flujo evaluable mínimo funciona end-to-end: autenticación, browse desde datos.gov.co y bookmarks persistidos. | Enunciado DEV, §9. | Criterio oficial de evaluación. |
| OF-08 | Aplicación funcional con backend, frontend, base de datos e integración externa, ejecutable localmente. | Enunciado DEV, §2 y §5; `README.md`. | Entrega técnica, no HU. |
| OF-09 | Repositorio público, `SOUL.md`, README reproducible y demo de 5–7 minutos. | Enunciado DEV, §4–§5; guía del programa. | Entrega y trazabilidad, no HU. |

## Decisiones aprobadas vigentes

| ID | Decisión |
|---|---|
| AP-01 | Stack base: Python 3.12, FastAPI, PostgreSQL 16, React 18 y Docker Compose, entre las dependencias ya aprobadas. |
| AP-02 | Backend organizado mediante arquitectura hexagonal. |
| AP-03 | El frontend consume la API propia; no consulta SECOP directamente. |
| AP-04 | La integración externa se normaliza detrás de un adaptador y debe distinguir timeout, error HTTP, payload inválido y respuesta vacía. |
| AP-05 | Cada HU requiere contrato y microplan aprobados antes de implementar, seguido de RED → GREEN → REFACTOR. |
| AP-06 | No existe todavía producto funcional; este backlog es documental y permanece pendiente de revisión. |
| AP-07 | La instrucción de reanudación del 2026-07-21 aprueba incorporar HU-010 para detalle mínimo y HU-011 para dashboard resumen, sin capacidades ampliadas, analítica, recomendaciones ni métricas externas. |

## Inferencias explícitas usadas por el backlog

| ID | Inferencia | Justificación verificable |
|---|---|---|
| IN-01 | Perfil, favoritos y búsquedas guardadas pertenecen al usuario autenticado y están aislados entre usuarios. | “Perfil propio” y persistencia por usuarios pierden sentido sin propiedad; además evita acceso cruzado. |
| IN-02 | Los filtros soportados pueden aplicarse individualmente y combinarse con semántica AND. | El requisito enumera entidad, fecha y estado como filtros de una misma consulta. |
| IN-03 | Una búsqueda guardada tiene nombre por usuario y al menos un filtro. | Hace identificable y reutilizable la capacidad oficial “búsquedas guardadas”. |
| IN-04 | Reejecutar una búsqueda guardada vuelve a consultar datos vigentes. | El requisito exige consulta en vivo; guardar criterios no debe congelar resultados. |
| IN-05 | Guardar dos veces la misma convocatoria no crea duplicados para el mismo usuario. | Un bookmark representa una relación única usuario–convocatoria. |
| IN-06 | La interfaz diferencia loading, results, empty y error. | Son estados observables mínimos de una consulta remota y una decisión vigente de diseño. |
| IN-07 | La identidad de la convocatoria proviene de una clave estable del dataset acordado. | Favoritos persistentes requieren volver a identificar la oportunidad externa. |
| IN-08 | El filtro oficial por fecha se modela como un rango inclusivo con inicio y fin. | Un rango ofrece un criterio útil y verificable para convocatorias; el enunciado no fija todavía su semántica exacta. |
| IN-09 | Explorar y filtrar convocatorias requiere una sesión autenticada. | El enunciado atribuye estas capacidades a “usuarios registrados”, pero no prohíbe expresamente un browse público. |
| IN-10 | El detalle mínimo reutiliza la clave estable y el DTO acordados para browse, y muestra identidad, entidad, objeto o descripción breve, estado, fecha relevante y enlace a la fuente. | Hace observable la decisión AP-07 sin convertir referencias visuales en autoridad ni agregar enriquecimiento no confirmado. |
| IN-11 | El dashboard resume únicamente la consulta vigente y las colecciones propias de favoritos y búsquedas guardadas. | Hace observable AP-07 con información ya respaldada por HU-003, HU-007 y HU-009; excluye analítica y métricas externas. |

Estas inferencias deben ser ratificadas o sustituidas durante la revisión del backlog; no se presentan como texto oficial.

## Restricciones transversales del reto — no son HU

- La persona especifica, dirige, revisa e itera; el código se genera mediante IA y no manualmente.
- Hermes es el agente principal y canaliza el uso de los LLM de implementación.
- El dominio permanece fijo como Portal de Convocatorias Públicas.
- La entrega usa un repositorio público y debe ser ejecutable localmente.
- `SOUL.md`, README, demo y trazabilidad son entregables o evidencia, no valor funcional autónomo.
- Credenciales y secretos no se almacenan en código ni documentación versionada.
- Seguridad, resiliencia, accesibilidad, observabilidad y rendimiento se tratan como atributos transversales; sus umbrales medibles deben aprobarse con los contratos y microplanes.

## Reglas de negocio propuestas

1. El correo de cuenta es válido, se normaliza y es único.
2. Las contraseñas no se devuelven ni se persisten en texto plano.
3. Los errores de autenticación no confirman si una cuenta existe.
4. Las capacidades de perfil, exploración, favoritos y búsquedas guardadas requieren identidad autenticada.
5. Un usuario solo consulta y modifica sus propios recursos persistidos.
6. Las convocatorias se consultan desde SECOP por medio del backend y se normalizan a un contrato estable.
7. Entidad, rango inclusivo de fechas y estado pueden combinarse; un rango con inicio posterior al fin se rechaza.
8. Una consulta sin resultados es una respuesta válida, no un fallo.
9. Un usuario no tiene dos favoritos para la misma convocatoria.
10. Una búsqueda guardada posee un nombre único por usuario y al menos un criterio soportado.
11. Reejecutar una búsqueda guardada usa sus criterios y consulta información vigente.
12. El detalle mínimo reutiliza la clave estable y no enriquece la convocatoria con capacidades o datos no confirmados.
13. El dashboard solo resume convocatorias visibles, favoritos y búsquedas guardadas; no calcula analítica, recomendaciones ni métricas externas.

## Límites del alcance

### Dentro del producto mínimo

- Registro, login JWT y consulta de perfil propio.
- Browse en vivo de convocatorias SECOP.
- Filtros por entidad, fecha y estado.
- Detalle mínimo de una convocatoria seleccionada.
- Dashboard resumen de convocatorias visibles, favoritos y búsquedas guardadas.
- Guardar, listar y retirar favoritos persistentes.
- Guardar, listar, reejecutar y eliminar búsquedas guardadas.
- Estados web observables de carga, resultados, vacío y error.
- Aislamiento de datos por usuario.

### Fuera del backlog hasta nueva aprobación

- Roles administrativos y gestión de usuarios.
- Crear, editar o eliminar convocatorias en SECOP.
- Notificaciones, alertas o ejecución programada de búsquedas.
- Recuperación de contraseña, verificación de correo, MFA y proveedores sociales.
- Edición avanzada del perfil.
- Recomendaciones, analítica, métricas externas, pagos, mensajería o colaboración.
- Detalle ampliado con documentos, cronologías, enriquecimiento, acciones de edición o capacidades distintas del contenido mínimo aprobado en HU-010.
- Caché funcional, operación offline o réplica completa de SECOP.
- Soporte simultáneo para múltiples datasets SECOP.

## Decisiones pendientes antes de implementar

1. Campos mínimos del registro y perfil además del correo.
2. Política de contraseña, expiración del JWT, renovación y cierre de sesión.
3. Dataset SECOP definitivo y clave estable de convocatoria.
4. Mapeo exacto del DTO, catálogo de estados, semántica de fechas y zona horaria.
5. Paginación, orden por defecto y límites de consulta.
6. Datos mínimos conservados junto al bookmark y estrategia ante oportunidades retiradas de la fuente.
7. Longitud del nombre de búsqueda guardada y política para renombrar o actualizar criterios.
8. Política de caché, rate limits, reintentos y timeouts.
9. Ratificar los nombres y mapeos exactos de los campos mínimos de HU-010 dentro del DTO aprobado.
10. Definir si el resumen de convocatorias de HU-011 usa la página vigente o una consulta predeterminada y cómo comunica sus límites.
11. Ratificar si browse y filtros serán privados como propone IN-09 o también estarán disponibles sin sesión.
12. Definir objetivos medibles de accesibilidad, rendimiento y logging sin datos sensibles.
