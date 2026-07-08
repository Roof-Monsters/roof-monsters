#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BADGE = "Licensed \u2022 Insured \u2022 Family Owned \u2022 Serving Tampa Bay Since 1988"
FULL = "Licensed \u2022 Insured \u2022 Roofing CCC1335398, CCC052490 \u00b7 Building CBC015719"

patterns = [
    (re.compile(r"Licensed &amp; Insured .{1,4} CCC1335398 &amp; CBC015719"), FULL),
    (re.compile(r"Licensed &amp; Insured .{1,4} CCC1335398"), BADGE),
]

for path in ROOT.rglob("*.html"):
    text = path.read_text(encoding="utf-8")
    new = text
    for pattern, replacement in patterns:
        new = pattern.sub(replacement, new)
    if new != text:
        path.write_text(new, encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)}")
