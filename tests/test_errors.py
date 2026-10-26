"""M5: typed errors, bounded retries, the local fallback and one trace per flow. Offline: the models are fakes."""

from __future__ import annotations

import json

import pytest

from milo import app as app_module
from milo.app import MAX_INPUT_CHARS, PROVIDER_MSG, build_app
from milo.embed import LexicalEmbedder
from milo.types import ChatReply, Document, Usage


class Failing:
    price_usd_per_mtok = (0.0, 0.0)

    def __init__(self) -> None:
        self.calls = 0

    def invoke(self, messages, tools=None):
        self.calls += 1
        raise TimeoutError("provider timed out")


class Answering:
    price_usd_per_mtok = (1.0, 1.0)

    def __init__(self, text: str = "ok") -> None:
        self.calls = 0
        self.text = text

    def invoke(self, messages, tools=None):
        self.calls += 1
        return ChatReply(content=self.text, usage=Usage(10, 5))


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr(app_module.time, "sleep", lambda s: None)


def ready(chat, fallback=None, trace_path=None):
    app = build_app(chat, LexicalEmbedder(), None)
    app.fallback = fallback
    app.trace_path = trace_path
    app.ingest(
        [Document("kb/x", "Invoices are issued on the first day of each month.", {})]
    )
    return app


@pytest.mark.parametrize(
    "text, reason",
    [
        ("", "empty"),
        ("   ", "empty"),
        ("a" * (MAX_INPUT_CHARS + 1), "longer"),
        ("hi\x00there", "control"),
    ],
)
def test_bad_input_is_a_typed_error_with_no_model_call(text, reason) -> None:
    chat = Answering()
    r = ready(chat).ask(text, "u1", "t1")
    assert r.error.startswith("invalid_input") and reason in r.error
    assert chat.calls == 0


def test_provider_failure_is_retried_a_bounded_number_of_times_then_reported() -> None:
    chat = Failing()
    r = ready(chat).ask("When are invoices issued each month?", "u1", "t1")
    assert chat.calls == app_module.RETRIES + 1
    assert r.error == "provider_error: TimeoutError"
    assert r.answer == PROVIDER_MSG and "Traceback" not in r.answer


def test_fallback_answers_when_the_primary_fails() -> None:
    fallback = Answering("from the local model")
    r = ready(Failing(), fallback=fallback).ask(
        "When are invoices issued each month?", "u1", "t1"
    )
    assert r.answer == "from the local model" and r.error is None
    assert fallback.calls == 1


def test_one_trace_line_per_flow_records_the_steps(tmp_path) -> None:
    path = tmp_path / "trace.jsonl"
    app = ready(Answering(), trace_path=path)
    app.ask("When are invoices issued each month?", "u1", "t1")
    app.ask("", "u1", "t1")
    lines = [json.loads(x) for x in path.read_text().splitlines()]
    assert len(lines) == 2
    assert [s["step"] for s in lines[0]["steps"]] == [
        "history_read",
        "retrieve",
        "model",
        "answer",
    ]
    assert "u1" not in path.read_text(), (
        "the trace must hold a hashed owner, not the owner id"
    )
    assert lines[1]["error"].startswith("invalid_input")
