# Roof Monsters — URL Map (live sitemap parity)

Demo routes use **root-relative paths** with trailing slashes (no `.html`), matching `roofmonsters.co` WordPress permalinks for seamless Google Search Console migration.

## Implemented pages

| Live URL | Demo path |
|----------|-----------|
| `/` | `index.html` |
| `/about-us/` | `about-us/index.html` |
| `/contact-us/` | `contact-us/index.html` |
| `/gallery/` | `gallery/index.html` |
| `/testimonials/` | `testimonials/index.html` |
| `/special-offers/` | `special-offers/index.html` |
| `/services/` | `services/index.html` |
| `/services/comprehensive-roof-installations/` | `services/comprehensive-roof-installations/index.html` |
| `/services/expert-roof-repairs-and-maintenance/` | `services/expert-roof-repairs-and-maintenance/index.html` |
| `/services/free-roof-inspections-and-consultations/` | `services/free-roof-inspections-and-consultations/index.html` |
| `/services/storm-damage-repair-specialists/` | `services/storm-damage-repair-specialists/index.html` |
| `/services/gutter-installation-and-cleaning/` | `services/gutter-installation-and-cleaning/index.html` |
| `/services/skylight-installation-and-repair/` | `services/skylight-installation-and-repair/index.html` |
| `/blog/` | `blog/index.html` |
| `/october-roofing-season-in-tampa-bay-why-fall-is-the-best-time-to-schedule-your-roof-work/` | `october-roofing-season-in-tampa-bay-why-fall-is-the-best-time-to-schedule-your-roof-work/index.html` |
| `/the-roof-monsters-way-what-sets-our-roofing-company-apart/` | `the-roof-monsters-way-what-sets-our-roofing-company-apart/index.html` |
| `/how-to-prepare-your-roof-for-floridas-hurricane-season/` | `how-to-prepare-your-roof-for-floridas-hurricane-season/index.html` |
| `/about-us/locations-we-serve/` | `about-us/locations-we-serve/index.html` |
| `/about-us/locations-we-serve/roofing-company-palm-harbor-florida/` | `about-us/locations-we-serve/roofing-company-palm-harbor-florida/index.html` |
| `/about-us/locations-we-serve/roofing-company-pinellas-county-florida/` | `about-us/locations-we-serve/roofing-company-pinellas-county-florida/index.html` |
| `/about-us/locations-we-serve/roofing-company-seminole-florida/` | `about-us/locations-we-serve/roofing-company-seminole-florida/index.html` |
| `/about-us/locations-we-serve/roofing-company-pasco-county-florida/` | `about-us/locations-we-serve/roofing-company-pasco-county-florida/index.html` |
| `/about-us/locations-we-serve/roofing-company-hernando-county-florida/` | `about-us/locations-we-serve/roofing-company-hernando-county-florida/index.html` |
| `/about-us/locations-we-serve/roofing-company-hillsborough-county-florida/` | `about-us/locations-we-serve/roofing-company-hillsborough-county-florida/index.html` |
| `/about-us/locations-we-serve/roofing-company-manatee-county-florida/` | `about-us/locations-we-serve/roofing-company-manatee-county-florida/index.html` |

## Live sitemap pages — add when built

Add each new folder + `index.html`, then append the URL to `sitemap.xml`.

| Live URL | Notes |
|----------|-------|
| `/warranty-guarantee/` | Warranty page |
| `/sustainability/` | Sustainability page |
| `/faqs/` | FAQs |
| `/what-is-tpo-roofing-and-why-its-perfect-for-florida-commercial-buildings/` | Blog post |
| `/5-signs-its-time-to-replace-your-roof-in-florida/` | Blog post |
| `/how-to-choose-the-right-roofing-contractor/` | Blog post |
| `/how-to-prepare-your-roof-for-storm-season/` | Blog post |
| `/the-benefits-of-eco-friendly-roofing-solutions/` | Blog post |
| `/advancements-in-roofing-technology-what-homeowners-need-to-know/` | Blog post |
| `/choosing-the-right-roofing-material-for-your-home/` | Blog post |
| `/the-importance-of-regular-roof-maintenance/` | Blog post |

## Conventions

- Internal links: root-relative with trailing slash (`/about-us/`, not `about-us.html`)
- Assets: `/assets/...`
- Includes: `/includes.js`, `/header.html`, `/footer.html`
- Blog posts live at **site root** (WordPress style), not under `/blog/` — only the listing is `/blog/`
- Regenerate sitemap after adding pages: `python scripts/build-sitemap.py` (or edit `sitemap.xml`)
- Regenerate location pages after editing areas: `python scripts/build-location-pages.py`

## Local preview

Serve from site root so `/about-us/` resolves:

```bash
cd roof-monsters
python -m http.server 5500
```

Open `http://127.0.0.1:5500/` — not `index.html` in the path.
