#!/usr/bin/env python3
"""Generate focused service landing pages under /services/."""

from __future__ import annotations

import html
from pathlib import Path

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

  <section class="service-intro-section section-pad">
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
        <img src="assets/images/gallery/quality-work.webp" alt="{esc(p["eyebrow"])} by Roof Monsters" />
      </div>
    </div>
  </section>

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
        <form class="estimate-form">
          <div class="form-row">
            <div class="form-group">
              <label>Name</label>
              <input type="text" name="name" placeholder="Your name" required />
            </div>
            <div class="form-group">
              <label>Email</label>
              <input type="email" name="email" placeholder="you@email.com" required />
            </div>
          </div>
          <div class="form-group">
            <label>Phone</label>
            <input type="tel" name="phone" placeholder="(727) 000-0000" />
          </div>
          <div class="form-group">
            <label>Message</label>
            <textarea name="message" rows="3" placeholder="Tell us about your roofing needs"></textarea>
          </div>
          <button type="submit" class="btn-submit">Send Request</button>
        </form>
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
