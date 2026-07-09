#!/usr/bin/env python3
"""Ensure estimate-form fields have name attributes and honeypot spam guard."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HONEYPOT = '<input type="text" name="_gotcha" class="form-honey" tabindex="-1" autocomplete="off" aria-hidden="true" />'
SUCCESS = '<p class="form-success" hidden>Thank you — we received your request and will respond soon.</p>'

FIELD_FIXES = [
    (r'<input([^>]*type="text"[^>]*)placeholder="(?:John Smith|Your name|First and last name)"([^>]*)>', r'<input\1name="name" placeholder="Your name" required autocomplete="name"\2>'),
    (r'<input([^>]*type="email"[^>]*)placeholder="(?:you@email\.com|Your email)"([^>]*)>', r'<input\1name="email" placeholder="you@email.com" required autocomplete="email"\2>'),
    (r'<input([^>]*type="tel"[^>]*)placeholder="(?:\(727\) 000-0000|\(727\) 000-0000)"([^>]*)>', r'<input\1name="phone" placeholder="(727) 000-0000" autocomplete="tel"\2>'),
    (r'<input([^>]*type="text"[^>]*)placeholder="(?:Street, City, FL|Street address|Street, City, FL)"([^>]*)>', r'<input\1name="address" placeholder="Street, City, FL" autocomplete="street-address"\2>'),
    (r'<textarea([^>]*)rows="[^"]*"([^>]*)placeholder="[^"]*"([^>]*)>', r'<textarea\1name="message" rows="4"\2placeholder="Tell us about your roofing needs"\3>'),
    (r'<select class="service-select"', r'<select class="service-select" name="service"'),
]


def patch_form_block(block: str) -> str:
    block = block.replace('name="_honey"', 'name="_gotcha"')
    if '_gotcha' not in block:
        block = block.replace("<form", f"<form", 1)
        block = re.sub(
            r'(<form[^>]*>)',
            r"\1\n          " + HONEYPOT,
            block,
            count=1,
        )
    for pattern, repl in FIELD_FIXES:
        block = re.sub(pattern, repl, block, flags=re.I)
    if 'class="form-success"' not in block and 'type="submit"' in block:
        block = re.sub(
            r'(<button[^>]*type="submit"[^>]*>.*?</button>)',
            r"\1\n          " + SUCCESS,
            block,
            count=1,
            flags=re.S | re.I,
        )
    if 'novalidate' not in block:
        block = re.sub(r"<form ", '<form novalidate ', block, count=1)
    if 'formspree.io/f/' not in block:
        block = re.sub(
            r'(<form[^>]*class="[^"]*estimate-form[^"]*"[^>]*)>',
            r'\1 action="https://formspree.io/f/mbdvvbnp" method="POST">',
            block,
            count=1,
            flags=re.I,
        )
    return block


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'class="estimate-form"' not in text:
        return False
    original = text

    def replacer(match: re.Match[str]) -> str:
        return patch_form_block(match.group(0))

    text = re.sub(
        r'<form[^>]*class="[^"]*estimate-form[^"]*"[^>]*>.*?</form>',
        replacer,
        text,
        flags=re.S | re.I,
    )
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        if path.parts[0] in {"scripts", "data"} or "node_modules" in path.parts:
            continue
        if patch_file(path):
            print(f"Patched {path.relative_to(ROOT)}")
            changed += 1
    print(f"Updated {changed} file(s)")


if __name__ == "__main__":
    main()
