#!/bin/bash
# Roda DENTRO de um container python:3.11-buster (Debian 10, glibc 2.28) para
# gerar um AppImage compativel com distros antigas (ex.: Linux Mint 20+).
# Chamado pelo workflow .github/workflows/build-linux-appimage.yml via:
#   docker run --rm -v "$PWD":/workspace -w /workspace python:3.11-buster bash app/appimage/build-in-container.sh
set -euo pipefail

# ponytail: buster saiu do mirror padrao (deb.debian.org, 404); so sobra em
# archive.debian.org, que congela o Release do dia do EOL em diante -- sem
# desligar o Check-Valid-Until o apt recusa o repo por "expirado".
sed -i 's|deb.debian.org|archive.debian.org|g' /etc/apt/sources.list
echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid-until

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates file

python3 -c "import tkinter"  # falha cedo se a imagem nao tiver Tk embutido

python3 -m pip install --upgrade pip
python3 -m pip install -r app/requirements-build.txt

python3 -m PyInstaller --noconfirm --clean --windowed --name Tomark \
    --add-data "app/icon.png:." \
    --collect-all magika \
    --collect-all customtkinter \
    --collect-submodules markitdown \
    app/markitdown_gui.py

# --- Monta AppDir ---
rm -rf AppDir
mkdir -p AppDir/usr/bin
cp -r dist/Tomark AppDir/usr/bin/Tomark
install -m 755 app/appimage/AppRun AppDir/AppRun
cp app/appimage/Tomark.desktop AppDir/Tomark.desktop
cp app/icon.png AppDir/tomark.png

curl -sSL -o /tmp/appimagetool \
    https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x /tmp/appimagetool

mkdir -p dist-appimage
# --appimage-extract-and-run: containers geralmente nao tem /dev/fuse.
/tmp/appimagetool --appimage-extract-and-run AppDir dist-appimage/Tomark-x86_64.AppImage

echo "AppImage gerado: dist-appimage/Tomark-x86_64.AppImage"
