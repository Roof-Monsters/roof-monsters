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


def estimate_form_compact(*, address_placeholder: str = "Street, City, FL") -> str:
    return f"""
        <form class="estimate-form" action="{FORM_ACTION}" method="POST" novalidate>
          <div class="estimate-form-fields">
{HONEYPOT}
          <div class="form-row">
            <div class="form-group">
              <label for="rm-name">Name</label>
              <input id="rm-name" type="text" name="name" placeholder="Your name" required autocomplete="name" />
            </div>
            <div class="form-group">
              <label for="rm-email">Email <span class="form-hint">(email or phone required)</span></label>
              <input id="rm-email" type="email" name="email" placeholder="you@email.com" autocomplete="email" inputmode="email" />
            </div>
          </div>
          <div class="form-group">
            <label for="rm-phone">Phone <span class="form-hint">(email or phone required)</span></label>
            <input id="rm-phone" type="tel" name="phone" placeholder="(727) 000-0000" autocomplete="tel" inputmode="tel" />
          </div>
          <div class="form-group">
            <label for="rm-address">Property Address</label>
            <input id="rm-address" type="text" name="address" placeholder="{esc(address_placeholder)}" autocomplete="street-address" />
          </div>
          <div class="form-group">
            <label for="rm-message">Message</label>
            <textarea id="rm-message" name="message" rows="3" placeholder="Tell us about your roofing needs"></textarea>
          </div>
          <button type="submit" class="btn-submit">Send Request</button>
          </div>
          <p class="form-note">Or email <a href="mailto:info@roofmonsters.co">info@roofmonsters.co</a> · Licensed &amp; Insured</p>
          <p class="form-success" hidden>
            <i class="fa-solid fa-circle-check" aria-hidden="true"></i>
            <span>Thank you — we received your request and will respond soon.</span>
          </p>
        </form>"""
