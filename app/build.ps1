# Build do Tomark em .exe (pasta, --onedir).
# Rode da raiz do projeto:  .\app\build.ps1
# Saida: dist\Tomark\Tomark.exe

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$py = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $py)) {
    throw "Virtualenv nao encontrada em .venv. Crie com: py -3.11 -m venv .venv"
}

& $py -m PyInstaller --noconfirm --clean --windowed --name Tomark `
    --icon app\icon.ico `
    --add-data "app\icon.ico;." `
    --collect-all magika `
    --collect-submodules markitdown `
    app\markitdown_gui.py

Write-Host ""
Write-Host "Build concluido. Executavel em: dist\Tomark\Tomark.exe"
