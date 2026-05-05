# Playbook 01 — Lead inbound (form do site)

Quando usar: um prospect preencheu o formulário de contato no site e os dados chegaram no CRM/planilha via webhook.

## O que o form capturou

Passo 1 (contato):
- Nome, e-mail, telefone/WhatsApp, empresa

Passo 2 (perfil do negócio):
- **Setor** (Varejo, Indústria, Serviços, Agronegócio, Setor Financeiro)
- **Regime tributário** (Simples, Presumido, Real, Não tenho certeza)
- **Faixa de faturamento mensal** (até R$ 100k / R$ 100k-500k / R$ 500k-2MM / acima R$ 2MM)

Passo 3 (situações marcadas — pode ter múltiplas):
- `planejamento` — "Nunca fizemos (ou faz mais de 2 anos) estudo comparando Simples/Presumido/Real"
- `inss` — "Folha de pagamento alta (acima de R$ 100k) com PLR, aviso-prévio, auxílios"
- `pis_cofins` — "Alto volume de compras mensais de insumos, energia, fretes"
- `icms_st` — "Trabalhamos com revenda e pagamos ICMS-ST"
- `refis` — "Temos débitos de impostos em aberto, queremos parcelamento"
- `holding` — "Sócios com patrimônio relevante pensando em sucessão/proteção"

## Passo 1 — Triagem (primeiros 30 minutos)

Abra o registro no CRM. Cheque os 3 sinais de aderência:

### ✅ Sinais verdes (seguir em frente)
- Regime: Presumido, Real ou "Não tenho certeza"
- Faturamento: acima de R$ 100k/mês
- Alguma situação marcada no Passo 3

### 🟡 Sinais amarelos (seguir com cautela)
- Simples Nacional + faturamento acima de R$ 400k/mês → pode ser caso de planejamento de regime
- Simples Nacional + marcou `icms_st` ou `refis` → algumas teses funcionam mesmo no Simples

### ❌ Sinais vermelhos (descartar educadamente)
- Simples Nacional + faturamento abaixo de R$ 100k/mês + nenhuma situação marcada
- Pessoa física buscando consultoria pessoal (não é o foco da Renegocia)

**Ação:** para leads amarelos/vermelhos, responder com template de descarte educado (ver fim do playbook). Para verdes, seguir ao Passo 2.

## Passo 2 — Primeiro contato (dentro de 2h úteis)

Canal preferido: **WhatsApp** (maior taxa de resposta que e-mail). Se não tiver WhatsApp declarado, e-mail. Se for lead grande, LinkedIn DM também.

### Script base (WhatsApp)

> Olá, [Nome]! Aqui é a [Seu nome], da Renegocia. Recebemos sua solicitação de diagnóstico gratuito agora pouco — obrigado pelo interesse.
>
> Rodei uma pré-análise rápida com base no que você informou ([setor] + [regime] + faturamento na faixa de [faixa]), e vi que as situações que você marcou abrem pelo menos [N] frentes de revisão tributária.
>
> Pra gente aproveitar o diagnóstico direito (30-45 min, sem custo), preciso só agendar um horário com você e nosso responsável técnico. Tem disponibilidade essa semana ou prefere semana que vem?

### Personalização por situação marcada

Logo depois do cumprimento, insira **um** parágrafo específico da situação mais quente marcada:

**Se marcou `planejamento`:**
> Você indicou que não tem feito estudo recente comparando regimes tributários. Esse é o pilar do diagnóstico — muitas PMEs no Presumido pagam 15-30% a mais do que pagariam no Real ou vice-versa.

**Se marcou `inss`:**
> Com folha acima de R$ 100k/mês e verbas como PLR ou aviso-prévio, costuma haver crédito de INSS recuperável relevante (decisão do STJ permite pedir de volta os últimos 5 anos). É uma das frentes mais rápidas.

**Se marcou `pis_cofins`:**
> Alto volume de compras de insumos + PIS/COFINS é um clássico. O STJ ampliou o conceito de insumo em 2018 — muitas empresas ainda não atualizaram a apuração. Pode haver 5 anos de crédito pra recuperar.

**Se marcou `icms_st`:**
> Quem paga ICMS-ST e vende abaixo do preço presumido pelo fisco tem direito ao ressarcimento da diferença (STF, Tema 201). Varejo farmacêutico, autopeças, bebidas — funciona bem.

**Se marcou `refis`:**
> Se vocês têm débitos abertos, hoje temos programas de parcelamento que podem reduzir juros e multas em até 100%. O diagnóstico inclui simulação de qual programa é melhor pro caso.

**Se marcou `holding`:**
> Patrimônio relevante + sucessão pede estruturação de holding — além de proteger o patrimônio, reduz ITCMD (que em alguns estados chega a 8%) e simplifica distribuição de lucros.

### Se o cliente responder "me conta mais por aqui antes de marcar"

Responda com 2-3 mensagens curtas:
1. Como funciona o diagnóstico ("30-45 min, você traz 12 meses de DRE/faturamento, a gente devolve número estimado de crédito ou economia")
2. Modelo comercial ("honorários são majoritariamente de êxito — se não recuperar, não paga")
3. Próximo passo sugerido ("posso te mandar o link do Calendly agora ou combinamos um horário direto?")

## Passo 3 — Se não responder em 24h

Segunda mensagem (WhatsApp):

> Oi [Nome], tudo bem? Só dando uma puxada pra ver se conseguiu pensar no diagnóstico. Rapidinho: [valor estimado conservador, calculado com o Simulador] é uma estimativa de piso pro que [Empresa] pode revisar. Tem 10 min esta semana pra gente conversar?

Se não responder em 48h (terceira e última mensagem):

> [Nome], última tentativa por aqui. Se não for o momento, sem problema — me avisa que te contato daqui 60 dias. Se mudar de ideia antes, chama direto. Abraço!

Depois disso: marcar como "nutrição" no CRM (receber conteúdo mensal, re-abordar em 60 dias).

## Passo 4 — Se aceitar, agendar

- Envie link do Calendly (ou horário proposto direto)
- Peça por mensagem: "Pra gente chegar na reunião com algo mapeado, me manda por aqui a DRE dos últimos 12 meses ou o faturamento mês a mês. Se tiver os últimos meses de SPED (o contador sabe o que é), manda também."
- No próprio CRM, agende a reunião e marque o lead como "Diagnóstico agendado"
- Escale para o stakeholder técnico — envie briefing curto (nome, empresa, setor, regime, faturamento, situações marcadas, data da reunião)

## Passo 5 — Véspera do diagnóstico

24h antes da reunião, WhatsApp de confirmação:
> Oi [Nome], só confirmando nosso papo amanhã às [hora]. Você conseguiu mandar a DRE? Se ficou apertado, a gente adapta — sem problema. Link da reunião: [link]

Se não respondeu em 12h → ligar (não perder no-show). Se confirmar, passar para o Playbook 02.

## Template — descarte educado

Use para leads vermelhos (Simples pequeno sem aderência, pessoa física, etc.):

> Olá [Nome], obrigado pelo interesse na Renegocia. Analisamos seu perfil e, com base no que você compartilhou, as frentes que trabalhamos hoje (recuperação de créditos e planejamento tributário) fazem sentido pra empresas em Lucro Presumido ou Real com volume de operações maior.
>
> Pro seu caso específico, o ROI do nosso trabalho seria baixo neste momento. Se a empresa crescer ou mudar de regime no futuro, estaremos aqui. Qualquer dúvida, pode me chamar por aqui. Sucesso!

## O que registrar no CRM após cada contato

- Data e canal do contato
- Resumo em 1 linha do que foi dito
- Próxima ação + data
- Status (Novo / Em contato / Agendado / Diagnóstico realizado / Proposta enviada / Fechou / Perdido / Nutrição)
- Situações marcadas no form (copiar do webhook)
- Qualquer dado adicional que o lead tenha compartilhado (CNPJ, contador, nome do sócio)
