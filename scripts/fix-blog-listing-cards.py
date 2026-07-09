#!/usr/bin/env python3
"""Unify blog listing cards to single-link pattern (matches homepage partial)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    ROOT / "blog" / "index.html",
    ROOT / "category" / "roof-repair" / "index.html",
    ROOT / "category" / "roof-monsters-news" / "index.html",
    ROOT / "category" / "roof-maintenance" / "index.html",
    ROOT / "category" / "roof-installation" / "index.html",
]

ARTICLE_RE = re.compile(
    r"<article class=\"blog-card\">\s*"
    r"<a href=\"([^\"]+)\" class=\"blog-img-link\">\s*"
    r"(<img[^>]+>)\s*"
    r"</a>\s*"
    r"<div class=\"blog-body\">(.*?)</div>\s*"
    r"</article>",
    re.S,
)


def normalize_body(body: str) -> str:
    body = re.sub(
        r"<h2><a href=\"[^\"]+\">([^<]+)</a></h2>",
        r"<h3>\1</h3>",
        body,
    )
    body = re.sub(
        r"<a href=\"[^\"]+\" class=\"read-more\">(Read more <i class=\"fa-solid fa-arrow-right\"></i>)</a>",
        r'<span class="read-more">\1</span>',
        body,
    )
    body = re.sub(
        r"<span class=\"blog-cat\"><a href=\"[^\"]+\">([^<]+)</a></span>",
        r'<span class="blog-cat">\1</span>',
        body,
    )
    # Ensure calendar icons are aria-hidden
    body = body.replace(
        '<i class="fa-regular fa-calendar"></i>',
        '<i class="fa-regular fa-calendar" aria-hidden="true"></i>',
    )
    body = body.replace(
        '<i class="fa-solid fa-arrow-right"></i>',
        '<i class="fa-solid fa-arrow-right" aria-hidden="true"></i>',
    )
    return body.strip()


def fix_article(match: re.Match[str]) -> str:
    url = match.group(1)
    img = match.group(2)
    body = normalize_body(match.group(3))
    return (
        f'<article class="blog-card">\n'
        f'        <a href="{url}" class="blog-card-link">\n'
        f'          <span class="blog-img-link">\n'
        f"            {img}\n"
        f"          </span>\n"
        f"          <div class=\"blog-body\">\n"
        f"            {body}\n"
        f"          </div>\n"
        f"        </a>\n"
        f"      </article>"
    )


def fix_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    new_text, n = ARTICLE_RE.subn(fix_article, text)
    if n and new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return n


def main() -> None:
    total = 0
    for path in TARGETS:
        if not path.exists():
            print("skip missing", path)
            continue
        n = fix_file(path)
        total += n
        print(f"{path.relative_to(ROOT)}: {n} cards")
    print("total cards", total)


if __name__ == "__main__":
    main()
