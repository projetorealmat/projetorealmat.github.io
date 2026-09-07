#!/usr/bin/env python3
"""Generate one Jekyll book page per catalog entry."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "_data" / "books.json"
OUTPUT_DIR = ROOT / "generated" / "books"


def current_release(book: dict) -> dict:
    return next(
        release
        for release in book["releases"]
        if release["version"] == book["current_version"]
    )


def display_date(value: str | None) -> str:
    if not value:
        return "Data não informada"
    year, month, day = value.split("-")
    return f"{day}/{month}/{year}"


def release_label(release: dict, current_version: str) -> str:
    state = "Atual" if release["version"] == current_version else "Histórica"
    return f"{state} · {release['version']} · {release['status']}"


def render_book(index: int, book: dict) -> str:
    current = current_release(book)
    title = html.escape(book["title"])
    subject = html.escape(book["subject"])
    short_title = html.escape(book["short_title"])
    book_id = html.escape(book["id"])
    description = (
        f"{book['title']}: edição {current['version']} para leitura e download."
    )
    history = []
    for release in book["releases"]:
        version = html.escape(release["version"])
        release_url = html.escape(release["release_url"], quote=True)
        pdf_url = html.escape(release["pdf_url"], quote=True)
        history.append(
            "    <li>"
            f'<span class="date">{html.escape(release_label(release, book["current_version"]))}</span>'
            f' <a href="{release_url}" target="_blank" rel="noopener noreferrer">Release</a>'
            f' · <a href="{pdf_url}" target="_blank" rel="noopener noreferrer">PDF</a>'
            f' · {html.escape(display_date(release.get("release_date")))}'
            "</li>"
        )

    return f"""---
layout: single
title: {json.dumps(book['title'], ensure_ascii=False)}
kicker: "Livro"
description: {json.dumps(description, ensure_ascii=False)}
permalink: /livros/{book_id}/
---

<section class="realmat-book-detail" aria-labelledby="{book_id}-reading-title">
  <div class="realmat-book-detail__cover realmat-book-poster realmat-book-poster--large" role="img" aria-label="Capa tipográfica de {title}">
    <span class="realmat-book-poster__inner">
      <span class="realmat-book-poster__number">{index:02d}</span>
      <span class="realmat-book-poster__name">{short_title}</span>
      <span class="realmat-book-poster__subject">{subject}</span>
      <span class="realmat-book-poster__formula" aria-hidden="true">p → q</span>
      <span class="realmat-book-poster__footer">edição {html.escape(current['version'])}</span>
    </span>
  </div>

  <div class="realmat-book-detail__copy">
    <header class="major">
      <span class="date">Leitura da edição {html.escape(current['version'])} · {html.escape(current['status'])}</span>
      <h2 id="{book_id}-reading-title">Leia no navegador ou baixe o PDF.</h2>
    </header>
    <p>{title} é uma obra de {subject}. A edição {html.escape(current['version'])} está {html.escape(current['status'])}. O portal publica o PDF oficial associado à release declarada no catálogo.</p>
    <ul class="actions">
      <li><a href="{html.escape(current['pdf_path'])}" class="button primary" target="_blank" rel="noopener noreferrer">Ler no navegador <span aria-hidden="true">↗</span></a></li>
      <li><a href="{html.escape(current['pdf_path'])}" class="button" download="{short_title}.pdf">Baixar PDF <span aria-hidden="true">↓</span></a></li>
      <li><a href="{html.escape(current['release_url'])}" class="button" target="_blank" rel="noopener noreferrer">Release e fontes <span aria-hidden="true">↗</span></a></li>
    </ul>
    <p class="realmat-note">O arquivo abre em uma nova aba e pode ser baixado pelo próprio navegador.</p>
  </div>
</section>

<hr />

<section class="realmat-facts" aria-label="Informações da edição">
  <div>
    <span class="realmat-facts__number">01</span>
    <h3>Estado</h3>
    <p>{html.escape(current['status'])}, versão {html.escape(current['version'])}.</p>
  </div>
  <div>
    <span class="realmat-facts__number">02</span>
    <h3>Assunto</h3>
    <p>{subject}.</p>
  </div>
  <div>
    <span class="realmat-facts__number">03</span>
    <h3>Formato</h3>
    <p>PDF de acesso aberto para leitura no navegador e estudo offline.</p>
  </div>
</section>

<section class="realmat-book-history" aria-labelledby="{book_id}-history-title">
  <header class="major">
    <span class="date">Histórico editorial</span>
    <h2 id="{book_id}-history-title">Versões publicadas</h2>
  </header>
  <p>A versão atual é mantida em destaque; as anteriores permanecem disponíveis para consulta, citação e bifurcação.</p>
  <ul>
{chr(10).join(history)}
  </ul>
</section>

<section class="realmat-callout" aria-labelledby="{book_id}-contribute-title">
  <div>
    <span class="date">Participação</span>
    <h2 id="{book_id}-contribute-title">Encontrou uma correção ou quer colaborar?</h2>
  </div>
  <div>
    <p>As discussões, orientações e fontes estão no repositório da obra.</p>
    <a href="https://github.com/{html.escape(current['repository'])}/issues" class="button" target="_blank" rel="noopener noreferrer">Contribuir <span aria-hidden="true">↗</span></a>
  </div>
</section>
"""


def main() -> int:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for stale_page in OUTPUT_DIR.glob("*.md"):
        stale_page.unlink()

    for index, book in enumerate(catalog, start=1):
        page = OUTPUT_DIR / f"{book['id']}.md"
        page.write_text(render_book(index, book), encoding="utf-8")

    print(f"Generated {len(catalog)} book page(s) in {OUTPUT_DIR}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
