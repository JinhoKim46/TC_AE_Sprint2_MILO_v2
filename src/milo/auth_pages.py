"""The sign-up, sign-in and user-list pages. Plain forms; the server checks everything."""

from __future__ import annotations

from html import escape

from milo.shell import FAVICON, SHELL_CSS, site_header

CSS = """
:root{--bg:#F5F4EF;--card:#FFFFFF;--line:#E2DFD6;--ink:#1F1E1B;--mut:#67645B;--accent:#2C6B5C;--accent-soft:#E6F0EC;--bad:#8A2F2F;--bad-soft:#F7E5E5}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.pagehead-unused{display:flex;align-items:center;gap:16px;flex-wrap:wrap;padding:14px 0;margin:0 -16px;padding-left:16px;padding-right:16px;background:var(--card);border-bottom:1px solid var(--line)}
header .sp{flex:1}
main{max-width:460px;margin:40px auto;display:flex;flex-direction:column;gap:14px}
main.wide{max-width:900px}
h1{font-size:26px;margin:0}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px}
label{display:block;font-size:14px;font-weight:600;margin:12px 0 4px}
input{width:100%;font:inherit;padding:11px 12px;border:1px solid var(--line);border-radius:10px;background:var(--bg);color:var(--ink)}
input:focus{outline:2px solid var(--accent);outline-offset:1px;border-color:var(--accent)}
.btn{font:inherit;padding:11px 18px;border-radius:12px;border:1px solid var(--accent);background:var(--accent);color:#fff;cursor:pointer;margin-top:16px;width:100%}
.muted{color:var(--mut);font-size:14px}
.error{background:var(--bad-soft);color:var(--bad);border-radius:10px;padding:10px 12px;font-size:14px;margin:0 0 6px}
table{width:100%;border-collapse:collapse;font-size:14px}
th,td{text-align:left;padding:9px 8px;border-bottom:1px solid var(--line)}
th{color:var(--mut);font-weight:600}
.pill{display:inline-block;font-size:12px;padding:2px 9px;border-radius:999px;background:var(--accent-soft);color:var(--accent)}
.notice{background:var(--accent-soft);color:var(--accent);border-radius:10px;padding:10px 12px;font-size:14px;margin:0 0 6px}
"""
SITE = """.sitenav a,.sitenav button{color:var(--mut)}"""


def _page(title: str, active: str, user, body: str) -> str:
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        f"<title>{escape(title)} · MILO</title>{FAVICON}"
        f"<style>{SHELL_CSS}{CSS}{SITE}</style></head><body>"
        f"{site_header(active, user)}"
        f"{body}</body></html>"
    )


def login_page(error: str = "", login_id: str = "", next_url: str = "/") -> str:
    err = f'<p class="error" role="alert">{escape(error)}</p>' if error else ""
    body = (
        '<main><div class="card"><h1>Log in</h1>'
        '<p class="muted">Sign in to start a conversation with MILO.</p>'
        f"{err}"
        '<form method="post" action="/login">'
        f'<input type="hidden" name="next" value="{escape(next_url)}">'
        '<label for="login_id">ID</label>'
        f'<input id="login_id" name="login_id" value="{escape(login_id)}" autocomplete="username" required>'
        '<label for="password">Password</label>'
        '<input id="password" name="password" type="password" autocomplete="current-password" required>'
        '<button class="btn" type="submit">Log in</button></form>'
        '<p class="muted" style="margin-top:14px">New here? <a href="/signup">Create an account</a>.</p>'
        "</div></main>"
    )
    return _page("Log in", "login", None, body)


def signup_page(error: str = "", name: str = "", login_id: str = "") -> str:
    err = f'<p class="error" role="alert">{escape(error)}</p>' if error else ""
    body = (
        '<main><div class="card"><h1>Create an account</h1>'
        '<p class="muted">Choose an ID and a password. You can then start a conversation right away.</p>'
        f"{err}"
        '<form method="post" action="/signup">'
        '<label for="name">Your name</label>'
        f'<input id="name" name="name" value="{escape(name)}" autocomplete="name" required maxlength="60">'
        '<label for="login_id">ID</label>'
        f'<input id="login_id" name="login_id" value="{escape(login_id)}" autocomplete="username" required maxlength="40">'
        '<label for="password">Password (at least 8 characters)</label>'
        '<input id="password" name="password" type="password" autocomplete="new-password" required minlength="8">'
        '<button class="btn" type="submit">Create account</button></form>'
        '<p class="muted" style="margin-top:14px">Already registered? <a href="/login">Log in</a>.</p>'
        "</div></main>"
    )
    return _page("Create an account", "signup", None, body)


def users_page(user, users) -> str:
    rows = "".join(
        f"<tr><td>{escape(u.display_name)}</td><td>{escape(u.login_id)}</td>"
        f'<td><span class="pill">{escape(u.role)}</span></td></tr>'
        for u in users
    )
    body = (
        '<main class="wide"><div class="card"><h1>Users</h1>'
        f'<p class="muted">{len(users)} registered. Passwords are stored only as hashes and are never shown.</p>'
        "<table><thead><tr><th>Name</th><th>ID</th><th>Role</th></tr></thead>"
        f"<tbody>{rows}</tbody></table></div></main>"
    )
    return _page("Users", "users", user, body)


def password_page(user, error: str = "", saved: bool = False) -> str:
    if saved:
        notice = '<p class="notice" role="status">Your password was changed. Use the new one next time you log in.</p>'
    else:
        notice = f'<p class="error" role="alert">{escape(error)}</p>' if error else ""
    body = (
        '<main><div class="card"><h1>Change password</h1>'
        '<p class="muted">Enter your current password, then the new one twice. The new password must be at least 8 characters.</p>'
        f"{notice}"
        '<form method="post" action="/account/password">'
        '<label for="current">Current password</label>'
        '<input id="current" name="current" type="password" autocomplete="current-password" required>'
        '<label for="new">New password</label>'
        '<input id="new" name="new" type="password" autocomplete="new-password" required minlength="8">'
        '<label for="again">Repeat the new password</label>'
        '<input id="again" name="again" type="password" autocomplete="new-password" required minlength="8">'
        '<button class="btn" type="submit">Change password</button></form>'
        "</div></main>"
    )
    return _page("Change password", "password", user, body)
