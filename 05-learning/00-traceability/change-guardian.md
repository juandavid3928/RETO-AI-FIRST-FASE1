# Change guardian

## Propósito

Evitar cambios aislados y mantener coherencia entre requisitos, arquitectura, DB, backend, frontend, pruebas y documentación.

## Flujo obligatorio

1. Identificar alcance aprobado e historia de usuario.
2. Identificar capas afectadas.
3. Revisar impactos aguas arriba y abajo.
4. Ejecutar validación pertinente.
5. Registrar hechos en `change-log.md`.
6. Resumir en `SOUL.md` solo si aporta evidencia o una decisión relevante.

## Mapa de propagación

- DB → repositorios, contratos, tipos, pruebas y documentación.
- Backend → contrato API, frontend, persistencia, pruebas y documentación.
- Frontend → supuestos de API, estados visuales y documentación.
- Integración externa → adaptador, normalización, errores, UI y pruebas.

## Checklist

- [ ] Alcance aprobado.
- [ ] Sin secretos.
- [ ] Capas afectadas revisadas.
- [ ] Validación ejecutada y observada.
- [ ] Change-log actualizado.
- [ ] SOUL actualizado solo con evidencia real.
