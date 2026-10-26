"""Shared pieces for every MILO page: the brand mark, the navigation and the common styles."""

from __future__ import annotations

from html import escape

NAV = (
    ("home", "/", "Product"),
    ("chat", "/chat", "Chat"),
    ("overview", "/dashboard", "Overview"),
    ("kb", "/kb", "Knowledge base"),
)

SHELL_CSS = """
.brandbar{display:flex;align-items:center;gap:10px;text-decoration:none;color:inherit;font-weight:700;letter-spacing:.02em}
.brandbar img{width:32px;height:32px;display:block}
.brandbar small{display:block;font-weight:400;color:var(--mut);font-size:12px;letter-spacing:0}
.sitenav{display:flex;gap:4px;flex-wrap:wrap}
.sitenav a{color:var(--mut);text-decoration:none;font-size:14px;padding:6px 10px;border-radius:8px}
.sitenav a:hover{color:var(--ink);background:var(--bg)}
.sitenav a[aria-current="page"]{color:var(--accent);font-weight:600}
"""


def nav_html(active: str) -> str:
    links = "".join(
        f'<a href="{href}"'
        + (' aria-current="page"' if key == active else "")
        + f">{escape(label)}</a>"
        for key, href, label in NAV
    )
    return '<nav class="sitenav" aria-label="Main">' + links + "</nav>"


def brand_html(href: str = "/") -> str:
    return (
        f'<a class="brandbar" href="{href}"><img src="/static/milo-mark.svg" alt="" width="32" height="32">'
        "<span>MILO<small>Diagnosis assistant</small></span></a>"
    )


FAVICON = '<link rel="icon" type="image/svg+xml" href="/static/milo-mark.svg">'
