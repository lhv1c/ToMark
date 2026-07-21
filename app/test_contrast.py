"""Trava o contraste minimo da UI (PRODUCT.md: meta WCAG 2.1 AA).

Sem isto, a proxima pessoa que "ajusta uma cor" desfaz o trabalho sem saber.
Rode com: python app/test_contrast.py
"""

from markitdown_gui import ACTION, ACTION_HOVER, BADGE_COLOR, GHOST_TEXT, HINT

# Fundos reais do CustomTkinter (tema dark-blue), por indice (claro, escuro).
PANEL = ("#e5e5e5", "#212121")     # CTkFrame: o painel da fila
ROW_SELECTED = ("#cfe3f7", "#264f78")

AA_TEXT = 4.5


def _rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def _luminance(value):
    def channel(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = map(channel, _rgb(value))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg):
    hi, lo = sorted((_luminance(fg), _luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def check(label, fg, bg, minimum=AA_TEXT):
    ratio = contrast(fg, bg)
    assert ratio >= minimum, f"{label}: {ratio:.2f}:1 < {minimum}:1 ({fg} sobre {bg})"
    return ratio


def main():
    for mode in (0, 1):
        theme = "claro" if mode == 0 else "escuro"

        # O nome do arquivo e legivel em todo fundo de linha que existe.
        for name, bg in (("painel", PANEL), ("selecionada", ROW_SELECTED)):
            check(f"nome do arquivo / linha {name} ({theme})",
                  GHOST_TEXT[mode], bg[mode])

        # Badge de estado: passa no painel E na linha selecionada. A linha
        # selecionada e o caso que a versao anterior errava.
        for status, pair in BADGE_COLOR.items():
            check(f"badge {status} / painel ({theme})", pair[mode], PANEL[mode])
            check(f"badge {status} / linha selecionada ({theme})",
                  pair[mode], ROW_SELECTED[mode])

        # Estado vazio: primeira instrucao que um usuario novo le.
        check(f"dica do estado vazio ({theme})", HINT[mode], PANEL[mode])

        # CTA em repouso E em hover. O hover era o furo: clarear derrubava
        # o texto branco pra 4.33:1.
        check(f"CTA em repouso ({theme})", "#ffffff", ACTION[mode])
        check(f"CTA em hover ({theme})", "#ffffff", ACTION_HOVER[mode])

    assert ACTION != ACTION_HOVER, "hover precisa diferir do repouso"
    assert contrast("#ffffff", ACTION_HOVER[0]) > contrast("#ffffff", ACTION[0]), \
        "hover deve escurecer, nao clarear"

    print("contraste OK — todos os pares passam 4.5:1 nos dois temas")


if __name__ == "__main__":
    main()
