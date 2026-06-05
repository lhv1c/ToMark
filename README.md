# Tomark

App desktop (Windows) que converte arquivos para **Markdown** numa janela com
tema escuro — sem terminal, sem linha de comando.

Selecione um arquivo, clique **Converter**, veja a pré-visualização e salve o
`.md`. Conversão 100% offline.

## Formatos suportados

PDF, Word (`.docx`), Excel (`.xlsx`, `.xls`), PowerPoint (`.pptx`), HTML, CSV,
TXT, JSON, XML, EPUB.

## Baixar e usar (pronto)

1. Baixe o `.zip` mais recente na aba [**Releases**](../../releases).
2. Extraia a pasta `Tomark`.
3. Dê dois cliques em `Tomark.exe`.

> O `.exe` precisa dos arquivos ao lado dele (pasta `_internal`). Para mover o
> app, copie a **pasta `Tomark` inteira**.

## Compilar do código-fonte

Requisitos: Windows + Python 3.10+.

```powershell
# 1. Ambiente (uma vez)
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install ".\packages\markitdown[pptx,docx,xlsx,xls,pdf]" pyinstaller

# 2. (opcional) regerar o ícone
.\.venv\Scripts\python.exe app\make_icon.py

# 3. Build
.\app\build.ps1
```

Saída: `dist\Tomark\Tomark.exe`.

Para rodar direto pelo Python, sem empacotar:

```powershell
.\.venv\Scripts\python.exe app\markitdown_gui.py
```

## Estrutura

| Caminho | O quê |
|---------|-------|
| `app/markitdown_gui.py` | Interface gráfica (tkinter, dark mode). |
| `app/build.ps1` | Script de build do `.exe` (PyInstaller). |
| `app/make_icon.py` | Gera `app/icon.ico`. |
| `packages/markitdown/` | Biblioteca de conversão (motor). |

## Créditos e licença

Tomark é uma versão com interface gráfica baseada em
[**microsoft/markitdown**](https://github.com/microsoft/markitdown), que faz todo
o trabalho de conversão. Projeto original sob licença **MIT** — veja
[`LICENSE`](LICENSE). Este projeto mantém a mesma licença.
