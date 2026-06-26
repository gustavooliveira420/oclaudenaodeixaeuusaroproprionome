#!/usr/bin/env python3
"""Patch V5.1 - corrige bug R$ -> RS nos slides 1 do Post 13 e Post 15.

Estrategia: render "R" + "$" + " 380k" com fontes diferentes ($ em SFNS
porque NewYork.ttf nao tem o glyph) - cosmetica preservada.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pathlib import Path

W, H = 1024, 1024
BG_DEEP   = (13, 53, 48)
BG_FOOTER = (8, 38, 33)
WHITE     = (245, 245, 240)
GOLD      = (200, 169, 106)
BEIGE     = (216, 191, 142)
DIM2      = (185, 195, 188)
ORANGE    = (217, 142, 85)
ROOT = Path.home() / "Documents/GitHub/renegociaconsultoria"
SFNS  = "/System/Library/Fonts/SFNS.ttf"
NY    = "/System/Library/Fonts/NewYork.ttf"
LOGO_PATH = ROOT / "brand-manual/brand/logo-circle.png"


def font(p, s): return ImageFont.truetype(p, s)


def make_logo(size=60):
    raw = Image.open(LOGO_PATH).convert("RGB").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([(0, 0), (size - 1, size - 1)], fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(raw, (0, 0), mask)
    return out


def photo_bg(path, opacity=0.86):
    bg = Image.open(path).convert("RGB")
    w, h = bg.size
    s = min(w, h)
    bg = bg.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))
    bg = bg.resize((W, H), Image.LANCZOS)
    bg = ImageEnhance.Color(bg).enhance(0.45)
    bg = ImageEnhance.Brightness(bg).enhance(0.55)
    bg = bg.filter(ImageFilter.GaussianBlur(1.5))
    overlay = Image.new("RGB", (W, H), BG_DEEP)
    return Image.blend(bg, overlay, opacity)


def add_chrome(im, draw, slide_num, kicker_text, show_swipe=False):
    draw.rectangle([(0, 0), (W, 5)], fill=GOLD)
    footer_h = 120
    draw.rectangle([(0, H - footer_h), (W, H)], fill=BG_FOOTER)
    draw.rectangle([(0, H - footer_h), (W, H - footer_h + 2)], fill=GOLD)
    logo = make_logo(60)
    im.paste(logo, (50, H - footer_h + 30), logo)
    f_b = font(SFNS, 30)
    for ox, oy in [(0,0),(1,0),(0,1),(1,1)]:
        draw.text((128 + ox, H - footer_h + 44 + oy), "RENEGOCIA", font=f_b, fill=WHITE)
    f_h = font(SFNS, 22)
    draw.text((W - 50, H - footer_h + 47), "@renegocia.tributario",
              font=f_h, fill=DIM2, anchor="rm")
    f_k = font(SFNS, 20)
    draw.text((75, 72), f"—   {str(slide_num).zfill(2)}  ·  {kicker_text.upper()}",
              font=f_k, fill=GOLD)
    if show_swipe:
        f_s = font(SFNS, 22)
        draw.text((W - 50, H - footer_h - 22), "→  deslize",
                  font=f_s, fill=ORANGE, anchor="rm")


def title_serif(draw, lines, y0, size, color=WHITE, highlight=None, highlight_color=BEIGE):
    fnt = font(NY, size)
    lh = int(size * 1.10)
    for i, ln in enumerate(lines):
        y = y0 + i * lh
        if highlight and highlight in ln:
            idx = ln.find(highlight)
            before, mid, after = ln[:idx], highlight, ln[idx + len(highlight):]
            x = 75
            for txt, col in [(before, color), (mid, highlight_color), (after, color)]:
                if not txt: continue
                for ox in [0, 1]:
                    draw.text((x + ox, y), txt, font=fnt, fill=col)
                x += draw.textbbox((0, 0), txt, font=fnt)[2]
        else:
            for ox in [0, 1]:
                draw.text((75 + ox, y), ln, font=fnt, fill=color)


def dots_decor(draw, y, count=3, x=75, spacing=18):
    f = font(SFNS, 32)
    for i in range(count):
        draw.text((x + i * spacing, y), "·", font=f, fill=GOLD)


def render_dollar_serif(draw, parts, y, size, color):
    """parts = [('R', NY), ('$ ', SFNS), ('380k', NY)] - mistura fontes,
    porque NewYork nao tem glyph $ (renderiza como S)."""
    fnt_ny = font(NY, size)
    fnt_sf = font(SFNS, int(size * 0.85))  # SFNS um pouco menor pra equilibrar
    x = 75
    for txt, fontname in parts:
        fnt = fnt_ny if fontname == "NY" else fnt_sf
        for ox in [0, 1]:
            draw.text((x + ox, y if fontname == "NY" else y + int(size * 0.05)),
                      txt, font=fnt, fill=color)
        x += draw.textbbox((0, 0), txt, font=fnt)[2]


# ============================================================
# Post 13 - slide 1 capa: "R$ 380k" em serif
# ============================================================
out = ROOT / "instagram-posts/post-13-distribuidora-380k"
im = photo_bg(out / "_bg/bg-capa.jpg", 0.86)
d = ImageDraw.Draw(im)
add_chrome(im, d, 1, "Caso real anonimizado", show_swipe=True)
render_dollar_serif(d, [("R", "NY"), ("$ ", "SFNS"), ("380k", "NY")],
                    y=170, size=130, color=BEIGE)
title_serif(d, ["recuperados em 8 meses."], y0=340, size=40, color=WHITE)
f = font(SFNS, 24)
d.text((75, 430), "Distribuidora de alimentos", font=f, fill=DIM2)
d.text((75, 462), "18 anos de mercado · Sorocaba · Lucro Real", font=f, fill=DIM2)
dots_decor(d, 530)
im.save(out / "slide-1-capa.png")
print("Patched Post 13 slide-1-capa.png")


# ============================================================
# Post 15 - slide 1 capa: "R$ 200k em creditos" em serif
# ============================================================
out = ROOT / "instagram-posts/post-15-diagnostico-45min"
im = photo_bg(out / "_bg/bg-capa.jpg", 0.84)
d = ImageDraw.Draw(im)
add_chrome(im, d, 1, "Bastidores Renegocia", show_swipe=True)
title_serif(d, ["45 minutos."], y0=180, size=92,
            highlight="45 minutos.", highlight_color=BEIGE)
# "Como identificamos" - linha 1 limpa em serif
title_serif(d, ["Como identificamos"], y0=340, size=44, color=WHITE)
# "R$ 200k em creditos." - linha 2 com mistura de fontes
render_dollar_serif(d, [("R", "NY"), ("$ ", "SFNS"), ("200k em creditos.", "NY")],
                    y=395, size=44, color=WHITE)
dots_decor(d, 500)
f = font(SFNS, 24)
d.text((75, 560), "Diagnostico consultivo passo a passo.", font=f, fill=DIM2)
im.save(out / "slide-1-capa.png")
print("Patched Post 15 slide-1-capa.png")
print()
print("V5.1 patch concluido - bug R$ corrigido nos 2 slides afetados.")
