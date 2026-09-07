#!/usr/bin/env python3
"""Validate the immutable book references used to build the REALMat portal."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


REQUIRED_FIELDS = (
    "id",
    "title",
    "short_title",
    "subject",
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
VERSION_RE = re.compile(r"^v\d+\.\d+\.\d+$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY_RE = re.compile(r"^[^/\s]+/[^/\s]+$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def fail(message: str) -> None:
    raise ValueError(message)


def validate_entry(entry: object, index: int, paths: set[str]) -> None:
    if not isinstance(entry, dict):
        fail(f"item {index} não é um objeto JSON")

    missing = [field for field in REQUIRED_FIELDS if not entry.get(field)]
    if missing:
        fail(f"item {index}: campos ausentes: {', '.join(missing)}")

    identifier = entry["id"]
    if not isinstance(identifier, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", identifier):
        fail(f"item {index}: id inválido: {identifier!r}")

    version = entry["version"]
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        fail(f"item {index}: versão inválida: {version!r}")

    status = entry["status"]
    if status not in ALLOWED_STATUSES:
        fail(f"item {index}: status editorial inválido: {status!r}")
    major, minor, patch = (int(part) for part in version[1:].split("."))
    if major == 0:
        expected_status = "em revisão"
    elif major == 1 and minor == 0 and patch == 0:
        expected_status = "tradução aprovada"
    elif major == 1:
        expected_status = "versão revisada"
    else:
        expected_status = "nova versão"
    if status != expected_status:
        fail(
            f"item {index}: status {status!r} incompatível com {version}; "
            f"esperado {expected_status!r}"
        )

    repository = entry["repository"]
    if not isinstance(repository, str) or not REPOSITORY_RE.fullmatch(repository):
        fail(f"item {index}: repositório inválido: {repository!r}")

    ref = entry["ref"]
    if ref in {"main", "master", "HEAD", "develop", "dev"}:
        fail(f"item {index}: a referência deve ser imutável, não {ref!r}")
    if not isinstance(ref, str) or not (VERSION_RE.fullmatch(ref) or COMMIT_RE.fullmatch(ref)):
        fail(f"item {index}: ref deve ser uma tag semver ou um SHA completo: {ref!r}")

    for field in ("release_url", "pdf_url"):
        parsed = urlparse(entry[field])
        if parsed.scheme != "https" or parsed.netloc != "github.com":
            fail(f"item {index}: {field} deve ser uma URL HTTPS do GitHub")

    pdf_path = entry["pdf_path"]
    if not isinstance(pdf_path, str) or not pdf_path.startswith("/assets/books/") or not pdf_path.endswith(".pdf"):
        fail(f"item {index}: pdf_path fora do diretório de livros: {pdf_path!r}")
    if pdf_path in paths:
        fail(f"item {index}: pdf_path duplicado: {pdf_path}")
    paths.add(pdf_path)

    digest = entry["sha256"]
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        fail(f"item {index}: sha256 inválido")


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
        for index, entry in enumerate(catalog, start=1):
            validate_entry(entry, index, paths)
            identifier = entry["id"]
            if identifier in identifiers:
                fail(f"id duplicado: {identifier}")
            identifiers.add(identifier)
    except ValueError as exc:
        print(f"Catálogo inválido: {exc}")
        return 1

    print(f"Catálogo válido: {len(catalog)} livro(s), referências imutáveis e checksums presentes.")
    return 0


if __name__ == "__main__":
    catalog_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_data/books.json")
    raise SystemExit(validate_catalog(catalog_path))
