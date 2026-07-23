# Criterios de aceptación observables

## Estado y convención

Los criterios de HU-001, HU-002 y HU-005 están aprobados e implementados en `main`. HU-003 está implementada y validada en la rama vigente para revisión mediante PR. HU-004 y HU-006 a HU-011 continúan propuestos y no autorizan implementación.

## HU-001 — Crear una cuenta

### AC-HU-001-01 — Registro exitoso

**Dado** un visitante con `email` y `password` válidos y un correo no registrado, **cuando** envía `POST /api/v1/auth/register`, **entonces** recibe `201` con UUID4, correo canónico y fecha UTC de creación, sin JWT, contraseña ni hash.

### AC-HU-001-02 — Correo único

**Dado** un correo ya asociado a una cuenta, incluso con diferencias de mayúsculas o espacios exteriores, **cuando** se intenta registrar de nuevo, incluso concurrentemente, **entonces** PostgreSQL conserva una sola cuenta y la API responde `409` al duplicado mediante el sobre de error estable.

### AC-HU-001-03 — Datos inválidos

**Dado** JSON inválido, campos desconocidos o ausentes, email con sintaxis inválida, password fuera de 12..128 caracteres o cuerpo mayor de 4 KiB, **cuando** se envía, **entonces** se rechaza con `422`, sobre estable y errores identificables por campo cuando aplica, sin persistir una cuenta.

### AC-HU-001-04 — Protección de contraseña

**Dado** un registro exitoso, **cuando** se inspeccionan respuesta, logs y persistencia mediante una prueba autorizada, **entonces** la contraseña nunca aparece y la persistencia contiene únicamente un hash Argon2id generado mediante `pwdlib[argon2]`.

### AC-HU-001-05 — Fallos controlados

**Dado** que PostgreSQL no está disponible o ocurre un fallo inesperado, **cuando** se solicita el registro, **entonces** la API responde respectivamente `503` o `500` con el sobre estable, revierte la transacción y no expone detalles internos ni credenciales.

### AC-HU-001-06 — Flujo web accesible

**Dado** un visitante en `/register`, **cuando** completa email, password y confirmación, **entonces** la interfaz accesible distingue estados idle, invalid, submitting, success, conflict, network y server; impide doble envío, envía solo email/password, limpia campos sensibles al completar y permanece en la ruta sin usar storage, analytics ni logs de credenciales.

## HU-002 — Iniciar sesión

### AC-HU-002-01 — Credenciales válidas

**Dado** un usuario registrado con credenciales válidas, **cuando** inicia sesión, **entonces** recibe un JWT verificable que permite acceder a una capacidad privada durante su vigencia.

### AC-HU-002-02 — Credenciales inválidas

**Dado** un correo inexistente o una contraseña incorrecta, **cuando** intenta iniciar sesión, **entonces** se rechaza con un mensaje equivalente que no revela si la cuenta existe.

### AC-HU-002-03 — Acceso sin sesión válida

**Dado** un token ausente, inválido o expirado, **cuando** se solicita una capacidad privada, **entonces** el sistema rechaza el acceso sin entregar datos del usuario.

## HU-003 — Explorar convocatorias vigentes

### AC-HU-003-01 — Consulta por medio del backend

**Dado** un usuario autenticado, **cuando** abre la exploración de convocatorias, **entonces** el frontend consulta `GET /api/v1/opportunities` en la API propia y el backend consulta el dataset oficial SECOP II acordado; el navegador no llama directamente a datos.gov.co ni a `community.secop.gov.co` para obtener el listado.

### AC-HU-003-02 — Resultado normalizado

**Dada** una respuesta válida de SECOP II con convocatorias abiertas y fecha de recepción vigente, **cuando** el backend la procesa, **entonces** entrega una lista paginada con el DTO estable acordado, incluyendo como mínimo `id`, `reference`, `entity_name`, `title`, `status`, `summary_status`, `opening_status`, `published_at`, `closing_at`, `estimated_amount_cop` y `source_url`, y usa `id_del_proceso` como clave externa propuesta.

### AC-HU-003-03 — Estados de interfaz

**Dada** una consulta de convocatorias, **cuando** está en curso, termina sin elementos, falla por integración externa o devuelve elementos válidos, **entonces** la interfaz diferencia explícitamente `loading`, `empty`, `external_error` y `success` sin presentar datos obsoletos como vigentes.

### AC-HU-003-04 — Fallo externo controlado

**Dado** un timeout, rate limit, error HTTP, JSON inválido o payload sin campos mínimos de SECOP II, **cuando** se exploran convocatorias, **entonces** la API responde con un error estable y la interfaz presenta un error recuperable sin exponer detalles internos ni datos parciales presentados como exitosos.

### AC-HU-003-05 — Acceso privado

**Dado** un visitante sin sesión válida, **cuando** intenta explorar convocatorias, **entonces** no obtiene el listado ni datos derivados de SECOP a través del portal.

## HU-004 — Filtrar convocatorias

### AC-HU-004-01 — Filtros individuales

**Dado** un usuario autenticado, **cuando** filtra por entidad, rango de fechas o estado de manera individual, **entonces** la consulta enviada a la integración incluye el criterio y los resultados normalizados lo respetan.

### AC-HU-004-02 — Filtros combinados

**Dados** dos o más filtros válidos, **cuando** se aplican juntos, **entonces** solo se muestran convocatorias que cumplen todos los criterios activos.

### AC-HU-004-03 — Rango inválido

**Dado** un rango cuya fecha inicial es posterior a la final, **cuando** se intenta buscar, **entonces** el sistema señala el error y no envía esa consulta inválida a SECOP.

### AC-HU-004-04 — Sin coincidencias

**Dados** filtros válidos sin coincidencias, **cuando** finaliza la consulta, **entonces** se muestra el estado empty y no se trata como fallo de integración.

## HU-005 — Consultar el perfil propio

### AC-HU-005-01 — Perfil autenticado

**Dado** un usuario autenticado, **cuando** consulta `GET /api/v1/users/me`, **entonces** recibe exactamente `id`, `email` y `created_at` de su propia cuenta.

### AC-HU-005-02 — Datos sensibles excluidos

**Dado** cualquier respuesta de perfil, **cuando** se inspeccionan payload, caché y almacenamiento cliente, **entonces** no contiene contraseña, hash, JWT ni claims, usa headers privados y el perfil no se persiste en `localStorage`.

### AC-HU-005-03 — Sin acceso cruzado

**Dado** un usuario autenticado, **cuando** intenta suministrar otro `user_id` por query, body o headers, **entonces** el sistema deriva la identidad de `AuthenticatedPrincipal.user_id` y no entrega el perfil ajeno; si el usuario del token ya no existe responde `401 invalid_token`.

## HU-006 — Guardar una convocatoria favorita

### AC-HU-006-01 — Creación del favorito

**Dada** una convocatoria de un resultado vigente, **cuando** el usuario autenticado la guarda, **entonces** el sistema confirma el favorito y lo asocia al usuario y a la clave estable de la convocatoria.

### AC-HU-006-02 — Persistencia

**Dado** un favorito creado, **cuando** el usuario inicia una sesión posterior o se reinicia la aplicación conservando la base de datos, **entonces** el favorito continúa disponible.

### AC-HU-006-03 — Sin duplicados

**Dado** un favorito ya existente para ese usuario y convocatoria, **cuando** intenta guardarlo otra vez, **entonces** no se crea un segundo registro y el resultado es determinista.

### AC-HU-006-04 — Propiedad autenticada

**Dado** un intento de crear un favorito, **cuando** no existe una sesión válida o se envía un propietario distinto, **entonces** el sistema rechaza el acceso o ignora la identidad suministrada y usa la identidad autenticada.

## HU-007 — Gestionar favoritos

### AC-HU-007-01 — Listado propio

**Dados** favoritos de varios usuarios, **cuando** un usuario consulta su lista, **entonces** solo recibe los favoritos que le pertenecen.

### AC-HU-007-02 — Retiro

**Dado** un favorito propio existente, **cuando** el usuario lo retira, **entonces** deja de aparecer en consultas posteriores sin afectar la fuente SECOP.

### AC-HU-007-03 — Aislamiento al retirar

**Dado** un favorito perteneciente a otro usuario, **cuando** se intenta retirarlo, **entonces** el sistema no lo modifica ni confirma información que permita acceder al recurso ajeno.

## HU-008 — Guardar criterios de búsqueda

### AC-HU-008-01 — Guardado válido

**Dados** un nombre válido y al menos un filtro soportado, **cuando** el usuario guarda la búsqueda, **entonces** se persisten el nombre y los criterios asociados a su identidad.

### AC-HU-008-02 — Persistencia

**Dada** una búsqueda guardada, **cuando** el usuario vuelve en una sesión posterior, **entonces** la entrada sigue disponible con los mismos criterios.

### AC-HU-008-03 — Nombre único por usuario

**Dado** un nombre ya usado por el mismo usuario, **cuando** intenta crear otra búsqueda con ese nombre, **entonces** el sistema rechaza el conflicto sin sobrescribir la existente; otro usuario puede usar ese nombre.

### AC-HU-008-04 — Búsqueda vacía o inválida

**Dado** un nombre ausente o un conjunto sin filtros soportados, **cuando** se intenta guardar, **entonces** no se crea la entrada y se identifican los datos inválidos.

## HU-009 — Gestionar búsquedas guardadas

### AC-HU-009-01 — Listado propio

**Dadas** búsquedas guardadas de varios usuarios, **cuando** un usuario consulta su lista, **entonces** solo recibe sus propias entradas y criterios.

### AC-HU-009-02 — Reejecución con datos vigentes

**Dada** una búsqueda guardada, **cuando** el usuario la ejecuta, **entonces** se aplican sus criterios mediante el flujo de HU-004 y se realiza una nueva consulta a la fuente acordada.

### AC-HU-009-03 — Eliminación

**Dada** una búsqueda guardada propia, **cuando** el usuario la elimina, **entonces** deja de aparecer y no puede reejecutarse desde su lista.

### AC-HU-009-04 — Aislamiento

**Dada** una búsqueda guardada ajena, **cuando** otro usuario intenta consultarla, ejecutarla o eliminarla, **entonces** el sistema no entrega sus criterios ni la modifica.

## HU-010 — Consultar detalle de convocatoria

### AC-HU-010-01 — Apertura desde una convocatoria

**Dado** un usuario autenticado y una convocatoria obtenida por HU-003, **cuando** solicita consultar su detalle, **entonces** el frontend usa su clave estable para consultar la API propia y el navegador no accede directamente a SECOP.

### AC-HU-010-02 — Contenido mínimo trazable

**Dada** una respuesta válida para la convocatoria seleccionada, **cuando** se muestra el detalle, **entonces** presenta únicamente los campos esenciales acordados del DTO —identidad, entidad, objeto o descripción breve, estado, fecha relevante y enlace a la fuente— sin inventar datos ausentes.

### AC-HU-010-03 — Consistencia con la fuente

**Dada** una convocatoria identificada por su clave estable, **cuando** el backend obtiene y normaliza su detalle, **entonces** la información corresponde a esa misma convocatoria y mantiene la semántica acordada para el browse.

### AC-HU-010-04 — Estados controlados

**Dada** una consulta de detalle, **cuando** está en curso, la convocatoria no existe o la integración falla, **entonces** la interfaz diferencia loading, not found y error sin presentar información de otra convocatoria ni capacidades ampliadas como edición, recomendaciones o analítica.

## HU-011 — Visualizar dashboard resumen

### AC-HU-011-01 — Resumen autenticado

**Dado** un usuario autenticado, **cuando** abre el dashboard, **entonces** ve un resumen de convocatorias visibles en la consulta vigente, sus favoritos y sus búsquedas guardadas, obtenido mediante la API propia.

### AC-HU-011-02 — Datos respaldados y consistentes

**Dados** resultados de HU-003, favoritos de HU-007 y búsquedas de HU-009, **cuando** el dashboard presenta cantidades o accesos resumidos, **entonces** estos coinciden con las colecciones devueltas y no incorporan tendencias, puntajes, recomendaciones ni métricas externas.

### AC-HU-011-03 — Acceso a capacidades existentes

**Dado** un bloque del resumen con información disponible, **cuando** el usuario activa su acceso, **entonces** navega a la capacidad ya definida de exploración, favoritos o búsquedas guardadas sin crear un flujo funcional adicional.

### AC-HU-011-04 — Vacío y fallo diferenciados

**Dada** una colección vacía o una consulta fallida, **cuando** se construye el resumen, **entonces** el dashboard distingue ausencia real de datos y error, y no convierte un fallo en un valor cero aparentemente exitoso.

### AC-HU-011-05 — Acceso privado

**Dado** un visitante sin sesión válida, **cuando** intenta abrir el dashboard, **entonces** no recibe convocatorias ni resúmenes de favoritos o búsquedas guardadas de ningún usuario.

## Definition of Done documental para cada HU

Antes de implementar una HU deben quedar aprobados sus criterios, contrato y microplan. Para cerrarla se exige evidencia real de RED → GREEN → REFACTOR, pruebas relevantes, revisión de seguridad y alcance, actualización trazable de documentación y ausencia de secretos. Las tareas técnicas no sustituyen estos resultados de negocio.
