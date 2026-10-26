"""Set a new password for an account from the terminal. For the owner, when the password is forgotten.

Usage: MILO_DATABASE_URL=... uv run python scripts/reset_password.py --login-id <id>
The new password is typed at a hidden prompt. Nothing is printed or written except the confirmation line.
"""

from __future__ import annotations

import argparse
import getpass
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from milo.pgstore import PostgresStore
from milo.users import check_new_account, hash_password


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--login-id", required=True)
    args = ap.parse_args()
    url = os.environ.get("MILO_DATABASE_URL", "").strip()
    if not url:
        raise SystemExit("MILO_DATABASE_URL is not set")
    password = getpass.getpass("New password (hidden): ")
    confirm = getpass.getpass("Repeat the new password: ")
    if password != confirm:
        raise SystemExit("The two passwords do not match.")
    problem = check_new_account(args.login_id, "reset", password)
    if problem:
        raise SystemExit(problem)
    store = PostgresStore(url)
    users = store.user_store()
    found = users.by_login(args.login_id)
    if found is None:
        store.close()
        raise SystemExit("No account with that ID.")
    users.set_password(found[0].id, hash_password(password))
    store.close()
    print(f"Password changed for {args.login_id}.")


if __name__ == "__main__":
    main()
