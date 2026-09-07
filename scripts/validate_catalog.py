#!/usr/bin/env python3
"""Validate immutable book releases used by the REALMat portal."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

BOOK_FIELDS = ("id", "title", "short_title", "subject", "current_version", "releases")
RELEASE_FIELDS = (
    "version",
    "status",
    "repository",
    "ref",
    "release_url",
    "pdf_url",
    "pdf_path",
    "sha256",
)
ALLOWED_STATUSES = {
    "em revisão",
    "tradução aprovada",
    "versão revisada",
    "nova versão",
}
VERSION_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY_RE = re.compile(r"^[^/\s]+/[^/\s]+$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def fail(message: str) -> None:
    raise ValueError(message)


def version_key(version: str) -> tuple[int, int, int]:
    match = VERSION_RE.fullmatch(version)
    if match is None:
        fail(f"versão inválida: {version!r}")
    return tuple(int(part) for part in match.groups())


def expected_status(version: str) -> str:
    major, minor, patch = version_key(version)
    if major == 0:
        return "em revisão"
    if (major, minor, patch) == (1, 0, 0):
        return "tradução aprovada"
    if major == 1:
        return "versão revisada"
    return "nova versão"


def validate_urls(release: dict, index: int) -> None:
    repository = release["repository"]
    ref = release["ref"]
    parsed_urls = {}
    repository_prefix = f"/{repository}/releases/"

    for field in ("release_url", "pdf_url"):
        parsed = urlparse(release[field])
        if (
            parsed.scheme != "https"
            or parsed.netloc != "github.com"
            or parsed.query
            or parsed.fragment
            or not parsed.path.startswith(repository_prefix)
        ):
            fail(f"release {index}: {field} não corresponde ao repositório declarado")
        parsed_urls[field] = parsed

    if VERSION_RE.fullmatch(ref):
        release_path = f"/{repository}/releases/tag/{ref}"
        pdf_name = parsed_urls["pdf_url"].path.rsplit("/", 1)[-1]
        pdf_path = f"/{repository}/releases/download/{ref}/{pdf_name}"
        if parsed_urls["release_url"].path != release_path:
            fail(f"release {index}: release_url não corresponde à tag {ref}")
        if parsed_urls["pdf_url"].path != pdf_path or not pdf_name.endswith(".pdf"):
            fail(f"release {index}: pdf_url não corresponde à tag {ref}")


def validate_release(release: object, index: int, paths: set[str]) -> None:
    if not isinstance(release, dict):
        fail(f"release {index} não é um objeto JSON")

    missing = [field for field in RELEASE_FIELDS if not release.get(field)]
    if missing:
        fail(f"release {index}: campos ausentes: {', '.join(missing)}")

    version = release["version"]
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        fail(f"release {index}: versão inválida: {version!r}")

    status = release["status"]
    if status not in ALLOWED_STATUSES:
        fail(f"release {index}: status editorial inválido: {status!r}")
    if status != expected_status(version):
        fail(
            f"release {index}: status {status!r} incompatível com {version}; "
            f"esperado {expected_status(version)!r}"
        )

    repository = release["repository"]
    if not isinstance(repository, str) or not REPOSITORY_RE.fullmatch(repository):
        fail(f"release {index}: repositório inválido: {repository!r}")

    ref = release["ref"]
    if ref in {"main", "master", "HEAD", "develop", "dev"}:
        fail(f"release {index}: ref não é imutável: {ref!r}")
    if not isinstance(ref, str) or not (
        VERSION_RE.fullmatch(ref) or COMMIT_RE.fullmatch(ref)
    ):
        fail(f"release {index}: ref deve ser uma tag semver ou SHA completo: {ref!r}")

    validate_urls(release, index)

    pdf_path = release["pdf_path"]
    if (
        not isinstance(pdf_path, str)
        or not pdf_path.startswith("/assets/books/")
        or not pdf_path.endswith(".pdf")
    ):
        fail(f"release {index}: pdf_path inválido: {pdf_path!r}")
    if pdf_path in paths:
        fail(f"release {index}: pdf_path duplicado: {pdf_path}")
    paths.add(pdf_path)

    digest = release["sha256"]
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        fail(f"release {index}: sha256 inválido")

    release_date = release.get("release_date")
    if release_date and (
        not isinstance(release_date, str) or not DATE_RE.fullmatch(release_date)
    ):
        fail(f"release {index}: release_date deve usar YYYY-MM-DD")


def validate_book(book: object, index: int, paths: set[str]) -> None:
    if not isinstance(book, dict):
        fail(f"livro {index} não é um objeto JSON")

    missing = [field for field in BOOK_FIELDS if not book.get(field)]
    if missing:
        fail(f"livro {index}: campos ausentes: {', '.join(missing)}")

    identifier = book["id"]
    if not isinstance(identifier, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", identifier):
        fail(f"livro {index}: id inválido: {identifier!r}")

    for field in ("title", "short_title", "subject"):
        if not isinstance(book[field], str) or not book[field].strip():
            fail(f"livro {index}: {field} inválido")

    releases = book["releases"]
    if not isinstance(releases, list) or not releases:
        fail(f"livro {index}: releases deve ser uma lista não vazia")

    versions: set[str] = set()
    for release_index, release in enumerate(releases, start=1):
        validate_release(release, release_index, paths)
        version = release["version"]
        if version in versions:
            fail(f"livro {index}: versão duplicada: {version}")
        versions.add(version)

    current_version = book["current_version"]
    if not isinstance(current_version, str) or not VERSION_RE.fullmatch(current_version):
        fail(f"livro {index}: current_version inválida: {current_version!r}")
    if current_version not in versions:
        fail(f"livro {index}: current_version não está em releases: {current_version}")


def validate_catalog(path: Path) -> int:
    try:
        catalog = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"Catálogo não encontrado: {path}")
        return 1
    except json.JSONDecodeError as exc:
        print(f"JSON inválido em {path}: {exc}")
        return 1

    if not isinstance(catalog, list) or not catalog:
        print("O catálogo deve ser uma lista JSON não vazia.")
        return 1

    identifiers: set[str] = set()
    paths: set[str] = set()
    try:
        for index, book in enumerate(catalog, start=1):
            validate_book(book, index, paths)
            identifier = book["id"]
            if identifier in identifiers:
                fail(f"livro {index}: id duplicado: {identifier}")
            identifiers.add(identifier)
    except ValueError as exc:
        print(exc)
        return 1

    total_releases = sum(len(book["releases"]) for book in catalog)
    print(f"Catálogo válido: {len(catalog)} livro(s), {total_releases} release(s).")
    return 0


if __name__ == "__main__":
    sys.exit(validate_catalog(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_data/books.json")))
