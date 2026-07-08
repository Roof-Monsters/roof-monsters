"""Shared SEO helpers for Roof Monsters static site."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data" / "site-seo.json"

ENCODING_FIXES = {
    "â€”": "—",
    "â€“": "–",
    "â€˜": "'",
    "â€™": "'",
    "â€œ": """,
    "â€\x9d": """,
    "â„¢": "™",
    "â€¦": "…",
    "Ã—": "×",
    "Â·": "·",
}

SEO_MARKER_START = "<!-- rm-seo:start -->"
SEO_MARKER_END = "<!-- rm-seo:end -->"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


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


def json_ld_block(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return f'  <script type="application/ld+json">\n{payload}\n  </script>'


def breadcrumb_schema(crumbs: list[dict[str, str]], page_url: str, base: str) -> dict | None:
    if len(crumbs) < 2:
        return None
    items = []
    for i, crumb in enumerate(crumbs, start=1):
        item: dict = {
            "@type": "ListItem",
            "position": i,
            "name": crumb["name"],
        }
        if crumb.get("url"):
            href = crumb["url"]
            if href.startswith("/"):
                item["item"] = urljoin(base.rstrip("/") + "/", href.lstrip("/"))
            elif href.startswith("http"):
                item["item"] = href
            elif href in ("./", "../", "..", ""):
                item["item"] = base.rstrip("/") + "/"
            else:
                item["item"] = urljoin(page_url, href)
        elif i == len(crumbs):
            item["item"] = page_url
        items.append(item)
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


def roofing_contractor_schema(config: dict) -> dict:
    b = config["business"]
    return {
        "@context": "https://schema.org",
        "@type": "RoofingContractor",
        "@id": f"{config['canonicalBase']}/#roofingcontractor",
        "name": b["name"],
        "legalName": b["legalName"],
        "url": config["canonicalBase"],
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
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": b["aggregateRating"]["ratingValue"],
            "reviewCount": b["aggregateRating"]["reviewCount"],
        },
    }


def local_business_schema(config: dict, area_name: str, page_url: str) -> dict:
    base = roofing_contractor_schema(config)
    base["@type"] = ["RoofingContractor", "LocalBusiness"]
    base["@id"] = f"{page_url}#localbusiness"
    base["url"] = page_url
    base["areaServed"] = [area_name, *config["business"]["areaServed"]]
    return base


def service_schema(config: dict, service: dict, page_url: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": f"{page_url}#service",
        "name": service["name"],
        "description": service["description"],
        "provider": {"@id": f"{config['canonicalBase']}/#roofingcontractor"},
        "areaServed": config["business"]["areaServed"],
        "url": page_url,
    }


def article_schema(config: dict, post: dict, page_url: str, title: str, description: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": description,
        "datePublished": post["datePublished"],
        "author": {
            "@type": "Organization",
            "name": config["business"]["name"],
        },
        "publisher": {
            "@type": "Organization",
            "name": config["business"]["name"],
            "logo": {
                "@type": "ImageObject",
                "url": config["business"]["logo"],
            },
        },
        "image": f"{config['canonicalBase']}/{post['image']}",
        "mainEntityOfPage": page_url,
        "url": page_url,
    }


def build_seo_head(path: Path, text: str, config: dict) -> str:
    page_url = page_path_to_url(path, config["canonicalBase"])
    title = extract_title(text)
    description = extract_description(text)
    og_image = og_image_for(path, config)
    page_type = classify_page(path)

    schemas: list[dict] = []
    if page_type in {"home", "contact"}:
        schemas.append(roofing_contractor_schema(config))
    if page_type == "service":
        slug = path.parent.name
        service = next((s for s in config["services"] if s["slug"] == slug), None)
        if service:
            schemas.append(service_schema(config, service, page_url))
    if page_type == "location":
        area_name = title.split("|")[0].replace("Roofing Company in", "").strip()
        schemas.append(local_business_schema(config, area_name, page_url))
    if page_type == "blog-post":
        slug = path.parent.name
        post = next((p for p in config["blogPosts"] if p["slug"] == slug), None)
        if post:
            schemas.append(article_schema(config, post, page_url, title, description))
    crumbs = extract_breadcrumbs(text)
    crumb_schema = breadcrumb_schema(crumbs, page_url, config["canonicalBase"])
    if crumb_schema:
        schemas.append(crumb_schema)

    schema_html = "\n".join(json_ld_block(s) for s in schemas)
    return f"""{SEO_MARKER_START}
  <link rel="canonical" href="{html.escape(page_url, quote=True)}" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />
  <meta property="og:type" content="{'website' if page_type == 'home' else 'article' if page_type == 'blog-post' else 'website'}" />
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


def inject_seo(text: str, seo_block: str) -> str:
    text = re.sub(
        rf"\s*{re.escape(SEO_MARKER_START)}.*?{re.escape(SEO_MARKER_END)}\s*",
        "\n",
        text,
        flags=re.S,
    )
    if 'name="description"' in text:
        return re.sub(
            r'(<meta\s+name="description"\s+content="[^"]*"\s*/>)',
            r"\1\n" + seo_block,
            text,
            count=1,
            flags=re.I,
        )
    return text.replace("</head>", seo_block + "\n</head>", 1)
