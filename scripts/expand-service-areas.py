#!/usr/bin/env python3
"""Add priority city entries to data/service-areas.json."""
from __future__ import annotations

import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "data" / "service-areas.json"
data = json.loads(p.read_text(encoding="utf-8"))

new_cities = [
    {
        "type": "city",
        "name": "Tarpon Springs, FL",
        "shortName": "Tarpon Springs",
        "slug": "roofing-company-tarpon-springs-florida",
        "county": "Pinellas County",
        "countySlug": "roofing-company-pinellas-county-florida",
        "blurb": "Tarpon Springs homeowners trust Roof Monsters for Atlas shingle installs, leak repair, and storm response along the northern Pinellas Gulf coast.",
        "localDetail": "A short drive from our Dunedin headquarters, Tarpon Springs projects get fast scheduling for waterfront and inland neighborhoods alike.",
        "nearbyCities": ["Palm Harbor", "Dunedin", "New Port Richey", "Safety Harbor"],
    },
    {
        "type": "city",
        "name": "Oldsmar, FL",
        "shortName": "Oldsmar",
        "slug": "roofing-company-oldsmar-florida",
        "county": "Pinellas County",
        "countySlug": "roofing-company-pinellas-county-florida",
        "blurb": "Oldsmar sits at the Pinellas–Hillsborough edge — Roof Monsters serves the city with full replacements, repairs, and free inspections from Dunedin.",
        "localDetail": "From East Lake corridors to residential subdivisions, Oldsmar is within our core Pinellas service territory with the same licensed crews used county-wide.",
        "nearbyCities": ["Safety Harbor", "Dunedin", "Tampa", "Palm Harbor"],
    },
    {
        "type": "city",
        "name": "Pinellas Park, FL",
        "shortName": "Pinellas Park",
        "slug": "roofing-company-pinellas-park-florida",
        "county": "Pinellas County",
        "countySlug": "roofing-company-pinellas-county-florida",
        "blurb": "Central Pinellas Park properties need roofing built for Florida storms — installations, repairs, and emergency tarping from Roof Monsters.",
        "localDetail": "Pinellas Park is a frequent project zone between Clearwater and St. Petersburg, covered under our full Pinellas County service area.",
        "nearbyCities": ["Largo", "St. Petersburg", "Seminole", "Clearwater"],
    },
    {
        "type": "city",
        "name": "Gulfport, FL",
        "shortName": "Gulfport",
        "slug": "roofing-company-gulfport-florida",
        "county": "Pinellas County",
        "countySlug": "roofing-company-pinellas-county-florida",
        "blurb": "Gulfport's bay-side homes need ventilation and materials suited to humidity and wind — Roof Monsters delivers licensed residential roofing nearby.",
        "localDetail": "Neighboring St. Petersburg, Gulfport is part of our complete Pinellas coverage with clear written estimates and Atlas installs.",
        "nearbyCities": ["St. Petersburg", "Pinellas Park", "Seminole", "Largo"],
    },
    {
        "type": "city",
        "name": "Port Richey, FL",
        "shortName": "Port Richey",
        "slug": "roofing-company-port-richey-florida",
        "county": "Pasco County",
        "countySlug": "roofing-company-pasco-county-florida",
        "blurb": "Port Richey Gulf-side roofs take a beating from sun and seasonal storms — Roof Monsters provides repair, replacement, and private-pay emergency response.",
        "localDetail": "Port Richey sits within our published Pasco County territory alongside New Port Richey and Holiday.",
        "nearbyCities": ["New Port Richey", "Holiday", "Trinity", "Tarpon Springs"],
    },
    {
        "type": "city",
        "name": "Holiday, FL",
        "shortName": "Holiday",
        "slug": "roofing-company-holiday-florida",
        "county": "Pasco County",
        "countySlug": "roofing-company-pasco-county-florida",
        "blurb": "Holiday homeowners call Roof Monsters for leak repair, Atlas replacements, and storm tarping across western Pasco.",
        "localDetail": "Holiday is a core Pasco market for our Tampa Bay crews — free inspections and clear written estimates.",
        "nearbyCities": ["New Port Richey", "Port Richey", "Trinity", "Tarpon Springs"],
    },
    {
        "type": "city",
        "name": "Trinity, FL",
        "shortName": "Trinity",
        "slug": "roofing-company-trinity-florida",
        "county": "Pasco County",
        "countySlug": "roofing-company-pasco-county-florida",
        "blurb": "Trinity's growing neighborhoods need reliable residential roofing — Roof Monsters installs Atlas systems and handles repairs across Pasco.",
        "localDetail": "Trinity projects are scheduled as part of our full Pasco County coverage from Tampa Bay operations.",
        "nearbyCities": ["New Port Richey", "Holiday", "Odessa", "Palm Harbor"],
    },
    {
        "type": "city",
        "name": "Wesley Chapel, FL",
        "shortName": "Wesley Chapel",
        "slug": "roofing-company-wesley-chapel-florida",
        "county": "Pasco County",
        "countySlug": "roofing-company-pasco-county-florida",
        "blurb": "Wesley Chapel growth corridors need roofing contractors who show up with clear scopes — Roof Monsters serves eastern Pasco with installs and repairs.",
        "localDetail": "From master-planned communities to established subdivisions, Wesley Chapel is within our published Pasco service area.",
        "nearbyCities": ["Land O' Lakes", "Zephyrhills", "Tampa", "New Port Richey"],
    },
    {
        "type": "city",
        "name": "Land O' Lakes, FL",
        "shortName": "Land O' Lakes",
        "slug": "roofing-company-land-o-lakes-florida",
        "county": "Pasco County",
        "countySlug": "roofing-company-pasco-county-florida",
        "blurb": "Land O' Lakes homeowners rely on Roof Monsters for Atlas shingle roofing, leak repair, and storm response in central Pasco.",
        "localDetail": "Land O' Lakes is a featured Pasco market with the same licensed crews and 15-year workmanship warranty used Tampa Bay–wide.",
        "nearbyCities": ["Wesley Chapel", "Odessa", "Tampa", "New Port Richey"],
    },
    {
        "type": "city",
        "name": "Spring Hill, FL",
        "shortName": "Spring Hill",
        "slug": "roofing-company-spring-hill-florida",
        "county": "Hernando County",
        "countySlug": "roofing-company-hernando-county-florida",
        "blurb": "Spring Hill is Hernando's largest residential market — Roof Monsters provides roof replacement, repair, and free inspections.",
        "localDetail": "We serve Spring Hill as part of full Hernando County coverage, not a limited map pin.",
        "nearbyCities": ["Brooksville", "Weeki Wachee", "Hudson", "New Port Richey"],
    },
    {
        "type": "city",
        "name": "Brooksville, FL",
        "shortName": "Brooksville",
        "slug": "roofing-company-brooksville-florida",
        "county": "Hernando County",
        "countySlug": "roofing-company-hernando-county-florida",
        "blurb": "Brooksville and surrounding Hernando communities get licensed roofing from Roof Monsters — installs, repairs, and storm response.",
        "localDetail": "County seat projects and rural Hernando properties are welcome; contact us to confirm scheduling.",
        "nearbyCities": ["Spring Hill", "Weeki Wachee", "Dade City", "Zephyrhills"],
    },
    {
        "type": "city",
        "name": "Brandon, FL",
        "shortName": "Brandon",
        "slug": "roofing-company-brandon-florida",
        "county": "Hillsborough County",
        "countySlug": "roofing-company-hillsborough-county-florida",
        "blurb": "Brandon is one of our most requested Hillsborough markets for roof replacement, repair, and free inspections.",
        "localDetail": "We serve Brandon as part of full Hillsborough County coverage alongside Tampa, Riverview, and Plant City.",
        "nearbyCities": ["Tampa", "Riverview", "Plant City", "Valrico"],
    },
    {
        "type": "city",
        "name": "Riverview, FL",
        "shortName": "Riverview",
        "slug": "roofing-company-riverview-florida",
        "county": "Hillsborough County",
        "countySlug": "roofing-company-hillsborough-county-florida",
        "blurb": "Riverview's growing south Hillsborough neighborhoods need durable Florida roofing — Atlas installs and repairs from Roof Monsters.",
        "localDetail": "Riverview projects are scheduled within our full Hillsborough County service territory.",
        "nearbyCities": ["Brandon", "Tampa", "Plant City", "Sun City Center"],
    },
    {
        "type": "city",
        "name": "Plant City, FL",
        "shortName": "Plant City",
        "slug": "roofing-company-plant-city-florida",
        "county": "Hillsborough County",
        "countySlug": "roofing-company-hillsborough-county-florida",
        "blurb": "Plant City properties across eastern Hillsborough get clear written estimates and licensed roofing from Roof Monsters.",
        "localDetail": "We serve Plant City as part of all-Hillsborough coverage — residential and light commercial.",
        "nearbyCities": ["Brandon", "Tampa", "Lakeland", "Riverview"],
    },
    {
        "type": "city",
        "name": "Bradenton, FL",
        "shortName": "Bradenton",
        "slug": "roofing-company-bradenton-florida",
        "county": "Manatee County",
        "countySlug": "roofing-company-manatee-county-florida",
        "blurb": "Bradenton Gulf Coast homes need roofing built for wind and humidity — Roof Monsters serves Manatee County with Atlas installs and repairs.",
        "localDetail": "Bradenton is a featured Manatee market within our published Tampa Bay five-county territory.",
        "nearbyCities": ["Palmetto", "Lakewood Ranch", "Sarasota", "Ellenton"],
    },
    {
        "type": "city",
        "name": "Palmetto, FL",
        "shortName": "Palmetto",
        "slug": "roofing-company-palmetto-florida",
        "county": "Manatee County",
        "countySlug": "roofing-company-manatee-county-florida",
        "blurb": "Palmetto homeowners call Roof Monsters for leak repair, storm response, and full roof replacement across northern Manatee.",
        "localDetail": "Palmetto sits within our full Manatee County coverage with licensed Florida crews.",
        "nearbyCities": ["Bradenton", "Ellenton", "Lakewood Ranch", "Ruskin"],
    },
    {
        "type": "city",
        "name": "Lakewood Ranch, FL",
        "shortName": "Lakewood Ranch",
        "slug": "roofing-company-lakewood-ranch-florida",
        "county": "Manatee County",
        "countySlug": "roofing-company-manatee-county-florida",
        "blurb": "Lakewood Ranch communities often need HOA-ready documentation and quality materials — Roof Monsters delivers Atlas roofing with clear scopes.",
        "localDetail": "Lakewood Ranch is a featured Manatee service zone; we also work throughout the county.",
        "nearbyCities": ["Bradenton", "Palmetto", "Sarasota", "Ellenton"],
    },
]

existing_slugs = {a["slug"] for a in new_cities}
cities = [a for a in data["areas"] if a.get("type") == "city" and a.get("slug") not in existing_slugs]
counties = [a for a in data["areas"] if a.get("type") == "county"]
data["areas"] = cities + new_cities + counties

feat = {
    "roofing-company-pinellas-county-florida": [
        {"name": "Dunedin", "slug": "roofing-company-dunedin-florida", "note": "Headquarters"},
        {"name": "Clearwater", "slug": "roofing-company-clearwater-florida"},
        {"name": "St. Petersburg", "slug": "roofing-company-st-petersburg-florida"},
        {"name": "Largo", "slug": "roofing-company-largo-florida"},
        {"name": "Palm Harbor", "slug": "roofing-company-palm-harbor-florida"},
        {"name": "Seminole", "slug": "roofing-company-seminole-florida"},
        {"name": "Safety Harbor", "slug": "roofing-company-safety-harbor-florida"},
        {"name": "Tarpon Springs", "slug": "roofing-company-tarpon-springs-florida"},
        {"name": "Oldsmar", "slug": "roofing-company-oldsmar-florida"},
        {"name": "Pinellas Park", "slug": "roofing-company-pinellas-park-florida"},
        {"name": "Gulfport", "slug": "roofing-company-gulfport-florida"},
    ],
    "roofing-company-pasco-county-florida": [
        {"name": "New Port Richey", "slug": "roofing-company-new-port-richey-florida"},
        {"name": "Port Richey", "slug": "roofing-company-port-richey-florida"},
        {"name": "Holiday", "slug": "roofing-company-holiday-florida"},
        {"name": "Trinity", "slug": "roofing-company-trinity-florida"},
        {"name": "Wesley Chapel", "slug": "roofing-company-wesley-chapel-florida"},
        {"name": "Land O' Lakes", "slug": "roofing-company-land-o-lakes-florida"},
    ],
    "roofing-company-hernando-county-florida": [
        {"name": "Spring Hill", "slug": "roofing-company-spring-hill-florida"},
        {"name": "Brooksville", "slug": "roofing-company-brooksville-florida"},
    ],
    "roofing-company-hillsborough-county-florida": [
        {"name": "Tampa", "slug": "roofing-company-tampa-florida"},
        {"name": "Brandon", "slug": "roofing-company-brandon-florida"},
        {"name": "Riverview", "slug": "roofing-company-riverview-florida"},
        {"name": "Plant City", "slug": "roofing-company-plant-city-florida"},
    ],
    "roofing-company-manatee-county-florida": [
        {"name": "Bradenton", "slug": "roofing-company-bradenton-florida"},
        {"name": "Palmetto", "slug": "roofing-company-palmetto-florida"},
        {"name": "Lakewood Ranch", "slug": "roofing-company-lakewood-ranch-florida"},
    ],
}

for a in data["areas"]:
    if a.get("slug") in feat:
        a["featuredCities"] = feat[a["slug"]]
        if a["slug"] == "roofing-company-pinellas-county-florida":
            a["additionalCommunities"] = ["Indian Rocks Beach", "Belleair", "Kenneth City"]
        if a["slug"] == "roofing-company-pasco-county-florida":
            a["additionalCommunities"] = ["Hudson", "Zephyrhills", "Dade City"]

p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("cities", sum(1 for a in data["areas"] if a["type"] == "city"))
print("total areas", len(data["areas"]))
