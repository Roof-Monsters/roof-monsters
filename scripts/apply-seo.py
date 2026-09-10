#!/usr/bin/env python3
"""Apply SEO meta, schema, encoding fixes, and content patches across all pages."""

from __future__ import annotations

import json
import re
from pathlib import Path

from seo_lib import (
    ROOT,
    build_seo_head,
    classify_page,
    fix_encoding,
    inject_seo,
    load_config,
)
from analytics_snippet import inject_analytics

SKIP_DIRS = {"partials", "scripts", "assets", "data"}
SKIP_FILES = {"GROWTH-ROADMAP-PROPOSAL.html"}

PINELLAS_CORE = [
    ("Dunedin", "about-us/locations-we-serve/roofing-company-dunedin-florida/"),
    ("Clearwater", "about-us/locations-we-serve/roofing-company-clearwater-florida/"),
    ("Palm Harbor", "about-us/locations-we-serve/roofing-company-palm-harbor-florida/"),
    ("Largo", "about-us/locations-we-serve/roofing-company-largo-florida/"),
    ("St. Petersburg", "about-us/locations-we-serve/roofing-company-st-petersburg-florida/"),
]

SERVICE_LOCATIONS = {
    "comprehensive-roof-installations": PINELLAS_CORE,
    "expert-roof-repairs-and-maintenance": PINELLAS_CORE[:4],
    "free-roof-inspections-and-consultations": PINELLAS_CORE[:3],
    "storm-damage-repair-specialists": [
        ("Dunedin", "about-us/locations-we-serve/roofing-company-dunedin-florida/"),
        ("Clearwater", "about-us/locations-we-serve/roofing-company-clearwater-florida/"),
        ("Tampa", "about-us/locations-we-serve/roofing-company-tampa-florida/"),
    ],
    "gutter-installation-and-cleaning": PINELLAS_CORE[:3],
    "skylight-installation-and-repair": PINELLAS_CORE[:2],
    "roof-replacement": PINELLAS_CORE,
    "roof-repair": PINELLAS_CORE,
    "emergency-roof-repair": [
        ("Dunedin", "about-us/locations-we-serve/roofing-company-dunedin-florida/"),
        ("Clearwater", "about-us/locations-we-serve/roofing-company-clearwater-florida/"),
        ("Tampa", "about-us/locations-we-serve/roofing-company-tampa-florida/"),
    ],
}

LOCATION_SERVICES = [
    ("Roof Replacement — primary", "services/roof-replacement/"),
    ("Roof Repair — primary", "services/roof-repair/"),
    ("Emergency Repair — primary", "services/emergency-roof-repair/"),
    ("Storm Damage — primary", "services/storm-damage-repair-specialists/"),
    ("Free Inspections", "services/free-roof-inspections-and-consultations/"),
    ("Atlas Shingle Roofing", "services/shingle-roofing/"),
]

CROSS_LINK_START = "<!-- rm-cross-links:start -->"
CROSS_LINK_END = "<!-- rm-cross-links:end -->"


def is_redirect_stub(text: str) -> bool:
    """Skip soft-redirect alias pages — they must stay noindex without JSON-LD."""
    lower = text.lower()
    if 'http-equiv="refresh"' in lower or "http-equiv='refresh'" in lower:
        return True
    if "<title>moved — roof monsters</title>" in lower:
        return True
    return False


def collect_pages() -> list[Path]:
    pages = []
    for index in sorted(ROOT.rglob("index.html")):
        rel = index.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS or rel.name in SKIP_FILES:
            continue
        if any(p.startswith(".") for p in rel.parts):
            continue
        pages.append(index)
    return pages


def service_cross_links(slug: str) -> str:
    links = SERVICE_LOCATIONS.get(slug) or PINELLAS_CORE
    if not links:
        return ""
    items = "\n".join(
        f'          <li><a href="/{href}">{name} roofing</a></li>' for name, href in links
    )
    return f"""
  {CROSS_LINK_START}
  <section class="rm-cross-links section-pad section-bg-white">
    <div class="container">
      <div class="section-header">
        <span class="section-eyebrow">Service Areas</span>
        <h2>Roofing Service Areas for This Work</h2>
        <p class="section-desc">Roof Monsters serves Pinellas first from Dunedin. These pages are the cities we want most for this work — not Jacksonville.</p>
      </div>
      <ul class="rm-cross-links-list">
{items}
      </ul>
      <p class="rm-cross-links-more"><a href="/about-us/locations-we-serve/">View all service areas</a></p>
    </div>
  </section>
  {CROSS_LINK_END}
"""


def location_cross_links() -> str:
    items = "\n".join(
        f'          <li><a href="{href}">{name}</a></li>' for name, href in LOCATION_SERVICES
    )
    return f"""
        {CROSS_LINK_START}
        <h3>Explore Our Roofing Services</h3>
        <ul class="rm-cross-links-inline">
{items}
        </ul>
        {CROSS_LINK_END}
"""


def patch_cross_links(text: str, path: Path) -> str:
    page_type = classify_page(path)
    if page_type != "service":
        return text
    text = re.sub(
        rf"\s*{re.escape(CROSS_LINK_START)}.*?{re.escape(CROSS_LINK_END)}\s*",
        "\n",
        text,
        flags=re.S,
    )
    slug = path.parent.name
    block = service_cross_links(slug)
    if not block:
        return text
    if "<!-- MINI STATS -->" in text:
        return text.replace("  <!-- MINI STATS -->", block + "\n\n  <!-- MINI STATS -->", 1)
    footer = '  <div id="site-footer-include"></div>'
    if footer in text:
        return text.replace(footer, block + "\n" + footer, 1)
    return text


def fix_blog_links(text: str) -> str:
    replacements = {
        'href="../index.html"': 'href="/"',
        'href="../blog.html"': 'href="/blog/"',
        'href="../contact.html"': 'href="/contact-us/"',
        'href="contact.html"': 'href="/contact-us/"',
        'href="blog.html"': 'href="/blog/"',
        'href="index.html"': 'href="/"',
        'href="./"': 'href="/"',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def main() -> None:
    config = load_config()
    changed = 0
    skipped_stubs = 0
    for path in collect_pages():
        original = path.read_text(encoding="utf-8", errors="replace")
        if is_redirect_stub(original):
            skipped_stubs += 1
            continue
        text = fix_encoding(original)
        text = fix_blog_links(text)
        text = patch_cross_links(text, path)
        seo = build_seo_head(path, text, config)
        text = inject_seo(text, seo)
        text = inject_analytics(text)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
            print(f"Updated: {path.relative_to(ROOT)}")
    print(f"Done. Updated {changed} pages. Skipped {skipped_stubs} redirect stub(s).")


if __name__ == "__main__":
    main()
