# Mi experiencia: Claude Code + Spec Engineering
### Guía rápida para el equipo dev — Jikkosoft AI-First
*Diego Trujillo · Etapa 1 · Miércoles 24 jun 2026*

---

## El cambio de paradigma

Llevaba usando Copilot y ChatGPT como aceleradores de escritura — útiles,
pero esencialmente glorificados snippets con contexto limitado. El cambio real
no fue el modelo: fue entender que el cuello de botella siempre estuvo del lado
del input, no del output. **El modelo no es el protagonista, la spec sí lo es.**
El mejor modelo con una spec mala produce basura. El modelo más barato con una
spec bien escrita produce output de producción. Eso lo confirma el experimento
interno `hermes-exploratory`.

---

## Workshop 1 — Claude Code + Hermes

### Las herramientas

| Herramienta | Rol |
|---|---|
| **Claude Code** (Anthropic) | Agente de código en terminal — ejecuta, edita, crea archivos, razona sobre el código |
| **Hermes** (NousResearch) | Capa de orquestación: selecciona el modelo y administra el contexto |

**Regla del programa:** toda interacción con LLMs pasa por Hermes. Claude Code
es el ejecutor — Hermes elige el modelo correcto para cada tarea.

### Instalación en 2 pasos

```bash
# 1. Claude Code
# Descargar desde https://claude.ai/code o seguir la guía oficial
claude --version   # verifica instalación

# 2. Hermes
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes doctor      # verifica conexión a proveedores
hermes setup       # conecta Anthropic / DeepSeek / Moonshot
```

### Conectar Hermes al modelo

**Paso 1 — configurar API keys (primera vez)**

```bash
# Opción A — env vars en ~/.zshrc (persistente, recomendado)
export ANTHROPIC_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="..."
source ~/.zshrc

# Opción B — hermes setup (interactivo, guarda internamente)
hermes setup

hermes doctor          # confirma qué proveedores están activos
hermes config list     # muestra claves configuradas (valores enmascarados)
```

**Paso 2 — elegir el modelo activo**

```bash
hermes model                             # picker interactivo — muestra todos los disponibles
/model anthropic:claude-sonnet-4-6      # dentro de una sesión Hermes
/model anthropic:claude-haiku-4-5       # más barato, tareas rutinarias
/model deepseek:deepseek-coder          # alternativa para código
```

**Cambio de modelo mid-sesión sin perder contexto:**

```bash
/model anthropic:claude-opus-4-8        # tarea de razonamiento pesado
/model anthropic:claude-haiku-4-5       # generación masiva de código (3× más barato)
/model anthropic:claude-sonnet-4-6      # volver al punto de equilibrio
```

> Hermes es el orquestador — gestiona contexto y enruta tareas.
> El modelo que configuras es el implementador. Puedes cambiar el implementador
> sin reiniciar la sesión ni perder el historial.

### El ritual /init — por qué importa

```bash
# En cualquier repo vacío o existente:
claude /init
```

Genera el `CLAUDE.md` base: el **contrato AI del proyecto**. Sin este archivo,
el modelo trabaja sin contexto y alucina convenciones, nombres de columnas,
rutas. Con él, cualquier modelo (incluso Haiku) respeta las reglas del proyecto.

Lo que genera `/init`:
- Authority hierarchy (qué puede y qué no puede hacer la IA)
- Naming conventions del proyecto
- Safe/unsafe zones (qué archivos nunca tocar)
- Stack y arquitectura

> **Mi experiencia:** la primera vez que lo corrí en el repo de SILIN generó un
> CLAUDE.md de 4 KB que luego expandí a 21 KB. Desde entonces el modelo no volvió
> a inventar nombres de tablas.

### Navegación básica en el TUI de Hermes

```
hermes model          # selector visual de modelo
/model anthropic:claude-sonnet-4-6   # cambiar modelo sin salir
/new                  # conversación fresca — evita memory bleed entre tareas
hermes config list    # ver todas las claves de configuración aceptadas
```

**Modo interactivo vs. autónomo:**
- Interactivo (`hermes`): el agente pide confirmación antes de ejecutar
- Autónomo (`hermes --auto`): ejecuta sin confirmar — usar solo en ramas desechables

### Videos y recursos

- **800+ horas de Claude Code en 8 minutos** — resumen condensado, ideal para devs: https://www.youtube.com/watch?v=Ffh9OeJ7yxw
- **Claude Code Tutorial playlist** — workflow completo, CLAUDE.md, MCP, subagentes: https://www.youtube.com/playlist?list=PL4cUxeGkcC9g4YJeBqChhFJwKQ9TRiivY
- **Claude Code docs** — quickstart oficial: https://code.claude.com/docs/en/overview
- **Claude Code slash commands** — referencia completa de comandos: https://docs.anthropic.com/en/docs/claude-code/slash-commands
- **Repositorio Hermes**: https://github.com/NousResearch/hermes-agent

---

## Workshop 2 — Spec Engineering

### El hallazgo que lo cambia todo

Del experimento interno [`hermes-exploratory`](https://github.com/diegotrujillo-jikko/hermes-exploratory):

```
Spec A (~150 palabras) + Opus 4.8   → 72 pts
Spec C (~480 palabras) + Haiku 4.5  → 88 pts
```

**Conclusión:** mejorar la spec es 3× más barato y efectivo que subir de modelo.
El punto de equilibrio costo/calidad: **Spec B + Sonnet**.

### Cómo escribir tus propios specs

**Herramienta: Hermes** — describes tu dominio, Hermes genera las 3 versiones.
Usar la IA para escribir la spec que luego evalúa la IA es exactamente el punto del workshop.

En Hermes, con este prompt:

```
Tengo un sistema de [describe tu dominio en 2-3 oraciones: qué hace, qué entidades
maneja, qué stack usa].

Genera 3 versiones de spec para el mismo schema PostgreSQL:
- Spec A (~150 palabras): solo overview + tech stack
- Spec B (~480 palabras): agrega convenciones de naming, tipos de datos exactos,
  reglas de integridad (soft delete, FKs, constraints), fuera de scope
- Spec C (~900 palabras): Spec B + ejemplos de queries que deben funcionar + casos de borde

Formato: un bloque markdown por spec, sin SQL, solo la descripción.
```

Guardar cada respuesta como `phase-1/01-specs/spec_a.md`, `spec_b.md`, `spec_c.md`
(reemplazar con paths de tu repo) y correr el ejercicio con tu dominio real.

> El "aha moment" ocurre en el paso Spec A → Spec B: el modelo deja de alucinar
> nombres de tablas y constraints porque ya los describiste explícitamente.

### Cómo reproducir el ejercicio (sin W&B)

W&B es solo visualización — el ejercicio funciona sin él. Solo necesitas Hermes + `ANTHROPIC_API_KEY`.

```bash
# 1. Clonar
git clone https://github.com/diegotrujillo-jikko/hermes-exploratory
cd hermes-exploratory

# 2. Secrets (solo Anthropic, omitir WANDB_API_KEY)
cp .env.example .env
# editar .env: llenar solo ANTHROPIC_API_KEY

# 3. Python deps (sin wandb)
python3 -m venv .venv && source .venv/bin/activate
pip install python-dotenv
```

Para cada spec (`a`, `b`, `c`), el flujo es:

**1. Abrir Hermes y seleccionar modelo**
```bash
hermes
/model anthropic:claude-sonnet-4-6
/new
```

**2. Pegar el contenido de la spec + el prompt**

En el TUI, pegar el contenido de `phase-1/01-specs/spec_a.md` seguido de:
```
Generate the PostgreSQL schema. Output only SQL — no prose, no fences.
```

**3. Copiar la respuesta y guardarla como archivo**

El modelo responde con SQL puro en el TUI. Copiarlo y pegarlo en un archivo nuevo:
```
phase-1/02-outputs/r1_sonnet_a.sql
```

Repetir para `spec_b.md` → `r1_sonnet_b.sql` y `spec_c.md` → `r1_sonnet_c.sql`.

Registrar sin subir a W&B:

```bash
python phase-1/scripts/log_run.py \
  --round 1 --model sonnet-4-6 --spec a \
  --output phase-1/02-outputs/r1_sonnet_a.sql \
  --no-wandb
```

Resultados en `phase-1/03-analysis/runs.jsonl`. Repetir para specs `b` y `c`, luego
con Haiku y Opus para ver la matriz completa. Análisis final en
`phase-1/03-analysis/ANALYSIS.md`.

### Los 3 niveles de spec

| Nivel | Tamaño aprox. | Resultado típico |
|---|---|---|
| **Spec A** — básica | < 150 palabras | Modelo alucina tablas, ignora constraints |
| **Spec B** — equilibrio | 300–500 palabras | Punto de equilibrio costo/calidad ✓ |
| **Spec C** — detallada | 500+ palabras | Máxima calidad, mejor con tareas complejas |

### Checklist de una Spec B efectiva

Cada spec debe cubrir estos 8 puntos:

1. **Dominio** — qué representa en 2–3 oraciones
2. **Scope** — lista de entidades/tablas con columnas clave
3. **Tech stack** — versión de DB, IDs, formato de timestamps
4. **Convenciones** — naming, columnas de estado, tipo de moneda (ej: centavos)
5. **Reglas de integridad** — soft delete, ON DELETE, UNIQUE, CHECK constraints
6. **Reglas de safe-change** — columnas nullable, sin renombrados, índices en FKs
7. **Fuera de scope** — qué NO generar (evita tablas alucinadas)
8. **Entregable esperado** — formato exacto (solo SQL, sin prosa, sin fences)

### El ejercicio práctico que más me sirvió

Tomar cualquier feature del trabajo real y escribir 3 versiones:

```
Spec A: "Crea una tabla de órdenes con sus productos y precios."
          → el modelo inventa nombres, olvida FKs, ignora soft delete

Spec B: "Tabla `orders` con `id UUID PK`, `status VARCHAR CHECK(...)`,
          `created_at TIMESTAMPTZ DEFAULT NOW()`, FK a `customers(id)`.
          Soft delete: columna `deleted_at`. Montos en centavos (INTEGER).
          Fuera de scope: pagos, envíos."
          → output limpio, constraints correctos

Spec C: Spec B + ejemplos de queries que deben funcionar + casos de borde
          → output de producción directamente usable
```

Comparar los tres outputs. El ejercicio dura 20 minutos y convence mejor
que cualquier presentación.

### Regla práctica

> **score < 80 → la spec necesita más detalle, no un modelo más caro.**

Si el output no es lo que esperabas, antes de cambiar de modelo: agrega
el punto del checklist que falta. Casi siempre es el 4, 5 o 7.

### Recursos

- **Prompt engineering guide** (Anthropic): https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview
- **Tutorial interactivo** (Jupyter notebooks): https://github.com/anthropics/prompt-eng-interactive-tutorial
- **Experimento interno con datos reales**: https://github.com/diegotrujillo-jikko/hermes-exploratory

---

## TL;DR para el equipo

```
1. Instala: Claude Code + Hermes
2. Configura API keys en ~/.zshrc → export ANTHROPIC_API_KEY="sk-ant-..."
3. hermes setup  →  hermes doctor  →  verde en todos los proveedores
4. hermes model  →  elige el modelo implementador (Sonnet para balance, Haiku para volumen)
5. En cada repo nuevo: claude /init  →  expande el CLAUDE.md generado
6. Antes de pedir cualquier cosa al modelo: escribe la spec (mínimo Spec B)
7. Si el output es malo: mejora la spec, no cambies el modelo
8. Usa Hermes como entrada única — cambia de modelo mid-sesión sin perder contexto
9. Para validar spec depth: clonar hermes-exploratory → pip install python-dotenv →
   correr el ejercicio con --no-wandb → comparar runs.jsonl
```

---

*Preguntas → Diego Trujillo · diego.trujillo@jikkosoft.com*
