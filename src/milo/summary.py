"""The end-of-conversation summary: what MILO recorded, the estimate for each service area, and a proposed first spec.

Built in code from the owner's recorded facts and the computed estimates. No model is called, so it costs nothing and
never invents a figure: an area without the inputs it needs is listed as 'needs input', with what is missing.
"""

from __future__ import annotations

from typing import Any

from milo.tools import CATALOGUE


def _words(identifier: str) -> str:
    return identifier.replace("_", " ").replace("-", " ")


def build_summary(backend: Any, user_id: str) -> dict[str, Any]:
    recorded = backend.call("get_recorded_facts", {}, user_id=user_id)
    facts = [
        {
            "field": _words(field_id),
            "value": values[-1].get("value") if values else None,
            "status": values[-1].get("status", "") if values else "",
        }
        for field_id, values in recorded["facts"].items()
    ]
    areas = []
    for area in CATALOGUE["modules"]:
        estimate = backend.call(
            "estimate_effect", {"area_id": area["id"]}, user_id=user_id
        )
        areas.append(
            {
                "id": area["id"],
                "name": area["name"],
                "scope": area["includes"],
                "excluded": area["excludes"],
                "estimate": estimate,
            }
        )
    ready = sorted(
        (a for a in areas if a["estimate"].get("status") == "ok"),
        key=lambda a: -a["estimate"]["central"],
    )
    missing = [_words(x) for x in recorded["missing_must"]]
    return {
        "facts": facts,
        "areas": [
            {"id": a["id"], "name": a["name"], "estimate": a["estimate"]} for a in areas
        ],
        "missing": missing,
        "proposal": _proposal(ready, missing),
    }


def _proposal(ready: list[dict[str, Any]], missing: list[str]) -> dict[str, Any]:
    if not ready:
        return {
            "headline": "No estimate yet",
            "body": "MILO needs more facts before it can propose a first automation.",
            "scope": [],
            "excluded": [],
            "next": missing,
        }
    first = ready[0]
    est = first["estimate"]
    lo, hi = est["range"]
    return {
        "headline": f"Start with {first['name']}",
        "body": f"About {lo} to {hi} hours a week saved (central {est['central']}). The estimate uses these assumptions: "
        + "; ".join(est["assumed"])
        + ".",
        "scope": first["scope"],
        "excluded": first["excluded"],
        "next": missing,
        "then": [a["name"] for a in ready[1:]],
    }
