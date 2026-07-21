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
│   ├── pages/RegisterPage.tsx
│   ├── services/register.ts
│   └── styles/index.css
└── tests/
    ├── setup.ts
    ├── register.test.tsx
    └── e2e/register.spec.ts
```

La única ruta productiva es `/register`. El formulario no implementa `/login`, no persiste credenciales y consume exclusivamente `POST /api/v1/auth/register` a través del backend propio.
