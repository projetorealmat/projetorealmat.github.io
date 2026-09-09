#!/usr/bin/env python3
"""Regression checks for the versioned catalog contract."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "_data" / "books.json").read_text(encoding="utf-8"))
catalog_workflow = (ROOT / ".github" / "workflows" / "catalog-sync.yml").read_text(encoding="utf-8")

assert catalog, "catalog must not be empty"
assert "REALMAT_AUTOMATION_TOKEN" not in catalog_workflow
assert "PORTAL_DISPATCH_TOKEN" not in catalog_workflow
assert "projetorealmat/.github/.github/workflows/portal-catalog-sync.yml@v1" in catalog_workflow
assert "secrets: inherit" in catalog_workflow
for book in catalog:
    assert isinstance(book.get("current_version"), str), f"{book.get('id')}: current_version missing"
    if "source_url" in book:
        assert isinstance(book["source_url"], str) and book["source_url"].startswith(("http://", "https://"))
    if "source_license" in book:
        assert isinstance(book["source_license"], str) and book["source_license"].strip()
    releases = book.get("releases")
    assert isinstance(releases, list) and releases, f"{book.get('id')}: releases history missing"
    versions = [release.get("version") for release in releases]
    assert book["current_version"] in versions, f"{book.get('id')}: current version not in history"
    assert len(versions) == len(set(versions)), f"{book.get('id')}: duplicate versions"

forallx = next(book for book in catalog if book["id"] == "forallx")
assert forallx["current_version"] == "v0.1.3"
release_013 = next(release for release in forallx["releases"] if release["version"] == "v0.1.3")
assert release_013["sha256"] == "86a25d4f6bc36875be8a99c9b9fc607e5e27fe08914f56bde6dc3f287f44bb6a"
assert release_013["pdf_path"] == "/assets/books/forallx/v0.1.3/forallx.pdf"

assert forallx["source_url"] == "https://github.com/OpenLogicProject/forallx"
assert forallx["source_license"] == "CC BY 4.0"
