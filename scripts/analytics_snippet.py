"""Microsoft Clarity and other sitewide analytics snippets."""

from __future__ import annotations

import re

ANALYTICS_MARKER_START = "<!-- rm-analytics:start -->"
ANALYTICS_MARKER_END = "<!-- rm-analytics:end -->"

CLARITY_PROJECT_ID = "xk3zwtme0b"

ANALYTICS_HEAD_HTML = f"""{ANALYTICS_MARKER_START}
  <!-- Clarity tracking code for https://roofmonsters.co/ -->
  <script>
    (function(c,l,a,r,i,t,y){{
        c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i+"?ref=bwt";
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "{CLARITY_PROJECT_ID}");
  </script>
{ANALYTICS_MARKER_END}"""


def inject_analytics(text: str) -> str:
    """Insert or refresh the analytics block immediately before </head>."""
    text = re.sub(
        rf"\s*{re.escape(ANALYTICS_MARKER_START)}.*?{re.escape(ANALYTICS_MARKER_END)}\s*",
        "\n",
        text,
        flags=re.S,
    )
    if "</head>" not in text:
        return text
    return text.replace("</head>", ANALYTICS_HEAD_HTML + "\n</head>", 1)
