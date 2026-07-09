#!/usr/bin/env python3
"""Generate focused service landing pages under /services/."""

from __future__ import annotations

import html
from pathlib import Path

from form_snippet import estimate_form_compact

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "services"

# Existing hub pages — do not overwrite
SKIP_SLUGS = {
    "comprehensive-roof-installations",
    "expert-roof-repairs-and-maintenance",
    "free-roof-inspections-and-consultations",
    "storm-damage-repair-specialists",
    "gutter-installation-and-cleaning",
    "skylight-installation-and-repair",
}

PAGES = [
    {
        "slug": "roof-replacement",
        "title": "Roof Replacement | Roof Monsters — Tampa Bay",
        "description": "Full roof replacement in Tampa Bay with Atlas shingles, clear written estimates, and a 15-year workmanship warranty from Roof Monsters.",
        "h1": "Roof <span class=\"accent\">Replacement</span>",
        "eyebrow": "Full Re-Roof Projects",
        "lead": "When repair is no longer enough, Roof Monsters delivers complete roof replacement with premium Atlas materials, licensed Florida crews, and a 15-year workmanship warranty.",
        "body": "Most of our work comes from neighbors who recommend us. We scope every replacement clearly — tear-off, underlayment, ventilation, and Atlas Designer Shingles — so you know what you are buying before work begins.",
        "related": [
            ("comprehensive-roof-installations", "Roof Installation Hub"),
            ("shingle-roofing", "Atlas Shingle Roofing"),
            ("residential-roofing", "Residential Roofing"),
            ("free-roof-inspections-and-consultations", "Free Inspection"),
        ],
    },
    {
        "slug": "roof-repair",
        "title": "Roof Repair | Roof Monsters — Tampa Bay",
        "description": "Professional roof repair for leaks, missing shingles, and storm wear across Pasco, Pinellas, Hernando, Hillsborough, and Manatee County.",
        "h1": "Roof <span class=\"accent\">Repair</span>",
        "eyebrow": "Targeted Fixes",
        "lead": "Small roof problems become expensive fast in Florida weather. Roof Monsters repairs leaks, flashing, and damaged shingles with the same care we bring to full replacements.",
        "body": "We diagnose the real source of the problem, explain options in plain language, and provide a clear written estimate. Licensed & insured. Family-owned since 1988.",
        "related": [
            ("expert-roof-repairs-and-maintenance", "Repairs & Maintenance Hub"),
            ("roof-leak-repair", "Leak Repair"),
            ("emergency-roof-repair", "Emergency Repair"),
            ("roof-maintenance", "Maintenance"),
        ],
    },
    {
        "slug": "emergency-roof-repair",
        "title": "Emergency Roof Repair | Roof Monsters — Tampa Bay",
        "description": "24/7 emergency roof repair and tarping in Tampa Bay. Private-pay storm response from Roof Monsters — call (727) 439-3869.",
        "h1": "Emergency Roof <span class=\"accent\">Repair</span>",
        "eyebrow": "24/7 Response",
        "lead": "When a storm opens your roof or a leak is active, call Roof Monsters for emergency tarping and private-pay repairs — fast response from our Dunedin headquarters.",
        "body": "We document damage, stop water intrusion, and schedule permanent repairs with clear written estimates. We do not manage insurance claims; we focus on getting your home protected.",
        "related": [
            ("storm-damage-repair-specialists", "Storm Damage Hub"),
            ("roof-leak-repair", "Leak Repair"),
            ("roof-repair", "Roof Repair"),
            ("free-roof-inspections-and-consultations", "Free Inspection"),
        ],
    },
    {
        "slug": "roof-leak-repair",
        "title": "Roof Leak Repair | Roof Monsters — Tampa Bay",
        "description": "Find and fix roof leaks at valleys, flashings, and penetrations. Licensed Tampa Bay roof leak repair from Roof Monsters.",
        "h1": "Roof Leak <span class=\"accent\">Repair</span>",
        "eyebrow": "Stop the Water",
        "lead": "Roof leaks rarely fix themselves. We locate the source — often flashing, valleys, or worn shingles — and restore a watertight seal before interior damage spreads.",
        "body": "Free inspections help you decide between spot repair and replacement. Atlas materials available for matching repairs on qualifying systems.",
        "related": [
            ("roof-repair", "Roof Repair"),
            ("expert-roof-repairs-and-maintenance", "Repairs Hub"),
            ("emergency-roof-repair", "Emergency Repair"),
            ("free-roof-inspections-and-consultations", "Free Inspection"),
        ],
    },
    {
        "slug": "residential-roofing",
        "title": "Residential Roofing | Roof Monsters — Tampa Bay",
        "description": "Residential roofing for Tampa Bay homeowners — Atlas installs, repairs, inspections, and storm response since 1988.",
        "h1": "Residential <span class=\"accent\">Roofing</span>",
        "eyebrow": "Homes Across Tampa Bay",
        "lead": "From Dunedin bungalows to Hillsborough subdivisions, Roof Monsters protects family homes with Atlas shingles, careful flashing, and a 15-year workmanship warranty.",
        "body": "Licenses CCC1335398, CCC052490, CBC015719. Free inspections. Clear written estimates. Most of our residential work comes from neighbors who recommend us.",
        "related": [
            ("roof-replacement", "Roof Replacement"),
            ("shingle-roofing", "Shingle Roofing"),
            ("roof-repair", "Roof Repair"),
            ("comprehensive-roof-installations", "Installations"),
        ],
    },
    {
        "slug": "commercial-roofing",
        "title": "Commercial Roofing | Roof Monsters — Tampa Bay",
        "description": "Commercial roofing in Tampa Bay — flat roofs, TPO, repairs, and planned replacements for businesses and multi-unit properties.",
        "h1": "Commercial <span class=\"accent\">Roofing</span>",
        "eyebrow": "Business & Multi-Unit",
        "lead": "Commercial properties need predictable scopes and durable systems. We handle low-slope and flat roofing, including TPO, plus repairs that keep operations moving.",
        "body": "Ask about scheduling around business hours and phased work. Atlas materials for steep-slope commercial buildings; TPO and flat systems for low-slope decks.",
        "related": [
            ("tpo-roofing", "TPO Roofing"),
            ("flat-roofing", "Flat Roofing"),
            ("roof-maintenance", "Maintenance"),
            ("comprehensive-roof-installations", "Installations"),
        ],
    },
    {
        "slug": "shingle-roofing",
        "title": "Atlas Shingle Roofing | Roof Monsters — Tampa Bay",
        "description": "Atlas Designer Shingle roofing with Scotchgard protection on qualifying Tampa Bay installs from Roof Monsters.",
        "h1": "Atlas Shingle <span class=\"accent\">Roofing</span>",
        "eyebrow": "Atlas-Only Installs",
        "lead": "We install Atlas Designer Shingles — including Scotchgard protection on qualifying projects — because Florida roofs need materials built for heat, wind, and humidity.",
        "body": "Atlas materials are also available when you need product for a project. Manufacturer warranties apply per Atlas terms; our 15-year workmanship warranty covers installation labor on qualifying jobs.",
        "related": [
            ("roof-replacement", "Roof Replacement"),
            ("comprehensive-roof-installations", "Installations"),
            ("residential-roofing", "Residential"),
            ("warranty-guarantee", "Warranty", True),
        ],
    },
    {
        "slug": "metal-roofing",
        "title": "Metal Roofing | Roof Monsters — Tampa Bay",
        "description": "Metal roofing installation and repair for Tampa Bay homes and buildings that need long-term wind and heat performance.",
        "h1": "Metal <span class=\"accent\">Roofing</span>",
        "eyebrow": "Long-Term Performance",
        "lead": "Metal roofing can be a strong choice for Florida properties that want durability and heat reflection. We install and repair metal systems with licensed Florida crews.",
        "body": "Not every home is a metal candidate — we help you compare metal vs. Atlas shingles based on structure, budget, and HOA rules.",
        "related": [
            ("roof-replacement", "Roof Replacement"),
            ("residential-roofing", "Residential"),
            ("commercial-roofing", "Commercial"),
            ("free-roof-inspections-and-consultations", "Free Inspection"),
        ],
    },
    {
        "slug": "tile-roofing",
        "title": "Tile Roofing | Roof Monsters — Tampa Bay",
        "description": "Tile roof repair and replacement for Tampa Bay properties that need durable, coastal-ready tile systems.",
        "h1": "Tile <span class=\"accent\">Roofing</span>",
        "eyebrow": "Tile Systems",
        "lead": "Tile roofs need specialized fastening, underlayment, and repair techniques. Roof Monsters handles tile repair and replacement for Tampa Bay coastal and inland homes.",
        "body": "Broken tiles and underlayment failures are common after storms — we assess structure and recommend repair vs. full replacement with a clear written estimate.",
        "related": [
            ("roof-repair", "Roof Repair"),
            ("roof-replacement", "Roof Replacement"),
            ("storm-damage-repair-specialists", "Storm Damage"),
            ("free-roof-inspections-and-consultations", "Free Inspection"),
        ],
    },
    {
        "slug": "flat-roofing",
        "title": "Flat Roofing | Roof Monsters — Tampa Bay",
        "description": "Flat and low-slope roofing for Tampa Bay homes and commercial buildings, including TPO options from Roof Monsters.",
        "h1": "Flat <span class=\"accent\">Roofing</span>",
        "eyebrow": "Low-Slope Systems",
        "lead": "Flat and low-slope roofs fail differently than steep shingle roofs. We repair and replace flat systems with drainage and membrane details suited to Florida heat.",
        "body": "TPO is a common commercial choice; we also evaluate existing membranes for repair vs. recover. See our TPO page for commercial-focused details.",
        "related": [
            ("tpo-roofing", "TPO Roofing"),
            ("commercial-roofing", "Commercial"),
            ("roof-leak-repair", "Leak Repair"),
            ("roof-maintenance", "Maintenance"),
        ],
    },
    {
        "slug": "tpo-roofing",
        "title": "TPO Roofing | Roof Monsters — Tampa Bay",
        "description": "TPO roofing for Florida commercial and low-slope buildings — reflective, durable systems installed by Roof Monsters.",
        "h1": "TPO <span class=\"accent\">Roofing</span>",
        "eyebrow": "Commercial Low-Slope",
        "lead": "TPO roofing is popular on Florida commercial buildings for reflectivity and seam strength. Roof Monsters installs and repairs TPO systems across Tampa Bay.",
        "body": "We scope deck condition, insulation, and drainage before recommending a full TPO install or targeted repair.",
        "related": [
            ("flat-roofing", "Flat Roofing"),
            ("commercial-roofing", "Commercial"),
            ("roof-maintenance", "Maintenance"),
            ("free-roof-inspections-and-consultations", "Free Inspection"),
        ],
    },
    {
        "slug": "roof-maintenance",
        "title": "Roof Maintenance | Roof Monsters — Tampa Bay",
        "description": "Preventative roof maintenance and seasonal checkups for Tampa Bay properties — catch small issues before they become leaks.",
        "h1": "Roof <span class=\"accent\">Maintenance</span>",
        "eyebrow": "Prevent Costly Repairs",
        "lead": "Florida sun and storms age roofs faster than many homeowners expect. Seasonal maintenance and free inspections keep small issues from becoming interior damage.",
        "body": "Maintenance visits can include debris clearing checks, flashing review, and ventilation notes — paired with honest repair recommendations when needed.",
        "related": [
            ("expert-roof-repairs-and-maintenance", "Repairs Hub"),
            ("roof-ventilation", "Ventilation"),
            ("free-roof-inspections-and-consultations", "Free Inspection"),
            ("roof-repair", "Roof Repair"),
        ],
    },
    {
        "slug": "roof-ventilation",
        "title": "Roof Ventilation | Roof Monsters — Tampa Bay",
        "description": "Roof ventilation upgrades that reduce attic heat and moisture — protecting shingles and improving comfort in Tampa Bay homes.",
        "h1": "Roof <span class=\"accent\">Ventilation</span>",
        "eyebrow": "Attic Airflow",
        "lead": "Poor ventilation shortens shingle life and drives up attic heat. We evaluate ridge, soffit, and exhaust balance and upgrade systems during repair or replacement projects.",
        "body": "Ventilation is part of every quality Atlas install we complete — and a common fix when homeowners notice curling shingles or hot upstairs rooms.",
        "related": [
            ("roof-maintenance", "Maintenance"),
            ("roof-replacement", "Roof Replacement"),
            ("shingle-roofing", "Shingle Roofing"),
            ("residential-roofing", "Residential"),
        ],
    },
]


SERVICE_IMAGES: dict[str, str] = {
    "roof-replacement": "replacement-08.webp",
    "roof-repair": "project-09.webp",
    "emergency-roof-repair": "installation-01.webp",
    "roof-leak-repair": "completed-05.webp",
    "residential-roofing": "quality-work.webp",
    "commercial-roofing": "project-02.webp",
    "shingle-roofing": "atlas-install-02.webp",
    "metal-roofing": "completed-06.webp",
    "tile-roofing": "completed-03.webp",
    "flat-roofing": "installation-07.webp",
    "tpo-roofing": "tampa-bay-project.webp",
    "roof-maintenance": "installation-04.webp",
    "roof-ventilation": "pinellas-new-roof.webp",
}

# Per-page parallax backgrounds (main intro + expertise sections use different images).
SERVICE_PARALLAX: dict[str, dict[str, str]] = {
    "roof-replacement": {
        "main": "pinellas-new-roof.webp",
        "detail": "atlas-install-01.webp",
        "main_pos": "center 35%",
        "detail_pos": "center 30%",
    },
    "roof-repair": {
        "main": "installation-07.webp",
        "detail": "installation-01.webp",
        "main_pos": "center 40%",
        "detail_pos": "center 35%",
    },
    "emergency-roof-repair": {
        "main": "project-09.webp",
        "detail": "tampa-bay-project.webp",
        "main_pos": "center 30%",
        "detail_pos": "center 35%",
    },
    "roof-leak-repair": {
        "main": "installation-01.webp",
        "detail": "completed-05.webp",
        "main_pos": "center 35%",
        "detail_pos": "center 40%",
    },
    "residential-roofing": {
        "main": "pinellas-new-roof.webp",
        "detail": "quality-work.webp",
        "main_pos": "center 35%",
        "detail_pos": "center 30%",
    },
    "commercial-roofing": {
        "main": "tampa-bay-project.webp",
        "detail": "installation-04.webp",
        "main_pos": "center 35%",
        "detail_pos": "center 40%",
    },
    "shingle-roofing": {
        "main": "atlas-install-01.webp",
        "detail": "atlas-install-02.webp",
        "main_pos": "center 30%",
        "detail_pos": "center 35%",
    },
    "metal-roofing": {
        "main": "completed-06.webp",
        "detail": "completed-03.webp",
        "main_pos": "center 35%",
        "detail_pos": "center 40%",
    },
    "tile-roofing": {
        "main": "completed-03.webp",
        "detail": "replacement-08.webp",
        "main_pos": "center 40%",
        "detail_pos": "center 35%",
    },
    "flat-roofing": {
        "main": "project-02.webp",
        "detail": "installation-04.webp",
        "main_pos": "center 35%",
        "detail_pos": "center 45%",
    },
    "tpo-roofing": {
        "main": "installation-04.webp",
        "detail": "tampa-bay-project.webp",
        "main_pos": "center 40%",
        "detail_pos": "center 35%",
    },
    "roof-maintenance": {
        "main": "quality-work.webp",
        "detail": "installation-07.webp",
        "main_pos": "center 30%",
        "detail_pos": "center 35%",
    },
    "roof-ventilation": {
        "main": "atlas-install-02.webp",
        "detail": "pinellas-new-roof.webp",
        "main_pos": "center 35%",
        "detail_pos": "center 30%",
    },
}


def parallax_bg(p: dict, section: str) -> str:
    cfg = SERVICE_PARALLAX.get(p["slug"], {})
    image = cfg.get(section, "quality-work.webp" if section == "main" else "installation-04.webp")
    position = cfg.get(f"{section}_pos", "center 35%")
    return (
        f'<div class="rm-parallax-bg" style="background-image: url(\'assets/images/gallery/{image}\'); '
        f"background-position: {position};\" aria-hidden=\"true\"></div>"
    )


SERVICE_EXPANSIONS: dict[str, dict] = {
    "roof-replacement": {
        "paragraphs": [
            "Florida replacements often involve wind-rated fastening, balanced attic ventilation, and underlayment choices that stand up to Gulf humidity. We specify Atlas Designer Shingles on qualifying steep-slope projects because they are engineered for heat, algae resistance, and coastal weather.",
            "Whether your roof failed from age, storm wear, or repeated repairs, we help you compare repair vs. replacement honestly. Most homeowners in Tampa Bay replace between 20–25 years on standard shingle systems, sooner when ventilation or prior repairs were neglected.",
            "Every replacement starts with a walk-through of decking, drip edge, and penetration flashings. We photograph problem areas, explain what must be repaired before new material goes on, and include those items in your written estimate so there are no surprise change orders mid-project.",
        ],
        "process": [
            ("Free inspection", "We walk the roof, check decking and ventilation, and photograph areas that affect scope."),
            ("Written estimate", "You receive a clear line-item estimate covering tear-off, materials, labor, and disposal — no surprise add-ons."),
            ("Permits & scheduling", "We coordinate permitting and dumpster placement, then confirm your install window before tear-off begins."),
            ("Atlas install & warranty", "Our crew completes the install to Florida code and manufacturer specs, then reviews warranty paperwork with you."),
        ],
        "includes": [
            ("Complete tear-off", "Removal of existing roofing down to decking on scoped areas, with debris hauled away and magnetic nail sweep on qualifying projects."),
            ("Underlayment & flashing", "Ice-and-water or synthetic underlayment at valleys and penetrations, plus new drip edge and pipe boot details as needed."),
            ("Atlas Designer Shingles", "Wind-rated install of Atlas shingles on qualifying steep-slope homes, including ridge cap and manufacturer fastening patterns."),
            ("Ventilation review", "Ridge, soffit, and exhaust balance checked so your new roof is not fighting attic heat on day one."),
        ],
        "signs": [
            "Widespread curling, cracking, or missing shingles across multiple roof planes",
            "Repeated leak repairs in different areas within a few years",
            "Daylight visible through attic decking or soft spots when walking the roof",
            "Granule loss heavy enough to expose mat on large sections",
            "Roof age past 20 years with prior patchwork and ventilation issues",
        ],
        "faqs": [
            ("How long does a roof replacement take?", "Most residential tear-offs and re-roofs complete in a few days depending on size, weather, and decking repairs. We confirm timeline before work begins."),
            ("Do you pull permits for roof replacement?", "Yes — permitted work is part of a proper Florida replacement. We handle permitting and final inspection coordination on qualifying projects."),
            ("Can you match Atlas shingles to my neighborhood?", "We help select Atlas profiles and colors that suit your home and HOA requirements when applicable."),
            ("What does a roof replacement cost in Tampa Bay?", "Cost depends on square footage, pitch, decking condition, and material choice. We provide a free inspection and written line-item estimate before you commit."),
            ("Do you offer financing?", "We focus on clear private-pay estimates. Ask during your consultation if you need help planning project timing."),
            ("Is Atlas the only shingle brand you install?", "Yes — we install Atlas materials on qualifying steep-slope projects and can supply Atlas product when needed for your scope."),
        ],
        "why": [
            ("Written Scopes", "Line-item estimates explain tear-off, materials, labor, and disposal before work starts — no vague allowances."),
            ("Atlas Focus", "We install Atlas Designer Shingles on qualifying projects for heat, wind, and algae resistance suited to Florida."),
            ("Licensed Crews", "Florida roofing and building licenses CCC1335398, CCC052490, CBC015719 — family-owned since 1988."),
            ("Neighbor Trust", "Most of our replacement work comes from referrals across Pasco, Pinellas, Hernando, Hillsborough, and Manatee County."),
        ],
        "guide_sections": [
            (
                "When Replacement Beats Another Patch",
                "A Tampa Bay roof replacement usually makes sense when wear is no longer isolated: repeated leaks on different roof planes, soft decking, widespread granule loss, or shingles past their realistic Florida service life. Afternoon storms and Gulf humidity punish weak spots quickly, so another patch can buy only weeks if the field is brittle. We compare repair and replacement in writing, with photos from the roof and attic when accessible, so you can decide from conditions instead of pressure.",
            ),
            (
                "Decking, Ventilation, and Florida Code",
                "Full replacement is the moment to correct problems hidden under old material. We check decking, drip edge, underlayment, pipe boots, wall flashings, and attic airflow before new shingles go down. Poor soffit intake or blocked ridge exhaust can cook shingles from underneath, especially through long Pinellas and Hillsborough summers. Roof Monsters works under roofing licenses CCC1335398 and CCC052490 and building license CBC015719, and permitted replacement work is completed to applicable Florida code requirements.",
            ),
            (
                "Atlas Shingles for Steep-Slope Homes",
                "On qualifying steep-slope replacements, we specify Atlas Designer Shingles because they fit the heat, algae, and wind realities of Gulf Coast neighborhoods. Product selection includes color, profile, ridge cap, underlayment, starter course, and ventilation details, not just the visible shingle. Manufacturer coverage follows Atlas terms and registration. Our 15-year workmanship warranty covers qualifying installation labor, giving homeowners separate protection for how the system was installed.",
            ),
            (
                "Planning Around Storm Season",
                "Replacement scheduling in Florida has to respect rain windows, permitting, material staging, and safe dry-in timing. If a tropical system has already opened the roof, we can stabilize with private-pay emergency protection and then quote permanent replacement once weather allows. We do not manage insurance claims or adjuster meetings. The value we provide is a clear scope, licensed installation, documented decking repairs, and communication before tear-off begins.",
            ),
            (
                "Why Neighbors Refer Roof Monsters",
                "Roof Monsters is family-owned, headquartered in Dunedin, and serving Tampa Bay since 1988. Many replacements come from homeowners who saw our crew protect landscaping, keep the job site clean, and explain the final walkthrough without jargon. Review related <a href=\"/services/shingle-roofing/\">Atlas shingle roofing</a>, browse the <a href=\"/gallery/\">project gallery</a>, or call <a href=\"tel:7274393869\">(727) 439-3869</a> to schedule a free inspection.",
            ),
        ],
    },
    "roof-repair": {
        "paragraphs": [
            "Tampa Bay repairs see the same patterns: lifted shingles after storms, dried flashing sealant at chimneys and walls, and valley debris that channels water under tabs. Catching these early prevents drywall and insulation damage inside.",
            "We do not upsell replacement when a targeted repair will last. Our reputation in Pinellas and Hillsborough is built on neighbors referring us because we explain the tradeoffs clearly.",
            "Repair visits include photos you can keep for your records. If we find conditions that make a patch short-lived, we tell you upfront so you can budget for a larger fix later.",
        ],
        "process": [
            ("Leak diagnosis", "We trace water paths — flashing, valleys, penetrations, and shingle wear — instead of only patching visible stains."),
            ("Repair options", "You get a written recommendation for spot repair, partial re-roof, or full replacement when that is the better long-term value."),
            ("Quality materials", "Repairs use compatible Atlas or system-matched materials so repaired areas perform with the rest of the roof."),
            ("Follow-up guidance", "We note maintenance items — debris in valleys, attic ventilation, tree contact — that help the repair last."),
        ],
        "includes": [
            ("Flashing & penetration work", "Chimney, wall, skylight, and pipe boot repairs using compatible sealants and metal details."),
            ("Shingle replacement", "Matching or complementary Atlas shingles on qualifying systems for wind-damaged or worn tabs."),
            ("Leak tracing", "Attic and rooftop inspection to find the entry point, not just the ceiling stain."),
            ("Written estimate", "Clear pricing for the repair scope before we schedule the fix."),
        ],
        "signs": [
            "Water stains on ceilings or walls after rain",
            "Missing, lifted, or creased shingles after wind events",
            "Rust or gaps at roof-to-wall or chimney flashings",
            "Granules collecting in gutters on a young-looking roof",
            "Musty attic smell or damp insulation near the ridge",
        ],
        "faqs": [
            ("Can you repair a roof without replacing it?", "Often yes — if the system has life left and damage is localized. We document conditions so you can plan ahead."),
            ("Do you repair roofs other companies installed?", "Yes. We evaluate existing work and fix deficiencies to Florida code regardless of who installed the original roof."),
            ("How fast can you schedule a roof repair?", "Many repairs schedule within days; active leaks and storm openings are prioritized for emergency response."),
            ("Will a repair match my existing shingles?", "We match Atlas or compatible materials on qualifying systems. Weathering may show slight color variation on older roofs."),
            ("How much does roof repair cost?", "Simple flashing or shingle repairs differ widely from structural decking work. We inspect first and provide a written estimate."),
        ],
        "why": [
            ("Honest Diagnosis", "We trace leaks to the source instead of guessing from interior stains alone."),
            ("Repair-First Mindset", "Replacement is recommended only when patches will not last."),
            ("Atlas Repairs", "Compatible Atlas materials on qualifying shingle systems."),
            ("Fast Scheduling", "Active leaks and storm damage are prioritized from our Dunedin headquarters."),
        ],
        "guide_sections": [
            (
                "Repair Starts With Finding the Failure",
                "Good roof repair in Tampa Bay starts by tracing the failure, not by sealing the closest crack. Water can enter at a pipe boot, chimney flashing, valley, or lifted shingle tab and travel several feet before staining drywall. We inspect the roof plane and attic when accessible, photograph the entry point, and explain whether a targeted fix is likely to last through another rainy season. That diagnosis keeps small repairs from becoming recurring service calls.",
            ),
            (
                "Materials That Match the Existing Roof",
                "A repair should work with the roof already on the home. On qualifying steep-slope systems, we use Atlas or compatible materials for shingle tabs, ridge work, and localized replacements so repaired areas perform with the surrounding field. Older roofs may show color variation because sun and humidity age shingles unevenly. We discuss that before scheduling, along with whether flashing metal, sealants, or underlayment need replacement for the repair to hold.",
            ),
            (
                "When a Patch Is Not Honest",
                "Some damage looks repairable from the driveway but fails the closer inspection: brittle shingles that break when lifted, soft decking around a leak, widespread nail pops, or multiple previous patches in the same valley. In those cases we explain why the repair may be short-lived and price replacement or partial re-roof options separately. The goal is not to upsell; it is to avoid charging for work that Florida heat and storms will undo quickly.",
            ),
            (
                "Storm Repairs Without Claim Hype",
                "After wind or debris damage, we provide private-pay repair scopes with photos and clear pricing. Missing shingles, torn ridge cap, and exposed nail patterns can allow water into the deck during the next afternoon storm, so timing matters. We do not manage insurance claims or coordinate adjuster meetings. Our job is licensed roof repair under CCC1335398, CCC052490, and CBC015719, completed with practical documentation for your own records.",
            ),
            (
                "Local Repair Accountability",
                "Roof Monsters has served homeowners from Dunedin since 1988, and most repair work still comes from neighbors who recommend us. You get a written estimate, repair photos, and guidance on maintenance items that could trigger the next leak. If the problem is active now, call <a href=\"tel:7274393869\">(727) 439-3869</a>; you can also compare <a href=\"/services/roof-leak-repair/\">roof leak repair</a> and <a href=\"/services/roof-maintenance/\">maintenance</a> options.",
            ),
        ],
    },
    "emergency-roof-repair": {
        "paragraphs": [
            "After tropical weather, Tampa Bay homeowners need a roofer who answers the phone. Our Dunedin headquarters keeps Pinellas and Hillsborough within practical emergency reach for tarping and dry-in work.",
            "We focus on protecting your home first. We do not manage insurance claims or adjuster meetings — we deliver licensed emergency roofing and permanent repairs on private-pay terms you can understand upfront.",
            "Emergency response includes stabilizing the opening, documenting conditions with photos, and scheduling permanent repairs once weather allows safe completion.",
        ],
        "process": [
            ("Stabilize the opening", "Emergency tarping and temporary dry-in stop active water intrusion until permanent repairs are scheduled."),
            ("Document conditions", "Photos and notes capture damage for your records and help scope permanent repairs."),
            ("Permanent repair plan", "We follow up with a written estimate for lasting repairs — private-pay storm response with clear pricing."),
            ("Final walk-through", "After permanent work, we review completed repairs and cleanup with you on site."),
        ],
        "includes": [
            ("Emergency tarping", "Temporary weather protection for active leaks and open roof areas."),
            ("Dry-in details", "Plastic and fastening patterns suited to wind until permanent repairs begin."),
            ("Damage documentation", "Photos and notes for your records — not insurance claim management."),
            ("Permanent repair estimate", "Written scope for lasting fixes once the home is stabilized."),
        ],
        "signs": [
            "Active water entering the home during or immediately after rain",
            "Large sections of missing shingles or exposed decking after wind",
            "Tree or debris impact that punctured the roof membrane",
            "Tarp failure from a prior temporary repair",
            "Ceiling collapse risk from saturated drywall",
        ],
        "faqs": [
            ("Are you available after hours for roof emergencies?", "Yes — call (727) 439-3869 for active leaks and storm openings. Regular estimating hours are Monday–Saturday, 7 AM–7 PM."),
            ("Is emergency tarping a permanent fix?", "No — tarps are temporary protection. We schedule permanent repairs once weather and access allow safe completion."),
            ("Do you work with insurance adjusters?", "No. We provide private-pay emergency response and repairs with clear written estimates."),
            ("How quickly can you tarp a roof?", "We prioritize active intrusion calls and dispatch from Dunedin for Tampa Bay properties."),
            ("What should I do before you arrive?", "Move valuables away from leaks, avoid attic travel on wet decking, and photograph damage if it is safe to do so."),
        ],
        "why": [
            ("24/7 Response", "Call for active leaks and storm openings — we focus on stopping water first."),
            ("Private-Pay Clarity", "Clear written estimates without insurance claim coordination."),
            ("Licensed Work", "Emergency and permanent repairs by Florida-licensed roofing crews."),
            ("Local Reach", "Dunedin HQ with practical response across Pinellas and Hillsborough."),
        ],
        "guide_sections": [
            (
                "What Counts as a Roofing Emergency",
                "A roofing emergency is active water entering the home, exposed decking after wind, tree impact, a failed tarp, or ceiling material becoming saturated enough to create a safety concern. Tampa Bay storms can drop heavy rain again the same afternoon, so the first goal is stopping intrusion before insulation, drywall, and electrical fixtures take more damage. If conditions are unsafe for roof access, we explain the delay and return when the roof can be approached responsibly.",
            ),
            (
                "Temporary Tarping and Dry-In",
                "Emergency tarping is temporary protection, not a finished repair. We secure plastic or tarp material over the opening, fasten for expected wind where possible, and document what we can see once the home is stabilized. The temporary scope buys time until weather clears and permanent repair materials can be staged. It also helps separate immediate water control from the later decision about spot repair, partial replacement, or full roof replacement.",
            ),
            (
                "Private-Pay Storm Response",
                "Roof Monsters handles emergency roof repair as private-pay work with clear pricing. We do not manage insurance claims, meet adjusters, or promise claim outcomes. Homeowners who choose to involve a carrier should handle that process directly. Our role is licensed emergency roofing from a Dunedin contractor: stop the water, document conditions, and provide a written estimate for permanent work under Florida roofing licenses CCC1335398 and CCC052490.",
            ),
            (
                "Response Area and Weather Reality",
                "Our Dunedin headquarters gives practical emergency reach across Pinellas, nearby Pasco and Hillsborough, and other Tampa Bay service areas as scheduling and weather allow. During widespread tropical events, active intrusion and open roof areas are prioritized ahead of routine estimates. We will tell you what can be done safely, what is temporary, and when a crew can return for permanent repairs after lightning, wind, or saturated surfaces make access risky.",
            ),
            (
                "Call Before Interior Damage Spreads",
                "Move valuables away from the leak, catch dripping water if safe, and avoid walking in a wet attic. Then call <a href=\"tel:7274393869\">(727) 439-3869</a> for emergency roof repair. Family-owned since 1988, Roof Monsters focuses on stabilizing the home first and explaining the next step clearly. For non-emergency planning, review <a href=\"/services/roof-repair/\">roof repair</a> or browse the <a href=\"/gallery/\">gallery</a>.",
            ),
        ],
    },
    "roof-leak-repair": {
        "paragraphs": [
            "Leak repair is detective work. Water often travels along decking or trusses before it stains a ceiling, so we inspect uphill from the stain at valleys, wall flashings, HVAC penetrations, and compromised shingles.",
            "Atlas materials are available for matching repairs on qualifying shingle systems. We explain when a leak points to a small fix versus ventilation or age-related failure across the field.",
            "Free inspections help you decide before interior damage spreads. Most neighbors call us after a second stain appears — we encourage earlier checks when you notice attic moisture or shingle wear.",
        ],
        "process": [
            ("Interior & attic review", "We note stain patterns and attic moisture to narrow the search area."),
            ("Rooftop tracing", "Hose testing or visual inspection at flashings, valleys, and penetrations as appropriate."),
            ("Targeted repair", "Compatible materials and flashing details restore a watertight seal at the source."),
            ("Prevention notes", "We flag ventilation or maintenance items that could cause repeat leaks."),
        ],
        "includes": [
            ("Flashing repairs", "Wall, chimney, skylight, and pipe boot corrections at the leak source."),
            ("Valley & penetration work", "Sealing and shingle integration where water channels into the home."),
            ("Shingle replacement", "Atlas or compatible tabs on qualifying systems in the repair zone."),
            ("Photo documentation", "Images of the failure point and completed repair for your records."),
        ],
        "signs": [
            "Brown rings on ceilings that grow after each storm",
            "Drips at light fixtures or bathroom vents during rain",
            "Wet insulation near chimneys, skylights, or valleys",
            "Rust streaks on pipe boots or wall flashings",
            "Mold odor in attic spaces after extended rainy weeks",
        ],
        "faqs": [
            ("Can you find a leak without removing drywall?", "Usually yes — attic and rooftop inspection locates most entry points without interior demolition."),
            ("Why does my leak only happen in heavy rain?", "Wind-driven rain exposes marginal flashings and valley paths that light rain does not reach."),
            ("Is leak repair covered under your workmanship warranty?", "Qualifying repair work is documented; warranty terms are reviewed on your estimate."),
            ("Should I replace the roof if I have multiple leaks?", "Not always — we compare localized repairs vs. system age and document honest options."),
            ("Do you repair flat roof leaks?", "Yes — low-slope membranes and TPO systems are evaluated separately from shingle leaks."),
        ],
        "why": [
            ("Source-First Fixes", "We repair where water enters, not just where it stains."),
            ("Atlas Matching", "Compatible materials on qualifying shingle systems."),
            ("Free Inspections", "Written options before you commit to repair scope."),
            ("Tampa Bay Experience", "Decades of valley, flashing, and penetration work across five counties."),
        ],
        "guide_sections": [
            (
                "Why Roof Leaks Are Hard to Read",
                "A ceiling stain rarely sits directly below the roof opening. In Florida downpours, water follows rafters, decking seams, insulation, and electrical penetrations before it shows up indoors. That is why roof leak repair starts uphill from the stain, checking valleys, pipe boots, wall flashings, skylights, and worn shingle fields. We combine interior clues with roof inspection so the repair addresses the source instead of chasing drywall marks after every storm.",
            ),
            (
                "Common Leak Sources in Tampa Bay",
                "The most frequent leak sources we see are dried sealant at penetrations, rusted or lifted flashing, debris-packed valleys, cracked pipe boots, nail pops, and wind-lifted shingles. Coastal humidity also accelerates algae and granule wear on shaded roof planes. On qualifying shingle systems, Atlas or compatible materials help repaired areas integrate with the existing roof. If the leak starts at a flat-to-shingle transition, we evaluate the membrane and steep-slope side together.",
            ),
            (
                "Moisture Damage Beyond the Roof",
                "Leak repair is partly about preventing secondary damage. Wet insulation loses performance, ceiling stains can spread after one more storm, and attic humidity can encourage mold on decking. We photograph conditions when accessible and explain what roofing work can solve versus what may need interior cleanup by another trade. Prompt repair is especially important before hurricane season, when one small entry point can become a much larger interior problem.",
            ),
            (
                "Repair, Partial Re-Roof, or Replacement",
                "A single failed boot may need a straightforward repair. Multiple leaks across different planes, soft decking, or brittle shingles often signal a system nearing replacement. We put those options in writing so you can compare cost, risk, and timing. Qualifying installation labor is backed by our 15-year workmanship warranty, while Atlas manufacturer coverage follows Atlas terms on qualifying products. Licenses CCC1335398, CCC052490, and CBC015719 support the work.",
            ),
            (
                "Schedule a Leak Inspection",
                "If a stain grows after each storm, do not wait for drywall to fail. Roof Monsters is headquartered in Dunedin, family-owned since 1988, and referral-trusted across Tampa Bay. Call <a href=\"tel:7274393869\">(727) 439-3869</a> for leak repair, compare <a href=\"/services/emergency-roof-repair/\">emergency repair</a> if water is active, or view completed work in the <a href=\"/gallery/\">gallery</a>.",
            ),
        ],
    },
    "residential-roofing": {
        "paragraphs": [
            "Residential roofing in Tampa Bay spans 1960s ranch homes in Pinellas, newer construction in Wesley Chapel, and waterfront properties that need corrosion-aware flashing details. We tailor scopes to how your home is built and ventilated.",
            "From first inspection to final magnet sweep, the same licensed crew standards apply whether you need a few shingle tabs or a full Atlas re-roof. Our 15-year workmanship warranty applies on qualifying installation labor.",
            "Most residential clients find us through neighbors. We return calls promptly, show up for scheduled inspections, and leave job sites clean — expectations that matter when the work is on your home.",
        ],
        "process": [
            ("Home inspection", "We review roof planes, attic ventilation, and interior leak evidence if present."),
            ("Options & estimate", "Repair, partial, or full replacement recommendations with Atlas material specs when applicable."),
            ("Scheduled install or repair", "Crews protect landscaping, complete work to code, and haul debris."),
            ("Walk-through & warranty", "Final review with you and manufacturer paperwork on qualifying Atlas installs."),
        ],
        "includes": [
            ("Steep-slope Atlas installs", "Designer shingles on qualifying homes with manufacturer fastening patterns."),
            ("Targeted repairs", "Flashing, valley, and shingle fixes without unnecessary full replacement."),
            ("Ventilation upgrades", "Ridge and soffit improvements during replacement projects when needed."),
            ("Free inspections", "No-obligation assessments for buyers, sellers, and long-term owners."),
        ],
        "signs": [
            "HOA or insurer requests a roof condition letter",
            "Preparing to list a home and want documented roof condition",
            "Recurring attic heat or high cooling bills with an aging roof",
            "Storm season approaching with visible wear or prior patchwork",
            "Neighbor replaced recently and your roof is the same age",
        ],
        "faqs": [
            ("Do you work on single-family homes and townhomes?", "Yes — we serve residential properties across our published Tampa Bay counties."),
            ("Can you help with HOA roof requirements?", "We document materials and colors and select Atlas profiles that meet many HOA guidelines."),
            ("Do you offer roof inspections before buying a home?", "Yes — free inspections for qualifying inquiries help buyers understand near-term roof needs."),
            ("How do I know if I need repair or replacement?", "We inspect decking, shingle age, and leak history, then explain both paths in writing."),
            ("Are you family-owned?", "Yes — Terrance McKeever Enterprises, Inc. DBA Roof Monsters, serving Tampa Bay since 1988."),
        ],
        "why": [
            ("Homeowner Focus", "Residential schedules, cleanup, and communication built around your household."),
            ("Atlas Installs", "Designer shingles on qualifying steep-slope homes."),
            ("15-Year Workmanship", "Installation labor warranty on qualifying projects."),
            ("Referral Reputation", "Most work comes from neighbors who recommend us."),
        ],
        "guide_sections": [
            (
                "Residential Roofing by Home Type",
                "Residential roofing in Tampa Bay is not one-size-fits-all. A Dunedin bungalow, a Palm Harbor ranch, a Wesley Chapel subdivision home, and a coastal townhome can have different decking, ventilation, pitch, HOA rules, and wind exposure. We inspect the specific structure before recommending repair, partial re-roof, or replacement. That keeps the scope tied to how the home was built instead of forcing every homeowner into the same roofing package.",
            ),
            (
                "What Homeowners Should Expect",
                "A good residential roofing estimate should explain materials, labor, disposal, permit needs, ventilation, and any unknowns like decking that can only be confirmed during tear-off. We provide photos and written recommendations before work begins, then communicate schedule windows, driveway access, and cleanup expectations. Magnetic nail sweeps on qualifying projects and careful staging matter because your family, pets, landscaping, and neighbors live around the job site.",
            ),
            (
                "Atlas, Warranty, and Licensing",
                "On qualifying steep-slope residential projects, Roof Monsters installs Atlas Designer Shingles selected for Florida heat, wind, and algae pressure. Manufacturer warranty coverage follows Atlas terms and registration. Our 15-year workmanship warranty covers qualifying installation labor, giving homeowners clear local accountability for the install. We operate under Florida roofing licenses CCC1335398 and CCC052490 plus building license CBC015719, with work coordinated from our Dunedin headquarters.",
            ),
            (
                "Storm Readiness for Family Homes",
                "Before storm season, residential roofs deserve a practical check: lifted tabs, loose ridge cap, debris in valleys, cracked pipe boots, and attic moisture should be addressed before a tropical system tests them. If weather already caused an opening, we provide private-pay emergency response and permanent repair estimates. We do not manage insurance claims or adjuster meetings; we focus on protecting the home and completing licensed roofing work.",
            ),
            (
                "Referral-Trusted Since 1988",
                "Most residential work comes from neighbors who recommend Roof Monsters after seeing clear scopes, clean job sites, and follow-through. Family-owned since 1988, we serve Pasco, Pinellas, Hernando, Hillsborough, and Manatee County from Dunedin. Explore <a href=\"/services/roof-replacement/\">replacement</a>, <a href=\"/services/roof-repair/\">repair</a>, and the <a href=\"/gallery/\">gallery</a>, or call <a href=\"tel:7274393869\">(727) 439-3869</a>.",
            ),
        ],
    },
    "commercial-roofing": {
        "paragraphs": [
            "Commercial roofs in Tampa Bay include retail plazas, churches, multi-family buildings, and owner-occupied offices. Low-slope TPO and modified systems dominate many decks, while steep-slope commercial buildings may use Atlas shingles.",
            "We plan around business hours when possible — phased repairs, weekend work, and clear staging areas so tenants and customers are not surprised by debris or blocked entries.",
            "Maintenance agreements and inspection reports help property managers budget capital work instead of reacting to interior damage after every storm season.",
        ],
        "process": [
            ("Site walk & scope", "We review deck type, drainage, HVAC curbs, and interior leak evidence."),
            ("Written proposal", "Materials, phasing, timeline, and warranty terms explained for decision-makers."),
            ("Licensed execution", "Crews complete work to Florida code with safety and access planning."),
            ("Documentation", "Completion photos and warranty paperwork for your property files."),
        ],
        "includes": [
            ("TPO & low-slope work", "Membrane repair and replacement on qualifying commercial decks."),
            ("Steep-slope commercial", "Atlas shingle systems on qualifying buildings."),
            ("Penetration & curb details", "HVAC, vent, and parapet corrections that stop chronic leaks."),
            ("Maintenance planning", "Inspection notes for capital budgeting and storm readiness."),
        ],
        "signs": [
            "Ponding water on flat roofs after routine rain",
            "Interior ceiling tiles staining above HVAC units",
            "Membrane seams lifting or bubbling in heat",
            "Tenant complaints about leaks in multiple units",
            "Roof past service life with recurring patch history",
        ],
        "faqs": [
            ("Do you work on multi-tenant buildings?", "Yes — we coordinate access and phasing with property managers when needed."),
            ("Can you repair TPO without full replacement?", "Often yes — we evaluate seam condition, attachment, and deck before recommending recover vs. tear-off."),
            ("Do you provide documentation for asset managers?", "Written estimates, photos, and completion notes are available for your files."),
            ("Are commercial estimates free?", "Inspections and estimates are free for qualifying commercial roofing inquiries."),
            ("What licenses do you carry?", "Roofing CCC1335398, CCC052490 and building CBC015719."),
        ],
        "why": [
            ("Low-Slope Expertise", "TPO and flat systems alongside steep-slope commercial work."),
            ("Phased Scheduling", "Planning around operations and tenant access."),
            ("Clear Proposals", "Written scopes for owners and managers before work begins."),
            ("Licensed & Insured", "Florida-licensed crews for commercial properties."),
        ],
        "guide_sections": [
            (
                "Commercial Roofing Needs Predictable Scopes",
                "Commercial roofing decisions affect tenants, customers, inventory, equipment, and operating hours. A small leak over an office ceiling tile can point to HVAC curb flashing, membrane seams, ponding water, or a steep-slope transition. We inspect the roof and interior evidence, then write proposals that separate urgent repairs from capital replacement planning. That structure helps owners and managers make budget decisions without guessing from a single stain.",
            ),
            (
                "Low-Slope, TPO, and Steep-Slope Areas",
                "Many Tampa Bay commercial properties combine low-slope membrane areas with steep-slope architectural sections. TPO may be appropriate for reflective commercial decks, while qualifying steep-slope sections can use Atlas shingles. We evaluate drainage, insulation moisture, deck type, rooftop equipment, parapets, and access before recommending repair, recover, or tear-off. The best commercial roof scope matches the building's use, not just the material already installed.",
            ),
            (
                "Documentation for Owners and Managers",
                "Commercial clients often need documentation for property files, boards, lenders, or future sale planning. We provide written scopes, completion photos, warranty information, and maintenance recommendations when applicable. Roof Monsters operates under Florida roofing licenses CCC1335398 and CCC052490 and building license CBC015719. Our 15-year workmanship warranty applies to qualifying installation labor, while manufacturer coverage follows the material provider's terms and registration requirements.",
            ),
            (
                "Scheduling Around Business Disruption",
                "Roof work can affect parking, dumpster placement, customer entrances, tenant access, and noise. We discuss staging before the project begins and can phase work where the building and scope allow. Afternoon thunderstorms and summer heat also shape safe work windows on commercial roofs. If storm damage opens the roof, we provide private-pay emergency protection and clear permanent repair pricing, without insurance claim management.",
            ),
            (
                "Talk Through the Property Plan",
                "Whether you manage a retail plaza, church, office, or multi-family building, a free commercial roofing inspection can clarify immediate risk and long-term budget. Roof Monsters is family-owned since 1988 and based in Dunedin. Review <a href=\"/services/tpo-roofing/\">TPO roofing</a>, <a href=\"/services/flat-roofing/\">flat roofing</a>, or call <a href=\"tel:7274393869\">(727) 439-3869</a> to discuss access and timing.",
            ),
        ],
    },
    "shingle-roofing": {
        "paragraphs": [
            "Atlas Designer Shingles are engineered for Florida heat, wind, and algae pressure. Scotchgard™ protection on qualifying products helps resist black streaks common in humid Gulf Coast neighborhoods.",
            "We install Atlas exclusively on steep-slope work — not a menu of unrelated brands. That focus keeps fastening patterns, ridge details, and warranty registration consistent job to job.",
            "Atlas materials are also available when you need product supplied for your project scope. Manufacturer coverage applies per Atlas terms; our 15-year workmanship warranty covers qualifying installation labor.",
        ],
        "process": [
            ("Profile & color selection", "We review Atlas options suited to your home style and HOA rules when applicable."),
            ("Deck & ventilation prep", "Underlayment and airflow corrections before shingles are installed."),
            ("Manufacturer-spec install", "Wind-rated nailing and ridge cap details per Atlas requirements."),
            ("Warranty registration", "Paperwork review for Atlas coverage and our workmanship warranty."),
        ],
        "includes": [
            ("Atlas Designer Shingles", "Profiles selected for Florida performance on qualifying installs."),
            ("Scotchgard™ options", "Algae-resistant products on qualifying Atlas lines."),
            ("Underlayment & flashing", "System components that protect valleys and penetrations."),
            ("Ventilation integration", "Balanced exhaust and intake with the new shingle system."),
        ],
        "signs": [
            "Black streaks or algae growth across north-facing planes",
            "Original builder-grade shingles past 15–20 years",
            "Frequent granule loss in gutters after light rain",
            "HOA letter requiring approved shingle profiles",
            "Planning a replacement and wanting a single manufacturer focus",
        ],
        "faqs": [
            ("Why Atlas only?", "Focused expertise and consistent warranty registration across our installs."),
            ("What is Scotchgard™ protection?", "Atlas algae-resistant technology on qualifying shingle products — ask which profiles qualify for your project."),
            ("How long do Atlas shingles last in Florida?", "Lifespan depends on ventilation, tree cover, and maintenance; we inspect and explain realistic expectations."),
            ("Can I buy Atlas materials without install?", "Atlas materials are available for qualifying projects — ask during your estimate."),
            ("Do Atlas shingles qualify for wind ratings?", "Atlas publishes wind ratings by product; we install to manufacturer and Florida code requirements."),
        ],
        "why": [
            ("Atlas-Only Focus", "One manufacturer for consistent steep-slope results."),
            ("Scotchgard™ Options", "Algae resistance on qualifying Designer Shingle lines."),
            ("15-Year Workmanship", "Installation labor warranty on qualifying projects."),
            ("Florida Install Patterns", "Heat, wind, and humidity-aware detailing."),
        ],
        "guide_sections": [
            (
                "Why We Focus on Atlas Shingles",
                "Shingle roofing performs best when the installer understands one system deeply: starter, underlayment, field shingles, ridge cap, ventilation, nail patterns, and warranty registration. Roof Monsters installs Atlas Designer Shingles on qualifying steep-slope projects because they are engineered for Florida heat, wind, humidity, and algae pressure. That focus keeps product selection and installation details consistent from one Tampa Bay referral job to the next.",
            ),
            (
                "Algae, Heat, and Gulf Humidity",
                "Black streaking is common in humid neighborhoods with tree cover and shaded roof planes. Qualifying Atlas products with Scotchgard protection help resist algae staining, which is especially useful around Pinellas, Pasco, and Hillsborough homes that stay damp after afternoon storms. Heat matters too: attic ventilation, underlayment, and correct fastening all affect how long shingles last. A premium shingle still needs a Florida-aware install underneath it.",
            ),
            (
                "Installation Details You Cannot See",
                "Most shingle failures start in details homeowners rarely see from the driveway. Starter course placement, valley method, flashing integration, drip edge, pipe boots, ridge vent cuts, and nail depth all shape performance in wind-driven rain. Our crews inspect decking and ventilation before covering them. Qualifying installation labor is backed by a 15-year workmanship warranty, separate from Atlas manufacturer coverage that follows Atlas terms and registration.",
            ),
            (
                "Repairing Existing Shingle Roofs",
                "Not every shingle problem requires replacement. Lifted tabs, isolated storm creases, a failed pipe boot, or missing ridge cap may be repairable when the roof still has life. If shingles are brittle, granules are gone, or leaks appear across multiple planes, replacement may be the honest recommendation. Storm-related shingle repairs are quoted as clear private-pay work; we do not manage insurance claims or adjuster meetings.",
            ),
            (
                "Choose a Shingle System With Local Support",
                "Roof Monsters is family-owned since 1988, headquartered in Dunedin, and licensed under CCC1335398, CCC052490, and CBC015719. We help homeowners compare Atlas profiles, colors, and warranty terms before ordering materials. View examples in the <a href=\"/gallery/\">gallery</a>, read about <a href=\"/warranty-guarantee/\">warranty coverage</a>, or call <a href=\"tel:7274393869\">(727) 439-3869</a> for a free inspection for Tampa Bay homes.",
            ),
        ],
    },
    "metal-roofing": {
        "paragraphs": [
            "Metal roofing reflects heat and can outperform aging shingle systems on structures that support the load. We install and repair standing-seam and panel systems suited to Florida wind exposure when the building is a good candidate.",
            "Not every home should switch to metal — we compare weight, cost, HOA rules, and noise before recommending it over Atlas shingles. Honest guidance keeps you from investing in the wrong system.",
            "Repairs include fastener checks, seam resealing, and panel replacement after storm impact. We document whether damage is isolated or a sign of wider attachment issues.",
        ],
        "process": [
            ("Structural review", "We confirm decking and framing can support metal or identify lighter alternatives."),
            ("System selection", "Panel type, color, and fastening strategy for your exposure and architecture."),
            ("Install or repair", "Licensed crews complete flashing transitions at walls and penetrations."),
            ("Maintenance guidance", "Fastener and coating checks to extend system life."),
        ],
        "includes": [
            ("Panel installation", "New metal systems on qualifying structures."),
            ("Storm damage repair", "Panel replacement and seam corrections after wind events."),
            ("Flashing transitions", "Wall, chimney, and penetration details that stop metal-to-shingle leaks."),
            ("Comparison estimates", "Metal vs. Atlas shingle options when both are viable."),
        ],
        "signs": [
            "Repeated shingle replacement on a low-pitch plane that struggles in wind",
            "Desire for longer service life and heat reflection",
            "HOA-approved metal profiles for architectural style homes",
            "Loose fasteners or oil-canning on an existing metal roof",
            "Storm dents or lifted seams after hail or wind",
        ],
        "faqs": [
            ("Is metal louder than shingles?", "Proper underlayment and attic insulation minimize noise; we discuss expectations during consultation."),
            ("Does metal rust near the coast?", "Coatings and marine-aware selections matter — we specify materials suited to salt exposure when applicable."),
            ("Can metal be installed over shingles?", "Sometimes — deck condition and code must allow it; we inspect before recommending overlay."),
            ("Is metal more expensive than shingles?", "Upfront cost is often higher; we compare lifecycle and goals in your written estimate."),
            ("Do you repair existing metal roofs?", "Yes — fastener, seam, and panel repairs are common after Florida storms."),
        ],
        "why": [
            ("Honest Comparison", "Metal recommended only when it fits structure, budget, and HOA rules."),
            ("Wind-Aware Details", "Florida fastening and flashing transitions."),
            ("Repair & Install", "Storm panel work and new system installs."),
            ("Licensed Crews", "Family-owned Tampa Bay contractor since 1988."),
        ],
        "guide_sections": [
            (
                "When Metal Roofing Is a Good Fit",
                "Metal roofing can be a strong long-term option for Florida properties that want reflectivity, wind performance, and a different architectural look. It is not automatically the best choice for every home. We review structure, pitch, deck condition, HOA rules, budget, noise expectations, and existing roof transitions before recommending metal over Atlas shingles. A clear comparison prevents homeowners from paying for a system that does not fit the building.",
            ),
            (
                "Coastal Exposure and Material Selection",
                "Tampa Bay roofs face salt air, humidity, heat cycling, and fast-moving storms. Metal systems need compatible fasteners, coatings, trims, and flashing details that account for expansion and corrosion risk. We pay close attention to wall transitions, valleys, penetrations, and edges where wind can start lifting panels. The same Florida licensing standards apply: CCC1335398, CCC052490, and CBC015719 for qualifying roofing and building work.",
            ),
            (
                "Metal Roof Repair After Storms",
                "Existing metal roofs often need fastener replacement, seam resealing, panel correction, or flashing repair after wind and debris impact. Dents alone may be cosmetic, while lifted seams or punctures can admit water quickly during the next thunderstorm. We document whether damage is isolated or connected to wider attachment issues. Storm repairs are private-pay scopes with written pricing; we do not manage insurance claims or adjuster meetings.",
            ),
            (
                "Comparing Metal With Atlas Shingles",
                "Metal usually carries a higher upfront cost than shingle roofing, so the decision should consider lifecycle goals, appearance, HOA approval, attic heat, and future maintenance. Atlas shingles remain a practical steep-slope choice for many Tampa Bay homes, especially when ventilation and flashing are corrected during replacement. We present both paths when both are viable, then explain warranty terms and qualifying workmanship coverage before materials are ordered.",
            ),
            (
                "Ask for a Straight Recommendation",
                "Roof Monsters has been family-owned since 1988, and referrals depend on honest recommendations, not forcing every homeowner into the most expensive system. If metal is right, we will explain why; if a shingle replacement or repair is smarter, we will say that too. Call <a href=\"tel:7274393869\">(727) 439-3869</a> or compare <a href=\"/services/roof-replacement/\">roof replacement</a> options.",
            ),
        ],
    },
    "tile-roofing": {
        "paragraphs": [
            "Tile roofs are common across coastal Pinellas and upscale Hillsborough neighborhoods. Underlayment — not just the tile — is the waterproof layer; aged felt under tile often fails before tiles look worn.",
            "We handle broken tile replacement, ridge repairs, and full tear-offs when underlayment is exhausted. Matching profiles and colors keeps HOA and architectural consistency.",
            "After storms, lifted tiles and cracked hips expose underlayment to UV and rain. Prompt repair prevents decking damage that turns a tile swap into a major project.",
        ],
        "process": [
            ("Tile & underlayment inspection", "We assess whether damage is cosmetic tile or failed substrate."),
            ("Scope recommendation", "Spot repair, partial re-tile, or full system replacement with clear pricing."),
            ("Code-compliant install", "Fastening and underlayment suited to Florida wind zones."),
            ("Cleanup & walk-through", "Broken tile haul-off and final review with you."),
        ],
        "includes": [
            ("Broken tile replacement", "Matching profiles on qualifying systems."),
            ("Underlayment tear-off", "Full system replacement when felt or synthetic barrier failed."),
            ("Ridge & hip repair", "Mortar or mechanical ridge details restored after wind."),
            ("Storm documentation", "Photos for your records — private-pay repair focus."),
        ],
        "signs": [
            "Cracked or slid tiles after wind events",
            "Water stains with intact-looking tile above",
            "Ridge mortar missing on hips and peaks",
            "Tile roof past 25–30 years with unknown underlayment age",
            "HOA notice requiring tile repair or replacement",
        ],
        "faqs": [
            ("Can you match my existing tile?", "We source compatible profiles and colors when available for your system."),
            ("Do tile roofs leak at the tile?", "Usually at underlayment, flashings, or penetrations — we inspect both tile and substrate."),
            ("Is tile heavier than shingles?", "Yes — structure must support it; we note decking concerns during inspection."),
            ("How long does tile repair take?", "Small repairs may finish in a day; full re-tile depends on square footage and weather."),
            ("Do you replace underlayment without replacing every tile?", "Sometimes — scope depends on access and underlayment condition; we explain options in writing."),
        ],
        "why": [
            ("Underlayment Focus", "We fix the waterproof layer, not only cosmetic tile."),
            ("Storm Experience", "Post-wind tile and ridge repairs across Tampa Bay."),
            ("HOA Awareness", "Profiles and colors suited to neighborhood standards."),
            ("Written Estimates", "Repair vs. replacement explained before work begins."),
        ],
        "guide_sections": [
            (
                "Tile Is Not the Waterproof Layer",
                "Tile roofs look durable because the visible surface is concrete or clay, but the underlayment and flashing do the waterproofing. In coastal Pinellas and Hillsborough neighborhoods, tile can look acceptable while aged felt below it has become brittle. We inspect broken tiles, slipped pieces, ridge details, valleys, and signs of underlayment failure before recommending repair or replacement. That prevents cosmetic tile work from hiding a continuing leak.",
            ),
            (
                "Matching Tile and HOA Expectations",
                "Tile repairs often require matching profile, color, and exposure so the roof still fits the home and neighborhood requirements. Availability can vary, especially on older communities where the original tile line is discontinued. We explain match limitations before work begins and provide written scopes for repair, partial replacement, or full tear-off. HOA documentation can be included when material selections or roof appearance need approval.",
            ),
            (
                "Storm Damage on Tile Roofs",
                "Wind can lift ridge tiles, slide field tiles, crack hips, or expose underlayment to ultraviolet light and heavy rain. Walking tile incorrectly can also create new breaks, so inspection technique matters. We provide private-pay storm repair estimates with photos for your records and do not manage insurance claims or adjuster meetings. Permanent repair focuses on restoring the water-shedding system, not only replacing the most visible cracked pieces.",
            ),
            (
                "Structure, Underlayment, and Licensing",
                "Tile is heavier than asphalt shingles and requires structure that can support it. When a tile roof needs replacement, we review deck condition, fastening, underlayment options, flashing, and code requirements before rebuilding the system. Roof Monsters operates under roofing licenses CCC1335398 and CCC052490 plus building license CBC015719. Our 15-year workmanship warranty applies on qualifying installation labor, with terms reviewed in the written estimate.",
            ),
            (
                "Plan Tile Work Before Leaks Spread",
                "Tile roof leaks can travel under the field before staining a ceiling, so early inspection is valuable when you notice slipped pieces or missing ridge mortar. Roof Monsters is headquartered in Dunedin and family-owned since 1988. Browse related <a href=\"/services/roof-leak-repair/\">leak repair</a>, see examples in the <a href=\"/gallery/\">gallery</a>, or call <a href=\"tel:7274393869\">(727) 439-3869</a>.",
            ),
        ],
    },
    "flat-roofing": {
        "paragraphs": [
            "Flat and low-slope roofs rely on positive drainage and intact membranes. Ponding water accelerates seam failure in Florida heat — we check slopes, drains, and crickets around HVAC curbs.",
            "Residential flat sections over porches and additions often tie into shingle roofs. Transition flashings are a frequent leak point we correct during repair or recover projects.",
            "When recover is not viable, tear-off to decking exposes hidden rot early. We include decking repairs in written estimates before membrane install begins.",
        ],
        "process": [
            ("Drainage assessment", "Ponding, drain clearance, and curb heights reviewed."),
            ("Membrane evaluation", "Seams, attachment, and insulation condition documented."),
            ("Repair or replace", "Targeted patches or full system install with written scope."),
            ("Maintenance plan", "Seasonal checks to extend membrane life."),
        ],
        "includes": [
            ("Leak repair", "Seam, curb, and penetration patches on qualifying membranes."),
            ("Full replacement", "Tear-off and new low-slope system when recover is not advised."),
            ("Drain & cricket work", "Improved flow away from HVAC and parapet walls."),
            ("Shingle transitions", "Flashing where flat meets steep-slope roofs."),
        ],
        "signs": [
            "Standing water 48 hours after rain",
            "Bubbling or splitting membrane seams",
            "Interior leaks at flat roof corners",
            "Previous patch layers failing repeatedly",
            "Soft spots when walking near drains or curbs",
        ],
        "faqs": [
            ("What flat roof types do you work on?", "We evaluate modified bitumen, TPO, and other low-slope systems common in Tampa Bay."),
            ("Can you fix ponding without replacement?", "Sometimes — crickets, drains, or localized re-slope may help; we inspect before recommending."),
            ("How long do flat roofs last?", "Depends on membrane, drainage, and maintenance; we document condition during free inspections."),
            ("Is TPO the same as flat roofing?", "TPO is a popular flat membrane — see our TPO page for commercial-focused detail."),
            ("Do you work on porch flat sections?", "Yes — small residential low-slope areas tied to shingle roofs are common repairs."),
        ],
        "why": [
            ("Drainage First", "Ponding and curb issues addressed before membrane work."),
            ("Transition Expertise", "Where flat meets shingle is a common leak zone."),
            ("TPO Options", "Commercial-grade membranes on qualifying decks."),
            ("Clear Scopes", "Recover vs. tear-off explained in writing."),
        ],
        "guide_sections": [
            (
                "Flat Roofs Fail Around Water",
                "Flat and low-slope roofs are really drainage systems. In Florida heat, ponding water stresses seams, softens old patch materials, and accelerates membrane wear around drains, scuppers, and HVAC curbs. We check whether water has a path off the roof and whether previous repairs are trapping moisture. A patch can help a localized puncture, but it will not solve a slope problem that leaves water standing after every afternoon storm.",
            ),
            (
                "Membrane Choices and Existing Conditions",
                "Flat roofing may involve TPO, modified bitumen, older built-up systems, or small residential porch membranes tied into shingles. Before recommending recover or replacement, we look at deck condition, insulation moisture, seam strength, attachment, and the number of old patch layers. Wet insulation or soft decking often makes tear-off the better value. Written estimates separate repairs, drainage improvements, and full membrane work so owners can compare options clearly.",
            ),
            (
                "Where Flat Roofs Meet Shingles",
                "Many Tampa Bay homes leak where a low-slope addition, porch, or commercial-style section meets a steep-slope shingle roof. That transition needs flashing, counterflashing, and compatible materials that move water away from the joint. On qualifying steep-slope areas we use Atlas shingles, while the low-slope side may need membrane-specific repair. Treating both sides together prevents one trade from blaming the other while water keeps entering.",
            ),
            (
                "Maintenance in Florida Heat",
                "Flat roof maintenance should include clearing drains, checking seams, inspecting around rooftop equipment, and looking for blisters, splits, or soft spots. Summer heat expands materials during the day and sudden storms cool them quickly, a cycle that exposes weak details. If storm damage creates an active opening, we provide private-pay emergency protection and permanent repair pricing. We do not manage insurance claims or adjuster meetings.",
            ),
            (
                "Get a Low-Slope Assessment",
                "Roof Monsters serves residential and commercial flat roofing clients from Dunedin with Florida licenses CCC1335398, CCC052490, and CBC015719. Family-owned since 1988, we focus on drainage, clear scopes, and repair-versus-replacement honesty. Read more about <a href=\"/services/tpo-roofing/\">TPO roofing</a>, compare <a href=\"/services/commercial-roofing/\">commercial roofing</a>, or call <a href=\"tel:7274393869\">(727) 439-3869</a> for Tampa Bay properties.",
            ),
        ],
    },
    "tpo-roofing": {
        "paragraphs": [
            "TPO membranes are reflective, heat-welded, and common on Tampa Bay retail, office, and multi-family buildings. Seam strength and attachment to deck matter in high wind and afternoon heat cycles.",
            "We inspect insulation for moisture before recommending overlay. Wet insulation reduces R-value and can blister new membrane from below — tear-off may be the better long-term value.",
            "Repairs use compatible TPO patches and heat welding. Chronic seam failure often signals wider attachment or drainage issues we document before quoting another patch.",
        ],
        "process": [
            ("Core & moisture checks", "Insulation and deck condition inform recover vs. tear-off."),
            ("Attachment plan", "Mechanical or adhesive patterns suited to building height and exposure."),
            ("Welded install", "Seams and flashings completed to manufacturer specs."),
            ("Warranty & maintenance", "Manufacturer terms reviewed; maintenance intervals recommended."),
        ],
        "includes": [
            ("New TPO install", "Full tear-off or recover when deck and insulation allow."),
            ("Seam & penetration repair", "Heat-welded patches at leaks and HVAC curbs."),
            ("Insulation assessment", "Wet board replacement scoped before new membrane."),
            ("Drainage review", "Flow paths and crickets around rooftop equipment."),
        ],
        "signs": [
            "Membrane seams separating or pulling at walls",
            "Energy bills rising with aging dark roof surface",
            "Multiple patch areas failing within a year",
            "Building sale or refinance requiring roof documentation",
            "Ponding that never clears near rooftop units",
        ],
        "faqs": [
            ("What is TPO roofing?", "Thermoplastic polyolefin — a white, heat-welded membrane common on commercial low-slope roofs."),
            ("How long does TPO last?", "Service life depends on installation quality, drainage, and maintenance; we document realistic expectations per property."),
            ("Can TPO go over an old roof?", "Recover is possible when deck and insulation are dry and code allows — we inspect first."),
            ("Is TPO good for Florida heat?", "Reflectivity helps reduce heat load; attachment and seam work must suit wind exposure."),
            ("Do you repair TPO without replacement?", "Yes — welded patches address many localized failures when substrate is sound."),
        ],
        "why": [
            ("Commercial Focus", "Low-slope planning for businesses and multi-unit properties."),
            ("Heat-Welded Seams", "Manufacturer-consistent TPO detailing."),
            ("Insulation Honesty", "Wet board identified before recover is recommended."),
            ("Maintenance Mindset", "Inspection notes for property managers and owners."),
        ],
        "guide_sections": [
            (
                "Why TPO Fits Many Florida Buildings",
                "TPO roofing is common on Tampa Bay commercial and multi-family properties because the reflective membrane helps reduce heat load and the seams are heat-welded rather than glued like some older systems. It is still only as good as the deck, insulation, attachment, and drainage below it. We evaluate the whole assembly before recommending a new TPO install, recover, or targeted repair, especially on buildings with rooftop HVAC equipment.",
            ),
            (
                "Seams, Curbs, and Heat Cycling",
                "TPO leaks often show up at seams, wall terminations, drains, and HVAC curbs. Florida heat expands the membrane, afternoon storms cool it rapidly, and wind can stress edges if attachment is weak. We inspect weld quality, flashing height, membrane pull, and ponding patterns before quoting repairs. A single patch may solve a puncture, but repeated seam failures usually point to a broader installation or drainage issue.",
            ),
            (
                "Insulation Moisture Changes the Scope",
                "Recovering an old roof with new TPO can be efficient only when the existing deck and insulation are dry and code allows the assembly. Wet insulation reduces performance, traps moisture under the new membrane, and can create blistering or odor problems later. We check for moisture indicators and explain when tear-off is the responsible recommendation. Written commercial scopes help owners budget the work instead of inheriting hidden wet board.",
            ),
            (
                "Repair and Maintenance Planning",
                "TPO repairs should use compatible membrane and proper welding techniques. Maintenance should include drain clearing, seam checks, curb inspection, and prompt attention to punctures from service traffic. After storms, we provide private-pay emergency protection and permanent repair estimates when a membrane is opened. We do not manage insurance claims or adjuster meetings. Roof Monsters performs qualifying work under CCC1335398, CCC052490, and CBC015719.",
            ),
            (
                "Talk With a Local TPO Roofer",
                "Property managers and owners need roofers who communicate access, staging, and documentation clearly. Roof Monsters is family-owned since 1988 and based in Dunedin, serving Tampa Bay commercial properties with low-slope roofing experience. Compare <a href=\"/services/flat-roofing/\">flat roofing</a>, review <a href=\"/services/commercial-roofing/\">commercial roofing</a>, or call <a href=\"tel:7274393869\">(727) 439-3869</a> for a free inspection.",
            ),
        ],
    },
    "roof-maintenance": {
        "paragraphs": [
            "Maintenance is cheaper than emergency tarping. Seasonal checks catch lifted shingles, clogged valleys, and attic moisture before they become ceiling stains.",
            "Florida sun bakes sealant at penetrations faster than northern climates. Re-flashing and small shingle fixes during maintenance visits extend roof life between replacements.",
            "We pair maintenance findings with written repair quotes — you choose what to fix now vs. budget for later. No pressure to bundle unnecessary work.",
        ],
        "process": [
            ("Roof & attic walk", "Shingles, flashings, ventilation, and interior signs reviewed."),
            ("Maintenance report", "Photos and notes of items to monitor or repair."),
            ("Quoted repairs", "Optional written estimates for issues found during the visit."),
            ("Seasonal follow-up", "Schedule the next check before storm season or after major weather."),
        ],
        "includes": [
            ("Debris & valley check", "Clearing paths that trap water under shingles."),
            ("Flashing inspection", "Pipe boots, walls, chimneys, and skylight seals."),
            ("Ventilation review", "Blocked soffits and exhaust balance noted."),
            ("Repair quotes", "Optional fixes with clear pricing — no automatic upsells."),
        ],
        "signs": [
            "It has been years since anyone walked the roof",
            "Trees deposit debris in valleys each season",
            "You want to avoid surprise leaks before hurricane season",
            "Recent home purchase with unknown roof history",
            "Small issues noted but not yet leaking inside",
        ],
        "faqs": [
            ("How often should I maintain my roof in Florida?", "Many homeowners schedule annual or pre-storm-season checks; coastal and tree-heavy lots may need more frequent visits."),
            ("Is maintenance the same as an inspection?", "Maintenance includes proactive checks and minor clearing; inspections focus on condition documentation for decisions."),
            ("Do you maintain flat and shingle roofs?", "Yes — low-slope membranes and steep-slope shingles are evaluated differently during the same visit."),
            ("Will you try to sell a new roof on every visit?", "No — we recommend repairs when they make sense and document replacement timing honestly."),
            ("Can maintenance prevent insurance issues?", "We do not manage claims; documented maintenance helps you understand condition before storms."),
        ],
        "why": [
            ("Prevent Leaks", "Catch small issues before interior damage."),
            ("Storm Readiness", "Pre-season checks across Tampa Bay."),
            ("Honest Reports", "Photos and notes without unnecessary upsells."),
            ("Atlas Familiarity", "Maintenance on Atlas and mixed systems."),
        ],
        "guide_sections": [
            (
                "Why Maintenance Matters in Florida",
                "Florida roofs age between storms, not only during them. Sun bakes sealants, humidity supports algae, oak debris blocks valleys, and afternoon downpours test every flashing detail. Roof maintenance catches small problems before they become emergency tarps or interior drywall repairs. A seasonal check is especially useful before hurricane season, after heavy tree shedding, or when you have inherited a home and do not know who last inspected the roof.",
            ),
            (
                "What We Look For During a Visit",
                "A maintenance visit can include checking lifted shingles, pipe boots, wall flashings, ridge cap, valley debris, gutter edges, attic moisture, and ventilation paths when accessible. On low-slope roofs we look at seams, drains, ponding, and rooftop equipment curbs. We photograph findings and separate items to monitor from items that deserve repair now. That written report helps homeowners and property managers budget instead of reacting to leaks.",
            ),
            (
                "Atlas and Mixed-System Maintenance",
                "On Atlas shingle systems, maintenance protects the installation details that support manufacturer coverage and workmanship expectations: ventilation, ridge cap, flashing, and prompt repair of storm damage. We also maintain mixed systems where shingles meet flat membranes, tile, metal, skylights, or gutters. Those transitions often fail before the main field does. Catching them early can extend roof life and protect qualifying 15-year workmanship coverage on installation labor.",
            ),
            (
                "Storm Readiness Without Claim Promises",
                "Maintenance before storm season is practical preparation, not insurance claim work. We do not manage claims, meet adjusters, or promise payout outcomes. We identify weak points, quote repairs as private-pay scopes, and document conditions for your own records. If a storm later creates an active opening, emergency tarping is temporary protection and should be followed by permanent repair once weather allows safe work.",
            ),
            (
                "Set a Maintenance Baseline",
                "Roof Monsters is family-owned since 1988, headquartered in Dunedin, and licensed under CCC1335398, CCC052490, and CBC015719. A maintenance baseline helps you decide what to fix now and what to watch through the next rainy season. Learn about <a href=\"/services/roof-repair/\">roof repair</a>, review <a href=\"/services/roof-ventilation/\">ventilation</a>, or call <a href=\"tel:7274393869\">(727) 439-3869</a>.",
            ),
        ],
    },
    "roof-ventilation": {
        "paragraphs": [
            "Attic heat cooks shingles from underneath. Balanced intake at soffits and exhaust at ridge or fans lowers temperature and moisture that shorten roof life in Florida.",
            "Signs of poor ventilation include curling shingles, mold in attics, and high upstairs cooling bills. We measure airflow paths during replacement and standalone ventilation projects.",
            "Ventilation upgrades pair naturally with re-roofs — opening decking for ridge vent is easier during tear-off than as a standalone retrofit, though both are possible.",
        ],
        "process": [
            ("Attic assessment", "Intake, exhaust, insulation baffles, and moisture signs."),
            ("Design recommendation", "Ridge, soffit, gable, or powered options suited to roof geometry."),
            ("Install during repair or re-roof", "Ventilation integrated with flashing and shingle details."),
            ("Homeowner walk-through", "Explain what changed and what to monitor seasonally."),
        ],
        "includes": [
            ("Ridge vent install", "Exhaust at peak on qualifying shingle replacements."),
            ("Soffit intake review", "Blocked or insufficient intake corrected when possible."),
            ("Baffle & insulation gaps", "Paths that keep insulation from choking soffit vents."),
            ("Moisture documentation", "Attic photos when ventilation may be driving shingle wear."),
        ],
        "signs": [
            "Upstairs rooms hot despite AC running constantly",
            "Curling shingle edges on south-facing planes",
            "Mold or mildew odor in attic spaces",
            "Frost or condensation on decking in cooler months",
            "No visible ridge or soffit venting on an older home",
        ],
        "faqs": [
            ("Does poor ventilation void shingle warranties?", "Manufacturer warranties often require adequate ventilation — we document airflow during Atlas installs."),
            ("Can you add ventilation without replacing the roof?", "Sometimes — options depend on roof geometry; we inspect before recommending retrofit."),
            ("Are powered attic fans worth it?", "Depends on intake balance and attic volume; we explain pros and cons for your home."),
            ("Is ventilation required by Florida code?", "Code and manufacturer specs both matter; permitted work follows applicable requirements."),
            ("Will better ventilation lower my bills?", "Many homeowners see improved comfort upstairs; results vary with insulation and AC condition."),
        ],
        "why": [
            ("Shingle Life", "Heat and moisture control protects Atlas systems."),
            ("Attic Science", "Balanced intake and exhaust, not just more holes."),
            ("Re-Roof Integration", "Best time to fix airflow is during tear-off."),
            ("Comfort Gains", "Cooler upstairs rooms and less attic moisture."),
        ],
        "guide_sections": [
            (
                "Balanced Airflow Protects the Roof",
                "Roof ventilation is about balanced intake and exhaust, not simply adding more vents. In Tampa Bay heat, trapped attic air can cook shingles from below, drive moisture into decking, and make upstairs rooms uncomfortable. Soffit intake, ridge exhaust, baffles, insulation depth, and roof geometry all affect performance. We inspect airflow paths before recommending ridge vents, soffit corrections, powered options, or ventilation upgrades during replacement.",
            ),
            (
                "Signs Ventilation Is Part of the Problem",
                "Homeowners often call about curling shingles, algae-heavy roof planes, hot bedrooms, musty attic odor, or high cooling bills. Those symptoms can point to ventilation, but they can also involve insulation, HVAC, roof age, or leaks. We document what is visible in the attic and on the roof so the recommendation is specific. Adding exhaust without intake can make problems worse by pulling conditioned air from the home.",
            ),
            (
                "Best Time to Upgrade Ventilation",
                "The best time to correct roof ventilation is during a re-roof, when decking is open and ridge cuts, baffles, intake paths, and underlayment can be coordinated cleanly. Standalone retrofits are sometimes possible, but access and roof geometry limit options. On qualifying Atlas shingle installs, ventilation supports product performance and warranty expectations. Our 15-year workmanship warranty covers qualifying installation labor, including ventilation details within the contracted scope.",
            ),
            (
                "Florida Climate and Moisture Control",
                "Humidity makes ventilation a year-round concern. Warm, damp attic air can condense during cooler weather, while summer heat accelerates shingle aging and stresses roof sealants. Coastal homes may also deal with salt air and wind-driven rain entering weak intake or exhaust details. We focus on durable, code-aware solutions under Florida licenses CCC1335398, CCC052490, and CBC015719, with written estimates before work begins.",
            ),
            (
                "Ask for an Attic Airflow Review",
                "Roof Monsters is family-owned since 1988 and based in Dunedin, serving Tampa Bay homeowners who want practical roofing guidance without guesswork. If your upstairs stays hot or shingles are aging early, schedule a ventilation review before replacing materials blindly. Compare <a href=\"/services/roof-replacement/\">roof replacement</a>, read about <a href=\"/services/shingle-roofing/\">Atlas shingle roofing</a>, or call <a href=\"tel:7274393869\">(727) 439-3869</a>.",
            ),
        ],
    },
}


def default_expansion(p: dict) -> dict:
    label = p["slug"].replace("-", " ")
    return {
        "process": [
            ("Consultation", f"We discuss your {label} goals, property type, and timeline during a free inspection when applicable."),
            ("Clear scope", "You receive a written estimate that explains materials, labor, and warranty coverage before work starts."),
            ("Licensed completion", "Our Florida-licensed crews complete the work, walk the site with you, and leave the property clean."),
        ],
        "paragraphs": [
            f"{p['lead']} Gulf Coast heat, afternoon storms, and salt air near the bay all stress roofing systems in Pasco, Pinellas, Hernando, Hillsborough, and Manatee County. A walk-the-roof inspection with attic notes beats guessing from a ceiling stain alone.",
            p["body"] + " Contact our Dunedin team for honest guidance — most of our work comes from neighbors who recommend us. We photograph problem areas and explain tradeoffs before you commit.",
            f"Whether you need {label} on a single-family home, multi-unit property, or light commercial building, we schedule around access constraints and leave the site clean. Written estimates list materials, labor, and warranty coverage up front.",
        ],
        "includes": [
            ("Licensed crews", "Florida roofing and building licenses CCC1335398, CCC052490, CBC015719."),
            ("Written estimates", "Clear scopes before work begins — no surprise add-ons."),
            ("Atlas materials", "Designer shingles on qualifying steep-slope projects."),
            ("15-year workmanship", "Installation labor warranty on qualifying projects."),
            ("Photo documentation", "Condition photos for your records before and after work when applicable."),
        ],
        "signs": [
            f"Visible wear or damage related to {label}",
            "Storm season approaching with an aging roof",
            "Neighbor referrals pointing you to a second opinion",
            "Interior stains or attic moisture after rain",
            "HOA or buyer requesting a roof condition review",
            "High upstairs heat suggesting weak attic ventilation",
        ],
        "faqs": [
            (f"Do you serve all of Tampa Bay for {label}?", "Yes — we are headquartered in Dunedin and serve all five counties published on roofmonsters.co."),
            ("Are estimates free?", "Inspections and estimates are free for qualifying residential and commercial roofing inquiries."),
            ("What licenses does Roof Monsters hold?", "Roofing CCC1335398, CCC052490 and building CBC015719 — Terrance McKeever Enterprises, Inc. DBA Roof Monsters."),
            ("How do I schedule an inspection?", "Call (727) 439-3869, email info@roofmonsters.co, or use the form on this page."),
            ("Do you work with insurance adjusters?", "No. We provide private-pay emergency response and repairs with clear written estimates."),
            ("What materials do you install?", "On qualifying steep-slope projects we install Atlas Designer Shingles. Manufacturer coverage follows Atlas terms."),
            ("Do you pull permits?", "Yes — permitted work is part of proper Florida replacements on qualifying projects."),
        ],
        "why": [
            ("Family-Owned", "Serving Tampa Bay since 1988 with the same quality standards."),
            ("Atlas Focus", "Designer shingles on qualifying steep-slope installs."),
            ("Clear Estimates", "Written scopes before work begins."),
            ("Neighbor Trust", "Most work comes from referrals across the bay area."),
        ],
    }


def merge_expansion(p: dict) -> dict:
    data = {**default_expansion(p), **SERVICE_EXPANSIONS.get(p["slug"], {})}
    for key in ("paragraphs", "process", "includes", "signs", "faqs", "why"):
        if key in SERVICE_EXPANSIONS.get(p["slug"], {}):
            data[key] = SERVICE_EXPANSIONS[p["slug"]][key]
    return data


def mini_stats_block() -> str:
    return """
  <div class="mini-stats-banner" data-countup>
    <div class="container mini-stats-inner">
      <div>
        <div class="mini-stat-num" data-target="40" data-suffix=" Years">40 Years</div>
        <div class="mini-stat-label">Roofing Experience</div>
      </div>
      <div>
        <div class="mini-stat-num" data-target="5">5</div>
        <div class="mini-stat-label">Counties Served</div>
      </div>
      <div>
        <div class="mini-stat-num" data-target="30" data-suffix=" +" data-rm-live-review-count data-rm-live-review-suffix=" +">30 +</div>
        <div class="mini-stat-label">Google Reviews</div>
      </div>
    </div>
  </div>"""


def why_choose_block(p: dict, data: dict) -> str:
    cards = "".join(
        f"""
        <div class="why-card">
          <div class="why-num">{i:02d}</div>
          <h4>{esc(title)}</h4>
          <p>{esc(body)}</p>
        </div>"""
        for i, (title, body) in enumerate(data["why"], start=1)
    )
    return f"""
  <section class="why-choose-section section-pad">
    <div class="container">
      <div class="section-header">
        <span class="section-eyebrow">Why Roof Monsters</span>
        <h2>Why Choose Us for <span class="accent">{esc(p["eyebrow"])}</span></h2>
        <p class="section-desc">Family-owned since 1988 — licensed, referral-trusted, and focused on clear written estimates across Tampa Bay.</p>
      </div>
      <div class="why-choose-grid">
        {cards}
      </div>
    </div>
  </section>"""


def service_guide_block(p: dict, data: dict) -> str:
    """Long-form unique guide so service pages are not thin near-duplicates."""
    label = p["eyebrow"]
    slug = p["slug"]
    lead = p["lead"]
    body = p["body"]
    guides = data.get("guide_sections") or [
        (
            f"When {label} Makes Sense in Tampa Bay",
            f"{lead} Gulf Coast heat, afternoon thunderstorms, and salt air near the bay all stress roofing systems "
            f"across Pasco, Pinellas, Hernando, Hillsborough, and Manatee County. Homeowners usually call after "
            f"seeing stains, missing shingles, or a second opinion that feels unclear — we document conditions with "
            f"photos and explain repair versus replacement in plain language.",
        ),
        (
            "Florida Climate, Materials, and Workmanship",
            f"{body} On qualifying steep-slope projects we install Atlas Designer Shingles — including Scotchgard™ "
            f"protection on qualifying products — because they are engineered for heat, wind, and humidity. "
            f"Manufacturer coverage follows Atlas terms. Our 15-year workmanship warranty covers qualifying "
            f"installation labor. Licenses CCC1335398, CCC052490, and CBC015719 apply on every job.",
        ),
        (
            "What to Expect From Inspection to Final Walkthrough",
            f"We walk the roof and attic when accessible, note ventilation and flashing details, and provide a "
            f"written estimate before work begins. Permitting is coordinated on qualifying replacements. Crews "
            f"protect landscaping, haul debris, and complete magnetic nail sweeps on qualifying tear-offs. "
            f"If decking repairs appear after tear-off, we document them and confirm pricing before continuing.",
        ),
        (
            "Buying, Selling, or Preparing for Storm Season",
            f"If you are listing or purchasing a home, a documented roof inspection helps you plan capital work "
            f"instead of inheriting surprises. Before hurricane season, we catch lifted tabs, dried flashing "
            f"sealant, and clogged valleys. Storm openings get private-pay emergency tarping and permanent repairs "
            f"with clear estimates — we do not manage insurance claims or adjuster meetings.",
        ),
        (
            "Why Neighbors Refer Roof Monsters",
            f"Family-owned since 1988 and headquartered in Dunedin, most of our {label.lower()} work still comes "
            f"from referrals. Explore related services, browse our <a href=\"/gallery/\">project gallery</a>, or "
            f"see <a href=\"/about-us/locations-we-serve/\">locations we serve</a>. Call "
            f"<a href=\"tel:7274393869\">(727) 439-3869</a> or email "
            f"<a href=\"mailto:info@roofmonsters.co\">info@roofmonsters.co</a>.",
        ),
    ]
    # Allow HTML in last guide section links — escape others
    parts = []
    for i, (title, text) in enumerate(guides):
        if i == len(guides) - 1 and "<a href=" in text:
            parts.append(f"<h3>{esc(title)}</h3>\n      <p>{text}</p>")
        else:
            parts.append(f"<h3>{esc(title)}</h3>\n      <p>{esc(text)}</p>")
    return f"""
  <section class="section-pad">
    <div class="container content-page service-rich-content">
      <div class="section-header">
        <span class="section-eyebrow">{esc(label)} Guide</span>
        <h2>Local Expertise for {esc(label)}</h2>
        <p class="section-desc">Practical detail for Tampa Bay property owners — climate, materials, process, and honest repair-versus-replace guidance from a Dunedin-based contractor.</p>
      </div>
      {"".join(parts)}
    </div>
  </section>"""


def rich_content_block(p: dict, data: dict) -> str:
    includes = "".join(
        f"""
        <div class="benefit-item"><i class="fa-solid fa-check-circle"></i><p><strong>{esc(title)}</strong> — {esc(body)}</p></div>"""
        for title, body in data["includes"]
    )
    signs = "".join(f"\n          <li>{esc(sign)}</li>" for sign in data["signs"])
    return f"""
  <section class="section-pad section-bg-white">
    <div class="container content-page service-rich-content">
      <div class="section-header">
        <span class="section-eyebrow">Scope &amp; Value</span>
        <h2>What&apos;s Included in {esc(p["eyebrow"])}</h2>
        <p class="section-desc">Licensed Tampa Bay roofing with Atlas materials on qualifying projects, written estimates, and workmanship warranty coverage on qualifying installation labor.</p>
      </div>
      <div class="benefits-list">
        {includes}
      </div>
      <h3 class="u-mt-20">Signs You May Need {esc(p["eyebrow"])}</h3>
      <ul class="service-signs-list">
        {signs}
      </ul>
      <p class="u-mt-20">We serve Pasco, Pinellas, Hernando, Hillsborough, and Manatee County from our Dunedin headquarters. Explore <a href="/about-us/locations-we-serve/">all service areas</a> or call <a href="tel:7274393869">(727) 439-3869</a> to schedule a free inspection.</p>
    </div>
  </section>
{service_guide_block(p, data)}"""


def expansion_block(p: dict) -> str:
    data = merge_expansion(p)
    process_cards = "".join(
        f"""
        <div class="benefit-item"><i class="fa-solid fa-check-circle"></i><p><strong>{esc(title)}</strong> — {esc(body)}</p></div>"""
        for title, body in data["process"]
    )
    paragraphs = "".join(f"<p>{esc(paragraph)}</p>" for paragraph in data["paragraphs"])
    faq_items = "".join(
        f"""
        <article class="faq-item">
          <h2>{esc(question)}</h2>
          <p>{esc(answer)}</p>
        </article>"""
        for question, answer in data["faqs"]
    )
    return f"""
  <section class="service-intro-section service-intro-section--expertise section-pad rm-parallax-section">
    {parallax_bg(p, "detail")}
    <div class="service-intro-overlay" aria-hidden="true"></div>
    <div class="container service-intro-content">
      <span class="section-eyebrow">Florida Roofing Expertise</span>
      <h2>How We Approach {esc(p["eyebrow"])}</h2>
      {paragraphs}
      <h3 class="u-mt-20">Our Process</h3>
      <div class="benefits-list">
        {process_cards}
      </div>
    </div>
  </section>
{rich_content_block(p, data)}
{why_choose_block(p, data)}
{mini_stats_block()}

  <section class="section-pad">
    <div class="container content-page">
      <div class="section-header">
        <span class="section-eyebrow">Common Questions</span>
        <h2>{esc(p["eyebrow"])} <span class="accent">FAQs</span></h2>
      </div>
      <div class="faq-list">
        {faq_items}
      </div>
    </div>
  </section>
"""


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def related_links(items: list) -> str:
    lis = []
    for item in items:
        slug, label = item[0], item[1]
        external = len(item) > 2 and item[2]
        href = f"/{slug}/" if external else f"/services/{slug}/"
        lis.append(f'<li><a href="{href}">{esc(label)}</a></li>')
    return "\n          ".join(lis)


def page_html(p: dict) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <script>
(function () {{
  var path = location.pathname;
  var marker = '/roof-monsters/';
  var idx = path.indexOf(marker);
  window.__RM_BASE__ = idx >= 0 ? path.slice(0, idx + marker.length) : '/';
  document.write('<base href="' + window.__RM_BASE__ + '">');
}})();
  </script>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(p["title"])}</title>
  <meta name="description" content="{esc(p["description"])}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,400;1,700&family=Roboto+Slab:wght@400;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />
  <link rel="stylesheet" href="assets/css/style.css" />
</head>
<body>
  <div id="site-header-include"></div>

  <section class="page-hero">
    <div class="container">
      <h1>{p["h1"]}</h1>
      <nav class="breadcrumb" aria-label="breadcrumb">
        <a href="/">Home</a>
        <i class="fa-solid fa-chevron-right"></i>
        <a href="/services/">Services</a>
        <i class="fa-solid fa-chevron-right"></i>
        <span>{esc(p["slug"].replace("-", " ").title())}</span>
      </nav>
    </div>
  </section>

  <section class="service-intro-section service-intro-section--intro section-pad rm-parallax-section">
    {parallax_bg(p, "main")}
    <div class="service-intro-overlay" aria-hidden="true"></div>
    <div class="container service-intro-grid">
      <div class="service-intro-content">
        <span class="section-eyebrow">{esc(p["eyebrow"])}</span>
        <h2>{p["h1"]}</h2>
        <p>{esc(p["lead"])}</p>
        <p>{esc(p["body"])}</p>
        <ul class="about-trust-row" aria-label="Roof Monsters credentials">
          <li><i class="fa-solid fa-certificate" aria-hidden="true"></i> Licensed &amp; Insured</li>
          <li><i class="fa-solid fa-shield-halved" aria-hidden="true"></i> Atlas Materials</li>
          <li><i class="fa-solid fa-house" aria-hidden="true"></i> Family-Owned Since 1988</li>
          <li><i class="fa-solid fa-clipboard-check" aria-hidden="true"></i> Free Inspection</li>
        </ul>
        <p class="u-mt-20"><strong>Most of our work comes from neighbors who recommend us.</strong> Call or text <a href="tel:7274393869">(727) 439-3869</a> or email <a href="mailto:info@roofmonsters.co">info@roofmonsters.co</a>.</p>
        <div class="about-actions u-mt-20">
          <a href="tel:7274393869" class="btn btn-primary"><i class="fa-solid fa-phone"></i> Call (727) 439-3869</a>
          <a href="contact-us/" class="btn btn-about-call">Request Free Estimate</a>
        </div>
        <h3 class="u-mt-20">Related Services</h3>
        <ul class="rm-cross-links-inline">
          {related_links(p["related"])}
        </ul>
      </div>
      <div class="service-intro-img">
        <img src="assets/images/gallery/{SERVICE_IMAGES.get(p["slug"], "quality-work.webp")}" alt="{esc(p["eyebrow"])} by Roof Monsters in Tampa Bay" />
      </div>
    </div>
  </section>
{expansion_block(p)}
  <section class="service-cta-section">
    <div class="container service-cta-grid">
      <div class="service-cta-content">
        <p class="section-eyebrow">Get Started</p>
        <h2>Clear Estimates. <span class="accent">Local Crews.</span></h2>
        <p>Licenses CCC1335398, CCC052490, CBC015719 · Atlas installs · 15-year workmanship warranty on qualifying projects.</p>
        <div class="cta-features">
          <div class="cta-feature"><i class="fa-solid fa-check-circle"></i> Free roof inspections</div>
          <div class="cta-feature"><i class="fa-solid fa-check-circle"></i> Written estimates</div>
          <div class="cta-feature"><i class="fa-solid fa-check-circle"></i> Referral-trusted since 1988</div>
        </div>
        <a href="tel:7274393869" class="btn btn-primary u-mt-20"><i class="fa-solid fa-phone"></i> Call (727) 439-3869</a>
      </div>
      <div class="cta-form-card">
        <h3>Request a Free Estimate</h3>
        {estimate_form_compact()}
      </div>
    </div>
  </section>

  <div id="site-footer-include"></div>
  <script src="includes.js"></script>
  <script src="assets/js/main.js"></script>
</body>
</html>
"""


def main() -> None:
    for p in PAGES:
        if p["slug"] in SKIP_SLUGS:
            continue
        out = SERVICES / p["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page_html(p), encoding="utf-8")
        print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
