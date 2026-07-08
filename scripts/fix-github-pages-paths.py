#!/usr/bin/env python3
"""Rewrite root-absolute internal paths for GitHub Pages (/demo-sites/roof-monsters/)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BASE_SCRIPT = """  <script>
(function () {
  var path = location.pathname;
  var marker = '/roof-monsters/';
  var idx = path.indexOf(marker);
  window.__RM_BASE__ = idx >= 0 ? path.slice(0, idx + marker.length) : '/';
  document.write('<base href="' + window.__RM_BASE__ + '">');
})();
  </script>"""

SKIP_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "#",
    "//",
)

INTERNAL_PREFIXES = (
    "/assets/",
    "/partials/",
    "/includes.js",
    "/about-us/",
    "/services/",
    "/blog/",
    "/contact/",
    "/privacy-policy/",
    "/terms-of-service/",
    "/sitemap.xml",
)

ATTR_PATTERN = re.compile(
    r'(?P<attr>(?:href|src|srcset|data-partial))="(?P<value>[^"]+)"'
)


def rewrite_value(value: str) -> str:
    if value.startswith(SKIP_PREFIXES):
        return value
    if value == "/":
        return "./"
    if value.startswith("/"):
        return value.lstrip("/")
    return value


def patch_html(text: str, inject_base: bool) -> str:
    def repl(match: re.Match[str]) -> str:
        attr = match.group("attr")
        value = match.group("value")
        return f'{attr}="{rewrite_value(value)}"'

    updated = ATTR_PATTERN.sub(repl, text)

    if inject_base and "window.__RM_BASE__" not in updated:
        updated = updated.replace("<head>", f"<head>\n{BASE_SCRIPT}", 1)

    return updated


def should_patch(path: Path) -> bool:
    if path.suffix != ".html":
        return False
    return True


def main() -> None:
    html_files = sorted(ROOT.rglob("*.html"))
    changed = 0
    for path in html_files:
        original = path.read_text(encoding="utf-8")
        inject_base = path.name == "index.html" or "<!DOCTYPE html>" in original[:200]
        updated = patch_html(original, inject_base=inject_base and "<head>" in original)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            changed += 1
            print(f"Updated {path.relative_to(ROOT)}")

    print(f"Patched {changed} HTML file(s).")


if __name__ == "__main__":
    main()
