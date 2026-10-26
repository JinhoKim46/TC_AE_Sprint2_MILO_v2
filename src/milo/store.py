"""The storage interface. The app and the tools keep their state here, never in their own attributes.

Only `MemoryStore` exists: state lives in the process and is lost on restart, as issue #2 specifies. A database store
(SQLite or PostgreSQL) implements the same methods later; no caller changes.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Protocol

MAX_HISTORY_TURNS = 20  # the last 20 messages (10 exchanges) are sent to the model; older turns are kept but not sent


class Store(Protocol):
    def append_turns(
        self, owner: str, thread: str, turns: list[dict[str, str]]
    ) -> None: ...

    def history(
        self, owner: str, thread: str, limit: int = MAX_HISTORY_TURNS
    ) -> list[dict[str, str]]: ...

    def add_fact(self, owner: str, field_id: str, entry: dict[str, Any]) -> int: ...

    def facts(self, owner: str) -> dict[str, list[dict[str, Any]]]: ...

    def add_diagnosis(self, owner: str, card: dict[str, Any]) -> int: ...

    def diagnoses(self, owner: str) -> list[dict[str, Any]]: ...

    def record_flow(self, owner: str, thread: str, flow: dict[str, Any]) -> None: ...

    def flows(self, owner: str | None, limit: int = 50) -> list[dict[str, Any]]: ...

    def add_feedback(self, owner: str, rating: str, reason: str) -> None: ...


class MemoryStore:
    """Dictionaries in memory. Every read is keyed by the owner, so one owner never sees another's data."""

    def __init__(self) -> None:
        self._turns: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
        self._facts: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(
            lambda: defaultdict(list)
        )
        self._diagnoses: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self._flows: list[tuple[str, str, dict[str, Any]]] = []
        self._feedback: list[tuple[str, str, str]] = []

    def append_turns(
        self, owner: str, thread: str, turns: list[dict[str, str]]
    ) -> None:
        self._turns[(owner, thread)].extend(turns)

    def history(
        self, owner: str, thread: str, limit: int = MAX_HISTORY_TURNS
    ) -> list[dict[str, str]]:
        return list(self._turns[(owner, thread)][-limit:]) if limit > 0 else []

    def add_fact(self, owner: str, field_id: str, entry: dict[str, Any]) -> int:
        self._facts[owner][field_id].append(entry)
        return len(self._facts[owner][field_id])

    def facts(self, owner: str) -> dict[str, list[dict[str, Any]]]:
        return {k: list(v) for k, v in self._facts[owner].items()}

    def add_diagnosis(self, owner: str, card: dict[str, Any]) -> int:
        self._diagnoses[owner].append(card)
        return len(self._diagnoses[owner])

    def diagnoses(self, owner: str) -> list[dict[str, Any]]:
        return list(self._diagnoses[owner])

    def record_flow(self, owner: str, thread: str, flow: dict[str, Any]) -> None:
        self._flows.append((owner, thread, flow))

    def flows(self, owner: str | None, limit: int = 50) -> list[dict[str, Any]]:
        rows = [f for o, _, f in self._flows if owner is None or o == owner]
        return rows[-limit:][::-1]

    def add_feedback(self, owner: str, rating: str, reason: str) -> None:
        self._feedback.append((owner, rating, reason))
