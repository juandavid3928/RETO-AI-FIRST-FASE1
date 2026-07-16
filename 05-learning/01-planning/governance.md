# Governance

## Autoridad

- El usuario aprueba alcance, decisiones técnicas y acciones Git.
- Hermes inspecciona, propone, ejecuta lo aprobado y verifica resultados.
- Una recomendación no se convierte en decisión hasta aprobación explícita.

## Gates

1. Comprensión y clasificación.
2. Propuesta.
3. Aprobación explícita.
4. Ejecución mínima.
5. Verificación real.
6. Evidencia.

## Git

Flujo obligatorio para todo cambio:

```text
rama de trabajo → cambios → validaciones → commit → push de la rama → PR hacia main → revisión → merge mediante GitHub
```

- No crear commits, ejecutar push, abrir PR ni hacer merge sin autorización explícita para esa acción.
- Después del bootstrap inicial queda prohibido hacer push directo a `main`.
- No integrar una rama localmente ni publicar una integración directa en `main`.
- El merge requiere un PR previamente abierto, revisión y ejecución mediante GitHub.
- No usar force push salvo autorización excepcional, explícita y limitada a una reconstrucción controlada.

## Evidencia

No atribuir al proceso actual código, pruebas, commits o decisiones heredadas.
