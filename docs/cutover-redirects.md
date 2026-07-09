# Host redirects for Roof Monsters cutover

Use these on the **production host** (not GitHub Pages) after DNS points at this rebuild.

## Do NOT redirect these to the homepage

WordPress system URLs from GSC (soft-404 risk if redirected home):

- `/wp-admin/*`
- `/wp-content/*`
- `/wp-includes/*`
- `/wp-json/*`
- `/*.php` (including `wp-*.php`, `xmlrpc.php`)

Keep them as **404** (or **410 Gone** if the host supports it). `robots.txt` already disallows them.

## Do redirect (301) real public pages

Map any old public WP slugs that differ from the new static paths, for example:

| Old (example) | New |
|---------------|-----|
| `/contact/` | `/contact-us/` |
| `/about/` | `/about-us/` |
| `/locations/` | `/about-us/locations-we-serve/` |

Add host-specific rules (Cloudflare, nginx, Apache, or Netlify `_redirects`) only for URLs that had real public content.

## Sitemap

Only `sitemap.xml` should be submitted in GSC. Do not submit WordPress or plugin sitemaps after cutover.
