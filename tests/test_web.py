"""M6: the chat page and its JSON endpoint, through Flask's test client. Offline; the model is a fake."""

from __future__ import annotations

import json

from milo.app import build_app
from milo.embed import LexicalEmbedder
from milo.store import MemoryStore
from milo.tools import Backend
from milo.types import ChatReply, Document, ToolCall, Usage
from milo.web import create_app


class ToolThenAnswer:
    price_usd_per_mtok = (1.0, 1.0)

    def __init__(self, tool_name: str | None = None, args: dict | None = None) -> None:
        self.tool_name = tool_name
        self.args = args or {}
        self.calls = 0

    def invoke(self, messages, tools=None):
        self.calls += 1
        if self.tool_name and self.calls == 1:
            return ChatReply(
                tool_calls=[ToolCall("c1", self.tool_name, self.args)],
                usage=Usage(100, 50),
            )
        return ChatReply(
            content="Invoices are issued on the first day of each month [1].",
            usage=Usage(100, 50),
        )


def client(chat):
    milo = build_app(chat, LexicalEmbedder(), Backend())
    milo.ingest(
        [
            Document(
                "kb/billing", "Invoices are issued on the first day of each month.", {}
            )
        ]
    )
    return create_app(milo, secret_key="test").test_client()


def test_page_has_the_chat_composer_and_plain_language_panels() -> None:
    page = client(ToolThenAnswer()).get("/chat").get_data(as_text=True)
    for needle in (
        "New conversation",
        "How MILO works",
        "Session cost",
        'aria-live="polite"',
        "/api/ask",
        "/api/history",
        "Show technical details",
        "MILO is reading your question",
    ):
        assert needle in page, needle


def test_history_returns_the_stored_turns_for_this_browser() -> None:
    c = client(ToolThenAnswer())
    c.get("/chat")
    c.post("/api/ask", json={"question": "When are invoices issued each month?"})
    turns = c.get("/api/history").get_json()["turns"]
    assert [t["role"] for t in turns] == ["user", "assistant"]


def test_new_conversation_starts_an_empty_thread() -> None:
    c = client(ToolThenAnswer())
    c.get("/chat")
    c.post("/api/ask", json={"question": "When are invoices issued each month?"})
    c.get("/chat?new=1")
    assert c.get("/api/history").get_json()["turns"] == []


def test_answer_comes_back_with_sources_and_cost() -> None:
    c = client(ToolThenAnswer())
    body = c.post(
        "/api/ask", json={"question": "When are invoices issued each month?"}
    ).get_json()
    assert body["answer"].startswith("Invoices")
    assert body["sources"] and body["sources"][0]["doc_id"] == "kb/billing"
    assert body["cost_usd"] > 0 and body["error"] is None


def test_a_destructive_tool_call_shows_its_policy_decision_and_stops() -> None:
    c = client(ToolThenAnswer("reset_diagnosis", {"diagnosis_id": 1}))
    body = c.post(
        "/api/ask", json={"question": "When are invoices issued each month?"}
    ).get_json()
    assert body["stopped"] is True
    assert body["tool_results"][0]["policy_decision"] == "needs_approval"


def test_bad_input_is_a_typed_error_not_a_traceback() -> None:
    resp = client(ToolThenAnswer()).post("/api/ask", json={"question": ""})
    body = resp.get_json()
    assert body["error"].startswith("invalid_input")
    assert "Traceback" not in str(body)


def test_owner_comes_from_the_session_not_the_request() -> None:
    chat = ToolThenAnswer()
    milo = build_app(chat, LexicalEmbedder(), Backend())
    milo.ingest(
        [
            Document(
                "kb/billing", "Invoices are issued on the first day of each month.", {}
            )
        ]
    )
    web = create_app(milo, secret_key="test")
    seen: list[str] = []
    original = milo.ask

    def spy(question, user_id, thread_id):
        seen.append(user_id)
        return original(question, user_id, thread_id)

    milo.ask = spy
    a = web.test_client()
    b = web.test_client()
    a.get("/chat")
    b.get("/chat")
    a.post(
        "/api/ask",
        json={
            "question": "When are invoices issued each month?",
            "user_id": "someone-else",
        },
    )
    b.post("/api/ask", json={"question": "When are invoices issued each month?"})
    assert seen[0] != seen[1] and "someone-else" not in seen


def test_feedback_stores_rating_and_reason_with_a_hashed_owner(tmp_path) -> None:

    store = MemoryStore()
    milo = build_app(ToolThenAnswer(), LexicalEmbedder(), Backend(store=store))
    milo.store = store
    milo.trace_path = tmp_path / "trace.jsonl"
    web = create_app(milo, secret_key="test")
    c = web.test_client()
    c.get("/chat")
    ok = c.post("/api/feedback", json={"rating": "down", "reason": "missing_source"})
    assert ok.get_json()["ok"] is True
    bad_rating = c.post("/api/feedback", json={"rating": "maybe"})
    assert bad_rating.status_code == 400
    bad_reason = c.post("/api/feedback", json={"rating": "down", "reason": "free text"})
    assert bad_reason.status_code == 400
    lines = (tmp_path / "feedback.jsonl").read_text().splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["rating"] == "down" and record["reason"] == "missing_source"
    assert "free text" not in lines[0]
    assert record["owner"] != "" and len(record["owner"]) == 12
