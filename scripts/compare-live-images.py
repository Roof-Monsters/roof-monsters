#!/usr/bin/env python3
"""Normalize WP image URLs to source files and compare to demo."""

from __future__ import annotations

import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "assets" / "images"

PAGES = [
    "https://roofmonsters.co/",
    "https://roofmonsters.co/about-us/",
    "https://roofmonsters.co/services/",
    "https://roofmonsters.co/special-offers/",
    "https://roofmonsters.co/gallery/",
    "https://roofmonsters.co/testimonials/",
    "https://roofmonsters.co/contact-us/",
    "https://roofmonsters.co/locations-we-serve/",
]

IMG_RE = re.compile(
    r"https://roofmonsters\.co/wp-content/uploads/[^\s\"'>)]+?\.(?:jpe?g|png|webp|gif)",
    re.I,
)
SIZE_SUFFIX = re.compile(r"-\d+x\d+$", re.I)


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return resp.read().decode("utf-8", "ignore")


def source_key(url: str) -> str:
    name = url.rstrip("/").split("/")[-1].split("?")[0]
    stem, ext = name.rsplit(".", 1)
    stem = SIZE_SUFFIX.sub("", stem)
    return f"{stem}.{ext.lower()}"


def main() -> None:
    all_urls: set[str] = set()
    for page in PAGES:
        try:
            html = fetch(page)
            all_urls |= {m.group(0).split("?")[0] for m in IMG_RE.finditer(html)}
        except Exception as exc:
            print(f"FAIL {page}: {exc}")

    live_sources = {source_key(u): u for u in all_urls}

    # What our demo references (visible in rebuild)
    demo_refs: set[str] = set()
    for path in list(ROOT.glob("*.html")) + [ROOT / "header.html", ROOT / "footer.html", ROOT / "assets/css/style.css"]:
        if not path.is_file() or "GROWTH" in path.name:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r"(?:assets/images|\.\./images)/([^\"'\)\s]+)", text):
            demo_refs.add(m.group(1))

    local_files = {p.relative_to(IMAGES).as_posix() for p in IMAGES.rglob("*") if p.is_file()}

    # Map live source -> whether demo has equivalent content
    migrated = {
        "unnamed.png": "brand/logo.webp",
        "Png-2.png": None,  # alt mobile logo on live
        "IMG_6006.jpg": "gallery/installation-01.webp",
        "IMG_5993.jpg": "gallery/project-02.webp",
        "IMG_5994-1.jpg": "gallery/completed-03.webp",
        "IMG_6015.jpg": "gallery/installation-04.webp",
        "473619572_122153237438329090_1935536644784443363_n.jpg": "team/crew-01.webp",
        "436379617_122100952934329090_785895433237978047_n.jpg": "team/rob-lewis.webp",
        "FireShot-Capture-102-Atlas-roof-pictures-Google-Drive-drive.google.com_-e1737566288472.png": "gallery/atlas-install-01.webp",
        "FireShot-Capture-103-Atlas-roof-pictures-Google-Drive-drive.google.com_-e1737566357418.png": "gallery/atlas-install-02.webp",
        "Atlas_Designer_Shingles_featuring_Scotchgard_-_Lock-up_2.jpg": "brand/atlas-shingles-banner.webp",
        "Atlas_Designer_Shingles_featuring_Scotchgard_-_Lock-up_2-1024x400.jpg": "brand/atlas-shingles-banner.webp",
        "New-Roof-Pinellas-County-Florida.jpg": "gallery/pinellas-new-roof.webp",
        "F6.jpg": "backgrounds/stats-section.webp",
        "us-veteran-woman-leaving-for-military-service--1536x1024.jpg": "offers/military-discount-hero.webp",
        "roof-instalaltion.webp": "services/inspections.webp",
        "roof-instalation-roofmonster-878x1536.webp": "services/installation.webp",
        "roof-instalation-roofmonster.webp": "services/installation.webp",
        "repair-maintenance-878x1536.webp": "services/repairs.webp",
        "repair-maintenance.webp": "services/repairs.webp",
        "guteere2-878x1536.webp": "services/gutters.webp",
        "guteere2.webp": "services/gutters.webp",
        "emergency-roof-repair-878x1536.webp": "services/storm-damage.webp",
        "emergency-roof-repair.webp": "services/storm-damage.webp",
        "F5.jpg": "gallery/completed-05.webp",
        "F25.jpg": "team/crew-at-work.webp",
        "IMG_7565.jpeg": "gallery/completed-06.webp",
        "IMG_7610.jpeg": "gallery/installation-07.webp",
        "IMG_7611.jpg": "gallery/replacement-08.webp",
        "IMG_7612.jpg": "gallery/project-09.webp",
        "4353A7A7F8612BEFC428715EDFA7CC95-scaled.jpg": "gallery/quality-work.webp",
        "F28F4EF9BB3B4DDEE1861426C663ACB0-scaled.jpg": "gallery/tampa-bay-project.webp",
        "Gemini_Generated_Image_5fh1575fh1575fh1.png": "blog/october-roofing-season.webp",
        "aftermath-of-hurricane-debby-flooding-natural-disaster-.jpg": "blog/hurricane-prep.webp",
        "happy-customer.jpg": "blog/happy-customer.webp",
        "locations-we-serve.webp": None,
        "roofing-locations-we-serve.webp": None,
        "roofing-services.webp": None,
        "ChatGPT-Image-Apr-17-2025-12_30_46-PM.png": None,
        "worker-hands-installing-bitumen-roof-shingles-with-air-hammer-and-nail.jpg": None,
        "IMG_7307.jpeg": None,
        "IMG_7311.jpeg": None,
        "IMG_7402.jpeg": None,
        "IMG_7410.jpeg": None,
    }

    covered = []
    missing_visible = []
    not_in_demo = []

    for src, example_url in sorted(live_sources.items()):
        local = migrated.get(src)
        if local and local in local_files:
            covered.append((src, local))
        elif local is None and src in migrated:
            not_in_demo.append((src, example_url, "live-only page/content not in demo rebuild"))
        elif local and local not in local_files:
            missing_visible.append((src, local, example_url))
        else:
            missing_visible.append((src, "?", example_url))

    print(f"Live URL variants crawled: {len(all_urls)}")
    print(f"Live UNIQUE source images: {len(live_sources)}")
    print(f"Local asset files: {len(local_files)}")
    print(f"Demo image references: {len(demo_refs)}")
    print(f"Covered in local WebP: {len(covered)}")
    print(f"Not in demo rebuild: {len(not_in_demo)}")
    print(f"Missing from local library: {len(missing_visible)}")
    print()
    print("=== COVERED (live source -> local webp) ===")
    for src, loc in covered:
        print(f"  {src} -> {loc}")
    print()
    if not_in_demo:
        print("=== ON LIVE SITE BUT NOT IN OUR DEMO PAGES ===")
        for src, url, note in not_in_demo:
            print(f"  {src}")
            print(f"    {note}")
    print()
    if missing_visible:
        print("=== UNIQUE LIVE IMAGES WE DO NOT HAVE LOCALLY ===")
        for src, loc, url in missing_visible:
            print(f"  {src}")
    print()
    print("=== DEMO USES (all should be .webp except svg) ===")
    for ref in sorted(demo_refs):
        ext = Path(ref).suffix.lower()
        ok = ext in {".webp", ".svg"}
        print(f"  {'OK' if ok else 'BAD'} {ref}")


if __name__ == "__main__":
    main()
