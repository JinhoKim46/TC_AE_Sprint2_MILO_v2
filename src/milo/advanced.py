"""M2 advanced retrieval: one query translation and a schema-validated self-query with a safe fallback.

Offline versions (no model call), so the A/B can run without a key:
- `translate_keywords`: query translation by rewriting. Drops question words and maps the owner's loose words to the
  area vocabulary (e.g. "calls", "queue" -> request-dispatch terms).
- `self_query`: turns a question into metadata filters (`product`, `section`) through a schema. Anything that does not
  validate returns None, and the caller searches without filters.

A live LLM version can replace either function later; the schema and the fallback stay the same.
"""

from __future__ import annotations

import re
from typing import Any

STOP = {
    "a", "an", "the", "is", "are", "do", "does", "how", "what", "which", "when", "where", "who", "i", "we", "our", "my",
    "you", "it", "to", "of", "in", "on", "for", "and", "or", "be", "can", "should", "would", "about", "that", "this",
}  # fmt: skip

# Owner words -> the vocabulary of the area articles (fictional, from data/kb/solutions).
EXPANSIONS = {
    "calls": ["request", "intake"],
    "queue": ["request", "queue"],
    "dispatch": ["dispatch", "technician"],
    "duplicate": ["duplicate", "request"],
    "toner": ["consumables", "stock"],
    "stock": ["stock", "location"],
    "spare": ["stock", "parts"],
    "meter": ["reading", "usage"],
    "readings": ["reading", "usage"],
    "invoice": ["billing", "reading"],
    "status": ["open", "work", "board"],
    "owner": ["owner", "board"],
}

AREAS = {
    "request-dispatch": {
        "request",
        "dispatch",
        "queue",
        "duplicate",
        "calls",
        "technician",
    },
    "consumables-stock": {
        "consumables",
        "stock",
        "toner",
        "parts",
        "spare",
        "location",
    },
    "usage-billing-prep": {
        "usage",
        "billing",
        "readings",
        "meter",
        "invoice",
        "counter",
    },
    "operations-overview": {"status", "board", "blocker", "commitment", "overview"},
}
SECTIONS = {
    "solutions": {"area", "module", "includes", "excludes"},
    "cases": {"case", "example", "analogous"},
    "consultation": {"method", "estimate", "formula", "range"},
    "policies": {"policy", "approval", "personal"},
}
ALLOWED_KEYS = {"product", "section"}


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text.lower())


def translate_keywords(question: str) -> str:
    out: list[str] = []
    for tok in _tokens(question):
        if tok in STOP:
            continue
        out.append(tok)
        out.extend(EXPANSIONS.get(tok, []))
    return " ".join(out)


def validate_filters(raw: Any) -> dict[str, str] | None:
    """Accept only a dict with keys from ALLOWED_KEYS and values from the known enums. Anything else is rejected."""
    if not isinstance(raw, dict) or not raw or not set(raw) <= ALLOWED_KEYS:
        return None
    if "product" in raw and raw["product"] not in AREAS:
        return None
    if "section" in raw and raw["section"] not in SECTIONS:
        return None
    if not all(isinstance(v, str) for v in raw.values()):
        return None
    return dict(raw)


CASE_ID = re.compile(r"^c\d{2}$")


def self_query(
    question: str, case_products: dict[str, str] | None = None
) -> dict[str, str] | None:
    """The filters a question implies, or None.

    A case id (C04) that names a known case gives its area directly, using the case article's product tag. Otherwise the
    area with the most matching words wins; a tie means no product filter.
    """
    words = set(_tokens(question))
    case_hits = {
        case_products[w.upper()]
        for w in words
        if CASE_ID.match(w) and case_products and w.upper() in case_products
    }
    if len(case_hits) == 1:
        raw: dict[str, str] = {"product": case_hits.pop()}
    else:
        scores = {area: len(words & vocab) for area, vocab in AREAS.items()}
        best = max(scores.values())
        if best == 0 or list(scores.values()).count(best) > 1:
            return None
        raw = {"product": max(scores, key=scores.get)}
    section_hits = {s: len(words & vocab) for s, vocab in SECTIONS.items()}
    best_section = max(section_hits.values())
    if best_section > 0 and list(section_hits.values()).count(best_section) == 1:
        raw["section"] = max(section_hits, key=section_hits.get)
    return validate_filters(raw)


def retrieve(
    index: Any, vector: list[float], k: int, where: dict[str, str] | None
) -> list[Any]:
    """Filtered search when the filter is valid; unfiltered search when it is missing, invalid, or returns nothing."""
    if where is not None and validate_filters(where) is not None:
        hits = index.search(vector, k, where=where)
        if hits:
            return hits
    return index.search(vector, k)
