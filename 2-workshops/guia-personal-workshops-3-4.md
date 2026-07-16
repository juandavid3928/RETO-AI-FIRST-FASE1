# Mi experiencia: CLAUDE.md + Plan & Loop + MCP + Subagentes
### Guía rápida para el equipo dev — Jikkosoft AI-First
*Diego Trujillo · Etapa 1 · Jueves 25 jun 2026*

---

## El salto de usuario a arquitecto de contexto

Si los primeros dos workshops me enseñaron que el cuello de botella está en el
input, estos dos me mostraron cómo industrializarlo. El CLAUDE.md no es
documentación — es el sistema operativo del agente sobre tu repo. Y `/plan` no
es un atajo — es la diferencia entre generar código y *dirigir* cómo se genera.
Lo que cambia: pasas de pedirle cosas al modelo a definir las reglas bajo las
que opera.

---

## Workshop 3 — CLAUDE.md · Jueves 25 jun, mañana (1–1.5 hrs)

### La diferencia que nadie explica: README vs. AI operating contract

Un README le habla a un humano. Un CLAUDE.md le habla al modelo — y el modelo
lo lee en cada sesión antes de ejecutar cualquier cosa. Son documentos distintos
con audiencias distintas.

`/init` genera el esqueleto. Tu trabajo es convertirlo en un contrato preciso:
qué puede hacer el agente, qué nunca puede tocar, cómo se llaman las cosas en
**este** proyecto específico.

### Anatomía de un CLAUDE.md de producción

En el workshop revisamos en vivo el CLAUDE.md de la API de SILIN (21 KB). Los
componentes que realmente marcan la diferencia:

| Sección | Qué define |
|---|---|
| **Authority hierarchy** | Qué puede ejecutar el agente sin confirmación |
| **Safe/unsafe zones** | Archivos y directorios que el agente nunca modifica |
| **Naming conventions** | Cómo se llaman tablas, columnas, servicios — sin alucinaciones |
| **Model selection table** | Qué modelo usar para cada tipo de tarea (Haiku vs Sonnet vs Opus) |

### El ejercicio que más cambió mi perspectiva

Escribir el CLAUDE.md del repo actual desde cero — sin copiar, sin plantilla.
Forzarte a articular las reglas implícitas del proyecto (las que todos conocen
pero nadie escribió) es el ejercicio más valioso del programa.

Después: revisión cruzada en pares. Ver cómo otro interpreta tu repo con tu
CLAUDE.md revela qué secciones son ambiguas antes de que el modelo las
malinterprete.

### Track DEV vs. Track QA

- **Track DEV:** safe zones para schema, API y FE — el agente construye sin
  tocar lo que no debe.
- **Track QA:** qué no modificar del SUT, cómo describir el alcance de
  cobertura — el agente prueba sin alterar la aplicación.

> **Mi experiencia:** el CLAUDE.md de SILIN que generé con `/init` tenía 4 KB.
> Después del workshop lo expandí a 21 KB agregando las convenciones reales,
> los contratos de las APIs internas y las zonas restringidas. Desde esa versión,
> el modelo no volvió a proponer renombrar columnas ni a ignorar el soft delete.

### Recursos

- **CLAUDE.md reference** — estructura oficial y campos soportados: https://docs.anthropic.com/en/docs/claude-code/claude-md
- **Memory and CLAUDE.md** — cómo Claude Code carga contexto jerárquico: https://docs.anthropic.com/en/docs/claude-code/memory

---

## Workshop 4 — Plan & Loop + MCP + Subagentes + Git · Jueves 25 jun, tarde (1–1.5 hrs)

### /plan: el paso que cambia todo

Antes de generar cualquier línea de código en una tarea compleja:

```bash
/plan   # Claude razona la arquitectura antes de escribir
```

El modelo expone su plan, tú lo corriges si algo está mal, *luego* ejecuta.
El costo de corregir un plan es cero. El costo de corregir código generado con
el enfoque equivocado es alto. Este comando solo elimina la segunda categoría.

### Loop modes para tareas iterativas

```bash
/loop   # ejecuta iteraciones hasta que el criterio se cumpla
```

Útil para tareas con criterio de éxito medible: tests que pasan, score ≥ umbral,
build limpio. El agente itera sin intervención humana en cada ciclo.

### El sistema everything-claude-code: skill correcto para cada tarea

No todos los skills son iguales. La regla: elegir el skill más específico
disponible para la tarea — evita el skill genérico cuando hay uno dedicado.

| Skill | Cuándo usarlo |
|---|---|
| `:tdd-workflow` | Desarrollo guiado por pruebas (RED → GREEN → REFACTOR) |
| `:backend-patterns` | APIs y servicios — patrones de estructura |
| `:security-review` | Revisión de seguridad antes de merge |
| `:database-reviewer` | Schema y queries — constraints, índices, migraciones |

Flujo completo demostrado en vivo: `/init` → `/plan` → build con skills apropiados.

### MCP Servers que realmente cambian el flujo

Los MCP Servers conectan el agente a sistemas externos como fuentes de contexto
nativas — sin copy-paste, sin cambiar de herramienta.

| MCP Server | Qué resuelve |
|---|---|
| **Figma** | Diseño leíble por IA — el agente implementa directamente desde Figma |
| **Azure DevOps WI** | Work Items como PRD — el agente conoce el requerimiento antes de codificar |
| **claude-mem** | Memoria persistente entre sesiones — contexto que sobrevive al `/new` |

### Subagentes paralelos: patrón LLM-as-judge

El patrón más potente del programa: un modelo genera el output, otro lo evalúa.
Elimina el sesgo de autovalidación — el generador no puede aprobar su propio output.

Caso real de `hermes-exploratory` Phase 2:

```
spec → generator (Sonnet) → SQL
                           → judge (Opus) → score 0–100
                                          → gate: precision ≥ 0.85 = merge ✓
                                                  precision < 0.85 = retry
```

El generador nunca ve su propio score hasta que el judge lo aprueba. Esto
es lo que subió el benchmark de 72 pts (Spec A + Opus solo) a 88+ pts con
Spec C + Haiku + judge.

### Git con AI: trazabilidad de sesiones

```bash
# Commit semántico generado por el agente:
git commit -m "feat(orders): add soft delete with deleted_at column"

# ai-dev-log: cada sesión Hermes deja rastro en el log del repo
# PRs generados con contexto completo — sin redactar el cuerpo a mano
```

El objetivo no es que el agente haga commits ciegos — es que cada acción
quede trazada con el contexto de la sesión que la generó.

### Recursos

- **Claude Code subagents** — orquestación y patrones: https://docs.anthropic.com/en/docs/claude-code/sub-agents
- **MCP documentation** — conectar servidores externos: https://docs.anthropic.com/en/docs/claude-code/mcp
- **everything-claude-code skills** — catálogo de skills disponibles: https://github.com/disler/everything-claude-code

---

## TL;DR para el equipo

```
1. CLAUDE.md ≠ README — es el contrato del agente con tu repo, no documentación
2. /init genera el esqueleto; tú lo conviertes en contrato preciso (21 KB, no 4 KB)
3. /plan antes de cualquier tarea compleja — corregir un plan cuesta cero
4. Elige el skill más específico disponible — evita el genérico cuando hay uno dedicado
5. MCP Servers = contexto nativo (Figma, Azure DevOps, memoria persistente)
6. LLM-as-judge: el generador no puede aprobar su propio output
```

---

*Preguntas → Diego Trujillo · diego.trujillo@jikkosoft.com*
