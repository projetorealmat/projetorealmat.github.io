#!/usr/bin/env python3
"""Generate one Jekyll book page per catalog entry."""

from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit


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


def display_date(value: str | None) -> str:
    if not value:
        return "Data não informada"
    year, month, day = value.split("-")
    return f"{day}/{month}/{year}"


def release_label(release: dict, current_version: str) -> str:
    state = "Atual" if release["version"] == current_version else "Histórica"
    return f"{state} · {release['version']} · {stage_label(release)}"


def pdf_filename(url: str, fallback: str) -> str:
    name = unquote(urlsplit(url).path.rsplit("/", 1)[-1])
    return name if name.endswith(".pdf") else fallback


def render_book(index: int, book: dict) -> str:
    current = current_release(book)
    entrypoint = current["entrypoint"]
    pdf = publication(current, "pdf")
    title = html.escape(book["title"])
    subject = html.escape(book["subject"])
    short_title = html.escape(book["short_title"])
    book_id = html.escape(book["id"])
    stage = html.escape(stage_label(current))
    entrypoint_url = html.escape(entrypoint["url"], quote=True)
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
        source_note = (
            '<p class="realmat-note">Fonte, créditos e licença: '
            f'<a href="{source_url}" target="_blank" rel="noopener noreferrer">'
            "repositório de origem</a>.</p>"
        )
    history = []
    for release in book["releases"]:
        version = html.escape(release["version"])
        release_url = html.escape(release["release_url"], quote=True)
        release_pdf = publication(release, "pdf")
        release_pdf_url = html.escape(release_pdf["url"], quote=True)
        history.append(
            "    <li>"
            f'<span class="date">{html.escape(release_label(release, book["current_version"]))}</span>'
            f' <a href="{release_url}" target="_blank" rel="noopener noreferrer">Release</a>'
            f' · <a href="{release_pdf_url}" target="_blank" rel="noopener noreferrer">PDF</a>'
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
      <span class="date">Leitura da edição {html.escape(current['version'])} · {stage}</span>
      <h2 id="{book_id}-reading-title">Leia o livro ou baixe o PDF.</h2>
    </header>
    <p>{title} é uma obra de {subject}. A edição {html.escape(current['version'])} corresponde a uma {stage.lower()}. O portal mantém uma entrada principal de leitura, o PDF oficial para download e o repositório da edição.</p>
    <ul class="actions">
      <li><a href="{entrypoint_url}" class="button primary" target="_blank" rel="noopener noreferrer">Ler o livro <span aria-hidden="true">↗</span></a></li>
      <li><a href="{pdf_url}" class="button" download="{download_name}">Baixar PDF <span aria-hidden="true">↓</span></a></li>
      <li><a href="{repository_url}" class="button" target="_blank" rel="noopener noreferrer">Repositório <span aria-hidden="true">↗</span></a></li>
    </ul>
    <p class="realmat-note">A entrada principal pode ser uma versão web ou outro formato de leitura declarado pela edição. Os demais formatos são mantidos no README e no próprio formato de leitura.</p>
    {source_note}
  </div>
</section>

<hr />

<section class="realmat-facts" aria-label="Informações da edição">
  <div>
    <span class="realmat-facts__number">01</span>
    <h3>Nível da tradução</h3>
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
    <p>Entrada principal de leitura e PDF oficial para download.</p>
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
