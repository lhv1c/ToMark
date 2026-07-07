import os


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
