# Tomark — notas de desenvolvimento

App desktop (Windows, dark mode) que converte arquivos para Markdown numa janela
— sem terminal. Envolve a biblioteca `markitdown`. Documentação de usuário está no
[README principal](../README.md); aqui ficam detalhes de build.

## Recompilar o .exe

Precisa da virtualenv `.venv` na raiz do projeto:

```powershell
# 1. Ambiente (uma vez)
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install ".\packages\markitdown[pptx,docx,xlsx,xls,pdf]" pyinstaller

# 2. Build
.\app\build.ps1
```

Saída: `dist\Tomark\Tomark.exe`.

`--collect-all magika` no build é obrigatório — magika embarca um modelo ONNX que
o PyInstaller não detecta sozinho.

## Ícone

`app\make_icon.py` gera `app\icon.ico` (badge "M↓" na paleta dark). Rode após
alterar o desenho:

```powershell
.\.venv\Scripts\python.exe app\make_icon.py
```

## Teste headless (sem janela)

Valida o pipeline empacotado convertendo arquivos e gravando `selftest_report.txt`:

```powershell
.\dist\Tomark\Tomark.exe --selftest caminho\arquivo.pdf
```
