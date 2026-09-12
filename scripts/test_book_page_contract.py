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


if __name__ == "__main__":
    main()
