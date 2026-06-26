# Publicação automática no Instagram

Script `post_to_instagram.py` que publica os 9 posts de estreia do `@renegocia.tributario` via Instagram Graph API.

## Setup (uma única vez)

### 1. IG Business + Facebook Page
- `@renegocia.tributario` precisa estar como **Business** (já está)
- Precisa estar vinculado a uma **Facebook Page** (business.facebook.com → Configurações → Contas)

### 2. App Meta + Token
- Cria app em https://developers.facebook.com/apps (tipo Business, com produto **Instagram Graph API**)
- Em **Graph API Explorer** gera token com scopes: `instagram_basic, instagram_content_publish, pages_show_list, pages_read_engagement, business_management`
- Troca por long-lived token (ver `scripts/.env.example` passo a passo)
- Pega `IG_USER_ID` via `me/accounts` + `{page_id}?fields=instagram_business_account`

### 3. Hospedagem das imagens
A Graph API **não aceita upload binário** — precisa URL HTTPS pública. Três opções:

**(a) Vercel (recomendado quando o site estiver deployado):**
```bash
cp -r instagram-posts public/
git add public/instagram-posts && git commit -m "expose ig posts publicly" && git push
```
Aí no `.env`: `IG_IMAGE_BASE_URL=https://renegociaconsultoria.vercel.app/instagram-posts`

**(b) Cloudinary/S3/R2:** sobe as PNGs e usa a URL do bucket.

**(c) Tornar o repo público:** habilita `raw.githubusercontent.com` automaticamente.

### 4. Variáveis de ambiente
```bash
cp scripts/.env.example scripts/.env
# editar com os 3 valores
```

## Uso

```bash
# dry-run de todos os 9 (não publica, só mostra o que faria)
python3 scripts/post_to_instagram.py

# dry-run de um post específico
python3 scripts/post_to_instagram.py 1

# publicar de verdade (post único)
python3 scripts/post_to_instagram.py 1 --publish

# publicar todos do dia 1 (posts 1, 2, 3)
python3 scripts/post_to_instagram.py --day 1 --publish
```

## Calendário recomendado

| Dia | Posts | Tema |
|---|---|---|
| 1 | 1, 2, 3 | institucionais (base do perfil) |
| 2 | 4, 5, 6 | ganchos + tese forte |
| 3 | 7, 8, 9 | prova social + tese folha + CTA |

Posts 1 e 2 precisam ser **fixados no topo do perfil** — isso o script avisa, mas o Fix em si é manual (Instagram não expõe isso na API). Abre o app, 3 pontinhos no post → **Fixar no perfil**.

## Limites e cuidados

- Graph API permite **50 posts publicados por 24h** por IG (folgadíssimo).
- Tokens long-lived expiram em 60 dias — anotar pra renovar.
- Sempre rodar **dry-run primeiro** pra conferir caption + ordem dos slides.
- Caption já vem pronta no `instagram_posts.json` — não alterar sem checar com o Gabriel.

## Quando o script falhar

- **`status_code: ERROR` em container** → a Graph API rejeitou a imagem. Comum: URL não pública, imagem fora de 320-1440px, formato não-JPEG.
- **Token expirado** → regenera (ver `.env.example`).
- **`(#100) Invalid parameter`** → erro de parâmetro. Olha a mensagem completa no log.
