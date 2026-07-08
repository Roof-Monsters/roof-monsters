#!/usr/bin/env python3
"""Update gallery page with descriptive captions."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "gallery" / "index.html"

ITEMS = [
    ("installation-01.webp", "tall", "Atlas shingle roof installation in Clearwater, FL", "Clearwater", "Atlas Designer Shingles · Full Replacement"),
    ("project-02.webp", "", "Steep-slope roof repair in Dunedin, FL", "Dunedin", "Architectural Shingles · Repair & Flashing"),
    ("atlas-install-01.webp", "tall", "Atlas roof installation in Palm Harbor, FL", "Palm Harbor", "Atlas Scotchgard Shingles · New Install"),
    ("completed-03.webp", "", "Completed residential re-roof in Pinellas County, FL", "Pinellas County", "Architectural Shingles · Re-Roof"),
    ("crew-01.webp", "", "Roof Monsters installation crew on site in Tampa Bay", "Tampa Bay", "Licensed Crew · On-Site Install"),
    ("atlas-install-02.webp", "tall", "Atlas shingle installation in St. Petersburg, FL", "St. Petersburg", "Atlas Designer Shingles · Replacement"),
    ("installation-04.webp", "", "Roof installation project in Largo, FL", "Largo", "Architectural Shingles · Full Install"),
    ("pinellas-new-roof.webp", "", "New roof installation in Seminole, FL", "Seminole", "Architectural Shingles · New Construction"),
    ("project-09.webp", "", "Storm damage roof repair in Tampa, FL", "Tampa", "Storm Damage · Shingle & Flashing Repair"),
    ("replacement-08.webp", "", "Full roof replacement in New Port Richey, FL", "New Port Richey", "Architectural Shingles · Tear-Off & Re-Roof"),
    ("installation-07.webp", "", "Roof installation in Safety Harbor, FL", "Safety Harbor", "Atlas Shingles · Residential Install"),
    ("completed-06.webp", "", "Completed re-roof in Hillsborough County, FL", "Hillsborough County", "Architectural Shingles · Full Replacement"),
    ("quality-work.webp", "", "Quality roofing craftsmanship in Clearwater, FL", "Clearwater", "Designer Shingles · Detail Finish"),
    ("tampa-bay-project.webp", "", "Tampa Bay roofing project — residential re-roof", "Tampa Bay", "Architectural Shingles · Re-Roof"),
    ("rob-lewis-square.webp", "", "Roof Monsters team at Dunedin headquarters", "Dunedin HQ", "Family Owned · Since 1988"),
]

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <script>
(function () {
  var path = location.pathname;
  var marker = '/roof-monsters/';
  var idx = path.indexOf(marker);
  window.__RM_BASE__ = idx >= 0 ? path.slice(0, idx + marker.length) : '/';
  document.write('<base href="' + window.__RM_BASE__ + '">');
})();
  </script>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Project Gallery | Roof Monsters — Tampa Bay Roofing</title>
  <meta name="description" content="Browse Roof Monsters' project gallery — exceptional roofing installations, repairs, and custom solutions across Pasco, Pinellas, and Hillsborough County, FL." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,400;1,700&family=Roboto+Slab:wght@400;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />
  <link rel="stylesheet" href="assets/css/style.css" />
</head>
<body>
    <div id="site-header-include"></div>

<!-- PAGE HERO -->
  <section class="page-hero">
    <div class="container">
      <h1>Our Project <span class="accent">Gallery</span></h1>
      <nav class="breadcrumb" aria-label="breadcrumb">
        <a href="/">Home</a>
        <i class="fa-solid fa-chevron-right"></i>
        <span>Project Gallery</span>
      </nav>
    </div>
  </section>

  <!-- GALLERY GRID -->
  <section class="section-pad section-bg-light">
    <div class="container">
      <div class="section-header">
        <span class="section-eyebrow">Our Projects</span>
        <h2>Quality <span class="accent">Workmanship</span> Done Right The First Time.</h2>
        <p class="section-desc">Explore our project gallery showcasing exceptional roofing installations, repairs, and custom solutions — highlighting our craftsmanship and high-quality standards across Tampa Bay.</p>
      </div>
      <div class="gallery-page-grid">
"""

FOOT = """
      </div>
    </div>
  </section>

  <!-- CTA BANNER -->
  <section class="atlas-banner bg-atlas-banner-shingles">
    <div class="atlas-overlay"></div>
    <div class="container atlas-inner">
      <div class="atlas-content">
        <p class="section-eyebrow">Start Your Project</p>
        <h2>Ready For A <span class="accent">New Roof?</span></h2>
        <p>Join thousands of Tampa Bay homeowners who trust Roof Monsters for quality roofing solutions. Contact us today for your free inspection and estimate.</p>
        <a href="/contact-us/" class="btn btn-primary u-mt-20">Get A Free Estimate</a>
      </div>
      <div class="atlas-stat">
        <div class="atlas-num">10,000 +</div>
        <div class="atlas-label">Happy Clients All Over The Bay Area!</div>
      </div>
    </div>
  </section>
    <div id="site-footer-include"></div>

  <script src="includes.js"></script>
  <script src="assets/js/main.js"></script>
</body>
</html>
"""


def item_html(file: str, size: str, alt: str, city: str, meta: str) -> str:
    cls = f'gallery-page-item{" tall" if size else ""}'
    team_path = "assets/images/team/" if file == "rob-lewis-square.webp" else "assets/images/gallery/"
    return f"""
        <figure class="{cls}">
          <img src="{team_path}{file}" alt="{alt}" loading="lazy" />
          <figcaption class="gallery-caption"><span class="gallery-caption-city">{city}</span><span class="gallery-caption-meta">{meta}</span></figcaption>
        </figure>"""


def main() -> None:
    body = "".join(item_html(*row) for row in ITEMS)
    GALLERY.write_text(HEAD + body + FOOT, encoding="utf-8")
    print(f"Wrote {GALLERY}")


if __name__ == "__main__":
    main()
