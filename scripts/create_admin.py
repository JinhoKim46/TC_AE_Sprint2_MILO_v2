"""Create the owner's account (role admin). Run once, from the terminal, with the database URL in the environment.

Usage: MILO_DATABASE_URL=... uv run python scripts/create_admin.py --login-id <id> --name "<your name>"
The password is typed at a hidden prompt. It is never written to a file, a log or the command line.
"""

from __future__ import annotations

import argparse
import getpass
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from milo.pgstore import PostgresStore
from milo.users import MIN_PASSWORD, check_new_account, hash_password


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--login-id", required=True)
    ap.add_argument("--name", required=True)
    args = ap.parse_args()
    url = os.environ.get("MILO_DATABASE_URL", "").strip()
    if not url:
        raise SystemExit("MILO_DATABASE_URL is not set")
    password = getpass.getpass("Password (hidden): ")
    confirm = getpass.getpass("Repeat the password: ")
    if password != confirm:
        raise SystemExit("The two passwords do not match.")
    problem = check_new_account(args.login_id, args.name, password)
    if problem:
        raise SystemExit(problem)
    store = PostgresStore(url)
    users = store.user_store()
    if users.by_login(args.login_id) is not None:
        raise SystemExit("That ID already exists.")
    user = users.create(args.login_id, args.name, hash_password(password), "admin")
    store.close()
    print(
        f"Owner account created for {user.display_name} (ID {user.login_id}). Minimum password length: {MIN_PASSWORD}."
    )


if __name__ == "__main__":
    main()
