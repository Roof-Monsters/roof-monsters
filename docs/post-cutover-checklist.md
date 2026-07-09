# Post-cutover checklist (DNS / GSC / GBP)

Do these **after** `roofmonsters.co` points at this GitHub Pages rebuild (not while legacy WordPress still owns production).

## Deploy

- [x] Push latest to `Roof-Monsters/roof-monsters`
- [ ] Confirm GitHub Pages build succeeds
- [ ] DNS / custom domain cutover for `roofmonsters.co` (+ www if used)
- [ ] Confirm Email Agent still receives/sends from `info@roofmonsters.co`

## Google Search Console

- [ ] Property mapped (`sc-domain:roofmonsters.co` preferred)
- [ ] Submit `https://roofmonsters.co/sitemap.xml`
- [ ] Run GSC Auditer full audit: `node E:\GSC Auditer\tools\audit.mjs --full` (site config `localRoot` already set)
- [ ] Priority URL inspection for importantPages in `E:\GSC Auditer\sites\roofmonsters.co.json`

## Google Business Profile

- [ ] Website URL → `https://roofmonsters.co` (UTM on website link if desired)
- [ ] Primary phone `(727) 439-3869`, email `info@roofmonsters.co`
- [ ] Categories + services list aligned with site (no insurance-claim services)
- [ ] Photos + launch post
- [ ] Hours if published on GBP (omit from schema until confirmed)
