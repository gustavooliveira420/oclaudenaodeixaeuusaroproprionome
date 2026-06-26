# Contrato Semanal — Gerenciamento IG @renegocia.tributario

**Vigência:** a partir de 2026-06-01 · **Duração:** 24 meses (até 2028-05-31)

Este documento é o contrato entre Gabriel/Gustavo (clientes) e qualquer Claude que entrar no repo. Define as obrigações de gerenciamento de conteúdo IG, os entregáveis semanais e as salvaguardas anti-erro. Falhas em cumpri-lo geram revisão do gerenciador.

---

## 1. Cadência de publicação e revisão

- **6 posts/semana publicados**: seg, ter, qua, qui, sex + 1 bônus aos sábados
- **Domingo:** sem publicação (descanso editorial) — usado pra **entregar bundle de 12 posts** ao Gabriel revisar
- **Horários** (BRT):
  - 09:00 — turno manhã (alta atenção decisor PME)
  - 13:00 — segundo post no mesmo dia em semanas de campanha (não default)
  - 18:00 — turno fim-de-expediente (re-engajamento)
- Default = 1 post/dia útil às 09:00 BRT, exceto semanas de lançamento de tese (3/dia).
- **Ciclo de revisão:** Claude entrega 12 → Gabriel escolhe 6 até segunda 18:00 BRT → Claude atualiza `instagram_posts.json` e cron do workflow até terça 12:00 BRT.

## 2. Pilares de conteúdo (rotação semanal fixa)

| Dia | Pilar | Formato típico |
|---|---|---|
| **Seg** | Tese da semana (jurisprudência aplicada) | Carrossel 5-6 slides |
| **Ter** | Case real anonimizado (R$ recuperado) | Carrossel 3-4 slides ou imagem única com texto |
| **Qua** | Educativo / FAQ (conceito em linguagem simples) | Carrossel 4-5 slides |
| **Qui** | Bastidores / processo Renegocia | Imagem única, reel ou carrossel curto |
| **Sex** | Provocação + CTA diagnóstico | Imagem única com pergunta forte |
| **Sáb (bônus)** | Curadoria de notícia/decisão STF-STJ-CARF | Imagem com hook + caption explicativa |

## 3. Política de "se apropriar" de cases externos

Tributário é ecossistema de jurisprudência **pública** — todo case útil já está em algum lugar. Política de coleta:

**Fontes legítimas (citar fonte sempre que aplicável):**
- ✅ Decisões públicas STF, STJ, TRFs, CARF (sites oficiais, Conjur, Migalhas)
- ✅ Notícias de imprensa especializada (Valor Econômico, Conjur, JOTA, Migalhas)
- ✅ Publicações da Receita Federal, PGFN, secretarias estaduais
- ✅ Pareceres acadêmicos, dissertações em domínio público
- ✅ Cases publicados em sites de escritórios concorrentes — **mas só como ponto de partida temático**. Reescrever 100% do zero, do ângulo Renegocia, sem reproduzir copy.

**Proibido:**
- ❌ Copiar caption/copy de competitor (concorrência desleal + direito autoral)
- ❌ Republicar imagem/arte de competitor (mesmo sem créditos)
- ❌ Inventar números/cases (risco regulatório CFC/OAB + perda de credibilidade)
- ❌ Citar nome de cliente real sem autorização escrita

**Para cada case publicado**: registrar a fonte original em `docs/editorial/cases-bibliografia.md` (link + data de consulta). Auditoria a qualquer momento.

## 4. Entregável semanal obrigatório (todo DOMINGO 09:00 BRT)

> **Mudança em 2026-05-30:** Gabriel ajustou de segunda para DOMINGO porque quer ter o dia útil pra revisar e cortar. Cadência é **12 posts (2 semanas)** em cada entrega — ele escolhe a metade pra próxima semana. Resto vai pro estoque ou é descartado.

Todo domingo 09:00 BRT, o Claude que gerencia este projeto **DEVE** entregar:

1. **Bundle de 12 posts** em `docs/editorial/planos-semanais/{ANO}-W{NN}-W{NN+1}-bundle.md` contendo:
   - 12 posts (~2 semanas) com: pilar, ângulo, hook, caption rascunho COMPLETA, briefing visual (slides), **fonte oficial obrigatória** (link STF/STJ/CARF/Receita/Conjur/JOTA/Valor)
   - Hashtag fixa de auditoria `#rngc-{YYYYWNN}-{dia}` (oculta no fim da caption)
   - Marcação clara de quais 6 são "recomendação top" (numerados 1-6 com nota) e quais 6 são alternativos (7-12)
2. **Status da semana anterior:**
   - Quais posts saíram, horário real vs planejado
   - Métricas básicas (alcance, engajamento) via Graph API
   - Falhas detectadas e correção aplicada
3. **Sinalização de risco:**
   - Token Meta expira em < 30 dias? → alerta vermelho
   - Algum post falhou? → causa raiz já identificada
   - Mudança de algoritmo/política Meta? → ajuste proposto
   - Mudança legislativa relevante (LC/Lei/MP/IN) → impacto nos posts já programados

**Padrão de apuração (não-negociável):** cada post precisa de fonte oficial direta — não vale citar "STF decidiu" sem link/processo/data. Aceitas: portal.stf.jus.br, scon.stj.jus.br, carf.economia.gov.br, gov.br/receitafederal, in.gov.br, pgfn.gov.br, conjur.com.br, jota.info, valor.globo.com, migalhas.com.br. Toda fonte vai pra `cases-bibliografia.md` no mesmo commit.

Sem esse entregável no domingo, o gerenciamento está em falta.

## 5. Salvaguardas anti-erro (implementadas no workflow)

Histórico ruim: cronograma original 22-24/05 perdeu 6 de 9 posts e gerou 1 duplicado. Salvaguardas pra impedir repetição:

### 5.1 Idempotência pré-publicação

Antes de publicar o post N, o workflow consulta a Graph API e verifica se já existe post com a hashtag de auditoria `#rngc-{YYYYWNN}-{dia}` nas últimas 48h. Se existir → aborta com aviso. Impede dupla publicação por retry.

### 5.2 Verificação pós-publicação

Após `media_publish` retornar sucesso, o workflow:
1. Faz GET no media_id retornado
2. Compara caption real no IG vs caption do JSON
3. Se divergente → cria issue automática no repo com `[ALERTA] caption divergente post N`

### 5.3 Assinatura oculta

Toda caption termina com hashtag `#rngc-{YYYYWNN}-{D}` (D = 1-6 do dia da semana). Serve como:
- Detector de duplicação (item 5.1)
- Trilha de auditoria (qual post correspondia a qual planejamento)
- Não polui visualmente (perdida no meio das hashtags de marketing)

### 5.4 Notificação de falha por issue

Se qualquer step do workflow falhar (token, upload, publish), GitHub Action abre issue automática `[FALHA-IG] {data} post {N}: {causa}`. Visível na lista de issues do repo, sem depender de email.

### 5.5 Alerta de token expirando

Cron diário às 08:00 UTC verifica `debug_token` da Graph API. Se `expires_at` < 30 dias → issue automática `[TOKEN] expira em X dias`.

### 5.6 Lock anti-concorrência

Workflow tem `concurrency: group: ig-post / cancel-in-progress: false` — duas execuções simultâneas nunca rodam, segunda fica em fila.

## 6. O que está fora de escopo

Pra ser honesta sobre o que não dou conta sozinha:

- **Produção de arte (slides PNG):** Claude não desenha. Cada post precisa do Gabriel/Gustavo (ou designer) entregar os PNGs no caminho `instagram-posts/post-N-{tema}/slide-X.png` do repo público. O briefing semanal já vem com a especificação dos slides necessários.
- **Aprovação final de copy:** rascunho de caption sempre passa pelo Gabriel antes de virar `instagram_posts.json`. Auto-publicação só com config aprovada.
- **Resposta a DM/comentários:** Claude não responde mensagens diretas — é responsabilidade humana. Pode SUGERIR resposta se chamada.
- **Métricas avançadas / dashboards:** Graph API entrega básico (alcance, impressões, likes, comentários). Pra dashboard visual, usar ferramenta externa (Iconosquare, Meta Business Suite).

## 7. Critérios de revisão do contrato

A cada 90 dias (próximas datas: 2026-08-30, 2026-11-28, 2027-02-26, ...):
- Revisar pilares de conteúdo com base no que performou
- Re-priorizar teses tributárias por demanda real do funil
- Ajustar cadência se necessário (mais/menos posts)

Mudança fora do ciclo de 90 dias: só por solicitação explícita do Gabriel ou Gustavo.

---

**Assinatura digital:** este contrato vive em `docs/editorial/CONTRATO-SEMANAL.md` e é commit `f136b6f` (data de origem). Versionado via git — qualquer alteração tem histórico rastreável.
