#!/usr/bin/env python3
"""Sync formspree-id.txt into data/site-forms.json for client-side form posts."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID_FILE = ROOT / "formspree-id.txt"
CONFIG_PATH = ROOT / "data" / "site-forms.json"
RECIPIENT = "info@roofmonsters.co"


def main() -> None:
    form_id = ID_FILE.read_text(encoding="utf-8").strip() if ID_FILE.exists() else ""
    endpoint = ""
    if form_id and form_id != "PLACEHOLDER":
        endpoint = f"https://formspree.io/f/{form_id}"

    config = {
        "provider": "formspree",
        "formspreeId": form_id or "PLACEHOLDER",
        "endpoint": endpoint,
        "recipientEmail": RECIPIENT,
        "subjectPrefix": "Roof Monsters website lead",
        "fallbackEmail": RECIPIENT,
        "fallbackPhone": "(727) 439-3869",
    }
    CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    if endpoint:
        print(f"Wrote Formspree endpoint for {RECIPIENT}: {endpoint}")
    else:
        print(
            "Wrote site-forms.json with PLACEHOLDER form ID. "
            f"Create a Formspree form for {RECIPIENT}, paste the ID into formspree-id.txt, and re-run."
        )


if __name__ == "__main__":
    main()
