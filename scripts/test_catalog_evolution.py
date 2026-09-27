#!/usr/bin/env python3
"""Regression checks for the versioned generic publication catalog."""

from __future__ import annotations

import json
from pathlib import Path

from validate_catalog import validate_publication_manifest


ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "_data" / "books.json").read_text(encoding="utf-8"))
catalog_workflow = (ROOT / ".github" / "workflows" / "catalog-sync.yml").read_text(encoding="utf-8")

assert catalog, "catalog must not be empty"
assert "REALMAT_AUTOMATION_TOKEN" not in catalog_workflow
assert "PORTAL_DISPATCH_TOKEN" not in catalog_workflow
assert "projetorealmat/.github/.github/workflows/portal-catalog-sync.yml@v3" in catalog_workflow
assert "secrets: inherit" in catalog_workflow
assert (ROOT / "_data" / "translation_stages.yml").exists()

validate_publication_manifest(
    {
        "entrypoint": {
            "id": "html",
            "label": "Ler no navegador",
            "url": "https://books.example.org/book/",
        },
        "publications": [
            {
                "id": "html",
                "label": "Ler no navegador",
                "url": "https://books.example.org/book/",
            },
            {
                "id": "pdf",
                "label": "PDF",
                "format": "pdf",
                "url": "https://github.com/projetorealmat/example/releases/download/v1.0.0/example.pdf",
            },
        ],
    },
    0,
)

for book in catalog:
    assert isinstance(book.get("current_version"), str), f"{book.get('id')}: current_version missing"
    assert isinstance(book.get("repository"), str), f"{book.get('id')}: repository missing"
    assert book.get("translation_stage") in {"unreviewed", "reviewed", "adapted"}
    for field in ("source_url", "source_title", "source_authors", "source_license", "source_license_url"):
        assert isinstance(book.get(field), str) and book[field].strip(), f"{book['id']}: {field} missing"
    assert book["source_url"].startswith(("http://", "https://"))
    assert book["source_license_url"].startswith(("http://", "https://"))
    releases = book.get("releases")
    assert isinstance(releases, list) and releases, f"{book.get('id')}: releases history missing"
    versions = [release.get("version") for release in releases]
    assert book["current_version"] in versions, f"{book.get('id')}: current version not in history"
    assert len(versions) == len(set(versions)), f"{book.get('id')}: duplicate versions"

    for release in releases:
        assert release["repository"] == book["repository"]
        assert release["ref"] == release["version"]
        assert release["translation_stage"] in {"unreviewed", "reviewed", "adapted"}
        assert isinstance(release["entrypoint"], dict)
        publications = release["publications"]
        assert isinstance(publications, list) and publications
        assert sum(publication["id"] == "pdf" for publication in publications) == 1
        pdf = next(publication for publication in publications if publication["id"] == "pdf")
        assert pdf["format"] == "pdf"
        assert pdf["url"].startswith(
            f"https://github.com/{release['repository']}/releases/download/{release['version']}/"
        )

forallx = next(book for book in catalog if book["id"] == "forallx")
assert forallx["current_version"] == "v0.1.3"
release_013 = next(release for release in forallx["releases"] if release["version"] == "v0.1.3")
assert release_013["translation_stage"] == "unreviewed"
assert release_013["entrypoint"]["id"] == "pdf"
assert release_013["publications"][0]["url"].endswith("/v0.1.3/forallx.pdf")

assert forallx["source_url"] == "https://github.com/OpenLogicProject/forallx"
assert "CC BY 4.0" in forallx["source_license"]
assert next(book for book in catalog if book["id"] == "aata")["source_license_url"].startswith(
    "https://github.com/twjudson/aata/blob/"
)

calgary = next(book for book in catalog if book["id"] == "forallx-yyc")
assert calgary["title"] == "forall x: Calgary — Uma introdução à lógica formal"
assert calgary["subject"] == "lógica formal"

abstract_algebra = next(book for book in catalog if book["id"] == "aata")
assert abstract_algebra["subject"] == "álgebra abstrata"
real_analysis = next(book for book in catalog if book["id"] == "ra-volume-i")
assert real_analysis["subject"] == "análise real"
assert all(book["subject"] != "Real analysis" for book in catalog)
