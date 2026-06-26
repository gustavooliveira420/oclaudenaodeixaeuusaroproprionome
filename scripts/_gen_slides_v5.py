#!/usr/bin/env python3
"""V5 - gera os 23 slides dos 6 posts restantes do bundle W24-W25.

Posts: 12 (Tema 69 mecanica), 13 (Caso R$380k), 14 (ICMS dest/recolh),
       15 (Diagnostico 45min), 16 (Pre-2017), 17 (LC 224/2025).

Mesmo padrao V4: verde-petroleo, fotos tematicas com overlay 85-88%,
logo circular mascarada + RENEGOCIA bold, serif NewYork para titulos
e numeros, kicker numerado, citacao italico, CTA simples.
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
NY_IT = "/System/Library/Fonts/NewYorkItalic.ttf"
LOGO_PATH = ROOT / "brand-manual/brand/logo-circle.png"


def font(p, s): return ImageFont.truetype(p, s)


def make_logo(size=60):
    raw = Image.open(LOGO_PATH).convert("RGB").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([(0, 0), (size - 1, size - 1)], fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(raw, (0, 0), mask)
    return out


def photo_bg(photo_path, opacity_overlay=0.86):
    bg = Image.open(photo_path).convert("RGB")
    w, h = bg.size
    s = min(w, h)
    bg = bg.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))
    bg = bg.resize((W, H), Image.LANCZOS)
    bg = ImageEnhance.Color(bg).enhance(0.45)
    bg = ImageEnhance.Brightness(bg).enhance(0.55)
    bg = bg.filter(ImageFilter.GaussianBlur(1.5))
    overlay = Image.new("RGB", (W, H), BG_DEEP)
    return Image.blend(bg, overlay, opacity_overlay)


def solid_bg(): return Image.new("RGB", (W, H), BG_DEEP)


def wrap(draw, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textbbox((0, 0), t, font=fnt)[2] <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def add_chrome(im, draw, slide_num, kicker_text, show_swipe=False):
    draw.rectangle([(0, 0), (W, 5)], fill=GOLD)
    footer_h = 120
    draw.rectangle([(0, H - footer_h), (W, H)], fill=BG_FOOTER)
    draw.rectangle([(0, H - footer_h), (W, H - footer_h + 2)], fill=GOLD)
    logo = make_logo(60)
    logo_x, logo_y = 50, H - footer_h + 30
    im.paste(logo, (logo_x, logo_y), logo)
    f_brand = font(SFNS, 30)
    bx, by = logo_x + 78, logo_y + 14
    for ox, oy in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        draw.text((bx + ox, by + oy), "RENEGOCIA", font=f_brand, fill=WHITE)
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


def numbered_serif(draw, num, title_txt, desc, y, x_num=75):
    f_n = font(NY, 90)
    f_t = font(NY, 34)
    f_d = font(SFNS, 24)
    for ox in [0, 1]:
        draw.text((x_num + ox, y - 10), str(num), font=f_n, fill=GOLD)
    for ox in [0, 1]:
        draw.text((x_num + 100 + ox, y + 25), title_txt, font=f_t, fill=WHITE)
    lines = wrap(draw, desc, f_d, W - x_num - 100 - 75)
    for i, ln in enumerate(lines):
        draw.text((x_num + 100, y + 75 + i * 30), ln, font=f_d, fill=DIM2)
    return y + 75 + len(lines) * 30 + 22


def bullet(draw, text, y, size=28, x=100):
    f = font(SFNS, size)
    draw.rectangle([(x - 28, y + 10), (x - 14, y + 24)], fill=GOLD)
    lines = wrap(draw, text, f, W - x - 90)
    for i, ln in enumerate(lines):
        draw.text((x, y + i * int(size * 1.18)), ln, font=f, fill=WHITE)
    return y + len(lines) * int(size * 1.18) + 14


def cta_simple(draw, text, y, color=GOLD, size=46):
    f_t = font(NY, size)
    f_a = font(SFNS, size)
    for ox in [0, 1]:
        draw.text((75 + ox, y), text, font=f_t, fill=color)
    tw = draw.textbbox((0, 0), text, font=f_t)[2]
    for ox in [0, 1]:
        draw.text((75 + tw + 20 + ox, y + 4), "→", font=f_a, fill=color)


def dots_decor(draw, y, count=3, x_start=75, spacing=18):
    f = font(SFNS, 32)
    x = x_start
    for _ in range(count):
        draw.text((x, y), "·", font=f, fill=GOLD)
        x += spacing


def quote_italic(draw, text, y, color=GOLD, size=24, x=75):
    f = font(NY_IT, size)
    lines = wrap(draw, text, f, W - x - 75)
    for i, ln in enumerate(lines):
        draw.text((x, y + i * int(size * 1.3)), ln, font=f, fill=color)
    return y + len(lines) * int(size * 1.3) + 10


# ============================================================
# POST 12 — TESE — Tema 69 mecanica
# ============================================================
out = ROOT / "instagram-posts/post-12-tema69-mecanica"

im = photo_bg(out / "_bg/bg-capa.jpg", 0.86)
d = ImageDraw.Draw(im)
add_chrome(im, d, 1, "Tese do seculo", show_swipe=True)
title_serif(d, ["Por que o ICMS", "sai da base do", "PIS/COFINS."],
            y0=170, size=70, highlight="sai da base do", highlight_color=BEIGE)
f = font(SFNS, 26)
d.text((75, 540), "STF Tema 69 - 9 anos depois,", font=f, fill=DIM2)
d.text((75, 575), "ainda paga recuperacao retroativa.", font=f, fill=DIM2)
dots_decor(d, 630)
im.save(out / "slide-1-capa.png")

im = solid_bg(); d = ImageDraw.Draw(im)
add_chrome(im, d, 2, "A logica", show_swipe=True)
title_serif(d, ["Receita nao e", "tributo."], y0=160, size=68,
            highlight="tributo.", highlight_color=BEIGE)
quote_italic(d, '"PIS e COFINS incidem sobre faturamento (CF art. 195, I, b)."', y=330)
y = 410
y = bullet(d, "ICMS e tributo cobrado em nome do estado.", y, size=28)
y = bullet(d, "Nao e receita da empresa - apenas transita.", y, size=28)
y = bullet(d, "Tributar tributo = bitributacao indevida.", y, size=28)
y = bullet(d, "STF cravou em 15/03/2017 (RE 574.706).", y, size=28)
im.save(out / "slide-2-logica.png")

im = solid_bg(); d = ImageDraw.Draw(im)
add_chrome(im, d, 3, "Modulacao", show_swipe=True)
title_serif(d, ["Linha do tempo."], y0=160, size=64)
y = 320
y = numbered_serif(d, 1, "Mar/2017",
    "STF fixa a tese - RE 574.706, repercussao geral Tema 69.", y)
y = numbered_serif(d, 2, "Mai/2021",
    "Modulacao: efeitos a partir de 15/03/2017 (ressalvadas acoes anteriores).", y)
y = numbered_serif(d, 3, "Hoje (2026)",
    "Empresas pre-2017 ainda recuperam 5 anos corrigidos pela Selic.", y)
im.save(out / "slide-3-timeline.png")

im = solid_bg(); d = ImageDraw.Draw(im)
add_chrome(im, d, 4, "Voce tem direito?", show_swipe=True)
title_serif(d, ["3 perguntas."], y0=160, size=64)
y = 330
y = bullet(d, "Apura PIS/COFINS em Lucro Presumido ou Real?", y, size=30)
y = bullet(d, "Vende mercadoria tributada por ICMS?", y, size=30)
y = bullet(d, "Existe desde antes de 15/03/2017?", y, size=30)
f = font(NY_IT, 28)
d.text((75, y + 40), "3 sim = calculo praticamente automatico.", font=f, fill=BEIGE)
im.save(out / "slide-4-checklist.png")

im = solid_bg(); d = ImageDraw.Draw(im)
add_chrome(im, d, 5, "Proximo passo", show_swipe=False)
title_serif(d, ["Diagnostico"], y0=220, size=88)
title_serif(d, ["em 45 min."], y0=315, size=88, highlight="45 min.", highlight_color=BEIGE)
dots_decor(d, 460)
f = font(SFNS, 26)
d.text((75, 510), "Risco zero - so paga o grande quando recebe.", font=f, fill=DIM2)
cta_simple(d, "Link na bio", y=620)
im.save(out / "slide-5-cta.png")
print("Post 12 OK (5 slides)")


# ============================================================
# POST 13 — CASE — Distribuidora R$ 380k
# ============================================================
out = ROOT / "instagram-posts/post-13-distribuidora-380k"

im = photo_bg(out / "_bg/bg-capa.jpg", 0.86)
d = ImageDraw.Draw(im)
add_chrome(im, d, 1, "Caso real anonimizado", show_swipe=True)
f_big = font(NY, 130)
for ox in [0, 1]:
    d.text((75 + ox, 170), "R$ 380k", font=f_big, fill=BEIGE)
title_serif(d, ["recuperados em 8 meses."], y0=340, size=40, color=WHITE)
f = font(SFNS, 24)
d.text((75, 430), "Distribuidora de alimentos", font=f, fill=DIM2)
d.text((75, 462), "18 anos de mercado · Sorocaba · Lucro Real", font=f, fill=DIM2)
dots_decor(d, 530)
im.save(out / "slide-1-capa.png")

im = solid_bg(); d = ImageDraw.Draw(im)
add_chrome(im, d, 2, "Como dividiu", show_swipe=True)
title_serif(d, ["3 frentes."], y0=160, size=64)
y = 330
y = numbered_serif(d, 1, "PIS/COFINS - R$ 215k",
    "Exclusao do ICMS da base nos ultimos 5 anos (Tema 69 STF).", y)
y = numbered_serif(d, 2, "INSS folha - R$ 95k",
    "Verbas indenizatorias (aviso previo, terco de ferias, auxilio-creche).", y)
y = numbered_serif(d, 3, "Insumos - R$ 70k",
    "PIS/COFINS sobre insumos antes nao creditados (Tema 779 STJ).", y)
im.save(out / "slide-2-tres-frentes.png")

im = photo_bg(out / "_bg/bg-motivos.jpg", 0.88)
d = ImageDraw.Draw(im)
add_chrome(im, d, 3, "Por que distribuidora", show_swipe=True)
title_serif(d, ["Setor altamente", "recuperavel."], y0=160, size=64,
            highlight="recuperavel.", highlight_color=BEIGE)
y = 400
y = bullet(d, "Margem operacional apertada - cada R$ recuperado vira folego.", y, size=26)
y = bullet(d, "ICMS-ST intenso = varias frentes geradas.", y, size=26)
y = bullet(d, "Folha grande com verbas multiplas - INSS quase sempre recuperavel.", y, size=26)
im.save(out / "slide-3-motivos.png")

im = solid_bg(); d = ImageDraw.Draw(im)
add_chrome(im, d, 4, "Proximo passo", show_swipe=False)
title_serif(d, ["Sua empresa", "pode estar aqui."], y0=200, size=72,
            highlight="pode estar aqui.", highlight_color=BEIGE)
dots_decor(d, 420)
f = font(SFNS, 26)
d.text((75, 470), "Diagnostico gratuito de 45 minutos.", font=f, fill=DIM2)
d.text((75, 505), "Identifica todas as frentes do seu caso.", font=f, fill=DIM2)
cta_simple(d, "Link na bio", y=620)
im.save(out / "slide-4-cta.png")
print("Post 13 OK (4 slides)")


# ============================================================
# POST 14 — EDUCATIVO — ICMS destacado vs recolhido
# ============================================================
out = ROOT / "instagram-posts/post-14-icms-destacado-recolhido"

im = photo_bg(out / "_bg/bg-capa.jpg", 0.86)
d = ImageDraw.Draw(im)
add_chrome(im, d, 1, "Educativo - PIS/COFINS", show_swipe=True)
title_serif(d, ["ICMS destacado", "vs ICMS", "recolhido."], y0=170, size=64,
            highlight="recolhido.", highlight_color=BEIGE)
f = font(SFNS, 24)
d.text((75, 530), "A diferenca que vale 5 anos", font=f, fill=DIM2)
d.text((75, 562), "de PIS/COFINS - e quase ninguem sabe.", font=f, fill=DIM2)
dots_decor(d, 620)
im.save(out / "slide-1-capa.png")

im = solid_bg(); d = ImageDraw.Draw(im)
add_chrome(im, d, 2, "Diferenca conceitual", show_swipe=True)
title_serif(d, ["Sao coisas", "diferentes."], y0=160, size=68,
            highlight="diferentes.", highlight_color=BEIGE)
y = 380
y = numbered_serif(d, 1, "ICMS destacado",
    "Valor que aparece no campo 'ICMS' da nota fiscal - independente de ter sido pago.", y)
y = numbered_serif(d, 2, "ICMS recolhido",
    "O que efetivamente saiu do caixa pro estado, apos descontar creditos.", y)
im.save(out / "slide-2-conceito.png")

im = solid_bg(); d = ImageDraw.Draw(im)
add_chrome(im, d, 3, "Exemplo numerico", show_swipe=True)
title_serif(d, ["Operacao de", "R$ 100 mil."], y0=160, size=64,
            highlight="R$ 100 mil.", highlight_color=BEIGE)
y = 380
y = bullet(d, "ICMS destacado na NF: R$ 18.000 (18%).", y, size=28)
y = bullet(d, "ICMS recolhido apos creditos: R$ 11.000.", y, size=28)
y = bullet(d, "Diferenca: R$ 7.000 a recuperar a MAIS por nota.", y, size=28)
f = font(NY_IT, 26)
d.text((75, y + 30), "Em 5 anos, isso vira centenas de milhares.", font=f, fill=BEIGE)
im.save(out / "slide-3-numerico.png")

im = solid_bg(); d = ImageDraw.Draw(im)
add_chrome(im, d, 4, "STF foi claro", show_swipe=True)
title_serif(d, ["E o destacado."], y0=180, size=68,
            highlight="destacado.", highlight_color=BEIGE)
quote_italic(d, '"O ICMS que se exclui e o destacado na nota fiscal." - STF, RE 574.706 (modulacao 13/05/2021)',
             y=320, size=28)
y = 470
y = bullet(d, "IN RFB 2.121/2022 art. 26 confirma.", y, size=28)
y = bullet(d, "Parecer PGFN SEI 7698/2021 ratifica.", y, size=28)
y = bullet(d, "Nao tem mais espaco pra duvida juridica.", y, size=28)
im.save(out / "slide-4-stf.png")

im = solid_bg(); d = ImageDraw.Draw(im)
add_chrome(im, d, 5, "Pergunta-chave", show_swipe=False)
title_serif(d, ["Sua apuracao", "usa qual base?"], y0=200, size=64,
            highlight="qual base?", highlight_color=BEIGE)
dots_decor(d, 400)
f = font(SFNS, 24)
d.text((75, 450), "Se usa recolhido, voce recupera menos.", font=f, fill=DIM2)
d.text((75, 485), "A Renegocia identifica e corrige.", font=f, fill=DIM2)
cta_simple(d, "Diagnostico no link", y=620)
im.save(out / "slide-5-cta.png")
print("Post 14 OK (5 slides)")


# ============================================================
# POST 15 — BASTIDORES — Diagnostico 45 min
# ============================================================
out = ROOT / "instagram-posts/post-15-diagnostico-45min"

im = photo_bg(out / "_bg/bg-capa.jpg", 0.84)
d = ImageDraw.Draw(im)
add_chrome(im, d, 1, "Bastidores Renegocia", show_swipe=True)
title_serif(d, ["45 minutos."], y0=180, size=92,
            highlight="45 minutos.", highlight_color=BEIGE)
title_serif(d, ["Como identificamos", "R$ 200k em creditos."], y0=340, size=44,
            color=WHITE)
dots_decor(d, 500)
f = font(SFNS, 24)
d.text((75, 560), "Diagnostico consultivo passo a passo.", font=f, fill=DIM2)
im.save(out / "slide-1-capa.png")

im = solid_bg(); d = ImageDraw.Draw(im)
add_chrome(im, d, 2, "Como funciona", show_swipe=True)
title_serif(d, ["4 passos."], y0=160, size=64)
y = 300
y = numbered_serif(d, 1, "Leitura",
    "Ultimos 3 anos de DCTF, EFD-Contribuicoes e folha.", y)
y = numbered_serif(d, 2, "Cruzamento",
    "Confronto com o portfolio de 15 teses tributarias.", y)
y = numbered_serif(d, 3, "Identificacao",
    "Quais teses tem fundamentacao direta no seu caso.", y)
y = numbered_serif(d, 4, "Estimativa",
    "Valor recuperavel pelos ultimos 5 anos prescricionais.", y)
im.save(out / "slide-2-quatro-passos.png")

im = solid_bg(); d = ImageDraw.Draw(im)
add_chrome(im, d, 3, "Voce sai com", show_swipe=True)
title_serif(d, ["3 entregas", "concretas."], y0=160, size=64,
            highlight="concretas.", highlight_color=BEIGE)
y = 400
y = bullet(d, "Lista das teses aplicaveis ao seu caso.", y, size=30)
y = bullet(d, "Estimativa de valor recuperavel (margem declarada).", y, size=30)
y = bullet(d, "Decisao clara: vale a pena ou nao?", y, size=30)
f = font(NY_IT, 26)
d.text((75, y + 40), "Se nao vale, dizemos com a mesma clareza.", font=f, fill=BEIGE)
im.save(out / "slide-3-entregas.png")

im = solid_bg(); d = ImageDraw.Draw(im)
add_chrome(im, d, 4, "Compromisso", show_swipe=False)
title_serif(d, ["Custo:"], y0=200, size=88)
title_serif(d, ["zero."], y0=295, size=88, highlight="zero.", highlight_color=BEIGE)
dots_decor(d, 430)
f = font(SFNS, 26)
d.text((75, 480), "Compromisso depois: zero.", font=f, fill=DIM2)
d.text((75, 515), "Honorarios majoritarios so vencem no exito.", font=f, fill=DIM2)
cta_simple(d, "Link na bio", y=630)
im.save(out / "slide-4-cta.png")
print("Post 15 OK (4 slides)")


# ============================================================
# POST 16 — PROVOCACAO — Pre-2017 (imagem unica)
# ============================================================
out = ROOT / "instagram-posts/post-16-pre-2017"

im = photo_bg(out / "_bg/bg-unica.jpg", 0.84)
d = ImageDraw.Draw(im)
add_chrome(im, d, 1, "Provocacao - PIS/COFINS", show_swipe=False)
title_serif(d, ["Sua empresa", "existe desde antes", "de 15/03/2017?"], y0=180, size=64,
            highlight="15/03/2017?", highlight_color=BEIGE)
dots_decor(d, 460)
f = font(SFNS, 26)
d.text((75, 510), "Se sim e apura PIS/COFINS em LP ou LR,", font=f, fill=DIM2)
d.text((75, 545), "voce quase certamente paga imposto a mais.", font=f, fill=DIM2)
f2 = font(NY_IT, 24)
d.text((75, 620), '"Por que minha contabilidade nunca falou disso?"', font=f2, fill=BEIGE)
d.text((75, 660), 'Resposta: nao e funcao do contador fiscal revisar', font=font(SFNS, 22), fill=DIM2)
d.text((75, 690), '5 anos pra tras cacando credito. E consultoria.', font=font(SFNS, 22), fill=DIM2)
im.save(out / "slide-1-unica.png")
print("Post 16 OK (1 slide)")


# ============================================================
# POST 17 — TESE — LC 224/2025 Lucro Presumido
# ============================================================
out = ROOT / "instagram-posts/post-17-lc224-lucro-presumido"

im = photo_bg(out / "_bg/bg-capa.jpg", 0.86)
d = ImageDraw.Draw(im)
add_chrome(im, d, 1, "LC 224/2025", show_swipe=True)
title_serif(d, ["O aumento", "silencioso de", "10% no LP."], y0=170, size=66,
            highlight="10%", highlight_color=BEIGE)
f = font(SFNS, 26)
d.text((75, 550), "Empresas com faturamento > R$ 5MM/ano:", font=f, fill=DIM2)
d.text((75, 585), "presuncao de lucro foi elevada linearmente.", font=f, fill=DIM2)
dots_decor(d, 640)
im.save(out / "slide-1-capa.png")

im = solid_bg(); d = ImageDraw.Draw(im)
add_chrome(im, d, 2, "O que mudou", show_swipe=True)
title_serif(d, ["+10% linear", "na presuncao."], y0=160, size=64,
            highlight="+10% linear", highlight_color=BEIGE)
y = 360
y = bullet(d, "Atinge faixa de receita acima de R$ 5MM/ano.", y, size=28)
y = bullet(d, "Reclassifica LP como 'beneficio fiscal' - distorcao juridica.", y, size=28)
y = bullet(d, "Aumenta IRPJ e CSLL na conta do empresario PME medio-grande.", y, size=28)
y = bullet(d, "Vigencia: 2025/2026 - efeito ja sentido.", y, size=28)
im.save(out / "slide-2-mudanca.png")

im = solid_bg(); d = ImageDraw.Draw(im)
add_chrome(im, d, 3, "Tese de defesa", show_swipe=True)
title_serif(d, ["3 argumentos."], y0=160, size=64)
y = 320
y = numbered_serif(d, 1, "Isonomia ferida",
    "Comerciante e prestador tem margens diferentes - aumento uniforme viola CF art. 150, II.", y)
y = numbered_serif(d, 2, "Distorcao juridica",
    "LP nao e beneficio - e tecnica de apuracao prevista em lei.", y)
y = numbered_serif(d, 3, "Precedente favoravel",
    "Liminar em fev/2026 livrou empresa do aumento (Conjur).", y)
im.save(out / "slide-3-tese.png")

im = solid_bg(); d = ImageDraw.Draw(im)
add_chrome(im, d, 4, "Para sua empresa", show_swipe=False)
title_serif(d, ["Avalie agora."], y0=200, size=72,
            highlight="agora.", highlight_color=BEIGE)
quote_italic(d, '"Mandado de seguranca preventivo ainda e viavel."',
             y=340, size=26)
y = 430
y = bullet(d, "Calculo retroativo desde vigencia da LC.", y, size=26)
y = bullet(d, "Possivel migracao LP -> LR se a conta fechar melhor.", y, size=26)
cta_simple(d, "Diagnostico no link", y=640)
im.save(out / "slide-4-cta.png")
print("Post 17 OK (4 slides)")

print()
print("=== 23 slides V5 gerados em 6 posts ===")
