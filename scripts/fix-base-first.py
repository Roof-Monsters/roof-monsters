#!/usr/bin/env python3
"""Ensure __RM_BASE__ / <base> script is first in <head> on every page."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"partials", "scripts", "assets", "data", "node_modules", ".git"}

BASE_SCRIPT = """  <script>
(function () {
  var path = location.pathname;
  var marker = '/roof-monsters/';
  var idx = path.indexOf(marker);
  window.__RM_BASE__ = idx >= 0 ? path.slice(0, idx + marker.length) : '/';
  document.write('<base href="' + window.__RM_BASE__ + '">');
})();
  </script>"""


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "__RM_BASE__" not in text:
        return False
    # Already first element in head?
    if re.search(r"<head>\s*<script>[\s\S]*?__RM_BASE__", text):
        return False
    # Remove later duplicate base blocks
    text2 = re.sub(
        r"\s*<script>\s*\(function \(\) \{\s*var path = location\.pathname;[\s\S]*?__RM_BASE__[\s\S]*?\}\)\(\);\s*</script>",
        "",
        text,
        count=0,
    )
    text2 = text2.replace("<head>", f"<head>\n{BASE_SCRIPT}", 1)
    if text2 != text:
        path.write_text(text2, encoding="utf-8")
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
    print(f"Moved base script on {changed} page(s)")


if __name__ == "__main__":
    main()
