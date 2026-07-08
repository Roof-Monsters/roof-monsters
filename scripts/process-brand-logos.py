#!/usr/bin/env python3
"""Prepare Roof Monsters split brand assets (transparent BG + monster layer)."""

from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC_BG = ROOT / "RM-LogoBG.png"
SRC_MONSTER = ROOT / "RM-MonsterHouseLogo.png"
OUT_DIR = ROOT / "assets" / "images" / "brand"
WEBP_QUALITY = 92

# From logo-bg.png analysis — ROOF orange text top row / badge height
ROOF_LINE_RATIO = 0.7283
# From logo-monster.png — opaque feet row / image height (pre-crop)
FEET_ROW_RATIO = 0.8246


def flood_remove_white(path: Path) -> Image.Image:
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    pixels = img.load()
    visited: set[tuple[int, int]] = set()

    def is_background(x: int, y: int) -> bool:
        r, g, b, _a = pixels[x, y]
        return r >= 245 and g >= 245 and b >= 245

    seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    for sx, sy in seeds:
        queue: deque[tuple[int, int]] = deque([(sx, sy)])
        while queue:
            x, y = queue.popleft()
            if (x, y) in visited or x < 0 or x >= w or y < 0 or y >= h:
                continue
            if not is_background(x, y):
                continue
            visited.add((x, y))
            r, g, b, _a = pixels[x, y]
            pixels[x, y] = (r, g, b, 0)
            queue.extend([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])

    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    return img


def crop_opaque_bounds(img: Image.Image) -> Image.Image:
    arr = np.array(img.convert("RGBA"))
    alpha = arr[:, :, 3]
    rows = np.where(np.any(alpha > 20, axis=1))[0]
    cols = np.where(np.any(alpha > 20, axis=0))[0]
    if rows.size == 0 or cols.size == 0:
        return img
    return img.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))


def save_assets(img: Image.Image, stem: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    png_path = OUT_DIR / f"{stem}.png"
    webp_path = OUT_DIR / f"{stem}.webp"
    img.save(png_path, format="PNG", optimize=True)
    img.save(webp_path, format="WEBP", quality=WEBP_QUALITY, method=6, lossless=False)
    print(f"Wrote {png_path.name} ({png_path.stat().st_size // 1024} KB)")
    print(f"Wrote {webp_path.name} ({webp_path.stat().st_size // 1024} KB)")


def main() -> None:
    if not SRC_BG.exists():
        raise SystemExit(f"Missing {SRC_BG}")
    if not SRC_MONSTER.exists():
        raise SystemExit(f"Missing {SRC_MONSTER}")

    bg = flood_remove_white(SRC_BG)
    monster = crop_opaque_bounds(Image.open(SRC_MONSTER).convert("RGBA"))

    save_assets(bg, "logo-bg")
    save_assets(monster, "logo-monster")

    print(f"logo-bg size: {bg.size}")
    print(f"logo-monster size: {monster.size}")
    badge_ar = 640 / 736
    mon_w, mon_h = monster.size
    mon_ar = mon_w / mon_h
    top_margin = 0.02
    fit_h = ROOF_LINE_RATIO - top_margin
    fit_w = fit_h * mon_ar / badge_ar
    print(f"CSS: --rm-roof-line: {ROOF_LINE_RATIO * 100:.2f}%;")
    print(f"CSS: --rm-top-margin: {top_margin * 100:.0f}%;")
    print(f"CSS: --rm-monster-h: {fit_h * 100:.2f}%;")
    print(f"CSS: --rm-monster-w: {fit_w * 100:.2f}%;")
    print(f"CSS: --rm-monster-top: {(ROOF_LINE_RATIO - fit_h) * 100:.2f}%;")


if __name__ == "__main__":
    main()
