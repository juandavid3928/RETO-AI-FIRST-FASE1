# Árbol frontend vigente

```text
frontend/
├── Dockerfile
├── README.md
├── index.html
├── package.json
├── package-lock.json
├── playwright.config.ts
├── tsconfig.json
├── vite.config.ts
├── nginx.conf
├── .env.example
├── src/
│   ├── main.tsx
│   ├── app/App.tsx
│   ├── auth/authSession.ts
│   ├── pages/{RegisterPage,LoginPage}.tsx
│   ├── services/{register,login}.ts
│   └── styles/index.css
└── tests/
    ├── setup.ts
    ├── {register,login,authSession}.test.tsx
    └── e2e/{register,login}.spec.ts
```

Las rutas productivas son `/register` y `/login`. `auth/authSession.ts` centraliza validación, persistencia, restauración, expiración y limpieza segura bajo `portal.auth.session`; `LoginPage` sincroniza cambios entre pestañas y reevalúa al recuperar visibilidad. Logout continúa siendo cliente. `authenticatedFetch` se difiere hasta la primera capacidad privada autorizada; no existe todavía una pantalla privada de HU-005.
