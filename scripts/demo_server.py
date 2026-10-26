"""A throwaway demo server for recording the video: the real live model and embeddings, an in-memory store, and one
demo customer account. Nothing here is saved; restarting the server clears it.

Run: MILO_LIVE=1 MILO_DEMO_PASSWORD=<pick one> uv run python scripts/demo_server.py   (listens on 127.0.0.1:5057)
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from milo.app import App
from milo.embed import OpenRouterEmbedder
from milo.llm import live_chat_model, local_chat_model
from milo.serve import load_documents
from milo.store import MemoryStore
from milo.tools import Backend
from milo.users import MemoryUserStore, hash_password
from milo.web import create_app


def main() -> None:
    password = os.environ.get("MILO_DEMO_PASSWORD")
    if not password:
        raise SystemExit(
            "set MILO_DEMO_PASSWORD (it is only for this throwaway server)"
        )
    if os.environ.get("MILO_LIVE") != "1":
        raise SystemExit("the recording needs the live model: MILO_LIVE=1")
    store = MemoryStore()
    app = App(
        live_chat_model(),
        OpenRouterEmbedder(max_cost_usd=0.05),
        Backend(store=store),
        fallback_chat=local_chat_model(),
        store=store,
    )
    app.ingest(load_documents())
    users = MemoryUserStore()
    users.create("demo", "Demo Owner", hash_password(password), "customer")
    create_app(app, secret_key=os.urandom(16).hex(), users=users).run(
        host="127.0.0.1", port=5057
    )


if __name__ == "__main__":
    main()
