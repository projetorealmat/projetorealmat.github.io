#!/usr/bin/env python3
"""Static source checks for the REALMAT editorial skin."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

CHECKS = {
    "index.md": (
        "realmat-hero",
        "realmat-featured",
        "repositório",
    ),
    "_includes/masthead.html": (
        "realmat-masthead",
        "data-menu-toggle",
        "realmat-menu-panel",
        'aria-current="page"',
        'aria-controls="search-content"',
    ),
    "_includes/footer.html": (
        "realmat-footer",
        "Como contribuir",
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
        "projetorealmat/forallx",
    ),
    "assets/css/main.scss": (
        "--realmat-orange",
        "--realmat-orange-dark: #a94a05",
        ".realmat-hero",
        ".realmat-layout .page__footer footer",
        ".realmat-page__container--with-sidebar",
        ".realmat-page__body .page__content a:not(.realmat-button)",
        ".realmat-menu-js .realmat-nav-links",
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
