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

### ~~1 e 2. Foco/seleção divergentes na fila~~ — RESOLVIDO, com ressalva

**A auditoria errou o diagnóstico.** Os dois achados partiam de "usuário tabula
até uma linha". As linhas são `CTkFrame` sem `takefocus` — **nunca receberam
foco de Tab**. Logo:

- Item 1 (foco destruído no `_rebuild_list`): a linha não tinha foco pra perder.
- Item 2 (`Delete` apaga o arquivo errado): não reproduz. `Delete` sempre agiu
  sobre o último clicado, que é o mesmo que está destacado. Sem divergência,
  sem risco de apagar item errado.

O problema real por trás dos dois era mais simples e mais grave: **não existia
navegação por teclado na fila.** Sem mouse, não se chegava a arquivo nenhum.

**Corrigido:** `move_selection()` em `paths.py` (puro, coberto por
`test_output_path.py`), bind `<Up>`/`<Down>` e `_move_selection` /
`_scroll_into_view` em `markitdown_gui.py`. A seta é guardada contra o preview
— bind no root também dispara com o cursor no textbox, e lá a seta tem que
rolar o texto, não trocar o arquivo debaixo do leitor.

> **Ressalva, ainda em aberto:** as linhas continuam sem `takefocus`. Um leitor
> de tela não anuncia a fila. Se acessibilidade assistiva entrar no escopo, aí
> sim vale `takefocus=True` + anel de foco distinto da seleção — e aí o item 1
> original (devolver foco depois do rebuild) volta a valer.

### ~~3. Exceção crua do Python como mensagem de erro~~ — RESOLVIDO

`app/errors.py`: `friendly_error(exc)` casa por **nome de classe subindo a
MRO** (não por `isinstance`), então o módulo não importa `markitdown` e o teste
não carrega a dependência pesada. `error_text(exc, path)` monta o bloco do
preview — título, frase acionável, detalhe técnico truncado em 300 chars por
último. A tradução acontece no `_convert_worker`, com a exceção viva: o tipo é
o sinal mais confiável e ele se perde em `str(e)`. Coberto por
`app/test_errors.py`.

> **Achado colateral, não resolvido:** o markitdown quase não levanta exceção.
> `.xyz` com bytes binários e `.pdf` corrompido **convertem sem erro** — ele cai
> num leitor de texto puro e devolve lixo. Só `FileNotFoundError` disparou nos
> testes reais. Ou seja: o caminho de erro agora está educado, mas o caminho de
> **sucesso falso** é o mais provável na prática, e hoje não há nada avisando o
> usuário de que o resultado é lixo. Vale um item próprio — ver item 12.

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

### 12. Sucesso falso: lixo convertido sem aviso

**Onde:** `_convert_worker()` — nada valida o resultado de `md.convert()`
**Categoria:** Confiança · descoberto ao implementar o item 3

Medido, não suposto: `.xyz` binário e `.pdf` corrompido passam pelo markitdown
**sem exceção**, tratados como texto puro. O app grava um `.md` de bytes ilegíveis
e mostra badge de ok. O usuário não-técnico não tem como saber que falhou —
para ele, converteu.

Pior que o erro cru do item 3: erro cru ao menos avisava que algo deu errado.

**Correção a decidir:** heurística barata no resultado (proporção de bytes não
imprimíveis, markdown vazio ou quase) virando um estado "convertido com
ressalva" — badge próprio, aviso no preview, arquivo gravado do mesmo jeito.
Não inventar um validador por formato.

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
