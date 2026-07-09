#!/usr/bin/env python3
"""Build blog index and expand blog post bodies."""

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

BLOG_BODY = {
    "october-roofing-season-in-tampa-bay-why-fall-is-the-best-time-to-schedule-your-roof-work": """
      <p>As the sweltering Florida summer fades and the skies begin to clear, October marks the beginning of one of the best seasons for roofing in Tampa Bay. For homeowners and property managers across Pasco, Pinellas, and Hillsborough County, it is an ideal window to assess roof damage, schedule repairs, or plan for full replacements before holiday travel and the next storm cycle.</p>

      <h2>Why October Is Prime Time for Roofing in Tampa Bay</h2>
      <p>Cooler, more stable temperatures create ideal conditions for shingle adhesion, sealant curing, and safe, efficient installation. That means faster project completion and longer-lasting results compared to peak summer heat when materials can soften and crews face heat-related delays.</p>
      <p>October also sits after the most intense hurricane activity but before the late-season systems that can still affect the Gulf Coast. Scheduling now gives you time to address <a href="/services/expert-roof-repairs-and-maintenance/">roof repairs</a> discovered during summer storms without waiting until spring when demand spikes.</p>

      <h2>Post-Hurricane Season Inspections</h2>
      <p>Hurricane season runs through November, but by October most major systems have passed. Even without visible leaks, lifted shingles, cracked flashing, or weakened underlayment can lead to bigger problems when the next front arrives.</p>
      <p>A professional <a href="/services/free-roof-inspections-and-consultations/">free roof inspection</a> helps catch hidden storm damage early so you can plan private-pay repairs before the next system — especially important for investment properties and HOA-managed communities in <a href="/about-us/locations-we-serve/roofing-company-clearwater-florida/">Clearwater</a>, <a href="/about-us/locations-we-serve/roofing-company-tampa-florida/">Tampa</a>, and <a href="/about-us/locations-we-serve/roofing-company-palm-harbor-florida/">Palm Harbor</a>.</p>

      <h2>Prep Before the Holidays</h2>
      <p>Once November hits, schedules fill with holidays and travel. October gives you a practical window to complete repairs or a full <a href="/services/comprehensive-roof-installations/">roof replacement</a> before guests arrive or before seasonal weather shifts make outdoor work less predictable.</p>

      <h2>Recommended Fall Services for Florida Homeowners</h2>
      <ul>
        <li>Seasonal roof inspection to identify weak spots, aging shingles, and ventilation issues</li>
        <li>Roof tune-up: minor repairs, resealing, debris removal, and <a href="/services/gutter-installation-and-cleaning/">gutter flushing</a></li>
        <li>Full replacement with Atlas Designer Shingles and Roof Monsters' 15-year workmanship warranty</li>
        <li>Flat deck or low-slope evaluation common on Tampa Bay additions and commercial strips</li>
      </ul>

      <h2>Plan Ahead With a Local Contractor</h2>
      <p>Roof Monsters has served Tampa Bay from our Dunedin headquarters since 1988. Whether you need a targeted repair or a full re-roof, fall scheduling typically offers better availability and more comfortable working conditions for crews — which translates to meticulous installation details that matter long-term.</p>
""",
    "how-to-prepare-your-roof-for-floridas-hurricane-season": """
      <p>Every year from June through November, Florida braces for hurricane season. Your roof is your home's first line of defense against wind-driven rain, flying debris, and prolonged saturation. Preparing before a storm is named — not after — is the difference between a manageable repair and catastrophic interior damage.</p>

      <h2>Start With a Professional Roof Inspection</h2>
      <p>Visible shingles can look fine while flashing, pipe boots, and ridge caps fail under pressure. A licensed <a href="/services/free-roof-inspections-and-consultations/">roof inspection</a> documents existing wear and gives you time to fix vulnerabilities before a tropical system arrives.</p>
      <p>Homeowners in <a href="/about-us/locations-we-serve/roofing-company-pinellas-county-florida/">Pinellas County</a>, <a href="/about-us/locations-we-serve/roofing-company-pasco-county-florida/">Pasco County</a>, and along the Gulf coast should pay special attention to ridge vents, chimney flashing, and areas where previous repairs may have aged.</p>

      <h2>Trim Trees and Secure Loose Items</h2>
      <p>Overhanging branches scrape shingles and become projectiles in high wind. Trim back limbs that contact the roof plane and remove dead wood before storm warnings compress contractor availability.</p>

      <h2>Clean Gutters and Check Drainage</h2>
      <p>Clogged gutters force water behind fascia and into soffits. Pre-season <a href="/services/gutter-installation-and-cleaning/">gutter cleaning</a> ensures runoff moves away from the structure — critical during the heavy rain bands of a tropical storm.</p>

      <h2>Know Your Roof Age and Material</h2>
      <p>Asphalt shingle systems typically last 20–25 years in Florida's UV and heat exposure. If your roof is approaching that range, pre-season planning for replacement beats emergency tear-off during a storm week when materials and labor are scarce.</p>

      <h2>After the Storm: Document and Call Early</h2>
      <p>If damage occurs, photograph affected areas before temporary tarping when safe to do so. Roof Monsters provides <a href="/services/storm-damage-repair-specialists/">storm damage repair</a> and emergency response across Tampa Bay — early calls get faster scheduling when regional demand surges.</p>

      <h2>Build a Maintenance Rhythm</h2>
      <p>Annual inspections plus prompt <a href="/services/expert-roof-repairs-and-maintenance/">maintenance repairs</a> extend roof life and reduce surprise failures. Pair hurricane prep with a fall inspection to catch summer wear before the next season begins.</p>

      <h2>Insurance and Documentation Tips</h2>
      <p>Before storm season, photograph your roof from multiple angles and note the installation date if known. After a storm, compare new photos to your baseline to spot fresh damage versus pre-existing wear. Roof Monsters documents findings during <a href="/services/free-roof-inspections-and-consultations/">inspections</a> so you have a clear scope for private-pay emergency or permanent repairs.</p>
      <p>Communities in <a href="/about-us/locations-we-serve/roofing-company-tampa-florida/">Tampa</a>, <a href="/about-us/locations-we-serve/roofing-company-clearwater-florida/">Clearwater</a>, and <a href="/about-us/locations-we-serve/roofing-company-dunedin-florida/">Dunedin</a> frequently schedule pre-season tune-ups in April and May when contractor availability is highest — waiting until a named storm is in the Gulf compresses timelines and raises costs.</p>
""",
    "the-roof-monsters-way-what-sets-our-roofing-company-apart": """
      <p>When it comes to choosing a roofing company, the options can feel endless. At Roof Monsters, we believe homeowners deserve clear answers, fair pricing, and craftsmanship that lasts — without the runaround common in storm-chasing markets.</p>

      <h2>Family Owned Since 1988</h2>
      <p>Roof Monsters is a DBA of Terrance McKeever Enterprises, Inc., operated by Florida natives who built the company on repeat referrals across Tampa Bay. We are headquartered in <a href="/about-us/locations-we-serve/roofing-company-dunedin-florida/">Dunedin</a> and serve Pasco, Pinellas, Hernando, Hillsborough, and Manatee County — the same five-county territory published on roofmonsters.co.</p>

      <h2>Same Crew, Consistent Quality</h2>
      <p>Customers frequently mention that we use the same installation crew for replacements — that continuity matters for flashing details, ridge alignment, and cleanup discipline. You are not getting a different subcontractor team every time you call.</p>

      <h2>Warranty-Backed Materials</h2>
      <p>We install Atlas Designer Shingles featuring Scotchgard protection on qualifying projects, paired with a 15-year workmanship warranty from Roof Monsters. That combination gives homeowners manufacturer-backed product coverage plus local accountability if something needs attention.</p>

      <h2>Communication You Can Reach</h2>
      <p>Reviews highlight responsive communication and same-day callbacks — critical when you are deciding how to handle a leak or storm damage. Call or text <a href="tel:7274393869">(727) 439-3869</a> to talk with our team directly.</p>

      <h2>Full-Service Roofing</h2>
      <p>From <a href="/services/comprehensive-roof-installations/">installations</a> and <a href="/services/expert-roof-repairs-and-maintenance/">repairs</a> to <a href="/services/storm-damage-repair-specialists/">storm response</a>, <a href="/services/skylight-installation-and-repair/">skylights</a>, and <a href="/services/gutter-installation-and-cleaning/">gutters</a>, we handle the full roof system — not just a quick patch.</p>

      <h2>HOA and Property Manager Support</h2>
      <p>With CAM experience on staff since 2018, we understand documentation, scheduling, and communication expectations for communities and managers overseeing multiple properties.</p>

      <h2>See the Proof</h2>
      <p>Browse our <a href="/gallery/">project gallery</a> and <a href="/testimonials/">customer reviews</a>, or schedule a <a href="/contact-us/">free estimate</a> to experience the Roof Monsters process firsthand.</p>

      <h2>What Customers Say About Working With Us</h2>
      <p>Homeowners across Tampa Bay consistently mention communication, cleanup, and crew consistency in reviews — the same themes that drive our internal training and project checklists. We treat every roof as a referral opportunity because our business has grown through word of mouth since 1988, not storm-chasing billboards.</p>
      <p>Whether you are comparing contractors for a full <a href="/services/comprehensive-roof-installations/">replacement</a> or need urgent <a href="/services/storm-damage-repair-specialists/">storm help</a>, start with a conversation. We will tell you honestly if repair makes sense versus replacement — and show you comparable projects from your area in our gallery.</p>
""",
}


def blog_cards() -> str:
    cards = []
    for post in CONFIG["blogPosts"]:
        cards.append(f"""
      <article class="blog-card">
        <a href="/{post['slug']}/" class="blog-img-link">
          <img src="assets/{post['image'].replace('assets/', '')}" alt="{post['title']}" loading="lazy" />
        </a>
        <div class="blog-body">
          <div class="blog-meta">
            <span><i class="fa-regular fa-calendar"></i> {post['datePublished']}</span>
            <span class="blog-cat"><a href="/category/{post.get('categorySlug', 'roof-monsters-news')}/">{post['category']}</a></span>
          </div>
          <h2><a href="/{post['slug']}/">{post['title']}</a></h2>
          <p>{post['description']}</p>
          <a href="/{post['slug']}/" class="read-more">Read more <i class="fa-solid fa-arrow-right"></i></a>
        </div>
      </article>""")
    return "\n".join(cards)


def build_blog_index() -> None:
    out = ROOT / "blog" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    content = HEAD.format(
        title="Roofing Blog | Tips & News | Roof Monsters Tampa Bay",
        description="Expert roofing tips, storm prep guides, and Tampa Bay industry insights from Roof Monsters — family-owned since 1988.",
    ) + """
  <section class="page-hero">
    <div class="container">
      <h1>Roofing <span class="accent">Blog</span></h1>
      <nav class="breadcrumb" aria-label="breadcrumb">
        <a href="/">Home</a>
        <i class="fa-solid fa-chevron-right"></i>
        <span>Blog</span>
      </nav>
    </div>
  </section>

  <section class="section-pad section-bg-white">
    <div class="container">
      <div class="section-header">
        <span class="section-eyebrow">Expert Insights</span>
        <h2>Tampa Bay Roofing Tips &amp; <span class="accent">News</span></h2>
        <p class="section-desc">Maintenance guides, storm preparation, and contractor advice from a Dunedin-based roofing team serving Pasco, Pinellas, and Hillsborough County since 1988.</p>
      </div>
      <div class="blog-grid blog-grid--listing">
""" + blog_cards() + """
      </div>
    </div>
  </section>
""" + FOOT
    out.write_text(content, encoding="utf-8")
    print(f"Wrote {out}")


def expand_blog_post(slug: str, body: str) -> None:
    path = ROOT / slug / "index.html"
    if not path.exists():
        return
    rest = path.read_text(encoding="utf-8")
    post = next(p for p in CONFIG["blogPosts"] if p["slug"] == slug)
    replacement = f"""
      <div class="blog-article-meta">
        <span><i class="fa-regular fa-calendar"></i> {post['datePublished']}</span>
        <span class="blog-cat">{post['category']}</span>
        <span><i class="fa-solid fa-user"></i> Roof Monsters Team</span>
      </div>
{body}
      <div class="blog-article-cta">
        <p><strong>Ready to schedule roofing work in Tampa Bay?</strong> Roof Monsters serves Pasco, Pinellas, Hernando, Hillsborough, and Manatee County from our Dunedin headquarters.</p>
        <a href="/contact-us/" class="btn btn-primary"><i class="fa-solid fa-arrow-right"></i> Get a Free Estimate</a>
      </div>"""
    hero_end = rest.index("</section>", rest.index("page-hero")) + len("</section>")
    after_hero = rest[hero_end:]
    article_start = after_hero.index('<section class="section-pad section-bg-white">')
    article_end = after_hero.index("</section>", article_start) + len("</section>")
    new_article = f"""
  <section class="section-pad section-bg-white">
    <div class="container blog-article">
      <div class="blog-article-hero">
        <img src="assets/{post['image'].replace('assets/', '')}" alt="{post['title']}" />
      </div>{replacement}
    </div>
  </section>"""
    new_text = rest[:hero_end] + new_article + after_hero[article_end:]
    new_text = new_text.replace('href="../index.html"', 'href="/"').replace('href="../blog.html"', 'href="/blog/"').replace('href="../contact.html"', 'href="/contact-us/"')
    path.write_text(new_text, encoding="utf-8")
    print(f"Expanded: {path}")


def main() -> None:
    build_blog_index()
    for slug, body in BLOG_BODY.items():
        expand_blog_post(slug, body)


if __name__ == "__main__":
    main()
