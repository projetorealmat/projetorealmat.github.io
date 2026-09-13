#!/usr/bin/env python3
"""Acceptance tests for the individual book-page action contract."""

from __future__ import annotations

import re

from generate_book_pages import render_book


def sample_book() -> dict:
    return {
        "id": "sample",
        "title": "Livro de teste",
        "short_title": "Livro",
        "subject": "análise",
        "current_version": "v1.2.3",
        "translation_stage": "reviewed",
        "releases": [
            {
                "version": "v1.2.3",
                "translation_stage": "reviewed",
                "repository": "projetorealmat/sample",
                "ref": "v1.2.3",
                "release_url": "https://github.com/projetorealmat/sample/releases/tag/v1.2.3",
                "release_date": "2026-09-12",
                "entrypoint": {
                    "id": "html",
                    "label": "Ler no navegador",
                    "url": "https://books.example.org/sample/",
                },
                "publications": [
                    {
                        "id": "html",
                        "label": "Ler no navegador",
                        "format": "html",
                        "url": "https://books.example.org/sample/",
                    },
                    {
                        "id": "pdf",
                        "label": "PDF",
                        "format": "pdf",
                        "url": "https://github.com/projetorealmat/sample/releases/download/v1.2.3/sample.pdf",
                    },
                    {
                        "id": "epub",
                        "label": "EPUB",
                        "format": "epub",
                        "url": "https://books.example.org/sample/book.epub",
                    },
                ],
            }
        ],
    }


def pdf_only_book() -> dict:
    book = sample_book()
    release = book["releases"][0]
    pdf = release["publications"][1]
    release["entrypoint"] = {
        "id": "pdf",
        "label": "PDF",
        "url": pdf["url"],
    }
    release["publications"] = [pdf]
    return book


def encoded_pdf_book() -> dict:
    book = pdf_only_book()
    release = book["releases"][0]
    pdf = release["publications"][0]
    pdf["url"] = (
        "https://github.com/projetorealmat/sample/releases/download/"
        "v1.2.3/sample%20book.pdf"
    )
    release["entrypoint"]["url"] = pdf["url"]
    return book


def main() -> None:
    rendered = render_book(1, sample_book())
    buttons = re.findall(r'<a\b[^>]*class="[^"]*\bbutton\b[^"]*"[^>]*>', rendered)
    assert len(buttons) == 3, f"expected exactly three action buttons, got {len(buttons)}"
    assert "Ler o livro" in rendered
    assert "Baixar PDF" in rendered
    assert "Repositório" in rendered
    assert "https://books.example.org/sample/" in rendered
    assert "https://github.com/projetorealmat/sample/releases/download/v1.2.3/sample.pdf" in rendered
    assert "https://github.com/projetorealmat/sample\"" in rendered
    assert "Tradução revisada" in rendered
    assert "EPUB" not in rendered, "secondary formats must remain outside the portal actions"

    pdf_rendered = render_book(1, pdf_only_book())
    pdf_actions = re.search(r'<ul class="actions">(.*?)</ul>', pdf_rendered, flags=re.S)
    assert pdf_actions is not None
    pdf_buttons = re.findall(
        r'<a\b[^>]*class="[^"]*\bbutton\b[^"]*"[^>]*>',
        pdf_actions.group(1),
    )
    assert len(pdf_buttons) == 3
    assert (
        '<a href="/assets/books/sample/v1.2.3/sample.pdf" '
        'class="button primary" target="_blank" rel="noopener noreferrer">'
        "Ler o livro"
    ) in pdf_actions.group(1)
    assert (
        '<a href="https://github.com/projetorealmat/sample" '
        'class="button" target="_blank" rel="noopener noreferrer">Repositório'
    ) in pdf_actions.group(1)
    assert (
        '<a href="https://github.com/projetorealmat/sample/releases/download/v1.2.3/sample.pdf" '
        'class="button" download="sample.pdf">Baixar PDF'
    ) in pdf_actions.group(1)
    reading_button = re.search(r'<a href="/assets/books/[^>]+>', pdf_actions.group(1))
    assert reading_button is not None
    assert "download=" not in reading_button.group(0)

    encoded_rendered = render_book(1, encoded_pdf_book())
    assert (
        '<a href="/assets/books/sample/v1.2.3/sample%20book.pdf" '
        'class="button primary" target="_blank" rel="noopener noreferrer">'
        "Ler o livro"
    ) in encoded_rendered
    assert 'download="sample book.pdf"' in encoded_rendered

    unsafe_book = pdf_only_book()
    unsafe_release = unsafe_book["releases"][0]
    unsafe_pdf = unsafe_release["publications"][0]
    unsafe_pdf["url"] = (
        "https://github.com/projetorealmat/sample/releases/download/"
        "v1.2.3/..%2Fevil.pdf"
    )
    unsafe_release["entrypoint"]["url"] = unsafe_pdf["url"]
    unsafe_rendered = render_book(1, unsafe_book)
    assert '/assets/books/sample/v1.2.3/sample.pdf"' in unsafe_rendered
    assert "/assets/books/sample/v1.2.3/.." not in unsafe_rendered


if __name__ == "__main__":
    main()
