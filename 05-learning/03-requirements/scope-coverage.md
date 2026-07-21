# Cobertura y trazabilidad del alcance

## Estado

Matriz propuesta para revisión. El backlog cubre el producto mínimo oficial sin autorizar código.

## Matriz requisito → historias

| Requisito | Descripción resumida | Historias que lo cubren | Cobertura |
|---|---|---|---|
| OF-01 | Explorar, filtrar y guardar convocatorias como usuario registrado. | HU-001, HU-002, HU-003, HU-004, HU-006, HU-007. | Completa. |
| OF-02 | Registro, login JWT y perfil propio. | HU-001, HU-002, HU-005. | Completa; campos y políticas pendientes. |
| OF-03 | REST para búsqueda, filtros y bookmarks. | HU-003, HU-004, HU-006, HU-007, HU-010. | Completa a nivel funcional; HU-010 reutiliza el contrato mínimo de convocatoria. |
| OF-04 | Web funcional para browse, favoritos y perfil. | HU-003, HU-004, HU-005, HU-006, HU-007, HU-010, HU-011. | Completa a nivel funcional; detalle y dashboard se limitan a AP-07. |
| OF-05 | Persistencia de usuarios, bookmarks y búsquedas guardadas. | HU-001, HU-005, HU-006, HU-007, HU-008, HU-009. | Completa; modelo físico pendiente. |
| OF-06 | Consulta SECOP en vivo por entidad, fecha y estado. | HU-003, HU-004, HU-009. | Completa; dataset y mapeo pendientes. |
| OF-07 | E2E auth + browse + bookmarks persistidos. | HU-001, HU-002, HU-003, HU-006, HU-007, HU-010. | Completa como flujo incremental; el detalle mínimo apoya la decisión previa al bookmark. |
| OF-08 | Aplicación local con backend, frontend, DB e integración. | TT-02, TT-04, TT-05, TT-07 y slices de todas las HU. | Tarea de entrega, no HU independiente. |
| OF-09 | Repo público, README, SOUL y demo. | TT-08. | Tarea de entrega y trazabilidad. |

## Matriz historia → fuente y dependencia

| HU | Fuente principal | Dependencias | Prioridad | Estado |
|---|---|---|---|---|
| HU-001 | OF-01, OF-02, OF-05 | — | P0 | Refinada; pendiente de aprobación. |
| HU-002 | OF-01, OF-02, OF-07 | HU-001 | P0 | Refinada; pendiente de aprobación. |
| HU-003 | OF-01, OF-03, OF-04, OF-06, OF-07 | HU-002 | P0 | Refinada; pendiente de aprobación. |
| HU-004 | OF-01, OF-03, OF-06 | HU-003 | P0 | Agregada por división; pendiente. |
| HU-005 | OF-02, OF-04 | HU-002 | P0 | Agregada; pendiente. |
| HU-006 | OF-01, OF-03, OF-04, OF-05, OF-07 | HU-002, HU-003 | P0 | Agregada; pendiente. |
| HU-007 | OF-01, OF-03, OF-04, OF-05, OF-07 | HU-006 | P0 | Agregada; pendiente. |
| HU-008 | OF-05 | HU-004 | P0 | Agregada con inferencia explícita; pendiente. |
| HU-009 | OF-05, OF-06 | HU-003, HU-004, HU-008 | P0 | Agregada con inferencia explícita; pendiente. |
| HU-010 | AP-07; OF-03, OF-04; IN-07, IN-10 | HU-003 | P0 | Agregada con alcance mínimo aprobado; pendiente. |
| HU-011 | AP-07; OF-04; IN-01, IN-11 | HU-003, HU-007, HU-009 | P0 | Agregada como resumen de capacidades existentes; pendiente. |

## Grafo y orden incremental

```text
HU-001 → HU-002 ─┬→ HU-005
                  └→ HU-003 ─┬→ HU-004 → HU-008 → HU-009 ─┐
                             ├→ HU-010                     ├→ HU-011
                             └→ HU-006 → HU-007 ───────────┘
```

HU-009 también depende de HU-003 y HU-004. HU-011 depende de HU-003, HU-007 y HU-009. El grafo no contiene ciclos.

Orden recomendado: HU-001, HU-002, HU-005, HU-003, HU-004, HU-010, HU-006, HU-007, HU-008, HU-009, HU-011.

## Evaluación de las historias anteriores

### Conservadas

- **HU-001 — Registro:** se conserva el propósito y se agregan valor, prioridad, fuentes, dependencias y criterios observables.
- **HU-002 — Login/JWT:** se conserva el propósito y se explicitan seguridad, acceso privado y dependencia de registro.
- **HU-003 — Búsqueda SECOP:** conserva el objetivo central, se renombra como exploración de convocatorias vigentes y se acota al browse.

### Modificadas

- **HU-001, HU-002 y HU-003:** todas pasan de descripciones mínimas a historias trazables y verificables.
- **HU-003:** deja de concentrar browse, filtros y manejo de integración en una sola historia.

### Divididas

- La búsqueda original se divide en **HU-003 — Explorar convocatorias vigentes** y **HU-004 — Filtrar convocatorias**.
- La gestión de bookmarks se modela como **HU-006 — Guardar favorita** y **HU-007 — Gestionar favoritos**.
- La gestión de búsquedas guardadas se modela como **HU-008 — Guardar criterios** y **HU-009 — Gestionar búsquedas guardadas**.

### Agregadas

- **HU-004:** filtros por entidad, fecha y estado.
- **HU-005:** perfil propio.
- **HU-006 y HU-007:** ciclo persistente de favoritos.
- **HU-008 y HU-009:** ciclo persistente y reutilizable de búsquedas guardadas.
- **HU-010:** detalle mínimo de una convocatoria, ordenado por AP-07 y acotado mediante IN-10.
- **HU-011:** dashboard resumen de capacidades existentes, ordenado por AP-07 y acotado mediante IN-11.

### Combinadas

- Ninguna. Combinar creación y gestión de recursos produciría slices demasiado amplios.

### Retiradas

- Ninguna de las tres historias iniciales fue retirada.
- El detalle ampliado continúa fuera de alcance: HU-010 cubre únicamente el detalle mínimo aprobado.
- No se promovieron a HU funcionalidades sin respaldo suficiente como notificaciones, administración, recuperación de contraseña, analítica, recomendaciones o métricas externas.

## Cobertura de criterios de calidad

| Regla de refinamiento | Resultado documental |
|---|---|
| Cada HU entrega valor a un actor. | Todas usan visitante o usuario autenticado y declaran valor. |
| Requisitos obligatorios cubiertos. | OF-01 a OF-07 tienen HU; OF-08 y OF-09 tienen tareas técnicas. |
| Criterios observables. | AC identificados en formato Dado/Cuando/Entonces. |
| Sin duplicados. | Browse/filtros, crear/gestionar favoritos y crear/gestionar búsquedas tienen límites distintos. |
| Dependencias sin ciclos. | Grafo dirigido acíclico documentado. |
| Inferencias identificadas. | IN-01 a IN-11 están separadas de fuentes oficiales y decisiones. |
| Tareas técnicas separadas. | TT-01 a TT-08 no están redactadas como HU. |
| Alcance manejable. | Cada recurso persistente separa creación de consulta/eliminación; detalle y dashboard reutilizan capacidades existentes sin ampliarlas. |

## Riesgos y decisiones pendientes

- La fuente oficial ofrece un endpoint SECOP I como ejemplo, pero no fija el dataset definitivo.
- Faltan campos de perfil, política JWT y contraseña.
- Faltan DTO, paginación, orden y semántica exacta de fecha/estado.
- La política de nombre único para búsquedas guardadas es una inferencia y requiere ratificación.
- El backlog propone browse y filtros privados a partir de “usuarios registrados”, pero debe ratificarse si habrá consulta pública.
- Debe definirse qué snapshot mínimo conserva un bookmark y cómo se representa una convocatoria retirada.
- Falta ratificar el mapeo exacto de los campos mínimos del detalle HU-010 dentro del DTO.
- Falta decidir si HU-011 resume la página vigente o una consulta predeterminada y cómo comunica el límite del conjunto.
- El dashboard podría confundirse con analítica; se mantiene explícitamente restringido a datos de HU-003, HU-007 y HU-009.
- Caché, reintentos, rate limits y timeouts requieren decisión técnica sin crear nuevas HU.
- Faltan umbrales verificables de accesibilidad, rendimiento y observabilidad sin datos sensibles.

## Fuera de alcance

Administración, escritura en SECOP, notificaciones, búsquedas programadas, recuperación de contraseña, MFA, login social, perfil editable avanzado, detalle ampliado, recomendaciones, analítica, métricas externas, colaboración, operación offline y soporte multi-dataset permanecen fuera hasta una decisión explícita.
