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
    ".": "Family-owned since 1988. Roof repair, replacement & Atlas shingles across Tampa Bay. 4.4★ Google reviews — free estimates: (727) 439-3869.",
    "services": "Roof repair, full replacement, free inspections, storm response, gutters & skylights. Licensed Roof Monsters crews — free estimate: (727) 439-3869.",
    "contact-us": "Request a free roofing estimate from Roof Monsters. Call (727) 439-3869. Serving Pasco, Pinellas, Hernando, Hillsborough & Manatee, FL.",
    "testimonials": "Read Roof Monsters reviews from Tampa Bay homeowners — 4.4★ from 30+ Google reviews. Roof repair, replacement & storm response. Call (727) 439-3869.",
    "about-us": "Meet Terrance McKeever Enterprises / Roof Monsters — family-owned Tampa Bay roofing since 1988. Dunedin HQ, licensed crews, free estimates: (727) 439-3869.",
    "services/storm-damage-repair-specialists": "24/7 storm damage roof repair in Tampa Bay. Emergency tarping and private-pay restoration from Roof Monsters licensed crews — (727) 439-3869.",
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
    "services/tpo-roofing": "TPO roofing for Tampa Bay commercial & low-slope buildings. Reflective flat-roof systems, clear scopes, licensed crews. Call (727) 439-3869.",
    "services/emergency-roof-repair": "Need emergency roof repair in Tampa Bay? Same-day triage & tarping when weather allows. Private-pay storm response — call Roof Monsters (727) 439-3869.",
    "services/roof-repair": "Fast roof repair for leaks, missing shingles & storm wear across Tampa Bay. Clear written estimates from licensed Roof Monsters — (727) 439-3869.",
    "services/free-roof-inspections-and-consultations": "Free roof inspections across Tampa Bay. Honest repair-or-replace guidance from licensed Roof Monsters crews — schedule now: (727) 439-3869.",
    "services/roof-replacement": "Full roof replacement across Tampa Bay with Atlas shingles, clear estimates & 15-year workmanship warranty. Free quote: (727) 439-3869.",
    "the-importance-of-regular-roof-maintenance": "Why annual roof maintenance extends roof life in Florida heat and storms — catch small issues early with Roof Monsters in Tampa Bay.",
    "special-offers": "Current Roof Monsters specials for Tampa Bay roof repair & replacement. Ask about seasonal savings — free estimate: (727) 439-3869.",
    "the-roof-monsters-way-what-sets-our-roofing-company-apart": "What sets Roof Monsters apart — family ownership since 1988, Atlas warranties, same-crew quality, and Tampa Bay local expertise. Call (727) 439-3869.",
    "what-is-tpo-roofing-and-why-its-perfect-for-florida-commercial-buildings": "What is TPO roofing and when does it fit Tampa Bay commercial buildings? Reflective flat-roof systems from Roof Monsters — clear scopes, licensed crews.",
}

COUNTY_META = (
    "Roof repair, replacement, free inspections & storm damage in {place}, FL. "
    "Family-owned Roof Monsters since 1988 — free estimate: (727) 439-3869."
)
CITY_META = (
    "Roof repair, replacement, free inspections & storm damage in {place}, FL. "
    "Family-owned Roof Monsters since 1988 — free estimate: (727) 439-3869."
)

TITLE_OVERRIDES: dict[str, str] = {
    ".": "Roof Monsters | Tampa Bay Roof Repair &amp; Replacement",
    "testimonials": "Roof Monsters Reviews (4.4★) | Real Tampa Bay Customers",
    "about-us": "About Terrance McKeever &amp; Roof Monsters | Since 1988",
    "services": "Roofing Services Tampa Bay | Repair, Replace, Inspect",
    "services/emergency-roof-repair": "Emergency Roof Repair Tampa | 24/7 Tarping Response",
    "services/tpo-roofing": "TPO Roofing Tampa | Commercial Flat Roof Specialists",
    "services/roof-repair": "Roof Repair Tampa Bay | Leaks, Shingles &amp; Storm Wear",
    "services/free-roof-inspections-and-consultations": "Free Roof Inspection Tampa Bay | No-Cost Assessment",
    "services/storm-damage-repair-specialists": "Storm Damage Roof Repair Tampa Bay | Emergency Tarping",
    "services/roof-replacement": "Roof Replacement Tampa Bay | Atlas Shingles, Free Quote",
    "contact-us": "Contact Roof Monsters | Free Roofing Estimate Tampa Bay",
    "special-offers": "Roofing Special Offers Tampa Bay | Roof Monsters Deals",
    "the-roof-monsters-way-what-sets-our-roofing-company-apart": "Why Choose Roof Monsters | Tampa Bay Since 1988",
    "what-is-tpo-roofing-and-why-its-perfect-for-florida-commercial-buildings": "TPO Roofing in Tampa Bay | Florida Commercial Flat Roofs",
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
