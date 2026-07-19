"""
Gera app/icon.ico (Windows) e app/icon.png (Linux) — ícone do MarkItDown GUI
(badge Markdown "M v" na paleta dark).
Desenha em alta resolucao (supersampling) e salva .ico multi-tamanho + .png 256.

Uso:  ..\.venv\Scripts\python.exe app\make_icon.py
"""

import os
from PIL import Image, ImageDraw

# Paleta (mesma do app dark mode).
BG = (30, 30, 30, 0)        # transparente fora do badge
BADGE = (37, 37, 38, 255)   # #252526
ACCENT = (76, 194, 255, 255)  # #4cc2ff

SS = 1024  # canvas de trabalho (supersample)


def rounded_rect(draw, box, radius, **kw):
    draw.rounded_rectangle(box, radius=radius, **kw)


def build():
    img = Image.new("RGBA", (SS, SS), BG)
    d = ImageDraw.Draw(img)

    # Badge (retangulo arredondado) com borda accent.
    border = 44
    box = (80, 224, 944, 800)
    rounded_rect(d, box, radius=90, fill=BADGE, outline=ACCENT, width=border)

    # Conteudo em accent: "M" + seta para baixo.
    col = ACCENT
    stroke = 56

    # --- M (lado esquerdo) ---
    top, bot = 336, 688
    # haste esquerda
    d.rectangle((196, top, 196 + stroke, bot), fill=col)
    # haste direita do M
    d.rectangle((468 - stroke, top, 468, bot), fill=col)
    # V interno (dois tracos)
    mid_x = (196 + 468) // 2
    mid_y = 560
    d.line((196 + stroke // 2, top, mid_x, mid_y), fill=col, width=stroke,
           joint="curve")
    d.line((mid_x, mid_y, 468 - stroke // 2, top), fill=col, width=stroke,
           joint="curve")

    # --- seta para baixo (lado direito) ---
    ax = 700           # centro horizontal da seta
    d.rectangle((ax - stroke // 2, top, ax + stroke // 2, 600), fill=col)
    d.polygon([(ax - 96, 560), (ax + 96, 560), (ax, 696)], fill=col)

    # Downscale suave para 256 e salva multi-tamanho.
    base = img.resize((256, 256), Image.LANCZOS)
    here = os.path.dirname(__file__)
    out = os.path.join(here, "icon.ico")
    base.save(out, format="ICO",
              sizes=[(16, 16), (24, 24), (32, 32), (48, 48),
                     (64, 64), (128, 128), (256, 256)])
    print(f"Gravado: {out}")

    # Tk no Linux nao le .ico; iconphoto precisa de PNG.
    out_png = os.path.join(here, "icon.png")
    base.save(out_png, format="PNG")
    print(f"Gravado: {out_png}")


if __name__ == "__main__":
    build()
