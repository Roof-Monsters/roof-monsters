#!/usr/bin/env python3
"""Regenerate sitemap.xml and sitemap_index.xml from folder structure."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data" / "site-seo.json"
SKIP = {"partials", "scripts", "assets", "data", "GROWTH-ROADMAP-PROPOSAL.html"}
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"

def resolve_base(value: str | None) -> str:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if not value or value == "production":
        return config["productionBase"].rstrip("/")
    if value == "demo":
        return config["demoBase"].rstrip("/")
    return value.rstrip("/")


def collect_urls(base: str) -> list[tuple[str, str]]:
    urls: list[tuple[str, str]] = []
    if (ROOT / "index.html").exists():
        urls.append((f"{base}/", _lastmod(ROOT / "index.html")))

    for index in sorted(ROOT.rglob("index.html")):
        if index.parent == ROOT:
            continue
        rel = index.parent.relative_to(ROOT)
        if rel.parts[0] in SKIP or any(p.startswith(".") for p in rel.parts):
            continue
        path = "/" + "/".join(rel.parts) + "/"
        urls.append((f"{base}{path}", _lastmod(index)))

    return sorted(set(urls), key=lambda item: (item[0].count("/"), item[0]))


def _lastmod(path: Path) -> str:
    stamp = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return stamp.strftime("%Y-%m-%dT%H:%M:%S+00:00")


def write_sitemap_index(base: str) -> None:
    """Legacy-compatible sitemap index — points crawlers to the unified sitemap.xml."""
    index = ET.Element("sitemapindex", xmlns=SITEMAP_NS)
    entry = ET.SubElement(index, "sitemap")
    ET.SubElement(entry, "loc").text = f"{base}/sitemap.xml"
    # Date precision keeps consecutive generator runs byte-for-byte stable.
    ET.SubElement(entry, "lastmod").text = datetime.now(timezone.utc).date().isoformat()

    tree = ET.ElementTree(index)
    ET.indent(tree, space="  ")
    tree.write(ROOT / "sitemap_index.xml", encoding="UTF-8", xml_declaration=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build sitemap.xml for Roof Monsters")
    parser.add_argument(
        "--base",
        default="production",
        help="production | demo | full URL (default: production)",
    )
    args = parser.parse_args()
    base = resolve_base(args.base)
    urls = collect_urls(base)

    urlset = ET.Element("urlset", xmlns=SITEMAP_NS)
    for loc, lastmod in urls:
        url_el = ET.SubElement(urlset, "url")
        ET.SubElement(url_el, "loc").text = loc
        ET.SubElement(url_el, "lastmod").text = lastmod

    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ")
    tree.write(ROOT / "sitemap.xml", encoding="UTF-8", xml_declaration=True)
    write_sitemap_index(base)
    print(f"Wrote {len(urls)} URLs to sitemap.xml (base: {base})")
    print(f"Wrote sitemap_index.xml -> {base}/sitemap.xml")

if __name__ == "__main__":
    main()
