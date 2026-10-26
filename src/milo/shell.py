"""Shared pieces for every MILO page: the brand mark, the navigation that depends on who is signed in, and styles.

Visitors see the product page, sign-up and sign-in. Customers also see the chat and the knowledge base. The owner (admin)
also sees the overview and the user list. The overview is never shown to customers.
"""

from __future__ import annotations

from html import escape
from typing import Any

SHELL_CSS = """
.brandbar{display:flex;align-items:center;gap:10px;text-decoration:none;color:inherit;font-weight:700;letter-spacing:.02em}
.brandbar img{width:32px;height:32px;display:block}
.brandbar small{display:block;font-weight:400;color:var(--mut);font-size:12px;letter-spacing:0}
.sitenav{display:flex;gap:4px;flex-wrap:wrap;align-items:center}
.sitenav a,.sitenav button{color:var(--mut);text-decoration:none;font:inherit;font-size:14px;padding:6px 10px;border-radius:8px;background:none;border:0;cursor:pointer}
.sitenav a:hover,.sitenav button:hover{color:var(--ink);background:var(--bg)}
.sitenav a[aria-current="page"]{color:var(--accent);font-weight:600}
.sitenav .who{color:var(--ink);font-size:14px;padding:6px 10px}
"""


def nav_html(active: str, user: Any = None) -> str:
    links = [("home", "/", "Product")]
    if user is None:
        links += [("login", "/login", "Log in")]
    else:
        links += [("chat", "/chat", "Chat"), ("kb", "/kb", "Knowledge base")]
        if user.role == "admin":
            links += [
                ("overview", "/dashboard", "Overview"),
                ("users", "/admin/users", "Users"),
            ]
    parts = []
    for key, href, label in links:
        current = ' aria-current="page"' if key == active else ""
        parts.append(f'<a href="{href}"{current}>{escape(label)}</a>')
    if user is None:
        parts.append('<a href="/signup">Sign up</a>')
    else:
        parts.append(f'<span class="who">{escape(user.display_name)}</span>')
        parts.append(
            '<form method="post" action="/logout" style="margin:0">'
            '<button type="submit">Log out</button></form>'
        )
    return '<nav class="sitenav" aria-label="Main">' + "".join(parts) + "</nav>"


def brand_html(href: str = "/") -> str:
    return (
        f'<a class="brandbar" href="{href}"><img src="/static/milo-mark.svg" alt="" width="32" height="32">'
        "<span>MILO<small>Diagnosis assistant</small></span></a>"
    )


FAVICON = '<link rel="icon" type="image/svg+xml" href="/static/milo-mark.svg">'
