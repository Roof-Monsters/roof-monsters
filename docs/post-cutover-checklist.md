# Post-cutover checklist (DNS / GSC / GBP)

Do these **after** `roofmonsters.co` points at this GitHub Pages rebuild (not while legacy WordPress still owns production).

## Deploy

- [x] Push latest to `Roof-Monsters/roof-monsters`
- [ ] Confirm GitHub Pages build succeeds
- [ ] DNS / custom domain cutover for `roofmonsters.co` (+ www if used)
- [ ] Confirm Email Agent still receives/sends from `info@roofmonsters.co`

## Google Search Console

- [x] Property mapped (`sc-domain:roofmonsters.co` preferred)
- [x] Sitemap `https://roofmonsters.co/sitemap.xml` submitted (Success; last read 2026-07-17; 79 discovered)
- [x] Full GSC audit run 2026-07-23 (`E:\Website Audit\GSC\runs\2026-07-23\roofmonsters.co` + `gsc-audit/2026-07-23/`)
- [x] Priority URL inspection: all 10 importantPages PASS / Submitted and indexed
- [ ] Request indexing quota exhausted for today (Screen Team batch earlier) — retry tomorrow for location pages after AggregateRating fix
- [x] Validate Fix on AggregateRating / review-snippet enhancement (224 invalid items; schema dedupe deployed 2026-07-23)
- [x] Soft redirect stubs set to `noindex,follow` without JSON-LD (2026-07-27) so alias URLs stop emitting AggregateRating
- [x] Homepage FAQ visible section + FAQPage schema (2026-07-27)
- [x] Legacy `.html` redirect stubs for contact/about/locations/blog/faqs/gallery/services/testimonials (2026-07-27)
- [x] IndexNow ping 2026-07-23 (79 URLs, HTTP 200)

### Indexing snapshot

| Date | Indexed | Not indexed | Notes |
| --- | ---: | ---: | --- |
| 2026-07-23 | **39** | **65** | 404×8, redirect×3, other 4xx×1, duplicate×1, robots×1, crawled-not-indexed×29, discovered-not-indexed×22 |
| 2026-08-03 | **64** | **38** | 404×9, crawled-not-indexed×24, discovered×2, other 4xx×1, duplicate×1, robots×1 — sitemap still 79 discovered |

Money URLs inspected are already indexed; remaining not-indexed is mostly “crawled not indexed” + leftover 404s. Full CTR/indexing narrative: `docs/seo-performance-log.md`.

### CTR package (2026-08-03)

- [x] Baseline logged (Jul 29 API + Aug 3 UI) in `docs/seo-performance-log.md`
- [x] Title/meta CTR rewrites on reviews, about/McKeever, money services, all location pages (`scripts/apply-ctr-titles.py`)
- [ ] Deploy to production + request indexing on `/testimonials/`, `/about-us/`, top location URLs
- [ ] Fresh GSC API audit after ~14 days (`E:\Website Audit\GSC`) — append row to performance log

## Google Business Profile

- [ ] Website URL → `https://roofmonsters.co` (UTM on website link if desired)
- [ ] Primary phone `(727) 439-3869`, email `info@roofmonsters.co`
- [ ] Categories + services list aligned with site (no insurance-claim services)
- [ ] Photos + launch post
- [ ] Hours if published on GBP (omit from schema until confirmed)
