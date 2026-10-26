"""PostgreSQL implementation of the `Store` interface (schema `milo_v2`, see db/migrations/).

Every query filters by owner. One connection per store, autocommit, and a lock so the Flask threads share it safely.
"""

from __future__ import annotations

import json
import threading
from typing import Any

import psycopg

from milo.store import MAX_HISTORY_TURNS
from milo.users import User


class PostgresStore:
    def __init__(self, url: str) -> None:
        self._conn = psycopg.connect(url, autocommit=True)
        self._lock = threading.Lock()

    def close(self) -> None:
        self._conn.close()

    def user_store(self) -> PostgresUserStore:
        return PostgresUserStore(self._conn)

    def append_turns(
        self, owner: str, thread: str, turns: list[dict[str, str]]
    ) -> None:
        with self._lock, self._conn.cursor() as cur:
            cur.execute(
                "insert into milo_v2.threads (owner_id, thread_id) values (%s, %s) on conflict do nothing",
                (owner, thread),
            )
            cur.executemany(
                "insert into milo_v2.turns (owner_id, thread_id, role, content, sources) values (%s, %s, %s, %s, %s)",
                [
                    (
                        owner,
                        thread,
                        t["role"],
                        t["content"],
                        json.dumps(t.get("sources", [])),
                    )
                    for t in turns
                ],
            )

    def history(
        self, owner: str, thread: str, limit: int = MAX_HISTORY_TURNS
    ) -> list[dict[str, str]]:
        if limit <= 0:
            return []
        with self._lock, self._conn.cursor() as cur:
            cur.execute(
                "select role, content, sources from milo_v2.turns where owner_id = %s and thread_id = %s "
                "order by id desc limit %s",
                (owner, thread, limit),
            )
            rows = cur.fetchall()
        return [
            {"role": r, "content": c, "sources": src or []}
            for r, c, src in reversed(rows)
        ]

    def add_fact(self, owner: str, field_id: str, entry: dict[str, Any]) -> int:
        with self._lock, self._conn.cursor() as cur:
            cur.execute(
                "insert into milo_v2.facts (owner_id, field_id, value, unit, status, evidence_text) "
                "values (%s, %s, %s, %s, %s, %s)",
                (
                    owner,
                    field_id,
                    json.dumps(entry["value"]),
                    entry.get("unit"),
                    entry["status"],
                    entry["evidence_text"],
                ),
            )
            cur.execute(
                "select count(*) from milo_v2.facts where owner_id = %s and field_id = %s",
                (owner, field_id),
            )
            return int(cur.fetchone()[0])

    def facts(self, owner: str) -> dict[str, list[dict[str, Any]]]:
        with self._lock, self._conn.cursor() as cur:
            cur.execute(
                "select field_id, value, unit, status, evidence_text from milo_v2.facts "
                "where owner_id = %s order by id",
                (owner,),
            )
            rows = cur.fetchall()
        out: dict[str, list[dict[str, Any]]] = {}
        for field_id, value, unit, status, evidence in rows:
            out.setdefault(field_id, []).append(
                {
                    "value": value,
                    "unit": unit,
                    "status": status,
                    "evidence_text": evidence,
                }
            )
        return out

    def add_diagnosis(self, owner: str, card: dict[str, Any]) -> int:
        with self._lock, self._conn.cursor() as cur:
            cur.execute(
                "insert into milo_v2.diagnoses (owner_id, area_id, card) values (%s, %s, %s)",
                (owner, card["area_id"], json.dumps(card)),
            )
            cur.execute(
                "select count(*) from milo_v2.diagnoses where owner_id = %s", (owner,)
            )
            return int(cur.fetchone()[0])

    def diagnoses(self, owner: str) -> list[dict[str, Any]]:
        with self._lock, self._conn.cursor() as cur:
            cur.execute(
                "select card from milo_v2.diagnoses where owner_id = %s order by id",
                (owner,),
            )
            return [row[0] for row in cur.fetchall()]

    def delete_owner(self, owner: str) -> None:
        """Remove everything one owner has stored. Used by tests and by the owner-deletion request (not yet exposed)."""
        with self._lock, self._conn.cursor() as cur:
            for table in ("turns", "threads", "facts", "diagnoses"):
                cur.execute(
                    f"delete from milo_v2.{table} where owner_id = %s", (owner,)
                )


class PostgresUserStore:
    """Accounts in milo_v2.users. The same four methods as MemoryUserStore."""

    def __init__(self, conn: psycopg.Connection) -> None:
        self._conn = conn
        self._lock = threading.Lock()

    def create(
        self, login_id: str, display_name: str, password_hash: str, role: str
    ) -> User:
        with self._lock, self._conn.cursor() as cur:
            cur.execute(
                "insert into milo_v2.users (login_id, display_name, password_hash, role) values (%s, %s, %s, %s) returning id",
                (login_id, display_name, password_hash, role),
            )
            return User(cur.fetchone()[0], login_id, display_name, role)

    def by_login(self, login_id: str) -> tuple[User, str] | None:
        with self._lock, self._conn.cursor() as cur:
            cur.execute(
                "select id, display_name, role, password_hash from milo_v2.users where login_id = %s",
                (login_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return User(row[0], login_id, row[1], row[2]), row[3]

    def by_id(self, user_id: int) -> User | None:
        with self._lock, self._conn.cursor() as cur:
            cur.execute(
                "select login_id, display_name, role from milo_v2.users where id = %s",
                (user_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return User(user_id, row[0], row[1], row[2])

    def all(self) -> list[User]:
        with self._lock, self._conn.cursor() as cur:
            cur.execute(
                "select id, login_id, display_name, role from milo_v2.users order by id"
            )
            return [User(r[0], r[1], r[2], r[3]) for r in cur.fetchall()]
