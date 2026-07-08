#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

for path in ROOT.rglob('*.html'):
    if 'GROWTH-ROADMAP' in path.name:
        continue
    text = path.read_text(encoding='utf-8')
    original = text

    text = re.sub(
        r'class="([^"]+)"\s+class="([^"]+)"',
        lambda m: f'class="{m.group(1)} {m.group(2)}"',
        text,
    )
    text = text.replace(
        '<p style="font-size:12px; color:var(--text-mid); margin-top:12px; text-align:center;">',
        '<p class="form-note">',
    )
    text = text.replace('â€"', '—')

    if text != original:
        path.write_text(text, encoding='utf-8')
        print(f'Fixed {path.relative_to(ROOT)}')
