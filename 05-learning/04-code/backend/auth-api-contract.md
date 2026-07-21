# Auth API contract

Estado: HU-001 implementada y validada; pendiente de revisión y merge. HU-002 y cualquier otra capacidad de autenticación permanecen pendientes.

## HU-001 — `POST /api/v1/auth/register`

### Solicitud

`Content-Type: application/json`, con un límite de cuerpo de 4 KiB y exactamente:

```json
{
  "email": " visitor@example.com ",
  "password": "a password of at least 12 characters"
}
```

- Se rechazan campos desconocidos.
- `email` es obligatorio, se recortan espacios exteriores, se valida su sintaxis y se persiste en forma canónica minúscula. La identidad y unicidad son insensibles a mayúsculas y a espacios exteriores.
- `password` es obligatorio y debe tener entre 12 y 128 caracteres Unicode, sin reglas de composición.
- La confirmación de contraseña existe solo en el frontend y nunca se envía a la API.

### Respuesta exitosa — `201 Created`

```json
{
  "id": "b7d3a91e-78d1-4ad4-b8f5-c20a70ebfa75",
  "email": "visitor@example.com",
  "created_at": "2026-07-21T15:00:00Z"
}
```

`id` es UUID4. `created_at` es UTC. La respuesta no contiene JWT, contraseña ni hash.

El modelo persistido también conserva `updated_at` como `TIMESTAMPTZ NOT NULL`, inicialmente igual a `created_at`; este campo no se expone en la respuesta de registro.

### Errores estables

Todos los errores usan este sobre y no incluyen contraseña ni hash:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Registration data is invalid.",
    "fields": {"email": ["Enter a valid email address."]}
  }
}
```

| HTTP | `code` | Uso |
|---|---|---|
| 422 | `validation_error` | JSON, campos, email o password inválidos; `fields` identifica los campos cuando aplica. |
| 409 | `email_already_registered` | La restricción única exacta de PostgreSQL detecta la identidad canónica duplicada. |
| 503 | `database_unavailable` | PostgreSQL no está disponible. |
| 500 | `internal_error` | Fallo inesperado, sin detalles internos. |

La restricción única de base de datos es la autoridad ante concurrencia. El adaptador traduce a 409 únicamente la violación de la restricción `uq_users_email_canonical` y ejecuta rollback antes de devolver el control. Otras violaciones o fallos son inesperados.

## Fuera de HU-001

Login, JWT, roles, verificación, recuperación, perfil editable y cualquier otra ruta de autenticación no forman parte de este contrato.
