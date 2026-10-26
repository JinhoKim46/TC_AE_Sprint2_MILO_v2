"""Test helper: create an account in memory, sign in through the real /login form, and return the signed-in client."""

from __future__ import annotations

from milo.users import MemoryUserStore, hash_password
from milo.web import create_app

PASSWORD = "password-123"


def signed_in_app(
    milo_app, role: str = "customer", login_id: str = "u1", name: str = "Test Person"
):
    users = MemoryUserStore()
    users.create(login_id, name, hash_password(PASSWORD), role)
    web = create_app(milo_app, secret_key="test", users=users)
    client = web.test_client()
    client.post(
        "/login", data={"login_id": login_id, "password": PASSWORD, "next": "/chat"}
    )
    return web, client, users
