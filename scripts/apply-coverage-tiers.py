#!/usr/bin/env python3
"""Stamp coverageTier onto service-areas.json from job-priorities.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AREAS = ROOT / "data" / "service-areas.json"
PRI = ROOT / "data" / "job-priorities.json"

COUNTY_TIER = {
    "Pinellas County": "core",
    "Pasco County": "nearby",
    "Hillsborough County": "nearby",
    "Hernando County": "extended",
    "Manatee County": "extended",
}


def main() -> None:
    pri = json.loads(PRI.read_text(encoding="utf-8"))
    data = json.loads(AREAS.read_text(encoding="utf-8"))
    city_to_tier = {}
    for tier, cfg in pri["coverageTiers"].items():
        for city in cfg["cities"]:
            city_to_tier[city.lower()] = tier
    data["coverageDisclaimer"] = (
        "Roof Monsters dispatches from Dunedin. Pinellas is the primary service area. "
        "We regularly take Tampa and west Pasco jobs. Extended cities (Land O' Lakes, "
        "Wesley Chapel, Brandon, Manatee, Hernando) are a fit mainly for larger replacements. "
        "We do not serve Jacksonville, Orlando, or Miami."
    )
    data["notServed"] = pri["notServed"]
    for area in data["areas"]:
        if area["type"] == "city":
            area["coverageTier"] = city_to_tier.get(area["shortName"].lower(), "extended")
        elif area["type"] == "county":
            key = area["name"].replace(", FL", "")
            area["coverageTier"] = COUNTY_TIER.get(key, "extended")
    AREAS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("updated coverage tiers")


if __name__ == "__main__":
    main()
