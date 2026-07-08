#!/usr/bin/env python3
"""Add data-countup + data-target to mini-stats banners (variable first-stat labels)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BANNER_RE = re.compile(
    r'<div class="mini-stats-banner">\s*'
    r'<div class="container mini-stats-inner">\s*'
    r'<div>\s*'
    r'<div class="mini-stat-num">3,000 \+</div>\s*'
    r'<div class="mini-stat-label">[^<]+</div>\s*'
    r'</div>\s*'
    r'<div>\s*'
    r'<div class="mini-stat-num">5,000 \+</div>\s*'
    r'<div class="mini-stat-label">Satisfied Customers</div>\s*'
    r'</div>\s*'
    r'<div>\s*'
    r'<div class="mini-stat-num">10 K \+</div>\s*'
    r'<div class="mini-stat-label">5-Star Reviews</div>\s*'
    r'</div>\s*'
    r'</div>\s*'
    r'</div>',
    re.DOTALL,
)

REPLACEMENT = (
    '<div class="mini-stats-banner" data-countup>\n'
    '    <div class="container mini-stats-inner">\n'
    '      <div>\n'
    '        <div class="mini-stat-num" data-target="3000" data-suffix=" +">3,000 +</div>\n'
    '        <div class="mini-stat-label">LABEL1</div>\n'
    '      </div>\n'
    '      <div>\n'
    '        <div class="mini-stat-num" data-target="5000" data-suffix=" +">5,000 +</div>\n'
    '        <div class="mini-stat-label">Satisfied Customers</div>\n'
    '      </div>\n'
    '      <div>\n'
    '        <div class="mini-stat-num" data-target="10" data-suffix=" K +">10 K +</div>\n'
    '        <div class="mini-stat-label">5-Star Reviews</div>\n'
    '      </div>\n'
    '    </div>\n'
    '  </div>'
)

LABEL_RE = re.compile(
    r'<div class="mini-stats-banner">\s*'
    r'<div class="container mini-stats-inner">\s*'
    r'<div>\s*'
    r'<div class="mini-stat-num">3,000 \+</div>\s*'
    r'<div class="mini-stat-label">([^<]+)</div>',
    re.DOTALL,
)

def patch(text: str) -> str:
    match = LABEL_RE.search(text)
    if not match:
        return text
    label = match.group(1)
    replacement = REPLACEMENT.replace("LABEL1", label)
    return BANNER_RE.sub(replacement, text, count=1)

for path in (ROOT / "services").rglob("index.html"):
    text = path.read_text(encoding="utf-8")
    new_text = patch(text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"Updated {path.relative_to(ROOT)}")
