"""Compare the app's own tool loop with LangChain's create_agent on the same tool cases.

Live run (paid; both arms call the chat model): MILO_LIVE=1 uv run python scripts/eval_agent_arm.py --live --max-cost 0.10
Each arm gets the same facts, the same question and the same scorer as scripts/eval_tools.py.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from eval_tools import aggregate, score

from milo.types import Document

CASES = ROOT / "data" / "tool_cases.jsonl"
RESULTS = ROOT / "evals" / "results" / "tools" / "agent_arm_compare.json"
PLACEHOLDER = [
    Document("kb/placeholder", "Requests are logged in one shared queue.", {})
]


def cases() -> list[dict[str, Any]]:
    return [json.loads(x) for x in CASES.read_text().splitlines() if x.strip()]


def seeded_backend(case: dict[str, Any]):
    from milo.store import MemoryStore
    from milo.tools import Backend

    backend = Backend(store=MemoryStore())
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
    return backend


def run_app_arm(case: dict[str, Any], chat: Any) -> list[dict[str, Any]]:
    from milo.app import build_app
    from milo.embed import LexicalEmbedder

    backend = seeded_backend(case)
    app = build_app(chat, LexicalEmbedder(), backend)
    app.ingest(PLACEHOLDER)
    reply = app.ask(case["query"], user_id=case["user_id"], thread_id=case["id"])
    return [{"name": r.name, "args": r.arguments} for r in reply.tool_results]


def run_agent_arm(case: dict[str, Any], model: Any) -> list[dict[str, Any]]:
    from milo.agent_arm import run_agent

    backend = seeded_backend(case)
    result = run_agent(
        case["query"], backend, case["user_id"], model, thread_id=case["id"]
    )
    return [{"name": c["name"], "args": c["args"]} for c in result["calls"]] + [
        {"name": w["name"], "args": w["args"]} for w in result["waiting"]
    ]


def live(max_cost: float) -> None:
    from langchain_openai import ChatOpenAI

    from milo.llm import OPENROUTER_BASE_URL, live_chat_model

    if os.environ.get("MILO_LIVE") != "1":
        raise SystemExit("--live needs MILO_LIVE=1 (paid calls)")
    chat = live_chat_model()
    model = ChatOpenAI(
        model=os.environ.get("MILO_CHAT_MODEL", "anthropic/claude-haiku-5.5"),
        api_key=os.environ["OPENROUTER_API_KEY"].strip(),
        base_url=OPENROUTER_BASE_URL,
        temperature=0,
        timeout=30,
        max_retries=0,
    )
    rows: dict[str, list[dict[str, Any]]] = {"app": [], "agent": []}
    for case in cases():
        for arm, runner in (
            ("app", lambda c: run_app_arm(c, chat)),
            ("agent", lambda c: run_agent_arm(c, model)),
        ):
            called = runner(case)
            rows[arm].append(
                {
                    "id": case["id"],
                    "expected": case["expected_calls"],
                    "called": called,
                    **score(case, called),
                }
            )
    summary = {arm: aggregate(r) for arm, r in rows.items()}
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(
        json.dumps({"summary": summary, "rows": rows}, indent=2, ensure_ascii=False)
        + "\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--max-cost", type=float, default=0.10)
    args = ap.parse_args()
    if args.live:
        live(args.max_cost)
    else:
        raise SystemExit("run with --live (paid), or import the functions")
