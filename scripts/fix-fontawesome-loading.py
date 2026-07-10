#!/usr/bin/env python3
"""Ensure Font Awesome loads on every page that injects the shared header."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FA_DEFERRED = (
    '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" '
    'media="print" onload="this.media=\'all\'" />\n'
    '  <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" /></noscript>'
)
FA_SYNC_OLD = (
    '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />'
)
FA_RELIABLE = (
    '  <link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" as="style" />\n'
    '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />'
)
STYLE_MARKER = '  <link rel="stylesheet" href="assets/css/style.css" />'


def main() -> None:
    upgraded = 0
    added = 0
    for path in sorted(ROOT.rglob("*.html")):
        if "scripts" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if "site-header-include" not in text:
            continue
        orig = text
        if FA_DEFERRED in text:
            text = text.replace(FA_DEFERRED, FA_RELIABLE)
        elif FA_SYNC_OLD in text and FA_RELIABLE not in text:
            text = text.replace(FA_SYNC_OLD, FA_RELIABLE)
        elif "font-awesome" not in text and STYLE_MARKER in text:
            text = text.replace(STYLE_MARKER, f"{FA_RELIABLE}\n{STYLE_MARKER}")
            added += 1
        if text != orig:
            path.write_text(text, encoding="utf-8")
            upgraded += 1
            print(path.relative_to(ROOT))
    print(f"updated {upgraded} files ({added} missing FA added)")


if __name__ == "__main__":
    main()
