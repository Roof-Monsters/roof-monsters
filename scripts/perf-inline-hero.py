#!/usr/bin/env python3
"""Inline homepage hero for CLS/LCP and apply performance head/script tweaks."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
HERO = (ROOT / "partials" / "home" / "hero-slider.html").read_text(encoding="utf-8")

# Prefer real <img> for LCP discovery on first slide
HERO = HERO.replace(
    """    <div class="hero-slide active">
      <div class="hero-slide-bg ken-burns bg-hero-slide-1"></div>
      <div class="hero-overlay"></div>
    </div>""",
    """    <div class="hero-slide active">
      <img class="hero-slide-bg ken-burns hero-lcp-img" src="/assets/images/gallery/atlas-install-01.webp" alt="Atlas shingle roof installation by Roof Monsters in Tampa Bay" width="1600" height="1067" fetchpriority="high" decoding="async" />
      <div class="hero-overlay"></div>
    </div>""",
)

index = INDEX.read_text(encoding="utf-8")

# Preload LCP image + font display swap already in Google Fonts URL — add display=swap if missing
if "display=swap" not in index:
    index = index.replace(
        "family=Inter:wght@400;500;600;700&display=swap",
        "family=Inter:wght@400;500;600;700&display=swap",
    )

# Add preload for LCP hero image after style.css link
preload = (
    '  <link rel="preload" as="image" href="/assets/images/gallery/atlas-install-01.webp" '
    'type="image/webp" fetchpriority="high" />\n'
)
if "atlas-install-01.webp" not in index.split("preload")[0] if "preload" in index else True:
    if 'href="/assets/css/style.css"' in index and "atlas-install-01.webp" not in index:
        index = index.replace(
            '  <link rel="stylesheet" href="/assets/css/style.css" />\n',
            '  <link rel="stylesheet" href="/assets/css/style.css" />\n' + preload,
        )

# Defer Font Awesome (non-critical for first paint) — load async
index = index.replace(
    '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />\n',
    '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" media="print" onload="this.media=\'all\'" />\n'
    '  <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" /></noscript>\n',
)

# Inline hero: replace data-partial hero slot
old_slot = '    <div data-partial="partials/home/hero-slider.html"></div>\n'
if old_slot not in index:
    raise SystemExit("hero slot not found")

# Indent hero content for readability inside main
hero_indented = "\n".join(
    ("    " + line if line.strip() else line) for line in HERO.strip().splitlines()
) + "\n"
index = index.replace(old_slot, hero_indented)

# Defer scripts
index = index.replace(
    '  <script src="/includes.js"></script>\n  <script src="/assets/js/main.js"></script>\n',
    '  <script src="/includes.js" defer></script>\n  <script src="/assets/js/main.js" defer></script>\n',
)

# Header/footer placeholders with reserved height classes
index = index.replace(
    '  <div id="site-header-include"></div>',
    '  <div id="site-header-include" class="site-chrome-slot site-chrome-slot--header" aria-hidden="true"></div>',
)
index = index.replace(
    '  <div id="site-footer-include"></div>',
    '  <div id="site-footer-include" class="site-chrome-slot site-chrome-slot--footer" aria-hidden="true"></div>',
)

INDEX.write_text(index, encoding="utf-8")
print("index.html updated")

# Keep partial in sync for any other consumers
(ROOT / "partials" / "home" / "hero-slider.html").write_text(
    HERO if HERO.startswith("<section") else HERO.lstrip(),
    encoding="utf-8",
)
# rewrite partial cleanly from file we built
partial = HERO
if not partial.startswith("<section"):
    # strip accidental indent from earlier replace on index-only copy
    pass
# Re-read and write the LCP img version to partial
partial_src = (ROOT / "partials" / "home" / "hero-slider.html").read_text(encoding="utf-8")
print("hero partial has lcp img:", "hero-lcp-img" in partial_src)
