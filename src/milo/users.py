"""Accounts: password hashing and the user store (memory for tests and demos; PostgreSQL in the database store).

Passwords are hashed with scrypt and a random salt. A stored hash never leaves this module, and the plain password is
never logged or returned anywhere.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from dataclasses import dataclass
from typing import Protocol

ROLES = ("admin", "customer")
N, R, P = 2**14, 8, 1  # scrypt cost parameters
MIN_PASSWORD = 8


@dataclass(frozen=True)
class User:
    id: int
    login_id: str
    display_name: str
    role: str


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=N, r=R, p=P, dklen=32)
    return f"scrypt${N}${R}${P}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        _, n, r, p, salt_hex, digest_hex = stored.split("$")
        digest = hashlib.scrypt(
            password.encode(),
            salt=bytes.fromhex(salt_hex),
            n=int(n),
            r=int(r),
            p=int(p),
            dklen=32,
        )
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(digest.hex(), digest_hex)


def check_new_account(login_id: str, display_name: str, password: str) -> str | None:
    """A message describing the first problem with a sign-up, or None when it is acceptable."""
    if (
        not login_id
        or len(login_id) > 40
        or not login_id.replace("-", "").replace("_", "").replace(".", "").isalnum()
    ):
        return "The ID may use letters, digits, dot, dash and underscore (up to 40 characters)."
    if not display_name or len(display_name) > 60:
        return "Please enter your name (up to 60 characters)."
    if len(password) < MIN_PASSWORD:
        return f"The password must be at least {MIN_PASSWORD} characters."
    return None


class UserStore(Protocol):
    def create(
        self, login_id: str, display_name: str, password_hash: str, role: str
    ) -> User: ...

    def by_login(self, login_id: str) -> tuple[User, str] | None: ...

    def by_id(self, user_id: int) -> User | None: ...

    def all(self) -> list[User]: ...


class MemoryUserStore:
    def __init__(self) -> None:
        self._rows: dict[str, tuple[User, str]] = {}
        self._next = 1

    def create(
        self, login_id: str, display_name: str, password_hash: str, role: str
    ) -> User:
        if login_id in self._rows:
            raise ValueError("login_id already exists")
        user = User(self._next, login_id, display_name, role)
        self._next += 1
        self._rows[login_id] = (user, password_hash)
        return user

    def by_login(self, login_id: str) -> tuple[User, str] | None:
        return self._rows.get(login_id)

    def by_id(self, user_id: int) -> User | None:
        for user, _ in self._rows.values():
            if user.id == user_id:
                return user
        return None

    def all(self) -> list[User]:
        return [u for u, _ in self._rows.values()]
