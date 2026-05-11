"""
Gera os 32 slides da estreia do Instagram da Renegocia
via Gemini 3.1 Flash Image Preview (Nano Banana 2).

Estratégia:
 - Cada slide é uma cena fotográfica cinematográfica (still-life premium
   estilo Patek Philippe / Monocle Magazine).
 - A IA gera a cena com o rodapé RESERVADO (faixa de cor sólida sem nada).
 - Depois, PIL substitui o rodapé por uma faixa sólida (verde escuro ou
   creme) + logo real + wordmark "RENEGOCIA" + handle "@renegocia.tributario".

Organiza em pastas por post:
    instagram-posts/post-X-nome/slide-N-descricao.png

Uso:
    GEMINI_API_KEY=AIzaSy... python scripts/gen_all_posts.py
    GEMINI_API_KEY=... python scripts/gen_all_posts.py --only post-2-como-funciona
    GEMINI_API_KEY=... python scripts/gen_all_posts.py --skip-existing
    GEMINI_API_KEY=... python scripts/gen_all_posts.py --recomp-only
"""

import argparse
import os
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGO_PATH = PROJECT_ROOT / "brand-manual" / "brand" / "logo-circle.png"
OUTPUT_ROOT = PROJECT_ROOT / "instagram-posts"
HANDLE = "@renegocia.tributario"

MODEL_ID = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-3.1-flash-image-preview")

WIN_FONTS = Path("C:/Windows/Fonts")
FONT_WORDMARK = WIN_FONTS / "seguibl.ttf"   # Segoe UI Black (proxy Montserrat 800)
FONT_HANDLE = WIN_FONTS / "segoeui.ttf"     # Segoe UI Regular

COLORS = {
    "green_900": (15, 47, 42),    # #0F2F2A
    "cream": (247, 246, 242),     # #F7F6F2
    "gold": (212, 175, 55),       # #D4AF37
}

# ─────────────────────────────────────────────────────────────────────
#  BRAND SPEC
# ─────────────────────────────────────────────────────────────────────

BRAND_SPEC = """=== CRITICAL RENDERING RULE ===
The ONLY visible text on the image is what appears INSIDE QUOTES below "TEXT CONTENT" markers. NEVER render specification metadata (weight, opacity, size, hex codes, "left-aligned", etc.) as visible text. Specifications describe HOW to render — they are NOT what to render.

=== RESERVED FOOTER AREA ===
The BOTTOM 12% of the canvas (a horizontal band, full width) must be RESERVED as a uniform solid color band — same color as the slide's "FOOTER_BG" specified below. Render NO text, NO logo, NO objects, NO decorations whatsoever in this reserved bottom band. A logo and handle will be added programmatically.

=== VISUAL STYLE: CINEMATIC EDITORIAL PHOTOGRAPHY ===
Every slide is a still-life photograph composed like a magazine editorial spread (Patek Philippe, Monocle, Bloomberg Businessweek, Brioni). Premium, restrained, confident. Natural directional lighting from upper-left creating soft long shadows. Shallow depth of field where appropriate. Color palette dominated by warm neutrals.

Allowed objects: vintage brass mechanical calculator (with paper tape, NEVER digital), Brazilian Receita Federal tax documents (white paper with blurry official letterhead, never readable text), gold-rimmed fountain pen, brown leather portfolio, tortoiseshell reading glasses, small porcelain espresso cup, gold coins (3–6 max, never piles), magnifying glass with brass handle, wooden gavel, manila envelopes with red wax seal, antique brass balance scale, vintage pocket watch, single sheet invoice (nota fiscal), bound corporate document with twine, ribbon-tied scroll.

Forbidden: hands, fingers, people, faces, smartphones, laptops, modern computer screens, modern keyboards, plastic items, neon, cartoonish illustrations, stock-photo clichés, money fanned in piles (vulgar), Brazilian flag, the actual Renegocia logo or wordmark (those are added separately).

=== COLOR PALETTE (use these hex codes exactly when rendering text) ===
- Deep forest green #0F2F2A (text on cream, or atmospheric dark backgrounds)
- Warm off-white #F7F6F2 (text on dark scenes)
- Metallic gold #D4AF37 (eyebrow labels, single-word accents — NEVER whole paragraphs)
- Emerald green #16B98A (rare positive accent — check marks only)

=== TYPOGRAPHY ===
Headlines extra-bold geometric sans-serif (Montserrat or similar), weight 800. Eyebrow labels semibold uppercase weight 600, very wide letter-spacing. Body weight 500.

=== TEXT OVERLAY OVER PHOTOGRAPHY ===
When placing text on top of the photographic scene, position it in the UPPER LEFT QUADRANT (or another negative-space area you create). The scene composition should leave that quadrant slightly darker / less detailed so text reads cleanly. Apply a very subtle dark soft drop shadow (NOT a heavy shadow) only when needed for legibility. Text edges must remain sharp.

=== HARD RULES ===
- Portuguese diacritics (ã, ç, õ, é, á, í) must render correctly with sharp edges.
- Square 1:1 Instagram format, 1024x1024 ready to publish.
- All visible text content must come from this prompt's TEXT CONTENT lines."""


def _scene(world: str, footer_bg: str, text_zone: str, slide_brief: str, text_block: str) -> str:
    """Monta o prompt para um slide CINEMATOGRÁFICO (com cena fotográfica)."""
    bg_color_name = "deep forest green #0F2F2A" if footer_bg == "dark" else "warm cream #F7F6F2"
    return f"""{BRAND_SPEC}

=== VISUAL WORLD (this slide's scene) ===
{world}

=== TEXT NEGATIVE SPACE ===
{text_zone}

=== SLIDE BRIEF ===
{slide_brief}

=== FOOTER_BG ===
The reserved bottom 12% band must be filled with solid {bg_color_name} — no objects, no text, no gradient. A flat color band.

=== TEXT CONTENT TO RENDER ===
{text_block}"""


def _typo(footer_bg: str, slide_brief: str, text_block: str) -> str:
    """Monta o prompt para um slide TIPOGRÁFICO PREMIUM (sem fotografia)."""
    bg_color_name = "deep forest green #0F2F2A" if footer_bg == "dark" else "warm cream #F7F6F2"
    primary_text = "warm off-white #F7F6F2" if footer_bg == "dark" else "deep forest green #0F2F2A"
    return f"""{BRAND_SPEC}

=== STYLE: PREMIUM EDITORIAL TYPOGRAPHY — NO PHOTOGRAPHY ===
This slide is PURE TYPOGRAPHY on a solid colored background — NO photographic objects, NO scenes, NO still-life elements, NO illustrations, NO icons. Think: a single page of Bloomberg Businessweek, Financial Times Weekend Edition, or a fine wine label. Sophistication comes from typographic hierarchy, generous whitespace, and very thin gold hairline rules.

Background: solid {bg_color_name} filling the ENTIRE canvas (except the reserved footer band, which is also a separate solid block).
Primary text color on this slide: {primary_text}.

Allowed decorative elements (use sparingly):
- Very thin gold hairline rules (1px), short or long
- Small gold dots (em-dash, bullet)
- Em-dash characters (—) in gold for eyebrow prefixes
- Number-prefix style "01 ·", "02 ·" in gold

Forbidden: any photograph, illustration, icon, drawn shape (other than the listed decorative rules/dots), gradient, drop shadow, texture, or scene.

=== SLIDE BRIEF ===
{slide_brief}

=== FOOTER_BG ===
The reserved bottom 12% band must be filled with solid {bg_color_name} — flat color block, no objects, no text.

=== TEXT CONTENT TO RENDER ===
{text_block}"""


# ─────────────────────────────────────────────────────────────────────
#  POSTS — 32 slides cinematográficos
# ─────────────────────────────────────────────────────────────────────

# Mundos visuais reusáveis
WORLD_DARK_DESK = (
    "Top-down or slightly angled flat-lay photograph of an antique dark mahogany executive desk. "
    "Warm directional window light from upper-left creates soft long shadows. "
    "Color palette: deep mahogany browns, ivory paper, brass gold, hints of forest green. "
    "Aesthetic: 1920s law firm meets modern editorial."
)

WORLD_CREAM_DESK = (
    "Flat-lay photograph on a warm cream linen or off-white marble surface. "
    "Soft diffuse natural light from upper-left, minimal shadows. "
    "Color palette: cream, ivory, brass gold, deep forest green accents. "
    "Aesthetic: Hermès stationery editorial."
)

# Zona de texto padrão
TEXT_ZONE_UPPER_LEFT = (
    "Leave the UPPER LEFT QUADRANT of the canvas (roughly the left 55% × top 45% of the visible area, "
    "ABOVE the reserved footer band) with simpler composition and slightly darker tones — "
    "a clean area where overlaid text will remain perfectly legible."
)

TEXT_ZONE_RIGHT = (
    "Leave the RIGHT TWO-THIRDS of the canvas as a clean area where overlaid text will sit. "
    "Concentrate the photographic objects in the LEFT THIRD."
)

POSTS = [
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "post-1-manifesto",
        "slides": [
            {
                "name": "slide-1-manifesto", "bg": "dark",
                "prompt": _scene(
                    world=WORLD_DARK_DESK + " A single crisp white Brazilian tax invoice (nota fiscal) lies slightly off-center to the right, partially under a soft beam of light. A gold-rimmed fountain pen rests diagonally across one corner of the paper. Very minimal — only TWO objects total. The rest of the desk is bare wood with rich grain.",
                    footer_bg="dark",
                    text_zone=TEXT_ZONE_UPPER_LEFT,
                    slide_brief="Manifesto of the brand. Sober, declarative, almost confrontational.",
                    text_block="""1. Eyebrow (top of upper-left zone):
   TEXT CONTENT: — MANIFESTO
   Style: metallic gold #D4AF37, uppercase, semibold, very wide letter-spacing.

2. Hero headline (occupying upper-left quadrant, four lines, extra-bold):
   TEXT CONTENT (each on own line):
     Sua empresa pode
     estar pagando
     imposto que ela
     não deve.
   Style: lines 1–3 warm off-white #F7F6F2; line 4 ("não deve.") METALLIC GOLD #D4AF37.

3. Subheadline (just below the headline, smaller):
   TEXT CONTENT (single line, may wrap to two):
     A Renegocia recupera o que o fisco cobrou a mais.
   Style: warm off-white #F7F6F2 with 80% opacity, medium weight.""",
                ),
            }
        ],
    },
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "post-2-como-funciona",
        "slides": [
            {
                "name": "slide-1-capa", "bg": "dark",
                "prompt": _scene(
                    world=WORLD_DARK_DESK + " Wide establishing shot of the desk: a vintage brass mechanical calculator (with paper tape) sits to the right, a stack of three tax documents fanned slightly in the center-right, a gold-rimmed fountain pen, a pair of tortoiseshell reading glasses folded, a small porcelain espresso cup. Objects are distributed across the right and lower-right area of the canvas.",
                    footer_bg="dark",
                    text_zone=TEXT_ZONE_UPPER_LEFT,
                    slide_brief="Carousel cover for the 'how it works' explainer. The wide shot here will be progressively zoomed in across the next 4 slides.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: — COMO FUNCIONA
   Style: gold, uppercase, wide letter-spacing.

2. Hero headline (extra-bold, three lines):
   TEXT CONTENT (each on own line):
     Como a Renegocia
     recupera imposto
     pago a mais.
   Style: warm off-white #F7F6F2.

3. Small right-aligned hint near right edge just above the reserved footer:
   TEXT CONTENT: ↦ deslize
   Style: gold, small.""",
                ),
            },
            {
                "name": "slide-2-diagnostico", "bg": "dark",
                "prompt": _typo(
                    footer_bg="dark",
                    slide_brief="Step 1 of 4 in the process. The magnifier visualizes 'diagnosis'.",
                    text_block="""1. Large numeral (huge, dominant in upper-left):
   TEXT CONTENT: 1
   Style: metallic gold #D4AF37, extra-bold, very large.

2. Label to the right of the numeral or directly below it:
   TEXT CONTENT: DIAGNÓSTICO CONSULTIVO
   Style: gold, semibold, uppercase, wide letter-spacing.

3. Body paragraph below the numeral:
   TEXT CONTENT: 30 a 45 minutos. A gente olha os tributos da sua empresa e identifica onde tem oportunidade.
   Style: warm off-white #F7F6F2, medium weight.""",
                ),
            },
            {
                "name": "slide-3-proposta", "bg": "dark",
                "prompt": _typo(
                    footer_bg="dark",
                    slide_brief="Step 2 of 4 — proposal delivered. The sealed envelope evokes formality.",
                    text_block="""1. Large numeral:
   TEXT CONTENT: 2
   Style: gold, extra-bold, very large.

2. Label:
   TEXT CONTENT: PROPOSTA EM 72H
   Style: gold, semibold, uppercase, wide letter-spacing.

3. Body:
   TEXT CONTENT: Recebe um relatório com o valor estimado a recuperar, prazo e quanto custa o serviço.
   Style: warm off-white #F7F6F2.""",
                ),
            },
            {
                "name": "slide-4-execucao", "bg": "dark",
                "prompt": _typo(
                    footer_bg="dark",
                    slide_brief="Step 3 of 4 — execution phase, where the firm files and processes.",
                    text_block="""1. Large numeral:
   TEXT CONTENT: 3
   Style: gold, extra-bold, very large.

2. Label:
   TEXT CONTENT: EXECUÇÃO
   Style: gold, semibold, uppercase, wide letter-spacing.

3. Body:
   TEXT CONTENT: A gente cuida de tudo — administrativo ou judicial. Você só recebe atualizações.
   Style: warm off-white #F7F6F2.""",
                ),
            },
            {
                "name": "slide-5-risco-compartilhado", "bg": "dark",
                "prompt": _typo(
                    footer_bg="dark",
                    slide_brief="Step 4 of 4 — shared risk model. The balance scale symbolizes equilibrium of incentives.",
                    text_block="""1. Large numeral:
   TEXT CONTENT: 4
   Style: gold, extra-bold, very large.

2. Label:
   TEXT CONTENT: RISCO COMPARTILHADO
   Style: gold, semibold, uppercase, wide letter-spacing.

3. Body (max 75% width):
   TEXT CONTENT: Você paga uma parte na contratação. O restante dos honorários só vence quando seu crédito tributário é reconhecido.
   Style: warm off-white #F7F6F2.""",
                ),
            },
        ],
    },
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "post-3-o-que-recuperamos",
        "slides": [
            {
                "name": "slide-1-capa", "bg": "cream",
                "prompt": _scene(
                    world=WORLD_CREAM_DESK + " Four small stacks of folded tax documents arranged in a precise 2×2 grid in the lower-right area of the canvas, each stack tied with a thin colored ribbon (deep green, gold, soft burgundy, and ivory). Each stack is small (about 4 papers tall). The cream surface around the grid is clean and minimal.",
                    footer_bg="cream",
                    text_zone=TEXT_ZONE_UPPER_LEFT,
                    slide_brief="Cover of the 'what we recover' catalog carousel. The 4 stacks symbolize the 4 categories.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: — O QUE RECUPERAMOS
   Style: gold, uppercase, semibold, wide letter-spacing.

2. Hero headline (extra-bold):
   TEXT CONTENT (each on own line):
     O que a Renegocia
     recupera.
   Style: deep forest green #0F2F2A.

3. Small right-aligned hint near right edge above footer:
   TEXT CONTENT: ↦ deslize
   Style: gold.""",
                ),
            },
            {
                "name": "slide-2-pis-cofins", "bg": "cream",
                "prompt": _typo(
                    footer_bg="cream",
                    slide_brief="Category 01 — PIS and COFINS overpayments.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: 01 · PIS / COFINS
   Style: gold, semibold, wide letter-spacing.

2. Headline (extra-bold, two lines):
   TEXT CONTENT (each on own line):
     PIS e COFINS
     pagos a mais
   Style: deep forest green #0F2F2A.

3. Body:
   TEXT CONTENT: Em vendas, insumos, ICMS na base.
   Style: deep forest green #0F2F2A, medium weight.""",
                ),
            },
            {
                "name": "slide-3-irpj-csll", "bg": "cream",
                "prompt": _typo(
                    footer_bg="cream",
                    slide_brief="Category 02 — IRPJ and CSLL on state incentives.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: 02 · IRPJ / CSLL
   Style: gold, semibold, wide letter-spacing.

2. Headline:
   TEXT CONTENT (each on own line):
     IRPJ e CSLL
     sobre incentivos.
   Style: deep forest green #0F2F2A, extra-bold.

3. Body (max 75% width):
   TEXT CONTENT: Se sua empresa tem benefício fiscal estadual, pode estar pagando IR sobre ele. Não deveria.
   Style: deep forest green #0F2F2A, medium weight.""",
                ),
            },
            {
                "name": "slide-4-inss", "bg": "cream",
                "prompt": _typo(
                    footer_bg="cream",
                    slide_brief="Category 03 — INSS on indemnity payroll items.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: 03 · INSS
   Style: gold, semibold, wide letter-spacing.

2. Headline:
   TEXT CONTENT (each on own line):
     INSS sobre folha
     de pagamento.
   Style: deep forest green #0F2F2A, extra-bold.

3. Body (max 80% width):
   TEXT CONTENT: Verbas indenizatórias (aviso, PLR, auxílios) não entram na base. Muita empresa paga assim mesmo.
   Style: deep forest green #0F2F2A, medium weight.""",
                ),
            },
            {
                "name": "slide-5-icms", "bg": "cream",
                "prompt": _typo(
                    footer_bg="cream",
                    slide_brief="Category 04 — ICMS overpayments.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: 04 · ICMS
   Style: gold, semibold, wide letter-spacing.

2. Headline:
   TEXT CONTENT (each on own line):
     ICMS pago
     a mais.
   Style: deep forest green #0F2F2A, extra-bold.

3. Body (max 80% width):
   TEXT CONTENT: Substituição tributária, energia, telecomunicações. Recuperação direta nos próximos 5 anos.
   Style: deep forest green #0F2F2A, medium weight.""",
                ),
            },
            {
                "name": "slide-6-cta", "bg": "dark",
                "prompt": _typo(
                    footer_bg="dark",
                    slide_brief="CTA close. Premium 'ready to start' feel.",
                    text_block="""1. Headline (extra-bold):
   TEXT CONTENT (each on own line):
     Quer saber qual
     se aplica à
     sua empresa?
   Style: warm off-white #F7F6F2.

2. CTA line:
   TEXT CONTENT: Diagnóstico consultivo no link da bio →
   Style: metallic gold #D4AF37, bold.""",
                ),
            },
        ],
    },
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "post-4-icms-base-pis-cofins",
        "slides": [
            {
                "name": "slide-1-hook", "bg": "dark",
                "prompt": _scene(
                    world=WORLD_DARK_DESK + " Dramatic chiaroscuro: a single Brazilian nota fiscal lies in a pool of warm light at the lower-right of the canvas, the rest of the desk in deep shadow. The light is harsh and editorial. A subtle gold coin sits next to the invoice catching a glint.",
                    footer_bg="dark",
                    text_zone=TEXT_ZONE_UPPER_LEFT,
                    slide_brief="Cover/hook for the 'Tese do Século' carousel. Most dramatic of all covers.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: — TESE DO SÉCULO
   Style: gold, semibold, wide letter-spacing.

2. Hero headline (extra-bold, four lines):
   TEXT CONTENT (each on own line):
     Sua empresa pode
     ter pago ICMS dentro
     de outro imposto
     — por 25 anos.
   Style: lines 1–3 warm off-white #F7F6F2; line 4 ("— por 25 anos.") METALLIC GOLD #D4AF37.

3. Right-aligned hint above footer:
   TEXT CONTENT: ↦ deslize
   Style: gold.""",
                ),
            },
            {
                "name": "slide-2-problema", "bg": "cream",
                "prompt": _typo(
                    footer_bg="cream",
                    slide_brief="The problem: tax-within-tax visualized through inspection.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: 02 · O PROBLEMA
   Style: gold, semibold, wide letter-spacing.

2. Body (extra-bold, medium-large size, max 85% width):
   TEXT CONTENT: Por décadas, o fisco cobrou PIS e COFINS sobre o valor total da nota — incluindo o ICMS já cobrado pelo estado.
   Style: deep forest green #0F2F2A, semibold.

3. Below body, larger highlight (extra-bold):
   TEXT CONTENT: Resultado: você pagava imposto sobre imposto.
   Style: deep forest green #0F2F2A.""",
                ),
            },
            {
                "name": "slide-3-stf-decidiu", "bg": "dark",
                "prompt": _typo(
                    footer_bg="dark",
                    slide_brief="The STF ruling — the gavel evokes judicial finality.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: 03 · O QUE MUDOU
   Style: gold, semibold, wide letter-spacing.

2. Hero headline (extra-bold, two lines):
   TEXT CONTENT (each on own line):
     Em 2017, o STF
     disse: não pode.
   Style: line 1 warm off-white #F7F6F2; line 2 ("disse: não pode.") METALLIC GOLD #D4AF37.

3. Below headline, small uppercase tag:
   TEXT CONTENT: TEMA 69 · DECISÃO DEFINITIVA
   Style: warm off-white #F7F6F2 with 75% opacity, semibold, wide letter-spacing.""",
                ),
            },
            {
                "name": "slide-4-significado", "bg": "dark",
                "prompt": _typo(
                    footer_bg="dark",
                    slide_brief="What it means for the company — the pocket watch evokes 'time to act'.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: 04 · O QUE ISSO SIGNIFICA
   Style: gold, semibold, wide letter-spacing.

2. Headline (extra-bold, two lines):
   TEXT CONTENT (each on own line):
     O que isso significa
     pra sua empresa?
   Style: warm off-white #F7F6F2.

3. Body (max 85% width):
   TEXT CONTENT: Tudo que foi pago a mais nos últimos 5 anos pode voltar. Com correção.
   Style: warm off-white #F7F6F2 with 85% opacity, medium weight.""",
                ),
            },
            {
                "name": "slide-5-quanto-da", "bg": "cream",
                "prompt": _typo(
                    footer_bg="cream",
                    slide_brief="The financial range — coins symbolize the recoverable value.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: 05 · QUANTO DÁ?
   Style: gold, semibold, wide letter-spacing.

2. Hero stat (very large, extra-bold):
   TEXT CONTENT: R$ 50K — R$ 200K
   Style: deep forest green #0F2F2A.

3. Caption below the stat:
   TEXT CONTENT: empresas de médio porte recuperam, em média
   Style: deep forest green #0F2F2A, medium weight, slightly translucent.

4. Thin gold hairline (60% width) below the caption.

5. Secondary stat below the line (italic, gold):
   TEXT CONTENT: muito mais
   Style: metallic gold #D4AF37, extra-bold italic.

6. Caption beneath:
   TEXT CONTENT: indústrias e distribuidoras
   Style: deep forest green #0F2F2A, medium, translucent.""",
                ),
            },
            {
                "name": "slide-6-cta", "bg": "dark",
                "prompt": _typo(
                    footer_bg="dark",
                    slide_brief="CTA — ready to start the consult.",
                    text_block="""1. Headline (extra-bold):
   TEXT CONTENT (each on own line):
     A Renegocia faz
     esse cálculo no
     diagnóstico consultivo
     de 45 minutos.
   Style: warm off-white #F7F6F2.

2. CTA line:
   TEXT CONTENT: Link na bio →
   Style: metallic gold #D4AF37, bold.""",
                ),
            },
        ],
    },
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "post-5-pergunta",
        "slides": [
            {
                "name": "slide-1-pergunta", "bg": "cream",
                "prompt": _scene(
                    world=WORLD_CREAM_DESK + " Fifteen small folded documents (white tax-paper style, slightly varied sizes) fanned out in a loose half-arc in the lower-right area of the canvas. Some have small gold paper-clips. The cream surface around is minimal.",
                    footer_bg="cream",
                    text_zone=TEXT_ZONE_UPPER_LEFT,
                    slide_brief="A provocative question post. The 15 documents reinforce the '15 teses' number.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: — PORTFÓLIO
   Style: gold, semibold, wide letter-spacing.

2. Headline (extra-bold, three lines):
   TEXT CONTENT (each on own line):
     Sua empresa já
     analisou quantas
     teses tributárias?
   Style: deep forest green #0F2F2A.

3. Small line below:
   TEXT CONTENT: A maioria nunca analisou nenhuma.
   Style: deep forest green #0F2F2A, medium weight, slightly translucent.""",
                ),
            }
        ],
    },
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "post-6-incentivos-icms",
        "slides": [
            {
                "name": "slide-1-hook", "bg": "dark",
                "prompt": _scene(
                    world=WORLD_DARK_DESK + " A rolled ribbon-tied scroll (parchment-like, with a deep green ribbon) rests in the lower-right area of the canvas, suggesting a state decree. Next to it a single gold coin. Warm directional light.",
                    footer_bg="dark",
                    text_zone=TEXT_ZONE_UPPER_LEFT,
                    slide_brief="Cover for the 'Incentivos ICMS' carousel — the scroll evokes an official state decree.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: — TEMA 1.182 STJ
   Style: gold, semibold, wide letter-spacing.

2. Hero headline (extra-bold, three lines):
   TEXT CONTENT (each on own line):
     Sua empresa tem
     benefício fiscal do estado?
     Pode estar pagando IR sobre ele.
   Style: lines 1–2 warm off-white #F7F6F2 (larger); line 3 METALLIC GOLD #D4AF37 (slightly smaller).

3. Right-aligned hint above footer:
   TEXT CONTENT: ↦ deslize
   Style: gold.""",
                ),
            },
            {
                "name": "slide-2-quem-tem", "bg": "cream",
                "prompt": _typo(
                    footer_bg="cream",
                    slide_brief="Who qualifies — industries with formal state tax incentives.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: 02 · QUEM TEM
   Style: gold, semibold, wide letter-spacing.

2. Headline (extra-bold, two lines):
   TEXT CONTENT (each on own line):
     Muitas indústrias e
     agroindústrias têm:
   Style: deep forest green #0F2F2A.

3. Three line items (semibold, each on own line, prefixed with a gold em-dash):
   TEXT CONTENT (each on own line):
     — Redução de ICMS
     — Crédito presumido
     — Diferimento
   Style: deep forest green #0F2F2A.

4. Small closing line:
   TEXT CONTENT: Por decreto estadual.
   Style: deep forest green #0F2F2A, medium weight, translucent.""",
                ),
            },
            {
                "name": "slide-3-fisco-cobrava", "bg": "dark",
                "prompt": _typo(
                    footer_bg="dark",
                    slide_brief="What the fisco was doing — the red stamp suggests aggressive taxation.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: 03 · O QUE O FISCO FAZIA
   Style: gold, semibold, wide letter-spacing.

2. Headline (extra-bold, three lines):
   TEXT CONTENT (each on own line):
     O fisco federal vinha
     cobrando IRPJ e CSLL
     sobre esse benefício.
   Style: warm off-white #F7F6F2.

3. Italic quote with quotation marks:
   TEXT CONTENT: "Como se fosse renda."
   Style: metallic gold #D4AF37, italic, semibold.""",
                ),
            },
            {
                "name": "slide-4-stj-pacificou", "bg": "dark",
                "prompt": _typo(
                    footer_bg="dark",
                    slide_brief="The STJ ruling that settled the question.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: 04 · O QUE MUDOU
   Style: gold, semibold, wide letter-spacing.

2. Hero headline (extra-bold, three lines):
   TEXT CONTENT (each on own line):
     Em 2023, o STJ
     pacificou:
     não é renda.
   Style: lines 1–2 warm off-white #F7F6F2; line 3 METALLIC GOLD #D4AF37.

3. Small uppercase tag:
   TEXT CONTENT: TEMA 1.182 · IMPOSTO PAGO A MAIS PODE SER RECUPERADO
   Style: warm off-white #F7F6F2 with 75% opacity, semibold, wide letter-spacing.""",
                ),
            },
            {
                "name": "slide-5-cta", "bg": "dark",
                "prompt": _typo(
                    footer_bg="dark",
                    slide_brief="Final CTA.",
                    text_block="""1. Headline (extra-bold, two lines):
   TEXT CONTENT (each on own line):
     Tem incentivo estadual?
     Vale o diagnóstico.
   Style: warm off-white #F7F6F2.

2. CTA line:
   TEXT CONTENT: Link na bio →
   Style: metallic gold #D4AF37, bold.""",
                ),
            },
        ],
    },
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "post-7-case-142k",
        "slides": [
            {
                "name": "slide-1-case", "bg": "cream",
                "prompt": _scene(
                    world="Top-down photograph of a dark mahogany executive desk filling the full canvas. Composition elements positioned in the LOWER-RIGHT THIRD: vintage brass mechanical calculator with paper tape curling, gold-rimmed fountain pen, a small fanned stack of Brazilian Receita Federal tax forms (white paper, blurry letterhead), 4 small gold coins arranged casually, a pair of tortoiseshell folded reading glasses, a small porcelain espresso cup with saucer. Warm window light from upper-left creating soft long shadows. Cinematic editorial top-down flat-lay, Bon Appétit / Monocle Magazine aesthetic. Very shallow depth of field. NO HANDS, NO PEOPLE, NO COMPUTER SCREENS.",
                    footer_bg="cream",
                    text_zone="Leave the UPPER LEFT QUADRANT (left 50% × top 50%) as the empty/darker portion of the desk surface — bare wood with only the rich grain showing. Text overlay sits here.",
                    slide_brief="Case study proof. This is the brand's hero shot — the highest production-value slide.",
                    text_block="""1. Eyebrow (upper-left):
   TEXT CONTENT: — CASO REAL
   Style: metallic gold #D4AF37, semibold, uppercase, wide letter-spacing.

2. Hero stat (very large, extra-bold):
   TEXT CONTENT: R$ 142 MIL
   Style: warm off-white #F7F6F2.

3. Descriptive body (max 60% width):
   TEXT CONTENT: recuperáveis identificados em 1 diagnóstico de 45 minutos.
   Style: warm off-white #F7F6F2, medium weight, slightly translucent.

4. Small uppercase meta line below:
   TEXT CONTENT: AUTO POSTO · SP · 2026
   Style: warm off-white #F7F6F2, semibold, wide letter-spacing, 70% opacity.""",
                ),
            }
        ],
    },
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "post-8-inss-folha",
        "slides": [
            {
                "name": "slide-1-hook", "bg": "dark",
                "prompt": _scene(
                    world=WORLD_DARK_DESK + " Three Brazilian holerite (payment slip) printouts scattered loosely in the lower-right area of the canvas, slightly overlapping each other. A brass paperclip on top of the stack. Warm dramatic side light.",
                    footer_bg="dark",
                    text_zone=TEXT_ZONE_UPPER_LEFT,
                    slide_brief="Cover for INSS carousel. Scattered slips suggest 'mess to be sorted'.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: — INSS SOBRE FOLHA
   Style: gold, semibold, wide letter-spacing.

2. Three stacked tags (each on own line, italic extra-bold, with leading gold dot):
   TEXT CONTENT (each on own line):
     · Aviso prévio.
     · PLR.
     · Auxílio-creche.
   Style: metallic gold #D4AF37.

3. Question below the tags (extra-bold):
   TEXT CONTENT (each on own line):
     Sua empresa paga INSS
     sobre tudo isso?
   Style: warm off-white #F7F6F2.

4. Right-aligned hint above footer:
   TEXT CONTENT: ↦ deslize
   Style: gold.""",
                ),
            },
            {
                "name": "slide-2-regra", "bg": "cream",
                "prompt": _typo(
                    footer_bg="cream",
                    slide_brief="The legal rule — clean single slip evokes clarity.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: 02 · A REGRA
   Style: gold, semibold, wide letter-spacing.

2. Headline (extra-bold, two lines):
   TEXT CONTENT (each on own line):
     O INSS incide
     sobre o salário.
   Style: deep forest green #0F2F2A.

3. Counter-statement below (extra-bold):
   TEXT CONTENT: Não sobre verbas que não são salário.
   Style: metallic gold #D4AF37.""",
                ),
            },
            {
                "name": "slide-3-sistema", "bg": "dark",
                "prompt": _typo(
                    footer_bg="dark",
                    slide_brief="The system over-calculates — complexity visualized.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: 03 · O QUE ACONTECE
   Style: gold, semibold, wide letter-spacing.

2. Headline (extra-bold, two lines):
   TEXT CONTENT (each on own line):
     Mas o sistema da folha
     calcula sobre quase tudo.
   Style: warm off-white #F7F6F2.

3. Italic supporting line below:
   TEXT CONTENT: E o STJ já disse, em várias súmulas, que não é assim.
   Style: warm off-white #F7F6F2, italic, slightly translucent.""",
                ),
            },
            {
                "name": "slide-4-checklist", "bg": "cream",
                "prompt": _typo(
                    footer_bg="cream",
                    slide_brief="Checklist of recoverable items — orderly grid suggests completeness.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: 04 · O QUE ENTRA NA RECUPERAÇÃO
   Style: gold, semibold, wide letter-spacing.

2. Four checklist items (semibold, each on own line, prefixed with a small gold check mark "✓"):
   TEXT CONTENT (each on own line):
     ✓ Aviso prévio indenizado
     ✓ Terço de férias
     ✓ PLR
     ✓ Auxílio-creche, auxílio-doença, vale-transporte em pecúnia
   Style: deep forest green #0F2F2A.""",
                ),
            },
            {
                "name": "slide-5-quanto", "bg": "dark",
                "prompt": _typo(
                    footer_bg="dark",
                    slide_brief="Recoverable amount — coins symbolize the financial return.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: 05 · QUANTO PODE VOLTAR?
   Style: gold, semibold, wide letter-spacing.

2. Hero stat (very large, extra-bold):
   TEXT CONTENT: R$ 50K — R$ 300K
   Style: warm off-white #F7F6F2.

3. Context (max 80% width):
   TEXT CONTENT: recuperáveis em 5 anos, em empresas com folha acima de R$ 100k/mês.
   Style: warm off-white #F7F6F2, medium weight, slightly translucent.""",
                ),
            },
            {
                "name": "slide-6-cta", "bg": "dark",
                "prompt": _typo(
                    footer_bg="dark",
                    slide_brief="CTA — ready to inspect your payroll.",
                    text_block="""1. Headline (extra-bold, three lines):
   TEXT CONTENT (each on own line):
     Sua folha tem
     essas verbas?
     Faz sentido olhar.
   Style: warm off-white #F7F6F2.

2. CTA line:
   TEXT CONTENT: Link na bio →
   Style: metallic gold #D4AF37, bold.""",
                ),
            },
        ],
    },
    # ─────────────────────────────────────────────────────────────────
    {
        "id": "post-9-cta-institucional",
        "slides": [
            {
                "name": "slide-1-cta", "bg": "dark",
                "prompt": _scene(
                    world=WORLD_DARK_DESK + " Premium minimal composition: a single open leather portfolio (deep cordovan, edges visible) lies in the lower-right area of the canvas, revealing a cream sheet with a signature line. A gold-rimmed Montblanc-style fountain pen lies diagonally across the page, its gold nib catching dramatic warm light from upper-left. A small porcelain espresso cup with saucer to the side. NO HANDS visible.",
                    footer_bg="dark",
                    text_zone=TEXT_ZONE_UPPER_LEFT,
                    slide_brief="Institutional close. Premium 'signing the contract' feel without showing a hand. The hero shot of the institutional set.",
                    text_block="""1. Eyebrow:
   TEXT CONTENT: — O COMPROMISSO
   Style: gold, semibold, wide letter-spacing.

2. Three lines of headline (each on own line, different treatments):
   TEXT CONTENT (each on own line):
     Diagnóstico consultivo em 45 minutos.
     Se não houver oportunidade, dizemos.
     Se houver, você paga uma parte na contratação e o restante quando seu crédito é reconhecido.
   Style: line 1 warm off-white #F7F6F2 bold; line 2 warm off-white slightly translucent medium; line 3 metallic gold #D4AF37 bold.""",
                ),
            }
        ],
    },
]


# ─────────────────────────────────────────────────────────────────────
#  Footer overlay via PIL — pixel-perfect brand fidelity
# ─────────────────────────────────────────────────────────────────────

def composite_footer(image_path: Path, bg: str) -> None:
    """Sobrepõe logo real + wordmark + handle no rodapé.

    Estratégia robusta:
     1. Substitui completamente a área do rodapé por uma faixa sólida
        (cor segundo `bg` do slide). Garante legibilidade total e protege
        contra a IA renderizar o rodapé numa cor inesperada.
     2. Desenha logo + wordmark + handle por cima com cor contrastante.
     3. Adiciona hairline dourada como divisor visual sutil.
    """
    img = Image.open(image_path).convert("RGBA")
    w, h = img.size

    footer_h = int(h * 0.12)
    footer_top = h - footer_h
    side_margin = int(w * 0.05)

    if bg == "cream":
        band_color = COLORS["cream"]
        text_color = COLORS["green_900"]
    else:
        band_color = COLORS["green_900"]
        text_color = COLORS["cream"]

    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, footer_top), (w, h)], fill=(*band_color, 255))

    hairline_y = footer_top - 1
    draw.line([(0, hairline_y), (w, hairline_y)], fill=(*COLORS["gold"], 180), width=1)

    # ----- logo com máscara circular on-the-fly (PNG original é RGB sem alpha) -----
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo_size = int(footer_h * 0.72)
    logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
    # cria máscara circular suave (anti-aliased)
    mask = Image.new("L", (logo_size, logo_size), 0)
    ImageDraw.Draw(mask).ellipse([(0, 0), (logo_size, logo_size)], fill=255)
    logo_x = side_margin
    logo_y = footer_top + (footer_h - logo_size) // 2
    img.paste(logo_resized, (logo_x, logo_y), mask)

    wordmark_size = int(footer_h * 0.34)
    try:
        font_wm = ImageFont.truetype(str(FONT_WORDMARK), wordmark_size)
    except OSError:
        font_wm = ImageFont.load_default()
    tracking_px = int(wordmark_size * 0.12)
    wm_x = logo_x + logo_size + int(footer_h * 0.20)
    wm_y = footer_top + (footer_h - wordmark_size) // 2 - int(wordmark_size * 0.08)
    cursor = wm_x
    for ch in "RENEGOCIA":
        draw.text((cursor, wm_y), ch, fill=text_color, font=font_wm)
        ch_w = draw.textbbox((0, 0), ch, font=font_wm)[2]
        cursor += ch_w + tracking_px

    handle_size = int(footer_h * 0.26)
    try:
        font_handle = ImageFont.truetype(str(FONT_HANDLE), handle_size)
    except OSError:
        font_handle = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), HANDLE, font=font_handle)
    handle_w = bbox[2] - bbox[0]
    handle_h = bbox[3] - bbox[1]
    handle_x = w - side_margin - handle_w
    handle_y = footer_top + (footer_h - handle_h) // 2 - int(handle_h * 0.2)

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    odraw.text((handle_x, handle_y), HANDLE, fill=(*text_color, int(255 * 0.7)), font=font_handle)
    img = Image.alpha_composite(img, overlay)

    img.convert("RGB").save(image_path, "PNG", optimize=True)


# ─────────────────────────────────────────────────────────────────────
#  Main loop
# ─────────────────────────────────────────────────────────────────────

def run(args: argparse.Namespace) -> int:
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key and not args.recomp_only:
        print("ERRO: defina GEMINI_API_KEY no ambiente.", file=sys.stderr)
        return 1

    if not LOGO_PATH.exists():
        print(f"ERRO: logo não encontrado em {LOGO_PATH}", file=sys.stderr)
        return 1

    posts_to_run = POSTS
    if args.only:
        posts_to_run = [p for p in POSTS if p["id"] in args.only]
        if not posts_to_run:
            print(f"ERRO: nenhum post bate com --only {args.only}", file=sys.stderr)
            return 1

    total_slides = sum(len(p["slides"]) for p in posts_to_run)
    print(f"Modelo: {MODEL_ID}")
    print(f"Posts a gerar: {len(posts_to_run)} · Slides totais: {total_slides}")
    if args.recomp_only:
        print("Modo: APENAS overlay PIL nos PNGs já existentes (sem chamar IA).\n")
    else:
        print()

    client = None if args.recomp_only else genai.Client(api_key=api_key)

    count = 0
    success = 0
    failed = []

    for post in posts_to_run:
        post_dir = OUTPUT_ROOT / post["id"]
        post_dir.mkdir(parents=True, exist_ok=True)
        print(f"--- {post['id']} ({len(post['slides'])} slides) ---")

        for slide in post["slides"]:
            count += 1
            output_path = post_dir / f"{slide['name']}.png"
            label = f"  [{count}/{total_slides}] {slide['name']}.png"

            if args.recomp_only:
                if not output_path.exists():
                    print(f"{label}  SKIP (não existe ainda)")
                    continue
                try:
                    composite_footer(output_path, slide.get("bg", "dark"))
                    print(f"{label}  OVERLAY OK")
                    success += 1
                except Exception as exc:  # noqa: BLE001
                    print(f"{label}  ERRO overlay: {exc!s:.200}")
                    failed.append(slide["name"])
                continue

            if args.skip_existing and output_path.exists():
                print(f"{label}  (skip — já existe)")
                success += 1
                continue

            attempt = 0
            max_attempts = 3
            generated_ok = False
            while attempt < max_attempts:
                attempt += 1
                try:
                    response = client.models.generate_content(
                        model=MODEL_ID,
                        contents=[slide["prompt"]],
                    )
                    saved = False
                    for part in response.parts:
                        image = part.as_image()
                        if image is not None:
                            image.save(output_path)
                            saved = True
                            break
                    if saved:
                        generated_ok = True
                    else:
                        text = "".join(p.text or "" for p in response.parts)
                        print(f"{label}  AVISO: sem imagem. Texto: {text[:200]!r}")
                        failed.append(slide["name"])
                    break
                except Exception as exc:  # noqa: BLE001
                    msg = str(exc)
                    if "503" in msg or "UNAVAILABLE" in msg or "429" in msg:
                        wait = 8 * attempt
                        print(f"{label}  rate/load (tentativa {attempt}/{max_attempts}). Aguardando {wait}s...")
                        time.sleep(wait)
                        continue
                    print(f"{label}  ERRO: {msg[:200]}")
                    failed.append(slide["name"])
                    break

            if generated_ok:
                try:
                    composite_footer(output_path, slide.get("bg", "dark"))
                    print(f"{label}  OK + overlay")
                    success += 1
                except Exception as exc:  # noqa: BLE001
                    print(f"{label}  IA OK mas overlay falhou: {exc!s:.200}")
                    failed.append(slide["name"])

    print(f"\nResumo: {success}/{total_slides} sucesso.")
    if failed:
        print(f"Falhas: {failed}")
        return 2
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Gera + overlay dos 32 slides cinematográficos Instagram Renegocia.")
    parser.add_argument("--only", nargs="+", default=None,
                        help="Gerar apenas os post-ids listados.")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Pular slides que já têm .png salvo.")
    parser.add_argument("--recomp-only", action="store_true",
                        help="Não chamar a IA. Só refazer o overlay do footer.")
    args = parser.parse_args()
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
