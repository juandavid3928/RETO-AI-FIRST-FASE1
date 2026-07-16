# Criterios de aceptación iniciales

Estado: borrador para aprobación antes de implementar.

## HU-001

- Email válido y único.
- Contraseña nunca se devuelve ni persiste en texto plano.
- Respuestas de éxito y conflicto tienen contrato definido.

## HU-002

- Credenciales válidas entregan un JWT verificable.
- Credenciales inválidas no revelan si el usuario existe.
- Rutas privadas rechazan tokens ausentes o inválidos.

## HU-003

- El frontend no consume SECOP directamente.
- Backend normaliza una respuesta externa a un DTO estable.
- Timeout, HTTP error, payload inválido y respuesta vacía se manejan explícitamente.

## Definition of Done

Código, pruebas y evidencia real; impacto revisado; sin secretos; change-log y SOUL actualizados cuando corresponda.
