"""
Gera o Post 1 (Manifesto) do Instagram da Renegocia
via Gemini 3 Pro Image Preview ("Nano Banana Pro").

Uso:
    GEMINI_API_KEY=AIzaSy... python gen_post1_manifesto.py
"""

import os
import sys
from pathlib import Path

from google import genai
from google.genai import types

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGO_PATH = PROJECT_ROOT / "brand-manual" / "brand" / "logo-circle.png"
OUTPUT_DIR = PROJECT_ROOT / "instagram-posts"
OUTPUT_DIR.mkdir(exist_ok=True)

PROMPT = """Generate a premium Instagram post image (1:1 square format, 1080x1080).

BRAND: Renegocia Consultoria Prime — Brazilian tax consultancy. The aesthetic must feel like a high-end whiskey or private bank ad: editorial, restrained, confident, NEVER busy or salesy.

EXACT COLORS (use these hex codes, no approximations):
- Background: solid deep forest green #0F2F2A (filling 100% of the canvas)
- Primary text (headline + subheadline): warm off-white #F7F6F2
- Accent (specific words only): metallic gold #D4AF37
- A very subtle 1px gold hairline detail is acceptable but optional

TYPOGRAPHY: Use Montserrat (or a clean geometric sans-serif if Montserrat unavailable). Headline is weight 800 (Extra Bold). Eyebrow and footer are weight 600.

LAYOUT (strict — follow exactly):

1. TOP-LEFT (eyebrow label, ~50px from edges):
   "— MANIFESTO" in gold #D4AF37, uppercase, weight 600, font-size ~22px, letter-spacing 0.32em. Prefix with a short gold horizontal line "—".

2. CENTER-LEFT (headline, vertically centered, left-aligned, occupies the middle 60% of canvas):
   Two-line headline in font-size ~78px, line-height 1.02, letter-spacing -0.02em:
   Line 1: "Sua empresa pode" — in off-white #F7F6F2
   Line 2: "estar pagando" — in off-white #F7F6F2
   Line 3: "imposto que ela" — in off-white #F7F6F2
   Line 4: "não deve." — in METALLIC GOLD #D4AF37 (only this last line is gold)

3. BELOW HEADLINE (subheadline, ~40px gap):
   "A Renegocia recupera o que o fisco cobrou a mais." — in off-white #F7F6F2, weight 500, font-size ~26px, opacity 0.85.

4. BOTTOM-LEFT (footer, ~50px from bottom edge):
   Small circular gold-rimmed logo (~44px diameter) with a stylized white "R" mark inside, followed by the wordmark "RENEGOCIA" in off-white, weight 700, letter-spacing 0.18em, font-size ~14px.

5. BOTTOM-RIGHT (handle, ~50px from edges, baseline-aligned with the wordmark):
   "@renegocia.consultoria" in off-white #F7F6F2, weight 400, font-size ~12px, opacity 0.55.

STYLE NOTES:
- Generous whitespace. The headline and subheadline must breathe.
- NO decorative elements, NO gradients, NO shadows behind the text, NO photos or illustrations of money/people/buildings.
- The only visual richness is in the typography contrast and the single gold-accented line.
- The composition should feel like a Wall Street Journal full-page ad or a Patek Philippe campaign.
- Pixel-sharp text rendering. All Portuguese characters (ã, ç, õ, é, á) must render correctly with proper diacritics.

LOGO REFERENCE: I am providing the actual Renegocia logo (circular gold-rimmed seal with stylized "R" and "RENEGOCIA / CONSULTORIA PRIME / TRIBUTÁRIO" text). Use it as visual reference for the footer logo, but at small size (~44px) only show the circular mark + the "RENEGOCIA" wordmark next to it. Do NOT include "CONSULTORIA PRIME" or "TRIBUTÁRIO" labels in the footer — those are for the larger seal version only.

Output: square, ready-to-publish Instagram post."""


def main() -> int:
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERRO: defina GEMINI_API_KEY no ambiente.", file=sys.stderr)
        print("Pegue em https://aistudio.google.com/apikey", file=sys.stderr)
        return 1

    if not LOGO_PATH.exists():
        print(f"ERRO: logo não encontrado em {LOGO_PATH}", file=sys.stderr)
        return 1

    client = genai.Client(api_key=api_key)

    with open(LOGO_PATH, "rb") as f:
        logo_bytes = f.read()
    logo_part = types.Part.from_bytes(data=logo_bytes, mime_type="image/png")

    model_id = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-3.1-flash-image-preview")
    print(f"Gerando Post 1 (Manifesto) com {model_id}...")
    print(f"  Logo de ref:  {LOGO_PATH.name}\n")

    response = client.models.generate_content(
        model=model_id,
        contents=[PROMPT, logo_part],
    )

    images_saved = 0
    for part in response.parts:
        if part.text:
            print(f"[texto do modelo]: {part.text}\n")
        image = part.as_image()
        if image is not None:
            images_saved += 1
            output_path = OUTPUT_DIR / f"post-1-manifesto-v{images_saved}.png"
            image.save(output_path)
            print(f"OK -> {output_path}")

    if images_saved == 0:
        print("AVISO: nenhuma imagem retornada. Resposta bruta:", file=sys.stderr)
        print(response, file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
