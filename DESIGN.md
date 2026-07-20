---
name: Tomark
description: Conversor desktop de arquivos para Markdown — instrumento silencioso, plano por princípio.
colors:
  action-blue: "#2b6cb0"
  action-blue-dark: "#1f538d"
  action-blue-hover: "#1f538d"
  action-blue-hover-dark: "#164070"
  action-blue-ink: "#ffffff"
  surface-window-light: "#f2f2f2"
  surface-window-dark: "#1a1a1a"
  surface-panel-light: "#e5e5e5"
  surface-panel-dark: "#212121"
  surface-content-light: "#ffffff"
  surface-content-dark: "#333333"
  ink-light: "#1f1f1f"
  ink-dark: "#e6e6e6"
  muted-light: "#6b6b6b"
  muted-dark: "#9a9a9a"
  hint-light: "#666666"
  hint-dark: "#888888"
  disabled-light: "#a8adb2"
  disabled-dark: "#5a5d61"
  ghost-border-light: "#c8ccd0"
  ghost-border-dark: "#3a3d41"
  ghost-hover-light: "#ececec"
  ghost-hover-dark: "#2a2d31"
  row-selected-light: "#cfe3f7"
  row-selected-dark: "#264f78"
  row-hover-light: "#e6e6e6"
  row-hover-dark: "#333337"
  status-pending-light: "#5f5f5f"
  status-pending-dark: "#bdbdbd"
  status-running-light: "#0868a0"
  status-running-dark: "#5ec8ff"
  status-ok-light: "#257046"
  status-ok-dark: "#89cca2"
  status-error-light: "#be2626"
  status-error-dark: "#ffa6a6"
typography:
  body:
    fontFamily: "Roboto, SF Display, sans-serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.4
  mono:
    fontFamily: "Consolas, monospace"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.45
rounded:
  sm: "6px"
  md: "8px"
  full: "1000px"
spacing:
  xs: "2px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
components:
  button-primary:
    backgroundColor: "{colors.action-blue}"
    textColor: "{colors.action-blue-ink}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    height: "36px"
  button-primary-hover:
    backgroundColor: "{colors.action-blue-hover}"
  button-primary-disabled:
    textColor: "{colors.disabled-light}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.ink-light}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    height: "36px"
  button-ghost-hover:
    backgroundColor: "{colors.ghost-hover-light}"
  button-ghost-compact:
    height: "28px"
  button-icon:
    backgroundColor: "{colors.ghost-hover-light}"
    textColor: "{colors.ink-light}"
    rounded: "{rounded.sm}"
    height: "28px"
    width: "28px"
  list-row:
    backgroundColor: "transparent"
    textColor: "{colors.muted-light}"
    typography: "{typography.body}"
    rounded: "{rounded.sm}"
  list-row-hover:
    backgroundColor: "{colors.row-hover-light}"
  list-row-selected:
    backgroundColor: "{colors.row-selected-light}"
  preview:
    backgroundColor: "{colors.surface-content-light}"
    textColor: "{colors.ink-light}"
    typography: "{typography.mono}"
    rounded: "{rounded.sm}"
  progress:
    backgroundColor: "{colors.action-blue}"
    rounded: "{rounded.full}"
    height: "6px"
---

# Design System: Tomark

## 1. Overview

**Creative North Star: "The Quiet Instrument"**

Um instrumento silencioso é preciso sem ser chamativo. Não tem mostrador
decorativo, não comemora quando termina, e nunca deixa dúvida sobre o que está
acontecendo agora. Tomark é lido à distância — a fila diz seu estado, a barra
diz seu progresso, o rodapé diz o resultado — e nada nele pede para ser
admirado. PRODUCT.md coloca isso como primeiro princípio: *"A ferramenta some na
tarefa."* O sistema visual existe para tornar esse desaparecimento possível.

A densidade é baixa e deliberada. Duas colunas, uma barra superior, um rodapé.
Uma única ação preenchida na tela inteira; todo o resto vive em contorno
fantasma. A paleta é **Restrained** no sentido estrito do registro produto:
neutros tonais carregam praticamente toda a superfície, e a cor saturada aparece
em dois lugares apenas — a ação primária e os quatro estados da fila. Nada é
colorido por decoração.

O sistema rejeita, por nome, as quatro coisas que PRODUCT.md proíbe:
**ferramenta de dev** (nada de log verboso ou exceção crua na tela),
**conversor web cheio de anúncio** (nada de banner, upsell ou espera artificial),
**SaaS genérico** (nada de gradiente, card idêntico repetido ou ilustração 3D) e
**software corporativo dos anos 2000** (nada de barra de menus densa, toolbar de
ícones minúsculos ou cinza sobre cinza). Se um elemento novo não sobrevive a
esses quatro testes, ele está errado antes de ser bonito.

**Key Characteristics:**
- Um único botão preenchido por tela; todo o resto é fantasma ou texto
- Todo token de cor é um par claro/escuro — o tema troca sozinho, sem exceção
- Zero sombras, zero bordas estruturais: profundidade só por degrau tonal
- Uma família tipográfica para tudo, mono reservada exclusivamente ao conteúdo convertido
- Cor saturada apenas em ação primária e estado; nunca em decoração

## 2. Colors

Neutros tonais em três degraus carregam a superfície inteira; o azul aparece
para dizer "aja aqui" e a família de estado aparece para dizer "isto aconteceu".

### Primary

- **Action Blue** (`#2b6cb0`, hover `#2c7bd0`, texto `#ffffff`): a única cor
  preenchida da interface, exclusiva do botão Converter e da barra de progresso.
  Existe para que a próxima ação seja localizável sem leitura. Nunca aparece em
  borda, fundo de painel, ícone decorativo ou texto corrido.

### Secondary

- **Status Running** (`#0a7ec2` claro / `#4cc2ff` escuro): o arquivo sendo
  convertido agora. Irmão do Action Blue por hue, distinto por função — azul de
  ação é onde você clica, azul de estado é o que a máquina está fazendo.
- **Status OK** (`#2e8b57` claro / `#4caf72` escuro): conversão concluída e `.md`
  gravado em disco.
- **Status Error** (`#c62828` claro / `#ff6b6b` escuro): a conversão falhou. É a
  única cor que autoriza o usuário a parar e ler.

### Neutral

- **Ink** (`#1f1f1f` claro / `#e6e6e6` escuro): todo texto que precisa ser lido
  sem esforço — rótulo de botão, nome de arquivo, conteúdo do preview. É o piso
  de legibilidade do sistema (14.7:1 e 13.9:1).
- **Muted** (`#6b6b6b` claro / `#9a9a9a` escuro): informação de apoio que
  acompanha sem competir — contador de arquivos, linha de status do rodapé.
- **Hint** (`#666666` claro / `#888888` escuro): instrução do estado vazio.
  Passa 4.6:1 e 4.5:1 contra o painel. Travado por `app/test_contrast.py`.
- **Disabled** (`#a8adb2` claro / `#5a5d61` escuro): rótulo de controle inativo.
  Isento do mínimo de contraste por WCAG 1.4.3, mas fraco até como apagado.
- **Ghost Border** (`#c8ccd0` claro / `#3a3d41` escuro): contorno de 1px que dá
  forma a toda ação secundária sem preenchê-la.
- **Surfaces**, do fundo ao topo: janela (`#f2f2f2` / `#1a1a1a`), painel
  (`#e5e5e5` / `#212121`), conteúdo (`#ffffff` / `#333333`).
- **Row Selected** (`#cfe3f7` claro / `#264f78` escuro) e **Row Hover**
  (`#e6e6e6` claro / `#333337` escuro): estado da linha na fila.

### Named Rules

**The Paired Token Rule.** Toda cor do sistema é um par `(claro, escuro)` e o
tema troca sozinho. Uma cor declarada como string única é um bug, não um atalho
— hoje o Action Blue é o único infrator, e é por isso que ele é o único elemento
que não responde ao tema.

**The One Fill Rule.** Existe exatamente um elemento preenchido com cor saturada
por tela: a ação primária. Se um segundo aparecer, um dos dois está errado.

**The Earned Color Rule.** Cor saturada é permitida em ação primária e em estado
de item. Em qualquer outro lugar — fundo, borda, ícone, cabeçalho, separador —
é proibida.

**The Single Accent Rule.** O sistema tem um azul de ação, não dois. O botão
Converter e a barra de progresso usam o mesmo token `ACTION`; o acento herdado
do tema `dark-blue` não aparece em lugar nenhum.

**The Darkening Hover Rule.** Hover escurece, nunca clareia. Clarear o CTA
derrubava o texto branco para 4.33:1 — abaixo de AA no exato momento em que o
usuário está mirando o botão. Vale para todo controle preenchido.

## 3. Typography

**Body Font:** Roboto (com SF Display no macOS, fallback sans-serif)
**Label/Mono Font:** Consolas (com `monospace` no X11/Wayland)

**Character:** Uma família para toda a interface, uma para o conteúdo. Não há
par tipográfico e não deve haver: interface de produto não precisa de contraste
display/corpo, e um instrumento silencioso não tem voz tipográfica própria. A
mono não é estética — ela marca a fronteira entre *o app falando* e *o seu
arquivo convertido*.

### Hierarchy

- **Body** (400, 13px, 1.4): tudo na interface. Rótulo de botão, nome de arquivo
  na fila, contador, linha de status. Um único tamanho para toda a UI é
  intencional — a hierarquia aqui vem de cor e posição, não de escala.
- **Mono** (400, 12px, 1.45): exclusiva do painel de preview. Um grau menor que
  o corpo porque carrega texto longo e se beneficia da densidade.

### Named Rules

**The One Size Rule.** A interface tem um tamanho de texto. Hierarquia se faz
com peso, cor e posição. Introduzir um segundo tamanho de UI exige justificar
por que cor e posição falharam.

**The Mono Border Rule.** Monoespaçada significa "isto é o seu conteúdo, não a
nossa opinião". Usar mono em rótulo, botão, status ou mensagem de erro apaga
essa fronteira e é proibido.

## 4. Elevation

O sistema é **plano por princípio, em camadas por função**. Não há uma única
sombra na interface, e `border_width` é zero em todos os componentes. A
profundidade é comunicada exclusivamente por degrau tonal, e cada degrau
significa uma coisa específica: a janela é o fundo, o painel é onde o trabalho
se organiza, o conteúdo é o que você veio ver.

A escada, do fundo ao topo:

| Degrau | Claro | Escuro | Papel |
|---|---|---|---|
| Janela | `#f2f2f2` | `#1a1a1a` | Plano de fundo; barra superior e rodapé flutuam nele |
| Painel | `#e5e5e5` | `#212121` | A fila de arquivos; contêiner de trabalho |
| Conteúdo | `#ffffff` | `#333333` | O preview do Markdown; o destino da leitura |

Note que a escada **inverte** entre os temas: no claro ela sobe em direção ao
branco, no escuro ela sobe em direção ao cinza mais claro. Isso é correto — o
degrau significa proximidade do conteúdo, não luminosidade absoluta.

### Shadow Vocabulary

Nenhum. Deliberadamente vazio.

### Named Rules

**The No Shadow Rule.** Sombra é proibida. Não há elevação "sutil", não há
`box-shadow` de card, não há glow em foco. Se um elemento precisa se destacar,
ele sobe um degrau tonal ou ganha contorno de 1px — nunca uma sombra.

**The Meaningful Step Rule.** Cada degrau tonal carrega significado. Um quarto
degrau só é permitido se representar uma quarta camada real de informação.
Degrau por variedade visual é proibido.

**The Flat Test.** Se a interface parece ter sido desenhada em 2014, a sombra
que você acabou de adicionar é o motivo. Remova-a.

## 5. Components

### Buttons

- **Shape:** cantos suavemente arredondados (8px) nos botões próprios do app;
  6px é o padrão herdado do CustomTkinter e aparece nas linhas da fila, no
  preview e no botão de ícone. **Essa divergência é dívida** — 8px é o valor
  escolhido e deveria valer para todos.
- **Primary:** preenchido em Action Blue (`#2b6cb0`) com texto branco, 36px de
  altura. Um por tela. Ancorado à direita da barra superior.
- **Hover / Focus:** hover clareia para `#2c7bd0`. Não há tratamento de foco
  distinto — lacuna conhecida contra a meta WCAG AA de PRODUCT.md.
- **Ghost:** fundo transparente, contorno de 1px em Ghost Border, texto em Ink,
  36px de altura (28px no rodapé, onde a ação é terciária). Toda ação que não é
  a primária mora aqui: Selecionar arquivos, Limpar, Abrir pasta, alternar tema.
- **Icon:** 28×28px, raio 6px, fundo em Ghost Hover. Só o botão de copiar, que
  se sobrepõe ao canto superior direito do preview e só existe quando há
  Markdown para copiar.
- **Disabled:** o texto vai para Disabled; o preenchimento permanece. Um botão
  desabilitado nunca some da tela — o usuário precisa saber que a ação existe.

### List Rows

O componente mais carregado do sistema. Cada linha é um botão de largura total,
alinhado à esquerda, raio 6px, fundo transparente em repouso.

- **Badge + nome:** um glifo de estado (`•` pendente, `⟳` convertendo, `✓` ok,
  `✕` erro) seguido do nome do arquivo.
- **Hover:** fundo vai para Row Hover.
- **Selected:** fundo vai para Row Selected (`#cfe3f7` / `#264f78`).
- **Estrutura:** três widgets, não um. Um `CTkButton` tem um único
  `text_color`, e usá-lo pintava o nome do arquivo com a cor do estado
  (3.02–3.52:1). A linha é um frame com dois labels: badge colorido, nome
  sempre em Ink. Clique e hover são ligados nos três.

### Preview

- **Style:** superfície de conteúdo (`#ffffff` / `#333333`), raio 6px, sem
  borda, tipografia mono, quebra por palavra.
- **State:** somente leitura. Recebe o Markdown convertido, a mensagem de erro,
  ou o texto de espera "Ainda não convertido."
- **Overlay:** o botão de copiar ancora no canto superior direito, deslocado
  38px para não cobrir a barra de rolagem, e confirma com troca de glifo
  (`⧉` → `✓`) por 1200 ms.

### Progress

- **Style:** barra de 6px, cantos totalmente arredondados, largura total.
- **Behavior:** não existe em repouso. É inserida acima do rodapé quando o lote
  começa e removida quando termina. Progresso determinado (`done / total`),
  nunca indeterminado.

### Empty State

Texto centralizado em Hint, 24px de respiro vertical, com a instrução em duas
linhas: o gesto primário (arrastar) e o alternativo (o botão). Some no instante
em que o primeiro arquivo entra na fila.

### Named Rules

**The Ghost Default Rule.** Um controle novo nasce fantasma. Preenchê-lo exige
provar que ele é a ação primária — e como só existe uma, a resposta é quase
sempre não.

**The Silent Success Rule.** Sucesso é comunicado por mudança de estado, nunca
por interrupção. Sem diálogo modal de "pronto!", sem toast, sem som. A linha
vira `✓`, o rodapé conta quantos.

## 6. Do's and Don'ts

### Do:

- **Do** declarar toda cor como par `(claro, escuro)`, sem exceção. O tema troca
  sozinho e a exceção é sempre o elemento que quebra.
- **Do** usar Ink (`#1f1f1f` / `#e6e6e6`) em todo texto que precisa ser lido.
  Cor de estado pertence ao badge, não ao nome do arquivo.
- **Do** manter um único elemento preenchido em cor saturada por tela.
- **Do** atingir 4.5:1 em texto e 3:1 em elemento gráfico de interface — a meta
  WCAG 2.1 AA que PRODUCT.md fixa. Meça, não estime.
- **Do** comunicar profundidade por degrau tonal, e só quando o degrau significa
  uma camada real de informação.
- **Do** usar progresso determinado (`3/7`) sempre que o total for conhecido.
- **Do** reservar a monoespaçada para o conteúdo convertido do usuário.
- **Do** manter foco de teclado visível e rastreável, inclusive depois da lista
  ser reconstruída.

### Don't:

- **Don't** adicionar sombra. Nenhuma, em lugar nenhum, em intensidade nenhuma.
- **Don't** parecer **ferramenta de dev**: nada de log verboso, jargão, terminal
  embutido ou exceção crua de Python na tela. O preview mostrando `str(e)` hoje
  viola isto diretamente.
- **Don't** parecer **conversor web cheio de anúncio**: nada de banner, upsell,
  marca d'água, cadastro ou espera artificial.
- **Don't** parecer **SaaS genérico**: nada de gradiente, grid de cards
  idênticos, ilustração 3D ou onboarding de cinco telas.
- **Don't** parecer **software corporativo dos anos 2000**: nada de barra de
  menus densa, toolbar de ícones minúsculos, pilha de diálogos modais ou cinza
  sobre cinza.
- **Don't** introduzir um segundo azul de ação. O acento do tema `dark-blue`
  (`#3a7ebf` / `#1f538d`) não entra: `ACTION` é o único.
- **Don't** clarear um controle preenchido no hover. Escureça — clarear derruba
  o texto branco abaixo de AA.
- **Don't** ajustar uma cor sem rodar `python app/test_contrast.py`. Ele falha
  se qualquer par cair abaixo de 4.5:1 em qualquer um dos dois temas.
- **Don't** introduzir um segundo tamanho de texto de UI sem antes provar que
  cor e posição não resolvem a hierarquia.
- **Don't** interromper para anunciar sucesso. Sem modal, sem toast, sem som.
- **Don't** perguntar o que o app pode decidir sozinho — pasta de destino,
  confirmação de sobrescrita, formato de saída. PRODUCT.md trata isso como
  falha de design, não como flexibilidade.
- **Don't** inventar afordância para tarefa padrão. Barra de rolagem custom,
  controle de formulário estranho, modal não-nativo: o vocabulário é o do
  desktop Windows.
