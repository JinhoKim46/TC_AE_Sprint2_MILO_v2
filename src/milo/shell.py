"""The one header every MILO page uses, and the brand mark.

Same structure everywhere: brand on the left; the links for the viewer in the middle; the account on the right.
Visitors: Product, Chat, Knowledge base; then Log in and Sign up.
Customers: the same links; the account menu holds Change password and Log out.
The owner also gets Overview and Users, which only the owner can open.
"""

from __future__ import annotations

from html import escape
from typing import Any

FAVICON = '<link rel="icon" type="image/svg+xml" href="/static/milo-mark.svg">'

SHELL_CSS = """
.sitehead{height:56px;display:flex;align-items:center;gap:24px;padding:0 20px;background:var(--card,#fff);border-bottom:1px solid var(--line,#e2dfd6);position:relative;z-index:20}
.sitehead .brandbar{display:flex;align-items:center;gap:10px;text-decoration:none;color:inherit;font-weight:700;letter-spacing:.02em;flex:0 0 auto}
.sitehead .brandbar img{width:30px;height:30px;display:block}
.sitehead .brandbar small{display:block;font-weight:400;color:var(--mut,#67645b);font-size:11px;letter-spacing:0;line-height:1.2}
.sitehead .links{display:flex;gap:4px;align-items:center;flex:1;min-width:0;overflow:hidden}
.sitehead .links a{color:var(--mut,#67645b);text-decoration:none;font-size:14px;padding:7px 10px;border-radius:8px;white-space:nowrap}
.sitehead .links a:hover{color:var(--ink,#1f1e1b);background:var(--bg,#f5f4ef)}
.sitehead .links a[aria-current="page"]{color:var(--accent,#2c6b5c);font-weight:600}
.sitehead .account{display:flex;gap:8px;align-items:center;flex:0 0 auto}
.sitehead .account a{color:var(--mut,#67645b);text-decoration:none;font-size:14px;padding:7px 10px;border-radius:8px}
.sitehead .account a.signup{background:var(--accent,#2c6b5c);color:#fff;font-weight:600}
.sitehead details{position:relative}
.sitehead summary{list-style:none;cursor:pointer;font-size:14px;padding:7px 12px;border-radius:999px;border:1px solid var(--line,#e2dfd6);color:var(--ink,#1f1e1b);white-space:nowrap}
.sitehead summary::-webkit-details-marker{display:none}
.sitehead .menu{position:absolute;right:0;top:calc(100% + 8px);background:var(--card,#fff);border:1px solid var(--line,#e2dfd6);border-radius:12px;padding:6px;min-width:190px;box-shadow:0 10px 28px rgba(31,30,27,.10);display:flex;flex-direction:column}
.sitehead .menu a,.sitehead .menu button{font:inherit;font-size:14px;text-align:left;background:none;border:0;padding:9px 12px;border-radius:8px;color:var(--ink,#1f1e1b);text-decoration:none;cursor:pointer;width:100%}
.sitehead .menu a:hover,.sitehead .menu button:hover{background:var(--bg,#f5f4ef)}
.sitehead .menu form{margin:0}
@media (max-width:760px){.sitehead{gap:10px;padding:0 12px}.sitehead .links{overflow-x:auto;white-space:nowrap;min-width:0}.sitehead .links a{padding:6px 7px;font-size:13px}.sitehead .brandbar small{display:none}}
"""


def _link(href: str, label: str, active: str, key: str) -> str:
    current = ' aria-current="page"' if key == active else ""
    return f'<a href="{href}"{current}>{escape(label)}</a>'


def site_header(active: str, user: Any = None) -> str:
    links = [
        _link("/", "Product", active, "home"),
        _link("/chat", "Chat", active, "chat"),
        _link("/kb", "Knowledge base", active, "kb"),
    ]
    if user is not None and user.role == "admin":
        links += [
            _link("/dashboard", "Overview", active, "overview"),
            _link("/admin/users", "Users", active, "users"),
        ]
    if user is None:
        account = (
            '<a href="/login">Log in</a><a class="signup" href="/signup">Sign up</a>'
        )
    else:
        account = (
            "<details><summary>" + escape(user.display_name) + "</summary>"
            '<div class="menu"><a href="/account/password">Change password</a>'
            '<form method="post" action="/logout"><button type="submit">Log out</button></form></div></details>'
        )
    return (
        '<header class="sitehead">'
        '<a class="brandbar" href="/"><img src="/static/milo-mark.svg" alt="" width="30" height="30">'
        "<span>MILO<small>Diagnosis assistant</small></span></a>"
        '<nav class="links" aria-label="Main">' + "".join(links) + "</nav>"
        f'<div class="account">{account}</div>'
        "</header>"
    )
