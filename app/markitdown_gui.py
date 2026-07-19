"""
Tomark — janela desktop para converter arquivos em Markdown (em lote).

Envolve a API publica do markitdown: MarkItDown().convert(path).markdown
Selecione varios arquivos, converta, e cada .md e salvo ao lado do original.
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk

from markitdown import MarkItDown

from paths import resolve_output_path


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

BADGE = {"pendente": "•", "convertendo": "⟳", "ok": "✓", "erro": "✕"}
BADGE_COLOR = {"pendente": "#9a9a9a", "convertendo": "#4cc2ff",
               "ok": "#4caf72", "erro": "#ff6b6b"}


def _resource_path(name):
    """Caminho de um recurso, funcionando no fonte e no exe (PyInstaller)."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


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
        self.row_buttons = []           # botao por item (mesma ordem de items)
        self.selected = None            # indice do item selecionado

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

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self._build_ui()

    def _build_ui(self):
        # topo: selecionar + contador + converter
        top = ctk.CTkFrame(self.root, fg_color="transparent")
        top.pack(fill="x", padx=16, pady=(16, 8))
        # Secundario (ghost): a acao existe mas nao compete com o CTA.
        ctk.CTkButton(
            top, text="Selecionar arquivos…", command=self.on_select,
            corner_radius=8, height=36, fg_color="transparent",
            border_width=1, border_color="#3a3d41", text_color="#e6e6e6",
            hover_color="#2a2d31").pack(side="left")
        self.count_var = tk.StringVar(value="nenhum arquivo")
        ctk.CTkLabel(top, textvariable=self.count_var,
                     text_color="#9a9a9a").pack(side="left", padx=12)
        # Primario (CTA): unico botao preenchido, no accent do app.
        self.convert_btn = ctk.CTkButton(
            top, text="Converter", command=self.on_convert, state="disabled",
            corner_radius=8, height=36, fg_color="#2b6cb0",
            hover_color="#2c7bd0", text_color="#ffffff",
            text_color_disabled="#7f8a99")
        self.convert_btn.pack(side="right")

        # meio: lista (esq) + preview (dir)
        mid = ctk.CTkFrame(self.root, fg_color="transparent")
        mid.pack(fill="both", expand=True, padx=16, pady=8)

        self.list_frame = ctk.CTkScrollableFrame(
            mid, width=300, label_text="Arquivos")
        self.list_frame.pack(side="left", fill="y")

        self.preview = ctk.CTkTextbox(mid, wrap="word", font=FONT_MONO)
        self.preview.pack(side="left", fill="both", expand=True, padx=(12, 0))
        self.preview.configure(state="disabled")

        # rodape: status resumo
        self.status_var = tk.StringVar(value="Pronto.")
        ctk.CTkLabel(self.root, textvariable=self.status_var, anchor="w",
                     text_color="#9a9a9a").pack(fill="x", padx=16, pady=(0, 12))

    # ---- fila ----

    def _row_text(self, item):
        return f"{BADGE[item.status]}  {os.path.basename(item.path)}"

    def _rebuild_list(self):
        for b in self.row_buttons:
            b.destroy()
        self.row_buttons = []
        for i, item in enumerate(self.items):
            b = ctk.CTkButton(
                self.list_frame, text=self._row_text(item), anchor="w",
                fg_color="transparent", text_color=BADGE_COLOR[item.status],
                hover_color="#333337",
                command=lambda idx=i: self.on_row_click(idx))
            b.pack(fill="x", pady=2)
            self.row_buttons.append(b)

    def _update_row(self, i):
        item = self.items[i]
        b = self.row_buttons[i]
        fg = "#264f78" if i == self.selected else "transparent"
        b.configure(text=self._row_text(item),
                    text_color=BADGE_COLOR[item.status], fg_color=fg)

    # ---- acoes ----

    def on_select(self):
        paths = filedialog.askopenfilenames(
            title="Escolha os arquivos para converter", filetypes=FILE_TYPES)
        if not paths:
            return
        for p in paths:
            self.items.append(FileItem(p))
        self._rebuild_list()
        self.count_var.set(f"{len(self.items)} arquivo(s)")
        self.convert_btn.configure(state="normal")
        self.status_var.set("Pronto para converter.")

    def on_row_click(self, i):
        prev = self.selected
        self.selected = i
        if prev is not None and prev < len(self.row_buttons):
            self._update_row(prev)
        self._update_row(i)
        self._render_preview(self.items[i])

    def _render_preview(self, item):
        if item.status == "ok":
            text = item.markdown or ""
        elif item.status == "erro":
            text = f"[erro]\n{item.error}"
        else:
            text = "Ainda não convertido."
        self.preview.configure(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", text)
        self.preview.configure(state="disabled")

    def on_convert(self):
        pending = [i for i, it in enumerate(self.items)
                   if it.status in ("pendente", "erro")]
        if not pending:
            return
        self.convert_btn.configure(state="disabled")
        self.status_var.set("Convertendo…")
        threading.Thread(target=self._convert_worker, args=(pending,),
                         daemon=True).start()

    def _convert_worker(self, indices):
        # Sequencial: 1 erro nao para o lote. UI so e tocada via root.after.
        for i in indices:
            item = self.items[i]
            self.root.after(0, self._set_status, i, "convertendo")
            try:
                markdown = self.md.convert(item.path).markdown
                out = resolve_output_path(item.path)
                with open(out, "w", encoding="utf-8") as f:
                    f.write(markdown)
                self.root.after(0, self._on_item_ok, i, markdown, out)
            except Exception as e:  # noqa: BLE001 — falha de 1 nao derruba o lote
                self.root.after(0, self._on_item_err, i, str(e))
        self.root.after(0, self._on_batch_done)

    def _set_status(self, i, status):
        self.items[i].status = status
        self._update_row(i)

    def _on_item_ok(self, i, markdown, out):
        item = self.items[i]
        item.status = "ok"
        item.markdown = markdown
        item.output_path = out
        item.error = None
        self._update_row(i)
        if self.selected == i:
            self._render_preview(item)

    def _on_item_err(self, i, message):
        item = self.items[i]
        item.status = "erro"
        item.error = message
        self._update_row(i)
        if self.selected == i:
            self._render_preview(item)

    def _on_batch_done(self):
        ok = sum(1 for it in self.items if it.status == "ok")
        err = sum(1 for it in self.items if it.status == "erro")
        self.convert_btn.configure(state="normal")
        msg = f"✓ {ok} convertido(s), salvos ao lado do original"
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

    root = ctk.CTk()
    MarkItDownApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
