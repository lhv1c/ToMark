"""
Tomark — janela desktop (dark mode) para converter arquivos em Markdown.

Envolve a API publica do markitdown: MarkItDown().convert(path).markdown
Sem terminal, sem linha de comando. Selecione um arquivo, converta, salve .md.
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext

from markitdown import MarkItDown
from markitdown import MarkItDownException


# Filtros do dialogo de "abrir arquivo" (formatos comuns suportados offline).
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


# Paleta dark mode.
DARK = {
    "bg": "#1e1e1e",
    "panel": "#252526",
    "fg": "#e6e6e6",
    "muted": "#9a9a9a",
    "entry_bg": "#2d2d30",
    "btn": "#3a3d41",
    "btn_active": "#4a4d52",
    "btn_disabled": "#2a2a2a",
    "fg_disabled": "#6a6a6a",
    "accent": "#4cc2ff",
    "trough": "#333337",
    "select": "#264f78",
    "border": "#3c3c3c",
}


def _resource_path(name):
    """Caminho de um recurso, funcionando tanto no fonte quanto no exe (PyInstaller)."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


class MarkItDownApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.md = MarkItDown()  # plugins off; somente conversores embutidos
        self.source_path = None
        self.result_markdown = ""

        # Estado da barra de progresso animada.
        self._progress_value = 0.0
        self._progress_job = None

        root.title("Tomark — Conversor para Markdown")
        root.geometry("820x640")
        root.minsize(640, 480)
        try:
            root.iconbitmap(_resource_path("icon.ico"))
        except Exception:  # noqa: BLE001 — sem icone nao e fatal
            pass

        self._apply_dark_theme()
        self._build_ui()

    def _apply_dark_theme(self):
        d = DARK
        self.root.configure(bg=d["bg"])

        style = ttk.Style()
        style.theme_use("clam")  # tema mais customizavel que o nativo

        style.configure(".", background=d["bg"], foreground=d["fg"],
                        fieldbackground=d["entry_bg"], bordercolor=d["border"],
                        focuscolor=d["bg"])
        style.configure("TFrame", background=d["bg"])
        style.configure("TLabel", background=d["bg"], foreground=d["fg"])
        style.configure("Muted.TLabel", background=d["bg"], foreground=d["muted"])
        style.configure("Status.TLabel", background=d["panel"],
                        foreground=d["muted"])
        style.configure("Percent.TLabel", background=d["bg"],
                        foreground=d["accent"], font=("Segoe UI", 10, "bold"))

        style.configure("TButton", background=d["btn"], foreground=d["fg"],
                        borderwidth=0, padding=(12, 6), focuscolor=d["bg"])
        style.map("TButton",
                  background=[("active", d["btn_active"]),
                              ("disabled", d["btn_disabled"])],
                  foreground=[("disabled", d["fg_disabled"])])

        style.configure("Dark.Horizontal.TProgressbar",
                        background=d["accent"], troughcolor=d["trough"],
                        bordercolor=d["trough"], lightcolor=d["accent"],
                        darkcolor=d["accent"], thickness=14)

    def _build_ui(self):
        d = DARK
        pad = {"padx": 12, "pady": 6}

        top = ttk.Frame(self.root)
        top.pack(fill="x", **pad)
        ttk.Label(
            top,
            text="Converta PDF, Word, Excel, PowerPoint, HTML, CSV e texto para Markdown.",
            font=("Segoe UI", 10),
        ).pack(anchor="w")

        # Linha: selecionar arquivo
        row = ttk.Frame(self.root)
        row.pack(fill="x", **pad)
        self.select_btn = ttk.Button(
            row, text="Selecionar arquivo…", command=self.on_select
        )
        self.select_btn.pack(side="left")
        self.path_var = tk.StringVar(value="Nenhum arquivo selecionado.")
        ttk.Label(row, textvariable=self.path_var, style="Muted.TLabel").pack(
            side="left", padx=10
        )

        # Linha: acoes
        actions = ttk.Frame(self.root)
        actions.pack(fill="x", **pad)
        self.convert_btn = ttk.Button(
            actions, text="Converter", command=self.on_convert, state="disabled"
        )
        self.convert_btn.pack(side="left")
        self.save_btn = ttk.Button(
            actions, text="Salvar .md…", command=self.on_save, state="disabled"
        )
        self.save_btn.pack(side="left", padx=8)

        # Progresso em porcentagem (barra + rotulo "NN%")
        self.percent_var = tk.StringVar(value="0%")
        ttk.Label(actions, textvariable=self.percent_var,
                  style="Percent.TLabel", width=5, anchor="e").pack(side="right")
        self.progress = ttk.Progressbar(
            actions, style="Dark.Horizontal.TProgressbar",
            mode="determinate", maximum=100, length=200
        )
        self.progress.pack(side="right", padx=8)

        # Preview
        ttk.Label(self.root, text="Pré-visualização do Markdown:").pack(
            anchor="w", padx=12
        )
        self.preview = scrolledtext.ScrolledText(
            self.root, wrap="word", font=("Consolas", 10),
            bg=d["entry_bg"], fg=d["fg"], insertbackground=d["fg"],
            selectbackground=d["select"], selectforeground=d["fg"],
            relief="flat", borderwidth=8, highlightthickness=1,
            highlightbackground=d["border"], highlightcolor=d["accent"],
        )
        self.preview.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        # Status
        self.status_var = tk.StringVar(value="Pronto.")
        ttk.Label(self.root, textvariable=self.status_var, style="Status.TLabel",
                  anchor="w", padding=(8, 4)).pack(fill="x", side="bottom")

    # ---- barra de progresso animada ----
    # markitdown.convert() e uma chamada unica sem eventos de progresso, entao
    # nao ha % real. A barra sobe de forma assintotica ate ~95% enquanto converte
    # e salta para 100% ao concluir — feedback visual honesto sobre o limite.

    def _start_progress(self):
        self._progress_value = 0.0
        self.progress["value"] = 0
        self.percent_var.set("0%")
        self._tick_progress()

    def _tick_progress(self):
        # Aproxima 95% em passos decrescentes (ease-out).
        remaining = 95.0 - self._progress_value
        self._progress_value += max(remaining * 0.08, 0.3)
        if self._progress_value > 95.0:
            self._progress_value = 95.0
        self.progress["value"] = self._progress_value
        self.percent_var.set(f"{int(self._progress_value)}%")
        self._progress_job = self.root.after(120, self._tick_progress)

    def _stop_progress(self, complete: bool):
        if self._progress_job is not None:
            self.root.after_cancel(self._progress_job)
            self._progress_job = None
        value = 100 if complete else 0
        self.progress["value"] = value
        self.percent_var.set(f"{value}%")

    # ---- acoes ----

    def on_select(self):
        path = filedialog.askopenfilename(
            title="Escolha um arquivo para converter", filetypes=FILE_TYPES
        )
        if not path:
            return
        self.source_path = path
        self.path_var.set(os.path.basename(path))
        self.convert_btn.config(state="normal")
        self.save_btn.config(state="disabled")
        self.status_var.set(f"Selecionado: {path}")

    def on_convert(self):
        if not self.source_path:
            return
        # Desabilita UI e roda conversao em thread separada (nao trava a janela).
        self.select_btn.config(state="disabled")
        self.convert_btn.config(state="disabled")
        self.save_btn.config(state="disabled")
        self.status_var.set("Convertendo…")
        self._start_progress()

        path = self.source_path
        threading.Thread(target=self._convert_worker, args=(path,), daemon=True).start()

    def _convert_worker(self, path):
        try:
            markdown = self.md.convert(path).markdown
            self.root.after(0, self._on_convert_ok, markdown)
        except MarkItDownException as e:
            self.root.after(0, self._on_convert_err, f"Falha na conversão:\n{e}")
        except Exception as e:  # qualquer erro inesperado nao deve derrubar o app
            self.root.after(0, self._on_convert_err, f"Erro inesperado:\n{e}")

    def _on_convert_ok(self, markdown):
        self.result_markdown = markdown
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", markdown)
        self._stop_progress(complete=True)
        self._restore_buttons()
        self.save_btn.config(state="normal")
        self.status_var.set("Conversão concluída. Revise e salve o .md.")

    def _on_convert_err(self, message):
        self._stop_progress(complete=False)
        self._restore_buttons()
        self.status_var.set("Erro na conversão.")
        messagebox.showerror("Tomark", message)

    def _restore_buttons(self):
        self.select_btn.config(state="normal")
        self.convert_btn.config(state="normal")

    def on_save(self):
        if not self.result_markdown:
            return
        default_name = "saida.md"
        if self.source_path:
            base = os.path.splitext(os.path.basename(self.source_path))[0]
            default_name = base + ".md"

        out = filedialog.asksaveasfilename(
            title="Salvar Markdown",
            defaultextension=".md",
            initialfile=default_name,
            filetypes=[("Markdown", "*.md"), ("Todos os arquivos", "*.*")],
        )
        if not out:
            return
        try:
            with open(out, "w", encoding="utf-8") as f:
                f.write(self.result_markdown)
            self.status_var.set(f"Salvo em: {out}")
            messagebox.showinfo("Tomark", f"Arquivo salvo:\n{out}")
        except OSError as e:
            messagebox.showerror("Tomark", f"Não foi possível salvar:\n{e}")


def _selftest(paths):
    """Conversao headless (sem janela) p/ validar o pipeline empacotado.
    Uso: MarkItDownGUI.exe --selftest arquivo1 [arquivo2 ...]
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
    # stdout pode nao existir no modo --windowed; gravar log sempre.
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

    root = tk.Tk()
    MarkItDownApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
