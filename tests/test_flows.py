"""The flow view: per-owner flows from the trace file and the overview. Offline."""

from __future__ import annotations

import json

from milo.app import App
from milo.embed import LexicalEmbedder
from milo.flows import owner_hash, read_flows, summarize
from milo.store import MemoryStore
from milo.tools import Backend
from milo.types import ChatReply, Document, ToolCall, Usage
from milo.web import create_app


class CallThenAnswer:
    price_usd_per_mtok = (1.0, 1.0)

    def __init__(self) -> None:
        self.calls = 0

    def invoke(self, messages, tools=None):
        self.calls += 1
        if self.calls == 1:
            return ChatReply(
                tool_calls=[ToolCall("c1", "get_recorded_facts", {})],
                usage=Usage(50, 10),
            )
        return ChatReply(content="Nothing recorded yet [1].", usage=Usage(60, 12))


def test_trace_records_each_step_with_timing_and_the_table_it_touches(tmp_path) -> None:
    path = tmp_path / "trace.jsonl"
    store = MemoryStore()
    app = App(
        CallThenAnswer(),
        LexicalEmbedder(),
        Backend(store=store),
        trace_path=path,
        store=store,
    )
    app.ingest(
        [Document("kb/x", "Invoices are issued on the first day of each month.", {})]
    )
    r = app.ask("When are invoices issued each month?", "u1", "t1")
    kinds = [s["step"] for s in r.trace]
    assert kinds == ["history_read", "retrieve", "model", "tool", "model", "answer"]
    tool = next(s for s in r.trace if s["step"] == "tool")
    assert (
        tool["table"] == "facts (read)"
        and tool["decision"] == "allowed"
        and tool["ms"] >= 0
    )
    summary = summarize(read_flows(path, "u1"))
    assert summary["questions"] == 1 and summary["tool_calls"] == {
        "get_recorded_facts": 1
    }
    assert summary["tokens"] == {"input": 110, "output": 22}


def test_flows_are_per_owner(tmp_path) -> None:
    path = tmp_path / "trace.jsonl"
    store = MemoryStore()
    app = App(
        CallThenAnswer(),
        LexicalEmbedder(),
        Backend(store=store),
        trace_path=path,
        store=store,
    )
    app.ingest(
        [Document("kb/x", "Invoices are issued on the first day of each month.", {})]
    )
    app.ask("When are invoices issued each month?", "u1", "t1")
    assert read_flows(path, "u2") == []
    assert "u1" not in path.read_text()
    assert read_flows(path, "u1")[0]["owner"] == owner_hash("u1")


def test_flow_endpoints_and_dashboard_page(tmp_path) -> None:
    store = MemoryStore()
    path = tmp_path / "trace.jsonl"
    app = App(
        CallThenAnswer(),
        LexicalEmbedder(),
        Backend(store=store),
        trace_path=path,
        store=store,
    )
    app.ingest(
        [Document("kb/x", "Invoices are issued on the first day of each month.", {})]
    )
    c = create_app(app, secret_key="test").test_client()
    c.get("/chat")
    body = c.post(
        "/api/ask", json={"question": "When are invoices issued each month?"}
    ).get_json()
    assert [s["step"] for s in body["trace"]][-1] == "answer"
    flows = c.get("/api/flows").get_json()
    assert flows["summary"]["questions"] == 1 and flows["flows"][0]["steps"]
    page = c.get("/dashboard").get_data(as_text=True)
    assert "How MILO works" in page and "/api/flows" in page
    assert json.dumps(flows)  # serialisable
