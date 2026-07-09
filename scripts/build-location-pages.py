#!/usr/bin/env python3
"""Generate service area hub and location landing pages from data/service-areas.json."""

from __future__ import annotations

import html
import json
from pathlib import Path

from base_head_script import BASE_HEAD_SCRIPT
from form_snippet import estimate_form_compact
from icon_snippet import icon_head_html
from location_content import guide_for

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "service-areas.json"
HUB = ROOT / "about-us" / "locations-we-serve"
BASE = HUB

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
{base_head}
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
{icon_head}
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,400;1,700&family=Roboto+Slab:wght@400;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />
  <link rel="stylesheet" href="assets/css/style.css" />
</head>
<body>
  <div id="site-header-include"></div>
"""

FOOT = """
  <div id="site-footer-include"></div>
  <script src="includes.js"></script>
  <script src="assets/js/main.js"></script>
</body>
</html>
"""


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def area_url(slug: str) -> str:
    return f"about-us/locations-we-serve/{slug}/"


def cta_block(short: str) -> str:
    return f"""
  <section class="service-cta-section">
    <div class="container service-cta-grid">
      <div class="service-cta-content">
        <p class="section-eyebrow">Get Started</p>
        <h2>Schedule Your Free Roofing Consultation in <span class="accent">{esc(short)}</span></h2>
        <p>Contact Roof Monsters today for a free estimate. We'll inspect your roof, explain your options clearly, and help you protect your property with confidence.</p>
        <div class="cta-features">
          <div class="cta-feature"><i class="fa-solid fa-check-circle"></i> Free roof inspections</div>
          <div class="cta-feature"><i class="fa-solid fa-check-circle"></i> Atlas materials · 15-year workmanship warranty</div>
          <div class="cta-feature"><i class="fa-solid fa-check-circle"></i> Family-owned since 1988 · referral-trusted</div>
        </div>
        <a href="tel:7274393869" class="btn btn-primary u-mt-20"><i class="fa-solid fa-phone"></i> Call (727) 439-3869</a>
      </div>
      <div class="cta-form-card">
        <h3>Request a Free Estimate</h3>
        {estimate_form_compact(address_placeholder=short + " address")}
      </div>
    </div>
  </section>
"""


def local_faq_block(short: str, name: str, faqs: list[tuple[str, str]]) -> str:
    items = "".join(
        f"""
        <article class="faq-item">
          <h2>{esc(question)}</h2>
          <p>{esc(answer)}</p>
        </article>"""
        for question, answer in faqs
    )
    return f"""
  <section class="section-pad section-bg-white">
    <div class="container content-page">
      <div class="section-header">
        <span class="section-eyebrow">{esc(short)} Roofing</span>
        <h2>Local <span class="accent">Questions</span></h2>
        <p class="section-desc">Answers for property owners in {esc(name)} before you request an estimate.</p>
      </div>
      <div class="faq-list">
        {items}
      </div>
      <p class="u-mt-20">Call <a href="tel:7274393869">(727) 439-3869</a> or email <a href="mailto:info@roofmonsters.co">info@roofmonsters.co</a> — headquartered at 1391 Robin Hood Ln, Dunedin, FL 34698.</p>
    </div>
  </section>
"""


def local_guide_block(area: dict, guide: dict) -> str:
    short = area["shortName"]
    sections = "".join(
        f"""
      <h3>{esc(title)}</h3>
      <p>{esc(body)}</p>"""
        for title, body in guide["sections"]
    )
    signs = "".join(f"\n          <li>{esc(sign)}</li>" for sign in guide["signs"])
    secondary = guide["secondary_image"]
    return f"""
  <section class="section-pad">
    <div class="container content-page location-guide">
      <div class="section-header">
        <span class="section-eyebrow">{esc(short)} Roofing Guide</span>
        <h2>{esc(guide["headline"])}</h2>
        <p class="section-desc">Practical local detail for {esc(area["name"])} — climate, common repairs, process, and what to expect from a Dunedin-based Tampa Bay contractor.</p>
      </div>
      <div class="location-guide-layout">
        <div class="location-guide-copy">
          {sections}
          <h3>Signs You May Need Roofing Work in {esc(short)}</h3>
          <ul class="service-signs-list">
            {signs}
          </ul>
          <p class="u-mt-20">Explore <a href="/services/">roofing services</a>, browse the <a href="/gallery/">project gallery</a>, or request a free inspection for your {esc(short)} property.</p>
        </div>
        <figure class="location-guide-media">
          <img src="assets/images/gallery/{secondary}" alt="Roofing work related to {esc(short)} by Roof Monsters" loading="lazy" />
          <figcaption>Licensed Tampa Bay roofing — Atlas materials on qualifying projects · Family-owned since 1988</figcaption>
        </figure>
      </div>
    </div>
  </section>
"""


def services_block(short: str) -> str:
    return f"""
        <!-- rm-cross-links:start -->
        <h3>Roofing Services in {esc(short)}</h3>
        <ul class="rm-cross-links-inline">
          <li><a href="/services/roof-replacement/">Roof Replacement</a></li>
          <li><a href="/services/roof-repair/">Roof Repair</a></li>
          <li><a href="/services/emergency-roof-repair/">Emergency Roof Repair</a></li>
          <li><a href="/services/shingle-roofing/">Atlas Shingle Roofing</a></li>
          <li><a href="/services/storm-damage-repair-specialists/">Storm &amp; Emergency Response</a></li>
          <li><a href="/services/free-roof-inspections-and-consultations/">Free Roof Inspections</a></li>
          <li><a href="/services/residential-roofing/">Residential Roofing</a></li>
          <li><a href="/services/commercial-roofing/">Commercial Roofing</a></li>
        </ul>
        <!-- rm-cross-links:end -->
"""


WHY_VARIANTS: dict[str, list[tuple[str, str, str]]] = {
    "roofing-company-dunedin-florida": [
        ("Headquarters Advantage", "As our home base since 1988, Dunedin projects get the fastest scheduling, direct owner communication, and crews who know Gulf-side salt exposure block by block."),
        ("HOA & Waterfront Experience", "From downtown Dunedin to waterfront properties, we document work for HOAs and recommend ventilation and shingle systems suited to bay humidity."),
        ("Same Crew, Every Job", "Roof Monsters uses the same trained installation crew for replacements — a consistency our Dunedin customers cite in reviews."),
    ],
    "roofing-company-tampa-florida": [
        ("Hillsborough County Coverage", "We serve all of Hillsborough — not a narrow radius — from South Tampa and Westshore to Brandon and Plant City with licensed Florida crews."),
        ("Storm-Ready Repairs", "After tropical systems, Tampa homeowners call us for tarping, documentation, and permanent shingle or flat deck repairs that pass inspection."),
        ("Commercial & Residential", "From bungalows to multi-unit properties, we scope projects clearly and stand behind work with a 15-year workmanship warranty."),
    ],
    "roofing-company-clearwater-florida": [
        ("Beach & Inland Expertise", "Clearwater Beach wind exposure differs from Countryside subdivisions — we match materials and fastening patterns to each microclimate."),
        ("Pinellas County Reach", "Clearwater sits at the heart of our Pinellas service territory with quick dispatch from our Dunedin headquarters."),
        ("Atlas Warranty Backed", "Qualifying installs include Atlas Designer Shingles with manufacturer-backed protection — popular with Clearwater re-roof projects."),
    ],
    "roofing-company-st-petersburg-florida": [
        ("Historic & Modern Homes", "St. Pete's mix of older districts and newer builds requires flexible flashing, ventilation, and drainage strategies."),
        ("Bay Humidity Performance", "We prioritize underlayment and ventilation details that reduce moisture buildup common near Tampa Bay."),
        ("Storm Response Ready", "When storms hit St. Petersburg, we tarp, document damage, and complete permanent private-pay repairs with clear written estimates."),
    ],
    "roofing-company-palm-harbor-florida": [
        ("Gulf-Side Wind Design", "Palm Harbor waterfront and golf-community homes need systems rated for coastal wind zones — we install to Florida code and manufacturer specs."),
        ("Short Drive From HQ", "Minutes from Dunedin, Palm Harbor is one of our most active markets for full replacements and targeted leak repairs."),
        ("Neighborhood Familiarity", "Our crews know common roof ages and HOA requirements across Palm Harbor communities."),
    ],
    "roofing-company-pinellas-county-florida": [
        ("County-Wide, Not Patchwork", "We serve all Pinellas municipalities and unincorporated areas — city pages highlight frequent zones, not limits."),
        ("Dunedin Headquarters", "Operating from Dunedin since 1988 gives Pinellas County clients local accountability and fast response."),
        ("Five-County Tampa Bay Reach", "Pinellas is central to our published service area spanning Pasco, Hernando, Hillsborough, and Manatee."),
    ],
    "roofing-company-hillsborough-county-florida": [
        ("All of Hillsborough", "Tampa, Brandon, Riverview, Plant City, and surrounding communities — full-county roofing, not a small map pin."),
        ("Urban Scheduling Discipline", "Hillsborough projects often involve tight timelines and access constraints — we plan deliveries and tear-off accordingly."),
        ("Storm Season Readiness", "County-wide coverage means faster emergency response when tropical weather hits the Tampa metro."),
    ],
    "roofing-company-pasco-county-florida": [
        ("Gulf & Inland Pasco", "From New Port Richey on the Gulf to Wesley Chapel growth corridors, we serve all of Pasco County."),
        ("Post-Storm Demand", "Pasco sees heavy seasonal wear — we handle tarping, inspection, and permanent repairs after Gulf systems."),
        ("Published Service Territory", "Pasco is explicitly listed in our Tampa Bay coverage alongside Pinellas and Hillsborough."),
    ],
}


def why_cards_for_slug(slug: str, short: str, name: str) -> list[tuple[str, str, str]]:
    if slug in WHY_VARIANTS:
        return WHY_VARIANTS[slug]
    if "county" in slug:
        return [
            ("Full-County Service", f"We serve all of {name}, including featured cities and unincorporated communities — contact us to confirm scheduling anywhere in the county."),
            ("Licensed Florida Contractor", "Roofing licenses CCC1335398, CCC052490 and building license CBC015719 — fully insured on every project."),
            ("Family Owned Since 1988", "Florida natives serving Florida with clear estimates and craftsmanship you can verify in our project gallery."),
        ]
    return [
        ("Local Knowledge", f"We understand building codes, HOA requirements, and roofing systems that perform best in {name}."),
        ("Licensed & Insured", "Florida-licensed roofing and building contractor with documented insurance on every job."),
        ("Tampa Bay Experience", f"{short} projects benefit from nearly four decades of Gulf Coast roofing experience from our Dunedin team."),
    ]


def why_block(short: str, name: str, slug: str) -> str:
    cards = why_cards_for_slug(slug, short, name)
    icons = ["fa-map-location-dot", "fa-shield-halved", "fa-house-chimney"]
    card_html = []
    for (title, body, icon) in zip([c[0] for c in cards], [c[1] for c in cards], icons):
        card_html.append(f"""
        <div class="why-card">
          <div class="why-num"><i class="fa-solid {icon}"></i></div>
          <h4>{esc(title)}</h4>
          <p>{esc(body)}</p>
        </div>""")
    return f"""
  <section class="why-choose-section section-pad">
    <div class="container">
      <div class="section-header">
        <span class="section-eyebrow">Why Roof Monsters</span>
        <h2>Why {esc(short)} Property Owners <span class="accent">Choose Us</span></h2>
        <p class="section-desc">Local expertise, premium materials, and a customer-first process from first call through final walkthrough.</p>
      </div>
      <div class="why-choose-grid">
        {"".join(card_html)}
      </div>
    </div>
  </section>
"""


def featured_cities_html(area: dict) -> str:
    items = []
    for city in area.get("featuredCities", []):
        name = city["name"]
        slug = city.get("slug")
        note = city.get("note", "")
        badge = f' <span class="area-city-badge">{esc(note)}</span>' if note else ""
        if slug:
            items.append(
                f'<a class="area-city-link" href="{area_url(slug)}">{esc(name)}{badge}</a>'
            )
        else:
            items.append(f'<span class="area-city-link area-city-link--text">{esc(name)}</span>')
    grid = "\n        ".join(items)
    extra = area.get("additionalCommunities", [])
    extra_html = ""
    if extra:
        joined = ", ".join(esc(c) for c in extra)
        extra_html = f"""
      <p class="area-more-communities"><strong>Also serving communities such as:</strong> {joined} — and elsewhere in {esc(area["shortName"])}.</p>"""
    return f"""
  <section class="area-coverage-section section-pad section-bg-white">
    <div class="container">
      <div class="section-header">
        <span class="section-eyebrow">Service Coverage</span>
        <h2>Full <span class="accent">{esc(area["shortName"])}</span> Coverage</h2>
      </div>
      <p class="area-coverage-note">{esc(area.get("coverageStatement", ""))}</p>
      <div class="area-city-grid">
        {grid}
      </div>{extra_html}
    </div>
  </section>
"""


def city_page(area: dict, config: dict) -> str:
    name = area["name"]
    short = area["shortName"]
    hq = config["headquarters"]
    guide = guide_for(area)
    title = f"Roofing Company in {name} | Roof Monsters"
    description = (
        f"Roof Monsters provides roof repair, replacement, inspections, and storm damage "
        f"services in {name}. Dunedin-based, family owned Tampa Bay roofing since 1988."
    )

    hq_note = ""
    if area.get("isHeadquarters"):
        hq_note = f"""
        <p class="area-local-note area-local-note--hq"><strong>Company headquarters:</strong> Roof Monsters is based in {esc(hq["city"])}, {esc(hq["state"])} — serving {esc(area["county"])} and the greater Tampa Bay area since 1988.</p>"""
    elif area.get("countySlug"):
        county_link = area_url(area["countySlug"])
        hq_note = f"""
        <p class="area-local-note">Based in <strong>{esc(hq["city"])}</strong>, we regularly serve {esc(short)} and neighboring communities. This city page highlights a common service zone within our full <a href="{county_link}">{esc(area["county"])}</a> coverage.</p>"""

    nearby = area.get("nearbyCities", [])
    nearby_html = ""
    if nearby:
        joined = ", ".join(esc(c) for c in nearby)
        nearby_html = f'<p class="area-nearby"><strong>Nearby communities we also serve:</strong> {joined}.</p>'

    local_detail = area.get("localDetail", "")
    local_para = f"<p>{esc(local_detail)}</p>" if local_detail else ""
    intro_img = guide["intro_image"]

    return HEAD.format(title=esc(title), description=esc(description), icon_head=icon_head_html(), base_head=BASE_HEAD_SCRIPT) + f"""
  <section class="page-hero">
    <div class="container">
      <h1>Roofing in <span class="accent">{esc(short)}</span></h1>
      <nav class="breadcrumb" aria-label="breadcrumb">
        <a href="/">Home</a>
        <i class="fa-solid fa-chevron-right"></i>
        <a href="/about-us/locations-we-serve/">Service Areas</a>
        <i class="fa-solid fa-chevron-right"></i>
        <span>{esc(name)}</span>
      </nav>
    </div>
  </section>

  <section class="service-intro-section section-pad">
    <div class="container service-intro-grid">
      <div class="service-intro-content">
        <span class="section-eyebrow">{"Headquarters City" if area.get("isHeadquarters") else "Local Roofing Experts"}</span>
        <h2>Trusted Roofing Services in {esc(name)}</h2>
        <p>{esc(area["blurb"])} Roof Monsters brings nearly four decades of Florida roofing experience to every project, with clear estimates, quality materials, and crews who know how Gulf Coast weather affects your roof.</p>
        {local_para}
        {hq_note}
        {nearby_html}
        {services_block(short)}
      </div>
      <div class="service-intro-img">
        <img src="assets/images/gallery/{intro_img}" alt="Completed roofing project serving {esc(short)}" />
      </div>
    </div>
  </section>
""" + local_guide_block(area, guide) + why_block(short, name, area["slug"]) + local_faq_block(short, name, guide["faqs"]) + cta_block(short) + FOOT


def county_page(area: dict, config: dict) -> str:
    name = area["name"]
    short = area["shortName"]
    hq = config["headquarters"]
    guide = guide_for(area)
    title = f"Roofing Company in {name} | Roof Monsters"
    description = (
        f"Roof Monsters serves all of {name} with roof repair, replacement, inspections, and storm damage services. "
        f"Headquartered in {hq['city']}, FL. Family owned since 1988."
    )
    intro_img = guide["intro_image"]

    return HEAD.format(title=esc(title), description=esc(description), icon_head=icon_head_html(), base_head=BASE_HEAD_SCRIPT) + f"""
  <section class="page-hero">
    <div class="container">
      <h1>Roofing in <span class="accent">{esc(short)}</span></h1>
      <nav class="breadcrumb" aria-label="breadcrumb">
        <a href="/">Home</a>
        <i class="fa-solid fa-chevron-right"></i>
        <a href="/about-us/locations-we-serve/">Service Areas</a>
        <i class="fa-solid fa-chevron-right"></i>
        <span>{esc(name)}</span>
      </nav>
    </div>
  </section>

  <section class="service-intro-section section-pad">
    <div class="container service-intro-grid">
      <div class="service-intro-content">
        <span class="section-eyebrow">County-Wide Service</span>
        <h2>Trusted Roofing Throughout {esc(name)}</h2>
        <p>{esc(area["blurb"])} Our Dunedin headquarters puts Pinellas and the wider Tampa Bay region within practical reach for inspections, repairs, and full replacements.</p>
        <p class="area-coverage-note area-coverage-note--inline">{esc(area.get("coverageStatement", ""))}</p>
        {services_block(short)}
      </div>
      <div class="service-intro-img">
        <img src="assets/images/gallery/{intro_img}" alt="Completed roofing project serving {esc(short)}" />
      </div>
    </div>
  </section>
""" + featured_cities_html(area) + local_guide_block(area, guide) + why_block(short, name, area["slug"]) + local_faq_block(short, name, guide["faqs"]) + cta_block(short) + FOOT


def hub_page(config: dict, cities: list[dict], counties: list[dict]) -> str:
    hq = config["headquarters"]
    counties_label = ", ".join(config["serviceCounties"])

    city_cards = []
    for area in cities:
        badge = ' <span class="area-card-badge">HQ</span>' if area.get("isHeadquarters") else ""
        city_cards.append(f"""
        <div class="service-page-card">
          <div class="spc-icon"><i class="fa-solid fa-location-dot"></i></div>
          <h3>{esc(area["name"].replace(", FL", ", Florida"))}{badge}</h3>
          <p>{esc(area["blurb"])}</p>
          <a href="{area_url(area["slug"])}" class="service-link">View {esc(area["shortName"])} <i class="fa-solid fa-arrow-right"></i></a>
        </div>""")

    county_cards = []
    for area in counties:
        featured = ", ".join(c["name"] for c in area.get("featuredCities", [])[:4])
        county_cards.append(f"""
        <div class="service-page-card">
          <div class="spc-icon"><i class="fa-solid fa-map"></i></div>
          <h3>{esc(area["name"].replace(", FL", ", Florida"))}</h3>
          <p><strong>Full county coverage.</strong> {esc(area["blurb"])} Featured communities include {esc(featured)}.</p>
          <a href="{area_url(area["slug"])}" class="service-link">View {esc(area["shortName"])} <i class="fa-solid fa-arrow-right"></i></a>
        </div>""")

    return HEAD.format(
        title="Locations We Serve | Roof Monsters — Tampa Bay Roofing",
        description=(
            f"Roof Monsters is headquartered in {hq['city']}, FL and serves all of Pasco, Pinellas, "
            "Hernando, Hillsborough, and Manatee County with expert roofing services."
        ),
        icon_head=icon_head_html(),
        base_head=BASE_HEAD_SCRIPT,
    ) + f"""
  <section class="page-hero">
    <div class="container">
      <h1>Locations We <span class="accent">Serve</span></h1>
      <nav class="breadcrumb" aria-label="breadcrumb">
        <a href="/">Home</a>
        <i class="fa-solid fa-chevron-right"></i>
        <a href="/about-us/">About Us</a>
        <i class="fa-solid fa-chevron-right"></i>
        <span>Locations We Serve</span>
      </nav>
    </div>
  </section>

  <section class="service-intro-section section-pad">
    <div class="container service-intro-grid">
      <div class="service-intro-content">
        <span class="section-eyebrow">Dunedin Headquarters · Tampa Bay</span>
        <h2>Serving All of Tampa Bay — From Our Home Base in Dunedin</h2>
        <p>Roof Monsters is headquartered in <strong>{esc(hq["city"])}, Florida</strong> and provides roofing across <strong>{esc(counties_label)}</strong> — the same five-county Tampa Bay territory published on roofmonsters.co.</p>
        <p>{esc(config.get("coverageDisclaimer", ""))}</p>
        <p>City pages focus on high-intent local searches in Pinellas and select neighboring markets. County pages explain whole-county service and link to featured communities within our typical project radius.</p>

        <h3>Why Choose Roof Monsters in Florida?</h3>
        <div class="benefits-list">
          <div class="benefit-item"><i class="fa-solid fa-check-circle"></i><p><strong>Dunedin-Based Operations</strong> — Fast response across Pinellas and the wider bay area from a local headquarters, not a national call center.</p></div>
          <div class="benefit-item"><i class="fa-solid fa-check-circle"></i><p><strong>County-Wide Coverage</strong> — We serve all of Pasco, Pinellas, Hernando, Hillsborough, and Manatee Counties.</p></div>
          <div class="benefit-item"><i class="fa-solid fa-check-circle"></i><p><strong>HOA &amp; Property Manager Support</strong> — Documentation, scheduling, and communication tailored for communities and managers (CAM experience on staff).</p></div>
        </div>
      </div>
      <div class="service-intro-img">
        <img src="assets/images/gallery/pinellas-new-roof.webp" alt="Completed roof project by Roof Monsters serving Tampa Bay from Dunedin" />
      </div>
    </div>
  </section>

  <section class="services-page-section section-pad section-bg-white">
    <div class="container">
      <div class="section-header">
        <span class="section-eyebrow">Pinellas Cities</span>
        <h2>City Pages — <span class="accent">Pinellas &amp; Select Markets</span></h2>
        <p class="section-desc">Local landing pages for communities we serve frequently from Dunedin. Every Pinellas city is part of our full county coverage.</p>
      </div>
      <div class="services-page-grid">
        {"".join(city_cards)}
      </div>
    </div>
  </section>

  <section class="services-page-section section-pad">
    <div class="container">
      <div class="section-header">
        <span class="section-eyebrow">County Coverage</span>
        <h2>Full-County <span class="accent">Service Areas</span></h2>
        <p class="section-desc">Each county page confirms whole-county service and highlights cities within our typical Tampa Bay project radius.</p>
      </div>
      <div class="services-page-grid">
        {"".join(county_cards)}
      </div>
    </div>
  </section>

  <section class="atlas-banner atlas-banner--parallax">
    <div class="atlas-banner-bg bg-atlas-banner-locations" aria-hidden="true"></div>
    <div class="atlas-overlay"></div>
    <div class="container atlas-inner">
      <div class="atlas-content">
        <p class="section-eyebrow">Contact Us Today</p>
        <h2>Ready for Expert Roofing in <span class="accent">Your Area?</span></h2>
        <p>Trust Roof Monsters for roofing solutions tailored to your location — from Dunedin to every county we serve across Tampa Bay.</p>
        <a href="/contact-us/" class="btn btn-primary u-mt-20">Get A Free Estimate</a>
      </div>
      <div class="atlas-stat">
        <div class="atlas-num" data-rm-live-review-count data-rm-live-review-suffix=" +">30 +</div>
        <div class="atlas-label">Google Reviews Across Tampa Bay</div>
      </div>
    </div>
  </section>
""" + FOOT


def main() -> None:
    config = json.loads(DATA.read_text(encoding="utf-8"))
    areas = config["areas"]
    cities = [a for a in areas if a["type"] == "city"]
    counties = [a for a in areas if a["type"] == "county"]

    (HUB / "index.html").write_text(hub_page(config, cities, counties), encoding="utf-8")
    print(f"Wrote {HUB / 'index.html'}")

    for area in areas:
        out_dir = BASE / area["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        if area["type"] == "city":
            content = city_page(area, config)
        else:
            content = county_page(area, config)
        (out_dir / "index.html").write_text(content, encoding="utf-8")
        print(f"Wrote {out_dir / 'index.html'}")


if __name__ == "__main__":
    main()
