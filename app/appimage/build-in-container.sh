#!/bin/bash
# Roda DENTRO de um container ubuntu:18.04 (glibc 2.27) para gerar um
# AppImage compativel com distros antigas (ex.: Linux Mint 19).
# Chamado pelo workflow .github/workflows/build-linux-appimage.yml via:
#   docker run --rm -v "$PWD":/workspace -w /workspace ubuntu:18.04 bash app/appimage/build-in-container.sh
set -euo pipefail

# ponytail: 18.04 e EOL, os espelhos padrao nao servem mais o repo bionic.
sed -i \
    -e 's|archive.ubuntu.com|old-releases.ubuntu.com|g' \
    -e 's|security.ubuntu.com|old-releases.ubuntu.com|g' \
    /etc/apt/sources.list

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends \
    software-properties-common curl ca-certificates file build-essential

add-apt-repository -y ppa:deadsnakes/ppa
apt-get update
apt-get install -y --no-install-recommends \
    python3.10 python3.10-venv python3.10-dev python3.10-tk

python3.10 -m venv /tmp/venv
/tmp/venv/bin/pip install --upgrade pip
/tmp/venv/bin/pip install -r app/requirements-build.txt

/tmp/venv/bin/python -m PyInstaller --noconfirm --clean --windowed --name Tomark \
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
