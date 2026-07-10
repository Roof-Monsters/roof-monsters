#!/usr/bin/env python3
"""Defer includes/main scripts; keep Font Awesome on reliable preload + stylesheet."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FA_RELIABLE = (
    '  <link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" as="style" />\n'
    '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />'
)
FA_SYNC = '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />'
FA_DEFERRED = (
    '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" '
    'media="print" onload="this.media=\'all\'" />\n'
    '  <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" /></noscript>'
)

SCRIPTS_SYNC = '  <script src="/includes.js"></script>\n  <script src="/assets/js/main.js"></script>'
SCRIPTS_DEFER = '  <script src="/includes.js" defer></script>\n  <script src="/assets/js/main.js" defer></script>'

changed = 0
for path in ROOT.rglob("*.html"):
    if "scripts" in path.parts:
        continue
    text = path.read_text(encoding="utf-8")
    orig = text
    if FA_DEFERRED in text:
        text = text.replace(FA_DEFERRED, FA_RELIABLE)
    elif FA_SYNC in text and FA_RELIABLE not in text:
        text = text.replace(FA_SYNC, FA_RELIABLE)
    if SCRIPTS_SYNC in text:
        text = text.replace(SCRIPTS_SYNC, SCRIPTS_DEFER)
    if 'id="site-header-include"' in text and "site-chrome-slot--header" not in text:
        text = text.replace(
            '<div id="site-header-include"></div>',
            '<div id="site-header-include" class="site-chrome-slot site-chrome-slot--header" aria-hidden="true"></div>',
        )
        text = text.replace(
            '  <div id="site-header-include"></div>',
            '  <div id="site-header-include" class="site-chrome-slot site-chrome-slot--header" aria-hidden="true"></div>',
        )
    if 'id="site-footer-include"' in text and "site-chrome-slot--footer" not in text:
        text = text.replace(
            '<div id="site-footer-include"></div>',
            '<div id="site-footer-include" class="site-chrome-slot site-chrome-slot--footer" aria-hidden="true"></div>',
        )
        text = text.replace(
            '  <div id="site-footer-include"></div>',
            '  <div id="site-footer-include" class="site-chrome-slot site-chrome-slot--footer" aria-hidden="true"></div>',
        )
    if text != orig:
        path.write_text(text, encoding="utf-8")
        changed += 1
        print(path.relative_to(ROOT))
print("updated", changed, "files")
