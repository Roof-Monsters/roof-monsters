#!/usr/bin/env python3
"""Convert raster images under assets/images to WebP and update site references."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "assets" / "images"
QUALITY = 85
RASTER_EXT = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}
TEXT_GLOBS = ("*.html", "*.css", "*.js", "*.md")


def convert_to_webp(path: Path) -> Path:
    out = path.with_suffix(".webp")
    with Image.open(path) as img:
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
        img.save(out, format="WEBP", quality=QUALITY, method=6)
    return out


def main() -> None:
    mappings: list[tuple[str, str]] = []

    for src in sorted(IMAGES.rglob("*")):
        if not src.is_file():
            continue
        if src.suffix.lower() not in {e.lower() for e in RASTER_EXT}:
            continue
        rel_old = src.relative_to(ROOT).as_posix()
        webp = convert_to_webp(src)
        rel_new = webp.relative_to(ROOT).as_posix()
        mappings.append((rel_old, rel_new))
        src.unlink()
        old_kb = 0  # already deleted
        new_kb = webp.stat().st_size / 1024
        print(f"OK {rel_old} -> {rel_new} ({new_kb:.0f} KB)")

    if not mappings:
        print("No raster images to convert.")
        return

    # longest paths first to avoid partial replacements
    mappings.sort(key=lambda pair: len(pair[0]), reverse=True)

    files_to_update: list[Path] = []
    for pattern in TEXT_GLOBS:
        files_to_update.extend(ROOT.glob(pattern))
        files_to_update.extend((ROOT / "assets" / "css").glob(pattern))

    seen: set[Path] = set()
    for file in files_to_update:
        if file in seen or not file.is_file():
            continue
        seen.add(file)
        text = file.read_text(encoding="utf-8")
        original = text
        for old, new in mappings:
            text = text.replace(old, new)
            # CSS paths use ../images/...
            old_css = old.replace("assets/images/", "../images/")
            new_css = new.replace("assets/images/", "../images/")
            text = text.replace(old_css, new_css)
        if text != original:
            file.write_text(text, encoding="utf-8")
            print(f"Updated refs: {file.relative_to(ROOT)}")

    print(f"Converted {len(mappings)} image(s) to WebP.")


if __name__ == "__main__":
    main()
