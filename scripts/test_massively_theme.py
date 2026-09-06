#!/usr/bin/env python3
"""Source-level acceptance checks for the original Massively integration."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "_config.yml": (
        'title: "REALMAT"',
        'subtitle: "Recursos Educacionais Abertos na Licenciatura em Matemática"',
        'url: "https://projetorealmat.github.io"',
        "include:",
    ),
    "_data/navigation.yml": (
        '- title: "Livros"',
        '- title: "Contribuir"',
        '- title: "Arquivo"',
        '- title: "Tópicos"',
        '- title: "Sobre"',
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
        "assets/js/jquery.min.js",
        "assets/js/main.js",
    ),
    "_layouts/home.html": (
        "layout: default",
    ),
    "_layouts/single.html": (
        'class="post',
        'class="major"',
        "realmat-page-content",
    ),
    "_includes/massively-intro.html": (
        'id="intro"',
        "REALMat",
        "Recursos Educacionais Abertos na Licenciatura em Matemática",
        "scrolly",
    ),
    "_includes/massively-header.html": (
        'id="header"',
        "REALMat",
        "brand-real",
        "brand-l",
        "brand-mat",
        "assets/images/realmat-logo.png",
    ),
    "_includes/massively-nav.html": (
        'id="nav"',
        "site.data.navigation.main",
        "fa-search",
        "fa-github",
    ),
    "_includes/massively-footer.html": (
        'id="footer"',
        "Como contribuir",
        "Organização do projeto",
    ),
    "index.md": (
        'class="post featured',
        'class="posts',
        "REALMAT",
        "forallx",
        "/livros/",
        "/contribuir/",
    ),
    "_pages/livros.md": (
        "realmat-library",
        "forallx: Lógica",
        "assets/books/forallx.pdf",
    ),
    "_pages/forallx.md": (
        "realmat-book-detail",
        "Ler no navegador",
        'download="forallx.pdf"',
        "assets/books/forallx.pdf",
    ),
    "_pages/contribuir.md": (
        "realmat-contribution",
        "github.com/projetorealmat/forallx",
    ),
    "_pages/sobre.md": (
        "Recursos Educacionais Abertos na Licenciatura em Matemática",
        "O REALMat — Recursos Educacionais Abertos na Licenciatura em Matemática — é um projeto de extensão",
    ),
    "_pages/arquivo.md": (
        "permalink: /arquivo/",
        "realmat-updates",
        "forallx disponível para leitura",
    ),
    "_pages/topicos.md": (
        "permalink: /topicos/",
        "Lógica formal",
        "/livros/forallx/",
    ),
    "_pages/buscar.md": (
        "realmat-search",
        "REALMAT_SEARCH_INDEX",
    ),
    "assets/css/main.css": (
        "Massively by HTML5 UP",
        "#intro",
        "#wrapper",
        "#navPanel",
        "fontawesome-all.min.css",
    ),
    "assets/css/noscript.css": (
        "#intro",
        "#wrapper",
    ),
    "assets/css/realmat.css": (
        "--realmat-blue",
        "--realmat-gold",
        "--realmat-cyan",
        "realmat-bg",
        "realmat-logo",
        "brand-real",
        "realmat-book-poster",
        "@media",
    ),
    "assets/js/main.js": (
        "navPanel",
        "scrollex",
        "#intro",
    ),
    "assets/js/realmat-search.js": (
        "REALMAT_SEARCH_INDEX",
        "realmat-search",
        "URLSearchParams",
        ".every",
    ),
    "MASSIVELY_LICENSE.txt": (
        "Creative Commons Attribution 3.0",
    ),
}

FORBIDDEN = {
    "_config.yml": ("remote_theme:", "minimal_mistakes", "jekyll-include-cache"),
    "index.md": ("This is Massively", "Lorem ipsum", 'href="#"'),
    "_pages/livros.md": ('href="#"', "<iframe"),
    "_pages/forallx.md": ("<iframe", 'href="#"'),
    "_pages/contribuir.md": ('href="#"',),
    "_layouts/default.html": ("minimal-mistakes", "realmat-masthead", "realmat.js"),
    "assets/css/main.css": ("Minimal Mistakes",),
}

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
    "images/realmat-bg.png",
    "assets/images/realmat-logo.png",
)

def main() -> int:
    errors = []

    for relative, markers in REQUIRED.items():
        path = ROOT / relative
        if not path.exists():
            errors.append(f"arquivo ausente: {relative}")
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        for marker in markers:
            if marker not in content:
                errors.append(f"{relative}: marcador ausente: {marker}")
        for marker in FORBIDDEN.get(relative, ()):
            if marker in content:
                errors.append(f"{relative}: marcador proibido: {marker}")

    for relative in REQUIRED_ASSETS:
        if not (ROOT / relative).exists():
            errors.append(f"asset ausente: {relative}")

    for path in ROOT.rglob("*.md"):
        content = path.read_text(encoding="utf-8", errors="replace")
        if 'href="#"' in content or "<iframe" in content:
            errors.append(f"{path.relative_to(ROOT)}: placeholder ou leitor embutido")

    if (ROOT / "assets/css/main.scss").exists():
        errors.append("assets/css/main.scss: o CSS oficial deve ser servido como main.css")
    if (ROOT / "assets/js/realmat.js").exists():
        errors.append("assets/js/realmat.js: script antigo não deve permanecer")

    navigation = ROOT / "_data/navigation.yml"
    if navigation.exists():
        titles = [
            line.strip()
            for line in navigation.read_text(encoding="utf-8").splitlines()
            if line.strip().startswith("- title:")
        ]
        expected = [
            '- title: "Livros"',
            '- title: "Contribuir"',
            '- title: "Arquivo"',
            '- title: "Tópicos"',
            '- title: "Sobre"',
        ]
        if titles != expected:
            errors.append("_data/navigation.yml: menu principal inesperado")

    if errors:
        print("Massively source checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Massively source checks passed: {len(REQUIRED)} files.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
