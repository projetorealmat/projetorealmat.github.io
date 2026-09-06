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
        "realmat-editorial-intro",
        "realmat-featured",
        "Ler o PDF",
        'href="/livros/"',
        'href="/contribuir/"',
        'src="/assets/js/realmat.js"',
    ),
    "livros/index.html": (
        "realmat-catalog-list",
        "realmat-book-entry",
        'href="/livros/forallx/"',
        'href="/assets/books/forallx.pdf"',
    ),
    "livros/forallx/index.html": (
        "realmat-page",
        "realmat-book-overview",
        "Ler no navegador",
        'href="/assets/books/forallx.pdf"',
        'target="_blank"',
        'download="forallx.pdf"',
        'href="/contribuir/"',
    ),
    "sobre/index.html": (
        "realmat-page",
        "Uma biblioteca aberta de matemática",
    ),
    "contribuir/index.html": (
        "realmat-page",
        "Projetos de tradução",
        "realmat-contribution-card",
        "https://github.com/projetorealmat/forallx/issues",
        "https://github.com/projetorealmat/forallx",
        'target="_blank"',
        'rel="noopener noreferrer"',
    ),
    "buscar/index.html": (
        "realmat-search-results",
        "REALMAT_SEARCH_INDEX",
        'id="realmat-search-input"',
    ),
    "atualizacoes/index.html": (
        "realmat-page",
        "Histórico de novas obras e versões.",
        "forallx-disponivel",
    ),
}

FORBIDDEN_PAGE_MARKERS = {
    "index.html": (
        "realmat-hero",
        "realmat-statement",
        "Escolha o caminho que você precisa",
    ),
    "livros/index.html": (
        "https://github.com/projetorealmat/forallx",
    ),
    "livros/forallx/index.html": (
        "<iframe",
        "realmat-book-reader__frame",
        'href="#forallx-reader-frame"',
        "https://github.com/projetorealmat/forallx",
    ),
    "contribuir/index.html": (
        "Compartilhe",
        "Link direto",
    ),
}

REQUIRED_ASSETS = (
    "assets/css/main.css",
    "assets/js/realmat.js",
    "assets/books/forallx.pdf",
)


def _check_internal_links(errors):
    for path in ROOT.rglob("*.html"):
        content = path.read_text(encoding="utf-8")
        if "<iframe" in content:
            errors.append(f"{path.relative_to(ROOT)}: leitor embutido não permitido")

        for raw_href in re.findall(r'href="([^"]+)"', content):
            if raw_href.startswith(("#", "http://", "https://", "mailto:", "tel:")):
                if raw_href == "#":
                    errors.append(
                        f"{path.relative_to(ROOT)}: link vazio sem destino"
                    )
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

    forallx = ROOT / "livros" / "forallx" / "index.html"
    if forallx.exists():
        content = forallx.read_text(encoding="utf-8")
        browser_link = re.search(
            r'<a[^>]+href="/assets/books/forallx\.pdf"[^>]+target="_blank"'
            r'[^>]*>Ler no navegador',
            content,
        )
        download_link = re.search(
            r'<a[^>]+href="/assets/books/forallx\.pdf"[^>]+download="forallx\.pdf"',
            content,
        )
        if not browser_link:
            errors.append(
                "livros/forallx/index.html: PDF não abre no visualizador do navegador"
            )
        if not download_link:
            errors.append(
                "livros/forallx/index.html: download explícito do PDF ausente"
            )

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
