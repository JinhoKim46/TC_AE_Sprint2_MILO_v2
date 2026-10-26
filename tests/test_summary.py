"""The end-of-conversation summary: built from recorded facts and computed estimates, no model call. Offline."""

from __future__ import annotations

from milo.store import MemoryStore
from milo.summary import build_summary
from milo.tools import Backend


def record(backend: Backend, user: str, field: str, value, unit: str = "") -> None:
    backend.call(
        "record_fact",
        {
            "field_id": field,
            "value": value,
            "status": "reported",
            "evidence_text": str(value),
            "unit": unit or "x",
        },
        user_id=user,
    )


def test_no_facts_gives_no_estimate_and_lists_what_is_needed() -> None:
    backend = Backend(store=MemoryStore())
    d = build_summary(backend, "u1")
    assert d["proposal"]["headline"] == "No estimate yet"
    assert d["facts"] == []
    assert d["missing"], "the must-have items should be listed as missing"
    assert all(a["estimate"]["status"] != "ok" for a in d["areas"])


def test_recorded_facts_give_the_proposal_with_its_range_and_assumptions() -> None:
    backend = Backend(store=MemoryStore())
    record(backend, "u1", "requests_per_week", 40)
    record(backend, "u1", "minutes_to_assign", 12)
    d = build_summary(backend, "u1")
    area = next(a for a in d["areas"] if a["id"] == "request-dispatch")
    assert area["estimate"]["status"] == "ok"
    lo, hi = area["estimate"]["range"]
    assert d["proposal"]["headline"] == "Start with Request and dispatch management"
    assert f"{lo} to {hi} hours a week" in d["proposal"]["body"]
    assert {f["field"] for f in d["facts"]} == {
        "requests per week",
        "minutes to assign",
    }
    assert d["proposal"]["excluded"], "the spec must say what is not included"
