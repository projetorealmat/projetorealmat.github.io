#!/usr/bin/env python3
"""Regression checks for the versioned catalog contract."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "_data" / "books.json").read_text(encoding="utf-8"))
catalog_sync = (ROOT / ".github" / "workflows" / "catalog-sync.yml").read_text(encoding="utf-8")

assert catalog, "catalog must not be empty"
for book in catalog:
    assert isinstance(book.get("current_version"), str), f"{book.get('id')}: current_version missing"
    releases = book.get("releases")
    assert isinstance(releases, list) and releases, f"{book.get('id')}: releases history missing"
    versions = [release.get("version") for release in releases]
    assert book["current_version"] in versions, f"{book.get('id')}: current version not in history"
    assert len(versions) == len(set(versions)), f"{book.get('id')}: duplicate versions"

assert "REALMAT_AUTOMATION_TOKEN" in catalog_sync, (
    "catalog PR creation must support a trusted automation identity so PR checks run automatically"
)
