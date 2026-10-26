"""M3: tools run in code. The estimate is computed from recorded facts, assumptions are labelled, and missing data is asked for."""

from __future__ import annotations

import pytest

from milo.tools import Backend, specs, validate_args


def record(
    b: Backend, field_id: str, value, status: str = "reported", user: str = "u1"
) -> None:
    b.call(
        "record_fact",
        {
            "field_id": field_id,
            "value": value,
            "status": status,
            "evidence_text": "owner said it",
        },
        user_id=user,
    )


def test_estimate_is_computed_in_code_with_a_range_and_labelled_assumptions() -> None:
    b = Backend()
    record(b, "requests_per_week", 40)
    out = b.call("estimate_effect", {"area_id": "request-dispatch"}, user_id="u1")
    assert out["status"] == "ok"
    assert out["central"] == pytest.approx(
        40 * (12 - 4) / 60, abs=0.01
    )  # the owner gave no minutes, so 12 is assumed
    assert out["range"] == [
        pytest.approx(out["central"] * 0.8, abs=0.01),
        pytest.approx(out["central"] * 1.2, abs=0.01),
    ]
    assert any("assumed 12" in a for a in out["assumed"])


def test_estimate_asks_for_the_events_it_cannot_assume() -> None:
    out = Backend().call(
        "estimate_effect", {"area_id": "consumables-stock"}, user_id="u1"
    )
    assert out == {"status": "needs_input", "needed": "searches_per_week"}


def test_unknown_facts_do_not_feed_the_estimate() -> None:
    b = Backend()
    record(b, "requests_per_week", 40, status="unknown")
    assert (
        b.call("estimate_effect", {"area_id": "request-dispatch"}, user_id="u1")[
            "status"
        ]
        == "needs_input"
    )


def test_facts_are_kept_per_owner() -> None:
    b = Backend()
    record(b, "requests_per_week", 40, user="u1")
    assert b.call("get_recorded_facts", {}, user_id="u2")["facts"] == {}


def test_a_draft_diagnosis_is_conditional_when_must_have_items_are_missing() -> None:
    b = Backend()
    card = b.call("draft_diagnosis", {"area_id": "usage-billing-prep"}, user_id="u1")
    assert card["status"] == "conditional"
    assert "readings_per_month" in card["missing_must"]
    assert "business_type" in card["missing_must"]


def test_validate_args_rejects_unknown_fields_and_values() -> None:
    all_specs = specs()
    assert validate_args(
        "record_fact",
        {"field_id": "nope", "value": 1, "status": "reported", "evidence_text": "x"},
        all_specs,
    )
    assert validate_args(
        "estimate_effect", {"area_id": "request-dispatch", "extra": 1}, all_specs
    )
    assert (
        validate_args("estimate_effect", {"area_id": "request-dispatch"}, all_specs)
        is None
    )


def test_no_tool_result_contains_a_price() -> None:
    b = Backend()
    record(b, "requests_per_week", 40)
    text = str(b.call("estimate_effect", {"area_id": "request-dispatch"}, user_id="u1"))
    assert "USD" not in text and "$" not in text
