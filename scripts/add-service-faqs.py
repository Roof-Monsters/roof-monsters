#!/usr/bin/env python3
"""Add visible FAQ sections to service pages that lack them (for FAQPage schema)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "services"

FAQS: dict[str, list[tuple[str, str]]] = {
    "comprehensive-roof-installations": [
        (
            "How long does a full roof installation take?",
            "Most residential tear-off and installs finish in one to three days depending on size, pitch, weather, and decking repairs found after tear-off. We schedule around Tampa Bay storm windows and keep you updated if weather pauses work.",
        ),
        (
            "Do you use Atlas shingles on new installs?",
            "On qualifying steep-slope projects we install Atlas Designer Shingles, including Scotchgard protection on qualifying products. Manufacturer coverage follows Atlas terms and registration.",
        ),
        (
            "What warranties come with a new roof?",
            "Qualifying installation labor includes our 15-year workmanship warranty. Atlas manufacturer coverage applies on qualifying products after registration. We review both at final walkthrough.",
        ),
        (
            "Will you handle permits for a roof replacement?",
            "On qualifying replacements we handle permitting as required for your city or county and include that in the written scope so you know what is covered before work starts.",
        ),
        (
            "How do I prepare my home for installation day?",
            "Clear driveway access for dumpsters and materials, move vehicles, secure pets, and share gate codes or HOA rules when you schedule. We protect landscaping and complete magnetic nail sweeps on qualifying jobs.",
        ),
    ],
    "expert-roof-repairs-and-maintenance": [
        (
            "Can you repair a roof without replacing it?",
            "Often yes — if the system has life left and damage is localized. We document conditions with photos so you can plan repair now and replacement later if needed.",
        ),
        (
            "Do you repair roofs other companies installed?",
            "Yes. We evaluate existing work and fix deficiencies to Florida code regardless of who installed the original roof.",
        ),
        (
            "How fast can you schedule a roof repair?",
            "Many repairs schedule within days. Active leaks and storm openings are prioritized for private-pay emergency response.",
        ),
        (
            "What does preventative maintenance include?",
            "Typical visits cover leak tracing, flashing and pipe-boot checks, shingle or tile repairs, and recommendations for ventilation or gutter issues that shorten roof life in Florida humidity.",
        ),
        (
            "How much does roof repair cost?",
            "Simple flashing or shingle repairs differ widely from structural decking work. We inspect first and provide a clear written estimate before any paid work begins.",
        ),
    ],
    "free-roof-inspections-and-consultations": [
        (
            "Is the roof inspection really free?",
            "Yes. Free inspections and consultations are available across Pasco, Pinellas, Hernando, Hillsborough, and Manatee County with no obligation to hire us.",
        ),
        (
            "What do you look for during an inspection?",
            "We walk accessible roof planes and attic spaces when possible, photograph conditions, and explain repair versus replacement in plain language with a written follow-up.",
        ),
        (
            "How long does an inspection take?",
            "Most residential inspections take under an hour on site, plus time to prepare photos and recommendations. Complex commercial or multi-building properties may need longer.",
        ),
        (
            "Do I need to be home for the inspection?",
            "It helps for attic access and questions, but we can often inspect with gate codes and clear instructions if you cannot be present.",
        ),
        (
            "Will you pressure me to replace my roof?",
            "No. Most of our work comes from referrals. We recommend repair when it is the honest option and replacement only when the roof’s condition makes that the responsible path.",
        ),
    ],
    "storm-damage-repair-specialists": [
        (
            "What should I do after a storm opens my roof?",
            "Call (727) 439-3869 for private-pay emergency tarping and dry-in when needed. We document damage, then schedule permanent repairs with a clear written estimate.",
        ),
        (
            "Do you work with insurance companies?",
            "We focus on protecting your home and completing licensed private-pay repairs. We do not manage insurance claims or adjuster meetings.",
        ),
        (
            "How quickly can you tarp an active leak?",
            "Storm openings and active leaks are prioritized. Response timing depends on weather safety and call volume after major systems — call early so we can triage your address.",
        ),
        (
            "Will temporary tarping damage my roof further?",
            "Proper emergency tarping is meant to limit water intrusion until permanent repairs. We install temporary protection carefully and return for lasting repairs once conditions allow.",
        ),
        (
            "What areas do you cover for storm response?",
            "We serve Pasco, Pinellas, Hernando, Hillsborough, and Manatee County from our Dunedin headquarters, including after tropical weather when it is safe to work.",
        ),
    ],
    "gutter-installation-and-cleaning": [
        (
            "Do you install new gutters or only clean existing ones?",
            "Both. We install and clean gutters to protect fascia, foundation, and roof edges from Florida downpours.",
        ),
        (
            "How often should gutters be cleaned in Tampa Bay?",
            "Many homes need cleaning at least once or twice a year, more often under heavy tree cover. Clogged gutters push water under shingles and into soffits.",
        ),
        (
            "Can bad gutters cause roof leaks?",
            "Yes. Overflow and failed hangers can soak fascia and decking edges. We check gutter condition during roof inspections when relevant.",
        ),
        (
            "Do you match gutter color to my home?",
            "We discuss color and profile options during the estimate so new gutters fit your home’s look and water-management needs.",
        ),
        (
            "Are gutter services available with roof work?",
            "Yes. Many customers schedule gutter install or cleaning alongside roof repair or replacement so water management matches the new roof system.",
        ),
    ],
    "skylight-installation-and-repair": [
        (
            "Can you fix a leaking skylight without replacing it?",
            "Sometimes curb flashing, seals, or glass units can be repaired. We inspect first and recommend repair or replacement based on condition.",
        ),
        (
            "Do you install new skylights during a re-roof?",
            "Yes. Installing or replacing skylights during a full roof project often produces the cleanest flashing details and long-term watertight results.",
        ),
        (
            "Will a skylight increase my energy bills?",
            "Modern units with proper flashing and glazing can add light without the heat gain of older skylights. We discuss options for Florida sun exposure during the estimate.",
        ),
        (
            "How long does skylight installation take?",
            "Many residential skylight installs finish in a day when weather cooperates. Timing depends on curb work, roof access, and whether the surrounding roof field is also being replaced.",
        ),
        (
            "Are skylight repairs covered by your workmanship warranty?",
            "Qualifying installation labor on work we perform can include our 15-year workmanship warranty. Manufacturer coverage on the skylight unit follows the product maker’s terms.",
        ),
    ],
}


def faq_html(title_accent: str, pairs: list[tuple[str, str]]) -> str:
    items = "\n".join(
        f"""        <article class="faq-item">
          <h2>{q}</h2>
          <p>{a}</p>
        </article>"""
        for q, a in pairs
    )
    return f"""
  <section class="section-pad">
    <div class="container content-page">
      <div class="section-header">
        <span class="section-eyebrow">Common Questions</span>
        <h2>{title_accent}</h2>
      </div>
      <div class="faq-list">
{items}
      </div>
    </div>
  </section>
"""


TITLES = {
    "comprehensive-roof-installations": 'Roof Installation <span class="accent">FAQs</span>',
    "expert-roof-repairs-and-maintenance": 'Roof Repair <span class="accent">FAQs</span>',
    "free-roof-inspections-and-consultations": 'Inspection <span class="accent">FAQs</span>',
    "storm-damage-repair-specialists": 'Storm Damage <span class="accent">FAQs</span>',
    "gutter-installation-and-cleaning": 'Gutter Service <span class="accent">FAQs</span>',
    "skylight-installation-and-repair": 'Skylight <span class="accent">FAQs</span>',
}


def main() -> None:
    for slug, pairs in FAQS.items():
        path = ROOT / slug / "index.html"
        if not path.exists():
            print("missing", slug)
            continue
        text = path.read_text(encoding="utf-8")
        if 'class="faq-item"' in text:
            print("skip (has faqs)", slug)
            continue
        block = faq_html(TITLES[slug], pairs)
        # Insert before CTA section
        markers = [
            "<!-- CTA FORM -->",
            '<section class="service-cta-section">',
        ]
        inserted = False
        for marker in markers:
            if marker in text:
                text = text.replace(marker, block + "\n  " + marker, 1)
                inserted = True
                break
        if not inserted:
            text = text.replace("</body>", block + "\n</body>", 1)
        path.write_text(text, encoding="utf-8")
        print("added faqs", slug)


if __name__ == "__main__":
    main()
