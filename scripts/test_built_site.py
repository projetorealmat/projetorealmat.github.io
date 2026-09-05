#!/usr/bin/env python3
"""Smoke tests for the generated REALMAT Pages site."""

from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")

EXPECTED_PAGES = {
    "index.html": (
        'class="realmat-masthead"',
        "realmat-hero",
        "realmat-featured",
        "Como usar o portal",
        'href="/livros/"',
        'href="/contribuir/"',
        'src="/assets/js/realmat.js"',
    ),
    "livros/index.html": (
        "realmat-book-card",
        'realmat-book-card__cover realmat-cover realmat-cover--forallx',
        'href="/livros/forallx/"',
        "Cada obra pode ser lida diretamente no portal.",
    ),
    "livros/forallx/index.html": (
        "realmat-book-reader",
        'id="forallx-reader"',
        "Ir para o leitor",
        'href="#forallx-reader-frame"',
        'src="/assets/books/forallx.pdf"',
        "assets/books/forallx.pdf",
        'href="/contribuir/"',
    ),
    "sobre/index.html": ("realmat-page", "Uma biblioteca aberta de matemática"),
    "contribuir/index.html": (
        "realmat-page",
        "Projetos disponíveis",
        "realmat-contribution-links",
        "https://github.com/projetorealmat/forallx/issues",
        "https://github.com/projetorealmat/forallx",
        'target="_blank"',
        'rel="noopener noreferrer"',
    ),
    "atualizacoes/index.html": (
        "realmat-page",
        "Histórico de novas obras e versões.",
        "forallx-disponivel",
        'href="/livros/forallx/"',
    ),
}

FORBIDDEN_PAGE_MARKERS = {
    "index.html": ("/#recursos", "/livros/#traducoes"),
    "livros/index.html": ("https://github.com/projetorealmat/forallx",),
    "livros/forallx/index.html": ("https://github.com/projetorealmat/forallx",),
    "contribuir/index.html": ("Compartilhe", "Link direto"),
}

REQUIRED_ASSETS = (
    "assets/css/main.css",
    "assets/js/realmat.js",
    "assets/books/forallx.pdf",
)


def _check_internal_links(errors):
    for path in ROOT.rglob("*.html"):
        content = path.read_text(encoding="utf-8")
        for raw_href in re.findall(r'href="([^"]+)"', content):
            if raw_href.startswith(("#", "http://", "https://", "mailto:", "tel:")):
                continue

            parsed = urlsplit(raw_href)
            target = parsed.path
            if not target.startswith("/"):
                continue

            if target == "/":
                target_path = ROOT / "index.html"
            elif target.endswith("/"):
                target_path = ROOT / target.lstrip("/") / "index.html"
            else:
                target_path = ROOT / target.lstrip("/")

            if not target_path.exists():
                errors.append(
                    f"{path.relative_to(ROOT)}: link interno sem destino: {raw_href}"
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
        for marker in FORBIDDEN_PAGE_MARKERS.get(relative_path, ()):
            if marker in content:
                errors.append(f"{relative_path}: marcador proibido: {marker}")
        if "{{" in content or "{%" in content:
            errors.append(f"{relative_path}: expressão Liquid não processada")

        if relative_path == "index.html":
            nav_marker = content.find('id="site-nav"')
            nav_start = content.rfind("<nav", 0, nav_marker + 1)
            nav_end = content.find("</nav>", nav_marker)
            nav = content[nav_start:nav_end] if nav_start >= 0 and nav_end >= 0 else ""
            for label in ("Traduções", "Recursos", "Atualizações"):
                if label in nav:
                    errors.append(f"index.html: item antigo ainda aparece no menu: {label}")
            if nav.count('class="realmat-nav-link') != 3:
                errors.append("index.html: menu principal não contém exatamente três itens")

    for relative_path in REQUIRED_ASSETS:
        if not (ROOT / relative_path).exists():
            errors.append(f"recurso gerado ausente: {relative_path}")

    _check_internal_links(errors)

    if errors:
        print("Generated site checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Generated site checks passed: {len(EXPECTED_PAGES)} pages and "
        f"{len(REQUIRED_ASSETS)} assets."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
