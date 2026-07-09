"""Shared <head> bootstrap: GitHub Pages base path + favicon injection."""

from __future__ import annotations

BASE_HEAD_SCRIPT = """  <script>
(function () {
  var path = location.pathname;
  var marker = '/roof-monsters';
  var idx = path.indexOf(marker);
  var base = idx >= 0 ? path.slice(0, idx + marker.length) + '/' : '/';
  window.__RM_BASE__ = base;
  document.write(
    '<base href=\"' + base + '\">' +
    '<link rel=\"icon\" href=\"' + base + 'favicon.ico\" sizes=\"48x48\" />' +
    '<link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"' + base + 'assets/icons/favicon-32x32.png\" />' +
    '<link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"' + base + 'assets/icons/favicon-16x16.png\" />' +
    '<link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"' + base + 'assets/icons/apple-touch-icon.png\" />'
  );
})();
  </script>"""
