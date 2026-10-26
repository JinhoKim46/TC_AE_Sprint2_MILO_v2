"""Accounts: sign-up, sign-in, changing the password, and the owner-only pages. Offline."""

from __future__ import annotations

from _auth import PASSWORD, signed_in_app

from milo.app import build_app
from milo.embed import LexicalEmbedder
from milo.tools import Backend
from milo.types import ChatReply


class Quiet:
    price_usd_per_mtok = (0.0, 0.0)

    def invoke(self, messages, tools=None):
        return ChatReply(content="ok")


def fresh_app():
    return build_app(Quiet(), LexicalEmbedder(), Backend())


def test_password_change_needs_the_current_password() -> None:
    _, c, users = signed_in_app(fresh_app())
    bad = c.post(
        "/account/password",
        data={
            "current": "wrong-password",
            "new": "new-password-1",
            "again": "new-password-1",
        },
    )
    assert "not correct" in bad.get_data(as_text=True)
    assert (
        c.post("/login", data={"login_id": "u1", "password": PASSWORD}).status_code
        == 302
    )  # old password still works
    assert "new-password-1" not in users.by_login("u1")[1]  # only a hash is stored


def test_changed_password_works_at_the_next_sign_in_and_the_old_one_does_not() -> None:
    web, c, _ = signed_in_app(fresh_app())
    ok = c.post(
        "/account/password",
        data={"current": PASSWORD, "new": "new-password-1", "again": "new-password-1"},
    )
    assert "was changed" in ok.get_data(as_text=True)
    fresh = web.test_client()
    old = fresh.post("/login", data={"login_id": "u1", "password": PASSWORD})
    assert "not correct" in old.get_data(as_text=True)
    new = fresh.post("/login", data={"login_id": "u1", "password": "new-password-1"})
    assert new.status_code == 302


def test_mismatch_and_short_passwords_are_refused() -> None:
    _, c, _ = signed_in_app(fresh_app())
    mismatch = c.post(
        "/account/password",
        data={"current": PASSWORD, "new": "abcdefgh1", "again": "abcdefgh2"},
    )
    assert "do not match" in mismatch.get_data(as_text=True)
    short = c.post(
        "/account/password",
        data={"current": PASSWORD, "new": "short", "again": "short"},
    )
    assert "at least 8" in short.get_data(as_text=True)


def test_visitors_are_sent_to_sign_in_and_customers_cannot_open_the_owner_pages() -> (
    None
):
    web, c, _ = signed_in_app(fresh_app())
    anonymous = web.test_client()
    assert anonymous.get("/chat").status_code == 302
    assert anonymous.get("/account/password").status_code == 302
    assert c.get("/dashboard").status_code == 403
    assert c.get("/admin/users").status_code == 403
    assert c.get("/api/status").status_code == 403
