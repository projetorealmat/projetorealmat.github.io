#!/usr/bin/env python3
"""Smoke tests for the generated REALMat site."""

from pathlib import Path
import html
import json
import re
import sys
from urllib.parse import urlsplit


ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")
SOURCE_ROOT = ROOT.parent
CATALOG_PATH = SOURCE_ROOT / "_data" / "books.json"

STAGE_LABELS = {
    "unreviewed": "Tradução não revisada",
    "reviewed": "Tradução revisada",
    "adapted": "Tradução revisada e adaptada",
}

STATIC_PAGES = {
    "index.html": (
        'id="intro"',
        'id="header"',
        'id="nav"',
        'id="main"',
        'class="post featured',
        'class="posts',
        "Abrir a edição",
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
        "Catálogo de livros",
        "edição",
    ),
    "sobre/index.html": (
        'class="post realmat-page"',
        "Recursos Educacionais Abertos na Licenciatura em Matemática",
        "O REALMat — Recursos Educacionais Abertos na Licenciatura em Matemática — é um projeto de extensão",
    ),
    "contribuir/index.html": (
        'class="post realmat-page"',
        "realmat-contribution",
        "Discussões e correções",
        "Repositório da edição",
    ),
    "buscar/index.html": (
        'class="realmat-search"',
        "REALMAT_SEARCH_INDEX",
        'id="realmat-search-input"',
    ),
    "arquivo/index.html": (
        'class="post realmat-page"',
        "realmat-updates",
        "Histórico editorial",
    ),
    "topicos/index.html": (
        'class="post realmat-page"',
        "realmat-topics",
        "Tópicos",
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
)


def load_catalog():
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def _without_search_index_script(content):
    start = content.find("window.REALMAT_SEARCH_INDEX")
    if start < 0:
        return content
    end = content.find("</script>", start)
    if end < 0:
        return content[:start]
    return content[:start] + content[end:]


def check_navigation_order(errors):
    index = ROOT / "index.html"
    if not index.exists():
        return
    content = index.read_text(encoding="utf-8", errors="replace")
    nav_match = re.search(r'<ul class="links">(.*?)</ul>', content, flags=re.S)
    if not nav_match:
        errors.append("index.html: menu principal ausente")
        return
    titles = re.findall(r"<a[^>]*>([^<]+)</a>", nav_match.group(1))
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


def check_search_index(errors, catalog):
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
    for book in catalog:
        expected_url = f"/livros/{book['id']}/"
        if expected_url not in urls:
            errors.append(f"buscar/index.html: livro não indexado: {expected_url}")


def check_catalog_pages(errors, catalog):
    library = (ROOT / "livros" / "index.html").read_text(
        encoding="utf-8", errors="replace"
    )
    archive = (ROOT / "arquivo" / "index.html").read_text(
        encoding="utf-8", errors="replace"
    )
    topics = (ROOT / "topicos" / "index.html").read_text(
        encoding="utf-8", errors="replace"
    )

    for index, book in enumerate(catalog, start=1):
        current = next(
            release
            for release in book["releases"]
            if release["version"] == book["current_version"]
        )
        detail_path = ROOT / "livros" / book["id"] / "index.html"
        if not detail_path.exists():
            errors.append(f"página do livro ausente: {detail_path.relative_to(ROOT)}")
            continue

        detail = detail_path.read_text(encoding="utf-8", errors="replace")
        stage_label = STAGE_LABELS[current["translation_stage"]]
        entrypoint = current["entrypoint"]
        pdf = next(publication for publication in current["publications"] if publication["id"] == "pdf")
        repository_url = f"https://github.com/{current['repository']}"
        expected_markers = (
            book["title"],
            book["current_version"],
            stage_label,
            entrypoint["url"],
            pdf["url"],
            repository_url,
            current["release_url"],
            "Histórico editorial",
            "Versões publicadas",
            "Ler o livro",
            "Baixar PDF",
            "Repositório",
            'target="_blank"',
            f'download="{pdf["url"].rsplit("/", 1)[-1]}"',
        )
        for marker in expected_markers:
            if marker not in detail:
                errors.append(
                    f"{detail_path.relative_to(ROOT)}: marcador ausente: {marker}"
                )

        buttons = re.findall(
            r'<a\b[^>]*class="[^"]*\bbutton\b[^"]*"[^>]*>',
            detail,
        )
        if len(buttons) != 3:
            errors.append(
                f"{detail_path.relative_to(ROOT)}: esperado exatamente 3 botões, "
                f"encontrados {len(buttons)}"
            )

        if book["title"] not in library:
            errors.append(f"livros/index.html: livro ausente: {book['title']}")
        if book["title"] not in archive:
            errors.append(f"arquivo/index.html: livro ausente: {book['title']}")
        if book["subject"] not in topics:
            errors.append(f"topicos/index.html: assunto ausente: {book['subject']}")

        for release in book["releases"]:
            if release["version"] not in detail:
                errors.append(
                    f"{detail_path.relative_to(ROOT)}: versão ausente: {release['version']}"
                )
            if release["release_url"] not in detail:
                errors.append(
                    f"{detail_path.relative_to(ROOT)}: release ausente: {release['release_url']}"
                )


def check_branding(errors):
    index = ROOT / "index.html"
    if not index.exists():
        return
    content = index.read_text(encoding="utf-8", errors="replace")
    if not re.search(r"<li>©\s+[^<]+\s+REALMat</li>", content):
        errors.append("index.html: copyright ainda não usa a grafia REALMat")


def main() -> int:
    errors = []
    catalog = load_catalog()

    for relative_path, markers in STATIC_PAGES.items():
        path = ROOT / relative_path
        if not path.exists():
            errors.append(f"página gerada ausente: {relative_path}")
            continue

        content = path.read_text(encoding="utf-8", errors="replace")
        for marker in markers:
            if marker not in content:
                errors.append(f"{relative_path}: marcador ausente: {marker}")
        liquid_check_content = (
            _without_search_index_script(content)
            if relative_path == "buscar/index.html"
            else content
        )
        if "{{" in liquid_check_content or "{%" in liquid_check_content:
            errors.append(f"{relative_path}: expressão Liquid não processada")

    for relative_path in REQUIRED_ASSETS:
        if not (ROOT / relative_path).exists():
            errors.append(f"recurso gerado ausente: {relative_path}")

    check_catalog_pages(errors, catalog)
    check_navigation_order(errors)
    check_internal_links(errors)
    check_search_index(errors, catalog)
    check_branding(errors)

    if errors:
        print("Generated REALMat site checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Generated REALMat site checks passed: {len(STATIC_PAGES)} static pages, "
        f"{len(catalog)} book page(s), and {len(REQUIRED_ASSETS)} assets."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
