# Post-cutover checklist (DNS / GSC / GBP)

Do these **after** `roofmonsters.co` points at this GitHub Pages rebuild (not while legacy WordPress still owns production).

## Deploy

- [x] Push latest to `Roof-Monsters/roof-monsters`
- [ ] Confirm GitHub Pages build succeeds
- [ ] DNS / custom domain cutover for `roofmonsters.co` (+ www if used)
- [ ] Confirm Email Agent still receives/sends from `info@roofmonsters.co`

## Google Search Console

- [x] Property mapped (`sc-domain:roofmonsters.co` preferred)
- [ ] Submit `https://roofmonsters.co/sitemap.xml` (in progress — Jul 23 schema/indexing pass)
- [ ] Run full GSC audit: `node E:\Website Audit\GSC\tools\audit.mjs --site roofmonsters.co --ui`
- [ ] Priority URL inspection / Request indexing for importantPages in `E:\Website Audit\GSC\sites\roofmonsters.co.json`
- [ ] Validate Fix on AggregateRating enhancement after duplicate LocalBusiness schema deploy

## Google Business Profile

- [ ] Website URL → `https://roofmonsters.co` (UTM on website link if desired)
- [ ] Primary phone `(727) 439-3869`, email `info@roofmonsters.co`
- [ ] Categories + services list aligned with site (no insurance-claim services)
- [ ] Photos + launch post
- [ ] Hours if published on GBP (omit from schema until confirmed)
