"""Generate 1-programa-ai-first-fase1.pdf using ReportLab + DejaVu Sans."""
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,
    Spacer, Table, TableStyle,
)

FONT_DIR = "/Users/dorothy/Library/Fonts"
pdfmetrics.registerFont(TTFont("DejaVu", f"{FONT_DIR}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", f"{FONT_DIR}/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Italic", f"{FONT_DIR}/DejaVuSans-Oblique.ttf"))

TEAL = colors.HexColor("#006A71")
TEAL_LIGHT = colors.HexColor("#E0F2F3")
TEAL_MID = colors.HexColor("#B2DFDB")
WHITE = colors.white
GREY_ROW = colors.HexColor("#EEEEEE")

def styles():
    base = dict(fontName="DejaVu", fontSize=9.5, leading=16, alignment=TA_JUSTIFY,
                spaceAfter=6)
    return {
        "title": ParagraphStyle("title", fontName="DejaVu-Bold", fontSize=22,
                                textColor=TEAL, alignment=TA_CENTER, spaceAfter=14),
        "subtitle": ParagraphStyle("subtitle", fontName="DejaVu", fontSize=11,
                                   textColor=colors.HexColor("#444444"),
                                   alignment=TA_CENTER, spaceAfter=6),
        # h1 inner: white bold text inside the teal Table cell
        "h1": ParagraphStyle("h1", fontName="DejaVu-Bold", fontSize=14,
                              textColor=WHITE, alignment=TA_LEFT, leading=20),
        "h2": ParagraphStyle("h2", fontName="DejaVu-Bold", fontSize=11,
                              textColor=TEAL, spaceBefore=16, spaceAfter=6),
        "h3": ParagraphStyle("h3", fontName="DejaVu-Bold", fontSize=9.5,
                              textColor=colors.HexColor("#333333"),
                              spaceBefore=12, spaceAfter=5),
        "body": ParagraphStyle("body", **base),
        "bullet": ParagraphStyle("bullet", **{**base, "leftIndent": 14,
                                              "bulletIndent": 4, "spaceAfter": 5}),
        "note": ParagraphStyle("note", fontName="DejaVu-Italic", fontSize=8.5,
                               textColor=colors.HexColor("#555555"),
                               alignment=TA_JUSTIFY, spaceAfter=6, leading=13),
        "box": ParagraphStyle("box", fontName="DejaVu", fontSize=9.5,
                              backColor=TEAL_LIGHT, borderColor=TEAL, borderWidth=1,
                              borderPad=10, leading=16, alignment=TA_JUSTIFY,
                              spaceAfter=10),
        "roi_box": ParagraphStyle("roi_box", fontName="DejaVu-Italic", fontSize=9,
                                  backColor=colors.HexColor("#FFF8E1"),
                                  borderColor=colors.HexColor("#F9A825"),
                                  borderWidth=1, borderPad=8,
                                  leading=15, alignment=TA_JUSTIFY, spaceAfter=8),
        "code": ParagraphStyle("code", fontName="DejaVu", fontSize=8.5,
                               textColor=colors.HexColor("#1A237E"),
                               backColor=colors.HexColor("#F5F5F5"),
                               borderColor=colors.HexColor("#BDBDBD"),
                               borderWidth=0.5, borderPad=6,
                               leading=14, spaceAfter=4, alignment=TA_LEFT),
    }

LLM_NOTE = ("Hermes como agente principal y uno o varios LLMs de su preferencia "
            "para codificar o implementar (ej: Claude Sonnet, Haiku, Opus, Codex, "
            "DeepSeek, Kimi K2, etc.)")

def tbl_style(header_bg=TEAL, alt=GREY_ROW):
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "DejaVu-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("FONTNAME", (0, 1), (-1, -1), "DejaVu"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, alt]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BBBBBB")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ])

def build():
    S = styles()
    W = A4[0] - 4 * cm

    def h1(text):
        t = Table([[Paragraph(text, S["h1"])]], colWidths=[W])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), TEAL),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ]))
        return t
    def h2(text): return Paragraph(text, S["h2"])
    def h3(text): return Paragraph(text, S["h3"])
    def p(text):  return Paragraph(text, S["body"])
    def b(text):  return Paragraph(f"• {text}", S["bullet"])
    def note(text): return Paragraph(text, S["note"])
    def roi(text):  return Paragraph(text, S["roi_box"])
    def sp(h=0.4): return Spacer(1, h * cm)
    def hr(): return HRFlowable(width="100%", thickness=0.5,
                                color=colors.HexColor("#CCCCCC"), spaceAfter=4)

    story = []

    # ── Title block ──────────────────────────────────────────────────────────
    story += [
        sp(2.5),
        Paragraph("Programa AI-First · Fase 1", S["title"]),
        sp(0.5),
        Paragraph("Jikkosoft — Preparación y Reto", S["subtitle"]),
        sp(0.2),
        Paragraph("Preparado por Diego Trujillo · diego.trujillo@jikkosoft.com", S["subtitle"]),
        sp(1.2),
        hr(),
        sp(1.0),
    ]

    # ── Aspectos importantes ─────────────────────────────────────────────────
    story += [
        h1("Aspectos importantes"),
        sp(0.3),
        roi("<b>Por qué Hermes,</b> "
            "Jikkosoft pasa de escribir código a orquestar contexto. "
            "La investigación interna (<i>hermes-exploratory</i>, 2026) lo confirma con datos: "
            "mejorar la spec es <b>3× más efectivo que actualizar el modelo</b> — "
            "pasar de Spec A (~150 palabras) a Spec B (~480 palabras) produce +26 puntos "
            "promedio en calidad de output; subir de Haiku a Opus en la misma spec produce "
            "solo +12 a +24. Una spec mal escrita hace que el modelo más costoso alucine "
            "convenciones e ignore reglas de integridad. Una spec bien escrita hace que el "
            "modelo más barato produzca output de producción. Hermes es el canal obligatorio "
            "que hace este proceso repetible, trazable y transferible."),
        sp(0.3),
        h2("Requisitos mínimos"),
        sp(0.2),
    ]
    _rh = ParagraphStyle("_rh", fontName="DejaVu-Bold", fontSize=9,
                         textColor=WHITE, leading=13)
    _rb = ParagraphStyle("_rb", fontName="DejaVu", fontSize=8.5, leading=14)
    def _rc(t, hdr=False): return Paragraph(t, _rh if hdr else _rb)
    def _rl(label, url):
        return Paragraph(
            f'<a href="{url}" color="#0066CC"><u>{label}</u></a>', _rb
        )
    tbl_req = Table(
        [
            [_rc("Herramienta", hdr=True), _rc("Instalación / Acceso", hdr=True)],
            [_rc("Codex CLI"),
             _rl("Instalar desde github.com/openai/codex",
                 "https://github.com/openai/codex")],
            [_rc("Claude Code (Claude CLI)"),
             _rl("claude.ai/code — descarga el instalador o sigue la guía de la plataforma",
                 "https://claude.ai/code")],
            [_rc("Hermes agent (NousResearch)"),
             _rl("github.com/NousResearch/hermes-agent — install.sh | bash"
                 " · verificar: hermes --help && hermes doctor",
                 "https://github.com/NousResearch/hermes-agent")],
            [_rc("Git"),
             _rl("git-scm.com · macOS/Linux: preinstalado · Windows: descargar instalador",
                 "https://git-scm.com")],
            [_rc("API key LLM"),
             _rc("Contactar a Juan David para obtener acceso a una API")],
            [_rc("Cuenta GitHub o GitLab"),
             Paragraph(
                 '<a href="https://github.com" color="#0066CC"><u>github.com</u></a>'
                 ' o '
                 '<a href="https://gitlab.com" color="#0066CC"><u>gitlab.com</u></a>'
                 ' — repo público donde alojar la entrega del reto', _rb
             )],
        ],
        colWidths=[4.5 * cm, W - 4.5 * cm],
    )
    tbl_req.setStyle(tbl_style(header_bg=colors.HexColor("#00838F"), alt=TEAL_LIGHT))
    story += [tbl_req, sp(0.7)]

    # ── Principio fundacional ────────────────────────────────────────────────
    story += [KeepTogether([
        h1("Principio fundacional"),
        sp(0.5),
        Paragraph(
            "Todo proyecto AI empieza con <b>/init</b>. "
            "Antes de escribir una sola spec, antes de tocar código, antes de todo: "
            "ejecuta <b>claude /init</b> en el repositorio. Esto genera el CLAUDE.md "
            "base y establece el contrato AI del proyecto. Sin este paso, la IA "
            "trabaja sin contexto y los resultados son impredecibles.",
            S["box"],
        ),
        sp(0.5),
    ])]

    # ── Estructura general ───────────────────────────────────────────────────
    story += [h1("Estructura general"), sp(0.4)]
    _sh = ParagraphStyle("_sh", fontName="DejaVu-Bold", fontSize=9,
                         textColor=WHITE, leading=13)
    _sb = ParagraphStyle("_sb", fontName="DejaVu", fontSize=9, leading=14)
    COL_E = 4 * cm; COL_F = 3 * cm; COL_D = W - COL_E - COL_F
    tbl_struct = Table(
        [
            [Paragraph("Etapa", _sh), Paragraph("Descripción", _sh),
             Paragraph("Fechas", _sh)],
            [Paragraph("1 — Capacitación", _sb),
             Paragraph("Claude CLI · Spec Engineering · CLAUDE.md · "
                       "Plan &amp; Loop · MCP Servers · Subagentes · Git", _sb),
             Paragraph("24–25 jun", _sb)],
            [Paragraph("2 — Adaptabilidad", _sb),
             Paragraph("Construcción y entrega del proyecto "
                       "(Reto Fase 1: DEV + QA en paralelo)", _sb),
             Paragraph("26 jun – 6 jul", _sb)],
            [Paragraph("3 — Adaptabilidad con lo actual", _sb),
             Paragraph("Integración del workflow AI-first con proyectos "
                       "y contexto existente", _sb),
             Paragraph("hasta 7 jul", _sb)],
        ],
        colWidths=[COL_E, COL_D, COL_F],
    )
    tbl_struct.setStyle(tbl_style())
    story += [tbl_struct, sp(0.2),
              note("Evaluación: martes 7 de julio · demo de 5–7 min por track."),
              sp(0.5)]

    # ── Etapa 1 ──────────────────────────────────────────────────────────────
    story += [h1("Etapa 1 — Capacitación · 24–25 jun"), sp(0.2),
              h2("Workshop 1 — Apertura + Codex CLI · Miércoles 24 jun (1–1.5 hrs)"),
              b("Apertura del programa: contexto del “momento cero” y el nuevo modelo operativo AI-first."),
              b("Instalación: Claude Code (claude.ai/code) + Hermes (curl install → hermes setup)."),
              b("Verificación: <i>claude --version</i> · <i>hermes doctor</i> — ambos deben responder antes de continuar."),
              b("El ritual /init en vivo sobre un repo vacío: qué genera, por qué importa."),
              b("Navegación básica: slash commands, permisos, modo interactivo vs. autónomo."),
              b(f"Hermes como intermediario obligatorio: toda interacción con modelos pasa por aquí. "
                f"Libertad de elegir uno o varios LLMs para codificar o implementar "
                f"(ej: Claude Sonnet, Haiku, Opus, Codex, DeepSeek, Kimi K2, etc.)."),
              sp(0.2)]

    tc_hdr_w1 = ParagraphStyle("tc_hdr_w1", fontName="DejaVu-Bold", fontSize=8.5,
                                textColor=WHITE, leading=13)
    tc_body_w1 = ParagraphStyle("tc_body_w1", fontName="DejaVu", fontSize=8.5,
                                 leading=13, alignment=TA_LEFT)
    def tcw(t, hdr=False):
        return Paragraph(t, tc_hdr_w1 if hdr else tc_body_w1)
    tbl_hermes = Table(
        [
            [tcw("Comando", hdr=True), tcw("Uso", hdr=True)],
            [tcw("hermes setup"), tcw("Configuración inicial — conecta proveedores (Anthropic, DeepSeek, Moonshot)")],
            [tcw("hermes doctor"), tcw("Diagnóstico de instalación y conectividad")],
            [tcw("hermes model"), tcw("Selector interactivo de modelo (muestra todos los disponibles)")],
            [tcw("/model anthropic:claude-sonnet-4-6"), tcw("Cambia el modelo activo dentro del TUI")],
            [tcw("/new"), tcw("Abre conversación fresca — evita memory bleed entre tareas")],
            [tcw("hermes config list"), tcw("Lista las claves de config aceptadas por la versión instalada")],
        ],
        colWidths=[5.5 * cm, W - 5.5 * cm],
    )
    tbl_hermes.setStyle(tbl_style(header_bg=colors.HexColor("#00838F"), alt=TEAL_LIGHT))
    story += [KeepTogether([h3("Referencia de comandos Hermes:"), sp(0.1), tbl_hermes]), sp(0.3),
              h2("Workshop 2 — Spec Engineering · Miércoles 24 jun, tarde (1–1.5 hrs)"),
              b("Por qué la calidad de la spec supera la elección del modelo."),
              b("La matriz real: 3 niveles de spec × 7 modelos — caso de estudio extraído del "
                "experimento interno de Diego (<i>hermes-exploratory</i>)."),
              b("Hallazgo clave: Haiku + Spec C (88 pts) &gt; Opus + Spec A (72 pts). "
                "Spec B + Sonnet es el punto de equilibrio costo/calidad."),
              b("Ejercicio práctico: cada participante escribe 3 versiones de spec para algo de "
                "su contexto y compara outputs."),
              sp(0.2),
              h3("Checklist de una spec efectiva (nivel Spec B — punto de equilibrio):")]
    for item in [
        "<b>Dominio</b> — qué representa la spec, en 2–3 oraciones.",
        "<b>Scope</b> — lista explícita de entidades/tablas con columnas clave.",
        "<b>Tech stack</b> — versión de DB, estrategia de IDs, formato de timestamps.",
        "<b>Convenciones</b> — naming, columnas de estado (CHECK vs ENUM), tipo de moneda.",
        "<b>Reglas de integridad</b> — soft delete, ON DELETE, UNIQUE, CHECK constraints.",
        "<b>Reglas de safe-change</b> — columnas nullable, sin renombrados, índices en FKs.",
        "<b>Fuera de scope</b> — qué NO generar (evita tablas alucinadas).",
        "<b>Entregable esperado</b> — formato exacto de output (solo SQL, sin prosa, sin fences).",
    ]:
        story.append(b(item))

    tbl_rubric = Table(
        [
            ["Categoría", "Máx", "Qué evalúa"],
            ["Structure", "30", "Tablas requeridas, FKs, sin tablas inventadas"],
            ["Naming", "15", "snake_case, id/{table}_id, created_at/updated_at"],
            ["Integrity", "20", "PK/FK, NOT NULL, UNIQUE, soft delete, CASCADE/RESTRICT"],
            ["Comments", "15", "Tablas y decisiones no obvias documentadas"],
            ["Query feasibility", "10", "Queries clave soportados, índices en FKs y hot paths"],
            ["Spec adherence", "10", "Siguió la spec, sin features inventadas"],
        ],
        colWidths=[4 * cm, 1.2 * cm, W - 5.2 * cm],
    )
    tbl_rubric.setStyle(tbl_style(header_bg=colors.HexColor("#00838F"), alt=TEAL_LIGHT))
    story += [sp(0.25), KeepTogether([h3("Rubric de evaluación de output (0–100):"),
              sp(0.1), tbl_rubric]), sp(0.15),
              note("Regla práctica: score < 80 → la spec necesita más detalle, no un modelo más caro. "
                   "Referencia completa: github.com/diegotrujillo-jikko/hermes-exploratory"),
              sp(0.2),
              note("Días sin workshop: adaptación libre + punto de control "
                   "(3 líneas de avance + bloqueos vía Hermes)."),
              sp(0.3)]

    # ── Workshop 3 (dentro de Etapa 1) ───────────────────────────────────────
    story += [sp(0.4),
              h2("Workshop 3 — CLAUDE.md · Jueves 25 jun, mañana (1–1.5 hrs)"),
              b("El /init genera el esqueleto; tú lo conviertes en un contrato AI preciso."),
              b("Componentes esenciales: authority hierarchy, safe/unsafe zones, naming conventions, "
                "model selection table."),
              b("Revisión en vivo de un CLAUDE.md real de producción (21 KB, API de SILIN)."),
              b("Diferencia entre un README y un AI operating contract."),
              b("Cada participante toma su repo actual (SILIN / integraciones) y escribe "
                "su propio CLAUDE.md desde cero."),
              b("Track DEV: orientado a construcción (safe zones para schema, API, FE)."),
              b("Track QA: orientado a pruebas (qué no modificar del SUT, cómo describir "
                "el alcance de cobertura)."),
              b("Revisión cruzada en pares."),
              sp(0.3)]

    # ── Workshop 4 (dentro de Etapa 1) ───────────────────────────────────────
    story += [sp(0.4),
              h2("Workshop 4 — Plan & Loop + MCP + Subagentes + Git · Jueves 25 jun, tarde (1–1.5 hrs)"),
              b("/plan antes de cualquier tarea compleja: cómo estructurar el trabajo antes "
                "de generar código."),
              b("Loop modes para tareas iterativas."),
              b("Sistema everything-claude-code: el skill correcto para cada tipo de tarea.")]

    tbl5 = Table(
        [
            ["Skill", "Uso"],
            [":tdd-workflow", "Desarrollo guiado por pruebas"],
            [":backend-patterns", "APIs y servicios"],
            [":security-review", "Revisión de seguridad"],
            [":database-reviewer", "Schema y queries"],
        ],
        colWidths=[4 * cm, W - 4 * cm],
    )
    tbl5.setStyle(tbl_style(header_bg=colors.HexColor("#00838F"), alt=TEAL_LIGHT))
    story += [KeepTogether([sp(0.1), tbl5, sp(0.2),
              b("Demostración completa: /init → /plan → build con skills apropiados.")]),
              sp(0.3),
              b("MCP Servers: Figma como fuente de diseño leíble por IA · Azure DevOps WI como PRD "
                "· claude-mem para memoria persistente entre sesiones."),
              KeepTogether([
                  b("Subagentes paralelos: patrón <b>LLM-as-judge</b> — un modelo genera el output, "
                    "otro lo evalúa. Caso real en <i>hermes-exploratory</i> Phase 2: "
                    "spec → generator → SQL → judge → score 0–100 → gate (precision ≥ 0.85 = merge ✓)."),
                  b("Git con AI: commits semánticos, PRs, ai-dev-log para trazabilidad de sesiones."),
                  b("Cierre del curso y lanzamiento oficial de los Retos Fase 1."),
                  sp(0.3),
              ])]

    # ── Etapa 2 ──────────────────────────────────────────────────────────────
    story += [h1("Etapa 2 — Reto Fase 1 · 26 jun – 6 jul"), sp(0.2),
              h2("Dos tracks en paralelo"), sp(0.1)]

    # Track DEV
    story += [
        h2("Track DEV — Portal de Convocatorias Públicas"),
        p(f"<b>Misión:</b> En 4 días, implementar el <b>Portal de Convocatorias Públicas</b> "
          f"— autenticación, backend REST, base de datos e integración con datos.gov.co (SECOP) — "
          f"sin escribir código a mano. "
          f"Todo se genera y se itera a través de {LLM_NOTE}."),
        sp(0.15),
        h3("Componentes obligatorios:"),
    ]
    tbl_dev = Table(
        [
            ["Componente", "Requisito"],
            ["Autenticación", "Registro e inicio de sesión con JWT"],
            ["Backend", "API REST — búsqueda, filtros, gestión de bookmarks"],
            ["Frontend", "Interfaz web funcional: browse de convocatorias y favoritos"],
            ["Base de datos", "PostgreSQL o SQLite — usuarios, bookmarks, búsquedas guardadas"],
            ["Integración", "datos.gov.co SECOP — consulta en vivo de convocatorias públicas"],
        ],
        colWidths=[4 * cm, W - 4 * cm],
    )
    tbl_dev.setStyle(tbl_style())
    dev_rules = [h3("Reglas:")]
    for i, r in enumerate([
        "Cero código manual — solo especificas, diriges, revisas e iteras.",
        f"{LLM_NOTE} — obligatorio e innegociable.",
        "Dominio fijo: Portal de Convocatorias. La diferencia la hace la profundidad de tu spec.",
        "Repositorio público (GitHub o GitLab).",
    ], 1):
        dev_rules.append(Paragraph(f"{i}. {r}", S["bullet"]))
    story += [tbl_dev, sp(0.2), KeepTogether(dev_rules), sp(0.3)]

    # Track QA
    story += [KeepTogether([
        h2("Track QA — Diseña y ejecuta una estrategia de pruebas"),
        p(f"<b>Misión:</b> En 4 días, diseñar, automatizar y ejecutar una estrategia de pruebas "
          f"E2E sobre la aplicación base provista (<i>gestor-inventario</i>), sin escribir "
          f"scripts a mano. Se usa {LLM_NOTE}."),
        sp(0.15),
        h3("Requisitos mínimos de entrega:"),
    ])]
    tbl_qa = Table(
        [
            ["Componente", "Requisito"],
            ["Plan de pruebas", "Estrategia, alcance, riesgos y criterios de aceptación"],
            ["Pruebas funcionales", "Casos: happy path, borde y negativos"],
            ["Suite API", "Contrato + errores — generada con Hermes + LLM, ejecutable con pytest"],
            ["Suite E2E (deseable)", "Playwright contra localhost:8000 — generada con IA si el tiempo lo permite"],
            ["Pruebas de datos e integración",
             "Validación de BD y del servicio de alertas (ALERTS_FAIL=1 → 503)"],
            ["Reporte de defectos",
             "Hallazgos con severidad, pasos de reproducción y evidencia"],
        ],
        colWidths=[5.5 * cm, W - 5.5 * cm],
    )
    tbl_qa.setStyle(tbl_style())
    qa_rules = [h3("Reglas:")]
    for i, r in enumerate([
        "Cero scripts manuales — la IA los genera, tú especificas y revisas.",
        f"{LLM_NOTE} — obligatorio como agente principal.",
        "No modificar el código de producción del SUT.",
        "Repositorio público (GitHub o GitLab).",
    ], 1):
        qa_rules.append(Paragraph(f"{i}. {r}", S["bullet"]))
    story += [tbl_qa, sp(0.2), KeepTogether(qa_rules), sp(0.3)]

    # ── Cronograma ───────────────────────────────────────────────────────────
    story += [PageBreak(), h1("Cronograma — Etapa 2 · Reto Fase 1"), sp(0.2)]
    tc_hdr = ParagraphStyle("tc_hdr", fontName="DejaVu-Bold", fontSize=9,
                            textColor=WHITE, leading=13)
    tc_body = ParagraphStyle("tc_body", fontName="DejaVu", fontSize=8.5, leading=13,
                             alignment=TA_LEFT)
    def tc(text, hdr=False):
        return Paragraph(text, tc_hdr if hdr else tc_body)
    dia_w = 3 * cm
    col_w = (W - dia_w) / 2
    tbl_cron = Table(
        [
            [tc("Día", hdr=True), tc("DEV", hdr=True), tc("QA", hdr=True)],
            [tc("Vie 26 jun"),
             tc("/init → CLAUDE.md → primera spec → inicio de construcción"),
             tc("/init → plan de pruebas → setup Playwright / pytest")],
            [tc("Lun 30 jun –\nVie 4 jul"),
             tc("Backend + Frontend + DB + Integración · punto de control diario (3 líneas vía Hermes)"),
             tc("E2E + API + datos + escenario ALERTS_FAIL=1 · punto de control diario")],
            [tc("Dom 6 jul"),
             tc("Repo final + SOUL.md · entrega antes de medianoche"),
             tc("Repo final + SOUL.md · entrega antes de medianoche")],
            [tc("Mar 7 jul"),
             tc("Demo 5–7 min + cata por grupos · evaluación final"),
             tc("Demo 5–7 min + cata por grupos · evaluación final")],
        ],
        colWidths=[dia_w, col_w, col_w],
    )
    tbl_cron.setStyle(tbl_style())
    story += [tbl_cron, sp(0.3)]

    # ── Entregables ──────────────────────────────────────────────────────────
    story += [h1("Entregables de ambos tracks"), sp(0.2),
              b("<b>SOUL.md</b> (obligatorio, tan importante como el código)"),
              sp(0.15), h3("Track DEV:")]
    for item in [
        "Qué construiste y qué problema resuelve",
        "Stack y arquitectura: componentes y cómo se conectan",
        "Cómo usaste Hermes y los LLMs: skills, specs y prompts que mejor funcionaron",
        "Decisiones y trade-offs",
        "Bloqueos y cómo los resolviste",
        "Qué mejorarías o pedirías",
        "Enlace al repositorio",
    ]:
        story.append(b(item))
    story += [sp(0.2), h3("Track QA:")]
    for item in [
        "Alcance: qué probaste y bajo qué estrategia",
        "Enfoque y herramientas: tipos de prueba y stack usado",
        "Cómo usaste Hermes y los LLMs: skills, specs e iteraciones",
        "Decisiones y trade-offs: qué priorizaste y por qué",
        "Bloqueos y cómo los resolviste",
        "Hallazgos principales / riesgos detectados",
        "Enlace al repositorio",
    ]:
        story.append(b(item))
    story.append(sp(0.3))

    # ── Criterios ────────────────────────────────────────────────────────────
    story += [PageBreak(), h1("Criterios de evaluación"), sp(0.2)]
    tbl_crit = Table(
        [
            ["Dimensión", "Peso"],
            ["Calidad del SOUL.md y trazabilidad del proceso", "25%"],
            ["Autonomía: investigó y desbloqueó por cuenta propia", "25%"],
            ["Orquestación de IA: claridad de specs, iteración, manejo de contexto", "18%"],
            ["Funcionalidad E2E (DEV) / Cobertura y profundidad (QA)", "14%"],
            ["Previsión y comunicación a tiempo", "10%"],
            ["Criterio técnico (DEV) / Criterio de QA (QA)", "8%"],
        ],
        colWidths=[W - 2 * cm, 2 * cm],
    )
    tbl_crit.setStyle(tbl_style())
    story += [tbl_crit, sp(0.2),
              note("Se busca criterio y adaptación, no el proyecto más grande ni la suite más extensa."),
              sp(0.3)]

    # ── Créditos y costos ────────────────────────────────────────────────────
    story += [
        h1("Sobre créditos y costos"),
        sp(0.2),
        p("Los modelos tienen costo y las capas gratuitas se agotan. "
          "Prever esto es parte del reto."),
        sp(0.1),
        p("Si necesitas acceso a un modelo corporativo o te vas a quedar corto de créditos, "
          "levanta la mano a tiempo — no el último día. Anticiparte y comunicar a tiempo "
          "es una de las capacidades que se están evaluando."),
        sp(0.2),
        note("Dudas durante el programa: canalízalas a Diego Trujillo — diego.trujillo@jikkosoft.com o Google Chat."),
    ]

    out = "/Users/dorothy/Stuff/Jikkosoft/Code/ai/lab/reto-ai-first-fase1/1-docs/1a-guia-ai-first.pdf"
    doc = SimpleDocTemplate(
        out, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
    )
    doc.build(story)
    print(f"Generated: {out}")

if __name__ == "__main__":
    build()
