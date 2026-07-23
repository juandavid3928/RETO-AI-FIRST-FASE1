# Análisis técnico-documental HU-004 — Filtrar convocatorias

## Estado

Propuesta documental para revisión de Codex y aprobación humana. No autoriza implementación. No modifica `06-code/` ni crea backend, frontend, pruebas productivas o E2E. No inicia HU-010, HU-006, HU-007, HU-008, HU-009, HU-011 ni otra HU.

Estado base verificado antes de crear esta rama documental:

- Rama base: `main`.
- `main` y `origin/main`: `44a915acd905dadd562279202dd4c71ea5c1a4f0`.
- PR #8: cerrado y fusionado mediante GitHub.
- HU-003: integrada en `main`.
- Rama `feat/hu-003-explore-opportunities`: eliminada local y remotamente.
- Rama `backup/repository-structure-a0dfd0a`: conservada.
- Working tree: limpio.

## Alcance

HU-004 agrega filtros sobre la exploración privada de convocatorias ya implementada por HU-003.

Incluye definir, para una implementación posterior:

- filtros opcionales por entidad, rango de fecha límite y estado;
- contrato HTTP y errores;
- mapeo SoQL seguro hacia SECOP II;
- validaciones previas para evitar consultas inválidas a SECOP;
- comportamiento frontend mínimo;
- matriz TDD y E2E determinístico con stub SECOP.

Fuera de alcance de HU-004:

- endpoint de detalle o vista detalle HU-010;
- favoritos HU-006/HU-007;
- guardar o gestionar búsquedas HU-008/HU-009;
- dashboard HU-011;
- migraciones, nuevas tablas o persistencia de oportunidades;
- cambios de autenticación/JWT;
- cache persistente, recomendaciones, analítica o métricas externas.

## Base técnica heredada de HU-003

HU-004 debe extender lo ya integrado por HU-003:

- Endpoint backend actual: `GET /api/v1/opportunities?page=1&page_size=20`.
- Acceso privado con Bearer JWT y headers privados: `Cache-Control: no-store`, `Pragma: no-cache`, `Vary: Authorization`.
- Dataset SECOP II: `SECOP II - Procesos de Contratación`, Socrata `p6dx-8zbt`.
- Endpoint externo default: `https://www.datos.gov.co/resource/p6dx-8zbt.json`.
- Configuración runtime: `SECOP_BASE_URL` y `SECOP_TIMEOUT_SECONDS` desde `Settings`/`.env`.
- Regla HU-003 de vigencia: `estado_de_apertura_del_proceso='Abierto'` y `fecha_de_recepcion_de >= fecha actual de Colombia` calculada por backend.
- DTO vigente: `id`, `reference`, `entity_name`, `title`, `description`, `status`, `summary_status`, `opening_status`, `published_at`, `closing_at`, `estimated_amount_cop`, `source_url`.
- Paginación: `page` inicia en 1; `page_size` default 20 y máximo 50.
- Orden base: `fecha_de_recepcion_de ASC`, `fecha_de_publicacion_del DESC`, `id_del_proceso ASC`.
- Frontend: ruta privada `/opportunities`, `authenticatedFetch`, parser estricto, estados `loading`, `empty`, `external_error`, `success`.
- Arquitectura: dominio/aplicación no importan FastAPI, Pydantic, httpx ni infraestructura; SECOP permanece detrás de un puerto/adaptador backend.

## Contrato propuesto

Decisión documental cerrada para HU-004: extender el endpoint existente, no crear endpoint nuevo.

```text
GET /api/v1/opportunities?page=1&page_size=20&entity=<texto>&closing_from=YYYY-MM-DD&closing_to=YYYY-MM-DD&status=<valor>
Authorization: Bearer ***
```

Justificación:

- Los filtros refinan el mismo recurso paginado de HU-003: oportunidades vigentes.
- Evita duplicar DTO, headers privados, manejo de errores externos y navegación.
- Preserva compatibilidad: sin query params de filtro, la respuesta conserva el comportamiento HU-003.
- Mantiene el frontend aislado de datos.gov.co y centraliza SoQL/normalización en backend.

No se recomienda endpoint nuevo para HU-004. Un endpoint adicional solo se justificaría si Codex aprueba otra semántica, por ejemplo búsquedas guardadas persistidas HU-008/HU-009 o detalle HU-010, que no pertenecen a esta historia.

## Query params propuestos

| Parámetro | Tipo | Opcional | Semántica |
|---|---|---:|---|
| `entity` | string | Sí | Coincidencia parcial por entidad SECOP. |
| `closing_from` | date `YYYY-MM-DD` | Sí | Fecha límite mínima inclusiva. |
| `closing_to` | date `YYYY-MM-DD` | Sí | Fecha límite máxima inclusiva. |
| `status` | enum string | Sí | Fase/estado controlado sobre `estado_resumen`. |
| `page` | int | Sí | Página 1..n, heredada de HU-003. |
| `page_size` | int | Sí | Tamaño 1..50, heredado de HU-003. |

Parámetros desconocidos: deben rechazarse con `422 validation_error`; no se deben ignorar silenciosamente porque podrían ocultar errores de UI o de futuras búsquedas guardadas.

## Semántica de filtro por entidad

Decisión propuesta:

- Campo SECOP: `entidad`.
- Query param: `entity`.
- Coincidencia: parcial.
- Case: insensible a mayúsculas/minúsculas.
- Normalización: trim exterior, colapsar espacios internos consecutivos a uno y rechazar resultado vacío.
- Longitud: mínimo 3 caracteres después de normalizar; máximo 120 caracteres.
- Caracteres: permitir texto Unicode, números, espacios y signos comunes de nombres institucionales; escapar comillas simples para SoQL o construir el predicado mediante helper de quoting controlado.
- Semántica SoQL cerrada: `upper(entidad) like '%<ENTITY_UPPER_ESCAPED>%'`. La consulta viva de solo lectura ejecutada para este PR confirmó compatibilidad de Socrata con `upper(entidad) like` sobre `p6dx-8zbt`.

Justificación del mínimo de 3 caracteres: reduce consultas masivas y ruido, sin impedir búsquedas reales como `SENA`, `ANI` o municipios de nombres cortos.

## Semántica del rango de fechas

Decisión propuesta:

- Campo SECOP: `fecha_de_recepcion_de`.
- `closing_from`: inclusivo.
- `closing_to`: inclusivo.
- Formato aceptado: `YYYY-MM-DD` estricto.
- Zona horaria: fechas interpretadas como fecha civil de Colombia por el backend.
- Conversión SoQL:
  - `closing_from=2026-08-01` → `fecha_de_recepcion_de >= '2026-08-01T00:00:00'`.
  - `closing_to=2026-08-31` → `fecha_de_recepcion_de <= '2026-08-31T23:59:59'`.
- Si solo llega `closing_from`, aplica límite inferior adicional.
- Si solo llega `closing_to`, aplica límite superior adicional.
- Si ambos llegan, deben cumplir `closing_from <= closing_to`.

Convivencia con HU-003:

- HU-003 siempre mantiene `fecha_de_recepcion_de >= fecha actual de Colombia a las 00:00:00`.
- El filtro efectivo inferior es el más restrictivo entre fecha actual Colombia y `closing_from`.
- `closing_to` puede acotar hacia una fecha futura cercana.
- Si `closing_to` es anterior a la fecha actual Colombia, la consulta es válida y debe producir `empty` mediante short-circuit local, sin consultar SECOP, porque la regla de vigencia HU-003 hace imposible cualquier coincidencia.

No se propone filtrar por `fecha_de_publicacion_del` para HU-004 porque la historia habla de oportunidad vigente y HU-003 ya modela `fecha_de_recepcion_de` como `closing_at`/fecha límite operativa.

## Semántica de estado

Decisión propuesta: `status` debe mapear a `estado_resumen`, manteniendo siempre `estado_de_apertura_del_proceso='Abierto'` como regla obligatoria de HU-003.

Campos evaluados:

| Campo SECOP | Uso propuesto | Razón |
|---|---|---|
| `estado_de_apertura_del_proceso` | Regla base fija, no filtro libre. | Define apertura/vigencia HU-003. Permitir otros valores rompería la promesa de oportunidades vigentes. |
| `estado_resumen` | Filtro HU-004 recomendado. | Representa fase visible como “Presentación de oferta” y ya está en el DTO como `summary_status`. |
| `estado_del_procedimiento` | Expuesto como `status`, no filtro inicial recomendado. | Puede ser amplio/ambiguo (“Publicado”) y menos útil para reducir fases de oportunidad. |
| Combinación | No recomendada inicialmente. | Aumenta ambigüedad, enum y pruebas sin valor mínimo adicional. |

Enum cerrado para `status` en HU-004 inicial:

- `presentation` → `estado_resumen = 'Presentación de oferta'`.

No se agregan otros valores de estado en HU-004 inicial. `published`/`estado_del_procedimiento='Publicado'` queda fuera porque mezclarlo con `estado_resumen` ampliaría la semántica y produciría ambigüedad frente al DTO `status`. Si una iteración posterior requiere más estados, deberá aprobarse como ampliación documental antes de código.

Decisión concreta: aceptar únicamente `status=presentation` en HU-004 inicial y mapearlo a `estado_resumen='Presentación de oferta'`.

Esta decisión conserva la regla HU-003: todos los resultados siguen siendo abiertos y vigentes.

## Mapeo SECOP y SoQL propuesto

Predicados base heredados:

```text
estado_de_apertura_del_proceso='Abierto'
fecha_de_recepcion_de >= '<today_colombia> T00:00:00'
id_del_proceso IS NOT NULL
```

Predicados HU-004 opcionales:

```text
-- entity
upper(entidad) like '%<ENTITY_NORMALIZED_UPPER_ESCAPED>%'

-- closing_from
fecha_de_recepcion_de >= '<closing_from>T00:00:00'

-- closing_to
fecha_de_recepcion_de <= '<closing_to>T23:59:59'

-- status=presentation
estado_resumen='Presentación de oferta'
```

Construcción recomendada:

1. Validar y normalizar filtros en aplicación antes de llamar al puerto SECOP.
2. Pasar un objeto de filtros tipado al puerto, no strings SoQL crudos.
3. El adaptador SECOP traduce filtros tipados a SoQL mediante helpers de quoting/escaping probados.
4. Unir predicados con `AND`; los filtros combinados son intersección.
5. Mantener `$limit=page_size+1`, `$offset` y `$order` de HU-003.

## Verificación viva SECOP para `upper(entidad) like`

Consulta ejecutada como evidencia externa no determinística, de solo lectura y acotada:

```bash
curl -sS --get 'https://www.datos.gov.co/resource/p6dx-8zbt.json' \
  --data-urlencode '$select=id_del_proceso,entidad,estado_resumen,fecha_de_recepcion_de' \
  --data-urlencode '$where=estado_de_apertura_del_proceso="Abierto" AND fecha_de_recepcion_de >= "2026-07-23T00:00:00" AND upper(entidad) like "%MUNICIPIO%"' \
  --data-urlencode '$limit=1'
```

Resultado observado:

- HTTP `200`.
- 1 registro devuelto.
- Campos presentes: `id_del_proceso`, `entidad`, `estado_resumen`, `fecha_de_recepcion_de`.
- Muestra: `entidad="MUNICIPIO DE SUCRE"`, `estado_resumen="Presentación de oferta"`, `fecha_de_recepcion_de="2026-07-23T00:00:00.000"`.

Conclusión: Socrata acepta `upper(entidad) like` en el dataset `p6dx-8zbt`; HU-004 puede cerrar la semántica case-insensitive con ese predicado, manteniendo tests determinísticos con stub para implementación posterior.

## Validaciones

| Caso | Resultado propuesto | Consulta SECOP |
|---|---|---|
| `entity` ausente | Válido. | Sí, sin predicado entidad. |
| `entity=''` o solo espacios | `422 validation_error`. | No. |
| `entity` normalizado < 3 chars | `422 validation_error`. | No. |
| `entity` > 120 chars | `422 validation_error`. | No. |
| `closing_from` formato inválido | `422 validation_error`. | No. |
| `closing_to` formato inválido | `422 validation_error`. | No. |
| `closing_from > closing_to` | `422 validation_error`. | No. |
| `closing_to` anterior a hoy Colombia | `200 empty` por short-circuit local. | No. |
| `status` no permitido | `422 validation_error`. | No. |
| parámetro desconocido | `422 validation_error`. | No. |
| `page`/`page_size` inválidos | `422 validation_error`, igual que HU-003. | No. |
| filtros válidos sin coincidencias | `200` con `items=[]`, `has_more=false`. | Sí, salvo short-circuit imposible. |

Interacción con paginación:

- La paginación se aplica después de todos los filtros.
- Cambiar cualquier filtro en frontend debe reiniciar `page=1`.
- `has_more` conserva la técnica `page_size+1` después de aplicar filtros.
- Si una página posterior queda vacía por cambios externos del dataset, se muestra `empty` para esa consulta sin tratarlo como error.

## Contrato de error

Errores de validación local de filtros:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Opportunity query is invalid.",
    "fields": {
      "closing_from": ["Use YYYY-MM-DD."],
      "closing_to": ["Must be on or after closing_from."],
      "status": ["Unsupported opportunity status."],
      "entity": ["Use 3 to 120 characters."],
      "query": ["Unknown query parameter."]
    }
  }
}
```

Propuesta:

- HTTP: `422`.
- Código: `validation_error`.
- Mensaje estable: `Opportunity query is invalid.`.
- `fields`: incluir campos específicos cuando aplique.
- Headers privados: iguales a HU-003 para `/api/v1/opportunities`.
- Garantía: filtros inválidos no invocan el caso de uso ni el adaptador SECOP.

Errores externos de SECOP:

- HTTP: `503`.
- Código: `external_service_unavailable`.
- Mensaje: `Opportunities are temporarily unavailable.`.
- Frontend: estado `external_error`, con opción de reintentar y filtros preservados en pantalla.

Autenticación:

- Se hereda HU-003/HU-002: `401 authentication_required` o `401 invalid_token`; no entrega datos derivados de SECOP.

## Comportamiento frontend

Controles mínimos:

- Campo texto “Entidad” (`entity`) con ayuda “mínimo 3 caracteres”.
- Dos campos de fecha nativos o accesibles: “Desde” (`closing_from`) y “Hasta” (`closing_to`).
- Select “Estado” (`status`) con valores aprobados; inicialmente “Cualquier estado vigente” y “Presentación de oferta”.
- Botón “Aplicar filtros”.
- Botón “Limpiar filtros”.

Estados:

- `idle/success`: muestra resultados actuales y formulario.
- `loading`: deshabilita aplicación duplicada y anuncia carga con `role=status`.
- `empty`: filtros válidos sin coincidencias; no es error.
- `validation_error`: muestra errores por campo sin borrar resultados previos.
- `external_error`: conserva filtros y permite reintentar.
- `unauthorized`: se hereda de `authenticatedFetch`/guard privado.

Accesibilidad:

- Cada control debe tener label visible.
- Errores asociados por campo y anunciados con `role=alert` o región viva apropiada.
- Botones con texto claro; no depender solo de color.
- Al aplicar filtros, mover foco de forma no intrusiva al resumen de resultados o al primer error.

Preservación y limpieza:

- Al editar filtros no se debe consultar automáticamente en cada tecla para evitar rate limits; aplicar con botón o submit del formulario.
- Al aplicar filtros válidos, resetear a `page=1` y consultar API propia.
- Si hay `validation_error`, conservar resultados previos y mostrar errores.
- “Limpiar filtros” borra filtros, vuelve a `page=1` y recupera comportamiento HU-003.
- No persistir filtros en localStorage para HU-004; esa capacidad pertenece a HU-008/HU-009.

Exclusiones explícitas de UI:

- No agregar vista detalle, drawer/modal de detalle ni navegación a HU-010.
- No agregar guardar favorito.
- No agregar guardar búsqueda.
- No agregar dashboard, métricas, recomendaciones o analítica.

## Pruebas TDD propuestas

Backend aplicación:

1. RED: `ListCurrentOpportunities` no acepta filtros tipados; agregar `OpportunityFilters` con validación de entidad, fechas y estado.
2. GREEN: filtros válidos llegan al puerto; inválidos lanzan error de query sin tocar la fuente.
3. RED/GREEN: `closing_to < today_colombia` retorna página vacía sin llamar SECOP.
4. RED/GREEN: paginación y filtros se combinan sin cambiar límites 1..50.

Adaptador SECOP:

1. RED: `SecopOpportunitySource` no genera predicados opcionales.
2. GREEN: construye SoQL con `AND`, quoting seguro, `$limit=page_size+1`, `$offset` y orden estable.
3. RED/GREEN: entidad con comillas, espacios múltiples y mayúsculas/minúsculas no rompe encoding.
4. RED/GREEN: `status=presentation` mapea exactamente a `estado_resumen='Presentación de oferta'`.
5. RED/GREEN: filtros válidos sin coincidencias retornan página vacía, no error.

API:

1. RED: `GET /api/v1/opportunities?entity=minsalud&closing_from=2026-08-01&closing_to=2026-08-31&status=presentation` debe invocar el caso de uso con filtros tipados.
2. RED/GREEN: cada filtro inválido devuelve `422 validation_error`, `Opportunity query is invalid.`, fields específicos y headers privados.
3. RED/GREEN: parámetros desconocidos devuelven `422` sin invocar el caso de uso.
4. Regresión: login y registro conservan sus mensajes de validación.

Frontend:

1. RED: servicio `fetchOpportunities` no acepta filtros; agregar serialización con `URLSearchParams`.
2. RED/GREEN: no envía params vacíos; serializa fechas y estado permitidos.
3. RED/GREEN: página muestra controles accesibles, aplica filtros, limpia filtros y preserva resultados ante validación local/API.
4. RED/GREEN: `external_error` mantiene filtros y permite reintentar.

No crear estas pruebas hasta aprobación explícita de implementación HU-004.

## E2E determinístico propuesto

Usar el mismo patrón de HU-003 con stub SECOP local y sin Internet:

1. Levantar PostgreSQL 16 en volumen limpio.
2. Ejecutar Alembic `upgrade head`.
3. Levantar backend con `SECOP_BASE_URL` apuntando al stub local y `SECOP_TIMEOUT_SECONDS=5`.
4. El stub debe validar query params Socrata recibidos y devolver fixtures diferenciados:
   - sin filtros: varias oportunidades vigentes;
   - `entity=SENA`: solo entidad esperada;
   - rango de fechas: resultados dentro del rango;
   - `status=presentation`: solo `estado_resumen='Presentación de oferta'`;
   - combinación de filtros: intersección;
   - sin coincidencias: lista vacía.
5. Ejecutar flujo browser: registro → login → perfil/opportunities → aplicar filtros → ver resultados esperados → limpiar filtros.
6. Verificar que el navegador llama solo al backend propio y nunca a datos.gov.co/community.secop.gov.co para obtener listado.
7. Mantener consulta viva SECOP real como verificación manual/acotada separada y no determinística, nunca como test normal.

## Riesgos

- SoQL: diferencias en soporte de funciones como `upper`, escaping de comillas y precedencia de `AND` pueden alterar resultados.
- Encoding: tildes, espacios, comillas, `%`, `_` y caracteres Unicode en entidad requieren escaping y tests explícitos.
- Rate limits: filtros demasiado amplios o submit por cada tecla pueden aumentar presión sobre datos.gov.co.
- Campos SECOP inconsistentes: `entidad`, `estado_resumen` o fechas pueden faltar o cambiar de forma; normalizador debe fallar controladamente.
- Estado ambiguo: `estado_resumen`, `estado_del_procedimiento` y `estado_de_apertura_del_proceso` no son equivalentes; mezclar sin enum aprobado rompería expectativas.
- Paginación con filtros: cambios del dataset entre páginas pueden causar duplicados/omisiones; se acepta para consulta viva sin persistencia.
- Fechas límite: zona Colombia vs timestamp Socrata puede generar bordes al inicio/fin del día; documentar y probar inclusividad.
- Short-circuit local: `closing_to` anterior a hoy evita tráfico externo pero debe comunicar empty, no error.
- Futuras búsquedas guardadas: HU-004 no persiste filtros; el contrato debe ser estable para HU-008/HU-009 sin implementarlas ahora.

## Decisiones cerradas para HU-004 inicial

Estas decisiones cierran las opciones pendientes dentro del PR documental y forman el contrato a aprobar antes de código:

1. HU-004 extiende `GET /api/v1/opportunities` con query params opcionales; no se crea endpoint nuevo.
2. Nombres exactos de query params: `entity`, `closing_from`, `closing_to`, `status`.
3. `entity` usa mínimo/máximo 3..120 caracteres después de normalizar espacios.
4. `entity` usa `upper(entidad) like '%<ENTITY_UPPER_ESCAPED>%'`; la consulta viva SECOP confirmó compatibilidad.
5. `status` inicial acepta solo `presentation` y mapea a `estado_resumen='Presentación de oferta'`.
6. No se agregan más valores de estado en HU-004 inicial; cualquier ampliación requiere aprobación documental posterior.
7. Parámetros desconocidos se rechazan con `422 validation_error`.
8. `closing_to` anterior a hoy Colombia retorna página vacía mediante short-circuit local y no consulta SECOP.
9. HU-004 no persiste filtros; persistencia de criterios queda reservada para HU-008/HU-009.

## Microplan de implementación posterior

1. Usar las decisiones cerradas de este documento como contrato base; no reabrir endpoint, nombres, estado inicial o persistencia sin aprobación explícita.
2. RED aplicación: filtros tipados, validaciones, short-circuit y no invocación de SECOP ante errores.
3. GREEN aplicación: `OpportunityFilters` y extensión del caso de uso conservando paginación HU-003.
4. RED adaptador: SoQL con predicados opcionales y escaping.
5. GREEN adaptador: traducción segura a Socrata, fixtures de éxito/empty/encoding/status.
6. RED API: query params opcionales, parámetros desconocidos, errores fields y headers privados.
7. GREEN API: wiring FastAPI sin romper login/registro/HU-003 sin filtros.
8. RED frontend servicio: serialización de filtros con `URLSearchParams` y errores.
9. GREEN frontend UI: formulario accesible, aplicar/limpiar, conservar resultados ante errores.
10. RED/GREEN E2E con stub SECOP: registro/login/perfil/oportunidades filtradas sin Internet.
11. Validación final full-stack con PostgreSQL real, frontend completo, build, audit, locks, Compose, frontera hexagonal, secretos, diff y limpieza.
12. Actualizar README/SOUL/changelog con evidencia real solo después de implementación aprobada.
