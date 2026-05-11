# Deploy na Vercel — passo a passo (Gustavo, primeira vez)

Guia em linguagem leiga para subir o site `renegociaconsultoria` na Vercel pela primeira vez. Toda vez que você ou o Gabriel fizerem `push` na branch `main`, a Vercel rebuilda e republica automaticamente.

## O que você vai precisar antes de começar

- [ ] Conta no GitHub criada (a sua) — https://github.com
- [ ] Estar listado como **Collaborator** no repo `GabrielMendesIA/renegociaconsultoria` (Gabriel adiciona pela página Settings → Collaborators e você aceita por e-mail)
- [ ] Cartão de crédito **não** é necessário para o plano gratuito da Vercel (Hobby) — só pede se passar dos limites

## Passo 1 — Criar conta na Vercel

1. Acesse **https://vercel.com/signup**
2. Clica em **"Continue with GitHub"** (não use Google ou e-mail — perde a integração)
3. O GitHub vai pedir autorização para a Vercel — clica em **Authorize Vercel**
4. Na tela seguinte, escolhe o **plano Hobby (Free)** — é grátis e cobre site de marketing/landing tranquilamente
5. Pula a parte de "convide seu time" — pode fazer depois

Você cai no dashboard da Vercel.

## Passo 2 — Importar o repositório

1. No dashboard, clica em **Add New… → Project**
2. Aparece a lista de repositórios do seu GitHub. **Provavelmente o `renegociaconsultoria` não vai aparecer** porque ele está na conta do Gabriel, não na sua.
3. Clica em **Adjust GitHub App Permissions** (link discreto, em geral abaixo da lista). Isso abre uma página do GitHub.
4. Na página do GitHub, em **Repository access**:
   - Escolhe **"Only select repositories"**
   - Clica em **Select repositories** → adiciona `GabrielMendesIA/renegociaconsultoria`
   - Clica em **Save**
5. Voltando pra Vercel, o repo agora aparece na lista. Clica em **Import** no card dele.

> **Se mesmo assim não aparecer:** confirma com o Gabriel que você foi adicionado como Collaborator (o convite chega no seu e-mail e você precisa clicar em "Accept invitation"). Sem isso, a Vercel não enxerga o repo.

## Passo 3 — Configurar o projeto

A Vercel detecta automaticamente que é um projeto Vite. Confere se está assim:

| Campo | Valor esperado |
|---|---|
| **Framework Preset** | `Vite` |
| **Root Directory** | `./` (deixa em branco mesmo) |
| **Build Command** | `npm run build` (já vem) |
| **Output Directory** | `dist` (já vem) |
| **Install Command** | `npm install` (já vem) |

**Environment Variables** — não precisa nenhuma agora. Pula a seção.

Clica em **Deploy**.

## Passo 4 — Aguardar o primeiro deploy

- Tempo médio: **1-3 minutos** na primeira vez
- Você vê o log em tempo real (instalação de dependências → build → upload)
- Quando terminar, aparece confete na tela e um botão **Visit**

## Passo 5 — Acessar o site

A Vercel dá uma URL provisória, algo como:
- `renegociaconsultoria-{algumas-letras}.vercel.app`

Clica em **Visit** ou copia a URL e abre no navegador.

**Confere se está tudo:**
- [ ] Logo aparece no header
- [ ] Hero carrega com fundo verde escuro
- [ ] Stats animam ao rolar
- [ ] As 3 soluções aparecem (Revisão / Recuperação / Renegociação)
- [ ] Form de contato funciona — preenche os 3 passos e envia (o webhook é o mesmo: `webhooks-mvp.algomaisacai.com.br`)

## Passo 6 — Manda o link no grupo

Manda no WhatsApp pro Gabriel pra ele validar também. Se tudo bem, partimos pra fase de domínio.

## Daqui pra frente — deploys automáticos

A partir desse setup inicial:

- **Toda vez que alguém fizer `git push` pra `main`** → a Vercel rebuilda e republica em ~1 minuto. Não precisa fazer nada manualmente.
- **Toda branch nova com `git push` (ex: `feature-x`)** → Vercel cria um **Preview Deploy** numa URL própria (`renegocia...-feature-x-{hash}.vercel.app`). Útil pra testar antes de mergear no main.
- **Pull Requests** → a Vercel comenta automaticamente no PR com o link do preview. Bem útil pra revisar visualmente antes de aprovar merge.

## Passo 7 — Domínio próprio (quando o Gabriel comprar)

Quando o Gabriel registrar o domínio (ex: `renegocia.com.br`):

1. Na Vercel: Project → **Settings → Domains**
2. Clica em **Add** → digita o domínio (ex: `renegocia.com.br`)
3. A Vercel mostra os registros DNS que você precisa cadastrar
4. No painel do registrador onde foi comprado o domínio (Registro.br, GoDaddy, Hostinger, etc.), você cadastra os registros mostrados pela Vercel:
   - Para o domínio raiz (`renegocia.com.br`): um registro **A** apontando para o IP da Vercel
   - Para o www (`www.renegocia.com.br`): um **CNAME** apontando para `cname.vercel-dns.com`
5. Aguarda **propagação DNS** (de 5 minutos a algumas horas)
6. A Vercel detecta automaticamente quando os DNS estão corretos e ativa o domínio
7. **HTTPS sai sozinho** (Let's Encrypt, automático)

## Troubleshooting comum

### "Build failed" no primeiro deploy
- Quase sempre é dependência faltando ou erro de TypeScript
- Abre os logs do build, copia a mensagem de erro, manda pro Claude (do Gabriel ou seu) — resolve em minutos
- Comando local pra reproduzir: `npm install && npm run build`

### Repo não aparece na lista da Vercel
- Você não foi adicionado como Collaborator → pede pro Gabriel adicionar
- Você não autorizou o repo no GitHub App da Vercel → volta no passo 2.3

### Form de contato não envia depois do deploy
- Abrir Console do navegador (F12 → Console) e ver erro
- Provavelmente é CORS no webhook — me chama (ou o Claude) pra verificar
- A URL do webhook está hardcoded no código (`ContactSection.tsx`), então funciona igual ao localhost

### Site ficou bonito mas link do WhatsApp não funciona
- O número está no código (`Hero.tsx` e `WhatsAppButton.tsx`) — o Gabriel confirma ou ajusta

### Como ver o site da última versão de uma branch específica
- Toda branch com push tem URL própria — no dashboard da Vercel → aba **Deployments** → cada item tem link próprio
- Útil pra mostrar pro Gabriel uma mudança antes de mergear

## Limites do plano Hobby (Free)

- 100 GB de bandwidth/mês (mais que suficiente pra site de marketing)
- Build minutes: 6000/mês (cada deploy gasta ~1 min, então 6000 deploys/mês)
- Domínio próprio: ilimitado
- Membros: 1 (a conta sua)

Se um dia precisar mais (e-commerce de alto tráfego, etc.), Pro fica em US$ 20/mês.

## Quem mexe em quê

| Quem | O quê |
|---|---|
| **Gabriel** | Owner do repo, paga domínio, aprova PRs |
| **Gustavo** | Owner da Vercel (deploy), monitora performance |
| **Ambos** | Push pro `main` dispara deploy — combinem antes de mexer em arquivos críticos (ver `docs/colaboracao.md`) |

## Próximos passos depois do primeiro deploy funcionar

1. Comprar domínio `renegocia.com.br` (Gabriel) — Registro.br custa ~R$ 40/ano
2. Apontar DNS para Vercel (Gustavo, Passo 7)
3. Atualizar canonical do site (`index.html`) com o domínio real
4. Configurar Google Search Console + Google Analytics quando estabilizar
