#!/usr/bin/env python3
"""Generate legacy WordPress URL pages: FAQs, warranty, sustainability, categories, missing blog posts."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "data" / "site-seo.json").read_text(encoding="utf-8"))

HEAD = """<!DOCTYPE html>
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

EXISTING_BLOG_SLUGS = {
    "october-roofing-season-in-tampa-bay-why-fall-is-the-best-time-to-schedule-your-roof-work",
    "how-to-prepare-your-roof-for-floridas-hurricane-season",
    "the-roof-monsters-way-what-sets-our-roofing-company-apart",
}

BLOG_EXTRA = {
    "what-is-tpo-roofing-and-why-its-perfect-for-florida-commercial-buildings": """
      <p>TPO (thermoplastic polyolefin) is one of the most popular single-ply membranes for flat and low-slope commercial roofs across Florida. It reflects heat, handles ponding water when installed correctly, and offers a strong balance of performance and value for warehouses, retail strips, and multi-family buildings.</p>
      <h2>Why TPO Works in Florida</h2>
      <p>Florida's intense UV exposure and summer heat punish roofing systems. White or light-colored TPO membranes reflect solar energy, which can reduce cooling loads on commercial structures. Proper seam welding and flashing details are critical — installation quality matters more than the brand name on the roll.</p>
      <h2>When to Consider TPO</h2>
      <p>TPO is a practical choice for flat decks, additions, and commercial properties that need a durable membrane without the cost of some premium systems. Roof Monsters evaluates existing decking, drainage, and insulation before recommending TPO versus modified bitumen or other flat-roof options.</p>
      <p>Schedule a <a href="/services/free-roof-inspections-and-consultations/">free inspection</a> for flat-roof properties in <a href="/about-us/locations-we-serve/roofing-company-tampa-florida/">Tampa</a>, <a href="/about-us/locations-we-serve/roofing-company-clearwater-florida/">Clearwater</a>, and surrounding Tampa Bay markets.</p>
""",
    "5-signs-its-time-to-replace-your-roof-in-florida": """
      <p>Florida roofs age faster than roofs in milder climates. Sun, salt air, and hurricane-season wind all accelerate wear. Here are five signs it may be time for replacement rather than another round of repairs.</p>
      <h2>1. Shingles Are Curling, Cracking, or Missing</h2>
      <p>Granule loss and lifted tabs often indicate the roof is near end of life — especially on south-facing slopes that bake in summer sun.</p>
      <h2>2. Recurring Leaks in Multiple Areas</h2>
      <p>One leak can be repaired. Several active leaks often mean systemic failure — underlayment, flashing, or widespread shingle breakdown.</p>
      <h2>3. The Roof Is 20+ Years Old</h2>
      <p>Many asphalt shingle systems in Florida perform well for 15–25 years depending on ventilation, tree cover, and storm history. Past that range, replacement planning is prudent.</p>
      <h2>4. Storm or Hail Damage Documented on Inspection</h2>
      <p>After major weather, a licensed <a href="/services/storm-damage-repair-specialists/">storm damage specialist</a> can document whether repair or full replacement is the better financial decision.</p>
      <h2>5. Rising Energy Bills or Attic Moisture</h2>
      <p>Poor ventilation and failing roof decks can show up as higher cooling costs, mold odors, or stained ceilings. A <a href="/services/free-roof-inspections-and-consultations/">professional inspection</a> clarifies the cause.</p>
""",
    "how-to-choose-the-right-roofing-contractor": """
      <p>Hiring the wrong roofer costs more than money — it costs time, stress, and sometimes insurance complications. Use this checklist when comparing Tampa Bay roofing contractors.</p>
      <h2>Verify License and Insurance</h2>
      <p>Florida roofing contractors should hold active state licensing and carry liability and workers' compensation insurance. Roof Monsters publishes license numbers on every page and provides documentation on request.</p>
      <h2>Get a Detailed Written Estimate</h2>
      <p>A professional estimate should specify materials, tear-off scope, flashing, ventilation, cleanup, and warranty terms — not just a single bottom-line number.</p>
      <h2>Check Local References and Reviews</h2>
      <p>Look for consistent themes in Google reviews: communication, cleanup, and crew quality. Ask for recent projects in your city or HOA community.</p>
      <h2>Understand Warranties</h2>
      <p>Manufacturer product warranties and contractor workmanship warranties are different. We install Atlas systems with a 15-year Roof Monsters workmanship warranty on qualifying projects.</p>
      <p><a href="/contact-us/">Contact us</a> for a free estimate or read <a href="/the-roof-monsters-way-what-sets-our-roofing-company-apart/">what sets Roof Monsters apart</a>.</p>
""",
    "how-to-prepare-your-roof-for-storm-season": """
      <p>Storm season in Florida demands preparation — not panic. A few proactive steps before warnings are issued protect your home and simplify insurance documentation if damage occurs.</p>
      <h2>Schedule a Pre-Season Inspection</h2>
      <p>Loose flashing, worn pipe boots, and lifted shingles are easy to fix before wind-driven rain exploits them. Our <a href="/services/free-roof-inspections-and-consultations/">free inspections</a> identify vulnerabilities early.</p>
      <h2>Trim Overhanging Branches</h2>
      <p>Branches that scrape shingles during normal weather become projectiles in high wind. Clear debris from valleys and gutters so water flows freely during heavy rain.</p>
      <h2>Document Your Roof's Condition</h2>
      <p>Take dated photos of all slopes before storm season. Baseline documentation helps you and your contractor distinguish new storm damage from pre-existing wear when planning repairs.</p>
      <h2>Know Your Emergency Plan</h2>
      <p>Keep tarps, contractor contact info, and insurance policy numbers accessible. For urgent response after a storm, call <a href="tel:7274393869">(727) 439-3869</a>.</p>
""",
    "the-benefits-of-eco-friendly-roofing-solutions": """
      <p>Sustainable roofing is not just about environmental branding — in Florida it can mean lower cooling costs, longer material life, and better storm resilience when systems are specified correctly.</p>
      <h2>Cool Roof Performance</h2>
      <p>Reflective shingles and membranes reduce heat absorption. That matters on sunny Gulf Coast homes where attic temperatures directly affect HVAC runtime.</p>
      <h2>Durable Materials Reduce Waste</h2>
      <p>A roof that lasts 20+ years with proper maintenance replaces fewer tons of material over a home's lifetime than repeated patch jobs on a failing system.</p>
      <h2>Atlas Scotchgard Protection</h2>
      <p>We install Atlas Designer Shingles featuring Scotchgard protection on qualifying projects — algae resistance that keeps roofs looking cleaner longer in humid Florida climates.</p>
      <p>Learn more on our <a href="/sustainability/">sustainability page</a> or explore <a href="/services/comprehensive-roof-installations/">roof installation options</a>.</p>
""",
    "advancements-in-roofing-technology-what-homeowners-need-to-know": """
      <p>Roofing technology has improved significantly over the past decade — better underlayment, ventilation products, impact-resistant materials, and digital inspection tools all help homeowners make smarter decisions.</p>
      <h2>Improved Underlayment and Ice & Water Barriers</h2>
      <p>Modern synthetic underlayments and self-adhered barriers at valleys, eaves, and penetrations provide backup protection if shingles are compromised in wind events.</p>
      <h2>Ventilation That Matches Florida Heat</h2>
      <p>Proper ridge, soffit, and attic ventilation extends shingle life and reduces moisture buildup — critical in Tampa Bay's humid climate.</p>
      <h2>Impact-Resistant Options</h2>
      <p>Some systems qualify for insurance discounts in wind-prone regions. We help homeowners compare upgrade costs against long-term premium savings.</p>
      <h2>Digital Documentation</h2>
      <p>Photo reports from inspections create clear records for insurance, HOAs, and future buyers — standard practice on every Roof Monsters project.</p>
""",
    "choosing-the-right-roofing-material-for-your-home": """
      <p>Material choice affects cost, curb appeal, wind rating, and maintenance for decades. Florida homeowners typically choose between architectural shingles, tile, metal, and flat-roof membranes depending on structure and budget.</p>
      <h2>Architectural Asphalt Shingles</h2>
      <p>The most common choice for Tampa Bay homes — excellent value, wide color selection, and proven performance when installed to manufacturer specs. We recommend Atlas Designer Shingles on qualifying projects.</p>
      <h2>Tile and Metal</h2>
      <p>Tile offers distinctive aesthetics and longevity; metal provides durability and energy reflectivity. Both require structural evaluation and specialized installation experience.</p>
      <h2>Flat and Low-Slope Systems</h2>
      <p>Additions, porches, and commercial buildings often need TPO or modified bitumen. Material must match slope, drainage, and building use.</p>
      <p>Not sure what fits your home? Start with a <a href="/services/free-roof-inspections-and-consultations/">free consultation</a> or browse our <a href="/gallery/">project gallery</a>.</p>
""",
    "the-importance-of-regular-roof-maintenance": """
      <p>Regular maintenance is the cheapest insurance policy for your roof. Small issues — a lifted shingle, cracked boot, or clogged valley — become expensive leaks if ignored through another Florida summer.</p>
      <h2>Annual Inspections Catch Problems Early</h2>
      <p>A yearly walk-through and attic check identifies wear before hurricane season. We document findings so you can plan repairs on your timeline, not during a storm scramble.</p>
      <h2>Gutter and Drainage Matter</h2>
      <p>Overflowing gutters push water under eaves and saturate fascia boards. Our <a href="/services/gutter-installation-and-cleaning/">gutter services</a> complement roof maintenance for whole-system protection.</p>
      <h2>Maintenance Extends Roof Life</h2>
      <p>Homes that receive consistent care often outperform neighbors' roofs by five to ten years — delaying full replacement costs and preserving interior finishes.</p>
      <p>Schedule <a href="/services/expert-roof-repairs-and-maintenance/">roof maintenance</a> with Roof Monsters — family owned in Dunedin since 1988.</p>
""",
}

LEGACY_PAGES = {
    "faqs": {
        "title": "Roofing FAQs | Roof Monsters Tampa Bay",
        "description": "Frequently asked questions about roof repair, replacement, warranties, insurance, and inspections — answered by Roof Monsters, Dunedin FL.",
        "h1": "Frequently Asked <span class=\"accent\">Questions</span>",
        "breadcrumb": "FAQs",
        "body": """
      <div class="faq-list">
        <article class="faq-item">
          <h2>How much does a new roof cost in Tampa Bay?</h2>
          <p>Cost depends on roof size, pitch, material, tear-off scope, and decking condition. We provide free written estimates after an on-site inspection — no pressure, no hidden fees.</p>
        </article>
        <article class="faq-item">
          <h2>Do you offer free roof inspections?</h2>
          <p>Yes. <a href="/services/free-roof-inspections-and-consultations/">Free inspections and consultations</a> are available across Pasco, Pinellas, Hernando, Hillsborough, and Manatee County.</p>
        </article>
        <article class="faq-item">
          <h2>What warranties do you provide?</h2>
          <p>Qualifying projects include Atlas manufacturer coverage plus Roof Monsters' 15-year workmanship warranty. See our <a href="/warranty-guarantee/">warranty &amp; guarantee page</a> for details.</p>
        </article>
        <article class="faq-item">
          <h2>Are you licensed and insured?</h2>
          <p>Yes. Roofing: CCC1335398, CCC052490. Building: CBC015719. Terrance McKeever Enterprises, Inc. DBA Roof Monsters — headquartered in Dunedin, FL.</p>
        </article>
        <article class="faq-item">
          <h2>What happens after storm damage?</h2>
          <p>We respond quickly with emergency tarping when needed, document the damage, and complete permanent private-pay repairs with clear written estimates. Learn more about our <a href="/services/storm-damage-repair-specialists/">storm damage services</a>.</p>
        </article>
        <article class="faq-item">
          <h2>What areas do you serve?</h2>
          <p>We serve all of Tampa Bay from our Dunedin headquarters. Browse <a href="/about-us/locations-we-serve/">locations we serve</a> for city and county pages.</p>
        </article>
      </div>
      <p class="faq-cta"><a href="/contact-us/" class="btn btn-primary"><i class="fa-solid fa-arrow-right"></i> Ask a Question</a></p>
""",
    },
    "warranty-guarantee": {
        "title": "Warranty & Guarantee | Roof Monsters Tampa Bay",
        "description": "Roof Monsters warranty and guarantee — 15-year workmanship warranty, Atlas manufacturer coverage, and licensed installation across Tampa Bay.",
        "h1": "Warranty &amp; <span class=\"accent\">Guarantee</span>",
        "breadcrumb": "Warranty & Guarantee",
        "body": """
      <p>Roof Monsters stands behind every installation with clear warranty terms and local accountability from our Dunedin headquarters — not a storm-chasing crew that disappears after the job.</p>
      <h2>15-Year Workmanship Warranty</h2>
      <p>On qualifying full roof replacements, Roof Monsters provides a 15-year workmanship warranty covering installation labor. If an issue relates to how we installed your system, we make it right.</p>
      <h2>Atlas Manufacturer Coverage</h2>
      <p>We install Atlas Designer Shingles featuring Scotchgard protection on qualifying projects. Manufacturer product warranties apply per Atlas terms and registration requirements.</p>
      <h2>Licensed, Insured Installation</h2>
      <p>All work is performed under Florida roofing license CCC1335398 / CCC052490 and building license CBC015719 by Terrance McKeever Enterprises, Inc. DBA Roof Monsters.</p>
      <h2>What Homeowners Should Keep</h2>
      <ul>
        <li>Signed contract and scope of work</li>
        <li>Material invoice and warranty registration confirmation</li>
        <li>Inspection photos and final walkthrough notes</li>
        <li>Roof Monsters contact: <a href="tel:7274393869">(727) 439-3869</a></li>
      </ul>
      <p><a href="/contact-us/" class="btn btn-primary"><i class="fa-solid fa-arrow-right"></i> Get a Free Estimate</a></p>
""",
    },
    "sustainability": {
        "title": "Sustainable Roofing | Roof Monsters Tampa Bay",
        "description": "Eco-friendly and energy-efficient roofing solutions for Florida — cool roofs, durable materials, and responsible installation from Roof Monsters.",
        "h1": "Sustainable <span class=\"accent\">Roofing</span>",
        "breadcrumb": "Sustainability",
        "body": """
      <p>Sustainability in roofing means building systems that last, reduce energy waste, and minimize repeat tear-offs over a home's lifetime. Roof Monsters approaches every project with that long view.</p>
      <h2>Energy-Efficient Materials</h2>
      <p>Reflective shingles and proper attic ventilation reduce heat transfer into living spaces — meaningful in Florida's cooling-dominated climate.</p>
      <h2>Durability Reduces Landfill Waste</h2>
      <p>A properly installed roof that lasts decades replaces fewer materials than repeated emergency patches on a failing system. Quality installation is the most sustainable choice.</p>
      <h2>Atlas Scotchgard Algae Resistance</h2>
      <p>Algae streaks are common in humid Gulf Coast conditions. Scotchgard-protected Atlas shingles resist black streaking, keeping roofs functional and attractive longer.</p>
      <h2>Responsible Tear-Off and Recycling</h2>
      <p>We haul away debris and follow jobsite cleanup standards that protect landscaping, driveways, and neighboring properties — magnetic nail sweeps included.</p>
      <p>Read more in our blog: <a href="/the-benefits-of-eco-friendly-roofing-solutions/">eco-friendly roofing benefits</a>.</p>
      <p><a href="/services/comprehensive-roof-installations/" class="btn btn-primary"><i class="fa-solid fa-arrow-right"></i> Explore Installations</a></p>
""",
    },
}


def page_shell(title: str, description: str, h1: str, breadcrumb: str, body: str) -> str:
    return HEAD.format(title=title, description=description) + f"""
  <section class="page-hero">
    <div class="container">
      <h1>{h1}</h1>
      <nav class="breadcrumb" aria-label="breadcrumb">
        <a href="/">Home</a>
        <i class="fa-solid fa-chevron-right"></i>
        <span>{breadcrumb}</span>
      </nav>
    </div>
  </section>

  <section class="section-pad section-bg-white">
    <div class="container content-page">
{body}
    </div>
  </section>
""" + FOOT


def blog_shell(post: dict, body: str, crumb_label: str) -> str:
    img = post["image"].replace("assets/", "")
    return HEAD.format(title=f"{post['title']} | Roof Monsters Blog", description=post["description"]) + f"""
  <section class="page-hero">
    <div class="container">
      <h1>{post['title']}</h1>
      <nav class="breadcrumb" aria-label="breadcrumb">
        <a href="/">Home</a>
        <i class="fa-solid fa-chevron-right"></i>
        <a href="/blog/">Blog</a>
        <i class="fa-solid fa-chevron-right"></i>
        <span>{crumb_label}</span>
      </nav>
    </div>
  </section>

  <section class="section-pad section-bg-white">
    <div class="container blog-article">
      <div class="blog-article-hero">
        <img src="assets/{img}" alt="{post['title']}" loading="lazy" />
      </div>
      <div class="blog-article-meta">
        <span><i class="fa-regular fa-calendar"></i> {post['datePublished']}</span>
        <span class="blog-cat"><a href="/category/{post['categorySlug']}/">{post['category']}</a></span>
        <span><i class="fa-solid fa-user"></i> Roof Monsters Team</span>
      </div>
{body}
      <div class="blog-article-cta">
        <p><strong>Ready to schedule roofing work in Tampa Bay?</strong> Roof Monsters serves Pasco, Pinellas, Hernando, Hillsborough, and Manatee County from our Dunedin headquarters.</p>
        <a href="/contact-us/" class="btn btn-primary"><i class="fa-solid fa-arrow-right"></i> Get a Free Estimate</a>
      </div>
    </div>
  </section>
""" + FOOT


def category_cards(slug: str) -> str:
    posts = [p for p in CONFIG["blogPosts"] if p.get("categorySlug") == slug]
    if not posts:
        return "<p>No posts in this category yet. <a href=\"/blog/\">Browse all articles</a>.</p>"
    cards = []
    for post in posts:
        img = post["image"].replace("assets/", "")
        cards.append(f"""
        <article class="blog-card">
          <a href="/{post['slug']}/" class="blog-img-link">
            <img src="assets/{img}" alt="{post['title']}" loading="lazy" />
          </a>
          <div class="blog-body">
            <div class="blog-meta">
              <span><i class="fa-regular fa-calendar"></i> {post['datePublished']}</span>
            </div>
            <h2><a href="/{post['slug']}/">{post['title']}</a></h2>
            <p>{post['description']}</p>
            <a href="/{post['slug']}/" class="read-more">Read more <i class="fa-solid fa-arrow-right"></i></a>
          </div>
        </article>""")
    return '<div class="blog-grid blog-grid--listing">\n' + "\n".join(cards) + "\n      </div>"


def write_page(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


def main() -> None:
    for slug, page in LEGACY_PAGES.items():
        write_page(ROOT / slug / "index.html", page_shell(**page))

    for cat in CONFIG["categories"]:
        body = f"""
      <p class="section-desc">{cat['description']}</p>
      <p><a href="/blog/">View all blog posts</a></p>
{category_cards(cat['slug'])}
"""
        write_page(
            ROOT / "category" / cat["slug"] / "index.html",
            page_shell(
                title=f"{cat['name']} | Roof Monsters Blog",
                description=cat["description"],
                h1=f"{cat['name']} <span class=\"accent\">Articles</span>",
                breadcrumb=cat["name"],
                body=body,
            ),
        )

    for post in CONFIG["blogPosts"]:
        if post["slug"] in EXISTING_BLOG_SLUGS:
            continue
        body = BLOG_EXTRA.get(post["slug"], f"<p>{post['description']}</p>")
        short = post["title"]
        if len(short) > 48:
            short = post["category"]
        write_page(
            ROOT / post["slug"] / "index.html",
            blog_shell(post, body, short),
        )


if __name__ == "__main__":
    main()
