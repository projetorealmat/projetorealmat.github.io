#!/usr/bin/env python3
"""Smoke tests for the generated REALMAT Pages site."""

from pathlib import Path
import sys

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")

EXPECTED_PAGES = {
    "index.html": (
        'class="realmat-masthead"',
        "realmat-hero",
        "realmat-featured",
        'data-menu-toggle',
        'href="/livros/"',
        'src="/assets/js/realmat.js"',
    ),
    "livros/index.html": (
        "realmat-book-card",
        'realmat-book-card__cover realmat-cover realmat-cover--forallx',
        "https://github.com/projetorealmat/forallx",
    ),
    "sobre/index.html": ("realmat-page", "Uma biblioteca aberta de matemática"),
    "contribuir/index.html": ("realmat-page", "Fluxo de colaboração"),
    "atualizacoes/index.html": ("realmat-page", "Estrutura inicial do portal"),
}

REQUIRED_ASSETS = (
    "assets/css/main.css",
    "assets/js/realmat.js",
)


def main() -> int:
    errors = []

    for relative_path, markers in EXPECTED_PAGES.items():
        path = ROOT / relative_path
        if not path.exists():
            errors.append(f"página gerada ausente: {relative_path}")
            continue

        content = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in content:
                errors.append(f"{relative_path}: marcador ausente: {marker}")
        if "{{" in content or "{%" in content:
            errors.append(f"{relative_path}: expressão Liquid não processada")

    for relative_path in REQUIRED_ASSETS:
        if not (ROOT / relative_path).exists():
            errors.append(f"recurso gerado ausente: {relative_path}")

    if errors:
        print("Generated site checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Generated site checks passed: {len(EXPECTED_PAGES)} pages and {len(REQUIRED_ASSETS)} assets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
