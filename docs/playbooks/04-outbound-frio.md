# Playbook 04 — Outbound frio

Prospecção ativa — você aborda uma empresa que **não** conhece a Renegocia e não pediu contato. O objetivo é despertar interesse em uma tese específica (não vender a Renegocia genericamente) e agendar um diagnóstico gratuito.

## Princípio fundamental

**Uma mensagem = uma tese específica = uma hipótese de valor concreto.**

Errado: "Somos uma consultoria tributária, queria apresentar nossos serviços."
Certo: "Empresas do seu CNAE com faturamento na sua faixa costumam ter R$ X em créditos de PIS/COFINS não aproveitados — vale 30 min de conversa?"

## Construindo a lista de prospects

### Fontes disponíveis
- **`Downloads/lista_empresas_enriquecida.xlsx`** — 135KB, já tem CNPJs enriquecidos (Gabriel já tem)
- **`Downloads/Empresas com CNPJ.xlsx`** — 55KB
- **`Downloads/lista_empresas.xlsx`** — 114KB
- Receita Federal (consulta pública por CNAE + UF)
- Feiras setoriais (listas de expositores)
- LinkedIn Sales Navigator (se disponível)

### Filtros mínimos antes de abordar

1. **CNAE compatível com uma tese** — use a matriz de priorização (memória `reference_renegocia_portfolio.md`)
2. **Porte** — empresa de médio para grande (funcionários > 20, ou faturamento estimado > R$ 500k/mês)
3. **Regime tributário** — Presumido ou Real (checar na consulta pública do Simples Nacional)
4. **Contato identificado** — nome do sócio, CFO, diretor financeiro ou contador. Nunca abordar "empresa".

### Mapa CNAE × Tese (priorize nessa ordem)

| Setor / CNAE | Tese principal | Abordagem |
|---|---|---|
| Indústria de transformação (Div. C) | PIS/COFINS Insumos + IPI Insumos + Tema 69 | Script 1 (abaixo) |
| Comércio atacadista / distribuidoras | Tema 69 + ICMS-ST | Script 1 |
| Varejo farmacêutico, autopeças, bebidas | ICMS-ST Ressarcimento | Script 2 |
| Agronegócio | Tema 1.182 (incentivos ICMS) + holding | Script 3 |
| Postos de combustíveis | PIS/COFINS + caso Cedro como prova social | Script 4 |
| TI, saúde, educação, consultorias | ISS × PIS/COFINS | Script 5 |
| Qualquer setor com folha > R$ 100k | INSS Indenizatórias | Script 6 |

## Scripts por tese (prontos na planilha)

Fonte autoritativa: `Downloads/17032026V1. Teses Tributárias (1).xlsx`, aba **Script de Abordagem**. Adapte [COLCHETES] com dados reais.

### Script 1 — Tema 69 (Tese do Século)

**Canal:** e-mail ou WhatsApp
**Assunto:** Sua empresa pode ter crédito tributário com o Fisco

> Prezado(a) [Nome do sócio/gestor],
>
> Identifiquei que empresas do seu segmento (CNAE [CNAE]) com faturamento próximo ao de [Empresa] têm direito à recuperação de valores de PIS/COFINS pagos a maior, com base em decisão definitiva do Supremo Tribunal Federal (Tema 69 — RE 574.706/PR).
>
> Estimativa preliminar para empresas com faturamento semelhante: **R$ [X]** em créditos referentes aos últimos 5 anos, passíveis de compensação com tributos correntes.
>
> Sem custo inicial — honorários exclusivamente de êxito.
>
> Pode agendar 30 min pra uma análise gratuita?
>
> [Assinatura]

**CTA:** link do Calendly.

### Script 2 — ICMS-ST Ressarcimento (varejo)

**Canal:** e-mail ou WhatsApp

> Prezado(a) [Nome],
>
> [Empresa] atua como varejista/distribuidor em um setor regido pela Substituição Tributária do ICMS. Quando o preço efetivo de venda ao consumidor é menor do que o presumido pelo fisco, há direito a ressarcimento da diferença — decisão do STF no Tema 201.
>
> Empresas do seu porte costumam ter R$ [X] recuperáveis por ano, e o processo é administrativo (Secretaria da Fazenda estadual) — sem judicial.
>
> Posso mandar o passo a passo do diagnóstico? Sem compromisso.
>
> [Assinatura]

### Script 3 — Incentivos ICMS × IRPJ/CSLL (agronegócio, indústria incentivada)

> [Nome], [Empresa] recebe algum incentivo fiscal de ICMS do estado (crédito presumido, diferimento, redução de base)?
>
> Se sim, o STJ pacificou em 2023 (Tema 1.182) que esses incentivos não devem compor a base de IRPJ/CSLL — o que abre recuperação dos últimos 5 anos. Para empresas incentivadas, o valor costuma passar de R$ 100k.
>
> Faço uma simulação rápida se me mandar o decreto ou contrato do incentivo. 30 min de conversa é suficiente pra começarmos.
>
> [Assinatura]

### Script 4 — Postos de combustíveis (com caso Cedro)

> [Nome], no mês passado fechamos diagnóstico de um posto em [Sorocaba/região] com faturamento anual de ~R$ 12MM. Identificamos:
>
> - R$ 35k/ano em créditos de PIS/COFINS não aproveitados (energia, fretes, serviços)
> - R$ 107k recuperáveis em INSS sobre ticket refeição (fora do PAT)
> - Estudo de migração Presumido → Real com economia projetada de 5 dígitos/ano
>
> É um padrão que repete em postos de porte semelhante ao de [Empresa]. Agenda 30 min pra gente conversar?
>
> [Assinatura]

### Script 5 — ISS × PIS/COFINS (prestadores de serviço)

> [Nome], [Empresa] é tributada pelo ISS sobre os serviços que presta. Há uma tese forte no STF (RE 592.616, pendente de julgamento) para excluir o ISS da base de PIS/COFINS — análoga à "Tese do Século" já decidida.
>
> Quem ajuíza **antes** do julgamento definitivo costuma entrar na modulação favorável. Quem espera demais perde os créditos anteriores.
>
> Posso mandar material técnico? Se fizer sentido, agendamos 30 min.
>
> [Assinatura]

### Script 6 — INSS Verbas Indenizatórias

**Canal:** e-mail ou LinkedIn DM

> Prezado(a) [Nome],
>
> Empresas com folha de pagamento relevante frequentemente recolhem INSS a maior sobre verbas indenizatórias (aviso-prévio, PLR, auxílio-educação), por orientação conservadora do fisco. O STJ tem jurisprudência consolidada que permite contestar.
>
> Para uma empresa com porte de [Empresa], o potencial de crédito pode superar **R$ [X]** referentes aos últimos 5 anos.
>
> Diagnóstico gratuito da folha em 30 min. Te liga interesse?
>
> [Assinatura]

### Script 7 — Retainer (assessoria mensal)

**Canal:** LinkedIn ou e-mail (para sócios/CFOs de médio porte)

> [Nome], empresas que crescem sem assessoria tributária especializada ficam expostas a três coisas: autuações evitáveis, regime tributário subótimo e créditos deixados sobre a mesa.
>
> A Renegocia tem um modelo de assessoria mensal sob medida — monitoramento de legislação, revisão de apurações e suporte preventivo — a partir de R$ 2.500/mês fixo.
>
> Faz sentido 30 min de conversa pra eu entender a realidade de [Empresa]?
>
> [Assinatura]

### Script 8 — Holding patrimonial (sócios +50, patrimônio relevante)

**Canal:** LinkedIn / indicação

> Prezado(a) [Nome],
>
> Empresas e famílias com patrimônio relevante frequentemente arcam com tributação desnecessária na distribuição de lucros, transferência de bens entre gerações e eventual saída de sócios.
>
> Estruturar uma holding patrimonial-operacional gera: (1) redução imediata de ITCMD na sucessão, (2) proteção de patrimônio contra riscos empresariais, (3) simplificação na sucessão familiar.
>
> Análise preliminar sem custo. Vale 30 min?
>
> [Assinatura]

## Cadência padrão (por prospect)

| Dia | Ação | Canal | Conteúdo |
|---|---|---|---|
| D+0 | Mensagem 1 (tese específica) | Canal primário (e-mail ou WhatsApp) | Script acima |
| D+3 | Mensagem 2 (reforço com número) | Mesmo canal | Versão encurtada: "[Nome], só reforçando — empresas do seu setor recuperam em média R$ [X]. Vale mesmo 30 min?" |
| D+7 | Mensagem 3 (prova social / case) | Canal secundário (LinkedIn se tentou e-mail/WhatsApp) | Compartilhar case curto anonimizado ("Cliente do setor [X] recuperou R$ [Y] no ano passado") |
| D+14 | Mensagem 4 (última tentativa) | Qualquer canal | "[Nome], última mensagem minha — se não é o momento, sem problema. Te coloco na lista pra contato daqui 90 dias. Posso?" |
| D+90 | Re-abordagem | Canal primário | Começar cadência de novo com ângulo diferente (tese diferente ou novo ângulo) |

## Meta de volume (sugerida para 1 SDR em tempo integral)

- 30-40 prospects novos abordados por dia
- 3-5 agendamentos de diagnóstico por semana
- Taxa de resposta esperada: 5-10% (inclui respostas negativas)
- Taxa de conversão resposta → diagnóstico: 20-30%
- Ou seja: ~150-200 prospects por semana = 3-5 diagnósticos

## O que evitar

❌ **Não use o mesmo script pra todo mundo.** Cada mensagem tem que parecer escrita pra aquela empresa.
❌ **Não mande áudio no primeiro contato.** Pessoa fria não ouve áudio.
❌ **Não mande PDFs ou anexos na primeira mensagem.** Acaba em spam.
❌ **Não peça uma reunião antes de mostrar o valor** ("posso te apresentar nossos serviços?"). Mostre o valor primeiro, a reunião vem como consequência.
❌ **Não encadeie mais de 4 tentativas.** Vira perseguição, queima o contato.

## Ferramentas úteis

- **Apollo / Hunter** — encontrar e-mail de sócios por domínio
- **LinkedIn Sales Navigator** — filtro por empresa, cargo, região
- **WhatsApp Business** — etiquetas por etapa (Novo, Tentativa 1, Tentativa 2, Agendado, Nutrição)
- **Calendly** — link direto no primeiro contato, reduz fricção
- **CRM** — nome/horário do contato não pode depender da sua memória

## Cases e provas sociais a usar

Você pode citar **anonimizadamente** nos scripts:

1. **Posto de combustíveis em Sorocaba** (baseado no parecer Cedro) — R$ 35k PIS/COFINS + R$ 107k INSS identificados em diagnóstico inicial
2. [Adicionar cases conforme forem acontecendo]

Nunca cite cliente com nome sem autorização por escrito.
