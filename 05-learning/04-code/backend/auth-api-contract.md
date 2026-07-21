# Auth API contract

Estado: HU-001 fusionada. HU-002 implementada y validada localmente en `feat/hu-002-user-login`, pendiente de publicación y revisión mediante PR.

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

## HU-002 — `POST /api/v1/auth/login`

### Solicitud

`Content-Type: application/json`, con límite real de cuerpo de 4 KiB y exactamente:

```json
{
  "email": " visitor@example.com ",
  "password": "opaque password"
}
```

- Se prohíben campos adicionales.
- El email se recorta exteriormente, valida y canoniza igual que en HU-001.
- La contraseña se trata como dato opaco, sin `trim`, con longitud de transporte de 1 a 128 caracteres. No se reaplica el mínimo de creación de HU-001.

### Respuesta exitosa — `200 OK`

```json
{
  "access_token": "<JWT>",
  "token_type": "bearer",
  "expires_in": 1800
}
```

Toda respuesta de login incluye `Cache-Control: no-store` y `Pragma: no-cache`.

### JWT

- Firma HS256; el verificador acepta exclusivamente ese algoritmo.
- Claims obligatorios y tipados: `sub` (UUID4 del usuario), `iss`, `aud`, `iat` y `exp`.
- `iss`: `portal-convocatorias-api`.
- `aud`: `portal-convocatorias-web`.
- TTL: 1800 segundos; tolerancia de validación: 30 segundos.
- Sin email, roles, perfil ni `jti`.
- `JWT_SECRET` es obligatorio al arrancar, debe ser base64url válido y decodificar al menos 32 bytes. No tiene valor predeterminado.
- La rotación del secreto invalida todos los tokens. Rotación con `kid` queda fuera de HU-002.

### Errores estables

| HTTP | `code` | Uso |
|---|---|---|
| 422 | `validation_error` | JSON, estructura, email o password inválidos. |
| 401 | `invalid_credentials` | Respuesta idéntica para email inexistente y contraseña incorrecta. |
| 503 | `database_unavailable` | PostgreSQL no está disponible. |
| 500 | `internal_error` | Fallo inesperado, sin detalles internos. |

El lookup usa email canónico y SQL parametrizado. Un usuario inexistente ejecuta una verificación Argon2id contra un hash dummy generado con los mismos parámetros recomendados; no se registran email, password, hash, JWT ni resultados sensibles.

### Contrato Bearer para futuros recursos protegidos

La dependencia productiva usa `HTTPBearer(auto_error=False)` y valida el JWT contra el contrato anterior:

- token ausente: `401 authentication_required`;
- token inválido o expirado: `401 invalid_token`;
- ambos incluyen `WWW-Authenticate: Bearer`.

HU-002 no agrega una ruta privada productiva. La dependencia se ejercita mediante una ruta creada únicamente dentro de tests; el primer recurso privado pertenece a HU-005.

### Sesión frontend

- `/login` permanece como destino después del éxito y muestra el estado autenticado.
- El cliente acepta la respuesta `200` solo si contiene exactamente un JWT estructural, `token_type: "bearer"` y `expires_in: 1800`; cualquier contrato malformado limpia la sesión y produce un error genérico.
- `localStorage` usa la clave `portal.auth.session` y guarda exclusivamente `{ "accessToken": "<JWT>", "expiresAt": 0 }`, donde `expiresAt` es epoch en milisegundos.
- La sesión válida se restaura al recargar y se sincroniza entre pestañas mediante `storage`; una sesión corrupta o expirada se elimina. Al recuperar visibilidad se reevalúa la expiración.
- Logout es exclusivamente cliente: elimina almacenamiento, estado y temporizador. No revoca un token robado, que sigue válido hasta `exp`.
- El riesgo XSS residual de `localStorage` se reduce mediante CSP estricta, ausencia de scripts de terceros y prohibición de registrar o incluir tokens en URLs.
- `authenticatedFetch` no está implementado; se añadirá con la primera capacidad privada autorizada.

## Fuera de HU-002

HU-005 y sus recursos privados, refresh tokens, cookies, sesiones server-side, roles, permisos, MFA, login social, recuperación de contraseña, revocación, `kid` y rate limiting quedan fuera. Rate limiting se mantiene como hardening pendiente antes de producción.
