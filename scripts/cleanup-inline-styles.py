#!/usr/bin/env python3
"""Remove inline styles and dead form handlers across Roof Monsters HTML."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = [
    (r'\s*onsubmit="handleForm\(event\)"', ''),
    (r' style="margin-top:0;"', ''),
    (r' class="estimate-form" style="margin-top:0;"', ' class="estimate-form estimate-form--flush"'),
    (r'<span style="color:var\(--orange\);">\*</span>', '<span class="form-required">*</span>'),
    (r' class="btn-submit" style="margin-top:8px;"', ' class="btn-submit btn-submit--spaced"'),
    ('<p style="font-size:12px; color:var(--text-mid); margin-top:12px; text-align:center;">', '<p class="form-note">'),
    (r' style="background:var\(--white\);"', ' class="section-bg-white"'),
    (r'<i class="([^"]+)" style="opacity:1;color:var\(--orange\);font-size:28px;"></i>', r'<i class="\1"></i>'),
    (r'<i class="([^"]+)" style="font-size:18px;"></i>', r'<i class="\1 step-icon--md"></i>'),
    (r'<i class="([^"]+)" style="font-size:16px;"></i>', r'<i class="\1"></i>'),
    (r'<i class="([^"]+)" style="font-size:14px;"></i>', r'<i class="\1 step-icon--sm"></i>'),
    (r' class="why-card" style="grid-column: 1 / -1;"', ' class="why-card why-card--wide"'),
    (r' style="color:var\(--orange\)"', ' class="cta-phone-link"'),
    (r'<section class="section-pad" style="background:var\(--white\);">', '<section class="section-pad section-bg-white">'),
    (r'<div style="margin:24px 0; display:flex; flex-direction:column; gap:14px;">', '<div class="cta-action-stack">'),
    (
        r'<a href="tel:7274393869" class="btn btn-primary" style="display:flex; align-items:center; justify-content:center; gap:10px; text-decoration:none;">',
        '<a href="tel:7274393869" class="btn btn-primary btn-block">',
    ),
    (
        r'<a href="contact\.html" class="btn btn-primary" style="display:flex; align-items:center; justify-content:center; gap:10px; text-decoration:none; background:var\(--dark\);">',
        '<a href="contact.html" class="btn btn-primary btn-block btn-block--dark">',
    ),
    (r'<p style="font-size:13px; color:var\(--text-mid\);">', '<p class="license-note">'),
    (r'â€"', '—'),
]

for path in ROOT.rglob('*.html'):
    if 'GROWTH-ROADMAP' in path.name:
        continue
    text = path.read_text(encoding='utf-8')
    original = text
    for pattern, repl in REPLACEMENTS:
        if isinstance(pattern, str) and pattern.startswith('<') and '(' not in pattern[1:]:
            text = text.replace(pattern, repl)
        else:
            text = re.sub(pattern, repl, text)
    if text != original:
        path.write_text(text, encoding='utf-8')
        print(f'Updated {path.relative_to(ROOT)}')
