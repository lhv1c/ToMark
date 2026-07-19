# Tomark

App desktop (Windows e Linux) que converte arquivos para **Markdown** — sem terminal, sem linha de comando.

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

### Windows

Requisitos: Python 3.10+.

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

### Linux

**Pronto pra usar (AppImage):** baixe `Tomark-x86_64.AppImage` nos artifacts do
workflow [`Build Linux AppImage`](../../actions/workflows/build-linux-appimage.yml)
(ou na aba Releases, se publicado numa tag `v*`). É buildado em Ubuntu 18.04
(glibc 2.27), então roda em distros antigas — Linux Mint 19 em diante.

```bash
chmod +x Tomark-x86_64.AppImage
./Tomark-x86_64.AppImage
```

**Compilar do código:** requisitos Python 3.10+ e o Tk do sistema (o Python do
Linux não traz `tkinter`):

```bash
sudo apt install python3-tk        # Debian/Ubuntu
# sudo dnf install python3-tkinter # Fedora
# sudo pacman -S tk                # Arch
```

```bash
# 1. Ambiente (uma vez)
python3 -m venv .venv
./.venv/bin/python -m pip install "./packages/markitdown[pptx,docx,xlsx,xls,pdf]" pyinstaller

# 2. Build
./app/build.sh
```

Saída: `dist/Tomark/Tomark`.

Sem empacotar:

```bash
./.venv/bin/python app/markitdown_gui.py
```

## Estrutura

| Caminho | O quê |
|---------|-------|
| `app/markitdown_gui.py` | Interface gráfica (tkinter, dark mode). |
| `app/build.ps1` | Build do `.exe` no Windows (PyInstaller). |
| `app/build.sh` | Build do binário no Linux (PyInstaller). |
| `app/appimage/` | Empacotamento em AppImage, build em Ubuntu 18.04 (CI). |
| `app/make_icon.py` | Gera `app/icon.ico`. |
| `packages/markitdown/` | Biblioteca de conversão (motor). |

## Créditos e licença

Tomark é uma versão com interface gráfica baseada em
[**microsoft/markitdown**](https://github.com/microsoft/markitdown), que faz todo
o trabalho de conversão. Projeto original sob licença **MIT** — veja
[`LICENSE`](LICENSE). Este projeto mantém a mesma licença.
