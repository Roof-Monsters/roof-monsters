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

SERVICE_LOCATIONS = {
    "comprehensive-roof-installations": [
        ("Pinellas County", "about-us/locations-we-serve/roofing-company-pinellas-county-florida/"),
        ("Hillsborough County", "about-us/locations-we-serve/roofing-company-hillsborough-county-florida/"),
        ("Tampa", "about-us/locations-we-serve/roofing-company-tampa-florida/"),
        ("Clearwater", "about-us/locations-we-serve/roofing-company-clearwater-florida/"),
    ],
    "expert-roof-repairs-and-maintenance": [
        ("Dunedin", "about-us/locations-we-serve/roofing-company-dunedin-florida/"),
        ("St. Petersburg", "about-us/locations-we-serve/roofing-company-st-petersburg-florida/"),
        ("Largo", "about-us/locations-we-serve/roofing-company-largo-florida/"),
    ],
    "free-roof-inspections-and-consultations": [
        ("Palm Harbor", "about-us/locations-we-serve/roofing-company-palm-harbor-florida/"),
        ("Seminole", "about-us/locations-we-serve/roofing-company-seminole-florida/"),
        ("Pasco County", "about-us/locations-we-serve/roofing-company-pasco-county-florida/"),
    ],
    "storm-damage-repair-specialists": [
        ("Tampa", "about-us/locations-we-serve/roofing-company-tampa-florida/"),
        ("Clearwater", "about-us/locations-we-serve/roofing-company-clearwater-florida/"),
        ("Hillsborough County", "about-us/locations-we-serve/roofing-company-hillsborough-county-florida/"),
    ],
    "gutter-installation-and-cleaning": [
        ("Safety Harbor", "about-us/locations-we-serve/roofing-company-safety-harbor-florida/"),
        ("New Port Richey", "about-us/locations-we-serve/roofing-company-new-port-richey-florida/"),
    ],
    "skylight-installation-and-repair": [
        ("Pinellas County", "about-us/locations-we-serve/roofing-company-pinellas-county-florida/"),
        ("Manatee County", "about-us/locations-we-serve/roofing-company-manatee-county-florida/"),
    ],
}

LOCATION_SERVICES = [
    ("Roof Installation", "services/comprehensive-roof-installations/"),
    ("Roof Repairs", "services/expert-roof-repairs-and-maintenance/"),
    ("Free Inspections", "services/free-roof-inspections-and-consultations/"),
    ("Storm Damage", "services/storm-damage-repair-specialists/"),
    ("Gutters", "services/gutter-installation-and-cleaning/"),
    ("Skylights", "services/skylight-installation-and-repair/"),
]

CROSS_LINK_START = "<!-- rm-cross-links:start -->"
CROSS_LINK_END = "<!-- rm-cross-links:end -->"


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
    links = SERVICE_LOCATIONS.get(slug, [])
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
        <p class="section-desc">Roof Monsters serves Tampa Bay from our Dunedin headquarters. Explore local pages related to this service.</p>
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
    if block and "<!-- MINI STATS -->" in text:
        return text.replace("  <!-- MINI STATS -->", block + "\n\n  <!-- MINI STATS -->", 1)
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
    for path in collect_pages():
        original = path.read_text(encoding="utf-8", errors="replace")
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
    print(f"Done. Updated {changed} pages.")


if __name__ == "__main__":
    main()
