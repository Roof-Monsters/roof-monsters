#!/usr/bin/env python3
"""Drop unused Inter font from Google Fonts URLs sitewide (saves requests)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = "&family=Inter:wght@400;500;600;700"
changed = 0
for path in ROOT.rglob("*.html"):
    if "scripts" in path.parts:
        continue
    text = path.read_text(encoding="utf-8")
    if OLD not in text:
        continue
    path.write_text(text.replace(OLD, ""), encoding="utf-8")
    changed += 1
print("updated", changed)
