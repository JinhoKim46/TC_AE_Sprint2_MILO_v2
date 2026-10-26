"""M6: the chat page and its JSON endpoint, through Flask's test client. Offline; the model is a fake."""

from __future__ import annotations

from _auth import signed_in_app

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
    return signed_in_app(milo)[1]


def test_page_has_the_chat_composer_and_plain_language_panels() -> None:
    page = client(ToolThenAnswer()).get("/chat").get_data(as_text=True)
    for needle in (
        "New conversation",
        "Sources and steps",
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


def test_owner_comes_from_the_signed_in_account_not_the_request() -> None:
    from milo.users import MemoryUserStore, hash_password

    chat = ToolThenAnswer()
    milo = build_app(chat, LexicalEmbedder(), Backend())
    milo.ingest(
        [
            Document(
                "kb/billing", "Invoices are issued on the first day of each month.", {}
            )
        ]
    )
    users = MemoryUserStore()
    users.create("ann", "Ann", hash_password("password-123"), "customer")
    users.create("ben", "Ben", hash_password("password-456"), "customer")
    web = create_app(milo, secret_key="test", users=users)
    seen: list[str] = []
    original = milo.ask

    def spy(question, user_id, thread_id):
        seen.append(user_id)
        return original(question, user_id, thread_id)

    milo.ask = spy
    a = web.test_client()
    b = web.test_client()
    a.post("/login", data={"login_id": "ann", "password": "password-123"})
    b.post("/login", data={"login_id": "ben", "password": "password-456"})
    a.post(
        "/api/ask",
        json={
            "question": "When are invoices issued each month?",
            "user_id": "someone-else",
        },
    )
    b.post("/api/ask", json={"question": "When are invoices issued each month?"})
    assert seen[0] != seen[1] and "someone-else" not in seen


def test_feedback_is_stored_with_rating_and_reason_and_no_text() -> None:
    store = MemoryStore()
    milo = build_app(ToolThenAnswer(), LexicalEmbedder(), Backend(store=store))
    milo.store = store
    _, c, _ = signed_in_app(milo)
    ok = c.post("/api/feedback", json={"rating": "down", "reason": "missing_source"})
    assert ok.get_json()["ok"] is True
    assert c.post("/api/feedback", json={"rating": "maybe"}).status_code == 400
    assert (
        c.post(
            "/api/feedback", json={"rating": "down", "reason": "free text"}
        ).status_code
        == 400
    )
    assert store._feedback == [("1", "down", "missing_source")]
