"""Generate 2a-reto-ai-first-fase1.pdf using ReportLab + DejaVu Sans."""
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
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
WHITE = colors.white
GREY_ROW = colors.HexColor("#EEEEEE")

LLM_NOTE = ("Hermes como agente principal y uno o varios LLMs de su preferencia "
            "para codificar o implementar (ej: Claude Sonnet, Haiku, Opus, Codex, "
            "DeepSeek, Kimi K2, etc.)")

def styles():
    base = dict(fontName="DejaVu", fontSize=9.5, leading=17, alignment=TA_JUSTIFY,
                spaceAfter=8)
    return {
        "title": ParagraphStyle("title", fontName="DejaVu-Bold", fontSize=20,
                                textColor=TEAL, alignment=TA_CENTER, spaceAfter=8),
        "subtitle": ParagraphStyle("subtitle", fontName="DejaVu", fontSize=10.5,
                                   textColor=colors.HexColor("#444444"),
                                   alignment=TA_CENTER, spaceAfter=5),
        "h1": ParagraphStyle("h1", fontName="DejaVu-Bold", fontSize=13,
                             textColor=WHITE, alignment=TA_LEFT, leading=18),
        "h2": ParagraphStyle("h2", fontName="DejaVu-Bold", fontSize=10.5,
                             textColor=TEAL, spaceBefore=18, spaceAfter=6),
        "body": ParagraphStyle("body", **base),
        "bullet": ParagraphStyle("bullet", **{**base, "leftIndent": 14,
                                              "bulletIndent": 4, "spaceAfter": 6}),
        "numbered": ParagraphStyle("numbered", **{**base, "leftIndent": 18,
                                                  "bulletIndent": 4, "spaceAfter": 6}),
        "note": ParagraphStyle("note", fontName="DejaVu-Italic", fontSize=8.5,
                               textColor=colors.HexColor("#555555"),
                               alignment=TA_JUSTIFY, spaceAfter=6, leading=13),
        "link": ParagraphStyle("link", fontName="DejaVu", fontSize=9.5,
                               textColor=colors.HexColor("#0066CC"),
                               leftIndent=14, bulletIndent=4,
                               leading=16, spaceAfter=5, alignment=TA_LEFT),
    }

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

    def p(text):  return Paragraph(text, S["body"])
    def b(text):  return Paragraph(f"• {text}", S["bullet"])
    def n(i, text): return Paragraph(f"{i}. {text}", S["numbered"])
    def lnk(label, url):
        return Paragraph(
            f'• <a href="{url}" color="#0066CC"><u>{label}</u></a>', S["link"]
        )
    def note(text): return Paragraph(text, S["note"])
    def sp(h=0.4): return Spacer(1, h * cm)
    def hr(): return HRFlowable(width="100%", thickness=0.5,
                                color=colors.HexColor("#CCCCCC"), spaceAfter=4)

    story = []

    # ── Title block ──────────────────────────────────────────────────────────
    story += [
        sp(1.0),
        Paragraph("Reto AI-First · Fase 1", S["title"]),
        sp(0.4),
        Paragraph("Construye el Portal de Convocatorias Públicas — sin escribir código manualmente", S["subtitle"]),
        Paragraph("Track DEV · Preparado por Diego Trujillo · diego.trujillo@jikkosoft.com · Jikkosoft", S["subtitle"]),
        sp(0.8),
        hr(),
        sp(0.6),
    ]

    # ── 1. Por qué hacemos esto ──────────────────────────────────────────────
    story += [
        h1("1. Por qué hacemos esto"),
        sp(0.4),
        p("Jikkosoft está dando un paso hacia un modelo de trabajo AI-first: el rol del "
          "desarrollador deja de ser escribir código línea por línea y pasa a ser "
          "<b>especificar, orquestar y validar</b> sistemas construidos con asistencia de IA."),
        p("Este reto es tu espacio para experimentar ese cambio de chip mental en un entorno "
          "seguro, con acompañamiento y una ruta de aprendizaje. No se trata de saberlo todo "
          "desde el día uno: se trata de adaptarte, investigar y construir."),
        sp(0.5),
    ]

    # ── 2. El reto en una frase ──────────────────────────────────────────────
    story += [
        h1("2. El reto en una frase"),
        sp(0.4),
        p(f"En 6 días hábiles, implementa el <b>Portal de Convocatorias Públicas</b> — una app con "
          f"autenticación, backend, base de datos e integración con datos.gov.co — "
          f"sin escribir código a mano: todo se genera y se itera a través de {LLM_NOTE}."),
        sp(0.5),
    ]

    # ── 3. Qué debes construir ───────────────────────────────────────────────
    story += [
        h1("3. Qué debes construir — Portal de Convocatorias Públicas"),
        sp(0.4),
        p("Un portal donde usuarios registrados pueden explorar, filtrar y guardar "
          "convocatorias públicas colombianas. La fuente de datos es la API abierta de "
          "<b>datos.gov.co</b> (SECOP — Sistema Electrónico para la Contratación Pública). "
          "El dominio es fijo para todos — la diferencia la hace la calidad de tu implementación "
          "y la profundidad de tu spec."),
        sp(0.2),
    ]
    tbl_comp = Table(
        [
            ["Componente", "Requisito mínimo"],
            ["Autenticación",
             "Registro e inicio de sesión con JWT — usuarios tienen perfil propio"],
            ["Backend",
             "API REST con lógica de negocio: búsqueda, filtros, gestión de bookmarks"],
            ["Frontend",
             "Interfaz web funcional: browse de convocatorias, guardar favoritos, perfil"],
            ["Base de datos",
             "PostgreSQL o SQLite — tablas: usuarios, bookmarks, búsquedas guardadas"],
            ["Integración",
             "datos.gov.co SECOP — consulta en vivo de convocatorias por entidad, fecha y estado"],
        ],
        colWidths=[3.5 * cm, W - 3.5 * cm],
    )
    tbl_comp.setStyle(tbl_style())
    story += [tbl_comp, sp(0.3),
              p("El endpoint base de datos.gov.co usa el protocolo Socrata Open Data API (SODA). "
                "Ejemplo: <font color='#0066CC'>https://www.datos.gov.co/resource/p6dx-8zbt.json</font> "
                "(SECOP I — contratos y convocatorias). No requiere API key para consultas básicas."),
              sp(0.3)]

    # ── 4. Reglas del juego ──────────────────────────────────────────────────
    story += [
        h1("4. Reglas del juego"),
        sp(0.4),
        n(1, "Cero código manual. No escribes código tú; lo genera la IA. Tu trabajo es "
           "especificar, dirigir, revisar e iterar."),
        n(2, f"{LLM_NOTE} — obligatorio e innegociable. Toda interacción con modelos "
           f"(generación, consulta, refactor) pasa a través de Hermes."),
        n(3, "Tu repo, tu casa. Sube el código a GitHub público o GitLab. El dominio es fijo "
           "(Portal de Convocatorias) — la diferencia la hace la profundidad de tu implementación."),
        n(4, "Provee tu acceso a modelos. Necesitarás un proveedor LLM conectado a Hermes "
           "(OpenAI, Anthropic, etc.). Ver punto 7 sobre créditos."),
        sp(0.5),
    ]

    # ── 5. Qué debes entregar ────────────────────────────────────────────────
    story += [
        h1("5. Qué debes entregar"),
        sp(0.4),
        n(1, "Repositorio (GitHub público o GitLab) con el proyecto funcional."),
        n(2, "Contexto de Hermes en un archivo <b>SOUL.md</b> — el resumen "
           "contextual de tu trabajo con Hermes (plantilla abajo). Este archivo es tan "
           "importante como el código: es la evidencia de cómo construiste."),
        n(3, "Demo corta (5–7 min) el viernes de la semana del reto."),
        sp(0.3),
    ]
    soul_items = [
        Paragraph("Plantilla del entregable SOUL.md", S["h2"]),
        b("Proyecto: qué construiste y qué problema resuelve"),
        b("Stack y arquitectura: componentes y cómo se conectan"),
        b("Cómo usaste Hermes y los LLMs: skills/instrucciones clave, specs o prompts que mejor funcionaron, iteraciones"),
        b("Decisiones y trade-offs: qué elegiste y por qué"),
        b("Bloqueos y cómo los resolviste"),
        b("Qué mejorarías o pedirías"),
        b("Enlace al repositorio"),
        sp(0.5),
    ]
    story.append(KeepTogether(soul_items))

    # ── 6. Cronograma ────────────────────────────────────────────────────────
    tc_hdr = ParagraphStyle("tc_hdr", fontName="DejaVu-Bold", fontSize=9,
                            textColor=WHITE, leading=13)
    tc_body = ParagraphStyle("tc_body", fontName="DejaVu", fontSize=8.5,
                             leading=13, alignment=TA_LEFT)
    def tc(text, hdr=False):
        return Paragraph(text, tc_hdr if hdr else tc_body)
    tbl_cron = Table(
        [
            [tc("Día", hdr=True), tc("Fecha", hdr=True), tc("Foco", hdr=True)],
            [tc("Apertura"), tc("Vie 26 jun"),
             tc("Lanzamiento del reto, ruta de aprendizaje, inicio de construcción")],
            [tc("Días 1–5"), tc("Lun–Vie 30 jun – 6 jul"),
             tc("Construcción + puntos de control diarios")],
            [tc("Evaluación"), tc("Mar 7 jul"),
             tc("Demos y revisión por grupos")],
        ],
        colWidths=[2.5 * cm, 2.5 * cm, W - 5 * cm],
    )
    tbl_cron.setStyle(tbl_style())
    story.append(KeepTogether([
        h1("6. Cronograma (tentativo)"), sp(0.4),
        tbl_cron, sp(0.3),
        note("Punto de control diario: un reporte breve (3 líneas) de avance + bloqueos, "
             "vía Hermes/Drive. Sirve para acompañarte, no para vigilarte."),
        sp(0.3),
    ]))

    # ── 7. Créditos ──────────────────────────────────────────────────────────
    story += [
        h1("7. Sobre créditos y costos — léelo"),
        sp(0.4),
        p("Los modelos cuestan y las capas gratuitas se agotan. Prever esto es parte del reto."),
        p("Si ves que te vas a quedar corto de créditos o necesitas acceso a un modelo "
          "corporativo, levanta la mano a tiempo (no el último día). Anticiparte y comunicar "
          "a tiempo es justamente una de las capacidades que estamos observando."),
        sp(0.3),
    ]

    # ── 8. Ruta de aprendizaje ───────────────────────────────────────────────
    story += [
        h1("8. Ruta de aprendizaje sugerida"),
        sp(0.4),
        p("No estás solo. Te sugerimos recursos para arrancar (no son obligatorios ni "
          "exhaustivos — explóralos y trae los tuyos). Sea cual sea la herramienta que "
          "elijas, recuerda que debe conectarse a través de Hermes."),
        sp(0.3),
    ]
    story += [KeepTogether([
        Paragraph("Fundamentos de orquestación de IA y agentes", S["h2"]),
        lnk("Anthropic — Effective context engineering for AI agents",
            "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents"),
        lnk("Anthropic Academy — Build with Claude",
            "https://www.anthropic.com/learn/build-with-claude"),
    ])]
    story += [KeepTogether([
        Paragraph("Escritura de specs / prompting efectivo", S["h2"]),
        lnk("Guía de prompt engineering (Claude Docs)",
            "https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview"),
        lnk("Tutorial interactivo de prompting (Anthropic)",
            "https://github.com/anthropics/prompt-eng-interactive-tutorial"),
    ])]
    story += [KeepTogether([
        Paragraph("Herramientas de desarrollo asistido por IA", S["h2"]),
        lnk("Documentación de Claude Code",
            "https://code.claude.com/docs/en/overview"),
    ])]
    story += [KeepTogether([
        Paragraph("Uso de Hermes (obligatorio)", S["h2"]),
        lnk("Hermes Agent (Nous Research) — repositorio y documentación oficial",
            "https://github.com/NousResearch/hermes-agent"),
    ])]
    story += [KeepTogether([
        Paragraph("Manejo de repositorios (GitHub / GitLab)", S["h2"]),
        lnk("GitHub — primeros pasos", "https://docs.github.com/get-started"),
        lnk("GitLab Docs", "https://docs.gitlab.com/"),
    ])]
    story.append(sp(0.3))

    # ── 9. Evaluación ────────────────────────────────────────────────────────
    story += [
        sp(0.5),
        h1("9. Cómo te vamos a evaluar (visión general)"),
        sp(0.4),
        p("No buscamos el proyecto más grande, buscamos <b>criterio y adaptación</b>. "
          "Valoramos especialmente:"),
        sp(0.2),
    ]
    for item in [
        "La calidad de tu SOUL.md y la trazabilidad de tu proceso",
        "Tu autonomía: cómo investigaste y resolviste bloqueos por tu cuenta",
        "Qué tan bien orquestaste la IA (claridad de tus specs, iteración, contexto)",
        "Que el producto funcione end-to-end: auth + browse de convocatorias desde datos.gov.co + bookmarks persistidos en DB",
        "Tu previsión y comunicación a tiempo",
    ]:
        story.append(b(item))
    story += [
        sp(0.4),
        note("Dudas durante el reto: canalízalas a Diego Trujillo — "
             "diego.trujillo@jikkosoft.com o Google Chat."),
    ]

    out = "/Users/dorothy/Stuff/Jikkosoft/Code/ai/lab/reto-ai-first-fase1/3-challenge/2a-reto-ai-first-fase1.pdf"
    doc = SimpleDocTemplate(
        out, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
    )
    doc.build(story)
    print(f"Generated: {out}")

if __name__ == "__main__":
    build()
