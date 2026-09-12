#!/usr/bin/env python3
"""Validate the generic, versioned publication catalog used by the REALMat portal."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

BOOK_FIELDS = (
    "id",
    "title",
    "short_title",
    "subject",
    "repository",
    "translation_stage",
    "current_version",
    "releases",
)
RELEASE_FIELDS = (
    "version",
    "translation_stage",
    "repository",
    "ref",
    "release_url",
    "release_date",
    "entrypoint",
    "publications",
)
STAGES = {
    "unreviewed": "Tradução não revisada",
    "reviewed": "Tradução revisada",
    "adapted": "Tradução revisada e adaptada",
}
VERSION_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY_RE = re.compile(r"^[^/\s]+/[^/\s]+$")
PUBLICATION_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
FORMAT_RE = re.compile(r"^[a-z0-9][a-z0-9+.-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SOURCE_FIELDS = ("source_url", "source_license")


def fail(message: str) -> None:
    raise ValueError(message)


def version_key(version: str) -> tuple[int, int, int]:
    match = VERSION_RE.fullmatch(version)
    if match is None:
        fail(f"versão inválida: {version!r}")
    return tuple(int(part) for part in match.groups())


def expected_stage(version: str) -> str:
    major, _, _ = version_key(version)
    if major == 0:
        return "unreviewed"
    if major == 1:
        return "reviewed"
    return "adapted"


def validate_http_url(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{field} deve ser uma URL não vazia")
    parsed = urlparse(value)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.netloc
        or any(character.isspace() for character in value)
    ):
        fail(f"{field} deve ser uma URL HTTP(S)")
    return value


def validate_publication_manifest(release: dict, index: int) -> None:
    entrypoint = release["entrypoint"]
    if not isinstance(entrypoint, dict):
        fail(f"release {index}: entrypoint deve ser um objeto")
    for field in ("id", "label", "url"):
        if not isinstance(entrypoint.get(field), str) or not entrypoint[field].strip():
            fail(f"release {index}: entrypoint.{field} inválido")
    if not PUBLICATION_ID_RE.fullmatch(entrypoint["id"]):
        fail(f"release {index}: entrypoint.id inválido")
    validate_http_url(entrypoint["url"], f"release {index}: entrypoint.url")

    publications = release["publications"]
    if not isinstance(publications, list) or not publications:
        fail(f"release {index}: publications deve ser uma lista não vazia")

    seen: set[str] = set()
    by_id: dict[str, dict] = {}
    for publication_index, publication in enumerate(publications, start=1):
        field = f"release {index}: publication {publication_index}"
        if not isinstance(publication, dict):
            fail(f"{field} não é um objeto")
        publication_id = publication.get("id")
        if not isinstance(publication_id, str) or not PUBLICATION_ID_RE.fullmatch(publication_id):
            fail(f"{field}: id inválido")
        if publication_id in seen:
            fail(f"{field}: id duplicado: {publication_id}")
        seen.add(publication_id)
        if not isinstance(publication.get("label"), str) or not publication["label"].strip():
            fail(f"{field}: label inválido")
        format_name = publication.get("format")
        if publication_id == "pdf":
            if not isinstance(format_name, str) or not FORMAT_RE.fullmatch(format_name):
                fail(f"{field}: a publicação PDF deve declarar format=pdf")
            if format_name != "pdf":
                fail(f"{field}: id=pdf deve ter format=pdf")
        elif format_name is not None and (
            not isinstance(format_name, str) or not FORMAT_RE.fullmatch(format_name)
        ):
            fail(f"{field}: format inválido")
        validate_http_url(publication.get("url"), f"{field}: url")
        by_id[publication_id] = publication

    if set(by_id) != seen or "pdf" not in by_id:
        fail(f"release {index}: falta a publicação PDF canônica")
    if len([key for key in by_id if key == "pdf"]) != 1:
        fail(f"release {index}: deve haver exatamente uma publicação PDF")
    selected = by_id.get(entrypoint["id"])
    if selected is None:
        fail(f"release {index}: entrypoint.id não está em publications")
    if selected["label"] != entrypoint["label"] or selected["url"] != entrypoint["url"]:
        fail(f"release {index}: entrypoint não coincide com a publicação selecionada")


def validate_release(release: object, index: int) -> None:
    if not isinstance(release, dict):
        fail(f"release {index} não é um objeto JSON")

    missing = [field for field in RELEASE_FIELDS if field not in release]
    if missing:
        fail(f"release {index}: campos ausentes: {', '.join(missing)}")

    version = release["version"]
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        fail(f"release {index}: versão inválida: {version!r}")
    stage = release["translation_stage"]
    if stage not in STAGES:
        fail(f"release {index}: translation_stage inválido: {stage!r}")
    if stage != expected_stage(version):
        fail(
            f"release {index}: translation_stage {stage!r} incompatível com {version}; "
            f"esperado {expected_stage(version)!r}"
        )

    repository = release["repository"]
    if not isinstance(repository, str) or not REPOSITORY_RE.fullmatch(repository):
        fail(f"release {index}: repositório inválido: {repository!r}")
    if not repository.startswith("projetorealmat/"):
        fail(f"release {index}: repositório fora da organização REALMat: {repository!r}")

    ref = release["ref"]
    if not isinstance(ref, str) or ref in {"main", "master", "HEAD", "develop", "dev"}:
        fail(f"release {index}: ref não é imutável: {ref!r}")
    if not (VERSION_RE.fullmatch(ref) or COMMIT_RE.fullmatch(ref)):
        fail(f"release {index}: ref deve ser uma tag semver ou SHA completo: {ref!r}")
    if VERSION_RE.fullmatch(ref) and ref != version:
        fail(f"release {index}: ref deve coincidir com version quando for uma tag")

    release_url = validate_http_url(release["release_url"], f"release {index}: release_url")
    parsed_release = urlparse(release_url)
    expected_release_path = f"/{repository}/releases/tag/{version}"
    if (
        parsed_release.scheme != "https"
        or parsed_release.netloc != "github.com"
        or parsed_release.query
        or parsed_release.fragment
        or parsed_release.path != expected_release_path
    ):
        fail(f"release {index}: release_url não corresponde à tag {version}")

    release_date = release["release_date"]
    if not isinstance(release_date, str) or not DATE_RE.fullmatch(release_date):
        fail(f"release {index}: release_date deve usar YYYY-MM-DD")
    try:
        date.fromisoformat(release_date)
    except ValueError as error:
        fail(f"release {index}: release_date inválida")
        raise AssertionError from error

    validate_publication_manifest(release, index)
    pdf = next(publication for publication in release["publications"] if publication["id"] == "pdf")
    parsed_pdf = urlparse(pdf["url"])
    pdf_prefix = f"/{repository}/releases/download/{version}/"
    pdf_name = parsed_pdf.path[len(pdf_prefix):] if parsed_pdf.path.startswith(pdf_prefix) else ""
    if (
        parsed_pdf.scheme != "https"
        or parsed_pdf.netloc != "github.com"
        or parsed_pdf.query
        or parsed_pdf.fragment
        or not pdf_name
        or "/" in pdf_name
        or not pdf_name.endswith(".pdf")
    ):
        fail(f"release {index}: a publicação PDF não corresponde à tag {version}")


def validate_book(book: object, index: int) -> None:
    if not isinstance(book, dict):
        fail(f"livro {index} não é um objeto JSON")

    missing = [field for field in BOOK_FIELDS if field not in book]
    if missing:
        fail(f"livro {index}: campos ausentes: {', '.join(missing)}")

    identifier = book["id"]
    if not isinstance(identifier, str) or not PUBLICATION_ID_RE.fullmatch(identifier):
        fail(f"livro {index}: id inválido: {identifier!r}")

    for field in ("title", "short_title", "subject"):
        if not isinstance(book[field], str) or not book[field].strip():
            fail(f"livro {index}: {field} inválido")

    repository = book["repository"]
    if not isinstance(repository, str) or not REPOSITORY_RE.fullmatch(repository):
        fail(f"livro {index}: repository inválido")
    if not repository.startswith("projetorealmat/"):
        fail(f"livro {index}: repository fora da organização REALMat")

    stage = book["translation_stage"]
    if stage not in STAGES:
        fail(f"livro {index}: translation_stage inválido: {stage!r}")

    for field in SOURCE_FIELDS:
        value = book.get(field)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            fail(f"livro {index}: {field} inválido")
    source_url = book.get("source_url")
    if source_url is not None:
        validate_http_url(source_url, f"livro {index}: source_url")

    releases = book["releases"]
    if not isinstance(releases, list) or not releases:
        fail(f"livro {index}: releases deve ser uma lista não vazia")

    versions: set[str] = set()
    previous_key: tuple[int, int, int] | None = None
    for release_index, release in enumerate(releases, start=1):
        validate_release(release, release_index)
        if release["repository"] != repository:
            fail(f"livro {index}: repository da release não coincide com o livro")
        if release["translation_stage"] != expected_stage(release["version"]):
            fail(f"livro {index}: nível da release incompatível com a versão")
        version = release["version"]
        if version in versions:
            fail(f"livro {index}: versão duplicada: {version}")
        versions.add(version)
        current_key = version_key(version)
        if previous_key is not None and current_key > previous_key:
            fail(f"livro {index}: releases devem estar em ordem decrescente")
        previous_key = current_key

    current_version = book["current_version"]
    if not isinstance(current_version, str) or not VERSION_RE.fullmatch(current_version):
        fail(f"livro {index}: current_version inválida: {current_version!r}")
    if current_version not in versions:
        fail(f"livro {index}: current_version não está em releases: {current_version}")
    current = next(release for release in releases if release["version"] == current_version)
    if book["translation_stage"] != current["translation_stage"]:
        fail(f"livro {index}: translation_stage não coincide com a release atual")


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
    try:
        for index, book in enumerate(catalog, start=1):
            validate_book(book, index)
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
