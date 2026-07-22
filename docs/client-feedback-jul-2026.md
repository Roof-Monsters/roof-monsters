## Client visual feedback — Jul 2026

Source: client email after reviewing the initial Roof Monsters site.

### Done in this pass

1. **Brand colors** — Replaced metallic yellow-gold (`#D4AF37`) with official logo orange (`#FD982A` / `#E07E14` / `#FFB65C`) sampled from the ROOF wordmark. CSS vars `--gold*` / `--orange*` now map to that palette; brand blue/purple tokens added for future use.
2. **Official logo (static)** — Header, mobile drawer, footer, and team section use `logo-official.webp/png` with `object-fit: contain` (no stretch). Spinning split-logo markup + CSS kept for revert:
   - Markup template: `partials/brand-logo-spin.html`
   - Assets still available: `logo-bg.*`, `logo-monster.*`
   - Spin CSS remains in `assets/css/style.css`
3. **Homepage hero sharpness** — Swapped soft/overcompressed hero slides for sharper photos; reduced Ken Burns zoom (`1.12` → `1.04`); lightened the dark overlay; softened eyebrow text stroke that looked fuzzy.
4. **Photo captions** — Homepage gallery captions neutralized to verified-safe Tampa Bay / project-type labels until the client supplies correct locations and descriptions.

### Waiting on client

- Correct photo descriptions + additional photos
- Confirmation if any accent should lean more blue/purple from the yard sign
- Performance agreement (non-site item from their email)
- They are staying on **Roofr** for estimating — no app transition work

### Revert spinning logo

Replace each static `.rm-brand-logo--static` block with the markup in `partials/brand-logo-spin.html` (set the size modifier: `--header`, `--drawer`, `--footer`, or `--team`) and drop the `--static` class.
