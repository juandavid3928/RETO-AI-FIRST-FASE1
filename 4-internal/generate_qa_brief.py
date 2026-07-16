"""Generate 2b-reto-ai-first-fase1-qa.pdf using ReportLab + DejaVu Sans."""
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
        "code": ParagraphStyle("code", fontName="DejaVu", fontSize=8.5,
                               textColor=colors.HexColor("#1a1a1a"),
                               backColor=colors.HexColor("#F6F8FA"),
                               leftIndent=14, leading=14, spaceAfter=6),
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
        Paragraph("Diseña y ejecuta una estrategia de pruebas sobre gestor-inventario — sin escribir scripts manualmente", S["subtitle"]),
        Paragraph("Track QA · Preparado por Diego Trujillo · diego.trujillo@jikkosoft.com · Jikkosoft", S["subtitle"]),
        sp(0.8),
        hr(),
        sp(0.6),
    ]

    # ── 1. Por qué hacemos esto ──────────────────────────────────────────────
    story += [
        h1("1. Por qué hacemos esto"),
        sp(0.4),
        p("Jikkosoft está dando un paso hacia un modelo de trabajo AI-first: el rol del "
          "QA Engineer deja de ser ejecutar casos manualmente y pasa a ser "
          "<b>diseñar estrategias, orquestar pruebas y analizar evidencia</b> con asistencia de IA."),
        p("Este reto es tu espacio para experimentar ese cambio de chip mental en un entorno "
          "seguro, con acompañamiento y una ruta de aprendizaje. No se trata de saberlo todo "
          "desde el día uno: se trata de adaptarte, investigar y construir."),
        sp(0.5),
    ]

    # ── 2. El reto en una frase ──────────────────────────────────────────────
    story += [
        h1("2. El reto en una frase"),
        sp(0.4),
        p(f"En 6 días hábiles, diseña y ejecuta una estrategia de pruebas completa sobre "
          f"<b>gestor-inventario</b> — la app incluida en este repositorio — sin escribir "
          f"scripts a mano: todo se genera y se itera a través de {LLM_NOTE}. "
          f"El objetivo es <b>probar la app, no modificarla</b>."),
        sp(0.5),
    ]

    # ── 3. La app que debes probar ───────────────────────────────────────────
    story += [
        h1("3. La app que debes probar — gestor-inventario"),
        sp(0.4),
        p("La aplicación está en <b>3-challenge/gestor-inventario/</b>. Es una app full-stack "
          "mínima y autocontenida: FastAPI + SQLite + frontend estático. "
          "No debes modificar su código — solo probarlo."),
        sp(0.2),
    ]
    tbl_api = Table(
        [
            ["Método", "Ruta", "Descripción"],
            ["GET", "/api/health", "Estado del servicio"],
            ["GET", "/api/suppliers", "Lista de proveedores activos"],
            ["GET", "/api/products", "Lista de productos activos"],
            ["GET", "/api/products/{id}", "Detalle — 404 si no existe"],
            ["POST", "/api/products", "Crear producto (201 / 409 SKU duplicado)"],
            ["POST", "/api/stock/movement", "Movimiento IN o OUT (201 / 503 si ALERTS_FAIL)"],
            ["GET", "/api/stock/alerts", "Productos con stock <= minimo (503 si ALERTS_FAIL)"],
            ["GET", "/api/movements", "Historial de movimientos"],
        ],
        colWidths=[1.8 * cm, 5.2 * cm, W - 7 * cm],
    )
    tbl_api.setStyle(tbl_style())
    story += [tbl_api, sp(0.3)]

    story += [
        p("Para ejecutar la app localmente:"),
        Paragraph("cd 3-challenge/gestor-inventario", S["code"]),
        Paragraph("pip install -r requirements.txt &amp;&amp; uvicorn app:app --port 8000", S["code"]),
        Paragraph("# Con Docker:  docker compose up --build", S["code"]),
        Paragraph("# Fallo de integracion:  ALERTS_FAIL=1 uvicorn app:app --port 8000", S["code"]),
        note("Todos los montos son en centavos (integer). La app siembra 3 proveedores y 6 productos al primer arranque."),
        sp(0.5),
    ]

    # ── 4. Alcance de cobertura requerido ────────────────────────────────────
    story += [
        h1("4. Alcance de cobertura requerido"),
        sp(0.4),
        p("Tu estrategia debe cubrir estas dimensiones obligatoriamente:"),
        sp(0.2),
    ]
    tbl_scope = Table(
        [
            ["Dimension", "Que validar"],
            ["Contrato de API",
             "HTTP status codes, campos requeridos en respuesta, shapes de error"],
            ["Funcional",
             "Happy path, edge cases y casos negativos para cada endpoint"],
            ["Integridad de datos",
             "Stock se actualiza correctamente tras movimientos IN/OUT; valores match aritmetica"],
            ["Fallo de integracion",
             "ALERTS_FAIL=1 → 503 en /api/stock/alerts y POST /api/stock/movement (OUT)"],
            ["UI / E2E",
             "Flujo de registro de movimientos y consulta de alertas desde el frontend"],
        ],
        colWidths=[3.5 * cm, W - 3.5 * cm],
    )
    tbl_scope.setStyle(tbl_style())
    story += [tbl_scope, sp(0.5)]

    # ── 5. Reglas del juego ──────────────────────────────────────────────────
    story += [
        h1("5. Reglas del juego"),
        sp(0.4),
        n(1, "Cero scripts manuales. No escribes codigo de pruebas tu; lo genera la IA. "
           "Tu trabajo es disenar la estrategia, dirigir la generacion, revisar e iterar."),
        n(2, f"{LLM_NOTE} — obligatorio e innegociable. Toda interaccion con modelos pasa a traves de Hermes."),
        n(3, "Tu repo, tu casa. Sube el codigo a GitHub publico o GitLab, donde prefieras."),
        n(4, "No modificar la app bajo prueba. Cualquier cambio al codigo de gestor-inventario invalida los hallazgos."),
        n(5, "Provee tu acceso a modelos. Necesitaras un proveedor LLM conectado a Hermes. Ver punto 8 sobre creditos."),
        sp(0.5),
    ]

    # ── 6. Qué debes entregar ────────────────────────────────────────────────
    story += [
        h1("6. Que debes entregar"),
        sp(0.4),
    ]
    tbl_del = Table(
        [
            ["Entregable", "Descripcion"],
            ["SOUL.md",
             "Log del proceso: scope, tooling, decisiones de estrategia, hallazgos, blockers"],
            ["Plan de pruebas",
             "Estrategia, alcance, riesgos, criterios de aceptacion"],
            ["Casos de prueba",
             "Happy path + edge + negativos, documentados (markdown o tabla)"],
            ["Suite API",
             "Contrato + validacion de errores — generada con Hermes + LLM, ejecutable con pytest"],
            ["Suite E2E (deseable)",
             "Playwright o equivalente contra localhost:8000 — generada con IA si el tiempo lo permite"],
            ["Reporte de defectos",
             "Hallazgos con severidad, pasos de reproduccion, evidencia"],
        ],
        colWidths=[3.8 * cm, W - 3.8 * cm],
    )
    tbl_del.setStyle(tbl_style())
    story += [tbl_del, sp(0.3)]

    story += [
        Paragraph("Plantilla del entregable SOUL.md", S["h2"]),
    ]
    for item in [
        "Proyecto: que app probaste y cual fue tu estrategia de cobertura",
        "Stack de pruebas: herramientas, frameworks y como se conectan",
        "Como usaste Hermes y los LLMs: prompts que mejor funcionaron, iteraciones de generacion",
        "Decisiones y trade-offs: que elegiste cubrir primero y por que",
        "Hallazgos: defectos encontrados con severidad y evidencia",
        "Bloqueos y como los resolviste",
        "Enlace al repositorio",
    ]:
        story.append(b(item))
    story.append(sp(0.5))

    # ── 7. Cronograma ────────────────────────────────────────────────────────
    tc_hdr = ParagraphStyle("tc_hdr", fontName="DejaVu-Bold", fontSize=9,
                            textColor=WHITE, leading=13)
    tc_body = ParagraphStyle("tc_body", fontName="DejaVu", fontSize=8.5,
                             leading=13, alignment=TA_LEFT)
    def tc(text, hdr=False):
        return Paragraph(text, tc_hdr if hdr else tc_body)
    tbl_cron = Table(
        [
            [tc("Dia", hdr=True), tc("Fecha", hdr=True), tc("Foco", hdr=True)],
            [tc("Apertura"), tc("Vie 26 jun"),
             tc("Lanzamiento del reto, exploracion de la app, diseno de estrategia")],
            [tc("Dias 1-5"), tc("Lun-Vie 30 jun - 6 jul"),
             tc("Generacion de suites + ejecucion + reporte de defectos")],
            [tc("Evaluacion"), tc("Mar 7 jul"),
             tc("Demos y revision de hallazgos por grupos")],
        ],
        colWidths=[2.5 * cm, 2.5 * cm, W - 5 * cm],
    )
    tbl_cron.setStyle(tbl_style())
    story += [KeepTogether([
        h1("7. Cronograma (tentativo)"), sp(0.4), tbl_cron, sp(0.3),
        note("Punto de control diario: un reporte breve (3 lineas) de avance + bloqueos. "
             "Sirve para acompanarte, no para vigilarte."),
        sp(0.3),
    ])]

    # ── 8. Créditos ──────────────────────────────────────────────────────────
    story += [
        h1("8. Sobre creditos y costos — leelo"),
        sp(0.4),
        p("Los modelos cuestan y las capas gratuitas se agotan. Prever esto es parte del reto."),
        p("Si ves que te vas a quedar corto de creditos o necesitas acceso a un modelo "
          "corporativo, levanta la mano a tiempo (no el ultimo dia). Anticiparte y comunicar "
          "a tiempo es justamente una de las capacidades que estamos observando."),
        sp(0.3),
    ]

    # ── 9. Ruta de aprendizaje ───────────────────────────────────────────────
    story += [
        h1("9. Ruta de aprendizaje sugerida"),
        sp(0.4),
        p("No estas solo. Te sugerimos recursos para arrancar (no son obligatorios ni "
          "exhaustivos — exploralos y trae los tuyos)."),
        sp(0.3),
    ]
    story += [KeepTogether([
        Paragraph("Testing con IA — frameworks recomendados", S["h2"]),
        lnk("Playwright — documentacion oficial", "https://playwright.dev/python/docs/intro"),
        lnk("pytest + httpx — testing de APIs async", "https://www.python-httpx.org/"),
    ])]
    story += [KeepTogether([
        Paragraph("Escritura de specs y prompts efectivos", S["h2"]),
        lnk("Guia de prompt engineering (Claude Docs)",
            "https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview"),
    ])]
    story += [KeepTogether([
        Paragraph("Hermes (obligatorio)", S["h2"]),
        lnk("Hermes Agent (Nous Research) — repositorio y documentacion oficial",
            "https://github.com/NousResearch/hermes-agent"),
    ])]
    story.append(sp(0.3))

    # ── 10. Evaluación ───────────────────────────────────────────────────────
    eval_items = [
        h1("10. Como te vamos a evaluar (vision general)"), sp(0.4),
        p("No buscamos la suite mas grande, buscamos <b>criterio y profundidad</b>. "
          "Valoramos especialmente:"),
        sp(0.2),
        b("La calidad de tu SOUL.md y la trazabilidad de tu proceso"),
        b("Tu autonomia: como investigaste y resolviste bloqueos por tu cuenta"),
        b("La profundidad de cobertura: no solo happy path — edge cases, negativos, integridad de datos"),
        b("Los defectos encontrados y la calidad de su documentacion (severidad, repro, evidencia)"),
        b("Las suites son ejecutables: Playwright y pytest corren contra localhost:8000 sin modificacion manual"),
        b("Tu prevision y comunicacion a tiempo"),
        sp(0.4),
        note("Dudas durante el reto: canarizalas a Diego Trujillo — "
             "diego.trujillo@jikkosoft.com o Google Chat."),
    ]
    story.append(KeepTogether(eval_items))

    out = "/Users/dorothy/Stuff/Jikkosoft/Code/ai/lab/reto-ai-first-fase1/3-challenge/2b-reto-ai-first-fase1-qa.pdf"
    doc = SimpleDocTemplate(
        out, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
    )
    doc.build(story)
    print(f"Generated: {out}")


if __name__ == "__main__":
    build()
