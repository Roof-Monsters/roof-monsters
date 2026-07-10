#!/usr/bin/env python3
"""Write static HTML redirect stubs for GitHub Pages (no host 301 engine)."""
from __future__ import annotations

from pathlib import Path

from analytics_snippet import ANALYTICS_HEAD_HTML

ROOT = Path(__file__).resolve().parents[1]

# Old public WP aliases -> canonical rebuild paths (root-relative on custom domain).
REDIRECTS: list[tuple[str, str]] = [
    ("contact", "/contact-us/"),
    ("about", "/about-us/"),
    ("locations", "/about-us/locations-we-serve/"),
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


def redirect_html(dest: str) -> str:
    # Absolute production URL for browsers/crawlers; base-tag aware relative href
    # also works on demo path via leading slash on custom domain.
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="refresh" content="0;url={dest}" />
  <link rel="canonical" href="https://roofmonsters.co{dest}" />
  <title>Moved — Roof Monsters</title>
  <script>location.replace({dest!r});</script>
{ANALYTICS_HEAD_HTML}
</head>
<body>
  <p>This page has moved to <a href="{dest}">https://roofmonsters.co{dest}</a>.</p>
</body>
</html>
"""


def main() -> None:
    for src, dest in REDIRECTS:
        out = ROOT / src / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(redirect_html(dest), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)} -> {dest}")


if __name__ == "__main__":
    main()
