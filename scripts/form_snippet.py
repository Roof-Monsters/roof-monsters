"""Shared estimate-form HTML for Roof Monsters page generators."""

from __future__ import annotations

import html


def esc(text: str) -> str:
    return html.escape(text, quote=True)


HONEYPOT = """
          <div class="form-honey-wrap" aria-hidden="true">
            <input id="rm-gotcha" type="text" name="_gotcha" class="form-honey" tabindex="-1" autocomplete="off" aria-label="Company website" />
          </div>"""

FORM_ACTION = "https://formspree.io/f/mbdvvbnp"

JOB_OPTIONS = [
    ("Roof Replacement", "Roof Replacement — primary"),
    ("Roof Repair / Leak", "Roof Repair / Leak — primary"),
    ("Emergency / Storm (need tarp)", "Emergency / Storm — primary"),
    ("Free Inspection", "Free Inspection"),
    ("Atlas / Shingle Install", "Atlas / Shingle Install"),
    ("Commercial / Flat / TPO", "Commercial / Flat / TPO"),
    ("Gutters or Skylights", "Gutters or Skylights — add-on"),
    ("Other", "Other"),
]


def _job_select(form_id: str) -> str:
    opts = "\n            ".join(
        f'<option value="{esc(value)}">{esc(label)}</option>' for value, label in JOB_OPTIONS
    )
    return f"""
          <div class="form-group">
            <label for="{form_id}-job">What do you need?</label>
            <select id="{form_id}-job" class="service-select" name="service" required>
            <option value="" selected disabled>Choose the job type</option>
            {opts}
            </select>
          </div>"""


def estimate_form_compact(
    *,
    address_placeholder: str = "Street, City, FL (Tampa Bay)",
    form_id: str = "rm",
) -> str:
    fid = form_id or "rm"
    return f"""
        <form class="estimate-form" action="{FORM_ACTION}" method="POST" novalidate>
          <div class="estimate-form-fields">
{HONEYPOT}
          <div class="form-row">
            <div class="form-group">
              <label for="{fid}-name">Name</label>
              <input id="{fid}-name" type="text" name="name" placeholder="Your name" required autocomplete="name" />
            </div>
            <div class="form-group">
              <label for="{fid}-email">Email <span class="form-required form-required--either" aria-hidden="true">*</span></label>
              <input id="{fid}-email" type="email" name="email" placeholder="you@email.com" autocomplete="email" inputmode="email" />
            </div>
          </div>
          <div class="form-group">
            <label for="{fid}-phone">Phone <span class="form-required form-required--either" aria-hidden="true">*</span></label>
            <input id="{fid}-phone" type="tel" name="phone" placeholder="(727) 000-0000" autocomplete="tel" inputmode="tel" />
          </div>
          {_job_select(fid)}
          <div class="form-group">
            <label for="{fid}-address">Property Address</label>
            <input id="{fid}-address" type="text" name="address" placeholder="{esc(address_placeholder)}" autocomplete="street-address" />
          </div>
          <div class="form-group">
            <label for="{fid}-message">Message</label>
            <textarea id="{fid}-message" name="message" rows="3" placeholder="Tell us about your roofing needs"></textarea>
          </div>
          <button type="submit" class="btn-submit">Send Request — We Call You</button>
          </div>
          <p class="form-note">We call the number you leave. Pinellas / Tampa Bay first. We do not serve Jacksonville or Orlando. Or call <a href="tel:7274393869">(727) 439-3869</a>.</p>
          <p class="form-success" hidden>
            <i class="fa-solid fa-circle-check" aria-hidden="true"></i>
            <span>Got it — we will call you at the number you provided. Keep (727) 439-3869 handy if it is a leak or storm.</span>
          </p>
        </form>"""
