"""M1: chunking, the offline embedder, the metrics and the app's retrieval. Offline; the live embedder is never built here."""

from __future__ import annotations

import math

import pytest

from milo.app import ABSTAIN, build_app
from milo.chunk import SIZE, chunk_body, chunk_section
from milo.embed import LexicalEmbedder, OpenRouterEmbedder
from milo.metrics import mean_ci, ndcg_at_k, recall_at_k
from milo.types import ChatReply, Document, Usage


class ScriptedChat:
    price_usd_per_mtok = (1.0, 2.0)

    def __init__(self) -> None:
        self.calls = 0

    def invoke(self, messages, tools=None):
        self.calls += 1
        return ChatReply(content="answer", usage=Usage(1_000_000, 500_000))


def test_paragraph_that_fits_is_never_cut() -> None:
    para = "The dispatcher decides every change. " * 10  # about 370 characters
    text = f"{para.strip()}\n\nA second short paragraph."
    pieces = chunk_section(text)
    assert any(para.strip() in p for p in pieces), (
        "the paragraph must sit whole in one chunk"
    )


def test_long_paragraph_is_cut_with_overlap_under_the_size() -> None:
    sentence = "Each visit is logged with the device, the fault and the time. "
    pieces = chunk_section(sentence * 40)
    assert len(pieces) > 1
    assert all(len(p) <= SIZE for p in pieces)


def test_chunks_never_cross_a_heading() -> None:
    body = "# Title\n\nFirst part.\n\n## Second\n\nSecond part."
    chunks = chunk_body("doc/x", body, {"title": "T", "section": "s", "product": "p"})
    assert len(chunks) == 2
    assert "First part" in chunks[0].text and "Second" not in chunks[0].text
    assert "Second part" in chunks[1].text and "First" not in chunks[1].text


def test_lexical_embedder_is_deterministic_and_normalised() -> None:
    e = LexicalEmbedder()
    a, b = e.embed(["request queue"]), e.embed(["request queue"])
    assert a == b
    assert math.isclose(sum(v * v for v in a[0]), 1.0)


def test_live_embedder_refuses_without_the_flag(monkeypatch) -> None:
    monkeypatch.delenv("MILO_LIVE", raising=False)
    with pytest.raises(PermissionError):
        OpenRouterEmbedder(0.02)


def test_recall_and_ndcg_on_known_ranks() -> None:
    assert recall_at_k(1) == 1.0 and recall_at_k(5) == 1.0 and recall_at_k(6) == 0.0
    assert recall_at_k(None) == 0.0
    assert ndcg_at_k(1) == 1.0
    assert math.isclose(ndcg_at_k(2), 1 / math.log2(3))
    assert ndcg_at_k(6) == 0.0


def test_bootstrap_interval_contains_the_mean_and_is_repeatable() -> None:
    values = [1.0, 0.0, 1.0, 1.0, 0.0, 1.0]
    mean, lo, hi = mean_ci(values)
    assert lo <= mean <= hi
    assert mean_ci(values) == mean_ci(values)


def test_app_answers_with_sources_and_the_top_passage_first() -> None:
    docs = [
        Document(
            "kb/alpha",
            "The alpha widget needs a firmware update every six months.",
            {"section": "hw"},
        ),
        Document(
            "kb/beta",
            "Invoices are issued on the first day of each month.",
            {"section": "billing"},
        ),
    ]
    chat = ScriptedChat()
    app = build_app(chat, LexicalEmbedder(), None)
    app.ingest(docs)
    r = app.ask("How often does the alpha widget need a firmware update?", "u1", "t1")
    assert r.sources and r.sources[0].doc_id == "kb/alpha"
    assert chat.calls == 1
    assert r.cost_usd == pytest.approx(
        1.0 + 1.0
    )  # 1M input at 1.0 plus 0.5M output at 2.0 per million


def test_app_abstains_without_a_model_call_when_nothing_matches() -> None:
    chat = ScriptedChat()
    app = build_app(chat, LexicalEmbedder(), None)
    app.ingest([Document("kb/alpha", "Firmware updates are needed.", {})])
    r = app.ask("zebra", "u1", "t1")
    assert (
        r.answer == ABSTAIN
        and r.sources == []
        and chat.calls == 0
        and r.cost_usd == 0.0
    )
