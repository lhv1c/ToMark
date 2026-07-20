#!/usr/bin/env bash
# Build do Tomark em binario (pasta, --onedir), Linux.
# Rode da raiz do projeto:  ./app/build.sh
# Saida: dist/Tomark/Tomark
set -euo pipefail
cd "$(dirname "$0")/.."

PY=./.venv/bin/python
[ -x "$PY" ] || { echo "Virtualenv nao encontrada em .venv. Crie com: python3 -m venv .venv" >&2; exit 1; }

# ponytail: --add-data usa ':' no Linux (no Windows e ';'). Sem --icon: PyInstaller
# so aplica icone em exe/app bundle; no Linux o icone vem do PNG via iconphoto.
"$PY" -m PyInstaller --noconfirm --clean --windowed --name Tomark \
    --add-data "app/icon.png:." \
    --collect-all magika \
    --collect-all customtkinter \
    --collect-all tkinterdnd2 \
    --collect-submodules markitdown \
    app/markitdown_gui.py

echo
echo "Build concluido. Executavel em: dist/Tomark/Tomark"
