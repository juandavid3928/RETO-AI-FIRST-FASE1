# Frontend HU-001/HU-002/HU-005

React 18, TypeScript, Vite y Tailwind CSS 4. `/register` crea cuentas, `/login` inicia una sesión JWT y `/profile` consulta el perfil propio como primera ruta privada.

Pruebas de componente y build:

```bash
npm ci
npm test
npm run build
```

El E2E requiere que el stack Compose esté saludable y el mismo secreto JWT efímero usado por el backend:

```bash
E2E_BASE_URL='http://127.0.0.1:8080' JWT_SECRET='<base64url-32-byte-minimum>' npm run test:e2e
```

La confirmación de registro nunca se envía al backend. Login acepta únicamente el contrato `access_token` JWT, `token_type: "bearer"` y `expires_in: 1800`, persiste la sesión mínima y navega con `replace` a `/profile`. `AuthSessionProvider` conserva exclusivamente `{ accessToken, expiresAt }` bajo `portal.auth.session`, elimina sesiones corruptas o expiradas, sincroniza `storage`, reevalúa visibilidad y administra un único temporizador. Logout es exclusivamente cliente.

`authenticatedFetch` solo acepta rutas relativas `/api/`, inyecta el Bearer central sin permitir override, no navega y limpia sesión ante cualquier `401`. `RequireAuth` protege `/profile` como UX, mientras el backend conserva la autoridad. El perfil exacto `id`, `email`, `created_at` vive únicamente en memoria y no se registran credenciales, JWT ni datos personales.
