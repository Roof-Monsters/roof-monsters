"""Per-area media + expanded local copy for service-area landing pages.

Google does not require a fixed word count for indexing. These expansions
aim for unique, useful local content (~1,000–1,800+ words per page when
combined with shared sections) so city/county pages are not near-duplicates.
"""

from __future__ import annotations

# Stable gallery pool (files that exist under assets/images/gallery/)
GALLERY = [
    "atlas-install-01.webp",
    "atlas-install-02.webp",
    "completed-03.webp",
    "completed-05.webp",
    "completed-06.webp",
    "installation-01.webp",
    "installation-04.webp",
    "installation-07.webp",
    "pinellas-new-roof.webp",
    "project-02.webp",
    "project-09.webp",
    "quality-work.webp",
    "replacement-08.webp",
    "tampa-bay-project.webp",
]

# Preferred intro image per slug (falls back to hashed gallery pick)
INTRO_IMAGE: dict[str, str] = {
    "roofing-company-dunedin-florida": "pinellas-new-roof.webp",
    "roofing-company-clearwater-florida": "tampa-bay-project.webp",
    "roofing-company-st-petersburg-florida": "installation-04.webp",
    "roofing-company-largo-florida": "atlas-install-01.webp",
    "roofing-company-palm-harbor-florida": "atlas-install-02.webp",
    "roofing-company-seminole-florida": "replacement-08.webp",
    "roofing-company-safety-harbor-florida": "project-09.webp",
    "roofing-company-tampa-florida": "completed-06.webp",
    "roofing-company-new-port-richey-florida": "project-02.webp",
    "roofing-company-tarpon-springs-florida": "completed-05.webp",
    "roofing-company-oldsmar-florida": "installation-07.webp",
    "roofing-company-pinellas-park-florida": "installation-01.webp",
    "roofing-company-gulfport-florida": "quality-work.webp",
    "roofing-company-port-richey-florida": "completed-03.webp",
    "roofing-company-holiday-florida": "pinellas-new-roof.webp",
    "roofing-company-trinity-florida": "tampa-bay-project.webp",
    "roofing-company-wesley-chapel-florida": "atlas-install-01.webp",
    "roofing-company-land-o-lakes-florida": "atlas-install-02.webp",
    "roofing-company-spring-hill-florida": "replacement-08.webp",
    "roofing-company-brooksville-florida": "project-09.webp",
    "roofing-company-brandon-florida": "installation-04.webp",
    "roofing-company-riverview-florida": "completed-06.webp",
    "roofing-company-plant-city-florida": "project-02.webp",
    "roofing-company-bradenton-florida": "completed-05.webp",
    "roofing-company-palmetto-florida": "installation-07.webp",
    "roofing-company-lakewood-ranch-florida": "quality-work.webp",
    "roofing-company-pinellas-county-florida": "pinellas-new-roof.webp",
    "roofing-company-pasco-county-florida": "installation-01.webp",
    "roofing-company-hernando-county-florida": "completed-03.webp",
    "roofing-company-hillsborough-county-florida": "tampa-bay-project.webp",
    "roofing-company-manatee-county-florida": "atlas-install-02.webp",
}

SECONDARY_IMAGE: dict[str, str] = {
    "roofing-company-dunedin-florida": "atlas-install-02.webp",
    "roofing-company-clearwater-florida": "completed-06.webp",
    "roofing-company-st-petersburg-florida": "project-09.webp",
    "roofing-company-largo-florida": "project-02.webp",
    "roofing-company-palm-harbor-florida": "pinellas-new-roof.webp",
    "roofing-company-seminole-florida": "tampa-bay-project.webp",
    "roofing-company-safety-harbor-florida": "atlas-install-01.webp",
    "roofing-company-tampa-florida": "installation-07.webp",
    "roofing-company-new-port-richey-florida": "completed-05.webp",
    "roofing-company-tarpon-springs-florida": "quality-work.webp",
    "roofing-company-oldsmar-florida": "replacement-08.webp",
    "roofing-company-pinellas-park-florida": "project-09.webp",
    "roofing-company-gulfport-florida": "installation-04.webp",
    "roofing-company-port-richey-florida": "installation-01.webp",
    "roofing-company-holiday-florida": "completed-03.webp",
    "roofing-company-trinity-florida": "atlas-install-01.webp",
    "roofing-company-wesley-chapel-florida": "completed-06.webp",
    "roofing-company-land-o-lakes-florida": "installation-04.webp",
    "roofing-company-spring-hill-florida": "project-02.webp",
    "roofing-company-brooksville-florida": "tampa-bay-project.webp",
    "roofing-company-brandon-florida": "pinellas-new-roof.webp",
    "roofing-company-riverview-florida": "replacement-08.webp",
    "roofing-company-plant-city-florida": "atlas-install-02.webp",
    "roofing-company-bradenton-florida": "installation-01.webp",
    "roofing-company-palmetto-florida": "completed-03.webp",
    "roofing-company-lakewood-ranch-florida": "project-09.webp",
    "roofing-company-pinellas-county-florida": "atlas-install-01.webp",
    "roofing-company-pasco-county-florida": "installation-04.webp",
    "roofing-company-hernando-county-florida": "completed-05.webp",
    "roofing-company-hillsborough-county-florida": "quality-work.webp",
    "roofing-company-manatee-county-florida": "replacement-08.webp",
}


def _pick(slug: str, offset: int = 0) -> str:
    idx = (sum(ord(c) for c in slug) + offset * 7) % len(GALLERY)
    return GALLERY[idx]


def intro_image(slug: str) -> str:
    return INTRO_IMAGE.get(slug) or _pick(slug, 0)


def secondary_image(slug: str) -> str:
    primary = intro_image(slug)
    preferred = SECONDARY_IMAGE.get(slug) or _pick(slug, 3)
    if preferred == primary:
        preferred = _pick(slug, 5)
    if preferred == primary:
        preferred = GALLERY[(GALLERY.index(primary) + 1) % len(GALLERY)]
    return preferred


# County climate / building themes used when a city lacks a full custom guide
COUNTY_THEMES: dict[str, dict[str, str]] = {
    "Pinellas County": {
        "climate": (
            "Pinellas County roofs face Gulf humidity, salt air near the coast, intense summer UV, "
            "and frequent afternoon thunderstorms. Attic ventilation, algae-resistant shingles, and "
            "wind-rated fastening matter more here than in cooler inland markets."
        ),
        "jobs": (
            "Common Pinellas calls include Atlas Designer Shingle replacements, valley and flashing "
            "leak repairs, ridge ventilation upgrades, and private-pay emergency tarping after tropical weather."
        ),
        "permitting": (
            "Most full replacements in Pinellas require permits and final inspection. We coordinate "
            "permitting on qualifying projects and install to Florida Building Code and manufacturer specs."
        ),
    },
    "Pasco County": {
        "climate": (
            "Pasco County spans Gulf-side communities and inland growth corridors. Western Pasco sees "
            "stronger coastal wind exposure; eastern Pasco deals with heat, tree debris, and rapid "
            "new-construction roof aging under Florida sun."
        ),
        "jobs": (
            "Pasco homeowners often need storm-season inspections, missing-shingle repairs, full re-roofs "
            "on 15–25 year systems, and clear written estimates before HOA or sale deadlines."
        ),
        "permitting": (
            "We handle permitting for qualifying Pasco replacements and document scope so you know "
            "tear-off, underlayment, ventilation, and Atlas materials before work begins."
        ),
    },
    "Hillsborough County": {
        "climate": (
            "Hillsborough County mixes urban Tampa heat islands, suburban subdivisions, and inland "
            "agricultural edges. Roofs here fail from UV, wind-driven rain, and deferred ventilation "
            "as often as from a single storm event."
        ),
        "jobs": (
            "Typical Hillsborough work includes residential Atlas installs, commercial low-slope repairs, "
            "leak tracing at chimneys and skylights, and phased replacements around occupied homes."
        ),
        "permitting": (
            "Hillsborough permitting and inspection timelines vary by jurisdiction. We build schedule "
            "buffers into written estimates and keep you updated from tear-off through final walkthrough."
        ),
    },
    "Hernando County": {
        "climate": (
            "Hernando County roofs see Florida heat, seasonal storms, and tree cover that traps debris "
            "in valleys. Older subdivisions and rural properties often need honest repair-vs-replace guidance."
        ),
        "jobs": (
            "Spring Hill and Brooksville calls frequently involve leak repair, ventilation corrections, "
            "Atlas replacements, and free inspections before listing a home."
        ),
        "permitting": (
            "Qualifying Hernando replacements include permit coordination and Florida-code fastening. "
            "We explain decking repairs if soft spots appear during tear-off."
        ),
    },
    "Manatee County": {
        "climate": (
            "Manatee County Gulf and inland homes deal with humidity, wind exposure near the bay, and "
            "HOA communities that expect clean job sites and documented materials."
        ),
        "jobs": (
            "Bradenton, Palmetto, and Lakewood Ranch projects often include Atlas shingle installs, "
            "storm repairs, and maintenance inspections before hurricane season."
        ),
        "permitting": (
            "We pull permits on qualifying Manatee replacements and review Atlas manufacturer paperwork "
            "plus our 15-year workmanship warranty on qualifying installation labor."
        ),
    },
}


# Optional long-form hooks keyed by slug (merged with generated sections)
AREA_GUIDES: dict[str, dict] = {
    "roofing-company-dunedin-florida": {
        "headline": "Dunedin Roofing From Our Home Base Since 1988",
        "sections": [
            (
                "Why Dunedin Roofs Need Local Attention",
                "Dunedin sits on the Gulf side of Pinellas County, where salt air, bay humidity, and "
                "mature tree canopies accelerate shingle wear. Waterfront and downtown properties often "
                "need careful flashing at chimneys, skylights, and wall transitions. Inland Dunedin "
                "neighborhoods see the same Florida UV and afternoon storms that shorten underlayment "
                "life when ventilation is weak. Because Roof Monsters is headquartered here at "
                "1391 Robin Hood Ln, crews know local roof ages, HOA documentation habits, and which "
                "Atlas profiles hold up on Gulf-facing planes.",
            ),
            (
                "Neighborhoods and Property Types We Serve",
                "We regularly work across downtown Dunedin, waterfront corridors, HOA communities, and "
                "commercial buildings along US-19. Projects range from targeted leak repairs on older "
                "bungalows to full Atlas Designer Shingle replacements on larger residential roofs. "
                "Property managers and HOA boards appreciate written scopes, photo documentation, and "
                "crews who protect landscaping during tear-off. If you are buying or selling in Dunedin, "
                "a free inspection helps you understand near-term repair needs versus a planned re-roof.",
            ),
            (
                "Storm Season and Private-Pay Emergency Response",
                "When tropical weather opens a roof or drives water at valleys, call (727) 439-3869. "
                "We prioritize active leaks with tarping and dry-in, then schedule permanent repairs with "
                "clear private-pay estimates. We do not manage insurance claims or adjuster meetings — "
                "we focus on licensed emergency response and lasting repairs you can understand upfront.",
            ),
            (
                "Materials, Warranties, and What to Expect",
                "On qualifying steep-slope projects we install Atlas Designer Shingles, including "
                "Scotchgard™ protection on qualifying products. Manufacturer coverage follows Atlas terms; "
                "our 15-year workmanship warranty covers installation labor on qualifying jobs. Licenses "
                "CCC1335398, CCC052490, and CBC015719 apply. Most Dunedin work still comes from neighbors "
                "who recommend us — referrals remain our primary lead source.",
            ),
        ],
        "signs": [
            "Curling or missing shingles after Gulf wind events",
            "Black algae streaks on north-facing planes",
            "Ceiling stains after afternoon thunderstorms",
            "Hot upstairs rooms that suggest weak attic ventilation",
            "A roof past 15–20 years with repeated patch history",
        ],
        "faqs": [
            (
                "How quickly can you schedule a Dunedin roof inspection?",
                "Dunedin is our headquarters city, so inspections and estimates often schedule within a few business days. Active leaks are prioritized for emergency response.",
            ),
            (
                "Do you work with Dunedin HOAs?",
                "Yes. We document materials and colors and help select Atlas profiles that meet many HOA guidelines when applicable.",
            ),
            (
                "Is Dunedin your only service area?",
                "No — Dunedin is home base. We serve all of Pinellas, Pasco, Hernando, Hillsborough, and Manatee County.",
            ),
        ],
    },
    "roofing-company-clearwater-florida": {
        "headline": "Clearwater Roofing for Beachside and Inland Homes",
        "sections": [
            (
                "Beach Wind vs. Inland Heat",
                "Clearwater Beach and Island Estates see stronger wind and salt exposure than Countryside "
                "or central Clearwater subdivisions. We match fastening patterns, underlayment choices, "
                "and ventilation details to each microclimate instead of using a one-size-fits-all scope. "
                "Inland Clearwater roofs still face intense UV and afternoon storms that dry out sealant "
                "at pipe boots and wall flashings.",
            ),
            (
                "Where We Work in Clearwater",
                "Roof Monsters serves Clearwater Beach, Island Estates, Countryside, and central Clearwater "
                "as part of full Pinellas County coverage from our Dunedin headquarters. Residential "
                "replacements, leak repairs, free inspections, and private-pay storm response are all "
                "available. Commercial and multi-unit properties can be scoped with phased scheduling "
                "when access or tenant disruption matters.",
            ),
            (
                "Common Clearwater Roof Problems",
                "Lifted tabs after tropical systems, algae staining, clogged valleys under oak canopy, "
                "and failed chimney flashings show up often. We photograph conditions, explain repair "
                "versus replacement honestly, and provide line-item written estimates before work begins.",
            ),
            (
                "Atlas Installs and Local Accountability",
                "Qualifying Clearwater re-roofs use Atlas Designer Shingles with manufacturer-backed "
                "protection per Atlas terms, plus our 15-year workmanship warranty on qualifying labor. "
                "You deal with a family-owned Florida contractor — not a national call center — with "
                "licenses CCC1335398, CCC052490, and CBC015719.",
            ),
        ],
        "signs": [
            "Wind-lifted shingles on beachside elevations",
            "Salt and algae staining on coastal exposures",
            "Leaks at skylights or chimney flashings",
            "Granule loss heavy enough to expose shingle mat",
            "HOA notice requiring approved roof materials",
        ],
        "faqs": [
            (
                "Do you serve Clearwater Beach?",
                "Yes — beachside and inland Clearwater are within our Pinellas service territory.",
            ),
            (
                "Can you match Atlas colors for my HOA?",
                "We help select Atlas profiles and colors that suit many Clearwater HOA requirements when applicable.",
            ),
            (
                "How far is Clearwater from your shop?",
                "We dispatch from Dunedin — a short Pinellas drive for inspections, repairs, and replacements.",
            ),
        ],
    },
    "roofing-company-st-petersburg-florida": {
        "headline": "St. Petersburg Roofing for Historic and Modern Homes",
        "sections": [
            (
                "Bay Humidity and Mixed Housing Stock",
                "St. Petersburg mixes older districts, bungalows, and newer subdivisions. Bay humidity "
                "pushes moisture into attics when soffit and ridge ventilation are unbalanced. Historic "
                "homes may need careful flashing and decking evaluation; newer builds still fail early "
                "when underlayment or fastening was rushed. We inspect both the roof plane and attic "
                "conditions before recommending repair or full replacement.",
            ),
            (
                "Neighborhoods Across St. Pete",
                "Roof Monsters provides installation, repair, inspections, and storm support throughout "
                "St. Petersburg as part of complete Pinellas County coverage. Nearby Gulfport, Pinellas "
                "Park, Largo, and Seminole are also within our published territory. Most residential "
                "work still arrives through neighbor referrals.",
            ),
            (
                "After Storms in St. Petersburg",
                "When wind opens a roof or drives rain at valleys, we tarp, document damage for your "
                "records, and complete permanent private-pay repairs with clear written estimates. We "
                "do not coordinate insurance claims — we focus on protecting the home and finishing "
                "licensed work to Florida code.",
            ),
            (
                "What a Clear Estimate Includes",
                "Your written estimate covers tear-off, materials, labor, disposal, and noted decking "
                "or ventilation items. Atlas Designer Shingles are specified on qualifying steep-slope "
                "projects. Call (727) 439-3869 or email info@roofmonsters.co to schedule.",
            ),
        ],
        "signs": [
            "Musty attic odor near the bay",
            "Repeated leaks in different roof planes",
            "Soft decking or daylight in the attic",
            "Storm-missing shingles after tropical weather",
            "Roof age past 20 years with patchwork repairs",
        ],
        "faqs": [
            (
                "Do you work on older St. Pete homes?",
                "Yes — we evaluate decking, flashing, and ventilation carefully on older housing stock before scoping work.",
            ),
            (
                "Can you repair without a full replacement?",
                "Often yes when damage is localized and the system has remaining life. We document tradeoffs in writing.",
            ),
            (
                "Do you serve downtown and south St. Pete?",
                "Yes — St. Petersburg is covered under our full Pinellas County service area.",
            ),
        ],
    },
    "roofing-company-tampa-florida": {
        "headline": "Tampa Roofing Across Hillsborough County",
        "sections": [
            (
                "Urban Heat and Storm Wear",
                "Tampa roofs deal with heat-island temperatures, wind-driven rain, and a mix of steep "
                "shingle and low-slope commercial systems. South Tampa bungalows, Westshore commercial "
                "properties, and suburban neighborhoods age differently — we scope each property type "
                "with photos and a written line-item estimate.",
            ),
            (
                "Full Hillsborough Coverage",
                "We serve Tampa as part of all-Hillsborough coverage — not a narrow radius map pin. "
                "Brandon, Riverview, Plant City, and surrounding communities are included. Scheduling "
                "from our Dunedin headquarters keeps Pinellas and Hillsborough within practical reach "
                "for inspections and storm response.",
            ),
            (
                "Residential and Light Commercial",
                "Family homes, multi-unit buildings, and light commercial roofs can be phased around "
                "occupancy. Atlas materials apply on qualifying steep-slope work; flat and TPO systems "
                "are evaluated separately when low-slope decks are involved.",
            ),
            (
                "Licenses, Warranties, and Referrals",
                "Licenses CCC1335398, CCC052490, and CBC015719. Fifteen-year workmanship warranty on "
                "qualifying installation labor. Atlas manufacturer coverage per Atlas terms. Most Tampa "
                "Bay work still comes from neighbors who recommend us.",
            ),
        ],
        "signs": [
            "Ceiling stains after heavy Tampa thunderstorms",
            "Commercial membrane seams lifting in heat",
            "Missing shingles after tropical systems",
            "High cooling bills with a hot attic",
            "Buyer or insurer requesting a roof condition review",
        ],
        "faqs": [
            (
                "Do you only serve South Tampa?",
                "No — we serve Tampa and all of Hillsborough County, including Brandon, Riverview, and Plant City.",
            ),
            (
                "Can you work around business hours?",
                "Often yes for commercial and multi-unit properties — ask about phased scheduling during your estimate.",
            ),
            (
                "Do you handle insurance claims?",
                "No. We provide private-pay emergency response and repairs with clear written estimates.",
            ),
        ],
    },
    "roofing-company-new-port-richey-florida": {
        "headline": "New Port Richey Roofing on Pasco’s Gulf Side",
        "sections": [
            (
                "Gulf-Side Wear in Western Pasco",
                "New Port Richey roofs take years of sun, seasonal storms, and Gulf-influenced humidity. "
                "Older shingle systems often show granule loss, lifted tabs, and valley leaks before "
                "homeowners expect a full replacement. We help you compare spot repair versus re-roof "
                "with photos and a clear written estimate — no pressure to replace when a lasting repair "
                "still makes sense.",
            ),
            (
                "Local Service From Tampa Bay Operations",
                "New Port Richey sits within our published Pasco County service area alongside Port "
                "Richey, Holiday, and Trinity. Crews schedule from our Dunedin headquarters with the "
                "same licensed standards used across Pinellas and Hillsborough. Free inspections are "
                "available for qualifying residential and commercial inquiries.",
            ),
            (
                "Storm Response Without Claim Hype",
                "After tropical weather, we tarp active openings, document conditions for your records, "
                "and complete permanent private-pay repairs. We do not promise claim maximization or "
                "adjuster coordination — just licensed emergency response and honest scopes.",
            ),
            (
                "Atlas Materials and Workmanship Warranty",
                "Qualifying steep-slope replacements use Atlas Designer Shingles. Manufacturer warranties "
                "follow Atlas terms; our 15-year workmanship warranty covers qualifying installation labor. "
                "Call (727) 439-3869 to schedule an inspection in New Port Richey.",
            ),
        ],
        "signs": [
            "Missing shingles after Gulf wind events",
            "Recurring leaks at valleys or pipe boots",
            "Heavy granule piles in gutters",
            "Soft spots when walking the roof",
            "Roof age past 15–20 years with prior patches",
        ],
        "faqs": [
            (
                "Is New Port Richey in your service area?",
                "Yes — New Port Richey is part of our full Pasco County coverage.",
            ),
            (
                "How fast can you tarp after a storm?",
                "Active leaks are prioritized. Call (727) 439-3869 for emergency response.",
            ),
            (
                "Do you serve nearby Port Richey and Holiday?",
                "Yes — those communities are also within our Pasco County territory.",
            ),
        ],
    },
    "roofing-company-palm-harbor-florida": {
        "headline": "Palm Harbor Roofing for Waterfront and Golf Communities",
        "sections": [
            (
                "Coastal Wind and HOA Expectations",
                "Palm Harbor waterfront and golf-course communities need wind-aware fastening and clean "
                "job sites. HOAs often want documented materials and colors before approval. We help "
                "select Atlas profiles that fit many community guidelines and install to Florida code "
                "and manufacturer specifications on qualifying projects.",
            ),
            (
                "Minutes From Dunedin Headquarters",
                "Palm Harbor is one of our most active Pinellas markets because it is a short drive from "
                "headquarters. That proximity means faster inspections, easier follow-up, and crews who "
                "already know common roof ages across local subdivisions.",
            ),
            (
                "Repairs, Replacements, and Ventilation",
                "Leak repairs at flashings and valleys, full Atlas replacements, and attic ventilation "
                "upgrades are common Palm Harbor requests. Poor ventilation shortens shingle life in "
                "Florida heat — we check ridge and soffit balance during inspections.",
            ),
            (
                "Clear Pricing and Referral Trust",
                "You receive a written estimate before work starts. Most Palm Harbor projects still come "
                "from neighbors who recommend us. Licenses CCC1335398, CCC052490, CBC015719.",
            ),
        ],
        "signs": [
            "Wind damage on waterfront elevations",
            "HOA letter about roof condition or materials",
            "Algae streaks and granule loss",
            "Leaks after wind-driven rain",
            "Hot upstairs rooms in summer",
        ],
        "faqs": [
            (
                "Do you work in Palm Harbor HOAs?",
                "Yes — we document materials and help with Atlas color/profile selection when HOAs require it.",
            ),
            (
                "How close are you to Palm Harbor?",
                "Our Dunedin headquarters is a short drive away, which helps with scheduling and follow-up.",
            ),
            (
                "Can you inspect before I buy a Palm Harbor home?",
                "Yes — free inspections for qualifying inquiries help buyers understand near-term roof needs.",
            ),
        ],
    },
    "roofing-company-wesley-chapel-florida": {
        "headline": "Wesley Chapel Roofing in Eastern Pasco Growth Corridors",
        "sections": [
            (
                "New Construction Aging Under Florida Sun",
                "Wesley Chapel’s master-planned communities and newer subdivisions still need Florida-ready "
                "roofing. Builder-grade systems can show early wear from UV, storms, and ventilation gaps. "
                "We inspect honestly — repair when it lasts, replace when the system is past reliable service.",
            ),
            (
                "Eastern Pasco Coverage",
                "Wesley Chapel is within our published Pasco County service area with Land O’ Lakes, "
                "Zephyrhills-adjacent communities, and western Pasco Gulf towns. Scheduling comes from "
                "Tampa Bay operations based in Dunedin with licensed Florida crews.",
            ),
            (
                "What Homeowners Ask For",
                "Full Atlas replacements, leak repairs before listing, free inspections for buyers, and "
                "storm tarping after tropical weather. Written estimates explain materials, labor, and "
                "warranty coverage before you commit.",
            ),
            (
                "Family-Owned Accountability",
                "Roof Monsters has served Tampa Bay since 1988. We are not a storm-chasing pop-up crew. "
                "Referrals drive most of our work, and we stand behind qualifying installs with a "
                "15-year workmanship warranty.",
            ),
        ],
        "signs": [
            "Early shingle wear on newer homes",
            "Leaks at poorly flashed penetrations",
            "Storm damage after seasonal weather",
            "HOA architectural review requirements",
            "Buyer inspection flags on the roof",
        ],
        "faqs": [
            (
                "Do you serve all of Wesley Chapel?",
                "Yes — Wesley Chapel is included in our full Pasco County coverage.",
            ),
            (
                "Can you meet HOA documentation needs?",
                "We provide material details and written scopes that many HOAs require for approval.",
            ),
            (
                "Are estimates free in Wesley Chapel?",
                "Inspections and estimates are free for qualifying residential and commercial inquiries.",
            ),
        ],
    },
    "roofing-company-bradenton-florida": {
        "headline": "Bradenton Roofing for Manatee County Gulf Coast Homes",
        "sections": [
            (
                "Wind, Humidity, and Gulf Exposure",
                "Bradenton homes near the Gulf and inland Manatee neighborhoods need materials and "
                "fastening suited to Florida wind zones and humidity. We evaluate steep-slope Atlas "
                "systems and repair options with the same care we bring to Pinellas projects.",
            ),
            (
                "Manatee County Service",
                "Bradenton is a featured Manatee market within our five-county Tampa Bay territory "
                "alongside Palmetto and Lakewood Ranch. Call to confirm timing for your neighborhood — "
                "we schedule from Dunedin with licensed crews CCC1335398, CCC052490, CBC015719.",
            ),
            (
                "Repairs Before Hurricane Season",
                "Pre-season inspections catch lifted tabs, dried flashing sealant, and valley debris "
                "before the next tropical system. Emergency tarping is available for active openings, "
                "followed by permanent private-pay repairs.",
            ),
            (
                "Clear Scopes and Atlas Options",
                "Written estimates list tear-off, underlayment, ventilation, and Atlas materials on "
                "qualifying projects. Manufacturer warranties follow Atlas terms; our workmanship "
                "warranty covers qualifying installation labor for 15 years.",
            ),
        ],
        "signs": [
            "Coastal wind damage on exposed elevations",
            "Humidity-driven attic moisture",
            "Leaks at wall and chimney flashings",
            "Aging shingles past 15–20 years",
            "Storm openings needing temporary dry-in",
        ],
        "faqs": [
            (
                "Is Bradenton in your service area?",
                "Yes — Bradenton is part of our Manatee County coverage within Tampa Bay.",
            ),
            (
                "Do you serve Lakewood Ranch as well?",
                "Yes — Lakewood Ranch and Palmetto are also within Manatee County coverage.",
            ),
            (
                "Do you work insurance claims?",
                "No. We provide private-pay emergency response and repairs with clear written estimates.",
            ),
        ],
    },
    "roofing-company-pinellas-county-florida": {
        "headline": "Pinellas County Roofing — Full County, Not a Map Pin",
        "sections": [
            (
                "County-Wide Coverage From Dunedin",
                "Roof Monsters serves all Pinellas municipalities and unincorporated areas from our "
                "Dunedin headquarters. City pages highlight frequent project zones — they are not "
                "service limits. Clearwater, St. Petersburg, Largo, Palm Harbor, Seminole, Safety Harbor, "
                "Tarpon Springs, Oldsmar, Pinellas Park, Gulfport, and more are included.",
            ),
            (
                "Coastal and Inland Pinellas Conditions",
                "Gulf-facing roofs need wind and salt awareness; inland Pinellas still battles UV, "
                "algae, and thunderstorms. We specify Atlas Designer Shingles on qualifying steep-slope "
                "projects and correct ventilation when attic heat is cooking the underside of the roof.",
            ),
            (
                "Services Across the County",
                "Roof replacement, repair, leak tracing, free inspections, storm tarping, residential "
                "and commercial work, gutters, and skylights are available through our service pages. "
                "Most Pinellas work still comes from neighbor referrals.",
            ),
            (
                "Licenses and Warranties",
                "Roofing CCC1335398, CCC052490 and building CBC015719. Fifteen-year workmanship warranty "
                "on qualifying installation labor. Atlas manufacturer coverage per Atlas terms.",
            ),
        ],
        "signs": [
            "County-wide storm damage after tropical weather",
            "Aging roofs across HOA communities",
            "Recurring leaks in older Pinellas housing stock",
            "Ventilation problems in hot upstairs rooms",
            "Need for permitted full replacements",
        ],
        "faqs": [
            (
                "Do you really serve all of Pinellas County?",
                "Yes — full county coverage, including cities highlighted on individual landing pages.",
            ),
            (
                "Where are you based?",
                "Dunedin, Florida — 1391 Robin Hood Ln — inside Pinellas County.",
            ),
            (
                "How do I pick a city page vs. this county page?",
                "City pages target local searches; this county page confirms whole-county service and links featured communities.",
            ),
        ],
    },
}


def guide_for(area: dict) -> dict:
    """Return merged guide content for an area (custom + generated)."""
    slug = area["slug"]
    short = area["shortName"]
    name = area["name"]
    county = area.get("county") or short
    theme = COUNTY_THEMES.get(county, COUNTY_THEMES["Pinellas County"])
    custom = AREA_GUIDES.get(slug, {})

    nearby = area.get("nearbyCities") or [c["name"] for c in area.get("featuredCities", [])[:6]]
    nearby_txt = ", ".join(nearby[:6]) if nearby else "neighboring Tampa Bay communities"

    generated_sections = [
        (
            f"Roofing Conditions in {short}",
            f"{area.get('blurb', '')} {area.get('localDetail', '')} {theme['climate']} "
            f"Property owners in {name} benefit from a Dunedin-based contractor who understands "
            f"Gulf Coast weather instead of a one-size national playbook. Afternoon storms, "
            f"prolonged UV exposure, and humidity cycles all stress underlayment, flashing sealants, "
            f"and attic ventilation — which is why a walk-the-roof inspection beats guessing from "
            f"a ceiling stain alone.",
        ),
        (
            f"Services Homeowners in {short} Request Most",
            f"{theme['jobs']} From {short}, we also regularly work in and around {nearby_txt}. "
            f"Every qualifying project starts with a free inspection when applicable and a written "
            f"estimate that explains materials, labor, and warranty coverage before work begins. "
            f"Typical scopes include Atlas Designer Shingle replacements on qualifying steep-slope "
            f"homes, targeted leak repairs at valleys and penetrations, ridge or soffit ventilation "
            f"corrections, and private-pay emergency tarping when storms open a roof.",
        ),
        (
            "How Our Process Works Locally",
            f"We walk the roof and attic when accessible, photograph problem areas, and review "
            f"repair versus replacement options in plain language. {theme['permitting']} "
            f"Crews protect landscaping, complete magnetic nail sweeps on qualifying tear-offs, "
            f"and walk the finished job with you before we leave the site. If decking repairs are "
            f"needed after tear-off, we document them and confirm pricing before continuing — "
            f"no surprise change orders mid-project.",
        ),
        (
            f"Climate, Materials, and Long-Term Performance in {short}",
            f"Florida roofs fail differently than northern systems. Heat cooks shingles from below "
            f"when attic airflow is weak; wind-driven rain finds marginal flashings; algae and "
            f"granule loss show up on shaded planes. On qualifying steep-slope projects we install "
            f"Atlas Designer Shingles — including Scotchgard™ protection on qualifying products — "
            f"because they are engineered for heat, wind, and Gulf humidity. Manufacturer coverage "
            f"follows Atlas terms. We also review drip edge, pipe boots, and wall transitions so "
            f"the new field of shingles is not fighting failed details at the edges.",
        ),
        (
            f"Buying, Selling, or Maintaining a Roof in {short}",
            f"If you are listing a home in {short}, a documented inspection helps buyers and agents "
            f"understand near-term needs. If you are purchasing, the same walkthrough can prevent "
            f"inheriting a roof that needs immediate capital work. Between those milestones, seasonal "
            f"checks catch lifted tabs, clogged valleys, and dried sealant before interior damage "
            f"spreads. We do not upsell replacement when a lasting repair is the better value — "
            f"and we say so in writing.",
        ),
        (
            f"Why {short} Neighbors Refer Roof Monsters",
            f"Family-owned since 1988, Roof Monsters is a DBA of Terrance McKeever Enterprises, Inc. "
            f"Licenses CCC1335398, CCC052490, and CBC015719. We install Atlas materials on qualifying "
            f"steep-slope projects and back qualifying installation labor with a 15-year workmanship "
            f"warranty. We do not advertise cash discounts or insurance-claim services — storm work "
            f"is private-pay emergency response with clear pricing. Most of our Tampa Bay work still "
            f"comes from neighbors who recommend us. Call (727) 439-3869 or email info@roofmonsters.co "
            f"to schedule an inspection for your {short} property.",
        ),
    ]

    sections = list(custom.get("sections") or [])
    # Append generated sections that add length/uniqueness without duplicating custom headlines
    custom_heads = {s[0].lower() for s in sections}
    for title, body in generated_sections:
        if title.lower() not in custom_heads:
            sections.append((title, body))

    signs = custom.get("signs") or [
        f"Visible shingle wear or storm damage in {short}",
        "Ceiling stains or attic moisture after rain",
        "Granule loss, curling tabs, or lifted flashings",
        "Hot upstairs rooms suggesting poor ventilation",
        "A roof inspection needed before buying or selling",
    ]

    default_faqs = [
        (
            f"Do you serve all of {name}?",
            f"Yes — {name} is within our published Tampa Bay coverage across Pasco, Pinellas, Hernando, Hillsborough, and Manatee County.",
        ),
        (
            f"How fast can Roof Monsters respond in {short}?",
            f"We dispatch from Dunedin for {short} inspections and repairs. Emergency tarping is available 24/7 for active leaks; routine estimates typically schedule within a few business days.",
        ),
        (
            "Are estimates free?",
            "Inspections and estimates are free for qualifying residential and commercial roofing inquiries.",
        ),
        (
            "What licenses do you hold?",
            "Roofing CCC1335398, CCC052490 and building CBC015719 — Terrance McKeever Enterprises, Inc. DBA Roof Monsters.",
        ),
        (
            "Do you work with insurance adjusters?",
            "No. We provide private-pay emergency response and repairs with clear written estimates.",
        ),
        (
            f"What roofing materials do you recommend in {short}?",
            f"On qualifying steep-slope projects we install Atlas Designer Shingles suited to Florida heat, wind, and humidity. We explain repair-versus-replace options based on your roof’s age and condition.",
        ),
        (
            "Do you pull permits for full replacements?",
            "Yes — permitted work is part of a proper Florida replacement on qualifying projects. We coordinate permitting and final inspection as needed.",
        ),
    ]
    faqs = list(custom.get("faqs") or [])
    seen = {q.lower() for q, _ in faqs}
    for q, a in default_faqs:
        if q.lower() not in seen:
            faqs.append((q, a))
            seen.add(q.lower())

    return {
        "headline": custom.get("headline") or f"Local Roofing Expertise for {short}",
        "sections": sections,
        "signs": signs,
        "faqs": faqs,
        "intro_image": intro_image(slug),
        "secondary_image": secondary_image(slug),
    }
