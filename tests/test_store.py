"""The storage interface: owners never see each other's data, history is capped, and the app and tools use the store."""

from __future__ import annotations

from milo.app import build_app
from milo.embed import LexicalEmbedder
from milo.store import MAX_HISTORY_TURNS, MemoryStore
from milo.tools import Backend
from milo.types import ChatReply, Document, ToolCall


def test_owners_and_threads_are_separate() -> None:
    s = MemoryStore()
    s.append_turns("u1", "t1", [{"role": "user", "content": "a"}])
    assert s.history("u2", "t1") == []
    assert s.history("u1", "t2") == []
    assert s.history("u1", "t1") == [{"role": "user", "content": "a"}]


def test_history_sent_to_the_model_is_capped_but_kept() -> None:
    s = MemoryStore()
    turns = [{"role": "user", "content": str(i)} for i in range(MAX_HISTORY_TURNS + 6)]
    s.append_turns("u1", "t1", turns)
    assert len(s.history("u1", "t1")) == MAX_HISTORY_TURNS
    assert s.history("u1", "t1")[-1] == turns[-1]


def test_facts_and_diagnoses_are_per_owner() -> None:
    s = MemoryStore()
    assert s.add_fact("u1", "requests_per_week", {"value": 5}) == 1
    assert s.facts("u2") == {}
    assert s.add_diagnosis("u1", {"area_id": "request-dispatch"}) == 1
    assert s.diagnoses("u2") == []


class Answer:
    price_usd_per_mtok = (0.0, 0.0)

    def invoke(self, messages, tools=None):
        return ChatReply(content="ok")


def test_the_app_keeps_its_history_in_the_injected_store() -> None:
    store = MemoryStore()
    app = build_app(Answer(), LexicalEmbedder(), Backend(store=store))
    app.store = store
    app.ingest(
        [Document("kb/x", "Invoices are issued on the first day of each month.", {})]
    )
    app.ask("When are invoices issued each month?", "u1", "t1")
    assert [t["role"] for t in store.history("u1", "t1")] == ["user", "assistant"]


class RecordFact:
    price_usd_per_mtok = (0.0, 0.0)

    def __init__(self) -> None:
        self.calls = 0

    def invoke(self, messages, tools=None):
        self.calls += 1
        if self.calls == 1:
            return ChatReply(
                tool_calls=[
                    ToolCall(
                        "c1",
                        "record_fact",
                        {
                            "field_id": "requests_per_week",
                            "value": 40,
                            "status": "reported",
                            "evidence_text": "about 40",
                        },
                    )
                ]
            )
        return ChatReply(content="recorded")


def test_tool_facts_land_in_the_store_per_owner() -> None:
    store = MemoryStore()
    app = build_app(RecordFact(), LexicalEmbedder(), Backend(store=store))
    app.ingest([Document("kb/x", "Requests come in by phone.", {})])
    app.ask("We get about 40 requests a week.", "u1", "t1")
    assert "requests_per_week" in store.facts("u1")
    assert store.facts("u2") == {}
