"""Rewrite relative asset paths to root-absolute across HTML and key scripts."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Attribute values that should become root-absolute
REL_ATTR = re.compile(
    r"""(?P<attr>\b(?:href|srcset|data-src|poster|src)\s*=\s*)(?P<q>['"])(?P<path>(?:assets/|includes\.js)[^'"]*)(?P=q)""",
    re.IGNORECASE,
)

# CSS url() in HTML style attributes / inline
REL_URL = re.compile(
    r"""url\(\s*(?P<q>['"]?)(?P<path>assets/[^)'"]+)(?P=q)\s*\)""",
    re.IGNORECASE,
)

# content="assets/..." in meta (rare)
REL_CONTENT = re.compile(
    r"""(?P<attr>\bcontent\s*=\s*)(?P<q>['"])(?P<path>assets/[^'"]+)(?P=q)""",
    re.IGNORECASE,
)


def fix_text(text: str) -> str:
    def attr_sub(m: re.Match[str]) -> str:
        path = m.group("path")
        if path.startswith("/"):
            return m.group(0)
        return f'{m.group("attr")}{m.group("q")}/{path}{m.group("q")}'

    def url_sub(m: re.Match[str]) -> str:
        path = m.group("path")
        if path.startswith("/"):
            return m.group(0)
        q = m.group("q") or ""
        return f"url({q}/{path}{q})"

    def content_sub(m: re.Match[str]) -> str:
        path = m.group("path")
        if path.startswith("/"):
            return m.group(0)
        return f'{m.group("attr")}{m.group("q")}/{path}{m.group("q")}'

    text = REL_ATTR.sub(attr_sub, text)
    text = REL_URL.sub(url_sub, text)
    text = REL_CONTENT.sub(content_sub, text)
    # Collapse accidental double slashes after domain-root (keep protocol //)
    text = text.replace('="/assets/', '="/assets/')  # noop clarity
    text = re.sub(r'(["\'])//assets/', r"\1/assets/", text)
    text = re.sub(r'(["\'])//includes\.js', r"\1/includes.js", text)
    return text


def fix_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = fix_text(original)
    if updated != original:
        path.write_text(updated, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    changed: list[str] = []
    # HTML pages
    for path in ROOT.rglob("*.html"):
        if any(part.startswith(".") for part in path.parts):
            continue
        if "node_modules" in path.parts:
            continue
        if fix_file(path):
            changed.append(str(path.relative_to(ROOT)))

    # Shared includes / partials already covered by *.html
    # Patch generator string literals that emit relative paths
    script_globs = [
        "scripts/build-*.py",
        "scripts/fix-fontawesome-loading.py",
        "scripts/perf-defer-assets.py",
        "scripts/perf-inline-hero.py",
        "scripts/apply-seo.py",
        "scripts/seo_lib.py",
    ]
    for pattern in script_globs:
        for path in ROOT.glob(pattern):
            if fix_file(path):
                changed.append(str(path.relative_to(ROOT)))

    print(f"Updated {len(changed)} files")
    for c in changed[:40]:
        print(" ", c)
    if len(changed) > 40:
        print(f"  ... and {len(changed) - 40} more")


if __name__ == "__main__":
    main()
