"""Shared favicon / PWA icon <head> markup for Roof Monsters pages."""

from __future__ import annotations

ICON_MARKER_START = "<!-- rm-icons:start -->"
ICON_MARKER_END = "<!-- rm-icons:end -->"


def icon_head_html() -> str:
    return f"""{ICON_MARKER_START}
  <link rel="icon" href="/favicon.ico" sizes="48x48" />
  <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg" />
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/icons/favicon-16x16.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png" />
  <link rel="apple-touch-icon" sizes="167x167" href="/assets/icons/apple-touch-icon-167x167.png" />
  <link rel="apple-touch-icon" sizes="152x152" href="/assets/icons/apple-touch-icon-152x152.png" />
  <link rel="apple-touch-icon" sizes="144x144" href="/assets/icons/apple-touch-icon-144x144.png" />
  <link rel="apple-touch-icon" sizes="120x120" href="/assets/icons/apple-touch-icon-120x120.png" />
  <link rel="apple-touch-icon" sizes="76x76" href="/assets/icons/apple-touch-icon-76x76.png" />
  <link rel="apple-touch-icon" sizes="57x57" href="/assets/icons/apple-touch-icon-57x57.png" />
  <link rel="mask-icon" href="/assets/icons/safari-pinned-tab.svg" color="#c9a227" />
  <link rel="manifest" href="/assets/icons/site.webmanifest" />
  <meta name="theme-color" content="#1a1a1a" />
  <meta name="msapplication-TileColor" content="#1a1a1a" />
  <meta name="msapplication-config" content="/assets/icons/browserconfig.xml" />
{ICON_MARKER_END}"""
