#!/usr/bin/env python3
"""Download and verify the current PDF for every catalog entry."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "_data" / "books.json"
USER_AGENT = "REALMat-portal-build/1.0"


def current_release(book: dict) -> dict:
    return next(
        release
        for release in book["releases"]
        if release["version"] == book["current_version"]
    )


def download_and_hash(url: str, target: Path) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    digest = hashlib.sha256()
    with urlopen(request, timeout=60) as response, target.open("wb") as output:
        while chunk := response.read(1024 * 1024):
            output.write(chunk)
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    for book in catalog:
        release = current_release(book)
        target = ROOT / release["pdf_path"].lstrip("/")
        target.parent.mkdir(parents=True, exist_ok=True)
        digest = download_and_hash(release["pdf_url"], target)
        if digest != release["sha256"]:
            raise SystemExit(
                f"{book['id']} {release['version']}: SHA-256 divergente: "
                f"esperado {release['sha256']}, obtido {digest}"
            )
        source_file = target.with_name(f"{book['id']}-source.txt")
        source_file.write_text(
            f"Release oficial: {release['release_url']}\n"
            f"Versão: {release['version']}\n",
            encoding="utf-8",
        )
        print(f"Verified {book['id']} {release['version']}: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
