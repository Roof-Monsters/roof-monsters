# Roof Monsters SEO Performance Log

Living record of GSC baselines, indexing health, and each SEO change batch — so we can see what moved clicks vs what only moved impressions.

**Property:** `sc-domain:roofmonsters.co`  
**Production:** https://roofmonsters.co  
**Cutover / sitemap submit:** 2026-07-09  
**Audit tooling:** `E:\Website Audit\GSC` (source of truth for API audits)

---

## Snapshot baselines

| Date | Source | Window | Clicks | Impressions | CTR | Avg position | Indexed | Sitemap discovered |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2026-07-09 | Cutover | — | — | — | — | — | ~pre-cutover (majority not indexed) | `/sitemap.xml` submitted |
| 2026-07-23 | Post-cutover checklist | Pages report | — | — | — | — | **39** | 79 |
| 2026-07-29 | GSC API audit `gsc-audit/2026-07-29` | 90d (Apr 30–Jul 26) | **35** | **4,697** | **0.75%** | **32.4** | — | 79 |
| 2026-08-03 | GSC UI (user screenshots) | Last 3 months | **67** | **9.57K** | **0.7%** | **30.1** | **64** | **79** |

### Read on the 7/9 → now pattern

- **Impressions roughly doubled** after cutover + sitemap + indexing recovery. That is working.
- **CTR stayed ~0.7%** because most new impressions sit deep in the SERP (**avg position ~30**). Expected organic CTR near position 30 is often ~0.5–1%, so flat CTR with rising impressions is normal until rankings climb **or** page-1/2 snippets convert better.
- **Clicks did rise in absolute terms** (35 → 67 across comparable windows), but not as fast as impressions — so the ratio looks “stuck.”
- Brand queries (`roof monsters`, `monsters roofing`, `roof monster`) already drive most clicks. Non-brand commercial queries are mostly positions 20–40 with near-zero CTR.

### Position bucket reality (API export ending 2026-07-26)

| Position band | Impressions | Clicks | CTR |
| --- | ---: | ---: | ---: |
| 1–3 | 45 | 1 | 2.2% |
| 4–10 | 289 | 4 | 1.4% |
| 11–20 | 427 | 0 | 0.0% |
| 21–40 | 1,626 | 9 | 0.55% |
| 41–100 | 1,279 | 2 | 0.16% |

**Implication:** ~60%+ of query impressions are beyond page 2. Title/meta wins matter most on URLs already ranking roughly positions **4–15**. Ranking work matters for the rest.

---

## Highest-ROI CTR leaks (pre–2026-08-03 fix)

From `gsc-audit/2026-07-29/api/performance.json` (page + query):

| Opportunity | Evidence | Why it hurts CTR |
| --- | --- | --- |
| `/testimonials/` | ~250 impressions @ avg pos **7.5**, **0 clicks** | Review intent queries ranking on page 1 with a weak SERP pitch |
| `roof monster reviews` / `roof-monster reviews` | ~142 combined impressions @ pos ~6, **0 clicks** (later UI showed some recovery) | Same page; snippet must scream reviews + rating |
| `mckeever` | 39 impressions @ pos **5.7**, **0 clicks** | About page title lacked McKeever name in SERP title |
| `/services/emergency-roof-repair/` | ~343 impressions @ pos ~36 | Deep ranking; still need Tampa + 24/7 in title for when it climbs |
| TPO blog + `/services/tpo-roofing/` | High impressions, 0 CTR @ pos ~30 | Same |
| Location pages (Lakewood Ranch, Land O' Lakes, Wesley Chapel, etc.) | Hundreds of impressions each @ pos 22–35 | Generic “Roofing Company in X” titles |

Homepage was already the only strong converter (~3.7% CTR @ pos ~12.6).

---

## Change log

### 2026-08-03 — CTR title/meta package (`apply-ctr-titles.py`)

**Goal:** Raise click ratio on URLs already getting impressions (esp. reviews + about + money services + all location pages), without waiting for position gains.

**Before (examples):**

| Page | Title (before) |
| --- | --- |
| `/testimonials/` | Roof Monster Reviews \| Real Customer Testimonials — Tampa Bay |
| `/about-us/` | About Us \| Roof Monsters — Tampa Bay Roofing Since 1988 |
| Location pages | Roofing Company in {City}, FL \| Roof Monsters |
| `/services/emergency-roof-repair/` | Emergency Roof Repair in Tampa Bay \| 24/7 Tarping — Roof Monsters |
| Free inspections meta | Truncated mid-sentence (“…and detailed.”) |
| Homepage meta | Corrupted star character (`4.4?`) in some views |

**After (examples):**

| Page | Title (after) |
| --- | --- |
| `/testimonials/` | Roof Monsters Reviews (4.4★) \| Real Tampa Bay Customers |
| `/about-us/` | About Terrance McKeever & Roof Monsters \| Since 1988 |
| Location pages | `{City} Roofing \| Repair & Replacement — Roof Monsters` |
| `/services/emergency-roof-repair/` | Emergency Roof Repair Tampa \| 24/7 Tarping Response |
| Free inspections | Free Roof Inspection Tampa Bay \| No-Cost Assessment (+ complete meta) |

**Also updated:** services hub, roof repair, roof replacement, TPO service + TPO blog, storm damage, contact, special offers, Roof Monsters Way post, all `/about-us/locations-we-serve/*` city/county pages.

**Code/template follow-through:**

- `scripts/apply-ctr-titles.py` — one-shot / re-runnable CTR rewrite
- `scripts/build-location-pages.py` — future location rebuilds use the new title/meta pattern
- Page list: `docs/seo-ctr-update-2026-08-03-pages.txt`

**Expected lag:** Google often takes **1–3 weeks** to refresh snippets; measure with a fresh GSC API audit after ~14 days.

**Negative-change watch:** If any branded CTR drops, revert that page’s title first (brand titles can over-optimize). Track reviews CTR and homepage CTR separately.

**Deploy required:** Push to production GitHub Pages so live HTML matches this repo.

**Deploy status (2026-08-03):** ✅ Pushed to `main` (`6d16d94`). Live verified — e.g. `/testimonials/` title updated on production.

**IndexNow (2026-08-03):** ✅ Submitted all 45 CTR-updated URLs (HTTP 200).

**GSC indexing requests:** ⏳ Blocked on expired OAuth token — `npm run auth` is waiting for a one-time Google consent click (cannot be automated without your Google account). After that, indexing submit + API audits run unattended.

---

### Indexing gap (79 sitemap / 64 indexed) — open work

| Reason (GSC UI ~2026-08-03) | Pages | Action |
| --- | ---: | --- |
| Crawled – currently not indexed | 24 | Quality/thin or soft-competition; strengthen unique copy; re-request indexing on priority URLs after content touch |
| Not found (404) | 9 | Fix or 301 remaining legacy URLs; clear dead internal links |
| Discovered – currently not indexed | 2 | Internal links + IndexNow / Inspect URL |
| Blocked other 4xx | 1 | Fix response code |
| Duplicate without user-selected canonical | 1 | Confirm canonical |
| Blocked by robots.txt | 1 | Allow if intentional money URL; else leave |

Progress vs 2026-07-23: **39 → 64 indexed** (good). Remaining gap is mostly Google’s “crawled not indexed” queue + leftover 404s — not a missing sitemap.

---

## Measurement plan (next checkpoints)

1. Re-auth GSC (`E:\Website Audit\GSC` → `npm run auth`) then:
   ```powershell
   cd "E:\Website Audit\GSC"
   node tools/audit.mjs --site roofmonsters.co --ui
   ```
2. Log a new row in the baseline table above.
3. Compare specifically:
   - `/testimonials/` CTR and clicks
   - Brand query CTR (`roof monsters`, reviews variants)
   - Overall CTR and avg position
   - Indexed count vs 79
4. If reviews CTR rises but overall CTR does not, next lever is **ranking** (on-page for pos 11–20 local queries: inspections / emergency / Clearwater), not more title tweaks.

---

## Related artifacts

- `gsc-audit/2026-07-27/`, `gsc-audit/2026-07-29/`
- `docs/post-cutover-checklist.md`
- `E:\Website Audit\runs\*\roofmonsters.co` (when present)
- `E:\Website Audit\GSC\sites\roofmonsters.co.json`
