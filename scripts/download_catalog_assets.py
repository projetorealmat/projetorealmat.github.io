#!/usr/bin/env python3
"""Download the current PDF for every catalog entry for browser reading.

The PDF remains published canonically as a GitHub Release asset. The portal
also stages that already-built PDF under ``assets/books`` so that the reading
button can open it inline; GitHub Release download URLs are served as
attachments by GitHub.
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.request import Request, urlopen

from generate_book_pages import current_release, pdf_asset_path, publication


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "_data" / "books.json"


def current_release(book: dict) -> dict:
    return next(
        release
        for release in book["releases"]
        if release["version"] == book["current_version"]
    )


def main() -> int:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    for book in catalog:
        release = current_release(book)
        pdf = publication(release, "pdf")
        target = ROOT / pdf_asset_path(book, release, pdf).lstrip("/")
        target.parent.mkdir(parents=True, exist_ok=True)
        request = Request(
            pdf["url"],
            headers={"User-Agent": "REALMat-portal-build/2.0"},
        )
        with urlopen(request, timeout=60) as response, target.open("wb") as output:
            first_bytes = response.read(5)
            if first_bytes != b"%PDF-":
                raise SystemExit(
                    f"{book['id']} {release['version']}: o asset publicado não é PDF"
                )
            output.write(first_bytes)
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
        print(f"Staged {book['id']} {release['version']}: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
