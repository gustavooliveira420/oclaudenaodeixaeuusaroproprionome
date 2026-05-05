# Como trabalhar em paralelo no projeto Renegocia

Guia para Gabriel e Gustavo trabalharem juntos no mesmo repositório, sem se atrapalhar. Linguagem leiga.

## Mapa mental

```
                ┌─────────────────────────┐
                │    GitHub (na nuvem)    │
                │   versão "oficial"      │
                └────────┬────────────────┘
                         │
           ┌─────────────┴─────────────┐
           │                           │
           ▼                           ▼
   ┌──────────────┐           ┌──────────────┐
   │ Computador   │           │ Computador   │
   │ do Gabriel   │           │ do Gustavo   │
   │              │           │              │
   │ + Claude     │           │ + Claude     │
   └──────────────┘           └──────────────┘
```

Cada um tem uma cópia local. O GitHub é o "mestre" — é dele que vocês baixam (pull) e pra ele que vocês mandam (push) as mudanças.

## Os 3 comandos que você precisa saber

Não precisa decorar — instala o **GitHub Desktop** que tem botão pra cada um. Mas é bom entender o que cada um faz:

| Comando | O que faz | Quando usar |
|---|---|---|
| `git pull` | Baixa do GitHub o que o outro fez | **Antes** de começar a trabalhar |
| `git commit` | "Salva" suas mudanças no histórico local | Quando termina uma parte do trabalho |
| `git push` | Envia teus commits pro GitHub | **Depois** de terminar |

## A rotina diária ideal

### Quando você vai começar a trabalhar (manhã, ou retomada)

1. Abre o GitHub Desktop (ou o terminal)
2. Clica em **"Fetch origin"** depois **"Pull origin"** (ou roda `git pull`)
3. Confere se baixou alguma coisa nova (vai aparecer mensagem)
4. **Pronto.** Agora pode abrir o projeto no Claude/VS Code

### Durante o trabalho

Faça **commits pequenos** sempre que terminar uma coisa. Não acumula.

Exemplo de bons commits:
- "Atualizou copy do hero"
- "Adicionou tese de holding na seção de serviços"
- "Corrigiu número do WhatsApp"

Exemplo de commit ruim:
- "Várias coisas" (não dá pra entender o que foi)

### Quando você vai parar (almoço, fim do dia)

1. Confere que está tudo commitado (no GitHub Desktop, não pode ter coisa em "Changes")
2. Clica em **"Push origin"** (ou roda `git push`)
3. **Avisa o outro:** "Acabei de mexer em X, dá um pull aí quando for trabalhar"

## Como evitar conflitos (a parte chata do Git)

Conflito acontece quando os dois mexem na **mesma linha do mesmo arquivo** sem dar pull antes. O Git pede pra escolher manualmente qual versão fica. Pra leigo, é confuso.

### Estratégia 1 — Dividir áreas (mais fácil)

Combina antes de começar:
- Gabriel: site (`src/`) + plano de marketing
- Gustavo: playbooks comerciais + outbound

Enquanto cada um mexe na sua área, **conflito é praticamente zero**.

### Estratégia 2 — Trabalhar em horários diferentes

Se for inevitável os dois mexerem nos mesmos arquivos:
- Combina turnos (manhã / tarde)
- O da tarde **sempre** dá pull antes de começar

### Estratégia 3 — Avisar no WhatsApp

Antes de mexer numa parte sensível, avisa o outro: "Vou mexer no playbook 01 agora, espera 30 min antes de mexer também."

### O que fazer se der conflito

1. **Não entra em pânico.** Não perdeu nada.
2. Chama o Gabriel/Gustavo (quem tiver mais experiência com Git no momento)
3. Ou pede ajuda pro Claude: "Deu conflito de merge no arquivo X, me ajuda a resolver"
4. Em último caso, **descarta tuas mudanças locais** e refaz com a versão do GitHub:
   ```
   git stash
   git pull
   ```
   (você perde o que estava trabalhando, mas o repo fica limpo)

## O Claude do outro NÃO sabe o que aconteceu no seu Claude

Importante: a memória pessoal do Claude (preferências, conversas anteriores) fica **só no seu computador**. Quando o Gustavo abrir o Claude dele no projeto, ele começa "do zero" — só lê o que está nos arquivos do repo.

Por isso:
- **Decisões importantes do projeto** vão pro `CLAUDE.md` na raiz (o Claude sempre lê)
- **Documentos e roteiros** vão pra `docs/`
- **Conversas pontuais com seu Claude** ficam só com você (e tudo bem)

Se você ensinou alguma coisa importante pro seu Claude que o Gustavo precisa saber, **escreva no CLAUDE.md** ou em algum doc de `docs/` e commita.

## Setup inicial — passo a passo (Gustavo)

1. **Instala Git** — https://git-scm.com/download/win (next, next, next)
2. **Instala GitHub Desktop** — https://desktop.github.com/ (interface gráfica, evita terminal)
3. **Cria conta no GitHub** se não tiver — https://github.com
4. **Pede pro Gabriel te adicionar como collaborator** no repo `renegociaconsultoria`
5. **Aceita o convite** que chega no e-mail
6. **No GitHub Desktop:** File → Clone Repository → escolhe `GabrielMendesIA/renegociaconsultoria` → escolhe pasta no seu computador
7. **Instala o Claude Code** — https://claude.com/claude-code
8. **Abre a pasta clonada no Claude** — pronto, o Claude vai ler o `CLAUDE.md` automaticamente e fica no contexto do projeto

## Glossário rápido

- **Repo / repositório** — pasta do projeto versionada (no caso, no GitHub)
- **Clone** — fazer uma cópia local do repo
- **Pull** — baixar mudanças do GitHub
- **Push** — enviar mudanças pro GitHub
- **Commit** — salvar um conjunto de mudanças no histórico
- **Conflict / conflito** — quando dois commits mexeram no mesmo lugar e o Git não sabe qual fica
- **Branch** — uma "linha do tempo" alternativa do projeto. Por enquanto vocês vão usar só a `main` (a principal)
- **Collaborator** — pessoa adicionada ao repo com permissão de push

## Quando algo der errado

| Problema | O que fazer |
|---|---|
| Esqueci de dar pull e dei conflito | Pede ajuda pro Claude: "deu conflito, me ajuda" |
| Commitei errado | `git reset --soft HEAD~1` (desfaz o último commit, mantém as mudanças) — ou pergunta pro Claude |
| Apaguei um arquivo sem querer | `git checkout HEAD -- nome-do-arquivo.md` |
| Não consigo dar push (rejected) | Roda pull primeiro, resolve o que aparecer, tenta push de novo |
| Tudo travou e tô perdido | **Para tudo, chama o outro, e olha o histórico no site do GitHub** — o GitHub guarda toda versão antiga, você nunca perde nada permanentemente |

## Combinados deste projeto

1. ✅ Sempre `pull` antes de começar a trabalhar
2. ✅ Commits pequenos, com mensagem descritiva
3. ✅ `push` ao terminar (não dorme com mudança não-empurrada)
4. ✅ Decisões de projeto vão pro `CLAUDE.md` ou `docs/`
5. ✅ Antes de mexer em arquivo crítico, avisa no WhatsApp
6. ✅ Em caso de dúvida sobre Git, pergunta antes de tentar coisa destrutiva
