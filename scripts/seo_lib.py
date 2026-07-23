"""Shared SEO helpers for Roof Monsters static site."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data" / "site-seo.json"
AREAS_PATH = ROOT / "data" / "service-areas.json"

ENCODING_FIXES = {
    "â€”": "—",
    "â€“": "–",
    "â€˜": "'",
    "â€™": "'",
    "â€œ": '"',
    "â€\x9d": '"',
    "â„¢": "™",
    "â€¦": "…",
    "Ã—": "×",
    "Â·": "·",
}

SEO_MARKER_START = "<!-- rm-seo:start -->"
SEO_MARKER_END = "<!-- rm-seo:end -->"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def load_areas() -> dict:
    if not AREAS_PATH.exists():
        return {"areas": []}
    return json.loads(AREAS_PATH.read_text(encoding="utf-8"))


def fix_encoding(text: str) -> str:
    for bad, good in ENCODING_FIXES.items():
        text = text.replace(bad, good)
    return text


def page_path_to_url(path: Path, base: str) -> str:
    rel = path.parent.relative_to(ROOT)
    if rel == Path("."):
        return urljoin(base, "/")
    return urljoin(base, "/" + "/".join(rel.parts) + "/")


def extract_title(text: str) -> str:
    m = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
    return html.unescape(m.group(1).strip()) if m else "Roof Monsters"


def extract_description(text: str) -> str:
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', text, re.I)
    return html.unescape(m.group(1)) if m else ""


def extract_breadcrumbs(text: str) -> list[dict[str, str]]:
    m = re.search(r'<nav class="breadcrumb"[^>]*>(.*?)</nav>', text, re.I | re.S)
    if not m:
        return []
    crumbs: list[dict[str, str]] = []
    inner = m.group(1)
    for a in re.finditer(r'<a\s+href="([^"]+)"[^>]*>(.*?)</a>', inner, re.I | re.S):
        crumbs.append({"name": strip_tags(a.group(2)), "url": a.group(1)})
    for span in re.finditer(r"<span>(.*?)</span>", inner, re.I | re.S):
        name = strip_tags(span.group(1))
        if name:
            crumbs.append({"name": name, "url": ""})
    return crumbs


def strip_tags(value: str) -> str:
    return re.sub(r"<[^>]+>", "", value).strip()


def og_image_for(path: Path, config: dict) -> str:
    base = config["canonicalBase"].rstrip("/")
    rel = path.parent.relative_to(ROOT)
    parts = rel.parts
    blog_slugs = {p["slug"] for p in config["blogPosts"]}
    if parts and parts[0] in blog_slugs:
        slug = parts[0]
        for post in config["blogPosts"]:
            if post["slug"] == slug:
                return f"{base}/{post['image']}"
    if "services" in parts:
        return f"{base}/assets/images/gallery/quality-work.webp"
    if "locations-we-serve" in parts:
        return f"{base}/assets/images/gallery/pinellas-new-roof.webp"
    return config["business"]["image"]


def classify_page(path: Path) -> str:
    rel = path.parent.relative_to(ROOT)
    if rel == Path("."):
        return "home"
    parts = rel.parts
    if parts == ("contact-us",):
        return "contact"
    if parts == ("about-us",):
        return "about"
    if parts == ("blog",):
        return "blog-index"
    if parts == ("faqs",):
        return "faq"
    if parts == ("gallery",):
        return "gallery"
    if parts == ("testimonials",):
        return "testimonials"
    if parts in {("privacy-policy",), ("terms-of-service",), ("warranty-guarantee",)}:
        return "webpage"
    if len(parts) == 2 and parts[0] == "category":
        return "category"
    blog_slugs = {p["slug"] for p in load_config()["blogPosts"]}
    if len(parts) == 1 and parts[0] in blog_slugs:
        return "blog-post"
    if parts == ("services",):
        return "services-hub"
    if len(parts) == 2 and parts[0] == "services":
        return "service"
    if parts == ("about-us", "locations-we-serve"):
        return "locations-hub"
    if len(parts) == 3 and parts[:2] == ("about-us", "locations-we-serve"):
        return "location"
    return "standard"


def _strip_context(node: dict) -> dict:
    return {k: v for k, v in node.items() if k != "@context"}


def graph_block(nodes: list[dict]) -> str:
    cleaned = [_strip_context(n) for n in nodes if n]
    payload = json.dumps(
        {"@context": "https://schema.org", "@graph": cleaned},
        ensure_ascii=False,
        indent=2,
    )
    return f'  <script type="application/ld+json">\n{payload}\n  </script>'


def _absolute_url(href: str, page_url: str, base: str) -> str:
    if href.startswith("/"):
        return urljoin(base.rstrip("/") + "/", href.lstrip("/"))
    if href.startswith("http"):
        return href
    if href in ("./", "../", "..", ""):
        return base.rstrip("/") + "/"
    return urljoin(page_url, href)


def breadcrumb_schema(crumbs: list[dict[str, str]], page_url: str, base: str) -> dict | None:
    if not crumbs:
        crumbs = [{"name": "Home", "url": page_url}]
    if len(crumbs) == 1 and crumbs[0]["name"].lower() == "home":
        crumbs = [{"name": "Home", "url": "/"}]
    items = []
    for i, crumb in enumerate(crumbs, start=1):
        item: dict = {
            "@type": "ListItem",
            "position": i,
            "name": crumb["name"],
        }
        if crumb.get("url"):
            item["item"] = _absolute_url(crumb["url"], page_url, base)
        elif i == len(crumbs):
            item["item"] = page_url
        items.append(item)
    return {
        "@type": "BreadcrumbList",
        "@id": f"{page_url}#breadcrumb",
        "itemListElement": items,
    }


def path_breadcrumbs(path: Path, page_url: str, title: str, config: dict) -> list[dict[str, str]]:
    """Build breadcrumbs from URL path when HTML nav crumbs are missing/incomplete."""
    rel = path.parent.relative_to(ROOT)
    if rel == Path("."):
        return [{"name": "Home", "url": "/"}]

    crumbs: list[dict[str, str]] = [{"name": "Home", "url": "/"}]
    parts = rel.parts
    labels = {
        "about-us": "About Us",
        "locations-we-serve": "Service Areas",
        "services": "Services",
        "contact-us": "Contact",
        "faqs": "FAQs",
        "blog": "Blog",
        "gallery": "Gallery",
        "testimonials": "Reviews",
        "special-offers": "Special Offers",
        "warranty-guarantee": "Warranty",
        "privacy-policy": "Privacy Policy",
        "terms-of-service": "Terms of Service",
        "sustainability": "Sustainability",
        "category": "Blog Categories",
    }

    blog_slugs = {p["slug"]: p for p in config.get("blogPosts", [])}
    if len(parts) == 1 and parts[0] in blog_slugs:
        crumbs.append({"name": "Blog", "url": "/blog/"})
        crumbs.append(
            {
                "name": title.split("|")[0].strip() or blog_slugs[parts[0]].get("title", parts[0]),
                "url": "",
            }
        )
        return crumbs

    built = ""
    for i, part in enumerate(parts):
        built += f"/{part}"
        is_last = i == len(parts) - 1
        if part in labels:
            name = labels[part]
        elif part.startswith("roofing-company-"):
            name = title.split("|")[0].replace("Roofing Company in", "").strip() or part.replace("-", " ").title()
        elif parts[0] == "services" and i == 1:
            service = next((s for s in config.get("services", []) if s["slug"] == part), None)
            name = service["name"] if service else title.split("|")[0].strip()
        elif parts[0] == "category" and i == 1:
            name = part.replace("-", " ").title()
        else:
            name = part.replace("-", " ").title()
        crumbs.append({"name": name, "url": "" if is_last else f"{built}/"})
    if crumbs:
        crumbs[-1]["url"] = ""
        if not crumbs[-1]["name"]:
            crumbs[-1]["name"] = title.split("|")[0].strip()
    return crumbs


def merge_breadcrumbs(html_crumbs: list[dict[str, str]], path_crumbs: list[dict[str, str]]) -> list[dict[str, str]]:
    if len(html_crumbs) >= 2:
        return html_crumbs
    return path_crumbs


def review_nodes(config: dict) -> list[dict]:
    reviews = config.get("business", {}).get("reviews") or []
    nodes = []
    for rev in reviews:
        nodes.append(
            {
                "@type": "Review",
                "author": {"@type": "Person", "name": rev["author"]},
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": rev.get("ratingValue", "5"),
                    "bestRating": "5",
                },
                "name": rev.get("name", "Customer review"),
                "reviewBody": rev["reviewBody"],
            }
        )
    return nodes


def organization_schema(config: dict) -> dict:
    b = config["business"]
    base = config["canonicalBase"].rstrip("/")
    return {
        "@type": "Organization",
        "@id": f"{base}/#organization",
        "name": b["name"],
        "legalName": b["legalName"],
        "url": base,
        "logo": {"@type": "ImageObject", "url": b["logo"]},
        "image": b["image"],
        "telephone": b["telephone"],
        "email": b["email"],
        "sameAs": b["sameAs"],
        "foundingDate": b["foundingDate"],
    }


def roofing_contractor_schema(config: dict, *, include_reviews: bool = False) -> dict:
    b = config["business"]
    base = config["canonicalBase"].rstrip("/")
    offer_items = [
        {
            "@type": "Offer",
            "itemOffered": {
                "@type": "Service",
                "name": s["name"],
                "url": f"{base}/services/{s['slug']}/",
            },
        }
        for s in config.get("services", [])
    ]
    schema: dict = {
        "@type": ["RoofingContractor", "LocalBusiness"],
        "@id": f"{base}/#roofingcontractor",
        "name": b["name"],
        "legalName": b["legalName"],
        "url": base,
        "telephone": b["telephone"],
        "email": b["email"],
        "description": b["description"],
        "foundingDate": b["foundingDate"],
        "priceRange": b["priceRange"],
        "image": b["image"],
        "logo": b["logo"],
        "address": {
            "@type": "PostalAddress",
            **b["address"],
        },
        "geo": {
            "@type": "GeoCoordinates",
            **b["geo"],
        },
        "areaServed": b["areaServed"],
        "sameAs": b["sameAs"],
        "parentOrganization": {"@id": f"{base}/#organization"},
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": b["telephone"],
            "email": b["email"],
            "contactType": "customer service",
            "areaServed": "US-FL",
            "availableLanguage": ["English"],
        },
        "identifier": [
            {"@type": "PropertyValue", "name": "Florida Roofing License", "value": "CCC1335398"},
            {"@type": "PropertyValue", "name": "Florida Roofing License", "value": "CCC052490"},
            {"@type": "PropertyValue", "name": "Florida Building License", "value": "CBC015719"},
        ],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": b["aggregateRating"]["ratingValue"],
            "reviewCount": b["aggregateRating"]["reviewCount"],
            "bestRating": "5",
            "worstRating": "1",
        },
    }
    hours = b.get("openingHoursSpecification") or []
    if hours:
        schema["openingHoursSpecification"] = [
            {"@type": "OpeningHoursSpecification", **spec} for spec in hours
        ]
    if offer_items:
        schema["hasOfferCatalog"] = {
            "@type": "OfferCatalog",
            "name": "Roofing Services",
            "itemListElement": offer_items,
        }
    if include_reviews:
        reviews = review_nodes(config)
        if reviews:
            schema["review"] = reviews
    return schema


def contractor_ref(config: dict) -> dict:
    base = config["canonicalBase"].rstrip("/")
    return {"@id": f"{base}/#roofingcontractor"}


def organization_ref(config: dict) -> dict:
    base = config["canonicalBase"].rstrip("/")
    return {"@id": f"{base}/#organization"}


def website_schema(config: dict) -> dict:
    base = config["canonicalBase"].rstrip("/")
    return {
        "@type": "WebSite",
        "@id": f"{base}/#website",
        "name": config["business"]["name"],
        "url": base,
        "publisher": contractor_ref(config),
        "inLanguage": "en-US",
    }


def webpage_schema(
    config: dict,
    page_url: str,
    title: str,
    description: str,
    *,
    page_types: str | list[str] = "WebPage",
    breadcrumb_id: str | None = None,
) -> dict:
    base = config["canonicalBase"].rstrip("/")
    node: dict = {
        "@type": page_types,
        "@id": f"{page_url}#webpage",
        "url": page_url,
        "name": title,
        "description": description,
        "isPartOf": {"@id": f"{base}/#website"},
        "about": contractor_ref(config),
        "publisher": contractor_ref(config),
        "inLanguage": "en-US",
    }
    if breadcrumb_id:
        node["breadcrumb"] = {"@id": breadcrumb_id}
    return node


def faq_schema_from_html(text: str, page_url: str) -> dict | None:
    items = []
    patterns = [
        r'<article class="faq-item">\s*<h2>(.*?)</h2>\s*<p>(.*?)</p>\s*</article>',
        r'<article class="faq-item">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</article>',
        r'<div class="faq-item">\s*<h2>(.*?)</h2>\s*<p>(.*?)</p>\s*</div>',
        r'<details[^>]*>\s*<summary>(.*?)</summary>\s*<p>(.*?)</p>\s*</details>',
    ]
    for pat in patterns:
        for m in re.finditer(pat, text, re.I | re.S):
            question = strip_tags(m.group(1))
            answer = strip_tags(m.group(2))
            if question and answer and len(question) > 8 and len(answer) > 20:
                items.append(
                    {
                        "@type": "Question",
                        "name": question,
                        "acceptedAnswer": {"@type": "Answer", "text": answer},
                    }
                )
        if items:
            break
    if not items:
        return None
    seen: set[str] = set()
    unique = []
    for item in items:
        key = item["name"].lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return {
        "@type": "FAQPage",
        "@id": f"{page_url}#faq",
        "mainEntity": unique,
    }


def local_business_schema(config: dict, area_name: str, page_url: str) -> dict:
    base = roofing_contractor_schema(config, include_reviews=True)
    base["@id"] = f"{page_url}#localbusiness"
    base["url"] = page_url
    base["areaServed"] = [area_name, *config["business"]["areaServed"]]
    base["parentOrganization"] = organization_ref(config)
    return base


def service_schema(config: dict, service: dict, page_url: str) -> dict:
    base = config["canonicalBase"].rstrip("/")
    return {
        "@type": "Service",
        "@id": f"{page_url}#service",
        "name": service["name"],
        "description": service["description"],
        "serviceType": "Roofing",
        "provider": contractor_ref(config),
        "areaServed": config["business"]["areaServed"],
        "url": page_url,
        "image": f"{base}/assets/images/gallery/quality-work.webp",
        "offers": {
            "@type": "Offer",
            "availability": "https://schema.org/InStock",
            "url": page_url,
            "priceCurrency": "USD",
            "description": "Free written estimate — pricing based on inspection scope",
        },
    }


def article_schema(config: dict, post: dict, page_url: str, title: str, description: str) -> dict:
    base = config["canonicalBase"].rstrip("/")
    return {
        "@type": "BlogPosting",
        "@id": f"{page_url}#article",
        "headline": title,
        "description": description,
        "datePublished": post["datePublished"],
        "dateModified": post.get("dateModified", post["datePublished"]),
        "author": contractor_ref(config),
        "publisher": {
            "@type": "Organization",
            "name": config["business"]["name"],
            "@id": f"{base}/#organization",
            "logo": {
                "@type": "ImageObject",
                "url": config["business"]["logo"],
            },
        },
        "image": f"{base}/{post['image']}",
        "mainEntityOfPage": {"@id": f"{page_url}#webpage"},
        "url": page_url,
        "inLanguage": "en-US",
        "isPartOf": {"@id": f"{base}/#website"},
    }


def services_itemlist(config: dict) -> dict:
    base = config["canonicalBase"].rstrip("/")
    return {
        "@type": "ItemList",
        "@id": f"{base}/services/#itemlist",
        "name": "Roof Monsters Roofing Services",
        "numberOfItems": len(config.get("services", [])),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "name": s["name"],
                "url": f"{base}/services/{s['slug']}/",
            }
            for i, s in enumerate(config.get("services", []), start=1)
        ],
    }


def locations_itemlist(config: dict) -> dict:
    base = config["canonicalBase"].rstrip("/")
    areas = load_areas().get("areas", [])
    return {
        "@type": "ItemList",
        "@id": f"{base}/about-us/locations-we-serve/#itemlist",
        "name": "Roof Monsters Service Areas",
        "numberOfItems": len(areas),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "name": a.get("shortName") or a.get("name"),
                "url": f"{base}/about-us/locations-we-serve/{a['slug']}/",
            }
            for i, a in enumerate(areas, start=1)
            if a.get("slug")
        ],
    }


def blog_itemlist(config: dict) -> dict:
    base = config["canonicalBase"].rstrip("/")
    posts = config.get("blogPosts", [])
    return {
        "@type": "ItemList",
        "@id": f"{base}/blog/#itemlist",
        "name": "Roof Monsters Blog Posts",
        "numberOfItems": len(posts),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "name": p["title"],
                "url": f"{base}/{p['slug']}/",
            }
            for i, p in enumerate(posts, start=1)
        ],
    }


def gallery_itemlist(config: dict) -> dict:
    base = config["canonicalBase"].rstrip("/")
    images = config.get("galleryImages", [])
    return {
        "@type": "ImageGallery",
        "@id": f"{base}/gallery/#gallery",
        "name": "Roof Monsters Project Gallery",
        "url": f"{base}/gallery/",
        "about": contractor_ref(config),
        "hasPart": {
            "@type": "ItemList",
            "numberOfItems": len(images),
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i,
                    "item": {
                        "@type": "ImageObject",
                        "contentUrl": f"{base}/assets/images/gallery/{img['file']}",
                        "url": f"{base}/assets/images/gallery/{img['file']}",
                        "name": img["name"],
                    },
                }
                for i, img in enumerate(images, start=1)
            ],
        },
    }


def testimonials_itemlist(config: dict) -> dict:
    base = config["canonicalBase"].rstrip("/")
    reviews = review_nodes(config)
    return {
        "@type": "ItemList",
        "@id": f"{base}/testimonials/#itemlist",
        "name": "Roof Monsters Customer Reviews",
        "numberOfItems": len(reviews),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "item": rev,
            }
            for i, rev in enumerate(reviews, start=1)
        ],
    }


def geo_meta_tags(config: dict) -> str:
    b = config["business"]
    addr = b["address"]
    geo = b["geo"]
    lat = geo["latitude"]
    lng = geo["longitude"]
    placename = f"{addr['addressLocality']}, {addr['addressRegion']}"
    return (
        f'  <meta name="geo.region" content="US-{html.escape(addr["addressRegion"], quote=True)}" />\n'
        f'  <meta name="geo.placename" content="{html.escape(placename, quote=True)}" />\n'
        f'  <meta name="geo.position" content="{lat};{lng}" />\n'
        f'  <meta name="ICBM" content="{lat}, {lng}" />\n'
    )


def build_seo_head(path: Path, text: str, config: dict) -> str:
    page_url = page_path_to_url(path, config["canonicalBase"])
    title = extract_title(text)
    description = extract_description(text)
    og_image = og_image_for(path, config)
    page_type = classify_page(path)
    geo_meta = geo_meta_tags(config)
    base = config["canonicalBase"].rstrip("/")

    html_crumbs = extract_breadcrumbs(text)
    path_crumbs = path_breadcrumbs(path, page_url, title, config)
    crumbs = merge_breadcrumbs(html_crumbs, path_crumbs)
    crumb = breadcrumb_schema(crumbs, page_url, config["canonicalBase"])
    crumb_id = f"{page_url}#breadcrumb" if crumb else None

    graph: list[dict] = []

    if page_type == "home":
        graph.append(organization_schema(config))
        graph.append(roofing_contractor_schema(config, include_reviews=True))
        graph.append(website_schema(config))
        graph.append(
            webpage_schema(
                config,
                page_url,
                title,
                description,
                page_types=["WebPage", "CollectionPage"],
                breadcrumb_id=crumb_id,
            )
        )
    elif page_type == "contact":
        graph.append(organization_schema(config))
        graph.append(roofing_contractor_schema(config, include_reviews=True))
        graph.append(website_schema(config))
        graph.append(
            webpage_schema(
                config,
                page_url,
                title,
                description,
                page_types="ContactPage",
                breadcrumb_id=crumb_id,
            )
        )
    elif page_type == "about":
        graph.append(organization_schema(config))
        graph.append(roofing_contractor_schema(config, include_reviews=True))
        graph.append(website_schema(config))
        graph.append(
            webpage_schema(
                config,
                page_url,
                title,
                description,
                page_types="AboutPage",
                breadcrumb_id=crumb_id,
            )
        )
    elif page_type == "faq":
        graph.append(organization_schema(config))
        graph.append(roofing_contractor_schema(config))
        graph.append(website_schema(config))
        graph.append(webpage_schema(config, page_url, title, description, breadcrumb_id=crumb_id))
    elif page_type == "blog-index":
        graph.append(organization_schema(config))
        graph.append(roofing_contractor_schema(config))
        graph.append(website_schema(config))
        graph.append(
            webpage_schema(
                config,
                page_url,
                title,
                description,
                page_types=["WebPage", "CollectionPage"],
                breadcrumb_id=crumb_id,
            )
        )
        graph.append(blog_itemlist(config))
    elif page_type == "services-hub":
        graph.append(organization_schema(config))
        graph.append(roofing_contractor_schema(config))
        graph.append(website_schema(config))
        graph.append(
            webpage_schema(
                config,
                page_url,
                title,
                description,
                page_types=["WebPage", "CollectionPage"],
                breadcrumb_id=crumb_id,
            )
        )
        graph.append(services_itemlist(config))
    elif page_type == "locations-hub":
        graph.append(organization_schema(config))
        graph.append(roofing_contractor_schema(config))
        graph.append(website_schema(config))
        graph.append(
            webpage_schema(
                config,
                page_url,
                title,
                description,
                page_types=["WebPage", "CollectionPage"],
                breadcrumb_id=crumb_id,
            )
        )
        graph.append(locations_itemlist(config))
    elif page_type == "service":
        slug = path.parent.name
        service = next((s for s in config["services"] if s["slug"] == slug), None)
        graph.append(organization_schema(config))
        graph.append(roofing_contractor_schema(config))
        graph.append(website_schema(config))
        if service:
            graph.append(service_schema(config, service, page_url))
        graph.append(webpage_schema(config, page_url, title, description, breadcrumb_id=crumb_id))
    elif page_type == "location":
        area_name = title.split("|")[0].replace("Roofing Company in", "").strip()
        graph.append(organization_schema(config))
        graph.append(local_business_schema(config, area_name, page_url))
        graph.append(website_schema(config))
        graph.append(webpage_schema(config, page_url, title, description, breadcrumb_id=crumb_id))
    elif page_type == "gallery":
        graph.append(organization_schema(config))
        graph.append(roofing_contractor_schema(config))
        graph.append(website_schema(config))
        graph.append(webpage_schema(config, page_url, title, description, breadcrumb_id=crumb_id))
        graph.append(gallery_itemlist(config))
    elif page_type == "testimonials":
        graph.append(organization_schema(config))
        graph.append(roofing_contractor_schema(config, include_reviews=True))
        graph.append(website_schema(config))
        graph.append(webpage_schema(config, page_url, title, description, breadcrumb_id=crumb_id))
        graph.append(testimonials_itemlist(config))
    elif page_type == "blog-post":
        slug = path.parent.name
        post = next((p for p in config["blogPosts"] if p["slug"] == slug), None)
        graph.append(organization_schema(config))
        graph.append(roofing_contractor_schema(config))
        graph.append(website_schema(config))
        if post:
            graph.append(article_schema(config, post, page_url, title, description))
        graph.append(webpage_schema(config, page_url, title, description, breadcrumb_id=crumb_id))
    else:
        graph.append(organization_schema(config))
        graph.append(roofing_contractor_schema(config))
        graph.append(website_schema(config))
        graph.append(webpage_schema(config, page_url, title, description, breadcrumb_id=crumb_id))

    # FAQ schema from visible Q&A content (never invent FAQs)
    if page_type in {
        "faq",
        "service",
        "location",
        "about",
        "contact",
        "webpage",
        "standard",
        "testimonials",
        "gallery",
    }:
        faq = faq_schema_from_html(text, page_url)
        if faq:
            graph.append(faq)

    if crumb:
        graph.append(crumb)

    schema_html = graph_block(graph)
    return f"""{SEO_MARKER_START}
  <link rel="canonical" href="{html.escape(page_url, quote=True)}" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />
{geo_meta}  <meta property="og:type" content="{'website' if page_type == 'home' else 'article' if page_type == 'blog-post' else 'website'}" />
  <meta property="og:site_name" content="Roof Monsters" />
  <meta property="og:title" content="{html.escape(title, quote=True)}" />
  <meta property="og:description" content="{html.escape(description, quote=True)}" />
  <meta property="og:url" content="{html.escape(page_url, quote=True)}" />
  <meta property="og:image" content="{html.escape(og_image, quote=True)}" />
  <meta property="og:locale" content="en_US" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{html.escape(title, quote=True)}" />
  <meta name="twitter:description" content="{html.escape(description, quote=True)}" />
  <meta name="twitter:image" content="{html.escape(og_image, quote=True)}" />
{schema_html}
  <script>
(function () {{
  var path = location.pathname;
  var marker = '/roof-monsters/';
  var idx = path.indexOf(marker);
  if (idx < 0) return;
  var demoBase = "{html.escape(config['demoBase'].rstrip('/'), quote=True)}";
  var rel = path.slice(idx + marker.length - 1);
  if (!rel.endsWith('/')) {{
    var last = rel.lastIndexOf('/');
    rel = last > 0 ? rel.slice(0, last + 1) : '/';
  }}
  var canonical = demoBase + (rel === '/' ? '/' : rel);
  var link = document.querySelector('link[rel="canonical"]');
  if (link) link.setAttribute('href', canonical);
  ['og:url'].forEach(function (prop) {{
    var meta = document.querySelector('meta[property="' + prop + '"]');
    if (meta) meta.setAttribute('content', canonical);
  }});
}})();
  </script>
{SEO_MARKER_END}"""


def _strip_orphan_seo_artifacts(text: str) -> str:
    """Remove SEO meta/schema left outside rm-seo markers from older injections.

    FAQPage / BreadcrumbList / LocalBusiness already live in the @graph block, so
    stripping all application/ld+json before re-inject is safe and required to
    clear GSC 'multiple AggregateRating' on location pages.
    """
    text = re.sub(
        r"\s*<script\s+type=[\"']application/ld\+json[\"']\s*>.*?</script>\s*",
        "\n",
        text,
        flags=re.S | re.I,
    )
    text = re.sub(
        r"\s*<link\s+rel=[\"']canonical[\"'][^>]*>\s*",
        "\n",
        text,
        flags=re.I,
    )
    # Meta names the SEO block re-injects
    for name in (
        "robots",
        "geo.region",
        "geo.placename",
        "geo.position",
        "ICBM",
        "twitter:card",
        "twitter:title",
        "twitter:description",
        "twitter:image",
    ):
        text = re.sub(
            rf"\s*<meta\s+name=[\"']{re.escape(name)}[\"'][^>]*>\s*",
            "\n",
            text,
            flags=re.I,
        )
    # Open Graph properties the SEO block re-injects
    for prop in (
        "og:type",
        "og:site_name",
        "og:title",
        "og:description",
        "og:url",
        "og:image",
        "og:locale",
    ):
        text = re.sub(
            rf"\s*<meta\s+property=[\"']{re.escape(prop)}[\"'][^>]*>\s*",
            "\n",
            text,
            flags=re.I,
        )
    # Collapse runs of blank lines left by stripping
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def inject_seo(text: str, seo_block: str) -> str:
    """Replace any existing SEO block, including orphaned start/end markers."""
    # Remove balanced blocks
    text = re.sub(
        rf"\s*{re.escape(SEO_MARKER_START)}.*?{re.escape(SEO_MARKER_END)}\s*",
        "\n",
        text,
        flags=re.S,
    )
    # Remove orphan markers left by prior bad injections
    text = text.replace(SEO_MARKER_START, "")
    text = text.replace(SEO_MARKER_END, "")
    # Clear leftover SEO meta + JSON-LD that sat outside markers
    text = _strip_orphan_seo_artifacts(text)
    if 'name="description"' in text:
        return re.sub(
            r'(<meta\s+name="description"\s+content="[^"]*"\s*/>)',
            r"\1\n" + seo_block,
            text,
            count=1,
            flags=re.I,
        )
    return text.replace("</head>", seo_block + "\n</head>", 1)
