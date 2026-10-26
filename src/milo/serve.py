"""Start the chat page. Choices come from the environment:

- MILO_STORE=postgres (needs MILO_DATABASE_URL) or memory (the default)
- MILO_LIVE=1 with OPENROUTER_API_KEY: the chosen model and embeddings. Without it, the offline lexical embedder and a
  model that answers nothing are used, so the page still starts and says so.
- The local Ollama model is the fallback when the primary fails.

Run:  MILO_LIVE=1 uv run python -m milo.serve
"""

from __future__ import annotations

import os
from pathlib import Path

from milo.app import App
from milo.chunk import front_matter
from milo.embed import LexicalEmbedder, OpenRouterEmbedder
from milo.llm import live_chat_model, local_chat_model
from milo.store import MemoryStore
from milo.tools import Backend
from milo.types import Document
from milo.web import create_app

ROOT = Path(__file__).resolve().parents[2]
KB = ROOT / "data" / "kb"
TRACE = ROOT / "logs" / "trace.jsonl"


def load_documents() -> list[Document]:
    docs = []
    for p in sorted(KB.rglob("*.md")):
        meta, body = front_matter(p.read_text())
        docs.append(Document(p.relative_to(KB).with_suffix("").as_posix(), body, meta))
    return docs


def build_store():
    if os.environ.get("MILO_STORE", "memory") == "postgres":
        from milo.pgstore import PostgresStore

        return PostgresStore(os.environ["MILO_DATABASE_URL"])
    return MemoryStore()


def build_web(secret_key: str | None = None):
    live = os.environ.get("MILO_LIVE") == "1" and bool(
        os.environ.get("OPENROUTER_API_KEY")
    )
    store = build_store()
    embeddings = OpenRouterEmbedder(max_cost_usd=0.05) if live else LexicalEmbedder()
    chat = live_chat_model() if live else local_chat_model()
    milo = App(
        chat,
        embeddings,
        Backend(store=store),
        fallback_chat=local_chat_model(),
        trace_path=TRACE,
        store=store,
    )
    milo.ingest(load_documents())
    return create_app(milo, secret_key=secret_key)


if __name__ == "__main__":
    build_web().run(host="127.0.0.1", port=5000)
