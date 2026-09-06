#!/usr/bin/env python3
"""Static checks for the Massively-adapted REALMAT site."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

CHECKS = {
    "index.md": (
        "realmat-editorial-intro",
        "realmat-featured",
        "Biblioteca",
        "Ler o PDF",
    ),
    "_config.yml": (
        'title: "REALMAT"',
        'url: "https://projetorealmat.github.io"',
        "include:",
    ),
    "_includes/masthead.html": (
        "realmat-masthead",
        "data-menu-toggle",
        "realmat-menu-panel",
        'id="realmat-search-toggle"',
    ),
    "_includes/footer.html": (
        "realmat-footer",
        "Livros",
        "Contribuir",
    ),
    "_layouts/default.html": (
        "realmat-layout",
        "realmat-skip-link",
        "realmat-search-panel",
        "assets/css/main.css",
        "assets/js/realmat.js",
    ),
    "_layouts/home.html": (
        "realmat-home",
        "layout: default",
    ),
    "_layouts/single.html": (
        "realmat-page",
        "realmat-page__hero",
        "realmat-prose",
    ),
    "_pages/livros.md": (
        "realmat-catalog-list",
        "realmat-book-entry",
        "assets/books/forallx.pdf",
    ),
    "_pages/forallx.md": (
        "realmat-book-overview",
        "Ler no navegador",
        'download="forallx.pdf"',
        "assets/books/forallx.pdf",
    ),
    "_pages/contribuir.md": (
        "Projetos de tradução",
        "realmat-contribution-card",
        "https://github.com/projetorealmat/forallx/issues",
        "https://github.com/projetorealmat/forallx",
    ),
    "_pages/buscar.md": (
        "realmat-search-results",
        "REALMAT_SEARCH_INDEX",
    ),
    "assets/css/main.scss": (
        "--realmat-orange",
        "realmat-button--primary",
        "realmat-footer",
        "realmat-book-overview",
        "@media (max-width: 760px)",
    ),
    "assets/js/realmat.js": (
        "data-menu-toggle",
        "aria-expanded",
        "search-content",
        "Escape",
        "REALMAT_SEARCH_INDEX",
    ),
}

FORBIDDEN = {
    "_config.yml": (
        "remote_theme:",
        "minimal_mistakes",
        "jekyll-include-cache",
    ),
    "index.md": (
        "realmat-hero",
        "realmat-statement",
        "Escolha o caminho que você precisa",
    ),
    "_includes/footer.html": (
        "Histórico de atualizações",
        "/feed.xml",
    ),
    "_layouts/default.html": (
        "minimal-mistakes",
    ),
    "_layouts/single.html": (
        "sidebar__right",
        "page__meta",
        "post_pagination",
    ),
    "_pages/forallx.md": (
        "<iframe",
        "realmat-book-reader__frame",
        "Ir para o leitor",
    ),
    "assets/css/main.scss": (
        '@import "minimal-mistakes',
        "--realmat-blue",
        "min-height: 600px",
        "realmat-book-reader__frame",
    ),
}


def main() -> int:
    errors = []

    for relative_path, markers in CHECKS.items():
        path = ROOT / relative_path
        if not path.exists():
            errors.append(f"arquivo ausente: {relative_path}")
            continue

        content = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in content:
                errors.append(f"{relative_path}: marcador ausente: {marker}")

        for marker in FORBIDDEN.get(relative_path, ()):
            if marker in content:
                errors.append(f"{relative_path}: marcador proibido: {marker}")

    navigation = ROOT / "_data/navigation.yml"
    if navigation.exists():
        actual_titles = [
            line.strip()
            for line in navigation.read_text(encoding="utf-8").splitlines()
            if line.strip().startswith("- title:")
        ]
        expected_titles = [
            '- title: "Livros"',
            '- title: "Sobre"',
            '- title: "Contribuir"',
        ]
        if actual_titles != expected_titles:
            errors.append(
                "_data/navigation.yml: menu principal diferente do percurso definido"
            )

    if errors:
        print("Massively adaptation checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Massively adaptation checks passed: {len(CHECKS)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
