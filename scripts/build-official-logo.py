"""Compose a high-res official logo from logo-bg + logo-monster PNGs."""
from pathlib import Path
from PIL import Image

brand = Path(__file__).resolve().parents[1] / "assets" / "images" / "brand"
bg = Image.open(brand / "logo-bg.png").convert("RGBA")
mon = Image.open(brand / "logo-monster.png").convert("RGBA")
bw, bh = bg.size

# Match CSS overlay math used by .rm-brand-logo
roof_line = 0.7283
top_margin = 0.02
monster_h = (roof_line - top_margin) * bh
monster_w = monster_h * (495 / 641) * (736 / 640)
monster_top = roof_line * bh - monster_h
monster_left = (bw - monster_w) / 2

mon_resized = mon.resize(
    (max(1, round(monster_w)), max(1, round(monster_h))),
    Image.Resampling.LANCZOS,
)
composite = bg.copy()
composite.alpha_composite(mon_resized, (round(monster_left), round(monster_top)))

composite.save(brand / "logo-official.png", optimize=True)
composite.save(brand / "logo-official.webp", "WEBP", quality=92, method=6)
composite.save(brand / "logo.png", optimize=True)
composite.save(brand / "logo.webp", "WEBP", quality=92, method=6)

# Sharper webps for the preserved spinning assets
bg.save(brand / "logo-bg.webp", "WEBP", quality=92, method=6)
mon.save(brand / "logo-monster.webp", "WEBP", quality=92, method=6)

print("official", composite.size)
print("logo.webp", Image.open(brand / "logo.webp").size)
print("logo-bg.webp", Image.open(brand / "logo-bg.webp").size)
print("logo-monster.webp", Image.open(brand / "logo-monster.webp").size)
