"""
Gera os 32 slides da estreia do Instagram da Renegocia
via Gemini 3.1 Flash Image Preview (Nano Banana 2).

Organiza em pastas por post:
    instagram-posts/post-X-nome/slide-N-descricao.png

Uso:
    GEMINI_API_KEY=AIzaSy... python scripts/gen_all_posts.py
    GEMINI_API_KEY=... python scripts/gen_all_posts.py --only post-2-como-funciona
    GEMINI_API_KEY=... python scripts/gen_all_posts.py --skip-existing
"""

import argparse
import os
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGO_PATH = PROJECT_ROOT / "brand-manual" / "brand" / "logo-circle.png"
OUTPUT_ROOT = PROJECT_ROOT / "instagram-posts"
HANDLE = "@renegocia.tributario"

MODEL_ID = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-3.1-flash-image-preview")

BRAND_SPEC = f"""=== CRITICAL RENDERING RULE — READ FIRST ===
The ONLY visible text on the image is what appears INSIDE QUOTES below the "TEXT CONTENT" markers in this prompt. NEVER render any specification metadata (e.g. "weight 400", "opacity 0.55", "font-size 12px", "letter-spacing 0.32em", "size ~22px", color names, hex codes, "left-aligned", layout descriptions) as visible text on the image. Specifications describe HOW to render — they are NOT what to render.

=== BRAND ===
Renegocia Consultoria Prime — Brazilian tax consultancy. Aesthetic: premium private bank or whiskey ad. Editorial, restrained, confident. NEVER busy or salesy.

=== COLOR PALETTE (use these hex codes, no approximations) ===
- Deep forest green #0F2F2A (primary dark background)
- Warm off-white #F7F6F2 (primary text color on dark backgrounds; cream alternative background)
- Metallic gold #D4AF37 (eyebrow labels, single-word accents, dividers — NEVER whole paragraphs)
- Emerald green #16B98A (rare positive accent for checks/success only)

=== TYPOGRAPHY ===
Use Montserrat or any clean geometric sans-serif. Headlines extra-bold (weight 800). Eyebrow labels semibold (weight 600), uppercase, with very wide letter-spacing. Body text medium (weight 500).

=== FOOTER (always present, near bottom edge of canvas) ===
The footer has TWO elements separated horizontally:

LEFT element of footer:
- Render a small circular gold-rimmed seal/logo (about 44 pixels diameter) containing a stylized "R" letterform inside.
- Immediately to the right of that seal, render the wordmark with these EXACT characters and nothing else:
  TEXT CONTENT (render exactly): RENEGOCIA
- Style for that wordmark: same color as primary text on this slide, bold, uppercase, with wide letter-spacing.

RIGHT element of footer:
- Render only these characters and nothing else:
  TEXT CONTENT (render exactly): {HANDLE}
- Style for that handle: same color as primary text, regular weight, small, slightly transparent.

DO NOT render any other text in the footer beyond "RENEGOCIA" (left) and "{HANDLE}" (right). DO NOT render words like "weight", "size", "opacity", "font", or any numeric pixel values anywhere on the image.

=== HARD RULES ===
- NO photos of money, people, buildings, or office desks.
- NO decorative gradients (except subtle dark→darker on CTA slides).
- NO drop shadows on text. NO emojis.
- Generous whitespace. Headlines must breathe.
- Portuguese diacritics (ã, ç, õ, é, á, í) must render correctly with sharp edges.
- Square 1:1 Instagram format, ready to publish."""

# ─────────────────────────────────────────────────────────────────────
#  POST DEFINITIONS — 32 slides total
# ─────────────────────────────────────────────────────────────────────

POSTS = [
    {
        "id": "post-1-manifesto",
        "slides": [
            {
                "name": "slide-1-manifesto",
                "use_logo": True,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Single static post (no carousel).
BACKGROUND: solid deep forest green #0F2F2A filling 100% of canvas.

LAYOUT:
1. TOP-LEFT eyebrow (~50px from edges): "— MANIFESTO" in gold #D4AF37, uppercase, weight 600, size ~22px, letter-spacing 0.32em. Prefix with short gold dash "—".

2. CENTER-LEFT headline (vertically centered, left-aligned, fills middle of canvas):
   Four-line headline, font-size ~78px, line-height 1.02, letter-spacing -0.02em:
     Line 1: "Sua empresa pode" — off-white #F7F6F2
     Line 2: "estar pagando" — off-white #F7F6F2
     Line 3: "imposto que ela" — off-white #F7F6F2
     Line 4: "não deve." — METALLIC GOLD #D4AF37

3. BELOW HEADLINE (~40px gap), subheadline: "A Renegocia recupera o que o fisco cobrou a mais." in off-white #F7F6F2, weight 500, size ~26px, opacity 0.85.

4. FOOTER as specified in BRAND SPEC.

The composition should feel like a Wall Street Journal full-page ad. The provided logo image is the actual Renegocia brand seal — use it as visual reference for the footer R-mark only (small, ~44px)."""
            }
        ],
    },
    {
        "id": "post-2-como-funciona",
        "slides": [
            {
                "name": "slide-1-capa",
                "use_logo": True,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel cover slide (1 of 5). Same dark background #0F2F2A.

LAYOUT:
1. TOP-LEFT eyebrow: "— COMO FUNCIONA" in gold #D4AF37, weight 600, size ~22px, letter-spacing 0.32em.
2. CENTER headline (left-aligned, vertically centered), font-size ~84px, line-height 0.98, weight 800, in off-white #F7F6F2:
     Line 1: "Como a Renegocia"
     Line 2: "recupera imposto"
     Line 3: "pago a mais."
3. Small "↦ deslize" hint at bottom-right above footer, in gold opacity 0.6, size 16px, with arrow glyph.
4. FOOTER as specified."""
            },
            {
                "name": "slide-2-diagnostico",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel slide 2 of 5. Background dark green #0F2F2A.

LAYOUT (left-aligned):
1. TOP-LEFT: huge numeral "1" in gold #D4AF37, font-size ~280px, weight 800, line-height 1, occupying upper-left quadrant.
2. TO THE RIGHT of the "1", aligned to its baseline middle: label "DIAGNÓSTICO CONSULTIVO" in gold #D4AF37, weight 600, uppercase, letter-spacing 0.32em, size ~24px.
3. CENTER-LEFT (below the numeral): body text in off-white #F7F6F2, weight 500, size ~36px, line-height 1.35, max-width 70% of canvas:
   "30 a 45 minutos. A gente olha os tributos da sua empresa e identifica onde tem oportunidade."
4. FOOTER as specified. NO LOGO IMAGE PROVIDED — render footer R-mark from text/spec alone."""
            },
            {
                "name": "slide-3-proposta",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel slide 3 of 5. Background dark green #0F2F2A.

LAYOUT (left-aligned):
1. TOP-LEFT: huge numeral "2" in gold #D4AF37, font-size ~280px, weight 800.
2. Label "PROPOSTA EM 72H" in gold, uppercase, letter-spacing 0.32em, size ~24px, to the right of the "2".
3. CENTER-LEFT body text in off-white, weight 500, size ~36px, max-width 70%:
   "Recebe um relatório com o valor estimado a recuperar, prazo e quanto custa o serviço."
4. FOOTER as specified."""
            },
            {
                "name": "slide-4-execucao",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel slide 4 of 5. Background dark green #0F2F2A.

LAYOUT (left-aligned):
1. TOP-LEFT: huge numeral "3" in gold #D4AF37, font-size ~280px, weight 800.
2. Label "EXECUÇÃO" in gold, uppercase, letter-spacing 0.32em, size ~24px.
3. Body text in off-white, weight 500, size ~36px, max-width 70%:
   "A gente cuida de tudo — administrativo ou judicial. Você só recebe atualizações."
4. FOOTER as specified."""
            },
            {
                "name": "slide-5-risco-compartilhado",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel CTA slide 5 of 5. Background: subtle gradient from #0F2F2A to #143b34 (top-left to bottom-right).

LAYOUT (left-aligned):
1. TOP-LEFT: huge numeral "4" in gold #D4AF37, font-size ~280px, weight 800.
2. Label "RISCO COMPARTILHADO" in gold, uppercase, letter-spacing 0.32em, size ~24px.
3. Body text in off-white, weight 500, size ~34px, max-width 75%:
   "Você paga uma parte na contratação. O restante dos honorários só vence quando seu crédito tributário é reconhecido."
4. FOOTER as specified."""
            },
        ],
    },
    {
        "id": "post-3-o-que-recuperamos",
        "slides": [
            {
                "name": "slide-1-capa",
                "use_logo": True,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel cover slide (1 of 6). Background dark green #0F2F2A.

LAYOUT:
1. TOP-LEFT eyebrow: "— O QUE RECUPERAMOS" in gold, weight 600, size ~22px, letter-spacing 0.32em.
2. CENTER headline (left-aligned), font-size ~96px, line-height 0.96, weight 800, off-white:
     "O que a Renegocia"
     "recupera."
3. Small "↦ deslize" hint at bottom-right above footer in gold opacity 0.6.
4. FOOTER as specified. Use the provided logo for the footer R-mark."""
            },
            {
                "name": "slide-2-pis-cofins",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel slide 2 of 6. Background CREAM #F7F6F2 with text in deep green #0F2F2A.

LAYOUT (centered vertically, left-aligned content):
1. TOP-LEFT eyebrow "01 · PIS / COFINS" in gold #D4AF37, weight 600, letter-spacing 0.32em, size ~22px.
2. Headline below eyebrow, font-size ~64px, line-height 1.02, weight 800, in deep green #0F2F2A:
     "PIS e COFINS"
     "pagos a mais"
3. Body text below headline (~30px gap), in deep green #0F2F2A weight 500, size ~28px:
   "Em vendas, insumos, ICMS na base."
4. FOOTER as specified, but text color is deep green #0F2F2A (since background is cream)."""
            },
            {
                "name": "slide-3-irpj-csll",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel slide 3 of 6. Background dark green #0F2F2A.

LAYOUT:
1. TOP-LEFT eyebrow "02 · IRPJ / CSLL" in gold, weight 600, letter-spacing 0.32em, size ~22px.
2. Headline below, font-size ~58px, weight 800, off-white:
     "IRPJ e CSLL"
     "sobre incentivos."
3. Body text in off-white opacity 0.85, weight 500, size ~28px, max-width 75%:
   "Se sua empresa tem benefício fiscal estadual, pode estar pagando IR sobre ele. Não deveria."
4. FOOTER as specified."""
            },
            {
                "name": "slide-4-inss",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel slide 4 of 6. Background CREAM #F7F6F2 with text in deep green.

LAYOUT:
1. TOP-LEFT eyebrow "03 · INSS" in gold, weight 600, letter-spacing 0.32em, size ~22px.
2. Headline, font-size ~58px, weight 800, deep green:
     "INSS sobre folha"
     "de pagamento."
3. Body in deep green weight 500, size ~28px, max-width 80%:
   "Verbas indenizatórias (aviso, PLR, auxílios) não entram na base. Muita empresa paga assim mesmo."
4. FOOTER as specified, text in deep green."""
            },
            {
                "name": "slide-5-icms",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel slide 5 of 6. Background dark green #0F2F2A.

LAYOUT:
1. TOP-LEFT eyebrow "04 · ICMS" in gold, weight 600, letter-spacing 0.32em, size ~22px.
2. Headline, font-size ~64px, weight 800, off-white:
     "ICMS pago"
     "a mais."
3. Body in off-white weight 500 opacity 0.85, size ~28px, max-width 80%:
   "Substituição tributária, energia, telecomunicações. Recuperação direta nos próximos 5 anos."
4. FOOTER as specified."""
            },
            {
                "name": "slide-6-cta",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel CTA slide 6 of 6. Background: gradient #0F2F2A to #143b34.

LAYOUT (vertically centered, left-aligned):
1. CENTER headline, font-size ~62px, weight 800, line-height 1.02, off-white:
     "Quer saber qual"
     "se aplica à"
     "sua empresa?"
2. Below headline (~40px gap), CTA line in gold #D4AF37, weight 700, size ~28px:
   "Diagnóstico consultivo no link da bio →"
3. FOOTER as specified."""
            },
        ],
    },
    {
        "id": "post-4-icms-base-pis-cofins",
        "slides": [
            {
                "name": "slide-1-hook",
                "use_logo": True,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel cover/hook slide (1 of 6). Background dark green #0F2F2A.

LAYOUT:
1. TOP-LEFT eyebrow "— TESE DO SÉCULO" in gold, weight 600, letter-spacing 0.32em, size ~22px.
2. CENTER headline, font-size ~70px, weight 800, line-height 1.0, off-white with one accent:
     Line 1: "Sua empresa pode" (off-white)
     Line 2: "ter pago ICMS dentro" (off-white)
     Line 3: "de outro imposto" (off-white)
     Line 4: "— por 25 anos." (METALLIC GOLD #D4AF37)
3. Small "↦ deslize" hint at bottom-right above footer in gold opacity 0.6.
4. FOOTER as specified. Use the provided logo for the footer R-mark."""
            },
            {
                "name": "slide-2-problema",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel slide 2 of 6. Background CREAM #F7F6F2 with text in deep green.

LAYOUT:
1. TOP-LEFT eyebrow "02 · O PROBLEMA" in gold, weight 600, letter-spacing 0.32em, size ~22px.
2. Body text, weight 600, size ~38px, line-height 1.3, deep green #0F2F2A, max-width 85%:
   "Por décadas, o fisco cobrou PIS e COFINS sobre o valor total da nota — incluindo o ICMS já cobrado pelo estado."
3. Below (~40px gap), highlighted phrase in deep green weight 800 size ~42px:
   "Resultado: você pagava imposto sobre imposto."
4. FOOTER as specified, text in deep green."""
            },
            {
                "name": "slide-3-stf-decidiu",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel slide 3 of 6. Background dark green #0F2F2A.

LAYOUT (centered):
1. TOP-LEFT eyebrow "03 · O QUE MUDOU" in gold, weight 600, letter-spacing 0.32em, size ~22px.
2. CENTER headline (vertically centered, left-aligned), font-size ~82px, weight 800, line-height 1.02:
     Line 1: "Em 2017, o STF" (off-white)
     Line 2: "disse: não pode." (METALLIC GOLD #D4AF37)
3. Below headline (~50px gap), tag-style label in off-white opacity 0.7, weight 600, letter-spacing 0.18em, size ~22px:
   "TEMA 69 · DECISÃO DEFINITIVA"
4. FOOTER as specified."""
            },
            {
                "name": "slide-4-significado",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel slide 4 of 6. Background dark green #0F2F2A.

LAYOUT:
1. TOP-LEFT eyebrow "04 · O QUE ISSO SIGNIFICA" in gold, weight 600, letter-spacing 0.32em, size ~22px.
2. Headline left-aligned, font-size ~60px, weight 800, line-height 1.05, off-white:
     "O que isso significa"
     "pra sua empresa?"
3. Body text below, weight 500, size ~32px, off-white opacity 0.85, max-width 85%:
   "Tudo que foi pago a mais nos últimos 5 anos pode voltar. Com correção."
4. FOOTER as specified."""
            },
            {
                "name": "slide-5-quanto-da",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel slide 5 of 6. Background CREAM #F7F6F2 with text in deep green.

LAYOUT (centered, premium financial-report look):
1. TOP-LEFT eyebrow "05 · QUANTO DÁ?" in gold #D4AF37, weight 600, letter-spacing 0.32em, size ~22px.
2. CENTER (vertically centered): two stacked stats with hairline gold rule between them.
   Stat 1: big number "R$ 50K — R$ 200K" in deep green #0F2F2A, weight 800, size ~76px, letter-spacing -0.02em. Label below in deep green weight 500 size ~22px opacity 0.7: "empresas de médio porte recuperam, em média"
   Hairline gold rule, 60% width, 1px height.
   Stat 2: smaller stat "muito mais" in gold #D4AF37 weight 800 size ~48px italic. Label below in deep green weight 500 size ~22px opacity 0.7: "indústrias e distribuidoras"
3. FOOTER as specified, text in deep green."""
            },
            {
                "name": "slide-6-cta",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel CTA slide 6 of 6. Background: gradient #0F2F2A to #143b34.

LAYOUT (vertically centered):
1. CENTER headline, font-size ~58px, weight 800, line-height 1.05, off-white:
     "A Renegocia faz"
     "esse cálculo no"
     "diagnóstico consultivo"
     "de 45 minutos."
2. Below (~40px gap), CTA line in gold #D4AF37 weight 700 size ~28px:
   "Link na bio →"
3. FOOTER as specified."""
            },
        ],
    },
    {
        "id": "post-5-pergunta",
        "slides": [
            {
                "name": "slide-1-pergunta",
                "use_logo": True,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Single static post. Background CREAM #F7F6F2 with text in deep green.

LAYOUT (centered, magazine cover feel):
1. TOP-LEFT eyebrow "— PORTFÓLIO" in gold #D4AF37, weight 600, letter-spacing 0.32em, size ~22px.
2. CENTER (vertically centered), headline left-aligned, font-size ~70px, weight 800, line-height 1.02, deep green #0F2F2A:
     Line 1: "Sua empresa já"
     Line 2: "analisou quantas"
     Line 3: "teses tributárias?"
3. Below (~40px gap), smaller line in deep green weight 500 size ~30px opacity 0.65:
   "A maioria nunca analisou nenhuma."
4. Number "15+" floating large in bottom-right area (above footer, ~40% canvas size), in gold #D4AF37 with subtle opacity 0.15, weight 800 size ~340px — pure decorative bg element behind text.
5. FOOTER as specified, text in deep green. Use provided logo for footer R-mark."""
            }
        ],
    },
    {
        "id": "post-6-incentivos-icms",
        "slides": [
            {
                "name": "slide-1-hook",
                "use_logo": True,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel cover (1 of 5). Background dark green #0F2F2A.

LAYOUT:
1. TOP-LEFT eyebrow "— TEMA 1.182 STJ" in gold, weight 600, letter-spacing 0.32em, size ~22px.
2. CENTER headline left-aligned, font-size ~64px, weight 800, line-height 1.02:
     Line 1: "Sua empresa tem" (off-white)
     Line 2: "benefício fiscal do estado?" (off-white)
     Line 3: "Pode estar pagando IR sobre ele." (METALLIC GOLD #D4AF37, smaller size ~46px)
3. Small "↦ deslize" hint at bottom-right above footer in gold opacity 0.6.
4. FOOTER as specified. Use the provided logo for the footer R-mark."""
            },
            {
                "name": "slide-2-quem-tem",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel slide 2 of 5. Background CREAM #F7F6F2 with text in deep green.

LAYOUT:
1. TOP-LEFT eyebrow "02 · QUEM TEM" in gold, weight 600, letter-spacing 0.32em, size ~22px.
2. Headline, font-size ~52px, weight 800, line-height 1.05, deep green:
     "Muitas indústrias e"
     "agroindústrias têm:"
3. Below headline, three line items in deep green weight 600 size ~38px, line-height 1.4, each prefixed with a gold em-dash "—":
     "— Redução de ICMS"
     "— Crédito presumido"
     "— Diferimento"
4. Below items (~30px gap), small line in deep green weight 500 size ~24px opacity 0.7:
   "Por decreto estadual."
5. FOOTER as specified, text in deep green."""
            },
            {
                "name": "slide-3-fisco-cobrava",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel slide 3 of 5. Background dark green #0F2F2A.

LAYOUT:
1. TOP-LEFT eyebrow "03 · O QUE O FISCO FAZIA" in gold, weight 600, letter-spacing 0.32em, size ~22px.
2. Headline left-aligned, font-size ~58px, weight 800, line-height 1.02, off-white:
     "O fisco federal vinha"
     "cobrando IRPJ e CSLL"
     "sobre esse benefício."
3. Below (~40px gap), small framed quote in gold #D4AF37 italic weight 600 size ~36px:
     "Como se fosse \\"renda\\"."
4. FOOTER as specified."""
            },
            {
                "name": "slide-4-stj-pacificou",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel slide 4 of 5. Background dark green #0F2F2A.

LAYOUT (centered, dramatic):
1. TOP-LEFT eyebrow "04 · O QUE MUDOU" in gold, weight 600, letter-spacing 0.32em, size ~22px.
2. CENTER headline (vertically centered, left-aligned), font-size ~72px, weight 800, line-height 1.02:
     Line 1: "Em 2023, o STJ" (off-white)
     Line 2: "pacificou:" (off-white)
     Line 3: "não é renda." (METALLIC GOLD #D4AF37)
3. Below headline (~40px gap), tag-style label in off-white opacity 0.7, weight 600, letter-spacing 0.18em, size ~22px:
   "TEMA 1.182 · IMPOSTO PAGO A MAIS PODE SER RECUPERADO"
4. FOOTER as specified."""
            },
            {
                "name": "slide-5-cta",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel CTA slide 5 of 5. Background: gradient #0F2F2A to #143b34.

LAYOUT (vertically centered):
1. CENTER headline, font-size ~72px, weight 800, line-height 1.02, off-white:
     "Tem incentivo estadual?"
     "Vale o diagnóstico."
2. Below (~40px gap), CTA line in gold #D4AF37 weight 700 size ~28px:
   "Link na bio →"
3. FOOTER as specified."""
            },
        ],
    },
    {
        "id": "post-7-case-142k",
        "slides": [
            {
                "name": "slide-1-case",
                "use_logo": True,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Single static post (case study / proof). Background CREAM #F7F6F2 with deep green text. Visual feels like a discreet auditor's report.

LAYOUT (centered vertically):
1. TOP-LEFT eyebrow "— CASO REAL" in gold #D4AF37, weight 600, letter-spacing 0.32em, size ~22px.

2. CENTER (vertically centered): hero number "R$ 142 MIL" in deep green #0F2F2A, weight 800, size ~160px, letter-spacing -0.03em, line-height 1.

3. Below the number (~30px gap), descriptive text in deep green weight 500, size ~26px, line-height 1.35, max-width 75%, opacity 0.8:
   "recuperáveis identificados em 1 diagnóstico de 45 minutos."

4. Below the description (~40px gap), thin gold horizontal rule (60% width, 1px high).

5. Below the rule, meta-info in deep green weight 600, letter-spacing 0.18em, uppercase, size ~16px, opacity 0.65:
   "AUTO POSTO · SP · 2026"

6. FOOTER as specified, text in deep green. Use the provided logo for the footer R-mark."""
            }
        ],
    },
    {
        "id": "post-8-inss-folha",
        "slides": [
            {
                "name": "slide-1-hook",
                "use_logo": True,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel cover (1 of 6). Background dark green #0F2F2A.

LAYOUT:
1. TOP-LEFT eyebrow "— INSS SOBRE FOLHA" in gold, weight 600, letter-spacing 0.32em, size ~22px.
2. CENTER (vertically centered, left-aligned):
   THREE STACKED TAGS in gold #D4AF37 weight 800 size ~52px italic, each on its own line, with small gold dot before each:
     "· Aviso prévio."
     "· PLR."
     "· Auxílio-creche."
3. Below the tags (~50px gap), question in off-white weight 800 size ~46px line-height 1.1:
   "Sua empresa paga INSS"
   "sobre tudo isso?"
4. Small "↦ deslize" hint at bottom-right above footer in gold opacity 0.6.
5. FOOTER as specified. Use the provided logo for the footer R-mark."""
            },
            {
                "name": "slide-2-regra",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel slide 2 of 6. Background CREAM #F7F6F2 with text in deep green.

LAYOUT (centered):
1. TOP-LEFT eyebrow "02 · A REGRA" in gold, weight 600, letter-spacing 0.32em, size ~22px.
2. CENTER headline (vertically centered, left-aligned), font-size ~64px, weight 800, line-height 1.02, deep green:
     Line 1: "O INSS incide"
     Line 2: "sobre o salário."
3. Below (~40px gap), counter-statement in gold #D4AF37 weight 800 size ~48px:
   "Não sobre verbas que não são salário."
4. FOOTER as specified, text in deep green."""
            },
            {
                "name": "slide-3-sistema",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel slide 3 of 6. Background dark green #0F2F2A.

LAYOUT:
1. TOP-LEFT eyebrow "03 · O QUE ACONTECE" in gold, weight 600, letter-spacing 0.32em, size ~22px.
2. Headline left-aligned, font-size ~58px, weight 800, line-height 1.05, off-white:
     "Mas o sistema da folha"
     "calcula sobre quase tudo."
3. Below (~40px gap), italic supporting line in off-white opacity 0.8 weight 500 size ~32px:
   "E o STJ já disse, em várias súmulas, que não é assim."
4. FOOTER as specified."""
            },
            {
                "name": "slide-4-checklist",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel slide 4 of 6. Background CREAM #F7F6F2 with deep green text.

LAYOUT:
1. TOP-LEFT eyebrow "04 · O QUE ENTRA NA RECUPERAÇÃO" in gold, weight 600, letter-spacing 0.28em, size ~20px.
2. Below (centered vertically, left-aligned), checklist of 4 items in deep green weight 600 size ~38px line-height 1.45, each prefixed with a small gold check "✓":
     "✓ Aviso prévio indenizado"
     "✓ Terço de férias"
     "✓ PLR"
     "✓ Auxílio-creche, auxílio-doença, vale-transporte em pecúnia"
3. FOOTER as specified, text in deep green."""
            },
            {
                "name": "slide-5-quanto",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel slide 5 of 6. Background dark green #0F2F2A.

LAYOUT (centered, stat-card style):
1. TOP-LEFT eyebrow "05 · QUANTO PODE VOLTAR?" in gold, weight 600, letter-spacing 0.32em, size ~22px.
2. CENTER (vertically centered, left-aligned): big number "R$ 50K — R$ 300K" in off-white #F7F6F2 weight 800 size ~80px letter-spacing -0.02em line-height 1.
3. Below number (~24px gap), context in off-white opacity 0.75 weight 500 size ~26px line-height 1.4 max-width 80%:
   "recuperáveis em 5 anos, em empresas com folha acima de R$ 100k/mês."
4. FOOTER as specified."""
            },
            {
                "name": "slide-6-cta",
                "use_logo": False,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Carousel CTA slide 6 of 6. Background: gradient #0F2F2A to #143b34.

LAYOUT (vertically centered):
1. CENTER headline, font-size ~64px, weight 800, line-height 1.02, off-white:
     "Sua folha tem"
     "essas verbas?"
     "Faz sentido olhar."
2. Below (~40px gap), CTA line in gold #D4AF37 weight 700 size ~28px:
   "Link na bio →"
3. FOOTER as specified."""
            },
        ],
    },
    {
        "id": "post-9-cta-institucional",
        "slides": [
            {
                "name": "slide-1-cta",
                "use_logo": True,
                "prompt": f"""{BRAND_SPEC}

POST TYPE: Single static post (institutional close). Background dark green #0F2F2A with subtle radial gradient brighter at top-left (#143b34 fading into #0F2F2A).

LAYOUT (vertically centered, left-aligned):
1. TOP-LEFT eyebrow "— O COMPROMISSO" in gold #D4AF37, weight 600, letter-spacing 0.32em, size ~22px.

2. CENTER (vertically centered), three lines of headline in different treatments, font-size ~46px, line-height 1.4:
   Line 1, off-white #F7F6F2 weight 700: "Diagnóstico consultivo em 45 minutos."
   Line 2, off-white opacity 0.7 weight 500: "Se não houver oportunidade, dizemos."
   Line 3, gold #D4AF37 weight 700: "Se houver, você paga uma parte na contratação e o restante quando seu crédito é reconhecido."

3. FOOTER as specified. Use the provided logo for the footer R-mark."""
            }
        ],
    },
]


def run(args: argparse.Namespace) -> int:
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERRO: defina GEMINI_API_KEY no ambiente.", file=sys.stderr)
        return 1

    if not LOGO_PATH.exists():
        print(f"ERRO: logo não encontrado em {LOGO_PATH}", file=sys.stderr)
        return 1

    with open(LOGO_PATH, "rb") as f:
        logo_bytes = f.read()
    logo_part = types.Part.from_bytes(data=logo_bytes, mime_type="image/png")

    client = genai.Client(api_key=api_key)

    posts_to_run = POSTS
    if args.only:
        posts_to_run = [p for p in POSTS if p["id"] in args.only]
        if not posts_to_run:
            print(f"ERRO: nenhum post bate com --only {args.only}", file=sys.stderr)
            return 1

    total_slides = sum(len(p["slides"]) for p in posts_to_run)
    print(f"Modelo: {MODEL_ID}")
    print(f"Posts a gerar: {len(posts_to_run)} · Slides totais: {total_slides}\n")

    count = 0
    success = 0
    failed = []

    for post in posts_to_run:
        post_dir = OUTPUT_ROOT / post["id"]
        post_dir.mkdir(parents=True, exist_ok=True)
        print(f"─── {post['id']} ({len(post['slides'])} slides) ───")

        for slide in post["slides"]:
            count += 1
            output_path = post_dir / f"{slide['name']}.png"
            label = f"  [{count}/{total_slides}] {slide['name']}.png"

            if args.skip_existing and output_path.exists():
                print(f"{label}  (skip — já existe)")
                success += 1
                continue

            contents = [slide["prompt"]]
            if slide.get("use_logo"):
                contents.append(logo_part)

            attempt = 0
            max_attempts = 3
            while attempt < max_attempts:
                attempt += 1
                try:
                    response = client.models.generate_content(
                        model=MODEL_ID,
                        contents=contents,
                    )
                    saved = False
                    for part in response.parts:
                        image = part.as_image()
                        if image is not None:
                            image.save(output_path)
                            saved = True
                            break
                    if saved:
                        print(f"{label}  OK")
                        success += 1
                    else:
                        text = "".join(p.text or "" for p in response.parts)
                        print(f"{label}  AVISO: sem imagem. Texto: {text[:200]!r}")
                        failed.append(slide["name"])
                    break
                except Exception as exc:  # noqa: BLE001
                    msg = str(exc)
                    if "503" in msg or "UNAVAILABLE" in msg or "429" in msg:
                        wait = 8 * attempt
                        print(f"{label}  rate/load (tentativa {attempt}/{max_attempts}). Aguardando {wait}s…")
                        time.sleep(wait)
                        continue
                    print(f"{label}  ERRO: {msg[:200]}")
                    failed.append(slide["name"])
                    break
            else:
                print(f"{label}  ERRO: esgotou tentativas")
                failed.append(slide["name"])

    print(f"\nResumo: {success}/{total_slides} sucesso.")
    if failed:
        print(f"Falhas: {failed}")
        return 2
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Gera todos os slides dos posts de Instagram da Renegocia.")
    parser.add_argument(
        "--only",
        nargs="+",
        default=None,
        help="Gerar apenas os post-ids listados (ex: post-2-como-funciona).",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Pular slides que já têm arquivo .png salvo.",
    )
    args = parser.parse_args()
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
