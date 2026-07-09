#!/usr/bin/env python3
"""Patch all pages to use robust GitHub Pages base + favicon bootstrap."""

from __future__ import annotations

import re
from pathlib import Path

from base_head_script import BASE_HEAD_SCRIPT

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"partials", "scripts", "assets", "data", "node_modules", ".git"}

OLD = re.compile(
    r"  <script>\s*\(function \(\) \{[\s\S]*?__RM_BASE__[\s\S]*?\}\)\(\);\s*</script>",
    re.M,
)


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "__RM_BASE__" not in text:
        return False
    updated, n = OLD.subn(BASE_HEAD_SCRIPT, text, count=1)
    if n:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("index.html")):
        if path.parts[0] in SKIP or any(p in SKIP for p in path.parts):
            continue
        if patch_file(path):
            print(path.relative_to(ROOT))
            changed += 1
    print(f"Patched {changed} page(s)")


if __name__ == "__main__":
    main()
