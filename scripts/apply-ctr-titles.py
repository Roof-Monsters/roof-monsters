"""Apply CTR-focused title/meta rewrites from GSC analysis (2026-08-03).

Targets high-impression / low-CTR URLs from GSC exports + live Performance UI.
Updates <title>, meta description, og/twitter title & description.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# page_key -> (title, description)
# Titles kept ~50-60 chars; descriptions ~140-155 with CTA + proof.
OVERRIDES: dict[str, tuple[str, str]] = {
    ".": (
        "Roof Monsters | Tampa Bay Roof Repair &amp; Replacement",
        "Family-owned since 1988. Roof repair, replacement &amp; Atlas shingles across Tampa Bay. 4.4★ Google reviews — free estimates: (727) 439-3869.",
    ),
    "testimonials": (
        "Roof Monsters Reviews (4.4★) | Real Tampa Bay Customers",
        "Read Roof Monsters reviews from Tampa Bay homeowners — 4.4★ from 30+ Google reviews. Roof repair, replacement &amp; storm response. Call (727) 439-3869.",
    ),
    "about-us": (
        "About Terrance McKeever &amp; Roof Monsters | Since 1988",
        "Meet Terrance McKeever Enterprises / Roof Monsters — family-owned Tampa Bay roofing since 1988. Dunedin HQ, licensed crews, free estimates: (727) 439-3869.",
    ),
    "services": (
        "Roofing Services Tampa Bay | Repair, Replace, Inspect",
        "Roof repair, full replacement, free inspections, storm response, gutters &amp; skylights. Licensed Roof Monsters crews — free estimate: (727) 439-3869.",
    ),
    "services/emergency-roof-repair": (
        "Emergency Roof Repair Tampa | 24/7 Tarping Response",
        "Need emergency roof repair in Tampa Bay? Same-day triage &amp; tarping when weather allows. Private-pay storm response — call Roof Monsters (727) 439-3869.",
    ),
    "services/tpo-roofing": (
        "TPO Roofing Tampa | Commercial Flat Roof Specialists",
        "TPO roofing for Tampa Bay commercial &amp; low-slope buildings. Reflective flat-roof systems, clear scopes, licensed crews. Call (727) 439-3869.",
    ),
    "services/roof-repair": (
        "Roof Repair Tampa Bay | Leaks, Shingles &amp; Storm Wear",
        "Fast roof repair for leaks, missing shingles &amp; storm wear across Tampa Bay. Clear written estimates from licensed Roof Monsters — (727) 439-3869.",
    ),
    "services/free-roof-inspections-and-consultations": (
        "Free Roof Inspection Tampa Bay | No-Cost Assessment",
        "Free roof inspections across Tampa Bay. Honest repair-or-replace guidance from licensed Roof Monsters crews — schedule now: (727) 439-3869.",
    ),
    "services/storm-damage-repair-specialists": (
        "Storm Damage Roof Repair Tampa Bay | Emergency Tarping",
        "24/7 storm damage roof repair in Tampa Bay. Emergency tarping and private-pay restoration from Roof Monsters licensed crews — (727) 439-3869.",
    ),
    "services/roof-replacement": (
        "Roof Replacement Tampa Bay | Atlas Shingles, Free Quote",
        "Full roof replacement across Tampa Bay with Atlas shingles, clear estimates &amp; 15-year workmanship warranty. Free quote: (727) 439-3869.",
    ),
    "contact-us": (
        "Contact Roof Monsters | Free Roofing Estimate Tampa Bay",
        "Request a free roofing estimate from Roof Monsters. Call (727) 439-3869. Serving Pasco, Pinellas, Hernando, Hillsborough &amp; Manatee, FL.",
    ),
    "what-is-tpo-roofing-and-why-its-perfect-for-florida-commercial-buildings": (
        "TPO Roofing in Tampa Bay | Florida Commercial Flat Roofs",
        "What is TPO roofing and when does it fit Tampa Bay commercial buildings? Reflective flat-roof systems from Roof Monsters — clear scopes, licensed crews.",
    ),
    "the-roof-monsters-way-what-sets-our-roofing-company-apart": (
        "Why Choose Roof Monsters | Tampa Bay Since 1988",
        "What sets Roof Monsters apart — family ownership since 1988, Atlas warranties, same-crew quality, and Tampa Bay local expertise. Call (727) 439-3869.",
    ),
    "special-offers": (
        "Roofing Special Offers Tampa Bay | Roof Monsters Deals",
        "Current Roof Monsters specials for Tampa Bay roof repair &amp; replacement. Ask about seasonal savings — free estimate: (727) 439-3869.",
    ),
}

# High-impression location pages from GSC (custom titles beat the generic template)
LOCATION_TITLE = "{short} Roofing | Repair &amp; Replacement — Roof Monsters"
LOCATION_META = (
    "Roof repair, replacement, free inspections &amp; storm damage in {name}. "
    "Family-owned Roof Monsters since 1988 — free estimate: (727) 439-3869."
)

# Cities that need shorter shortName handling for title length
LOCATION_SHORT: dict[str, str] = {
    "lakewood-ranch": "Lakewood Ranch",
    "land-o-lakes": "Land O' Lakes",
    "wesley-chapel": "Wesley Chapel",
    "oldsmar": "Oldsmar",
    "holiday": "Holiday",
    "palmetto": "Palmetto",
    "clearwater": "Clearwater",
    "palm-harbor": "Palm Harbor",
    "dunedin": "Dunedin",
    "tampa": "Tampa",
    "st-petersburg": "St. Petersburg",
    "new-port-richey": "New Port Richey",
    "spring-hill": "Spring Hill",
    "riverview": "Riverview",
    "trinity": "Trinity",
    "pinellas-park": "Pinellas Park",
    "brooksville": "Brooksville",
    "hillsborough-county": "Hillsborough Co.",
    "pinellas-county": "Pinellas County",
    "pasco-county": "Pasco County",
    "manatee-county": "Manatee County",
    "hernando-county": "Hernando County",
}


def page_key(path: Path) -> str:
    rel = path.relative_to(ROOT)
    if rel.name == "index.html":
        parts = rel.parts[:-1]
        return "/".join(parts) if parts else "."
    return str(rel).replace("\\", "/")


def set_meta(html: str, description: str) -> str:
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


def location_override(key: str) -> tuple[str, str] | None:
    prefix = "about-us/locations-we-serve/roofing-company-"
    if not key.startswith(prefix) or not key.endswith("-florida"):
        return None
    slug = key[len(prefix) : -len("-florida")]
    short = LOCATION_SHORT.get(
        slug,
        slug.replace("-", " ").title()
        .replace("O Lakes", "O' Lakes")
        .replace("St Petersburg", "St. Petersburg"),
    )
    name = f"{short}, FL" if "County" not in short and "Co." not in short else short
    if "County" in short or "Co." in short:
        name = short if short.endswith(", FL") else f"{short}, FL"
    title = LOCATION_TITLE.format(short=short)
    # Keep titles under ~60 visible chars
    if len(re.sub(r"&amp;", "&", title)) > 60:
        title = f"{short} Roofing | Free Estimates — Roof Monsters"
    meta = LOCATION_META.format(name=name)
    return title, meta


def main() -> None:
    changed: list[str] = []
    for path in sorted(ROOT.rglob("index.html")):
        if any(part.startswith(".") for part in path.parts):
            continue
        if path.parts[0] in {"scripts", "assets", "data", "partials", "gsc-audit", "docs"}:
            continue
        key = page_key(path)
        pair = OVERRIDES.get(key) or location_override(key)
        if not pair:
            continue
        title, description = pair
        text = path.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in text.lower() or "<title>Moved — Roof Monsters</title>" in text:
            continue
        if not re.search(r'<meta\s+name="description"', text, re.I):
            continue
        original = text
        text = set_title(text, title)
        text = set_meta(text, description)
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
            changed.append(key)
            safe_title = title.replace("★", "*").encode("ascii", "replace").decode("ascii")
            safe_meta = description.replace("★", "*").encode("ascii", "replace").decode("ascii")
            print(f"updated {key}")
            print(f"  title: {safe_title}")
            print(f"  meta:  {safe_meta[:90]}...")

    print(f"\nChanged {len(changed)} pages")
    out = ROOT / "docs" / "seo-ctr-update-2026-08-03-pages.txt"
    out.write_text("\n".join(changed) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
