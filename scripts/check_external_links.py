#!/usr/bin/env python3
"""Check external links used by the REALMat portal."""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    ROOT / "README.md",
    ROOT / "index.md",
    ROOT / "_data" / "books.json",
    *sorted((ROOT / "_pages").glob("*.md")),
)
URL_RE = re.compile(r"https?://[^\s)<>\"']+")
TRAILING = ".,;:!?]}>'"
USER_AGENT = "REALMat-portal-link-check/1.0"


def urls_from_files() -> list[str]:
    found: set[str] = set()
    for path in FILES:
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        for raw in URL_RE.findall(content):
            found.add(raw.rstrip(TRAILING))
    return sorted(found)


def request_status(url: str) -> int:
    headers = {"User-Agent": USER_AGENT}
    try:
        request = Request(url, headers=headers, method="HEAD")
        with urlopen(request, timeout=25) as response:
            return response.status
    except HTTPError as error:
        if error.code not in {403, 405, 501}:
            return error.code
    except (URLError, TimeoutError):
        pass

    request = Request(url, headers=headers, method="GET")
    with urlopen(request, timeout=25) as response:
        response.read(1024)
        return response.status


def main() -> int:
    failures: list[tuple[str, str]] = []
    urls = urls_from_files()
    print(f"Checking {len(urls)} external links...")

    for url in urls:
        try:
            status = request_status(url)
            if not 200 <= status < 400:
                failures.append((url, f"HTTP {status}"))
                print(f"FAIL {status}: {url}")
            else:
                print(f"OK {status}: {url}")
        except Exception as error:  # noqa: BLE001 - report the concrete URL failure
            failures.append((url, str(error)))
            print(f"FAIL {url}: {error}")
        time.sleep(0.15)

    if failures:
        print("\nExternal link checks failed:")
        for url, reason in failures:
            print(f"- {url}: {reason}")
        return 1

    print("All external links are reachable.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
