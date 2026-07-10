#!/usr/bin/env python3
"""Inject Microsoft Clarity (and future analytics) into all public HTML pages."""
from __future__ import annotations

from pathlib import Path

from analytics_snippet import inject_analytics

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {"partials", "scripts", "assets", "data", ".git"}


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in {"header.html", "footer.html"}:
            continue
        original = path.read_text(encoding="utf-8")
        updated = inject_analytics(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(path.relative_to(ROOT))
    print(f"Done. Updated {changed} files.")


if __name__ == "__main__":
    main()
