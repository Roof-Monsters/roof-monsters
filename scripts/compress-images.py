#!/usr/bin/env python3
"""Compress oversized WebP assets for Lighthouse without changing layout."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FFMPEG = Path(
    r"C:\Users\nknig\Downloads\ffmpeg-7.1.1-essentials_build"
    r"\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"
)
IMG = ROOT / "assets" / "images"

# path relative to assets/images, max width, webp quality (0-100)
JOBS = [
    ("gallery/tampa-bay-project.webp", 1600, 72),
    ("backgrounds/stats-section.webp", 1600, 72),
    ("gallery/installation-07.webp", 1200, 72),
    ("gallery/pinellas-new-roof.webp", 1400, 72),
    ("gallery/quality-work.webp", 1200, 72),
    ("gallery/completed-06.webp", 1200, 72),
    ("blog/hurricane-prep.webp", 1200, 75),
    ("team/crew-01.webp", 1200, 75),
    ("gallery/atlas-install-01.webp", 1600, 75),  # hero LCP
    ("services/inspections.webp", 1000, 75),
    ("services/skylights.webp", 1000, 75),
    ("services/repairs.webp", 1000, 75),
    ("gallery/project-09.webp", 1200, 75),
    ("gallery/atlas-install-02.webp", 1200, 75),
    ("gallery/replacement-08.webp", 1000, 75),
    ("blog/october-roofing-season.webp", 1000, 75),
    ("gallery/installation-01.webp", 1400, 75),
    ("blog/happy-customer.webp", 1000, 75),
    ("offers/military-discount-hero.webp", 1400, 75),
    ("brand/logo-monster.webp", 240, 80),
    ("brand/logo-bg.webp", 240, 80),
    ("gallery/installation-04.webp", 1400, 75),
    ("services/storm-damage.webp", 1000, 75),
    ("gallery/completed-03.webp", 1000, 75),
    ("team/crew-at-work.webp", 1000, 75),
]


def compress(rel: str, max_w: int, q: int) -> None:
    src = IMG / rel
    if not src.exists():
        print("MISSING", rel)
        return
    before = src.stat().st_size
    tmp = src.with_suffix(".tmp.webp")
    cmd = [
        str(FFMPEG),
        "-y",
        "-i",
        str(src),
        "-vf",
        f"scale='min({max_w},iw)':-2",
        "-c:v",
        "libwebp",
        "-quality",
        str(q),
        "-compression_level",
        "6",
        str(tmp),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not tmp.exists():
        print("FAIL", rel, r.stderr[-400:])
        if tmp.exists():
            tmp.unlink()
        return
    after = tmp.stat().st_size
    if after >= before * 0.98:
        # keep original if not meaningfully smaller
        tmp.unlink()
        print(f"SKIP {rel}: {before/1024:.0f}KB (no gain)")
        return
    shutil.move(str(tmp), str(src))
    print(f"OK   {rel}: {before/1024:.0f}KB -> {after/1024:.0f}KB")


def main() -> None:
    if not FFMPEG.exists():
        raise SystemExit(f"ffmpeg not found: {FFMPEG}")
    for rel, w, q in JOBS:
        compress(rel, w, q)


if __name__ == "__main__":
    main()
