import os


def next_selection(count: int, removed: int):
    """Indice a selecionar depois de remover `removed` de uma lista de `count`
    itens (contagem ANTES da remocao). None quando a lista fica vazia."""
    if count <= 1:
        return None
    return min(removed, count - 2)


def move_selection(count: int, current, delta: int):
    """Indice depois de mover `delta` na lista. Sem selecao, entra pela ponta
    de onde a tecla veio. Nas bordas fica parado — nao circula, pra que segurar
    a seta nao volte pro topo sem o usuario perceber."""
    if count <= 0:
        return None
    if current is None:
        return 0 if delta > 0 else count - 1
    return max(0, min(count - 1, current + delta))


def resolve_output_path(source_path: str) -> str:
    """.md ao lado do original; se ja existir, acrescenta ' (1)', ' (2)'..."""
    folder = os.path.dirname(source_path)
    base = os.path.splitext(os.path.basename(source_path))[0]
    candidate = os.path.join(folder, base + ".md")
    n = 1
    while os.path.exists(candidate):
        candidate = os.path.join(folder, f"{base} ({n}).md")
        n += 1
    return candidate
