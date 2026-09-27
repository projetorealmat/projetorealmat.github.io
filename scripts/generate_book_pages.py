#!/usr/bin/env python3
"""Generate one Jekyll book page per catalog entry."""

from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "_data" / "books.json"
OUTPUT_DIR = ROOT / "generated" / "books"

STAGE_LABELS = {
    "unreviewed": "Tradução não revisada",
    "reviewed": "Tradução revisada",
    "adapted": "Tradução revisada e adaptada",
}


def current_release(book: dict) -> dict:
    return next(
        release
        for release in book["releases"]
        if release["version"] == book["current_version"]
    )


def publication(release: dict, publication_id: str) -> dict:
    return next(
        item for item in release["publications"] if item["id"] == publication_id
    )


def stage_label(release: dict) -> str:
    return STAGE_LABELS[release["translation_stage"]]


def pdf_filename(url: str, fallback: str) -> str:
    name = unquote(urlsplit(url).path.rsplit("/", 1)[-1])
    if (
        not name.endswith(".pdf")
        or name in {"", ".", ".."}
        or "/" in name
        or "\\" in name
        or any(ord(character) < 32 or ord(character) == 127 for character in name)
    ):
        return fallback
    return name


def pdf_asset_path(book: dict, release: dict, pdf: dict) -> str:
    filename = pdf_filename(pdf["url"], f"{book['id']}.pdf")
    segments = (book["id"], release["version"], filename)
    return "/assets/books/" + "/".join(quote(segment, safe="") for segment in segments)


def pdf_asset_file_path(root: Path, book: dict, release: dict, pdf: dict) -> Path:
    filename = pdf_filename(pdf["url"], f"{book['id']}.pdf")
    return root / "assets" / "books" / book["id"] / release["version"] / filename


def render_book(index: int, book: dict) -> str:
    current = current_release(book)
    entrypoint = current["entrypoint"]
    pdf = publication(current, "pdf")
    title = html.escape(book["title"])
    subject = html.escape(book["subject"])
    short_title = html.escape(book["short_title"])
    book_id = html.escape(book["id"])
    stage = html.escape(stage_label(current))
    reading_url = entrypoint["url"]
    if entrypoint["id"] == "pdf":
        reading_url = pdf_asset_path(book, current, pdf)
    entrypoint_url = html.escape(reading_url, quote=True)
    pdf_url = html.escape(pdf["url"], quote=True)
    repository_url = html.escape(
        f"https://github.com/{current['repository']}",
        quote=True,
    )
    download_name = html.escape(
        pdf_filename(pdf["url"], f"{book['id']}.pdf"),
        quote=True,
    )
    description = (
        f"{book['title']}: edição {current['version']} — {stage_label(current)}."
    )
    source_note = ""
    if book.get("source_url"):
        source_url = html.escape(book["source_url"], quote=True)
        license_url = html.escape(book["source_license_url"], quote=True)
        source_title = html.escape(book["source_title"])
        source_authors = html.escape(book["source_authors"])
        source_license = html.escape(book["source_license"])
        source_note = (
            '<section class="realmat-source" aria-label="Origem e licença da obra">'
            '<p class="realmat-note"><strong>Obra de origem:</strong> '
            f'<em>{source_title}</em>, {source_authors}. '
            f'<a href="{source_url}" target="_blank" rel="noopener noreferrer">'
            "Consultar a fonte</a>.</p>"
            '<p class="realmat-note"><strong>Licença indicada na fonte:</strong> '
            f'{source_license}. '
            f'<a href="{license_url}" target="_blank" rel="noopener noreferrer">'
            "Ver a declaração original</a>.</p></section>"
        )

    previous_count = sum(
        release["version"] != book["current_version"]
        for release in book["releases"]
    )
    history_note = ""
    if previous_count:
        history_note = (
            f'<p class="realmat-note"><a href="/arquivo/#{book_id}">'
            "Consultar edições anteriores</a>.</p>"
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
    {{% assign poster_book = site.data.books | where: "id", "{book_id}" | first %}}
    {{% include book-poster-content.html book=poster_book index="{index:02d}" %}}
  </div>

  <div class="realmat-book-detail__copy">
    <header class="major">
      <span class="date">Leitura da edição {html.escape(current['version'])} · {stage}</span>
      <h2 id="{book_id}-reading-title">Leia o livro ou baixe o PDF.</h2>
    </header>
    <p>{title} é uma obra de {subject}. A edição {html.escape(current['version'])} corresponde a uma {stage.lower()}. Leia no formato indicado ou baixe o PDF oficial.</p>
    <ul class="actions">
      <li><a href="{entrypoint_url}" class="button primary" target="_blank" rel="noopener noreferrer">Ler o livro <span aria-hidden="true">↗</span></a></li>
      <li><a href="{pdf_url}" class="button" download="{download_name}">Baixar PDF <span aria-hidden="true">↓</span></a></li>
      <li><a href="{repository_url}" class="button" target="_blank" rel="noopener noreferrer">Repositório <span aria-hidden="true">↗</span></a></li>
    </ul>
    {source_note}
    {history_note}
  </div>
</section>

<hr />

<section class="realmat-facts" aria-label="Informações da edição">
  <div>
    <span class="realmat-facts__number">01</span>
    <h3>Situação da tradução</h3>
    <p>{stage}, versão {html.escape(current['version'])}.</p>
  </div>
  <div>
    <span class="realmat-facts__number">02</span>
    <h3>Assunto</h3>
    <p>{subject}.</p>
  </div>
  <div>
    <span class="realmat-facts__number">03</span>
    <h3>Publicação</h3>
    <p>Formato principal de leitura e PDF oficial.</p>
  </div>
</section>

<section class="realmat-callout" aria-labelledby="{book_id}-contribute-title">
  <div>
    <span class="date">Participação</span>
    <h2 id="{book_id}-contribute-title">Encontrou uma correção ou quer colaborar?</h2>
  </div>
  <div>
    <p>As discussões, orientações e fontes estão no repositório da obra. Use a página <a href="/contribuir/">Contribuir</a> para consultar o fluxo geral.</p>
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
