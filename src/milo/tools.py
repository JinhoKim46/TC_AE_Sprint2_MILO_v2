"""M3 tools: the specs come from data/tools.yaml; the handlers run in code, never in the model.

- Every argument is checked against the spec before a handler runs (`invalid_args`).
- Facts come from the intake harness (data/intake_harness.yaml); each keeps its status, unit and evidence text.
- `estimate_effect` is computed here from recorded facts. A value the owner did not give is either labelled assumed (the
  baseline and new minutes, as in the catalogue) or, for events, withheld: the answer then asks for it. The model never
  supplies a number.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml

from milo.store import MemoryStore, Store
from milo.types import ToolSpec

DATA = Path(__file__).resolve().parents[2] / "data"
TOOLS = yaml.safe_load((DATA / "tools.yaml").read_text())
HARNESS = yaml.safe_load((DATA / "intake_harness.yaml").read_text())
CATALOGUE = yaml.safe_load((DATA / "catalogue.yaml").read_text())
SLOTS = {s["id"]: s for s in HARNESS["common"]}
for _area, _items in HARNESS["areas"].items():
    SLOTS.update({s["id"]: {**s, "area": _area} for s in _items})
AREAS = {m["id"]: m for m in CATALOGUE["modules"]}
RANGE = (
    0.8,
    1.2,
)  # low and high factors on the central value, unless the owner gives a range
STATUSES = ("reported", "conflicting", "unknown")
ENUMS = {
    "enum_from:intake_harness": list(SLOTS),
    "enum_from:catalogue.modules": list(AREAS),
}


def _schema(args: dict[str, Any]) -> dict[str, Any]:
    props, required = {}, []
    for name, spec in args.items():
        prop: dict[str, Any] = {}
        t = spec.get("type", "string")
        prop["type"] = t
        if "enum" in spec:
            prop["enum"] = spec["enum"]
        if "enum_from" in spec:
            prop["enum"] = ENUMS[f"enum_from:{spec['enum_from']}"]
        if "items_from" in spec:
            prop["items"] = {"type": "string"}
        props[name] = prop
        if spec.get("required"):
            required.append(name)
    return {
        "type": "object",
        "properties": props,
        "required": required,
        "additionalProperties": False,
    }


def specs() -> list[ToolSpec]:
    return [
        ToolSpec(t["name"], t["description"], _schema(t["args"]), t["risk"])
        for t in TOOLS["tools"]
    ]


def validate_args(
    name: str, args: dict[str, Any], spec_list: list[ToolSpec]
) -> str | None:
    """A message describing the first problem with the arguments, or None when they are valid."""
    spec = next((s for s in spec_list if s.name == name), None)
    if spec is None:
        return f"unknown tool {name}"
    schema = spec.parameters
    for key in schema["required"]:
        if key not in args:
            return f"missing argument {key}"
    for key, value in args.items():
        if key not in schema["properties"]:
            return f"unexpected argument {key}"
        prop = schema["properties"][key]
        if "enum" in prop and value not in prop["enum"]:
            return f"{key} must be one of the allowed values"
        expected = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "array": list,
            "boolean": bool,
        }
        types = prop["type"] if isinstance(prop["type"], list) else [prop["type"]]
        allowed: list[type] = []
        for t in types:
            allowed.extend(
                expected[t] if isinstance(expected[t], tuple) else (expected[t],)
            )
        if not isinstance(value, tuple(allowed)):
            return f"{key} has the wrong type"
    return None


class Backend:
    """Holds each owner's facts and diagnoses in memory. Persistence is M4/M6's concern, not this milestone's."""

    def __init__(
        self,
        search: Callable[[str], list[Any]] | None = None,
        store: Store | None = None,
    ) -> None:
        self._search = search or (lambda q: [])
        self.store: Store = store if store is not None else MemoryStore()

    def attach_search(self, search: Callable[[str], list[Any]]) -> None:
        """The app gives the backend its retrieval, so search_knowledge uses the same index as the answers."""
        self._search = search

    def specs(self) -> list[ToolSpec]:
        return specs()

    def call(self, name: str, args: dict[str, Any], *, user_id: str) -> Any:
        handler = getattr(self, f"_{name}", None)
        if handler is None:
            raise ValueError(f"no handler for {name}")
        return handler(args, user_id)

    # ---- read tools -----------------------------------------------------------------------------------------

    def _search_knowledge(
        self, args: dict[str, Any], user_id: str
    ) -> list[dict[str, Any]]:
        return [
            {"chunk_id": s.chunk_id, "doc_id": s.doc_id, "text": s.text}
            for s in self._search(args["query"])
        ]

    def _get_recorded_facts(self, args: dict[str, Any], user_id: str) -> dict[str, Any]:
        recorded = {
            fid: vals for fid, vals in self.store.facts(user_id).items() if vals
        }
        missing = [
            s["id"] for s in SLOTS.values() if s["must"] and s["id"] not in recorded
        ]
        return {"facts": recorded, "missing_must": missing}

    def _estimate_effect(self, args: dict[str, Any], user_id: str) -> dict[str, Any]:
        area = AREAS[args["area_id"]]
        effect = area["effect_inputs"]
        facts = self.store.facts(user_id)
        events = self._latest(facts, effect["events"])
        if events is None:
            return {"status": "needs_input", "needed": effect["events"]}
        base = self._latest(facts, effect["baseline_minutes"])
        new = effect["new_minutes"]["assumed"]
        assumed = []
        if base is None:
            base = effect["baseline_default"]
            assumed.append(f"{effect['baseline_minutes']} (assumed {base})")
        assumed.append(f"new_minutes (assumed {new}): {effect['new_minutes']['note']}")
        central = events * (base - new) / 60
        lo, hi = central * RANGE[0], central * RANGE[1]
        period = SLOTS[effect["events"]]["unit"].split("/")[-1]
        return {
            "status": "ok",
            "unit": f"hours per {period}",
            "central": round(central, 2),
            "range": [round(lo, 2), round(hi, 2)],
            "assumed": assumed,
        }

    @staticmethod
    def _latest(facts: dict[str, list[dict[str, Any]]], field_id: str) -> float | None:
        values = [f for f in facts.get(field_id, []) if f["status"] != "unknown"]
        if not values:
            return None
        v = values[-1]["value"]
        return (
            float(v)
            if isinstance(v, (int, float, str)) and str(v).replace(".", "", 1).isdigit()
            else None
        )

    # ---- write tools ----------------------------------------------------------------------------------------

    def _record_fact(self, args: dict[str, Any], user_id: str) -> dict[str, Any]:
        if args["status"] not in STATUSES:
            return {"ok": False, "error": "invalid status"}
        entry = {
            "value": args["value"],
            "unit": args.get("unit", SLOTS[args["field_id"]]["unit"]),
            "status": args["status"],
            "evidence_text": args["evidence_text"],
        }
        count = self.store.add_fact(user_id, args["field_id"], entry)
        return {
            "ok": True,
            "field_id": args["field_id"],
            "recorded": count,
        }

    def _draft_diagnosis(self, args: dict[str, Any], user_id: str) -> dict[str, Any]:
        area = args["area_id"]
        recorded = self._get_recorded_facts({}, user_id)
        must = [
            s["id"]
            for s in SLOTS.values()
            if s["must"] and (s.get("area") in (None, area))
        ]
        missing = [m for m in must if m not in recorded["facts"]]
        effect = self._estimate_effect({"area_id": area}, user_id)
        card = {
            "area_id": area,
            "status": "conditional" if missing else "full",
            "missing_must": missing,
            "effect": effect,
        }
        number = self.store.add_diagnosis(user_id, card)
        return {"diagnosis_id": number, **card}

    def _reset_diagnosis(self, args: dict[str, Any], user_id: str) -> dict[str, Any]:
        return {
            "ok": False,
            "error": "needs approval",
        }  # the policy layer decides; this handler never runs unapproved
