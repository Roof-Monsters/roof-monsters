#!/usr/bin/env python3
"""Write static HTML redirect stubs for GitHub Pages (no host 301 engine).

Stubs are noindex + follow with canonical pointing at the destination.
They intentionally omit JSON-LD so Google does not count AggregateRating /
review markup on alias URLs (GSC “multiple aggregate ratings” noise).
"""
from __future__ import annotations

from pathlib import Path

from analytics_snippet import ANALYTICS_HEAD_HTML

ROOT = Path(__file__).resolve().parents[1]

# Old public WP / short aliases -> canonical rebuild paths (root-relative).
DIR_REDIRECTS: list[tuple[str, str]] = [
    ("contact", "/contact-us/"),
    ("about", "/about-us/"),
    ("locations", "/about-us/locations-we-serve/"),
    ("reviews", "/testimonials/"),
    ("home", "/"),
    ("mckeever", "/about-us/"),
    ("terrance-mckeever", "/about-us/"),
    (
        "blog/october-roofing-season-in-tampa-bay-why-fall-is-the-best-time-to-schedule-your-roof-work",
        "/october-roofing-season-in-tampa-bay-why-fall-is-the-best-time-to-schedule-your-roof-work/",
    ),
    (
        "blog/the-roof-monsters-way-what-sets-our-roofing-company-apart",
        "/the-roof-monsters-way-what-sets-our-roofing-company-apart/",
    ),
    (
        "blog/how-to-prepare-your-roof-for-floridas-hurricane-season",
        "/how-to-prepare-your-roof-for-floridas-hurricane-season/",
    ),
    (
        "blog/what-is-tpo-roofing-and-why-its-perfect-for-florida-commercial-buildings",
        "/what-is-tpo-roofing-and-why-its-perfect-for-florida-commercial-buildings/",
    ),
    (
        "blog/5-signs-its-time-to-replace-your-roof-in-florida",
        "/5-signs-its-time-to-replace-your-roof-in-florida/",
    ),
    (
        "blog/how-to-choose-the-right-roofing-contractor",
        "/how-to-choose-the-right-roofing-contractor/",
    ),
]

# Bare .html aliases (GitHub Pages ignores .htaccess).
FILE_REDIRECTS: list[tuple[str, str]] = [
    ("contact.html", "/contact-us/"),
    ("about.html", "/about-us/"),
    ("locations.html", "/about-us/locations-we-serve/"),
    ("blog.html", "/blog/"),
    ("faqs.html", "/faqs/"),
    ("gallery.html", "/gallery/"),
    ("services.html", "/services/"),
    ("testimonials.html", "/testimonials/"),
]


def redirect_html(dest: str) -> str:
    abs_dest = f"https://roofmonsters.co{dest}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="refresh" content="0;url={dest}" />
  <meta name="robots" content="noindex, follow" />
  <link rel="canonical" href="{abs_dest}" />
  <title>Moved — Roof Monsters</title>
  <script>location.replace({dest!r});</script>
{ANALYTICS_HEAD_HTML}
</head>
<body>
  <p>This page has moved to <a href="{dest}">{abs_dest}</a>.</p>
</body>
</html>
"""


def main() -> None:
    for src, dest in DIR_REDIRECTS:
        out = ROOT / src / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(redirect_html(dest), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)} -> {dest}")

    for src, dest in FILE_REDIRECTS:
        out = ROOT / src
        out.write_text(redirect_html(dest), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)} -> {dest}")


if __name__ == "__main__":
    main()
