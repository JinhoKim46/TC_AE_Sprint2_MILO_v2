"""`build_app` exists with the kit's interface. With nothing ingested, every question abstains without a model call."""

from __future__ import annotations

from milo.app import build_app
from milo.embed import LexicalEmbedder
from milo.types import ChatReply, Document, Response


class NoCallChat:
    price_usd_per_mtok = (0.0, 0.0)
    calls = 0

    def invoke(self, messages, tools=None):  # pragma: no cover - must not be called
        self.calls += 1
        raise AssertionError("an empty knowledge base makes no model call")


def test_build_app_has_the_kit_interface() -> None:
    chat = NoCallChat()
    app = build_app(chat, embeddings=LexicalEmbedder(), tools_backend=None)
    app.ingest([])
    r = app.ask("hello", user_id="u1", thread_id="t1")
    assert isinstance(r, Response)
    assert r.answer and r.sources == [] and r.tool_results == []
    assert r.cost_usd == 0.0 and r.error is None and r.stopped is False
    assert chat.calls == 0


class AnsweringChat:
    price_usd_per_mtok = (0.0, 0.0)

    def invoke(self, messages, tools=None):
        return ChatReply(content="On the first day of each month.")


def test_ingested_document_is_retrieved_by_a_quoted_question() -> None:
    chat = AnsweringChat()
    app = build_app(chat, embeddings=LexicalEmbedder(), tools_backend=None)
    app.ingest(
        [Document("kb/x", "Invoices are issued on the first day of each month.", {})]
    )
    r = app.ask("When are invoices issued each month?", user_id="u1", thread_id="t1")
    assert r.sources and r.sources[0].doc_id == "kb/x"
