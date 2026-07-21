# Frontend HU-001/HU-002

React 18, TypeScript, Vite y Tailwind CSS 4. `/register` crea cuentas y `/login` inicia/restaura/cierra una sesión JWT con estados accesibles y explícitos.

Pruebas de componente y build:

```bash
npm ci
npm test
npm run build
```

El E2E requiere que el stack Compose esté saludable y una conexión de verificación al mismo PostgreSQL:

```bash
E2E_BASE_URL='http://127.0.0.1:8080' TEST_DATABASE_URL='postgresql://...' npm run test:e2e
```

La confirmación de registro nunca se envía al backend. Login guarda exclusivamente `{ accessToken, expiresAt }` en `localStorage` bajo `portal.auth.session`, limpia sesiones corruptas o expiradas y no registra credenciales ni JWT. Logout es exclusivamente cliente.
