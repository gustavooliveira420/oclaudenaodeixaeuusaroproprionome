# Salvaguardas Anti-Falha — Publicação IG @renegocia.tributario

**Princípio:** "agente que se dá ao luxo de falhar, ou que não se auto-corrige, não serve." (Gabriel, 30/05/2026)

Este documento mapeia os modos de falha conhecidos e as 6 camadas de defesa implementadas. Atualizar sempre que um novo tipo de falha for descoberto.

---

## Mapa de modos de falha

| # | Falha | Causa típica | Camada que cobre |
|---|---|---|---|
| F1 | Cron não disparou no horário | GH Actions outage ou cron lag > 1h | **Camada 4 (catch-up)** |
| F2 | Token Meta revogado | Mudança de senha, desautorização, ação humana | **Camada 1 (pre-flight)** + **Camada 5 (watchdog)** |
| F3 | Imagem 404 (raw.github fora) | Repo de imagens caiu, pasta deletada | **Camada 1 (pre-flight valida URLs)** |
| F4 | Caption > 2200 chars | Editor passou do limite | **Camada 1 (pre-flight)** |
| F5 | Container órfão | Children criados, publish falhou no meio | **Camada 3 (retry)** + **Camada 4 (catch-up detecta)** |
| F6 | Erro transitório Meta (5xx, timeout) | Backend Meta lento | **Camada 3 (retry exponencial)** |
| F7 | Rate-limit Meta (code 4, 17, 32) | Muitos posts em pouco tempo | **Camada 3 (retry com backoff longo)** |
| F8 | Duas execuções simultâneas | Workflow disparado em paralelo | **Camada 0 (concurrency lock)** |
| F9 | Caption duplicada | Workflow re-rodou no mesmo post | **Camada 2 (idempotência)** |
| F10 | Post fora do cronograma | Cron mal configurado, branch errada | **Camada 5 (watchdog compara plano x realidade)** |
| F11 | instagram_posts.json mal-formado | Erro humano no merge | **Camada 1 (pre-flight valida JSON)** |
| F12 | Caption publicada diverge da planejada | Race condition, edição tardia, bug no script | **Camada 6 (pos-verify)** |

---

## As 6 camadas de defesa

### Camada 0 — Concurrency lock
**Onde:** `instagram-scheduled-posts.yml`, top-level `concurrency.group: ig-post`
**O quê:** Garante que nenhum workflow (principal ou catch-up) rode em paralelo com outro do mesmo grupo. Segundo workflow espera o primeiro terminar.
**Cobre:** F8.

### Camada 1 — Pre-flight (`scripts/preflight.py`)
**Onde:** step `Pre-flight` no workflow principal, ANTES de qualquer chamada de publicação.
**O quê:** Valida em sequência:
1. Token Meta via `debug_token` — válido? expira em > 7 dias?
2. IG user existe e responde (`GET /{user_id}?fields=username,account_type`)
3. JSON `instagram_posts.json` é parseável e contém o `post_number` esperado
4. Caption tem ≤ 2200 chars
5. Caption tem ≤ 30 hashtags e ≤ 5 menções @
6. URLs das imagens respondem 200 OK (HEAD ou GET com Range)
7. Hashtag de auditoria `#rngc-AAAAWNN-D` presente (aviso, não bloqueia)

**Exit codes:** 0 = OK, 1 = fatal, 2 = aviso.
**Cobre:** F2, F3, F4, F11.

### Camada 2 — Idempotência por assinatura de caption
**Onde:** step `Salvaguarda — idempotência` no workflow principal, ANTES do publish.
**O quê:** Faz `GET /{user_id}/media?limit=15` e compara os primeiros 60 chars da caption esperada com cada caption publicada nas últimas N posts. Se bater → aborta com `skip=true`.
**Cobre:** F9 (duplicação por re-execução).

### Camada 3 — Retry exponencial (`scripts/post_to_instagram.py`)
**Onde:** Função `api_call()` no script de publicação.
**O quê:** Em erros transitórios (HTTP 429, 500-504, ou Meta error codes 4, 17, 32, 613), tenta de novo 3 vezes com backoff: **30s → 90s → 180s**. Erros fatais (token, payload inválido) abortam imediatamente.
**Cobre:** F5 parcial, F6, F7.

### Camada 4 — Catch-up automático (`instagram-catchup.yml`)
**Onde:** Workflow separado, roda diário 02:00 UTC (23:00 BRT).
**O quê:**
1. Lê o cronograma esperado pra hoje (mapa `SCHEDULE` no script)
2. Lista posts publicados nas últimas 36h via Graph API
3. Compara: quais esperados não saíram?
4. Pra cada gap, dispara `post_to_instagram.py --publish` (com todas as camadas 1-3)
5. **Limites:** max 2 catch-ups por janela de 7 dias · só re-tenta posts com < 48h de atraso · idempotência mantida via Camada 2

**Persistência:** registro em `docs/editorial/audit-log/catchup-history.json` (commitado automaticamente pelo workflow).
**Cobre:** F1, F5 (container órfão antigo é detectado como "não publicado"), parcialmente F2 e F3 (catch-up vai falhar com mesmo erro até alguém corrigir, mas pelo menos sinaliza).

### Camada 5 — Watchdog semanal (`instagram-watchdog.yml`)
**Onde:** Workflow separado, roda segunda 11:00 UTC (08:00 BRT).
**O quê:** Audita os últimos 7 dias:
- Posts publicados (esperado = `EXPECTED_POSTS_PER_WEEK`, default 6) vs realidade → gap?
- Duplicatas detectadas?
- Token expira em quanto tempo? (< 30d = alerta)
- Catch-ups executados na semana > 1? (sinal de problema sistêmico)

**Se algum alerta:** cria issue `[WATCHDOG] {data} - N alerta(s) na semana` com diagnóstico e ações recomendadas.
**Cobre:** F2 (alerta antecipado de token), F10, supervisão geral.

### Camada 6 — Pos-verify (caption divergente)
**Onde:** step `Pos-verify` no workflow principal, APÓS publish bem-sucedido.
**O quê:** Aguarda 15s (reflexão na Graph API), faz `GET /{user_id}/media?limit=3`, pega o post mais recente e compara os primeiros 80 chars da caption real com a esperada. Se divergir → log de aviso (não falha o run, mas fica registrado).
**Cobre:** F12.

---

## O que NÃO está coberto (transparência)

1. **Outage prolongada do GitHub Actions** (> 24h) — não tem como compensar sem infra externa. Mitigação: Camada 5 vai gerar alerta na próxima segunda.
2. **Bloqueio de conta pela Meta** (violação de termos) — só ação humana resolve.
3. **Reforma da Graph API** — quebras de schema vão exigir update de código manual.
4. **Falha humana no merge** (PR errado pra main) — Camada 5 detecta posteriormente; idealmente CI deveria rodar pre-flight em PR também (futuro).
5. **Imagens cinzas/borradas** — pre-flight checa que URL responde 200, não checa qualidade visual.

---

## Fluxo completo de uma publicação saudável

```
┌─ cron 0 12 1 6 * ─────────────────────────────────────────────────┐
│                                                                   │
│  1. concurrency lock adquirido (Camada 0)                         │
│  2. checkout + python                                             │
│  3. decidir N do post (mapa cron → número)                        │
│  4. PRE-FLIGHT (Camada 1) ──┬── exit 0 OK → segue                 │
│                             ├── exit 2 AVISO → segue              │
│                             └── exit 1 FATAL → para + issue       │
│  5. IDEMPOTÊNCIA (Camada 2) ─┬── já publicado → skip + sai OK     │
│                              └── não publicado → segue            │
│  6. PUBLISH com RETRY (Camada 3)                                  │
│     - cria children, espera FINISHED                              │
│     - cria carrossel, espera FINISHED                             │
│     - chama media_publish                                         │
│  7. POS-VERIFY (Camada 6) → log de OK ou aviso                    │
│  8. SE ALGUM STEP FALHOU → issue [FALHA-IG] auto                  │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

## Fluxo de auto-correção quando algo dá errado

```
falha no cron principal
         │
         ▼
┌─ 23:00 BRT mesmo dia ─────────────────────────────────────────────┐
│ CATCH-UP (Camada 4) detecta gap e tenta republicar                │
│   ├── sucesso → issue [CATCH-UP] + log                            │
│   └── falha   → issue [CATCH-UP] urgente + log                    │
└───────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─ próxima segunda 08:00 BRT ───────────────────────────────────────┐
│ WATCHDOG (Camada 5) audita semana inteira                         │
│   - se gap persiste → issue [WATCHDOG] urgente                    │
│   - se token expirando → alerta antecipado                        │
│   - se duplicata ou muitos catchups → sinal sistêmico             │
└───────────────────────────────────────────────────────────────────┘
```

---

## Onde olhar quando algo der errado

| Sintoma | Primeiro lugar |
|---|---|
| "Post não saiu hoje" | Actions → Instagram Scheduled Posts → run do dia |
| "Veio uma issue [FALHA-IG]" | Corpo da issue tem causa + run URL |
| "Veio issue [CATCH-UP]" | Houve recuperação automática — checar `catchup-history.json` |
| "Veio issue [WATCHDOG]" | Semana com gap; abrir e seguir "ações recomendadas" |
| "Token expirando" | `scripts/.env.example` tem passo-a-passo de renovação |
| "Imagem 404" | Repo de imagens é o mesmo deste repo (pasta `instagram-posts/`) |

---

## Como testar as salvaguardas

```bash
# 1. Pre-flight standalone
python3 scripts/preflight.py 3        # valida post 3
python3 scripts/preflight.py --all-pending

# 2. Catch-up em dry-run (não publica)
python3 scripts/catchup.py --dry-run

# 3. Watchdog standalone
python3 scripts/watchdog.py

# 4. Workflow dispatch via GitHub UI:
#    Actions → Instagram Scheduled Posts → Run workflow → dry_run=true
```

---

**Versão:** 1.0 (2026-05-30) · **Próxima revisão:** após primeira execução do catch-up real (qualquer post que falhar nos próximos 30 dias).
