#!/usr/bin/env python3
"""Static source checks for the REALMAT editorial skin."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

CHECKS = {
    "index.md": (
        "realmat-hero",
        "realmat-featured",
        "Como usar o portal",
    ),
    "_data/navigation.yml": (
        'title: "Livros"',
        'title: "Sobre"',
        'title: "Contribuir"',
    ),
    "_includes/masthead.html": (
        "realmat-masthead",
        "data-menu-toggle",
        "realmat-menu-panel",
        "link_is_active",
        'aria-controls="search-content"',
    ),
    "_includes/footer.html": (
        "realmat-footer",
        "Como contribuir",
        "Histórico de atualizações",
    ),
    "_layouts/default.html": (
        "realmat-layout",
        "head.html",
        "scripts.html",
        "include masthead.html",
        'id="search-content"',
    ),
    "_layouts/home.html": (
        "realmat-home",
        "realmat-featured",
    ),
    "_layouts/single.html": (
        "realmat-page",
        "page__content",
        "realmat-page__container--with-sidebar",
        'class="page__meta realmat-page__meta"',
        "page_description",
        "page__taxonomy.html",
        "page__date.html",
        "page__related.html",
        "post_pagination.html",
    ),
    "_pages/livros.md": (
        "realmat-book-card",
        'class="realmat-book-card__cover realmat-cover realmat-cover--forallx"',
        "Cada obra pode ser lida diretamente no portal.",
    ),
    "_pages/forallx.md": (
        "realmat-book-reader",
        'id="forallx-reader"',
        'id="forallx-reader-frame"',
        "Ir para o leitor",
        "assets/books/forallx.pdf",
        "/contribuir/",
    ),
    "_pages/contribuir.md": (
        "Projetos disponíveis",
        "realmat-contribution-links",
        "https://github.com/projetorealmat/forallx/issues",
        'target="_blank"',
    ),
    "_pages/atualizacoes.md": (
        "Histórico de novas obras e versões.",
        "forallx-disponivel",
    ),
    "_config.yml": (
        "atom_feed:",
        "hide: true",
    ),
    "assets/css/main.scss": (
        "--realmat-orange",
        "--realmat-orange-dark: #a94a05",
        ".realmat-hero",
        ".realmat-book-reader",
        ".realmat-book-reader__frame",
        ".realmat-wayfinding",
        ".realmat-update-list",
        ".realmat-contribution-links",
        ".realmat-layout .page__footer footer",
        ".realmat-page__container--with-sidebar",
        ".realmat-page__body .page__content a:not(.realmat-button)",
        ".realmat-menu-js .realmat-nav-links",
        "scroll-margin-top",
        "@media (max-width: 760px)",
    ),
    "assets/js/realmat.js": (
        "data-menu-toggle",
        "aria-expanded",
        "is-open",
        "MutationObserver",
        "is--visible",
        "panel.contains(document.activeElement)",
        "toggle.focus()",
    ),
    ".github/workflows/pages.yml": (
        "url: $" "{{ steps.deployment.outputs.page_url }}",
        "scripts/test_built_site.py ./_site",
        "Verificar o site gerado",
    ),
}

FORBIDDEN = {
    "index.md": ("https://github.com/projetorealmat", "repositório"),
    "_data/navigation.yml": (
        'title: "Traduções"',
        'title: "Recursos"',
        'title: "Atualizações"',
    ),
    "_includes/masthead.html": ("https://github.com/projetorealmat",),
    "_includes/footer.html": (
        "https://github.com/projetorealmat",
        "/feed.xml",
    ),
    "_pages/livros.md": (
        "https://github.com/projetorealmat",
        "repositório",
    ),
    "_pages/forallx.md": ("https://github.com/projetorealmat/forallx",),
    "_pages/contribuir.md": (
        'share: true',
        'link: "https://github.com/projetorealmat"',
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

    workflow = ROOT / ".github/workflows/pages.yml"
    if workflow.exists():
        workflow_content = workflow.read_text(encoding="utf-8")
        if r"url: \${{" in workflow_content:
            errors.append(".github/workflows/pages.yml: URL do ambiente contém uma barra invertida")

    if errors:
        print("Editorial skin checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Editorial skin checks passed: {len(CHECKS)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
