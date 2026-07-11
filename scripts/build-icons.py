#!/usr/bin/env python3
"""Generate favicons, PWA icons, and social marks from Roof Monsters brand assets."""

from __future__ import annotations

import base64
import json
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "assets" / "images" / "brand"
OUT = ROOT / "assets" / "icons"
THEME = "#1a1a1a"
GOLD = "#c9a227"

PNG_SIZES = (16, 32, 48, 57, 72, 76, 96, 120, 128, 144, 152, 167, 180, 192, 256, 384, 512)


def load_layers() -> tuple[Image.Image, Image.Image]:
    bg = Image.open(BRAND / "logo-bg.png").convert("RGBA")
    monster = Image.open(BRAND / "logo-monster.png").convert("RGBA")
    return bg, monster


def composite_badge(bg: Image.Image, monster: Image.Image, canvas: int, pad: float = 0.08) -> Image.Image:
    """Stack badge + monster like the site header, centered on a square canvas."""
    badge_ar = bg.width / bg.height
    inner = int(canvas * (1 - pad * 2))
    badge_h = inner
    badge_w = int(badge_h * badge_ar)
    if badge_w > inner:
        badge_w = inner
        badge_h = int(badge_w / badge_ar)

    badge = bg.resize((badge_w, badge_h), Image.Resampling.LANCZOS)

    mon_ar = monster.width / monster.height
    mon_h = int(badge_h * 0.72)
    mon_w = int(mon_h * mon_ar)
    if mon_w > badge_w:
        mon_w = badge_w
        mon_h = int(mon_w / mon_ar)
    mon = monster.resize((mon_w, mon_h), Image.Resampling.LANCZOS)

    # Dark header-like backdrop for legibility in browser chrome.
    out = Image.new("RGBA", (canvas, canvas), THEME)
    bx = (canvas - badge_w) // 2
    by = (canvas - badge_h) // 2
    out.alpha_composite(badge, (bx, by))

    mx = bx + (badge_w - mon_w) // 2
    my = by + int(badge_h * 0.06)
    out.alpha_composite(mon, (mx, my))
    return out


def save_png(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rgb = Image.new("RGBA", img.size, THEME)
    rgb.alpha_composite(img)
    rgb.save(path, format="PNG", optimize=True)


def save_ico(sizes: list[int], master: Image.Image, path: Path) -> None:
    frames = [master.resize((s, s), Image.Resampling.LANCZOS) for s in sizes]
    path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=frames[1:],
    )


def write_svg(path: Path, master: Image.Image) -> None:
    """Embed the composited logo raster so SVG favicons match the PNG set."""
    flat = Image.new("RGBA", master.size, THEME)
    flat.alpha_composite(master)
    buf = BytesIO()
    flat.save(buf, format="PNG", optimize=True)
    b64 = base64.standard_b64encode(buf.getvalue()).decode("ascii")
    path.write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="Roof Monsters">
  <image width="512" height="512" href="data:image/png;base64,{b64}"/>
</svg>
""",
        encoding="utf-8",
    )


def write_mask_svg(path: Path, master: Image.Image) -> None:
    """Safari pinned-tab mask from logo alpha silhouette."""
    size = 128
    small = master.resize((size, size), Image.Resampling.LANCZOS)
    alpha = small.split()[3]
    pixels = alpha.load()
    rects: list[str] = []
    for y in range(size):
        for x in range(size):
            if pixels[x, y] > 32:
                rects.append(f'<rect x="{x}" y="{y}" width="1" height="1"/>')
    path.write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">
  <g fill="#000">{"".join(rects)}</g>
</svg>
""",
        encoding="utf-8",
    )


def write_manifest() -> None:
    icons = []
    for size in (192, 512):
        icons.append(
            {
                "src": f"android-chrome-{size}x{size}.png",
                "sizes": f"{size}x{size}",
                "type": "image/png",
                "purpose": "any",
            }
        )
        icons.append(
            {
                "src": f"android-chrome-{size}x{size}.png",
                "sizes": f"{size}x{size}",
                "type": "image/png",
                "purpose": "maskable",
            }
        )
    payload = {
        "name": "Roof Monsters",
        "short_name": "Roof Monsters",
        "description": "Tampa Bay roofing — repair, replacement, and inspections since 1988.",
        "start_url": "../..",
        "scope": "../..",
        "display": "standalone",
        "background_color": THEME,
        "theme_color": THEME,
        "icons": icons,
    }
    (OUT / "site.webmanifest").write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )


def write_browserconfig() -> None:
    (OUT / "browserconfig.xml").write_text(
        """<?xml version="1.0" encoding="utf-8"?>
<browserconfig>
  <msapplication>
    <tile>
      <square70x70logo src="mstile-70x70.png"/>
      <square150x150logo src="mstile-150x150.png"/>
      <square310x310logo src="mstile-310x310.png"/>
      <wide310x150logo src="mstile-310x150.png"/>
      <TileColor>""" + THEME + """</TileColor>
    </tile>
  </msapplication>
</browserconfig>
""",
        encoding="utf-8",
    )


def main() -> None:
    bg, monster = load_layers()
    master = composite_badge(bg, monster, 512)

    OUT.mkdir(parents=True, exist_ok=True)

    named = {
        16: "favicon-16x16.png",
        32: "favicon-32x32.png",
        48: "favicon-48x48.png",
        57: "apple-touch-icon-57x57.png",
        72: "apple-touch-icon-72x72.png",
        76: "apple-touch-icon-76x76.png",
        96: "android-chrome-96x96.png",
        120: "apple-touch-icon-120x120.png",
        128: "android-chrome-128x128.png",
        144: "apple-touch-icon-144x144.png",
        152: "apple-touch-icon-152x152.png",
        167: "apple-touch-icon-167x167.png",
        180: "apple-touch-icon.png",
        192: "android-chrome-192x192.png",
        256: "android-chrome-256x256.png",
        384: "android-chrome-384x384.png",
        512: "android-chrome-512x512.png",
    }

    for size, filename in named.items():
        save_png(master.resize((size, size), Image.Resampling.LANCZOS), OUT / filename)
        print(f"wrote {filename}")

    # Windows tiles
    for size, name in (
        (70, "mstile-70x70.png"),
        (150, "mstile-150x150.png"),
        (310, "mstile-310x310.png"),
    ):
        save_png(master.resize((size, size), Image.Resampling.LANCZOS), OUT / name)
        print(f"wrote {name}")

    wide = Image.new("RGBA", (310, 150), THEME)
    icon = master.resize((120, 120), Image.Resampling.LANCZOS)
    wide.alpha_composite(icon, ((310 - 120) // 2, (150 - 120) // 2))
    save_png(wide, OUT / "mstile-310x150.png")
    print("wrote mstile-310x150.png")

    save_ico([16, 32, 48], master, OUT / "favicon.ico")
    save_ico([16, 32, 48], master, ROOT / "favicon.ico")
    print("wrote favicon.ico (root + assets/icons)")

    write_svg(OUT / "favicon.svg", master)
    write_mask_svg(OUT / "safari-pinned-tab.svg", master)
    write_manifest()
    write_browserconfig()
    print("wrote site.webmanifest, browserconfig.xml, svg icons")


if __name__ == "__main__":
    main()
