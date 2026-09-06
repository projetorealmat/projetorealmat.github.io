#!/usr/bin/env python3
"""Source-level acceptance checks for the original Massively integration."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "_config.yml": (
        'title: "REALMat"',
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
        'rel="preload"',
        "images/realmat-bg.jpg",
        "REALMat</li>",
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
        '<h1>REALMat</h1>',
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
        'id="footer"',
        "Como contribuir",
        "Organização do projeto",
        "forallx: Lógica",
    ),
    "index.md": (
        'class="post featured',
        'class="posts',
        "REALMat",
        "forallx",
        "/livros/",
        "/contribuir/",
    ),
    "_pages/livros.md": (
        "realmat-library",
        "forallx: Lógica",
        "assets/books/forallx.pdf",
        "REALMat para leitura",
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
        "REALMat.",
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
        "search_index_count",
        "item.url == '/buscar/'",
        "item.url == '/404.html'",
    ),
    "_pages/atualizacoes.md": (
        "permalink: /atualizacoes/",
        'http-equiv="refresh"',
        "/arquivo/",
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
        "--realmat-orange",
        "realmat-bg",
        "realmat-logo",
        "brand-real",
        "realmat-wordmark__icon",
        "#wrapper.fade-in:before",
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
    "README.md": (
        "# REALMat",
        "Recursos Educacionais Abertos na Licenciatura em Matemática.",
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
    "images/realmat-bg.jpg",
    "assets/images/realmat-logo.jpg",
)

def check_intro_subtitle_color(errors):
    path = ROOT / "assets/css/realmat.css"
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8", errors="replace")
    matches = re.findall(
        r"#intro \.realmat-intro-subtitle\s*\{(.*?)\}",
        content,
        flags=re.S,
    )
    if not matches or "color: var(--realmat-orange);" not in matches[-1]:
        errors.append(
            "assets/css/realmat.css: subtítulo da intro não usa a cor laranja da marca"
        )


def _last_css_block(content, selector):
    pattern = r"(?m)^" + re.escape(selector) + r"\s*\{(.*?)\}"
    matches = re.findall(pattern, content, flags=re.S)
    return matches[-1] if matches else ""


def check_background_layers(errors):
    layout = ROOT / "_layouts/default.html"
    css = ROOT / "assets/css/realmat.css"
    layout_content = layout.read_text(encoding="utf-8", errors="replace") if layout.exists() else ""
    css_content = css.read_text(encoding="utf-8", errors="replace") if css.exists() else ""

    if 'rel="preload"' not in layout_content or "images/realmat-bg.jpg" not in layout_content:
        errors.append("_layouts/default.html: preload do fundo da home ausente")

    intro = _last_css_block(css_content, "#intro")
    wrapper = _last_css_block(css_content, "#wrapper")
    first_paint = _last_css_block(css_content, "#wrapper.fade-in:before")
    parallax = _last_css_block(css_content, "#wrapper > .bg")

    if not intro or "background: transparent;" not in intro or "realmat-bg.jpg" in intro:
        errors.append(
            "assets/css/realmat.css: #intro deve ser um plano transparente, sem duplicar a imagem do parallax"
        )

    if not wrapper or "background: var(--realmat-navy);" not in wrapper or "realmat-bg.jpg" in wrapper:
        errors.append(
            "assets/css/realmat.css: wrapper não deve manter uma segunda cópia fixa da imagem"
        )

    if (
        not first_paint
        or "background: var(--realmat-navy);" not in first_paint
        or "realmat-bg.jpg" in first_paint
    ):
        errors.append(
            "assets/css/realmat.css: primeiro paint deve ser somente o plano azul-marinho"
        )

    if not parallax or "realmat-bg.jpg" not in parallax:
        errors.append(
            "assets/css/realmat.css: camada .bg animada sem a imagem de fundo REALMat"
        )

    if not parallax or "100% auto" not in parallax or "top center" not in parallax:
        errors.append(
            "assets/css/realmat.css: camada .bg perdeu o dimensionamento/posicionamento do parallax do Massively"
        )

    if "auto 175%" not in css_content:
        errors.append(
            "assets/css/realmat.css: ajuste do parallax para orientação portrait ausente"
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
            '- title: "Arquivo"',
            '- title: "Tópicos"',
            '- title: "Contribuir"',
            '- title: "Sobre"',
        ]
        if titles != expected:
            errors.append("_data/navigation.yml: menu principal inesperado")

    check_intro_subtitle_color(errors)
    check_background_layers(errors)

    if errors:
        print("Massively source checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Massively source checks passed: {len(REQUIRED)} files.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
