# Backlog de UI — achados da auditoria

Origem: auditoria técnica de `app/markitdown_gui.py` (2026-07-20), com as
dimensões de acessibilidade, performance, tema e responsividade adaptadas de
web para Tkinter/CustomTkinter. Score na época: **12/20**.

Contexto estratégico em [`PRODUCT.md`](PRODUCT.md); sistema visual e regras
nomeadas em [`DESIGN.md`](DESIGN.md). Leia os dois antes de mexer — vários itens
abaixo só fazem sentido contra as regras de lá.

> **Já resolvido no commit `d936ec1`** (branch `fix/contraste-wcag-aa`): todos os
> achados de contraste de cor, o hover do CTA que reprovava AA, o acento
> duplicado e o texto da linha herdando cor de badge. Não refaça. `HINT`,
> `BADGE_COLOR`, `ACTION` e `ACTION_HOVER` estão travados por
> `app/test_contrast.py` — rode antes e depois de qualquer mexida em cor.

---

## P1 — corrigir antes de distribuir

### 1. Foco de teclado é destruído a cada mudança na lista

**Onde:** `markitdown_gui.py`, `_rebuild_list()`
**Categoria:** Acessibilidade · WCAG 2.4.3 / 2.1.1

`_rebuild_list()` chama `.destroy()` em todas as linhas e recria. Todo
`_add_paths` e todo `on_remove` passa por lá.

Usuário de teclado navega até um arquivo, aperta `Delete`, e o widget focado
deixa de existir: o foco volta pro root e a posição na lista se perde. Apagar 3
arquivos = tabular desde o início 3 vezes.

**Correção:** em `on_remove`, atualizar as linhas existentes em vez de
reconstruir; devolver o foco a `row_widgets[self.selected]` depois de qualquer
rebuild.

> Nota: a estrutura da linha mudou no `d936ec1`. Agora é
> `(frame, badge, name)` em `self.row_widgets`, não mais um `CTkButton` em
> `row_buttons`. O alvo de foco precisa ser decidido — provavelmente o frame,
> que exige `takefocus=True`.

### 2. Seleção e foco divergem, e o `Delete` obedece o errado

**Onde:** `_bind_shortcuts()`, `on_remove()`, `on_row_click()`
**Categoria:** Acessibilidade · WCAG 2.1.1

`self.selected` só muda por clique. Tabular pelas linhas move o foco visual do
SO, mas não a seleção.

Usuário tabula até o arquivo 5, aperta `Delete`, e o app apaga o arquivo 2 — o
último que ele clicou. Apagar o item errado, sem undo. É o achado mais próximo
de P0; só não é porque a fila é reconstruível a partir dos arquivos originais.

**Correção:** navegação por `<Up>`/`<Down>` movendo seleção e foco juntos, e
`<FocusIn>` em cada linha sincronizando `self.selected`.

### 3. Exceção crua do Python como mensagem de erro

**Onde:** `_render_preview()` — `text = f"[erro]\n{item.error}"`
**Categoria:** UX copy · viola anti-referência de `PRODUCT.md`

`item.error` é `str(e)` vindo do markitdown. O usuário lê
`FileNotFoundError: [WinError 2]...` ou stack de parser.

`PRODUCT.md` lista **"ferramenta de dev"** como anti-referência explícita, e
`DESIGN.md` repete como Don't. Este é o ponto onde o código contradiz o
documento de forma mais direta.

**Correção:** mapear as falhas comuns (arquivo corrompido, formato não
suportado, PDF protegido por senha, arquivo em uso) para frases acionáveis em
português. Texto técnico atrás de um "detalhes", nunca como mensagem principal.

### 4. Atalhos e remoção não são descobríveis

**Onde:** `_bind_shortcuts()`
**Categoria:** Onboarding

Cinco atalhos existem — `Ctrl+O`, `Ctrl+Enter`, `Delete`, `Ctrl+L`, `Esc` — e
nenhum aparece na interface. Nenhum menu, nenhuma dica, nenhum tooltip. Só quem
lê o fonte sabe. Nada indica que uma linha pode ser removida.

Lembrando que o público-alvo de `PRODUCT.md` é não-técnico: um atalho invisível
não existe para essa pessoa.

**Correção:** decidir entre tooltip nos botões, uma linha discreta no rodapé, ou
`×` na linha ao passar o mouse. O contraste do estado vazio já foi corrigido; a
descoberta não.

---

## P2 — próxima passada

### 5. Reconstrução total da lista a cada adição

**Onde:** `_add_paths()` → `_rebuild_list()`
**Categoria:** Performance

Destrói e recria **todas** as linhas a cada arquivo adicionado. Arrastar 200
arquivos cria 200 linhas; arrastar mais 50 depois destrói as 200 e cria 250.
Custo quadrático em adições incrementais, com a UI travada durante — e lote é o
caso de uso central.

**Piorou levemente no `d936ec1`:** cada linha agora são 3 widgets, não 1.

**Correção:** anexar só as linhas novas; reservar o rebuild pra remoção.

### 6. Markdown inteiro inserido no preview na thread principal

**Onde:** `_render_preview()` — `self.preview.insert("1.0", text)`
**Categoria:** Performance

Um PDF de 400 páginas gera megabytes numa única inserção. A janela congela ao
clicar num arquivo grande já convertido, sem spinner — parece travamento.

**Correção:** inserir só os primeiros ~50k chars com aviso de truncagem. O
`on_copy` continua usando `item.markdown` inteiro, então nada se perde.

### 7. Divisória lista/preview não é ajustável, e caminho completo é inacessível

**Onde:** `_build_ui()` — `self.list_frame` com `width=300` fixo
**Categoria:** Responsividade

Nomes longos ficam cortados sem recurso, e não há tooltip com caminho completo
em lugar nenhum. O usuário não distingue dois `relatorio.pdf` de pastas
diferentes.

**Correção:** `tk.PanedWindow` (nativo, sem dependência nova) entre lista e
preview. Tooltip de caminho completo na linha.

### 8. Tema e geometria não sobrevivem ao fechamento

**Onde:** `__init__` (`geometry("900x640")`), `on_toggle_theme()`
**Categoria:** Tema

Quem prefere escuro num sistema claro reescolhe toda sessão. Quem redimensiona
a janela, redimensiona sempre.

**Correção:** um JSON pequeno no diretório de config do usuário com `geometry` e
`appearance_mode`.

### 9. Divergência de raio: 8px vs 6px

**Onde:** botões próprios usam `corner_radius=8`; linhas, preview e botão de
ícone usam o padrão 6 do CustomTkinter
**Categoria:** Consistência visual

`DESIGN.md` registra 8px como o valor escolhido do projeto e chama a divergência
de dívida. Achado da passada de `document`, não da auditoria original.

---

## P3 — se sobrar tempo

### 10. Toggle de tema é caminho sem volta pro "system"

`on_toggle_theme()` alterna claro↔escuro. Uma vez tocado, não há como voltar a
seguir o SO até reiniciar. Resolve junto com o item 8.

### 11. Texto desabilitado muito fraco — sem violação

`DISABLED` mede 2.02:1 (claro) e 2.63:1 (escuro). **WCAG 1.4.3 isenta controles
desabilitados**, então não é violação e não entra em `test_contrast.py`.
Registrado porque 2.02:1 é fraco até como "apagado intencional" — o botão fica
quase invisível em vez de parecer desabilitado.

---

## O que estava certo, e deve continuar

Não quebre isto ao mexer nos itens acima:

- **Threading.** Worker daemon converte; toda mutação de UI passa por
  `root.after(0, ...)`. Uma falha não derruba o lote.
- **`resolve_output_path` nunca sobrescreve** (`paths.py`) — sufixo ` (1)`,
  ` (2)`. Zero risco de perda de dados, coberto por `test_output_path.py`.
- **Hierarquia de botões.** Um CTA preenchido, resto ghost.
- **Botão que vira "Cancelar"** durante o lote, mesma posição.
- **`_refresh_actions` como fonte única da verdade** dos estados da barra.
- **Degradação graciosa**: sem `tkinterdnd2`, sem ícone ou sem gerenciador de
  arquivos, o app cai em fallback em vez de quebrar.
- **Zero tells de AI.** Sem gradiente, sem card repetido, sem glassmorphism.

---

## Como retomar

```bash
python app/test_contrast.py      # cores: 26 pares nos dois temas
python app/test_output_path.py   # nomeacao de saida
./.venv/Scripts/python.exe app/markitdown_gui.py
```

Comandos do skill que mapeiam pros itens, se quiser usá-los:
`/impeccable harden` (1, 2, 8) · `/impeccable clarify` (3) ·
`/impeccable onboard` (4) · `/impeccable optimize` (5, 6) ·
`/impeccable adapt` (7) · `/impeccable polish` (9, fechamento)

O skill é web-only; ele vai trazer conselho de CSS que não se aplica a Tkinter.
Traduza, não siga literal.
