# Plano de marketing e captação — Renegocia Consultoria

## Contexto

A Renegocia é uma consultoria tributária com 15 teses/serviços mapeadas, tabela de honorários pronta, scripts de abordagem por canal e pareceres reais (Cedro Auto Posto, Decreto diesel, execução FRZZ). Os stakeholders responsáveis técnicos (advogados, contadores parceiros) ainda serão definidos. Este documento é o plano de captação — o que atrair, como atrair, por onde atrair, e como converter.

Fontes autoritativas (sempre consultar antes de criar qualquer peça):
- `Downloads/17032026V1. Teses Tributárias (1).xlsx` — portfólio, FAQ, matriz, script
- `Downloads/Planilha Precificação Tributária rev16102025.xlsx` — tabela, simulador, template proposta

---

## 1. Oferta-âncora

**Diagnóstico tributário gratuito** — 30 a 45 minutos, online. Entrega: levantamento preliminar de créditos recuperáveis e adequação do regime, baseado em 12 meses de DRE/SPED do prospecto.

Por que funciona: honorários são majoritariamente de êxito → atrito de venda é baixo → diagnóstico gratuito não é "chamariz", é a porta real de entrada. Já está validado na copy do site (`PricingSection.tsx`).

---

## 2. Segmentação e priorização

**Filtro mínimo (descarta):**
- Simples Nacional puro (exceção: ICMS-ST ressarcimento se tiver o recolhimento)
- Faturamento < R$ 500k/ano
- Empresa com equipe jurídica tributária interna robusta

**Perfis quentes (em ordem de prioridade comercial):**

| Prioridade | Perfil | Teses de entrada |
|---|---|---|
| 🔴 Máxima | Médio-Grande, Lucro Real, folha > R$ 100k/mês, indústria ou comércio relevante | Tema 69 (ICMS×PIS/COFINS), INSS Indenizatórias, PIS/COFINS Insumos |
| 🔴 Máxima | Beneficiário de incentivo ICMS estadual (Decreto Sefaz) | Tema 1.182 (ICMS incentivos × IRPJ/CSLL) |
| 🟠 Alta | Prestador de serviço (TI, saúde, educação, consultoria), LP ou LR | Exclusão ISS × PIS/COFINS |
| 🟠 Alta | Varejo farmacêutico / autopeças / bebidas / construção | ICMS-ST Ressarcimento |
| 🟠 Alta | PME em crescimento / prestes a estourar Simples | Planejamento de regime |
| 🟠 Alta | Família com patrimônio > R$ 2MM, sócios > 55 anos | Holding patrimonial |
| 🔵 Nicho | Bancos / seguradoras / corretoras | CSLL majoração |

**Segmentos de ALVO PRIMÁRIO (cruzando CNAE × tese, da Matriz de Priorização):**
1. Postos de combustíveis — já tem parecer pronto (Cedro) como case
2. Indústria de transformação — IPI insumos + PIS/COFINS insumos + Tema 69
3. Distribuidoras e atacado — Tema 69 + ICMS-ST
4. Agronegócio — ICMS incentivos + holding patrimonial
5. Clínicas e consultórios (saúde privada) — exclusão ISS + regime + holding

---

## 3. Funil

```
ATRAÇÃO           QUALIFICAÇÃO       DIAGNÓSTICO         PROPOSTA          EXECUÇÃO
────────          ─────────────      ───────────         ────────          ─────────
Conteúdo          Form 3-step         Reunião 30-45 min    Carta-proposta    Procuração +
orgânico          (já no site)        + dados DRE/SPED     (template da      contrato +
(LinkedIn                                                  planilha de       execução
institucional)    Script WhatsApp     Parecer              precificação)     (admin ou
                  por tese            simplificado                           judicial)
Outbound                              (2-3 páginas)
frio
                                                           UPSELL: Retainer
Anúncios                                                   mensal após
por tese                                                   entrega
```

**Gatilhos de conversão por etapa:**
- **Atração → Qualificação:** CTA "Agendar diagnóstico gratuito" em todo lugar
- **Qualificação → Diagnóstico:** resposta em até 24h + link Calendly com slots da semana
- **Diagnóstico → Proposta:** sempre sair da reunião com R$ estimado e prazo; enviar proposta em até 72h
- **Proposta → Execução:** proposta com assinatura digital (D4Sign ou similar); prazo de 7 dias úteis para fechamento
- **Execução → Retainer:** oferecer nos últimos 30 dias de execução da tese principal

---

## 4. Canais

### 4.1 Outbound frio (prioridade 1)

**Base de prospecção:** lista de CNPJs por CNAE + porte (a Receita Federal disponibiliza, e o Gabriel já tem planilhas de empresas enriquecidas em `Downloads/lista_empresas_enriquecida.xlsx` — pode ser reaproveitada).

**Canais:**
- **E-mail** para e-mail corporativo do sócio/financeiro/contador interno
- **WhatsApp Business** para número do responsável (mais efetivo que e-mail em PME)
- **LinkedIn** DM para sócios de empresas médias/grandes

**Scripts prontos** na aba Script de Abordagem — 5 tipos já escritos:
1. Tema 69 (ICMS × PIS/COFINS) — e-mail/WhatsApp
2. INSS Indenizatórias — e-mail/LinkedIn
3. Planejamento de regime — WhatsApp/e-mail
4. Retainer — LinkedIn/e-mail
5. Holding — indicação/LinkedIn

**Cadência sugerida por prospect:**
- Dia 0: mensagem 1 (tese principal do CNAE)
- Dia 3: mensagem 2 (reforço com número estimado)
- Dia 7: mensagem 3 (case study — parecer Cedro anonimizado)
- Dia 14: remover da cadência se sem resposta

### 4.2 Conteúdo orgânico (prioridade 2 — autoridade)

**Canal principal:** LinkedIn institucional da Renegocia (perfil de empresa). Quando stakeholders técnicos forem definidos, somar perfis pessoais deles como amplificadores.

**Formatos validados:**
- **Informativos de decreto/legislação** no estilo do PDF "Decreto 12.875/2026" — 300-500 palavras, explicando impacto prático em 5 minutos. Frequência: 2x/mês (sempre que sair decreto/MP/tema STF relevante).
- **Cases didáticos** anonimizados: "Posto de combustíveis em Sorocaba com R$ 35k/ano em créditos não aproveitados — aqui está o roteiro" (baseado no parecer Cedro).
- **Respostas à FAQ do portfólio** — cada pergunta da aba FAQ da planilha vira um post curto.

**Frequência mínima:** 2 posts/semana no LinkedIn.

### 4.3 Anúncios pagos (prioridade 3 — depois de validar tração orgânica)

**LinkedIn Ads:** públicos por CNAE + porte + cargo (sócio, CFO, controller). Criativos com tese específica + gancho numérico ("Setor industrial: até 2,5% do faturamento em PIS/COFINS recuperáveis").

**Google Ads:** palavras-chave transacionais: "recuperar PIS COFINS", "Tema 69 STF posto combustível", "advogado tributário Sorocaba", "exclusão ICMS PIS COFINS como fazer".

**Meta (Facebook/Instagram):** remarketing para quem visitou o site, não para tráfego frio — audiência PJ não está ativamente procurando lá.

### 4.4 Indicações e parcerias (prioridade 2 — ROI alto)

**Parceiros-alvo:**
- Contadores (fonte de indicação natural — eles não fazem tributário litigioso)
- Associações setoriais (sindicatos de postos, associações comerciais locais)
- Escritórios de contabilidade de porte médio em Sorocaba e São Paulo

**Contrapartida:** split de honorários (20-30% sobre êxito para o indicador, ou fee fixo por indicação convertida).

---

## 5. Site — gaps identificados e recomendações

### Pontos fortes do site atual
- `ContactSection.tsx` — formulário de qualificação em 3 passos com 6 situações mapeadas às teses é excelente. Webhook integrado em `webhooks-mvp.algomaisacai.com.br`.
- Copy "você só paga se houver resultado" alinhada com modelo de êxito.
- Design limpo, shadcn/ui + Tailwind + framer-motion — manutenção fácil.

### Gaps críticos (corrigir antes de rodar anúncios)
1. **WhatsApp placeholder** — `Hero.tsx:71` e `WhatsAppButton.tsx:5` usam `5500000000000`. Trocar pelo número comercial definido pelo Gabriel. *⚠️ bloqueia fluxo principal.*
2. **15 teses viraram 4 serviços genéricos** — `SolutionSection.tsx` tem "Recuperação, Planejamento, Holdings, Defesa". Perde a força numérica. Sugestão: criar seção nova "Principais teses" destacando as 4 🔴 com ticket estimado e fundamento legal.
3. **Falta autoria visível** — `AuthoritySection.tsx` é abstrato. Pendente até stakeholders técnicos serem definidos. Enquanto isso, manter texto institucional ("equipe especializada em tributário") sem personificação.
4. **Stats genéricos** — `StatsSection.tsx` mostra "5+ anos, 3 regimes, 12+ setores" (vago). Trocar por algo concreto quando houver números reais: "R$ [X] em créditos identificados", "[N] CNAEs atendidos", "[M] processos em andamento". Fonte dos números = Gabriel.
5. **Sem case study** — o parecer Cedro é uma arma subutilizada. Criar página `/cases/posto-combustivel-sorocaba` com recorte anonimizado (R$ 35k PIS/COFINS + R$ 107k INSS/PAT identificados).
6. **FAQ muito superficial** — `FaqSection.tsx` tem 4 perguntas básicas. A aba FAQ da planilha tem 15 perguntas técnicas por tese — puxar pelo menos 8 delas.

### Oportunidades (iteração 2)
- **Simulador de crédito** como lead magnet: replicar a lógica da aba Simulador da planilha de Precificação em React. Usuário digita faturamento + regime + setor → devolve estimativa de crédito potencial + botão "Quero diagnóstico detalhado".
- **Blog/centro de conteúdo** para os informativos estilo "Decreto diesel" — serve SEO e nutre leads frios.
- **Página por tese** (SEO): `/teses/tema-69-icms-pis-cofins`, `/teses/inss-verbas-indenizatorias`, etc. — ranqueia para pesquisa transacional.

---

## 6. Métricas a acompanhar

**Topo do funil:**
- Visitas no site / semana
- Taxa de conversão do form (3-step contact) — alvo inicial: 3-5% dos visitantes
- Respostas de outbound (e-mail, WhatsApp, LinkedIn) — alvo: 5-10% de taxa de resposta

**Meio do funil:**
- Diagnósticos agendados / semana
- Show-rate (compareceram ao diagnóstico agendado) — alvo: > 70%
- Propostas enviadas / diagnóstico

**Fundo:**
- Taxa de fechamento proposta → contrato — alvo: 25-40% (tributário tem ciclo longo)
- Ticket médio fechado
- Upsell retainer após tese principal — alvo: 15-25%

---

## 7. Próximos passos (ordenados)

1. **[Crítico, 1h]** Corrigir número WhatsApp em `Hero.tsx` e `WhatsAppButton.tsx`
2. **[Alta, 4h]** Reescrever `SolutionSection.tsx` destacando as 4 teses 🔴 com ticket e fundamento
3. **[Alta, 2h]** Substituir `StatsSection.tsx` por números reais (pedir ao Gabriel)
4. **[Bloqueado]** Seção "Quem somos / responsável técnico" — pendente até stakeholders serem definidos
5. **[Média, 6h]** Expandir `FaqSection.tsx` com 8 perguntas técnicas da planilha
6. **[Média, 1 dia]** Case study Cedro anonimizado em página dedicada
7. **[Média, 2 dias]** Simulador de crédito como lead magnet
8. **[Alta, contínuo]** Setup de outbound: lista CNPJs + sequência de 3 mensagens por tese + Calendly
9. **[Alta, contínuo]** 2 posts/semana LinkedIn institucional da Renegocia (informativos + FAQ); quando stakeholders definidos, replicar nos perfis pessoais

---

## 8. Perguntas em aberto (decidir com o Gabriel)

- **Stakeholders técnicos** — advogados e/ou contadores parceiros que vão executar as teses. Definir antes de qualquer copy que personalize autoria.
- Número oficial do WhatsApp a expor no site
- Calendly ou equivalente já configurado? Qual link?
- Perfil de LinkedIn institucional da Renegocia existe? (precisa antes de começar conteúdo orgânico)
- Orçamento mensal para anúncios? (define se Fase 4.3 é 3 meses ou 12 meses)
- Quer manter o site no Lovable (edição visual) ou vai passar a editar direto no código? (define workflow de edits pós-MVP)
- Há lista de clientes/casos reais além do Cedro para virarem case studies?
