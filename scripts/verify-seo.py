#!/usr/bin/env python3
"""Verify SEO schema coverage across Roof Monsters pages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from seo_lib import ROOT, classify_page

SKIP = {"partials", "scripts", "assets", "data"}

REQUIRED: dict[str, set[str]] = {
    "home": {"Organization", "RoofingContractor", "LocalBusiness", "WebSite", "WebPage", "BreadcrumbList"},
    "services-hub": {"Organization", "RoofingContractor", "ItemList", "BreadcrumbList"},
    "service": {"Organization", "RoofingContractor", "Service", "BreadcrumbList"},
    "locations-hub": {"Organization", "ItemList", "BreadcrumbList"},
    "location": {"RoofingContractor", "LocalBusiness", "FAQPage", "BreadcrumbList"},
    "faq": {"FAQPage", "BreadcrumbList"},
    "testimonials": {"RoofingContractor", "LocalBusiness", "ItemList", "BreadcrumbList"},
    "gallery": {"ImageGallery", "BreadcrumbList"},
    "blog-index": {"ItemList", "BreadcrumbList"},
    "blog-post": {"BlogPosting", "BreadcrumbList"},
    "contact": {"RoofingContractor", "LocalBusiness", "ContactPage", "BreadcrumbList"},
    "about": {"AboutPage", "RoofingContractor", "BreadcrumbList"},
}


def collect_types(html: str) -> set[str]:
    found: set[str] = set()
    for m in re.finditer(r"application/ld\+json\">\s*(\{.*?\})\s*</script>", html, re.S):
        data = json.loads(m.group(1))
        nodes = data.get("@graph", [data])
        for node in nodes:
            typ = node.get("@type")
            if isinstance(typ, list):
                found.update(typ)
            elif isinstance(typ, str):
                found.add(typ)
    return found


def main() -> int:
    pages = [
        p
        for p in ROOT.rglob("index.html")
        if p.relative_to(ROOT).parts[0] not in SKIP
        and not any(x.startswith(".") for x in p.relative_to(ROOT).parts)
    ]
    print(f"Pages: {len(pages)}")
    type_counts: dict[str, int] = {}
    failures: list[str] = []
    marker_issues: list[str] = []
    duplicate_issues: list[str] = []

    for path in pages:
        html = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        starts = html.count("<!-- rm-seo:start -->")
        ends = html.count("<!-- rm-seo:end -->")
        if starts != 1 or ends != 1:
            marker_issues.append(f"{rel} start={starts} end={ends}")

        ld_scripts = len(re.findall(r'type=["\']application/ld\+json["\']', html, flags=re.I))
        agg_count = html.count('"aggregateRating"')
        if ld_scripts != 1:
            duplicate_issues.append(f"{rel}: expected 1 ld+json script, found {ld_scripts}")
        if agg_count > 1:
            duplicate_issues.append(f"{rel}: expected at most 1 aggregateRating, found {agg_count}")

        found = collect_types(html)
        for t in found:
            type_counts[t] = type_counts.get(t, 0) + 1

        page_type = classify_page(path)
        required = REQUIRED.get(page_type)
        if required:
            missing = required - found
            if missing:
                failures.append(f"{rel} ({page_type}): missing {sorted(missing)}")

    print("Schema types:", dict(sorted(type_counts.items())))
    if marker_issues:
        print(f"Marker issues ({len(marker_issues)}):")
        for row in marker_issues[:10]:
            print(" ", row)
    if duplicate_issues:
        print(f"Duplicate schema issues ({len(duplicate_issues)}):")
        for row in duplicate_issues[:20]:
            print(" ", row)
    if failures:
        print(f"Coverage failures ({len(failures)}):")
        for row in failures[:20]:
            print(" ", row)
        return 1
    if marker_issues or duplicate_issues:
        return 1
    print("Coverage: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
