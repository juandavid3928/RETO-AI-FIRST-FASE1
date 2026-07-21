# Frontend HU-001

React 18, TypeScript, Vite y Tailwind CSS 4. La única ruta funcional es `/register`, con email, password y confirmación accesibles y estados explícitos del flujo.

```bash
npm ci
npm test
npm run build
npm run test:e2e
```

La confirmación nunca se envía al backend. El flujo no usa almacenamiento, analytics ni logging de credenciales.
