#!/usr/bin/env python3
"""Static smoke tests for the REALMAT editorial skin."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

CHECKS = {
    "index.md": (
        "realmat-hero",
        "realmat-featured",
        "repositório",
    ),
    "_includes/masthead.html": (
        "realmat-masthead",
        "data-menu-toggle",
        "realmat-menu-panel",
    ),
    "_includes/footer.html": (
        "realmat-footer",
        "Como contribuir",
    ),
    "_layouts/default.html": (
        "realmat-layout",
        "head.html",
        "scripts.html",
    ),
    "_layouts/home.html": (
        "realmat-home",
        "realmat-featured",
    ),
    "_layouts/single.html": (
        "realmat-page",
        "page__content",
    ),
    "assets/css/main.scss": (
        "--realmat-orange",
        ".realmat-hero",
        "@media (max-width: 760px)",
    ),
    "assets/js/realmat.js": (
        "data-menu-toggle",
        "aria-expanded",
        "is-open",
    ),
}


def main() -> int:
    errors = []

    for relative_path, markers in CHECKS.items():
        path = ROOT / relative_path
        if not path.exists():
            errors.append(f"arquivo ausente: {relative_path}")
            continue

        content = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in content:
                errors.append(f"{relative_path}: marcador ausente: {marker}")

    if errors:
        print("Editorial skin checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Editorial skin checks passed: {len(CHECKS)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
