# Product

## Register

product

## Platform

desktop

> Windows e Linux, Python + CustomTkinter. O schema do impeccable prevê apenas
> `web` / `ios` / `android` / `adaptive`; nenhum descreve esta superfície, e
> registrar `web` faria os comandos carregarem regras de CSS e viewport que não
> se aplicam a Tkinter. Nenhum livro de regras nativo (HIG, Material 3) vale
> aqui — as convenções que importam são as do desktop Windows.

## Users

Pessoa não-técnica de escritório que recebe PDFs, DOCXs e planilhas e precisa do
conteúdo em Markdown. Trabalha em máquina Windows corporativa, provavelmente sem
permissão de instalar nada, e nunca abriu um terminal — nem deveria precisar. O
trabalho a ser feito é curto e recorrente: pegar um arquivo que chegou por email
ou pasta compartilhada e obter o texto em Markdown, agora, sem virar um projeto.

Uma única audiência. Usuários técnicos podem usar o Tomark, mas não são para quem
as decisões são tomadas — quando os dois interesses conflitarem, o não-técnico
ganha.

## Product Purpose

Dar interface gráfica ao markitdown para que a conversão para Markdown não exija
linha de comando. Converte em lote, mostra o resultado antes do uso e grava o
`.md` ao lado do original. Tudo local, sem rede.

Sucesso é **fricção zero**: abrir, arrastar, pronto. O app acertou quando o
usuário não precisou pensar em nenhum momento — não escolheu pasta de destino,
não leu manual, não configurou nada, não decidiu o que fazer com um erro. Qualquer
passo que exija reflexão é falha de design, não do usuário.

## Positioning

O markitdown sem terminal. Mesmo motor de conversão da Microsoft, mesma qualidade
de saída, sem a barreira da linha de comando.

## Brand Personality

Discreto, direto, confiável. A ferramenta não tem voz própria e não deve querer
uma: nada de mascote, nada de tom animado, nada de celebrar a conversão de um
arquivo. Fala pouco, e o pouco que fala é literal — "3 arquivo(s)", "Convertendo…
2/7", "salvos ao lado do original". A meta emocional é confiança tranquila: o
usuário nunca deve se perguntar se algo deu errado silenciosamente.

Referência de clima: utilitários nativos do Windows, tipo PowerToys e a Ferramenta
de Captura. Familiares ao ponto de não serem notados, sem personalidade forçada, e
com a sensação de já fazerem parte do sistema em vez de terem sido instalados.

## Anti-references

Quatro coisas que o Tomark explicitamente não deve parecer:

**Ferramenta de dev.** Sem terminal embutido, sem log verboso, sem jargão, sem
exceção crua de Python na tela. Se o usuário precisa saber o que é um traceback
para entender a mensagem, a mensagem está errada.

**Conversor web cheio de anúncio.** Nada de cadastro, banner, upsell, marca
d'água ou espera artificial. Nada de "aguarde 30 segundos" quando não há motivo
para esperar.

**SaaS genérico.** Sem gradiente, sem grid de cards idênticos, sem ilustração 3D,
sem onboarding de cinco telas. Peso visual precisa ter função.

**Software corporativo dos anos 2000.** Sem barra de menus densa, sem toolbar de
ícones minúsculos, sem pilha de diálogos modais, sem cinza sobre cinza.

## Design Principles

**A ferramenta some na tarefa.** O usuário veio converter um arquivo, não conhecer
o Tomark. Toda decisão de interface é avaliada por quanto ela desaparece. Um
elemento que se faz notar precisa justificar por que está tomando atenção.

**Não perguntar o que o app pode decidir.** Cada escolha oferecida ao usuário é
uma escolha que ele precisa entender primeiro. Salvar ao lado do original em vez
de perguntar a pasta; nunca sobrescrever em vez de perguntar se pode; um único
botão de ação em vez de um menu. Padrão bom e silencioso vence configuração.

**Parecer parte do sistema, não uma visita.** As convenções do desktop Windows são
o vocabulário — ícone na barra de tarefas, atalhos padrão, tema seguindo o do SO.
Afordância inventada para tarefa padrão é custo cobrado do usuário sem retorno.

**Erro é informação para quem usa, não para quem desenvolveu.** Uma falha precisa
dizer o que aconteceu e o que fazer, em português comum. O texto técnico pode
existir, mas atrás de um passo, nunca como a mensagem principal.

**Confiança se constrói não pedindo nada.** Sem conta, sem rede, sem telemetria,
sem arquivo saindo da máquina. O usuário converte um contrato ou um laudo sem
precisar avaliar em quem está confiando.

## Accessibility & Inclusion

Meta **WCAG 2.1 AA**, adaptada ao que faz sentido fora da web: contraste mínimo
de 4.5:1 em texto e 3:1 em elementos gráficos de interface, operação completa por
teclado e foco sempre visível e rastreável.

Isso torna os achados da auditoria de contraste bugs a corrigir, não notas de
rodapé — em particular o texto das linhas da lista herdando cor de badge
(3.02–3.52:1) e o texto do estado vazio (2.77:1 no claro), que é a primeira
instrução que um usuário novo lê.

O público-alvo trabalha em máquinas corporativas onde alto contraste e escala de
texto do sistema são comuns; a interface não pode quebrar com nenhum dos dois.
