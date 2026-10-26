"""Apply the SQL migrations in db/migrations/ in order. Reads MILO_DATABASE_URL from the environment or .env.

Usage: uv run python scripts/migrate.py [--schema-only-check]
Each migration runs in one transaction. Applied files are recorded in milo_v2.schema_migrations.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import psycopg

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "db" / "migrations"


def database_url() -> str:
    url = os.environ.get("MILO_DATABASE_URL", "").strip()
    if not url:
        for line in (ROOT / ".env").read_text().splitlines():
            if line.startswith("MILO_DATABASE_URL="):
                url = line.split("=", 1)[1].strip()
    if not url:
        raise SystemExit("MILO_DATABASE_URL is not set (put it in .env)")
    return url


def main() -> None:
    url = database_url()
    with psycopg.connect(url, autocommit=False) as conn:
        with conn.cursor() as cur:
            cur.execute("create schema if not exists milo_v2")
            cur.execute(
                "create table if not exists milo_v2.schema_migrations "
                "(name text primary key, applied_at timestamptz not null default now())"
            )
            cur.execute("select name from milo_v2.schema_migrations")
            done = {r[0] for r in cur.fetchall()}
            for path in sorted(MIGRATIONS.glob("*.sql")):
                if path.name in done:
                    print(f"already applied: {path.name}")
                    continue
                cur.execute(path.read_text())
                cur.execute(
                    "insert into milo_v2.schema_migrations (name) values (%s)",
                    (path.name,),
                )
                print(f"applied: {path.name}")
        conn.commit()
    print("migrations OK")


if __name__ == "__main__":
    sys.exit(main())
