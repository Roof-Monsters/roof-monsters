#!/usr/bin/env python3
"""Verify every sitemap URL has a local index.html and optional live HTTP check."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data" / "site-seo.json"
SITEMAP_PATH = ROOT / "sitemap.xml"
SKIP = {"partials", "scripts", "assets", "data"}


def load_sitemap_locs() -> list[str]:
    tree = ET.parse(SITEMAP_PATH)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [el.text.strip() for el in tree.findall(".//sm:loc", ns)]
    if not locs:
        locs = [el.text.strip() for el in tree.iter() if el.tag.endswith("loc") and el.text]
    return locs


def url_to_local_path(url: str, bases: list[str]) -> Path:
    path = url
    for base in bases:
        if url.startswith(base):
            path = url[len(base) :]
            break
    path = path.strip("/")
    if not path:
        return ROOT / "index.html"
    return ROOT / path.replace("/", "\\") / "index.html" if "\\" in str(ROOT) else ROOT / path / "index.html"


def collect_site_pages() -> set[str]:
    pages: set[str] = set()
    if (ROOT / "index.html").exists():
        pages.add("/")
    for index in sorted(ROOT.rglob("index.html")):
        if index.parent == ROOT:
            continue
        rel = index.parent.relative_to(ROOT)
        if rel.parts[0] in SKIP or any(p.startswith(".") for p in rel.parts):
            continue
        pages.add("/" + "/".join(rel.parts) + "/")
    return pages


def validate_html(path: Path) -> list[str]:
    issues: list[str] = []
    if not path.exists():
        return ["missing file"]
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text.strip()) < 200:
        issues.append("file too small")
    if "<title>" not in text.lower():
        issues.append("no <title>")
    if 'id="site-header-include"' not in text and "site-header" not in text:
        issues.append("no site header include")
    return issues


def http_check(url: str, timeout: float = 15.0) -> tuple[int | None, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "RoofMonstersSitemapVerify/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, ""
    except urllib.error.HTTPError as exc:
        return exc.code, str(exc.reason)
    except Exception as exc:  # noqa: BLE001
        return None, str(exc)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify sitemap URLs map to real pages")
    parser.add_argument("--live", metavar="BASE", help="Also HTTP-check each URL (e.g. demo base URL)")
    args = parser.parse_args()

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    bases = [config["productionBase"].rstrip("/"), config["demoBase"].rstrip("/")]

    locs = load_sitemap_locs()
    site_pages = collect_site_pages()

    print(f"Sitemap URLs: {len(locs)}")
    print(f"Site index.html pages: {len(site_pages)}")
    print()

    missing: list[tuple[str, Path]] = []
    invalid: list[tuple[str, Path, list[str]]] = []

    sitemap_paths: set[str] = set()
    for loc in locs:
        local = url_to_local_path(loc, bases)
        rel = "/" if local.parent == ROOT else "/" + "/".join(local.parent.relative_to(ROOT).parts) + "/"
        sitemap_paths.add(rel)
        issues = validate_html(local)
        if "missing file" in issues:
            missing.append((loc, local))
        elif issues:
            invalid.append((loc, local, issues))

    orphans = sorted(site_pages - sitemap_paths)

    failed_live: list[tuple[str, str]] = []
    if args.live:
        live_base = args.live.rstrip("/")
        print(f"Live check base: {live_base}")
        for loc in locs:
            demo_loc = loc
            for base in bases:
                if loc.startswith(base):
                    demo_loc = live_base + loc[len(base) :]
                    break
            status, err = http_check(demo_loc)
            if status != 200:
                failed_live.append((demo_loc, f"HTTP {status}" if status else err))

    ok = not missing and not invalid and not orphans and not failed_live

    if missing:
        print("MISSING LOCAL PAGES (in sitemap, no index.html):")
        for loc, path in missing:
            print(f"  {loc}")
            print(f"    -> {path.relative_to(ROOT)}")
        print()

    if invalid:
        print("INVALID LOCAL PAGES:")
        for loc, path, issues in invalid:
            print(f"  {loc} ({', '.join(issues)})")
            print(f"    -> {path.relative_to(ROOT)}")
        print()

    if orphans:
        print("ORPHAN PAGES (exist on disk, not in sitemap):")
        for path in orphans:
            print(f"  {path}")
        print()

    if failed_live:
        print("FAILED LIVE HTTP CHECKS:")
        for url, reason in failed_live:
            print(f"  {url} — {reason}")
        print()

    if ok:
        print("PASS: Every sitemap URL has a valid local page.")
        if args.live:
            print(f"PASS: All {len(locs)} URLs returned HTTP 200 at {args.live}")
        return 0

    print("FAIL: See issues above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
