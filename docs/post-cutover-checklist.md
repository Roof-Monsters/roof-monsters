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
- [ ] Validate Fix on AggregateRating / review-snippet enhancement (224 invalid items; schema dedupe deployed 2026-07-23)
- [x] IndexNow ping 2026-07-23 (79 URLs, HTTP 200)

### Indexing snapshot (2026-07-23 Pages report)

- Indexed: **39**
- Not indexed: **65** (404×8, redirect×3, other 4xx×1, duplicate canonical×1, robots×1, crawled-not-indexed×29, discovered-not-indexed×22)
- Money URLs inspected are already indexed; remaining not-indexed is mostly legacy WP paths + Google “currently not indexed” queue

## Google Business Profile

- [ ] Website URL → `https://roofmonsters.co` (UTM on website link if desired)
- [ ] Primary phone `(727) 439-3869`, email `info@roofmonsters.co`
- [ ] Categories + services list aligned with site (no insurance-claim services)
- [ ] Photos + launch post
- [ ] Hours if published on GBP (omit from schema until confirmed)
