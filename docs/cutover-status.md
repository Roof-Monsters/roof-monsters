# Roof Monsters cutover status

Last verified: 2026-07-21

The GitHub Pages rebuild is prepared for `roofmonsters.co`, and this repository's root `CNAME` declares that domain. Production is **not cut over yet**: the public homepage still serves the legacy WordPress/JLG site.

Until the maintenance cutover is approved and completed:

- Treat `docs/post-cutover-checklist.md` as pending.
- Do not submit the rebuild sitemap or remove the legacy sitemap in Google Search Console.
- Do not change DNS, GitHub Pages domain settings, Formspree allowed origins, or production email routing as part of automated testing.
- Preserve the legacy production host as the rollback source.

After cutover, verify the homepage and `www` host, HTTPS, one non-billable form delivery, email-agent continuity, sitemap availability, and priority pages before marking the checklist complete.
