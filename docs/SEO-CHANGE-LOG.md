# Roof Monsters SEO change log

## 2026-09-17 — GA4 click-to-call + form events (next-report wiring)

**Why:** They said they have not noticed more calls. Historical GA4 cannot prove or disprove site `tel:` taps — GTM-MRDB8975 only had GA4 config `G-N5H8R8C170`, Conversion Linker, and Ahrefs. No `phone_click`, `sms_click`, or form events. Google Business Profile **does** have call clicks (12 in 90 days, 11 after Jul 9).

**Shipped 2026-09-17:** `assets/js/main.js` sends `phone_click`, `sms_click`, `form_start`, `form_submit`, `form_success`, and `generate_lead` to dataLayer + gtag on production hosts only. After GitHub Pages is live, mark `phone_click`, `sms_click`, and `generate_lead` as key events in GA4 Admin → Events. Do not mark `form_submit` / `form_start`.

**Not this change:** titles, metas, or recrawl. GA4 property ID `546292072` is now in site JSON so the next audit exports the event table.

## 2026-09-10 — Conversion + local job ranking (not a title pack)

**Why:** Website-only client. GSC 2026-06-12–2026-09-07: 78 clicks / 28,280 impressions / **0.28% CTR** / pos 21.7. Impressions and clicks are up vs the prior audit, but they say they “haven’t noticed calls.” Forms still hit Formspree → info@ → iCloud. They measure the phone, not the inbox.

**Snippet / recrawl:** GSC said **request-indexing, do not rewrite titles**. Seven important URLs were crawled before live Last-Modified 2026-08-25. **No title/meta/H1 pack shipped.** Conversion, coverage tiers, job-rank labels, forms, schema, and AI files only.

**Deployed 2026-09-11:** commit `754bd25` is live (GitHub Pages Last-Modified Fri, 11 Sep 2026 12:34:48 GMT). Indexing requested after this ship. No title/meta rewrite.

**Shipped in source (now live):**

- Ranked job labels (Rank 1 replacement/repair/emergency/storm → Rank 4 gutters/skylights) on services hub, homepage mosaic, generated service pages, and hand hub pages.
- Coverage tiers on location hub + city pages: Pinellas core, nearby Tampa/west Pasco, extended Land O’ Lakes / Manatee. Explicit: not Jacksonville / Orlando / Miami.
- Forms: job-type select, “We Call You,” Pinellas-first note, far-city warning, success copy = callback.
- Sticky mobile call bar to (727) 439-3869.
- Removed false homepage mosaic line about a “true Atlas 20-year warranty.”
- FAQs: McKeever = Roof Monsters; we call you; no Jacksonville.
- Schema: Pinellas-first `areaServed` City objects, `knowsAbout`, `disambiguatingDescription`, OfferCatalog name. `llms.txt` / `ai.txt` link in head.
- Verbose `ai.txt`, `llms.txt`, `llms-full.txt`.

**Do not treat CTR as a failed experiment** until Google recrawls post-deploy HTML **and** 7 complete GSC days exist.

**Follow-up hotfix:** Nested service pages had `href="contact-us/"` (404 at `/services/.../contact-us/`). Pointed those CTAs at `/contact-us/` and added the missing blog `roof-monsters-way.webp` so CI validate passes.

**Indexing:** `node E:\Website Audit\GSC\tools\submit-indexing.mjs --site roofmonsters.co --stale-crawl` after this hotfix is live (quota ~10/day).

## 2026-09-10 — Remove test gallery composites

Removed three field-app test composites (Roof Flashing, Roof Patch Repairs, Repair Roof Flashing) from the gallery grid, `job-gallery.json`, and image assets. Detail URLs stay as noindex redirects to `/gallery/` so they are not shown as project proof.
