#!/usr/bin/env python3
"""Split index.html main content into partials/home/*.html"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
index = (ROOT / "index.html").read_text(encoding="utf-8")
pattern = r'<div id="site-header-include"></div>\s*(.*?)\s*<div id="site-footer-include">'
m = re.search(pattern, index, re.S)
if not m:
    raise SystemExit("Could not find main content in index.html")

body = m.group(1)
parts = re.split(r"\n\s*<!-- =+ ([^=]+) =+ -->\n", body)
out_dir = ROOT / "partials" / "home"
out_dir.mkdir(parents=True, exist_ok=True)

chunks = []
if parts[0].strip():
    chunks.append(("intro", parts[0].strip()))

i = 1
while i < len(parts):
    title = parts[i].strip()
    content = parts[i + 1] if i + 1 < len(parts) else ""
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    chunks.append((title, content.strip()))
    i += 2

for title, content in chunks:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    (out_dir / f"{slug}.html").write_text(content + "\n", encoding="utf-8")
    print(f"Wrote {slug}.html ({title})")
