"""Trim/expand meta descriptions and titles to Ahrefs-friendly lengths."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Ahrefs: too long >160, too short often <120 in practice for this crawl
META_MAX = 155
META_MIN = 120
TITLE_MAX = 60

# Explicit rewrites for pages flagged in the latest Ahrefs crawl
META_OVERRIDES: dict[str, str] = {
    ".": "Expert roof repair, replacement, and Atlas shingle roofing in Pasco, Pinellas & Hillsborough County, FL. Free estimates from Roof Monsters.",
    "services": "Roof installations, repairs, free inspections, gutters, skylights, and storm damage repair from Roof Monsters across Tampa Bay.",
    "contact-us": "Request a free roofing estimate from Roof Monsters. Call (727) 439-3869. Serving Pasco, Pinellas, Hernando, Hillsborough & Manatee, FL.",
    "testimonials": "Read Tampa Bay homeowner reviews of Roof Monsters — 5-star feedback on roof installs, repairs, and maintenance across three counties.",
    "about-us": "Family-owned Florida roofing experts since 1988. Meet Roof Monsters — mission, values, and the Dunedin team Tampa Bay trusts.",
    "services/storm-damage-repair-specialists": "24/7 storm damage roof repair in Tampa Bay. Emergency tarping and private-pay restoration from Roof Monsters' licensed crews.",
    "services/skylight-installation-and-repair": "Skylight installation and repair in Tampa Bay. Proper sealing and maintenance for natural light without leaks — Roof Monsters.",
    "category/roof-monsters-news": "Company updates, contractor tips, and Tampa Bay roofing insights from Roof Monsters — family-owned since 1988 in Dunedin, FL.",
    "category/roof-installation": "Roof replacement guides, material comparisons, and Florida installation best practices from Roof Monsters — Dunedin crews since 1988.",
    "category/roof-maintenance": "Seasonal roof maintenance, inspections, and preventative tips for Tampa Bay homeowners from Roof Monsters in Dunedin, FL.",
    "category/roof-repair": "Roof repair advice, warning signs, and when to call a licensed Tampa Bay contractor — practical tips from Roof Monsters.",
    "the-benefits-of-eco-friendly-roofing-solutions": "Energy-efficient and sustainable roofing for Florida homes — cool roofs, durable materials, and long-term savings from Roof Monsters.",
    "blog": "Expert roofing tips, storm prep guides, and Tampa Bay industry insights from Roof Monsters — family-owned in Dunedin since 1988.",
    "services/flat-roofing": "Flat and low-slope roofing for Tampa Bay homes and commercial buildings, including TPO options from Roof Monsters since 1988.",
    "services/metal-roofing": "Metal roofing installation and repair for Tampa Bay homes and buildings that need long-term wind and heat performance from Roof Monsters.",
    "services/residential-roofing": "Residential roofing for Tampa Bay homeowners — Atlas installs, repairs, inspections, and storm response from Roof Monsters since 1988.",
    "services/shingle-roofing": "Atlas Designer Shingle roofing with Scotchgard protection on qualifying Tampa Bay installs — installed by Roof Monsters since 1988.",
    "services/tile-roofing": "Tile roof repair and replacement for Tampa Bay properties that need durable, coastal-ready tile systems from Roof Monsters.",
    "services/tpo-roofing": "TPO roofing for Florida commercial and low-slope buildings — reflective, durable systems installed by Roof Monsters in Tampa Bay.",
    "the-importance-of-regular-roof-maintenance": "Why annual roof maintenance extends roof life in Florida heat and storms — catch small issues early with Roof Monsters in Tampa Bay.",
}

COUNTY_META = (
    "Roof repair, replacement, inspections, and storm damage services in {place}, FL. "
    "Dunedin-based Roof Monsters — family owned since 1988."
)
CITY_META = (
    "Roof repair, replacement, inspections, and storm damage in {place}, FL. "
    "Family-owned Roof Monsters serving Tampa Bay since 1988."
)

TITLE_OVERRIDES: dict[str, str] = {
    ".": "Roof Monsters | Roof Repair & Replacement in Tampa Bay, FL",
}


def page_key(path: Path) -> str:
    rel = path.relative_to(ROOT)
    if rel.name == "index.html":
        parts = rel.parts[:-1]
        return "/".join(parts) if parts else "."
    return str(rel).replace("\\", "/")


def location_meta(key: str) -> str | None:
    prefix = "about-us/locations-we-serve/roofing-company-"
    if not key.startswith(prefix) or not key.endswith("-florida"):
        return None
    slug = key[len(prefix) : -len("-florida")]
    place = slug.replace("-", " ").title().replace("O Lakes", "O' Lakes").replace("St Petersburg", "St. Petersburg")
    counties = {
        "pinellas-county",
        "pasco-county",
        "hernando-county",
        "manatee-county",
        "hillsborough-county",
    }
    template = COUNTY_META if slug in counties else CITY_META
    return template.format(place=place)


def trim_to(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    cut = text[: limit - 1]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut.rstrip(" ,;:-") + "."


def set_meta(html: str, description: str) -> str:
    description = description.replace('"', "&quot;")
    html = re.sub(
        r'(<meta\s+name="description"\s+content=")[^"]*(")',
        rf"\g<1>{description}\g<2>",
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(
        r'(<meta\s+property="og:description"\s+content=")[^"]*(")',
        rf"\g<1>{description}\g<2>",
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(
        r'(<meta\s+name="twitter:description"\s+content=")[^"]*(")',
        rf"\g<1>{description}\g<2>",
        html,
        count=1,
        flags=re.I,
    )
    return html


def set_title(html: str, title: str) -> str:
    html = re.sub(r"(<title>)[^<]*(</title>)", rf"\g<1>{title}\g<2>", html, count=1, flags=re.I)
    html = re.sub(
        r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
        rf"\g<1>{title}\g<2>",
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(
        r'(<meta\s+name="twitter:title"\s+content=")[^"]*(")',
        rf"\g<1>{title}\g<2>",
        html,
        count=1,
        flags=re.I,
    )
    return html


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("index.html")):
        if any(p.startswith(".") for p in path.parts):
            continue
        if path.parts[0] in {"scripts", "assets", "data", "partials"}:
            continue
        key = page_key(path)
        text = path.read_text(encoding="utf-8")
        original = text

        m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', text, re.I)
        if not m:
            continue
        current = m.group(1).replace("&quot;", '"')
        new_desc = META_OVERRIDES.get(key) or location_meta(key)
        if new_desc is None:
            if len(current) > META_MAX:
                new_desc = trim_to(current, META_MAX)
            elif len(current) < META_MIN and key.startswith("category/"):
                new_desc = current  # should be in overrides
            else:
                new_desc = current
        if len(new_desc) > META_MAX:
            new_desc = trim_to(new_desc, META_MAX)
        if new_desc != current:
            text = set_meta(text, new_desc)

        if key in TITLE_OVERRIDES:
            text = set_title(text, TITLE_OVERRIDES[key])
        else:
            tm = re.search(r"<title>([^<]*)</title>", text, re.I)
            if tm and len(tm.group(1)) > TITLE_MAX:
                text = set_title(text, trim_to(tm.group(1), TITLE_MAX).rstrip("."))

        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
            changed += 1
            print(f"updated {key} meta={len(new_desc)}")

    print(f"Changed {changed} pages")


if __name__ == "__main__":
    main()
