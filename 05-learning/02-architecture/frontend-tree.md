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
│   ├── auth/{AuthSessionProvider,RequireAuth}.tsx
│   ├── pages/{RegisterPage,LoginPage,ProfilePage}.tsx
│   ├── services/{register,login,authenticatedFetch,profile}.ts
│   └── styles/index.css
└── tests/
    ├── setup.ts
    ├── {register,login,profile,authenticatedFetch}.test.tsx
    ├── authSession.test.ts
    └── e2e/{register,login,profile}.spec.ts
```

Las rutas productivas son `/register`, `/login` y `/profile`. `AuthSessionProvider` centraliza restauración, expiración, sincronización multitab, visibilidad y logout sobre la sesión mínima de `authSession.ts`; `RequireAuth` es únicamente un guard de UX. `authenticatedFetch` restringe destinos a rutas relativas `/api/`, inyecta el Bearer no sobrescribible desde el provider, clasifica errores y limpia la sesión ante `401` sin navegar. `ProfilePage` mantiene en memoria únicamente `id`, `email` y `created_at`, valida el payload exacto y diferencia loading, success, unauthorized, network, server y storage error.
