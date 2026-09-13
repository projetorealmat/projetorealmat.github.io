#!/usr/bin/env python3
"""Download the current canonical PDF publications for browser reading.

The PDF remains published canonically as a GitHub Release asset. The portal
also stages that already-built PDF under ``assets/books`` so that the reading
button can open it inline; GitHub Release download URLs are served as
attachments by GitHub.
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.request import Request, urlopen

from generate_book_pages import current_release, pdf_asset_file_path, publication


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "_data" / "books.json"


def main() -> int:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    asset_root = ROOT / "assets" / "books"
    expected_asset_root = ROOT.resolve() / "assets" / "books"
    if asset_root.resolve() != expected_asset_root:
        raise SystemExit("o diretório de assets para PDFs não pode ser um link simbólico")

    for book in catalog:
        release = current_release(book)
        pdf = publication(release, "pdf")
        target = pdf_asset_file_path(ROOT, book, release, pdf)
        try:
            target.resolve().relative_to(expected_asset_root)
        except ValueError as error:
            raise SystemExit(
                f"{book['id']} {release['version']}: caminho de PDF fora de assets/books"
            ) from error
        if target.is_symlink():
            raise SystemExit(
                f"{book['id']} {release['version']}: destino do PDF é um link simbólico"
            )
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name(f".{target.name}.part")
        request = Request(
            pdf["url"],
            headers={"User-Agent": "REALMat-portal-build/2.0"},
        )
        try:
            with urlopen(request, timeout=60) as response, temporary.open("wb") as output:
                first_bytes = response.read(5)
                if first_bytes != b"%PDF-":
                    raise SystemExit(
                        f"{book['id']} {release['version']}: o asset publicado não é PDF"
                    )
                output.write(first_bytes)
                while chunk := response.read(1024 * 1024):
                    output.write(chunk)
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)
        print(f"Staged {book['id']} {release['version']}: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
