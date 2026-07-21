# Frontend HU-001

React 18, TypeScript, Vite y Tailwind CSS 4. La única ruta funcional es `/register`, con email, password y confirmación accesibles y estados explícitos del flujo.

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

La confirmación nunca se envía al backend. El flujo no usa almacenamiento, analytics ni logging de credenciales.
