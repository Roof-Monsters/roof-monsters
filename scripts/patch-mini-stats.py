#!/usr/bin/env python3
"""Normalize mini-stats banners to safer trust counters."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SAFE = """<div class="mini-stats-banner" data-countup>
    <div class="container mini-stats-inner">
      <div>
        <div class="mini-stat-num" data-target="40" data-suffix=" Years">40 Years</div>
        <div class="mini-stat-label">Roofing Experience</div>
      </div>
      <div>
        <div class="mini-stat-num" data-target="5">5</div>
        <div class="mini-stat-label">Counties Served</div>
      </div>
      <div>
        <div class="mini-stat-num" data-target="30" data-suffix=" +" data-rm-live-review-count data-rm-live-review-suffix=" +">30 +</div>
        <div class="mini-stat-label">Google Reviews</div>
      </div>
    </div>
  </div>"""

# From banner open through trailing orphaned mini-stat markup, stop before next comment/section.
BLOCK = re.compile(
    r'<div class="mini-stats-banner"[^>]*>'
    r'[\s\S]*?'
    r'(?=\s*(?:<!--|<section\b))',
)


def main() -> None:
    updated = 0
    paths = list((ROOT / "services").rglob("index.html")) + [ROOT / "about-us" / "index.html"]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        if "mini-stats-banner" not in text:
            continue
        new = BLOCK.sub(SAFE + "\n\n  ", text, count=1)
        if new != text:
            path.write_text(new, encoding="utf-8")
            print(f"Updated {path.relative_to(ROOT)}")
            updated += 1
    print(f"Done. Updated {updated} pages.")


if __name__ == "__main__":
    main()
