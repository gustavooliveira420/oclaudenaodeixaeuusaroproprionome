# Renegocia Consultoria — guia para o Claude

Este arquivo é lido automaticamente pelo Claude quando você abre o projeto. Mantém todo Claude que entra no repo (de qualquer pessoa, em qualquer máquina) no mesmo nível de contexto.

## Sobre o time

- **Gabriel Mendes** — coordenação do projeto, marketing, site
- **Gustavo Oliveira** — co-responsável pelo projeto

Ambos não-técnicos em programação. Falar sempre em português claro, sem jargão. Se precisar usar termo técnico, explicar na hora numa frase.

## O que é a Renegocia

Consultoria tributária especializada em recuperação de créditos, planejamento fiscal e contencioso. Modelo comercial: honorários fixos baixos + êxito alto (15-35%) sobre valor recuperado. Porta de entrada = diagnóstico gratuito de 30-45 minutos.

**Stakeholders técnicos (advogados/contadores parceiros):** ainda em aberto. **Não personificar autoria** em copy, site ou propostas até definição. Os pareceres e materiais coletados (Cedro Auto Posto, decreto diesel, FRZZ) são exemplos/referências — não significam que o profissional que assinou é o responsável atual da Renegocia.

**Não confundir com:** Imunid (gestão de risco médico, projeto separado).

## Público-alvo

- Porte: PME a Grande, **não Simples Nacional** (foco em Lucro Presumido e Lucro Real)
- Segmentos quentes: comércio, indústria, distribuidoras, agronegócio, postos de combustíveis, saúde, TI, educação, setor financeiro (nicho CSLL)
- Filtro mínimo: faturamento mensal > R$ 100k

## Portfólio de 15 teses (resumo)

🔴 **Máxima prioridade:**
1. Exclusão ICMS da Base PIS/COFINS — Tema 69 STF — ticket R$ 15k-200k
2. Exclusão Incentivos ICMS do IRPJ/CSLL — Tema 1.182 STJ — R$ 20k-150k
3. Recuperação INSS Verbas Indenizatórias — R$ 10k-100k
4. Recuperação PIS/COFINS Insumos — Tema 779 STJ — R$ 15k-180k

🟠 **Alta prioridade:**
5. Planejamento Regime Tributário (Simples/LP/LR) — fixo R$ 3k-15k
6. Exclusão ISS da Base PIS/COFINS — R$ 10k-120k
7. ICMS-ST Ressarcimento — Tema 201 STF — R$ 5k-80k
8. Holding e Reestruturação Societária — fixo R$ 15k-80k

🟡 **Média prioridade:**
9. Revisão IRPJ/CSLL Lucro Real
10. Créditos de IPI Insumos
11. ITCMD Herança/Doação
12. Contencioso Administrativo (DRJ/CARF)
13. Parcelamento PERT/REFIS/RELP

🟢 **Estratégica (recorrência):** 14. Assessoria Mensal (Retainer) R$ 2,5k-15k/mês

🔵 **Nicho:** 15. CSLL Majoração Indevida (financeiro) R$ 30k-300k

Detalhes completos por tese (fundamento legal, ticket, êxito, FAQ de qualificação) estão em [docs/playbooks/99-glossario.md](docs/playbooks/99-glossario.md).

## Estrutura do repositório

```
renegocia/
├── CLAUDE.md                         # você está aqui
├── README.md                         # descrição padrão Lovable
├── src/                              # código React do site (editado via Lovable)
│   ├── pages/
│   └── components/landing/           # seções da landing page
├── docs/
│   ├── plano-marketing.md            # estratégia, segmentação, funil, canais
│   ├── colaboracao.md                # guia de pull/commit/push para leigos
│   └── playbooks/                    # 7 playbooks comerciais
│       ├── README.md
│       ├── 00-jornada-mapa.md
│       ├── 01-lead-inbound.md
│       ├── 02-diagnostico-gratuito.md
│       ├── 03-proposta-fechamento.md
│       ├── 04-outbound-frio.md
│       ├── 05-execucao-retencao.md
│       └── 99-glossario.md
└── package.json                      # dependências do site
```

## Stack do site

Vite + React + TypeScript + Tailwind + shadcn/ui + framer-motion. Editado primariamente via Lovable (https://renegociaconsultoria.lovable.app), versionado neste repo. Para rodar local: `npm install && npm run dev`.

## Decisões já tomadas

1. **Linguagem:** "consultoria tributária", nunca "advocacia tributária" no copy.
2. **Modelo comercial:** honorários majoritariamente de êxito é o diferencial. Sempre destacar.
3. **Porta de entrada:** diagnóstico gratuito de 30-45 minutos. Webhook do form do site já está integrado em `webhooks-mvp.algomaisacai.com.br`.
4. **Stakeholders técnicos:** em aberto — não criar copy personificada até definição.
5. **MVP:** publicado em 2026-04-24 via Lovable.
6. **Marca/domínio:** site institucional pendente (atual canonical é `henriquemelo.adv.br` — a substituir).

## Fontes autoritativas (fora do repo)

- `Downloads/Planilha Precificação Tributária rev16102025.xlsx` — tabela de honorários, simulador, template de proposta. **Apenas no computador do Gabriel** — quem precisar do conteúdo, perguntar a ele.
- `Downloads/17032026V1. Teses Tributárias (1).xlsx` — portfólio detalhado, FAQ de qualificação, matriz de priorização, scripts de abordagem. Idem.
- PDFs de referência (parecer Cedro Auto Posto, informativo decreto diesel 12.875/2026, mandado FRZZ): com Gabriel.

Pra que o conteúdo dessas fontes fique disponível pros dois Claudes: **converter as planilhas mais críticas em arquivos `docs/*.md` neste repo** sempre que necessário (já está parcialmente feito via playbooks e plano de marketing).

## Como pedir ajuda ao Claude neste projeto

- Para entender qualquer parte: "lê os playbooks e me explica X"
- Para escrever copy: "puxa o tom dos playbooks e escreve um post sobre Y"
- Para revisar site: "abre `src/components/landing/` e me diz se Z está bem implementado"
- Para criar nova peça (anúncio, e-mail, post): primeiro o Claude vai invocar a skill `brainstorming` para alinhar antes de escrever
- Para colaborar com o repo: ler [docs/colaboracao.md](docs/colaboracao.md) primeiro

## Regras transversais (CLAUDE.md global do Gabriel já cobre, mas vale lembrar aqui)

- Skill `brainstorming` antes de criar features/conteúdos novos
- Skill `simplify` após mudanças de código não-triviais
- Plan Mode (Shift+Tab) antes de tarefas com >3 arquivos ou decisão arquitetural
- `/clear` entre tarefas sem relação

## Próximas frentes em aberto

1. Definir stakeholder(s) técnico(s) parceiros — destrava copy autoral, autoria de pareceres, perfis no LinkedIn
2. Configurar CRM + Calendly + WhatsApp Business — destrava o Playbook 01 (lead inbound)
3. Domínio próprio (`renegocia.com.br` ou similar) — substituir canonical atual
4. Implementar gaps do site listados em `docs/plano-marketing.md` (WhatsApp real, seção de teses, case Cedro anonimizado, FAQ expandida, simulador)
5. Definir lista inicial de prospects para outbound (Playbook 04)

Histórico vivo do projeto: `git log` deste repo + memórias pessoais de cada Claude (não compartilhadas).
