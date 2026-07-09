#!/usr/bin/env python3
"""Inject favicon / PWA icon tags into all index.html pages."""

from __future__ import annotations

import re
from pathlib import Path

from icon_snippet import ICON_MARKER_END, ICON_MARKER_START, icon_head_html

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"partials", "scripts", "assets", "data", "node_modules", ".git"}
SNIPPET = icon_head_html()


def patch_head(text: str) -> str:
    if ICON_MARKER_START in text:
        return re.sub(
            rf"{re.escape(ICON_MARKER_START)}.*?{re.escape(ICON_MARKER_END)}",
            SNIPPET,
            text,
            count=1,
            flags=re.S,
        )
    anchor = '<meta name="viewport" content="width=device-width, initial-scale=1.0" />'
    if anchor in text:
        return text.replace(anchor, f"{anchor}\n{SNIPPET}", 1)
    return text


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("index.html")):
        if path.parts[0] in SKIP or any(p in SKIP for p in path.parts):
            continue
        original = path.read_text(encoding="utf-8")
        updated = patch_head(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print(f"Patched {path.relative_to(ROOT)}")
            changed += 1
    print(f"Updated {changed} page(s)")


if __name__ == "__main__":
    main()
