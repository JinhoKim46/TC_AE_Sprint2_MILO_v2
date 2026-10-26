"""PostgreSQL store, against the real database. Runs only with MILO_DB_TESTS=1 and MILO_DATABASE_URL set.

Each test uses a fresh owner id and deletes that owner's rows afterwards, so no test data is left behind.
"""

from __future__ import annotations

import os
import uuid

import pytest

from milo.store import MAX_HISTORY_TURNS

URL = os.environ.get("MILO_DATABASE_URL", "")
pytestmark = pytest.mark.skipif(
    os.environ.get("MILO_DB_TESTS") != "1" or not URL,
    reason="needs MILO_DB_TESTS=1 and MILO_DATABASE_URL (a real database)",
)


@pytest.fixture
def store():
    from milo.pgstore import PostgresStore

    s = PostgresStore(URL)
    owners: list[str] = []

    def new_owner() -> str:
        o = f"test-{uuid.uuid4().hex}"
        owners.append(o)
        return o

    s.new_owner = new_owner  # type: ignore[attr-defined]
    yield s
    for o in owners:
        s.delete_owner(o)
    s.close()


def test_history_round_trips_and_is_capped(store) -> None:
    o = store.new_owner()
    turns = [{"role": "user", "content": str(i)} for i in range(MAX_HISTORY_TURNS + 4)]
    store.append_turns(o, "t1", turns)
    got = store.history(o, "t1")
    assert len(got) == MAX_HISTORY_TURNS and got[-1] == turns[-1]


def test_owners_are_isolated(store) -> None:
    a, b = store.new_owner(), store.new_owner()
    store.append_turns(a, "t1", [{"role": "user", "content": "private"}])
    assert store.history(b, "t1") == []
    store.add_fact(
        a,
        "requests_per_week",
        {"value": 40, "status": "reported", "evidence_text": "about 40"},
    )
    assert store.facts(b) == {}


def test_facts_and_diagnoses_round_trip(store) -> None:
    o = store.new_owner()
    n = store.add_fact(
        o,
        "requests_per_week",
        {
            "value": 40,
            "unit": "requests/week",
            "status": "reported",
            "evidence_text": "about 40",
        },
    )
    assert n == 1
    assert store.facts(o)["requests_per_week"][0]["value"] == 40
    assert (
        store.add_diagnosis(o, {"area_id": "request-dispatch", "status": "conditional"})
        == 1
    )
    assert store.diagnoses(o)[0]["area_id"] == "request-dispatch"
