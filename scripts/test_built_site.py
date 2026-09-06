#!/usr/bin/env python3
"""Smoke tests for the generated REALMAT site using the Massively structure."""

from pathlib import Path
import json
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")

EXPECTED_PAGES = {
    "index.html": (
        'id="intro"',
        'id="header"',
        'id="nav"',
        'id="main"',
        'class="post featured',
        'class="posts',
        "Ler o PDF",
        'href="/livros/"',
        'href="/contribuir/"',
        'src="/assets/js/main.js"',
        "Recursos Educacionais Abertos na Licenciatura em Matemática",
        "realmat-logo",
        "<h1>REALMat</h1>",
        "realmat-wordmark__icon",
        'href="/arquivo/"',
        'href="/topicos/"',
        'href="/images/realmat-bg.jpg"',
        "REALMat</li>",
    ),
    "livros/index.html": (
        'class="realmat-library"',
        "forallx: Lógica",
        'href="/livros/forallx/"',
        'href="/assets/books/forallx.pdf"',
    ),
    "livros/forallx/index.html": (
        'class="post realmat-page"',
        'class="realmat-book-detail"',
        "Ler no navegador",
        'href="/assets/books/forallx.pdf"',
        'target="_blank"',
        'download="forallx.pdf"',
        'href="/contribuir/"',
    ),
    "sobre/index.html": (
        'class="post realmat-page"',
        "Recursos Educacionais Abertos na Licenciatura em Matemática",
        "O REALMat — Recursos Educacionais Abertos na Licenciatura em Matemática — é um projeto de extensão",
    ),
    "contribuir/index.html": (
        'class="post realmat-page"',
        "realmat-contribution",
        "https://github.com/projetorealmat/forallx/issues",
        "https://github.com/projetorealmat/forallx",
        'target="_blank"',
        'rel="noopener noreferrer"',
    ),
    "buscar/index.html": (
        'class="realmat-search"',
        "REALMAT_SEARCH_INDEX",
        'id="realmat-search-input"',
    ),
    "arquivo/index.html": (
        'class="post realmat-page"',
        "realmat-updates",
        "forallx disponível para leitura",
    ),
    "topicos/index.html": (
        'class="post realmat-page"',
        "Lógica formal",
        'href="/livros/forallx/"',
    ),
    "atualizacoes/index.html": (
        'http-equiv="refresh"',
        'href="/arquivo/"',
    ),
}

FORBIDDEN = (
    "This is Massively",
    "Lorem ipsum",
    "minimal-mistakes",
    '<iframe',
    'href="#"',
)

REQUIRED_ASSETS = (
    "assets/css/main.css",
    "assets/css/noscript.css",
    "assets/css/fontawesome-all.min.css",
    "assets/js/jquery.min.js",
    "assets/js/jquery.scrollex.min.js",
    "assets/js/jquery.scrolly.min.js",
    "assets/js/browser.min.js",
    "assets/js/breakpoints.min.js",
    "assets/js/util.js",
    "assets/js/main.js",
    "assets/js/realmat-search.js",
    "assets/webfonts/fa-solid-900.woff2",
    "assets/webfonts/fa-brands-400.woff2",
    "images/bg.jpg",
    "images/overlay.png",
    "images/realmat-bg.jpg",
    "assets/images/realmat-logo.jpg",
    "assets/books/forallx.pdf",
)

def check_navigation_order(errors):
    index = ROOT / "index.html"
    if not index.exists():
        return
    content = index.read_text(encoding="utf-8", errors="replace")
    nav_match = re.search(r'<ul class="links">(.*?)</ul>', content, flags=re.S)
    if not nav_match:
        errors.append("index.html: menu principal ausente")
        return
    titles = re.findall(r'<a[^>]*>([^<]+)</a>', nav_match.group(1))
    expected = ["Livros", "Arquivo", "Tópicos", "Contribuir", "Sobre"]
    if titles != expected:
        errors.append(f"index.html: ordem do menu inesperada: {titles}")


def check_internal_links(errors):
    for path in ROOT.rglob("*.html"):
        content = path.read_text(encoding="utf-8", errors="replace")
        for marker in FORBIDDEN:
            if marker in content:
                errors.append(f"{path.relative_to(ROOT)}: marcador proibido: {marker}")

        for raw_href in re.findall(r'href="([^"]+)"', content):
            if raw_href.startswith(("http://", "https://", "mailto:", "tel:")):
                continue
            parsed = urlsplit(raw_href)
            target = parsed.path
            if target.startswith("#"):
                if target == "#":
                    errors.append(f"{path.relative_to(ROOT)}: link vazio sem destino")
                continue
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

def check_search_index(errors):
    path = ROOT / "buscar" / "index.html"
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(
        r"window\.REALMAT_SEARCH_INDEX\s*=\s*(\[.*?\]);",
        content,
        flags=re.S,
    )
    if not match:
        errors.append("buscar/index.html: índice de busca não encontrado")
        return
    try:
        items = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        errors.append(f"buscar/index.html: índice de busca inválido: {exc}")
        return
    urls = {item.get("url") for item in items}
    for forbidden in ("/buscar/", "/404.html", "/atualizacoes/"):
        if forbidden in urls:
            errors.append(
                f"buscar/index.html: página estrutural indevidamente indexada: {forbidden}"
            )
    if "/livros/" not in urls:
        errors.append("buscar/index.html: páginas de conteúdo não foram indexadas")


def check_branding(errors):
    path = ROOT / "index.html"
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8", errors="replace")
    if not re.search(r"<li>©\s+[^<]+\s+REALMat</li>", content):
        errors.append("index.html: copyright ainda não usa a grafia REALMat")

def main() -> int:
    errors = []

    for relative_path, markers in EXPECTED_PAGES.items():
        path = ROOT / relative_path
        if not path.exists():
            errors.append(f"página gerada ausente: {relative_path}")
            continue

        content = path.read_text(encoding="utf-8", errors="replace")
        for marker in markers:
            if marker not in content:
                errors.append(f"{relative_path}: marcador ausente: {marker}")
        if "{{" in content or "{%" in content:
            errors.append(f"{relative_path}: expressão Liquid não processada")

    for relative_path in REQUIRED_ASSETS:
        if not (ROOT / relative_path).exists():
            errors.append(f"recurso gerado ausente: {relative_path}")

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
            errors.append("forallx: PDF não abre no visualizador do navegador")
        if not download_link:
            errors.append("forallx: download explícito do PDF ausente")

    check_navigation_order(errors)
    check_internal_links(errors)
    check_search_index(errors)
    check_branding(errors)

    if errors:
        print("Generated Massively site checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Generated Massively site checks passed: {len(EXPECTED_PAGES)} pages and "
        f"{len(REQUIRED_ASSETS)} assets."
    )
    return 0

if __name__ == "__main__":
    sys.exit(main())
