# Análisis técnico-documental HU-003 — Explorar convocatorias vigentes

## Estado

Propuesta documental para revisión de Codex y aprobación humana. No autoriza implementación. No modifica `06-code/` ni inicia HU-003, HU-004, HU-010 ni otra HU.

## Autoridad y alcance revisado

- Requisitos oficiales ya documentados: OF-01, OF-03, OF-04, OF-06 y OF-07 exigen explorar/buscar convocatorias, REST propio, web funcional, consulta SECOP en vivo por entidad/fecha/estado y flujo E2E con usuario registrado.
- Decisiones aprobadas vigentes: backend hexagonal, frontend consume únicamente API propia, integración SECOP mediante adaptador backend, PostgreSQL como persistencia local y flujo privado derivado de usuario registrado.
- Estado productivo actual documentado: HU-001, HU-002 y HU-005 están fusionadas; existen registro, login JWT, `authenticatedFetch`, guard UX privado y `GET /api/v1/users/me`.
- Restricción de esta propuesta: HU-003 cubre solo exploración/listado inicial. Filtros avanzados quedan en HU-004; detalle mínimo en HU-010; favoritos en HU-006/HU-007; búsquedas guardadas en HU-008/HU-009; dashboard en HU-011.

## Fuente oficial SECOP II recomendada

- Dataset oficial de datos.gov.co: `SECOP II - Procesos de Contratación`.
- Identificador Socrata: `p6dx-8zbt`.
- Endpoint JSON: `https://www.datos.gov.co/resource/p6dx-8zbt.json`.
- Metadata oficial: `https://www.datos.gov.co/api/views/p6dx-8zbt`.
- Consulta viva acotada observada el 2026-07-22: el dataset responde con columnas como `id_del_proceso`, `referencia_del_proceso`, `entidad`, `nombre_del_procedimiento`, `descripci_n_del_procedimiento`, `estado_del_procedimiento`, `estado_de_apertura_del_proceso`, `estado_resumen`, `fecha_de_publicacion_del`, `fecha_de_recepcion_de`, `precio_base` y `urlproceso`.

## Justificación

Se recomienda `p6dx-8zbt` porque:

1. Corresponde explícitamente a SECOP II y no al ejemplo SECOP I mencionado como no definitivo en la documentación vigente.
2. Está publicado en datos.gov.co, fuente abierta oficial compatible con consulta pública JSON y SoQL.
3. Contiene campos suficientes para el browse mínimo: identidad de proceso, entidad, nombre/objeto, estado, fecha de publicación, fecha de recepción de respuestas, valor base y URL oficial del proceso.
4. Permite consultas acotadas por estado de apertura y fecha de recepción, evitando descargar el dataset completo.
5. Mantiene una URL pública hacia `community.secop.gov.co` para trazabilidad humana sin que el frontend consulte SECOP directamente.

## Definición operativa de “convocatorias vigentes”

Para HU-003, una convocatoria vigente es un registro del dataset `p6dx-8zbt` que cumple simultáneamente:

- `estado_de_apertura_del_proceso = 'Abierto'`.
- `fecha_de_recepcion_de >= fecha actual local de consulta a las 00:00:00`.
- Tiene `id_del_proceso` no vacío.

Notas:

- `fecha_de_recepcion_de` se usa como fecha límite operativa para recepción de respuestas/ofertas. En el DTO se expondrá como `closing_at`.
- Si `fecha_de_recepcion_de` está ausente, el registro no entra al listado vigente inicial porque no existe una fecha confiable para afirmar vigencia.
- `estado_resumen` y `estado_del_procedimiento` se exponen para trazabilidad, pero no sustituyen la regla mínima anterior.
- La zona horaria exacta de corte debe quedar implementada de forma determinista en backend; propuesta inicial: usar fecha local configurada del servidor y convertir el parámetro a literal ISO sin depender del navegador.

Consulta SoQL propuesta para HU-003 inicial:

```text
$select=id_del_proceso,referencia_del_proceso,entidad,nombre_del_procedimiento,descripci_n_del_procedimiento,estado_del_procedimiento,estado_de_apertura_del_proceso,estado_resumen,fecha_de_publicacion_del,fecha_de_recepcion_de,precio_base,urlproceso
$where=estado_de_apertura_del_proceso='Abierto' AND fecha_de_recepcion_de >= '<YYYY-MM-DD>T00:00:00'
$order=fecha_de_recepcion_de ASC, fecha_de_publicacion_del DESC, id_del_proceso ASC
$limit=<page_size>
$offset=<offset>
```

## Campos mínimos del DTO de listado

Respuesta propuesta del backend:

```json
{
  "items": [
    {
      "id": "CO1.REQ.10658713",
      "reference": "SA-SIE-016-2026 (Presentación de oferta)",
      "entity_name": "MUNICIPIO DE BRICEÑO",
      "title": "CONTRATAR EL ARRENDAMIENTO...",
      "description": "CONTRATAR EL ARRENDAMIENTO...",
      "status": "Publicado",
      "summary_status": "Presentación de oferta",
      "opening_status": "Abierto",
      "published_at": "2026-07-15T00:00:00.000",
      "closing_at": "2026-07-22T00:00:00.000",
      "estimated_amount_cop": 77500000,
      "source_url": "https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.10512397"
    }
  ],
  "page": 1,
  "page_size": 20,
  "has_more": true
}
```

Mapeo mínimo:

| DTO | Campo SECOP II | Regla |
|---|---|---|
| `id` | `id_del_proceso` | Obligatorio; clave estable externa. |
| `reference` | `referencia_del_proceso` | Opcional; texto trazable para usuario. |
| `entity_name` | `entidad` | Obligatorio para presentación; si falta, error de normalización del registro. |
| `title` | `nombre_del_procedimiento` | Obligatorio para tarjeta/listado. |
| `description` | `descripci_n_del_procedimiento` | Opcional; recortable en UI sin perder `title`. |
| `status` | `estado_del_procedimiento` | Valor original normalizado como texto. |
| `summary_status` | `estado_resumen` | Valor original para contexto de fase. |
| `opening_status` | `estado_de_apertura_del_proceso` | Debe ser `Abierto` para HU-003. |
| `published_at` | `fecha_de_publicacion_del` | Fecha ISO opcional. |
| `closing_at` | `fecha_de_recepcion_de` | Fecha ISO obligatoria para considerar vigencia. |
| `estimated_amount_cop` | `precio_base` | Entero COP; no convertir a centavos para el listado SECOP. |
| `source_url` | `urlproceso.url` | URL oficial opcional pero recomendada; nunca se usa como identificador primario. |

## Clave estable de convocatoria

La clave estable propuesta para HU-003 es `id_del_proceso` (`id` en DTO).

Razones:

- Es el identificador explícito del proceso dentro del dataset SECOP II.
- Es más estable que el enlace público, que depende de `noticeUID` y de la forma del portal `community.secop.gov.co`.
- Permite que HU-010 consulte detalle y que HU-006/HU-007 persistan favoritos contra una clave externa única.

Decisión pendiente: confirmar si `id_del_proceso` es único por fila en todos los lotes relevantes o si debe componerse con `referencia_del_proceso`/`urlproceso.url` para casos excepcionales. La implementación TDD debe incluir una prueba de duplicados simulados antes de persistir favoritos.

## Endpoint propio propuesto del backend

```text
GET /api/v1/opportunities?page=1&page_size=20
Authorization: Bearer <JWT>
```

Reglas:

- Privado: requiere JWT válido por consistencia con HU-003 actual, HU-002 y AC-HU-003-05.
- No acepta filtros de entidad/fecha/estado en HU-003; esos parámetros pertenecen a HU-004.
- `page` inicia en 1; valores no enteros o menores a 1 responden `422` con sobre estable.
- `page_size` por defecto 20; máximo inicial 50.
- El backend aplica timeout externo de 5 segundos a datos.gov.co.
- Errores externos se traducen a `503 external_service_unavailable` o equivalente estable sin filtrar payload interno de SECOP.

## Comportamiento esperado del frontend

- Nueva ruta privada propuesta: `/opportunities` o equivalente de navegación autenticada.
- La pantalla usa `authenticatedFetch('/api/v1/opportunities?page=1&page_size=20')`; nunca consulta datos.gov.co desde el navegador.
- Al montar la pantalla, solicita la primera página y renderiza tarjetas/filas con entidad, título, estado/fase, fecha límite, valor estimado y enlace “ver en SECOP” cuando exista.
- El enlace oficial abre en nueva pestaña con texto claro; no sustituye el detalle HU-010.
- La paginación inicial puede ser “Cargar más” o controles página anterior/siguiente, siempre alimentados por la API propia.
- No muestra filtros de entidad/fecha/estado todavía; pueden quedar deshabilitados o ausentes hasta HU-004 para evitar ampliar alcance.

## Estados de UI requeridos

1. `loading`: solicitud en curso; no muestra datos obsoletos como resultado vigente.
2. `empty`: respuesta exitosa con `items=[]`; comunica que no hay convocatorias vigentes según la regla acordada.
3. `external_error`: timeout, 5xx/4xx externo, JSON inválido o forma inesperada normalizada por backend; muestra mensaje recuperable sin detalles internos.
4. `success`: lista normalizada con controles de paginación y trazabilidad a SECOP.

El estado no autenticado se hereda de HU-002/HU-005 mediante `RequireAuth`/`authenticatedFetch` y no cuenta como estado SECOP de HU-003, aunque debe cubrirse en pruebas.

## Reglas de autenticación

HU-003 debe permanecer privada según el backlog actual:

- La historia dice “Como usuario autenticado”.
- Depende de HU-002.
- AC-HU-003-05 exige que un visitante sin sesión válida no obtenga resultados.
- IN-09 registró la inferencia de browse/filtros privados a partir de “usuarios registrados”.

Decisión pendiente: si Codex/humano decide permitir browse público, habría que modificar HU-003, HU-004, HU-010 y HU-011 antes de implementar. Con el estado actual, no se recomienda cambiarlo en esta iteración.

## Límites iniciales

- Página inicial: `page=1`.
- Tamaño por página: default 20, máximo 50.
- Orden: `fecha_de_recepcion_de ASC`, luego `fecha_de_publicacion_del DESC`, luego `id_del_proceso ASC`.
- Timeout externo: 5 segundos por solicitud a datos.gov.co.
- Sin caché persistente en HU-003. Cualquier caché debe ser efímero y no impedir consulta vigente.
- Sin reintentos automáticos iniciales en el flujo de usuario para evitar duplicar carga y confundir la evidencia; el usuario puede reintentar manualmente.

## Riesgos técnicos

- Disponibilidad: datos.gov.co puede responder lento, 5xx o cortar conexión.
- Rate limits: Socrata puede aplicar límites por IP o sin token; la app debe consultar acotadamente y tratar 429/403 como fallo externo controlado.
- Esquema cambiante: nombres con tildes normalizadas (`descripci_n_del_procedimiento`, `fecha_de_ultima_publicaci`) pueden variar o desaparecer; el normalizador debe fallar controladamente.
- Datos incompletos: `precio_base`, `urlproceso`, descripción o fechas pueden faltar o venir en formato inesperado.
- Semántica de vigencia: `Abierto` sin fecha de recepción futura existe en volumen alto; por eso no debe considerarse vigente sin `fecha_de_recepcion_de` confiable.
- Duplicidad o granularidad: procesos/lotes pueden generar registros con identificadores repetidos o variantes; debe verificarse antes de usar la clave en persistencia de favoritos.
- Moneda/monto: `precio_base` se observa como COP numérico; no convertir a centavos en HU-003 para evitar doble conversión.

## Criterios de aceptación ajustados propuestos

Los criterios existentes son válidos, pero se propone precisarlos antes de implementación:

- AC-HU-003-01 debe fijar `GET /api/v1/opportunities` como API propia y prohibir llamadas del navegador a datos.gov.co.
- AC-HU-003-02 debe nombrar explícitamente el DTO de listado anterior y `id_del_proceso` como clave estable propuesta.
- AC-HU-003-03 debe separar `loading`, `empty`, `external_error` y `success`.
- AC-HU-003-04 debe cubrir timeout, error HTTP, 429/rate limit, JSON inválido y payload sin campos mínimos.
- AC-HU-003-05 se conserva: HU-003 es privada salvo decisión explícita posterior.

## Microplan TDD para iteración posterior

1. RED dominio/aplicación: crear puerto `SecopOpportunitySource` y caso de uso `ListCurrentOpportunities`; fallar por ausencia de tipos/normalización.
2. GREEN mínimo aplicación: DTO interno, paginación validada, regla de vigencia y mapeo feliz con fixture SECOP controlado.
3. RED fallos de integración: timeout, HTTP 503/429, JSON inválido, lista vacía y registro sin campos mínimos.
4. GREEN infraestructura: adaptador HTTP datos.gov.co con `httpx`, timeout 5s, query SoQL acotada, errores externos sanitizados y sin dependencia de red en suite normal.
5. RED API: `GET /api/v1/opportunities` requiere Bearer, valida `page`/`page_size`, responde lista normalizada y error estable.
6. GREEN API: router privado FastAPI, wiring en bootstrap y headers privados coherentes con capacidades autenticadas.
7. RED frontend: ruta privada `/opportunities`, uso de `authenticatedFetch`, estados loading/empty/external_error/success y ausencia de filtros HU-004.
8. GREEN frontend: pantalla mínima accesible con listado, paginación inicial y enlace fuente.
9. RED/GREEN E2E controlado: usuario registrado/login navega a browse y ve fixtures servidos por backend mockeado o adaptador inyectado; sin Internet en test determinista.
10. Validación viva separada: una consulta real de solo lectura a datos.gov.co con `$limit` pequeño, marcada como evidencia externa no determinista.

## Decisiones pendientes antes de implementar

- Ratificar `p6dx-8zbt` como dataset definitivo para HU-003.
- Ratificar `id_del_proceso` como clave estable suficiente o definir clave compuesta si se detectan duplicados relevantes.
- Aprobar que `fecha_de_recepcion_de` es la fecha límite operativa para “vigente”.
- Aprobar el endpoint `GET /api/v1/opportunities` y el DTO mínimo.
- Confirmar que HU-003 continúa privada.
- Confirmar límites iniciales: page size 20/50, orden y timeout 5s.
