# Backlog de historias de usuario

## Estado

Backlog funcional completo. HU-001, HU-002, HU-003 y HU-005 fueron fusionadas o implementadas en la rama vigente. HU-004 y HU-006 a HU-011 no autorizan implementación y requieren aprobación de criterios, contrato y microplan.

Prioridad:

- **P0:** necesaria para cubrir el producto mínimo aprobado.
- **P1:** valiosa pero no necesaria para el mínimo.

Todas las historias de este backlog son P0: HU-001 a HU-009 trazan al mínimo oficial y HU-010/HU-011 resuelven la cobertura funcional mínima aprobada por la instrucción de reanudación. Las decisiones técnicas se mantienen fuera de las HU.

## Orden de implementación propuesto

1. HU-001 — Crear una cuenta.
2. HU-002 — Iniciar sesión.
3. HU-005 — Consultar el perfil propio.
4. HU-003 — Explorar convocatorias vigentes.
5. HU-004 — Filtrar convocatorias.
6. HU-010 — Consultar detalle de convocatoria.
7. HU-006 — Guardar una convocatoria favorita.
8. HU-007 — Gestionar favoritos.
9. HU-008 — Guardar criterios de búsqueda.
10. HU-009 — Gestionar búsquedas guardadas.
11. HU-011 — Visualizar dashboard resumen.

El orden respeta dependencias y entrega valor incremental sin ciclos.

## HU-001 — Crear una cuenta

**Historia:** Como visitante, quiero crear una cuenta para acceder de forma identificada al portal.

- **Valor de negocio:** habilita la relación individual con perfil, favoritos y búsquedas guardadas.
- **Prioridad:** P0.
- **Dependencias:** ninguna HU.
- **Fuente:** OF-01, OF-02, OF-05.
- **Estado:** implementada, validada y fusionada en `main`.
- **Criterios:** AC-HU-001-01 a AC-HU-001-06 en `acceptance-criteria.md`.

## HU-002 — Iniciar sesión

**Historia:** Como usuario registrado, quiero iniciar sesión para acceder de manera segura a mis funcionalidades privadas.

- **Valor de negocio:** protege la experiencia personal y permite atribuir recursos a su propietario.
- **Prioridad:** P0.
- **Dependencias:** HU-001.
- **Fuente:** OF-01, OF-02, OF-07.
- **Estado:** implementada, validada y fusionada en `main`.
- **Criterios:** AC-HU-002-01 a AC-HU-002-03.

## HU-003 — Explorar convocatorias vigentes

**Historia:** Como usuario autenticado, quiero explorar convocatorias públicas obtenidas desde SECOP para identificar oportunidades relevantes con información vigente.

- **Valor de negocio:** entrega el objetivo central del portal sin obligar al usuario a consultar directamente la fuente abierta.
- **Prioridad:** P0.
- **Dependencias:** HU-002.
- **Fuente:** OF-01, OF-03, OF-04, OF-06, OF-07; AP-03, AP-04; IN-06, IN-07, IN-09.
- **Estado:** implementada y validada en `feat/hu-003-explore-opportunities`; pendiente de revisión mediante PR.
- **Criterios:** AC-HU-003-01 a AC-HU-003-05.

## HU-004 — Filtrar convocatorias

**Historia:** Como usuario autenticado, quiero filtrar convocatorias por entidad, fecha y estado para reducir los resultados a oportunidades relevantes.

- **Valor de negocio:** disminuye el esfuerzo de revisión sobre un volumen amplio de contratación pública.
- **Prioridad:** P0.
- **Dependencias:** HU-003.
- **Fuente:** OF-01, OF-03, OF-06; IN-02, IN-08, IN-09.
- **Estado:** agregada al dividir el alcance de búsqueda de la HU-003 original; pendiente de aprobación para implementación.
- **Criterios:** AC-HU-004-01 a AC-HU-004-04.

## HU-005 — Consultar el perfil propio

**Historia:** Como usuario autenticado, quiero consultar mi perfil para confirmar la identidad con la que uso el portal.

- **Valor de negocio:** hace visible la propiedad de la cuenta y de sus recursos privados.
- **Prioridad:** P0.
- **Dependencias:** HU-002.
- **Fuente:** OF-02, OF-04; IN-01.
- **Estado:** implementada, validada y fusionada en `main`.
- **Criterios:** AC-HU-005-01 a AC-HU-005-03.

## HU-006 — Guardar una convocatoria favorita

**Historia:** Como usuario autenticado, quiero guardar una convocatoria como favorita para poder retomarla sin volver a localizarla.

- **Valor de negocio:** conserva oportunidades relevantes entre sesiones y habilita el flujo end-to-end evaluado.
- **Prioridad:** P0.
- **Dependencias:** HU-002, HU-003.
- **Fuente:** OF-01, OF-03, OF-04, OF-05, OF-07; IN-01, IN-05, IN-07.
- **Estado:** agregada al explicitar la creación de bookmarks; pendiente de aprobación para implementación.
- **Criterios:** AC-HU-006-01 a AC-HU-006-04.

## HU-007 — Gestionar favoritos

**Historia:** Como usuario autenticado, quiero consultar y retirar mis convocatorias favoritas para mantener una selección personal útil.

- **Valor de negocio:** permite recuperar y depurar la colección persistida creada por el usuario.
- **Prioridad:** P0.
- **Dependencias:** HU-006.
- **Fuente:** OF-01, OF-03, OF-04, OF-05, OF-07; IN-01.
- **Estado:** agregada y separada de la creación del bookmark para mantener un incremento manejable; pendiente de aprobación para implementación.
- **Criterios:** AC-HU-007-01 a AC-HU-007-03.

## HU-008 — Guardar criterios de búsqueda

**Historia:** Como usuario autenticado, quiero guardar un conjunto de filtros con un nombre para reutilizar una búsqueda relevante más adelante.

- **Valor de negocio:** reduce el trabajo repetitivo al volver a consultar segmentos frecuentes del mercado público.
- **Prioridad:** P0.
- **Dependencias:** HU-004.
- **Fuente:** OF-05; IN-01, IN-03.
- **Estado:** agregada para convertir la persistencia oficial de búsquedas guardadas en valor observable; pendiente de ratificar IN-03 y aprobar implementación.
- **Criterios:** AC-HU-008-01 a AC-HU-008-04.

## HU-009 — Gestionar búsquedas guardadas

**Historia:** Como usuario autenticado, quiero consultar, ejecutar y eliminar mis búsquedas guardadas para reutilizar criterios sobre datos vigentes y mantener organizada mi lista.

- **Valor de negocio:** completa el ciclo de uso de la búsqueda persistida y conserva la consulta en vivo exigida por el reto.
- **Prioridad:** P0.
- **Dependencias:** HU-003, HU-004, HU-008.
- **Fuente:** OF-05, OF-06; IN-01, IN-04.
- **Estado:** agregada y separada de la creación para mantener un incremento manejable; pendiente de aprobación para implementación.
- **Criterios:** AC-HU-009-01 a AC-HU-009-04.

## HU-010 — Consultar detalle de convocatoria

**Historia:** Como usuario autenticado, quiero consultar el detalle mínimo de una convocatoria seleccionada para comprender sus datos esenciales y decidir si deseo conservarla como favorita.

- **Valor de negocio:** reduce la incertidumbre antes de guardar una oportunidad sin ampliar el portal con capacidades no confirmadas.
- **Prioridad:** P0.
- **Dependencias:** HU-003.
- **Fuente:** AP-07; OF-03, OF-04 como respaldo del browse; IN-07, IN-10. La referencia visual solo orienta presentación y no amplía el alcance funcional.
- **Estado:** agregada por instrucción aprobada para completar la cobertura mínima; pendiente de aprobación para implementación.
- **Criterios:** AC-HU-010-01 a AC-HU-010-04.

## HU-011 — Visualizar dashboard resumen

**Historia:** Como usuario autenticado, quiero visualizar un dashboard con el resumen de mis convocatorias visibles, favoritos y búsquedas guardadas para retomar rápidamente las capacidades ya disponibles en el portal.

- **Valor de negocio:** concentra el acceso a información ya respaldada por el backlog sin introducir analítica, recomendaciones ni métricas externas.
- **Prioridad:** P0.
- **Dependencias:** HU-003, HU-007, HU-009.
- **Fuente:** AP-07; OF-04 como respaldo de la interfaz web; IN-01, IN-11. La referencia visual solo orienta presentación y no autoriza nuevas métricas.
- **Estado:** agregada por instrucción aprobada para completar la cobertura mínima; pendiente de aprobación para implementación.
- **Criterios:** AC-HU-011-01 a AC-HU-011-05.

## Tareas técnicas — no son historias de usuario

| ID | Tarea habilitadora | HUs relacionadas |
|---|---|---|
| TT-01 | Definir contratos HTTP, errores y DTO por incremento. | HU-001 a HU-011. |
| TT-02 | Diseñar y versionar persistencia para usuarios, bookmarks y búsquedas guardadas. | HU-001, HU-005 a HU-009. |
| TT-03 | Implementar seguridad de credenciales, JWT, autenticación y aislamiento por propietario. | HU-001, HU-002, HU-005 a HU-011. |
| TT-04 | Construir el puerto/adaptador SECOP, normalización, límites y manejo de fallos. | HU-003, HU-004, HU-009, HU-010, HU-011. |
| TT-05 | Crear shell web, navegación y estados loading/empty/error/success. | HU-001 a HU-011 según cada slice. |
| TT-06 | Añadir pruebas unitarias, integración, contrato y E2E trazadas a los AC. | HU-001 a HU-011. |
| TT-07 | Incorporar entrypoints, Compose completo y ejecución reproducible cuando existan aplicaciones. | Entrega técnica OF-08. |
| TT-08 | Mantener README, SOUL, changelog y evidencia de demo. | Entrega OF-09. |

Estas tareas se planifican dentro del incremento que las necesite; no deben redactarse como «Como / quiero / para» ni competir por valor funcional con las HU.
