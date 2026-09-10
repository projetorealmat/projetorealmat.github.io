#!/usr/bin/env python3
"""Source-level acceptance checks for the REALMat portal."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "_config.yml": (
        'title: "REALMat"',
        'subtitle: "Recursos Educacionais Abertos na Licenciatura em Matemática"',
        'url: "https://projetorealmat.github.io"',
        "- generated",
    ),
    "_data/books.json": (
        '"current_version"',
        '"releases"',
        '"release_date"',
    ),
    ".github/workflows/pages.yml": (
        "scripts/test_catalog_evolution.py",
        "scripts/validate_catalog.py",
        "scripts/download_catalog_assets.py",
        "scripts/generate_book_pages.py",
    ),
    ".github/workflows/catalog-sync.yml": (
        "repository_dispatch",
        "github.event.client_payload",
        "projetorealmat/.github/.github/workflows/portal-catalog-sync.yml@v2",
        "payload:",
        "validate_catalog.py",
    ),
    "_layouts/default.html": (
        'id="wrapper"',
        'id="main"',
        "include massively-intro.html",
        "include massively-header.html",
        "include massively-nav.html",
        "include massively-footer.html",
        "html5up.net/massively",
        "assets/css/main.css",
        "assets/css/realmat.css",
        'rel="preload"',
        "images/realmat-bg.jpg",
        "REALMat</li>",
        "assets/js/jquery.min.js",
        "assets/js/main.js",
    ),
    "_includes/massively-intro.html": (
        'id="intro"',
        "REALMat",
        "<h1>REALMat</h1>",
        "Recursos Educacionais Abertos na Licenciatura em Matemática",
        "scrolly",
    ),
    "_includes/massively-header.html": (
        'id="header"',
        "REALMat",
        "brand-real",
        "brand-l",
        "brand-mat",
        "realmat-wordmark__icon",
        'viewBox="0 0 32 32"',
    ),
    "_includes/massively-nav.html": (
        'id="nav"',
        "site.data.navigation.main",
        "fa-search",
        "fa-github",
    ),
    "_includes/massively-footer.html": (
        "site.data.books",
        "Como contribuir",
        "Organização do projeto",
    ),
    "index.md": (
        'class="post featured',
        'class="posts',
        "REALMat",
        "featured_book",
        "featured_release",
        "/livros/",
        "/contribuir/",
    ),
    "_pages/livros.md": (
        "site.data.books",
        "book.releases",
        "book.current_version",
        "current.pdf_path",
    ),
    "_pages/contribuir.md": (
        "for book in site.data.books",
        "current.repository",
        "Discussões e correções",
    ),
    "_pages/arquivo.md": (
        "book.releases",
        "release.version",
        "release.release_url",
    ),
    "_pages/topicos.md": (
        "group_by:",
        "site.data.books",
        "book.title",
    ),
    "_pages/buscar.md": (
        "REALMAT_SEARCH_INDEX",
        "site.data.books",
        "search_index_count",
    ),
    "assets/css/main.css": (
        "Massively by HTML5 UP",
        "#intro",
        "#wrapper",
        "#navPanel",
        "fontawesome-all.min.css",
    ),
    "assets/css/noscript.css": ("#intro", "#wrapper"),
    "assets/css/realmat.css": (
        "--realmat-blue",
        "--realmat-gold",
        "--realmat-cyan",
        "--realmat-orange",
        "realmat-bg",
        "realmat-logo",
        "brand-real",
        "realmat-wordmark__icon",
        "#wrapper.fade-in:before",
        "realmat-book-poster",
        "@media",
    ),
    "assets/js/main.js": ("navPanel", "scrollex", "#intro"),
    "assets/js/realmat-search.js": (
        "REALMAT_SEARCH_INDEX",
        "realmat-search",
        "URLSearchParams",
        ".every",
    ),
    "scripts/validate_catalog.py": ("current_version", "RELEASE_FIELDS", "sha256"),
    "scripts/download_catalog_assets.py": ("sha256", "pdf_url", "current_release"),
    "scripts/generate_book_pages.py": ("OUTPUT_DIR", "current_release", "Histórico editorial"),
}

FORBIDDEN = (
    "This is Massively",
    "Lorem ipsum",
    "minimal-mistakes",
    '<iframe',
    'href="#"',
)


def main() -> int:
    errors = []

    for relative_path, markers in REQUIRED.items():
        path = ROOT / relative_path
        if not path.exists():
            errors.append(f"arquivo ausente: {relative_path}")
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        for marker in markers:
            if marker not in content:
                errors.append(f"{relative_path}: marcador ausente: {marker}")

    if (ROOT / "_pages" / "forallx.md").exists():
        errors.append("_pages/forallx.md: página fixa deve ser gerada pelo catálogo")

    for relative_path in ("index.md", "_pages/livros.md", "_pages/contribuir.md", "_pages/topicos.md"):
        path = ROOT / relative_path
        if path.exists() and "/livros/forallx/" in path.read_text(encoding="utf-8"):
            errors.append(f"{relative_path}: referência fixa a forallx encontrada")

    if errors:
        print("Source-level Massively checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Source-level Massively checks passed: {len(REQUIRED)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
