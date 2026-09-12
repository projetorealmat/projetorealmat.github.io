#!/usr/bin/env python3
"""Check that every current release exposes a canonical PDF publication.

The portal links directly to the immutable GitHub Release asset. It does not
download or compile book formats while building the site.
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse


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
        pdf = next(
            publication
            for publication in release["publications"]
            if publication["id"] == "pdf"
        )
        parsed = urlparse(pdf["url"])
        expected_prefix = (
            f"/{release['repository']}/releases/download/{release['version']}/"
        )
        if (
            parsed.scheme != "https"
            or parsed.netloc != "github.com"
            or not parsed.path.startswith(expected_prefix)
            or not parsed.path.endswith(".pdf")
            or parsed.query
            or parsed.fragment
        ):
            raise SystemExit(
                f"{book['id']} {release['version']}: URL do PDF canônico inválida"
            )
        print(f"Verified {book['id']} {release['version']}: {pdf['url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
