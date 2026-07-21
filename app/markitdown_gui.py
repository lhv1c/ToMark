"""
Tomark — janela desktop para converter arquivos em Markdown (em lote).

Envolve a API publica do markitdown: MarkItDown().convert(path).markdown
Selecione varios arquivos, converta, e cada .md e salvo ao lado do original.
"""

import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk

from markitdown import MarkItDown

from errors import error_text
from paths import move_selection, next_selection, resolve_output_path

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:  # ponytail: DnD e opcional — sem ela so perde o arrastar
    DND_FILES = None
    TkinterDnD = None


FILE_TYPES = [
    ("Todos suportados", "*.pdf *.docx *.doc *.xlsx *.xls *.pptx "
                         "*.html *.htm *.csv *.txt *.md *.json *.xml *.epub"),
    ("PDF", "*.pdf"),
    ("Word", "*.docx *.doc"),
    ("Excel", "*.xlsx *.xls"),
    ("PowerPoint", "*.pptx"),
    ("HTML", "*.html *.htm"),
    ("Texto / CSV", "*.txt *.csv *.md *.json *.xml"),
    ("Todos os arquivos", "*.*"),
]

# Consolas so existe no Windows; "monospace" e o alias generico no X11/Wayland.
FONT_MONO = ("Consolas" if sys.platform == "win32" else "monospace", 12)

# Cores como (claro, escuro): o CTk troca sozinho no appearance_mode.
# Todo token e par — cor em string unica nao responde ao tema (DESIGN.md,
# The Paired Token Rule). Contrastes medidos contra o fundo real do widget.
MUTED = ("#6b6b6b", "#9a9a9a")
HINT = ("#666666", "#888888")        # 4.6:1 / 4.5:1 sobre o painel da fila
ROW_SEL = ("#cfe3f7", "#264f78")
ROW_HOVER = ("#e6e6e6", "#333337")
GHOST_BORDER = ("#c8ccd0", "#3a3d41")
GHOST_TEXT = ("#1f1f1f", "#e6e6e6")
GHOST_HOVER = ("#ececec", "#2a2d31")
DISABLED = ("#a8adb2", "#5a5d61")

# Acento unico do app (DESIGN.md, The Single Accent Rule): CTA e progresso
# usam o mesmo azul, nao o do tema. Hover ESCURECE — clarear derrubava o
# texto branco pra 4.33:1, abaixo de AA.
ACTION = ("#2b6cb0", "#1f538d")        # branco por cima: 5.4:1 / 7.8:1
ACTION_HOVER = ("#1f538d", "#164070")  # 7.8:1 / 10.6:1

BADGE = {"pendente": "•", "convertendo": "⟳", "ok": "✓", "erro": "✕"}
# Cor do badge, nunca do nome do arquivo (DESIGN.md, The Earned Color Rule).
# Cada par passa 4.5:1 sobre o painel E sobre a linha selecionada.
BADGE_COLOR = {"pendente": ("#5f5f5f", "#bdbdbd"),
               "convertendo": ("#0868a0", "#5ec8ff"),
               "ok": ("#257046", "#89cca2"),
               "erro": ("#be2626", "#ffa6a6")}

COPY_GLYPH = "⧉"      # dois quadrados sobrepostos: copiar
COPIED_GLYPH = "✓"

EMPTY_HINT = ("Arraste arquivos aqui\n"
              "ou clique em “Selecionar arquivos…”")


def _resource_path(name):
    """Caminho de um recurso, funcionando no fonte e no exe (PyInstaller)."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


def reveal_in_file_manager(path):
    """Abre a pasta que contem `path` no gerenciador de arquivos do sistema."""
    folder = os.path.dirname(os.path.abspath(path))
    if sys.platform == "win32":
        os.startfile(folder)  # noqa: S606 — caminho vem do proprio app
    elif sys.platform == "darwin":
        subprocess.Popen(["open", folder])
    else:
        subprocess.Popen(["xdg-open", folder])


def make_root():
    """CTk com drag & drop quando tkinterdnd2 (e a lib tkdnd) estao presentes."""
    if TkinterDnD is None:
        return ctk.CTk()

    class _DnDCTk(ctk.CTk, TkinterDnD.DnDWrapper):
        def __init__(self):
            super().__init__()
            self.TkdndVersion = TkinterDnD._require(self)

    try:
        return _DnDCTk()
    except Exception:  # noqa: BLE001 — tkdnd ausente: segue sem arrastar
        return ctk.CTk()


class FileItem:
    def __init__(self, path):
        self.path = path
        self.status = "pendente"   # pendente | convertendo | ok | erro
        self.markdown = None
        self.error = None
        self.output_path = None


class MarkItDownApp:
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.md = MarkItDown()          # plugins off; conversores embutidos
        self.items = []                 # list[FileItem]
        self.row_widgets = []           # (row, badge, name) por item
        self.selected = None            # indice do item selecionado
        self.done = 0                   # itens finalizados no lote atual
        self.total = 0                  # tamanho do lote atual (0 = parado)
        self.cancel = threading.Event()  # pedido de parada do lote

        root.title("Tomark — Conversor para Markdown")
        root.geometry("900x640")
        root.minsize(680, 480)
        try:
            if sys.platform == "win32":
                root.iconbitmap(_resource_path("icon.ico"))
            else:
                # Tk fora do Windows nao le .ico. A PhotoImage precisa
                # continuar viva, senao o Tk descarta a imagem.
                self._icon = tk.PhotoImage(file=_resource_path("icon.png"))
                root.iconphoto(True, self._icon)
        except Exception:  # noqa: BLE001 — sem icone nao e fatal
            pass

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("dark-blue")
        self._build_ui()
        self._bind_shortcuts()
        self._setup_dnd()
        self._rebuild_list()
        self._refresh_actions()

    def _build_ui(self):
        # topo: selecionar + limpar + contador + converter
        top = ctk.CTkFrame(self.root, fg_color="transparent")
        top.pack(fill="x", padx=16, pady=(16, 8))
        # Secundario (ghost): a acao existe mas nao compete com o CTA.
        self._ghost_button(top, "Selecionar arquivos…",
                           self.on_select).pack(side="left")
        self.clear_btn = self._ghost_button(top, "Limpar", self.on_clear)
        self.clear_btn.pack(side="left", padx=(8, 0))
        self.count_var = tk.StringVar(value="nenhum arquivo")
        ctk.CTkLabel(top, textvariable=self.count_var,
                     text_color=MUTED).pack(side="left", padx=12)
        # Primario (CTA): unico botao preenchido, no accent do app.
        self.convert_btn = ctk.CTkButton(
            top, text="Converter", command=self.on_convert, state="disabled",
            corner_radius=8, height=36, fg_color=ACTION,
            hover_color=ACTION_HOVER, text_color="#ffffff",
            text_color_disabled=DISABLED)
        self.convert_btn.pack(side="right")

        # meio: lista (esq) + preview (dir)
        mid = ctk.CTkFrame(self.root, fg_color="transparent")
        mid.pack(fill="both", expand=True, padx=16, pady=8)

        self.list_frame = ctk.CTkScrollableFrame(
            mid, width=300, label_text="Arquivos")
        self.list_frame.pack(side="left", fill="y")
        self.empty_label = ctk.CTkLabel(
            self.list_frame, text=EMPTY_HINT, text_color=HINT,
            justify="center")

        self.preview = ctk.CTkTextbox(mid, wrap="word", font=FONT_MONO)
        self.preview.pack(side="left", fill="both", expand=True, padx=(12, 0))
        self.preview.configure(state="disabled")
        # Copiar como icone sobreposto no canto do preview, no lugar de mais
        # um botao no rodape. Fica escondido enquanto nao ha o que copiar.
        self.copy_btn = ctk.CTkButton(
            self.preview, text=COPY_GLYPH, width=28, height=28,
            corner_radius=6, font=("Segoe UI Symbol", 14),
            fg_color=GHOST_HOVER, hover_color=ROW_HOVER,
            text_color=GHOST_TEXT, command=self.on_copy)
        # Abrir pasta acompanha o Copiar: as duas acoes do resultado moram
        # no canto do preview, nao mais no rodape. So aparecem quando ha .md.
        self.open_btn = ctk.CTkButton(
            self.preview, text="Abrir pasta", height=28, corner_radius=6,
            fg_color=GHOST_HOVER, hover_color=ROW_HOVER,
            text_color=GHOST_TEXT, command=self.on_open_folder)

        # cheat-sheet de atalhos: linha discreta, sempre visivel, no rodape
        # da janela. O publico e nao-tecnico — atalho invisivel nao existe.
        shortcuts = ("Ctrl+O selecionar  ·  Ctrl+Enter converter  ·  "
                     "Delete remover  ·  Ctrl+L limpar  ·  Esc cancelar")
        ctk.CTkLabel(self.root, text=shortcuts, text_color=HINT,
                     anchor="center").pack(side="bottom", pady=(0, 8))

        # rodape: tema (cromo, longe do CTA) + status. Abrir pasta migrou pro
        # canto do preview. A barra de progresso entra acima do rodape so
        # enquanto o lote roda (pack before=self.footer).
        self.footer = ctk.CTkFrame(self.root, fg_color="transparent")
        self.footer.pack(fill="x", side="bottom", padx=16, pady=(0, 8))
        self.theme_btn = self._ghost_button(self.footer, "",
                                            self.on_toggle_theme, height=28)
        self.theme_btn.configure(width=40)
        self.theme_btn.pack(side="left")
        self._sync_theme_btn()
        self.status_var = tk.StringVar(value="Pronto.")
        ctk.CTkLabel(self.footer, textvariable=self.status_var, anchor="w",
                     text_color=MUTED).pack(side="left", padx=(8, 0))

        self.progress = ctk.CTkProgressBar(self.root, height=6,
                                           progress_color=ACTION)
        self.progress.set(0)

    def _ghost_button(self, parent, text, command, height=36):
        return ctk.CTkButton(
            parent, text=text, command=command, corner_radius=8, height=height,
            fg_color="transparent", border_width=1, border_color=GHOST_BORDER,
            text_color=GHOST_TEXT, hover_color=GHOST_HOVER,
            text_color_disabled=DISABLED)

    def _bind_shortcuts(self):
        self.root.bind("<Control-o>", lambda e: self.on_select())
        self.root.bind("<Control-Return>", lambda e: self.on_convert())
        self.root.bind("<Delete>", lambda e: self.on_remove())
        self.root.bind("<Control-l>", lambda e: self.on_clear())
        self.root.bind("<Escape>", lambda e: self.on_cancel())
        self.root.bind("<Up>", lambda e: self._move_selection(-1))
        self.root.bind("<Down>", lambda e: self._move_selection(1))

    def _setup_dnd(self):
        if DND_FILES is None or not hasattr(self.root, "drop_target_register"):
            return
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self._on_drop)

    def _on_drop(self, event):
        # splitlist entende o formato do tkdnd: caminho com espaco vem em {}.
        paths = [p for p in self.root.tk.splitlist(event.data)
                 if os.path.isfile(p)]
        self._add_paths(paths)

    # ---- fila ----

    def _row_bg(self, i, hover=False):
        if i == self.selected:
            return ROW_SEL
        return ROW_HOVER if hover else "transparent"

    def _make_row(self, i, item):
        """Badge e nome sao widgets separados de proposito: o estado colore o
        badge, o nome fica sempre em GHOST_TEXT. Um CTkButton so tem um
        text_color, e pintar a linha inteira derrubava o nome do arquivo
        pra 3.0-3.5:1 (DESIGN.md, The Earned Color Rule)."""
        row = ctk.CTkFrame(self.list_frame, corner_radius=8,
                           fg_color=self._row_bg(i))
        badge = ctk.CTkLabel(row, text=BADGE[item.status], width=16,
                             text_color=BADGE_COLOR[item.status])
        badge.pack(side="left", padx=(8, 0), pady=4)
        name = ctk.CTkLabel(row, text=os.path.basename(item.path), anchor="w",
                            text_color=GHOST_TEXT)
        name.pack(side="left", fill="x", expand=True, padx=(4, 8), pady=4)
        # ponytail: Enter/Leave em cada filho porque o Tk dispara Leave no pai
        # ao entrar num filho. Os dois eventos caem no mesmo ciclo, entao nao
        # pisca; se piscar, trocar por winfo_containing no Leave.
        for w in (row, badge, name):
            w.bind("<Button-1>", lambda e, idx=i: self.on_row_click(idx))
            w.bind("<Enter>", lambda e, idx=i: self._set_row_bg(idx, True))
            w.bind("<Leave>", lambda e, idx=i: self._set_row_bg(idx, False))
        return row, badge, name

    def _set_row_bg(self, i, hover):
        if i < len(self.row_widgets):
            self.row_widgets[i][0].configure(fg_color=self._row_bg(i, hover))

    def _move_selection(self, delta):
        """Seta move a selecao da fila. As linhas nao recebem foco de Tab, entao
        esta e a unica forma de chegar num arquivo sem mouse."""
        # Bind no root tambem dispara com o cursor dentro do preview; la a seta
        # tem que rolar o texto, nao trocar o arquivo debaixo do leitor.
        focused = self.root.focus_get()
        if focused is not None and str(focused).startswith(str(self.preview)):
            return
        i = move_selection(len(self.items), self.selected, delta)
        if i is None or i == self.selected:
            return
        self.on_row_click(i)
        self._scroll_into_view(i)

    def _scroll_into_view(self, i):
        """Sem isto a selecao sai da area visivel e a seta parece nao fazer
        nada — justo no lote grande, que e o caso de uso central."""
        # ponytail: _parent_canvas e privado do CustomTkinter. hasattr degrada
        # pra "nao rola" se a versao mudar, no mesmo espirito dos outros
        # fallbacks do app. Trocar por API publica quando existir uma.
        canvas = getattr(self.list_frame, "_parent_canvas", None)
        row = self.row_widgets[i][0]
        if canvas is None or not row.winfo_ismapped():
            return
        self.list_frame.update_idletasks()
        total = max(canvas.bbox("all")[3], 1)
        top, bottom = canvas.yview()
        y0 = row.winfo_y() / total
        y1 = (row.winfo_y() + row.winfo_height()) / total
        if y0 < top:
            canvas.yview_moveto(y0)
        elif y1 > bottom:
            canvas.yview_moveto(y1 - (bottom - top))

    def _rebuild_list(self):
        for row, _, _ in self.row_widgets:
            row.destroy()
        self.row_widgets = []
        for i, item in enumerate(self.items):
            widgets = self._make_row(i, item)
            widgets[0].pack(fill="x", pady=2)
            self.row_widgets.append(widgets)
        if self.items:
            self.empty_label.pack_forget()
        else:
            self.empty_label.pack(pady=24)

    def _update_row(self, i):
        item = self.items[i]
        row, badge, _ = self.row_widgets[i]
        badge.configure(text=BADGE[item.status],
                        text_color=BADGE_COLOR[item.status])
        row.configure(fg_color=self._row_bg(i))

    def _refresh_actions(self):
        """Contador e estado dos botoes — fonte unica da verdade da barra."""
        n = len(self.items)
        self.count_var.set(f"{n} arquivo(s)" if n else "nenhum arquivo")
        running = self.total > 0
        pending = any(it.status in ("pendente", "erro") for it in self.items)
        if running:
            # Mesmo botao: durante o lote a acao util e parar, nao converter.
            self.convert_btn.configure(
                text="Cancelar", command=self.on_cancel,
                state="disabled" if self.cancel.is_set() else "normal")
        else:
            self.convert_btn.configure(
                text="Converter", command=self.on_convert,
                state="normal" if pending else "disabled")
        self.clear_btn.configure(
            state="normal" if n and not running else "disabled")
        sel = self.items[self.selected] if self.selected is not None else None
        done = bool(sel and sel.status == "ok")
        if done:
            self.copy_btn.configure(text=COPY_GLYPH)
            # canto superior direito, deslocado pra nao cobrir a barra de
            # rolagem. Abrir pasta fica a esquerda do Copiar, sem sobrepor.
            self.copy_btn.place(relx=1.0, y=8, x=-38, anchor="ne")
            self.open_btn.place(relx=1.0, y=8, x=-74, anchor="ne")
        else:
            self.copy_btn.place_forget()
            self.open_btn.place_forget()

    def _add_paths(self, paths):
        if not paths:
            return
        for p in paths:
            self.items.append(FileItem(p))
        self._rebuild_list()
        self._refresh_actions()
        self.status_var.set("Pronto para converter.")

    # ---- acoes ----

    def on_select(self):
        paths = filedialog.askopenfilenames(
            title="Escolha os arquivos para converter", filetypes=FILE_TYPES)
        self._add_paths(list(paths))

    def on_remove(self):
        if self.selected is None or self.total:
            return
        i = self.selected
        self.selected = next_selection(len(self.items), i)
        del self.items[i]
        self._rebuild_list()
        self._refresh_actions()
        self._render_preview(
            self.items[self.selected] if self.selected is not None else None)

    def on_clear(self):
        if self.total:
            return
        self.items = []
        self.selected = None
        self._rebuild_list()
        self._refresh_actions()
        self._render_preview(None)
        self.status_var.set("Pronto.")

    def _sync_theme_btn(self):
        dark = ctk.get_appearance_mode() == "Dark"
        self.theme_btn.configure(text="☀" if dark else "☾")

    def on_toggle_theme(self):
        ctk.set_appearance_mode(
            "light" if ctk.get_appearance_mode() == "Dark" else "dark")
        self._sync_theme_btn()

    def on_copy(self):
        if self.selected is None:
            return
        item = self.items[self.selected]
        if item.status != "ok":
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(item.markdown or "")
        self.copy_btn.configure(text=COPIED_GLYPH)
        self.root.after(1200, lambda: self.copy_btn.configure(text=COPY_GLYPH))
        self.status_var.set("Markdown copiado.")

    def on_cancel(self):
        if not self.total:
            return
        self.cancel.set()
        self.status_var.set("Cancelando… (termina o arquivo atual)")
        self._refresh_actions()

    def on_open_folder(self):
        if self.selected is None:
            return
        item = self.items[self.selected]
        try:
            reveal_in_file_manager(item.output_path or item.path)
        except Exception as e:  # noqa: BLE001 — sem gerenciador de arquivos
            self.status_var.set(f"Nao foi possivel abrir a pasta: {e}")

    def on_row_click(self, i):
        prev = self.selected
        self.selected = i
        if prev is not None and prev < len(self.row_widgets):
            self._update_row(prev)
        self._update_row(i)
        self._render_preview(self.items[i])
        self._refresh_actions()

    def _render_preview(self, item):
        if item is None:
            text = ""
        elif item.status == "ok":
            text = item.markdown or ""
        elif item.status == "erro":
            # Ja vem pronto do worker, com titulo e frase acionavel.
            text = item.error or ""
        else:
            text = "Ainda não convertido."
        self.preview.configure(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", text)
        self.preview.configure(state="disabled")

    def on_convert(self):
        if self.total:
            return
        pending = [i for i, it in enumerate(self.items)
                   if it.status in ("pendente", "erro")]
        if not pending:
            return
        self.done, self.total = 0, len(pending)
        self.cancel.clear()
        self._refresh_actions()
        self.progress.set(0)
        self.progress.pack(fill="x", padx=16, pady=(0, 8), before=self.footer)
        self.status_var.set(f"Convertendo…  0/{self.total}")
        threading.Thread(target=self._convert_worker, args=(pending,),
                         daemon=True).start()

    def _convert_worker(self, indices):
        # Sequencial: 1 erro nao para o lote. UI so e tocada via root.after.
        for i in indices:
            if self.cancel.is_set():
                break
            item = self.items[i]
            self.root.after(0, self._set_status, i, "convertendo")
            try:
                markdown = self.md.convert(item.path).markdown
                out = resolve_output_path(item.path)
                with open(out, "w", encoding="utf-8") as f:
                    f.write(markdown)
                self.root.after(0, self._on_item_ok, i, markdown, out)
            except Exception as e:  # noqa: BLE001 — falha de 1 nao derruba o lote
                # Traduz aqui, com a excecao viva: o tipo dela e o sinal mais
                # confiavel, e ele se perde em str(e).
                self.root.after(0, self._on_item_err, i,
                                error_text(e, item.path))
        self.root.after(0, self._on_batch_done)

    def _set_status(self, i, status):
        self.items[i].status = status
        self._update_row(i)

    def _tick(self):
        self.done += 1
        self.progress.set(self.done / self.total if self.total else 0)
        self.status_var.set(f"Convertendo…  {self.done}/{self.total}")

    def _on_item_ok(self, i, markdown, out):
        item = self.items[i]
        item.status = "ok"
        item.markdown = markdown
        item.output_path = out
        item.error = None
        self._update_row(i)
        self._tick()
        if self.selected == i:
            self._render_preview(item)
            self._refresh_actions()  # faz Copiar/Abrir pasta surgirem no canto

    def _on_item_err(self, i, message):
        item = self.items[i]
        item.status = "erro"
        item.error = message
        self._update_row(i)
        self._tick()
        if self.selected == i:
            self._render_preview(item)

    def _on_batch_done(self):
        ok = sum(1 for it in self.items if it.status == "ok")
        err = sum(1 for it in self.items if it.status == "erro")
        cancelled = self.cancel.is_set()
        self.cancel.clear()
        self.done = self.total = 0
        self.progress.pack_forget()
        self._refresh_actions()
        msg = ("⊘ cancelado — " if cancelled else "")
        msg += f"✓ {ok} convertido(s), salvos ao lado do original"
        if err:
            msg += f"  ·  ✕ {err} com erro"
        self.status_var.set(msg)


def _selftest(paths):
    """Conversao headless (sem janela) p/ validar o pipeline empacotado.
    Uso: Tomark.exe --selftest arquivo1 [arquivo2 ...]
    Grava <arquivo>.selftest.md ao lado de cada entrada."""
    md = MarkItDown()
    lines = []
    rc = 0
    for path in paths:
        try:
            markdown = md.convert(path).markdown
            out = os.path.splitext(path)[0] + ".selftest.md"
            with open(out, "w", encoding="utf-8") as f:
                f.write(markdown)
            lines.append(f"OK  {path} -> {out} ({len(markdown)} chars)")
        except Exception as e:  # noqa: BLE001
            lines.append(f"ERRO {path}: {e}")
            rc = 1
    report = "\n".join(lines)
    with open("selftest_report.txt", "w", encoding="utf-8") as f:
        f.write(report + "\n")
    try:
        print(report)
    except Exception:  # noqa: BLE001
        pass
    return rc


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(_selftest(sys.argv[2:]))

    root = make_root()
    MarkItDownApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
