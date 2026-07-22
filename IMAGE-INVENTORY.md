## Status: migrated (June 2026)

All images downloaded to `assets/images/`. HTML/CSS/header/footer use local paths. Testimonial avatars use `assets/images/brand/default-avatar.svg` instead of the logo.

Re-run downloads: `scripts/migrate-images.ps1`  
Re-apply URL map after HTML edits: `scripts/apply-local-assets.ps1`

---

## How to identify photos today

| Signal | Reliable? | Notes |
|--------|-----------|-------|
| `alt` attribute | **Best** | Most gallery/hero images have descriptive alts |
| Surrounding heading/copy | Good | Service pages tie images to context |
| WP filename | **Poor** | `IMG_*.jpg`, `FireShot-Capture-*`, hash names tell you nothing |
| CSS `background-image` | Partial | Often no alt; check section title |

**Recommendation:** When you migrate, rename to `category-subject-location.webp` (e.g. `gallery-atlas-shingle-clearwater.webp`) and keep this mapping.

---

## Unique images (30) — suggested local names

| Current WP file | Alt / context | Suggested local path |
|-----------------|---------------|----------------------|
| `unnamed.png` | Roof Monsters Logo | `assets/images/brand/logo.webp` |
| `IMG_6006.jpg` | Roof Installation Project | `assets/images/gallery/installation-01.webp` |
| `IMG_5993.jpg` | Roofing Work | `assets/images/gallery/project-02.webp` |
| `IMG_5994-1.jpg` | Completed Roof Project | `assets/images/gallery/completed-03.webp` |
| `IMG_6015.jpg` | Roof Installation | `assets/images/gallery/installation-04.webp` |
| `473619572_*.jpg` | Roof Monsters Team | `assets/images/team/crew-01.webp` |
| `436379617_*-1536x1536.jpg` | Roof Monsters Team | `assets/images/team/rob-lewis.webp` |
| `FireShot-Capture-102-*.png` | Atlas Roof Installation | `assets/images/gallery/atlas-install-01.webp` |
| `FireShot-Capture-103-*.png` | Atlas Roof Project | `assets/images/gallery/atlas-install-02.webp` |
| `Atlas_Designer_Shingles_*-1024x400.jpg` | Atlas Designer Shingles banner | `assets/images/brand/atlas-shingles-banner.webp` |
| `New-Roof-Pinellas-County-Florida.jpg` | Roofing Company Pinellas Florida | `assets/images/gallery/pinellas-new-roof.webp` |
| `F6.jpg` | (stats section bg, no alt) | `assets/images/backgrounds/stats-section.webp` |
| `us-veteran-woman-*-1536x1024.jpg` | Special offers hero | `assets/images/offers/military-discount-hero.webp` |
| `roof-instalaltion.webp` | Roof inspection | `assets/images/services/inspections.webp` |
| `roof-instalation-roofmonster-*.webp` | Roof installation in progress | `assets/images/services/installation.webp` |
| `repair-maintenance-*.webp` | Skylight installation | `assets/images/services/skylights.webp` |
| `guteere2-*.webp` | Gutter installation | `assets/images/services/gutters.webp` |
| `emergency-roof-repair-*.webp` | Emergency storm damage | `assets/images/services/storm-damage.webp` |
| `F5.jpg` | Completed roofing project | `assets/images/gallery/completed-05.webp` |
| `F25.jpg` | Roof Monsters crew at work | `assets/images/team/crew-at-work.webp` |
| `IMG_7565.jpeg` | Completed Roofing Project | `assets/images/gallery/completed-06.webp` |
| `IMG_7610.jpeg` | Roofing Installation | `assets/images/gallery/installation-07.webp` |
| `IMG_7611.jpg` | Roof Replacement Project | `assets/images/gallery/replacement-08.webp` |
| `IMG_7612.jpg` | Roof Monsters Project | `assets/images/gallery/project-09.webp` |
| `4353A7A7*.jpg` | Roof Monsters Quality Work | `assets/images/gallery/quality-work.webp` |
| `F28F4EF9*.jpg` | Tampa Bay Roofing Project | `assets/images/gallery/tampa-bay-project.webp` |
| `Gemini_Generated_Image_*.png` | Blog: October roofing season | `assets/images/blog/october-roofing-season.webp` |
| `aftermath-of-hurricane-debby-*.jpg` | Blog: Hurricane prep | `assets/images/blog/hurricane-prep.webp` |
| `happy-customer.jpg` | Blog: Roof Monsters Way | `assets/images/blog/happy-customer.webp` |

## Wrong alts fixed during migration

- Testimonial/review avatars now use `default-avatar.svg` instead of the logo PNG
- `service-skylights.html` uses `services/skylights.webp` (copy of repairs photo until a dedicated skylight shot is supplied)

## Jul 2026 client feedback (captions / brand)

- Homepage + `/gallery/` captions neutralized to Tampa Bay / project-type labels until client supplies verified descriptions
- Official static logo: `assets/images/brand/logo-official.webp` (+ `.png`); spinning assets retained for revert — see `docs/client-feedback-jul-2026.md`
- Brand accent shifted from metallic gold to logo orange `#FD982A`
