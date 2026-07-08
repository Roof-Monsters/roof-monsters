#!/usr/bin/env python3
"""Migrate Roof Monsters demo to live-matching clean URLs (folder + index.html)."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# demo file -> site path (trailing slash, index.html inside)
PAGE_MAP: dict[str, str] = {
    "about.html": "about-us",
    "contact.html": "contact-us",
    "gallery.html": "gallery",
    "testimonials.html": "testimonials",
    "special-offers.html": "special-offers",
    "services.html": "services",
    "service-installation.html": "services/comprehensive-roof-installations",
    "service-repairs.html": "services/expert-roof-repairs-and-maintenance",
    "service-inspections.html": "services/free-roof-inspections-and-consultations",
    "service-storm-damage.html": "services/storm-damage-repair-specialists",
    "service-gutters.html": "services/gutter-installation-and-cleaning",
    "service-skylights.html": "services/skylight-installation-and-repair",
    "blog.html": "blog",
    "blog/october-roofing-season.html": (
        "october-roofing-season-in-tampa-bay-why-fall-is-the-best-time-to-schedule-your-roof-work"
    ),
    "blog/roof-monsters-way.html": "the-roof-monsters-way-what-sets-our-roofing-company-apart",
    "blog/hurricane-season-prep.html": "how-to-prepare-your-roof-for-floridas-hurricane-season",
}

# old href token -> new root-relative path
LINK_REPLACEMENTS: list[tuple[str, str]] = [
    ("index.html", "/"),
    ("about.html", "/about-us/"),
    ("contact.html", "/contact-us/"),
    ("gallery.html", "/gallery/"),
    ("testimonials.html", "/testimonials/"),
    ("special-offers.html", "/special-offers/"),
    ("services.html", "/services/"),
    ("service-installation.html", "/services/comprehensive-roof-installations/"),
    ("service-repairs.html", "/services/expert-roof-repairs-and-maintenance/"),
    ("service-inspections.html", "/services/free-roof-inspections-and-consultations/"),
    ("service-storm-damage.html", "/services/storm-damage-repair-specialists/"),
    ("service-gutters.html", "/services/gutter-installation-and-cleaning/"),
    ("service-skylights.html", "/services/skylight-installation-and-repair/"),
    ("blog.html", "/blog/"),
    (
        "blog/october-roofing-season.html",
        "/october-roofing-season-in-tampa-bay-why-fall-is-the-best-time-to-schedule-your-roof-work/",
    ),
    (
        "blog/roof-monsters-way.html",
        "/the-roof-monsters-way-what-sets-our-roofing-company-apart/",
    ),
    (
        "blog/hurricane-season-prep.html",
        "/how-to-prepare-your-roof-for-floridas-hurricane-season/",
    ),
]

ASSET_PREFIX_RE = re.compile(
    r'(?P<attr>href|src|data-partial)=(["\'])'
    r'(?!\/?assets\/|https?:|\/|#|tel:|mailto:|\.\.)'
    r'assets\/'
)


def rewrite_links(text: str) -> str:
    for old, new in LINK_REPLACEMENTS:
        text = text.replace(f'href="{old}"', f'href="{new}"')
        text = text.replace(f"href='{old}'", f"href='{new}'")

    # ../assets from nested blog -> /assets
    text = re.sub(r'(?:\.\./)+assets/', '/assets/', text)
    text = text.replace('src="../includes.js"', 'src="/includes.js"')
    text = text.replace('src="includes.js"', 'src="/includes.js"')
    text = text.replace('src="../assets/', 'src="/assets/')
    text = text.replace('src="assets/', 'src="/assets/')
    text = text.replace('href="../assets/', 'href="/assets/')
    text = text.replace('href="assets/', 'href="/assets/')
    text = text.replace('data-partial="partials/', 'data-partial="/partials/')
    return text


def migrate_pages() -> None:
    for source, dest in PAGE_MAP.items():
        src = ROOT / source
        if not src.exists():
            print(f"skip missing {source}")
            continue
        dest_dir = ROOT / dest
        dest_dir.mkdir(parents=True, exist_ok=True)
        content = rewrite_links(src.read_text(encoding="utf-8"))
        (dest_dir / "index.html").write_text(content, encoding="utf-8")
        print(f"migrated {source} -> {dest}/index.html")


def rewrite_shared_files() -> None:
    for rel in ["index.html", "header.html", "footer.html"]:
        path = ROOT / rel
        if path.exists():
            path.write_text(rewrite_links(path.read_text(encoding="utf-8")), encoding="utf-8")
            print(f"updated links in {rel}")

    partials = ROOT / "partials"
    if partials.exists():
        for path in partials.rglob("*.html"):
            path.write_text(rewrite_links(path.read_text(encoding="utf-8")), encoding="utf-8")
        print("updated partials")


def remove_legacy_files() -> None:
    for source in PAGE_MAP:
        path = ROOT / source
        if path.exists():
            path.unlink()
            print(f"removed legacy {source}")
    blog_dir = ROOT / "blog"
    if blog_dir.exists() and not any(blog_dir.iterdir()):
        blog_dir.rmdir()
    elif blog_dir.exists():
        # remove leftover short-slug files if empty dirs remain
        for child in sorted(blog_dir.rglob("*"), reverse=True):
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                try:
                    child.rmdir()
                except OSError:
                    pass
        try:
            blog_dir.rmdir()
        except OSError:
            pass


def main() -> None:
    migrate_pages()
    rewrite_shared_files()
    remove_legacy_files()
    print("done")


if __name__ == "__main__":
    main()
