# Roof Monsters — Digital Presence Audit

**Client:** Terrance McKeever Enterprises dba Roof Monsters  
**Domain:** https://roofmonsters.co/  
**Audit date:** June 15, 2026  
**Prepared for:** Sales conversation + rebuild pitch  
**Lead contact:** (727) 439-3869 · roofmonsters@icloud.com  

**Service area:** Pasco, Pinellas, Hernando, Hillsborough & Manatee Counties — Tampa Bay, FL  
**HQ references:** Clearwater · Dunedin (1391 Robin Hood Ln) · Tarpon Springs  

**Local rebuild:** `e:\All Client Websites\roof-monsters`  
**Local preview:** http://127.0.0.1:5500/

---

## Executive summary

Roof Monsters has a **strong real-world reputation** — nearly 40 years in business, Atlas-backed warranties, military/first-responder discounts, and testimonials that emphasize communication and same-day response. The brand line **"Your Roof Is Our Proof"** is memorable and fits a family-owned contractor.

The live WordPress site **undermines that trust online**. Broken stat counters show **"0 +"** for experience and projects, the gallery still has **placeholder filler text**, mission/vision copy is **duplicated**, and key pages repeat the same form and testimonial blocks instead of doing their job. For a homeowner comparing three roofers on a phone after a storm, those details matter.

| Area | Grade | One-line verdict |
|------|-------|------------------|
| Brand & messaging | B+ | Strong tagline, warranty story, local identity |
| Reputation (reviews) | B | ~4.4–4.5★ / ~24 Google reviews — solid, room to grow |
| Website trust signals | C- | Broken counters, placeholder copy, inconsistent stats |
| Conversion UX | C | Forms everywhere; phone is good but buried in WP clutter |
| Content depth | B- | Blog is active; service pages thin; no city landing pages |
| Gallery / proof | D | Gallery page lacks real project showcase; lorem on homepage |
| Technical SEO | C | Basic WP SEO; missing RoofingContractor schema depth |
| Performance (est.) | C/D | WordPress + remote hero assets = likely slow mobile LCP |
| Local SEO | C+ | Counties named; no dedicated city/service URL strategy |
| Automation / tracking | ? | Unknown form routing, call tracking, CRM — needs discovery |

---

## Pros (what's working)

### Business fundamentals
- **Family owned since 1988** — 30+ years of operating history, Florida natives.
- **Atlas partnership** — 15-year workmanship warranty + Atlas 20-year system warranty is a real differentiator.
- **$750 hero discount** for military, veterans, first responders, and teachers — strong conversion hook.
- **Same-day / fast response** — repeated in reviews (Rob came same day, Terrance returned call in 30 min).
- **Wide service footprint** — residential + commercial across five counties.

### Website & content (partial)
- Clear primary CTA: **Free Estimates** and click-to-call **(727) 439-3869**.
- Service taxonomy covers installs, repairs, inspections, storm damage, gutters, skylights.
- **Blog is live** with Florida-relevant topics (hurricane prep, TPO, seasonal timing).
- Testimonials name real people and specific outcomes — not generic filler.
- Facebook presence linked from site.

### Local visibility
- Branded search returns roofmonsters.co with service-area messaging.
- Listed on local roofer directories with **4.4★ / 23 reviews** and Dunedin address.
- "Terrance McKeever Enterprises dba Roof Monsters" ties legal entity to brand.

---

## Cons (risks & opportunities)

### Critical: broken trust elements on the live site

| Issue | Where | Why it hurts |
|-------|-------|--------------|
| Stat counters stuck at **0 +** | Homepage, About | Makes a 40-year company look brand new or broken |
| **"A small river named Duden…"** placeholder | Homepage project section | Instant credibility loss — looks unfinished |
| **"Gallary"** typo | Gallery page title | Sloppy first impression |
| **"Our Mision"** typo | About page | Same |
| Vision copies mission verbatim | About page | Reads templated, not intentional |
| **"Mike Alexa — Atook \| Founder"** | Team section | Unclear / likely typo |
| Conflicting client counts | 10,000+ vs 1,200+ vs 0 | Numbers don't reinforce trust |
| Gallery page shows testimonials, not projects | `/gallery/` | Misses the #1 proof asset for roofers |

### Conversion & UX
- **Estimate forms repeated** on homepage, services, contact, gallery, special offers — form fatigue without clear hierarchy.
- No prominent **Google review widget** or star rating above the fold despite having real reviews.
- **roofmonsters@icloud.com** on contact — less professional than `@roofmonsters.co`.
- No visible **FL license / insurance / Atlas certification badges** near CTAs.
- Mobile nav and hero likely heavy — WordPress theme + slider + multiple font families.

### SEO & discoverability gaps
- No dedicated pages for high-intent local queries: *roof repair Clearwater*, *roof replacement Tampa*, *storm damage roof Pinellas*, etc.
- Likely missing or thin **RoofingContractor / LocalBusiness** JSON-LD with `areaServed`, `geo`, `aggregateRating`, `hasOfferCatalog`.
- Blog posts exist but may not interlink to service + city pages.
- Single social link (Facebook) — no GBP embed, Instagram, or review generation funnel visible.

### Technical (WordPress typical)
- Hero and gallery images load from `wp-content/uploads` — often oversized PNG/JPG without modern formats.
- Multiple Google Font families (Roboto, Roboto Slab, Inter) + Font Awesome + Elementor-style bloat.
- Plugin stack unknown without host access — likely similar performance drag as other WP contractor sites.
- No evidence of **GA4 event tracking** for `click_call`, `submit_estimate`, or `click_review`.

---

## Demo rebuild vs live site

A static rebuild preview exists locally with improvements already prototyped:

| Feature | Live (roofmonsters.co) | Demo rebuild (localhost:5500) |
|---------|------------------------|-------------------------------|
| Hero | WP slider | Ken Burns slider, cleaner CTA |
| Stats | Broken (0+) | Animated count-up (3,000+ roofs, etc.) |
| Service pages | Thin / bundled | Dedicated pages per service |
| Navigation | WP menu | Streamlined nav + mobile hamburger |
| Special offers | Basic block | Dedicated $750 offer page with proof points |
| Performance | WP overhead | Static HTML/CSS/JS — Lighthouse-friendly path |
| Gallery | Weak / missing projects | Structure ready for real project photos |
| Forms | Repeated WP forms | Validated estimate form pattern |

**Note:** Demo still hotlinks some images from the live WordPress media library. Production launch should migrate to optimized local/CDN assets.

---

## Highest-impact improvements (ranked)

1. **Fix or replace broken counters and remove all placeholder copy** — same-day trust fix.
2. **Build a real project gallery** — before/after, shingle types, storm repairs, commercial TPO.
3. **Launch city + service landing pages** — Clearwater, Tampa, St. Pete, Pasco, storm damage, replacement.
4. **Custom fast site** (or heavily optimized WP) — target 90+ mobile performance for storm-season mobile traffic.
5. **RoofingContractor schema** — licenses, warranties, service area, reviews (per Google guidelines).
6. **Review funnel** — on-site Google rating display + post-job SMS/email review requests.
7. **Call + form tracking** — GA4 events, optional call tracking number for ad attribution.
8. **Professional email** — `info@roofmonsters.co` or similar on Google Workspace.
9. **Credential strip** — licensed, insured, Atlas certified, BBB if applicable, near every CTA.
10. **CRM / lead routing** — ensure every form submission gets instant notification + follow-up task.

---

## Access needed for exact forecasts

| Access | Why |
|--------|-----|
| Google Business Profile | Calls, direction requests, review velocity, photo gaps |
| Google Search Console | Queries (city + service), indexing, CTR |
| GA4 | Top pages, form submissions, bounce on mobile |
| Form / email routing | Where leads go today, response time |
| Hosting / WP admin | Plugin list, cache, image sizes, security |
| Call tracking (if any) | Cost per lead from ads or directories |

Without access, growth estimates below are conservative planning ranges.

---

## Suggested next pass

1. Replace live homepage stats and remove Duden placeholder immediately (quick WP wins).
2. Upload 12–24 gallery photos with captions (shingle type, city, year).
3. Review demo rebuild with Rob/Terrance — align on brand, stats, team bios.
4. Deploy custom build with redirects, schema, tracking, and optimized images.
5. Launch 5–10 city/service pages and interlink from blog.
6. Run Lighthouse + Rich Results Test post-launch.

---

*Prepared by Knight Logics · knightlogics.com*
