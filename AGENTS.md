# Roof Monsters — Agent Instructions

**Domain:** `roofmonsters.co`  
**Repo:** `E:\All Client Websites\roof-monsters`  
**GitHub:** `Roof-Monsters/roof-monsters`

## Public contact (use on site / GBP / directories)

- Phone: `(727) 439-3869`
- Email: `info@roofmonsters.co`
- HQ: Dunedin, Florida — Tampa Bay
- Licenses: Roofing CCC1335398, CCC052490 · Building CBC015719
- DBA of Terrance McKeever Enterprises, Inc.
- Family owned since 1988; Atlas shingles; 15-year workmanship warranty

## Internal ops (do NOT put on the public website)

See [`docs/ops-notes.md`](docs/ops-notes.md) for full detail. Summary:

- Lead sources are primarily **word of mouth / referrals**
- Payments sometimes include **cash / private-pay** — never advertise cash on the site
- **No insurance company work** — do not promise claim help, adjuster coordination, or “maximize your claim”
- Storm/emergency repair stays as **private-pay emergency response**
- Estimating uses the **Roofer** app (internal tooling only)
- Materials: **Atlas only**; sometimes sell Atlas product — explore Atlas contractor/dealer affiliation before claiming certified/dealer status
- Email Agent account: `zoho_roofmonsters_info` (Zoho REST → `info@roofmonsters.co`)
- OutreachEngine business id: `rm` / `roof_monsters` — **not** in active cold outreach until explicitly enabled

## Soft public trust language (allowed)

- Referrals / neighbors who recommend us
- Family-owned since 1988
- Clear written estimates
- Licensed & insured (liability / workers — not insurance *claims*)
- Atlas materials and warranties

## GSC audits

Config: `E:\GSC Auditer\sites\roofmonsters.co.json`  
`localRoot` should point at this folder. Full GSC audit after DNS cutover to this rebuild (live WP may still own production until then).

## SEO / build scripts

- `data/site-seo.json` + `scripts/apply-seo.py` / `scripts/seo_lib.py`
- Location pages: `scripts/build-location-pages.py` + `data/service-areas.json`
- Sitemap: `scripts/build-sitemap.py`
- Verify: `scripts/verify-sitemap-pages.py`, `scripts/verify-seo.py`
