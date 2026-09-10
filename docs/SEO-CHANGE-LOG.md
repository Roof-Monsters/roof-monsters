# Roof Monsters SEO change log

## 2026-09-10 — Conversion + local job ranking (not a title pack)

**Why:** Website-only client. GSC 2026-06-12–2026-09-07: 78 clicks / 28,280 impressions / **0.28% CTR** / pos 21.7. Impressions and clicks are up vs the prior audit, but they say they “haven’t noticed calls.” Forms still hit Formspree → info@ → iCloud. They measure the phone, not the inbox.

**Snippet / recrawl:** GSC said **request-indexing, do not rewrite titles**. Seven important URLs were crawled before live Last-Modified 2026-08-25. **No title/meta/H1 pack shipped.** Conversion, coverage tiers, job-rank labels, forms, schema, and AI files only.

**Shipped in source (deploy to go live):**

- Ranked job labels (Rank 1 replacement/repair/emergency/storm → Rank 4 gutters/skylights) on services hub, homepage mosaic, generated service pages, and hand hub pages.
- Coverage tiers on location hub + city pages: Pinellas core, nearby Tampa/west Pasco, extended Land O’ Lakes / Manatee. Explicit: not Jacksonville / Orlando / Miami.
- Forms: job-type select, “We Call You,” Pinellas-first note, far-city warning, success copy = callback.
- Sticky mobile call bar to (727) 439-3869.
- Removed false homepage mosaic line about a “true Atlas 20-year warranty.”
- FAQs: McKeever = Roof Monsters; we call you; no Jacksonville.
- Schema: Pinellas-first `areaServed` City objects, `knowsAbout`, `disambiguatingDescription`, OfferCatalog name. `llms.txt` / `ai.txt` link in head.
- Verbose `ai.txt`, `llms.txt`, `llms-full.txt`.

**Do not treat CTR as a failed experiment** until Google recrawls post-deploy HTML **and** 7 complete GSC days exist.

**Follow-up:** After deploy, `node E:\Website Audit\GSC\tools\submit-indexing.mjs --site roofmonsters.co --stale-crawl` (quota ~10/day).

## 2026-09-10 — Remove test gallery composites

Removed three field-app test composites (Roof Flashing, Roof Patch Repairs, Repair Roof Flashing) from the gallery grid, `job-gallery.json`, and image assets. Detail URLs stay as noindex redirects to `/gallery/` so they are not shown as project proof.
