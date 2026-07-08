#!/usr/bin/env python3
"""Generate county-grouped Service Areas nav in header.html from data/service-areas.json."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "service-areas.json"
HEADER = ROOT / "header.html"

DESKTOP_START = "<!-- rm-nav-areas:desktop:start -->"
DESKTOP_END = "<!-- rm-nav-areas:desktop:end -->"
MOBILE_START = "<!-- rm-nav-areas:mobile:start -->"
MOBILE_END = "<!-- rm-nav-areas:mobile:end -->"


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def area_href(slug: str) -> str:
    return f"about-us/locations-we-serve/{slug}/"


def desktop_group(county: dict, cities: list[dict]) -> str:
    slug = county["slug"]
    name = county["shortName"]
    lines = [
        f'          <div class="nav-area-group">',
        f'            <button class="nav-area-group-btn" type="button" aria-expanded="false" aria-haspopup="true">',
        f"              {esc(name)}",
        f'              <i class="fa-solid fa-chevron-right" aria-hidden="true"></i>',
        f"            </button>",
        f'            <div class="nav-area-submenu" role="menu">',
        f'              <a href="{area_href(slug)}" role="menuitem">All {esc(name)}</a>',
    ]
    for city in cities:
        label = city["shortName"]
        if city.get("isHeadquarters"):
            label += " (HQ)"
        lines.append(
            f'              <a href="{area_href(city["slug"])}" role="menuitem">{esc(label)}</a>'
        )
    lines.extend(["            </div>", "          </div>"])
    return "\n".join(lines)


def desktop_county_link(county: dict) -> str:
    return (
        f'          <a href="{area_href(county["slug"])}" role="menuitem">'
        f'{esc(county["shortName"])}</a>'
    )


def mobile_group(county: dict, cities: list[dict]) -> str:
    slug = county["slug"]
    name = county["shortName"]
    group_id = slug.replace("roofing-company-", "").replace("-florida", "")
    lines = [
        f'      <button class="mobile-area-county-toggle" type="button" aria-expanded="false" '
        f'data-target="mobile-area-{group_id}">',
        f"        {esc(name)}",
        f'        <i class="fa-solid fa-chevron-down" aria-hidden="true"></i>',
        f"      </button>",
        f'      <div class="mobile-area-county-sub" id="mobile-area-{group_id}">',
        f'        <a href="{area_href(slug)}">All {esc(name)}</a>',
    ]
    for city in cities:
        label = city["shortName"]
        if city.get("isHeadquarters"):
            label += " (HQ)"
        lines.append(f'        <a href="{area_href(city["slug"])}">{esc(label)}</a>')
    lines.extend(["      </div>"])
    return "\n".join(lines)


def mobile_county_link(county: dict) -> str:
    return f'      <a href="{area_href(county["slug"])}">{esc(county["shortName"])}</a>'


def build_nav(config: dict) -> tuple[str, str]:
    counties = [a for a in config["areas"] if a["type"] == "county"]
    cities = [a for a in config["areas"] if a["type"] == "city"]

    # Pinellas first (HQ), then remaining counties in published order.
    county_order = ["Pinellas County", "Hillsborough County", "Pasco County", "Hernando County", "Manatee County"]
    counties_by_name = {c["name"].replace(", FL", ""): c for c in counties}
    ordered = [counties_by_name[n] for n in county_order if n in counties_by_name]

    desktop = [
        '          <a href="about-us/locations-we-serve/" role="menuitem">All Service Areas</a>',
    ]
    mobile = ['      <a href="about-us/locations-we-serve/">All Service Areas</a>']

    for county in ordered:
        county_key = county["name"].replace(", FL", "")
        county_cities = [c for c in cities if c.get("county") == county_key]
        county_cities.sort(key=lambda c: (not c.get("isHeadquarters", False), c["shortName"]))
        if county_cities:
            desktop.append(desktop_group(county, county_cities))
            mobile.append(mobile_group(county, county_cities))
        else:
            desktop.append(desktop_county_link(county))
            mobile.append(mobile_county_link(county))

    return "\n".join(desktop), "\n".join(mobile)


def patch_header() -> None:
    config = json.loads(DATA.read_text(encoding="utf-8"))
    desktop, mobile = build_nav(config)
    text = HEADER.read_text(encoding="utf-8")

    if DESKTOP_START not in text or DESKTOP_END not in text:
        raise SystemExit("header.html missing desktop nav markers")
    if MOBILE_START not in text or MOBILE_END not in text:
        raise SystemExit("header.html missing mobile nav markers")

    before_desktop, rest = text.split(DESKTOP_START, 1)
    _, after_desktop = rest.split(DESKTOP_END, 1)
    before_mobile, rest = after_desktop.split(MOBILE_START, 1)
    _, after_mobile = rest.split(MOBILE_END, 1)

    new_text = (
        before_desktop
        + DESKTOP_START
        + "\n"
        + desktop
        + "\n        "
        + DESKTOP_END
        + before_mobile
        + MOBILE_START
        + "\n"
        + mobile
        + "\n    "
        + MOBILE_END
        + after_mobile
    )
    HEADER.write_text(new_text, encoding="utf-8")
    print(f"Updated {HEADER}")


if __name__ == "__main__":
    patch_header()
