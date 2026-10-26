"""M2: query translation, the self-query schema and its fallback to unfiltered search. Offline."""

from __future__ import annotations

from milo.advanced import retrieve, self_query, translate_keywords, validate_filters
from milo.chunk import chunk_article
from milo.embed import LexicalEmbedder
from milo.index import Index


class RecordingIndex:
    def __init__(self) -> None:
        self.calls: list[dict | None] = []

    def search(self, vector, k, where=None):
        self.calls.append(where)
        return [] if where else [("c1", "text", 0.9)]


def test_invalid_self_query_output_falls_back_to_unfiltered_search() -> None:
    idx = RecordingIndex()
    for bad in (
        {"product": "not-an-area"},
        {"owner": "u1"},
        {"section": 3},
        {},
        "product=x",
    ):
        idx.calls.clear()
        retrieve(idx, [0.0], 5, bad)  # type: ignore[arg-type]
        assert idx.calls[-1] is None, (
            f"invalid filter {bad!r} must not reach the index as a filter"
        )


def test_valid_filter_is_used_and_empty_result_falls_back() -> None:
    idx = RecordingIndex()
    retrieve(idx, [0.0], 5, {"product": "consumables-stock"})
    assert idx.calls == [{"product": "consumables-stock"}, None]


def test_validate_filters_accepts_only_known_keys_and_values() -> None:
    assert validate_filters({"product": "request-dispatch", "section": "cases"}) == {
        "product": "request-dispatch",
        "section": "cases",
    }
    assert validate_filters({"product": "request-dispatch", "price": "1"}) is None
    assert (
        validate_filters({"section": "pricing"}) is None
    )  # the old section no longer exists


def test_case_id_maps_to_its_area() -> None:
    assert self_query(
        "What does C04 say about stock?", {"C04": "consumables-stock"}
    ) == {"product": "consumables-stock"}


def test_ambiguous_question_gets_no_product_filter() -> None:
    assert self_query("Tell me something general about this.") is None


def test_translation_drops_question_words_and_adds_area_terms() -> None:
    out = translate_keywords("How do calls become a queue?")
    assert "how" not in out.split() and "request" in out.split()


def test_filtered_search_returns_only_the_filtered_area() -> None:
    from milo.types import Document

    docs = [
        Document(
            "solutions/a",
            "Stock is kept by location.",
            {"product": "consumables-stock"},
        ),
        Document(
            "solutions/b",
            "Requests go into one queue.",
            {"product": "request-dispatch"},
        ),
    ]
    chunks = []
    for d in docs:
        chunks.extend(
            chunk_article(
                d.doc_id,
                f"---\ntitle: t\nsection: solutions\nproduct: {d.metadata['product']}\n---\n{d.text}",
            )
        )
    emb = LexicalEmbedder()
    idx = Index(chunks, emb.embed([c.text for c in chunks]))
    hits = retrieve(
        idx, emb.embed(["requests"])[0], 5, {"product": "consumables-stock"}
    )
    assert hits and all(
        "consumables" in idx._col.get(ids=[h[0]])["metadatas"][0]["product"]
        for h in hits
    )
