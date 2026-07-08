#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"partials", "scripts", "assets", "data"}
pages = [
    p
    for p in ROOT.rglob("index.html")
    if p.relative_to(ROOT).parts[0] not in SKIP
    and not any(x.startswith(".") for x in p.relative_to(ROOT).parts)
]
print(f"Pages: {len(pages)}")
types: dict[str, int] = {}
for p in pages:
    t = p.read_text(encoding="utf-8")
    for m in re.finditer(r"application/ld\+json\">\s*(\{.*?\})\s*</script>", t, re.S):
        data = json.loads(m.group(1))
        typ = data.get("@type")
        key = typ if isinstance(typ, str) else "+".join(typ) if isinstance(typ, list) else str(typ)
        types[key] = types.get(key, 0) + 1
print("Schema types:", types)
print("blog/index.html:", (ROOT / "blog" / "index.html").exists())
print("llms.txt:", (ROOT / "llms.txt").exists())
legacy = [
    str(p.relative_to(ROOT))
    for p in pages
    if any(x in p.read_text(encoding="utf-8") for x in ("../blog.html", "../contact.html", "../index.html"))
]
print("Legacy links:", len(legacy), legacy[:5])
