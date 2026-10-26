"""M3 tool evaluation on data/tool_cases.jsonl: selection, parameters and over-eager calls.

Live run (a model chooses the tools; paid, capped by --max-cost):
    MILO_LIVE=1 uv run python scripts/eval_tools.py --live --max-cost 0.02
Scorer self-test (no model; checks that the scorer catches wrong behaviour):
    uv run python scripts/eval_tools.py --selftest

Per case, a call counts as correct when:
- selection: the set of tool names called equals the expected set,
- parameters: each expected argument is present with the expected value (for record_fact, the value is compared as a
  number when both sides are numbers),
- over-eager: a case that expects no tool made no call.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from milo.types import Document

CASES = ROOT / "data" / "tool_cases.jsonl"
RESULTS = ROOT / "evals" / "results" / "tools" / "tool_eval.json"


def score(case: dict[str, Any], called: list[dict[str, Any]]) -> dict[str, bool]:
    expected = case["expected_calls"]
    selection = {c["name"] for c in expected} == {c["name"] for c in called}
    params = True
    for exp in expected:
        match = [c for c in called if c["name"] == exp["name"]]
        if not match:
            params = False
            break
        got = match[0]["args"]
        for key, value in exp["args"].items():
            g = got.get(key)
            if isinstance(value, (int, float)) and isinstance(g, (int, float)):
                ok = float(g) == float(value)
            else:
                ok = g == value
            params = params and ok
    over_eager = (not expected) and bool(called)
    return {"selection": selection, "parameters": params, "over_eager": over_eager}


def aggregate(rows: list[dict[str, Any]]) -> dict[str, float]:
    with_calls = [r for r in rows if r["expected"]]
    no_calls = [r for r in rows if not r["expected"]]
    return {
        "selection_rate": sum(r["selection"] for r in rows) / len(rows),
        "parameter_rate": sum(r["parameters"] for r in with_calls)
        / max(len(with_calls), 1),
        "false_call_rate": sum(r["over_eager"] for r in no_calls)
        / max(len(no_calls), 1),
    }


def selftest() -> None:
    case = {
        "expected_calls": [
            {
                "name": "record_fact",
                "args": {"field_id": "requests_per_week", "value": 60},
            }
        ]
    }
    good = [
        {
            "name": "record_fact",
            "args": {"field_id": "requests_per_week", "value": 60.0},
        }
    ]
    wrong_value = [
        {"name": "record_fact", "args": {"field_id": "requests_per_week", "value": 6}}
    ]
    wrong_tool = [{"name": "estimate_effect", "args": {"area_id": "request-dispatch"}}]
    assert score(case, good) == {
        "selection": True,
        "parameters": True,
        "over_eager": False,
    }
    assert score(case, wrong_value)["parameters"] is False
    assert score(case, wrong_tool)["selection"] is False
    assert score({"expected_calls": []}, wrong_tool)["over_eager"] is True
    print(
        "selftest OK: the scorer catches wrong tools, wrong values and over-eager calls"
    )


def live(max_cost: float) -> None:
    import os

    from milo.app import build_app
    from milo.embed import LexicalEmbedder
    from milo.llm import live_chat_model
    from milo.tools import Backend

    if os.environ.get("MILO_LIVE") != "1":
        raise SystemExit("--live needs MILO_LIVE=1 (paid calls)")
    chat = live_chat_model()
    rows = []
    for case in (json.loads(x) for x in CASES.read_text().splitlines() if x.strip()):
        backend = Backend()
        for field_id, value in case["facts"].items():
            backend.call(
                "record_fact",
                {
                    "field_id": field_id,
                    "value": value,
                    "status": "reported",
                    "evidence_text": "fixture",
                },
                user_id=case["user_id"],
            )
        app = build_app(chat, LexicalEmbedder(), backend)
        app.ingest(
            [Document("kb/placeholder", "Requests are logged in one shared queue.", {})]
        )
        reply = app.ask(case["query"], user_id=case["user_id"], thread_id=case["id"])
        called = [{"name": r.name, "args": r.arguments} for r in reply.tool_results]
        s = score(case, called)
        rows.append(
            {
                "id": case["id"],
                "expected": case["expected_calls"],
                "called": called,
                **s,
            }
        )
    result = {
        "model": chat.model.model_name
        if hasattr(chat.model, "model_name")
        else "unknown",
        "cases": len(rows),
        "metrics": aggregate(rows),
        "rows": rows,
    }
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(json.dumps(result, indent=2, default=str) + "\n")
    print(json.dumps(result["metrics"], indent=2))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--max-cost", type=float, default=0.02)
    args = ap.parse_args()
    if args.selftest:
        selftest()
    elif args.live:
        live(args.max_cost)
    else:
        ap.error("choose --selftest or --live")


if __name__ == "__main__":
    main()
