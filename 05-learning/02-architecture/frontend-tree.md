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
│   ├── pages/{RegisterPage,LoginPage}.tsx
│   ├── services/{register,login}.ts
│   └── styles/index.css
└── tests/
    ├── setup.ts
    ├── {register,login}.test.tsx
    └── e2e/{register,login}.spec.ts
```

Las rutas productivas son `/register` y `/login`. Login consume `POST /api/v1/auth/login`, conserva únicamente token/expiración bajo `portal.auth.session`, restaura o expira la sesión localmente y realiza logout cliente. No existe todavía una pantalla privada de HU-005.
