"""Build labeling batch 5: real MILO answers to dev questions, with the passages each answer was given.

Live (paid, a few cents): MILO_LIVE=1 uv run python scripts/make_answer_batch.py --max-cost 0.05
Only dev items are used. The test and held-out sets are never read here.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from eval_retrieval import GOLD, GOLD_EXTRA

OUT = ROOT / "evals/labeling/batch5/items.jsonl"


def dev_questions() -> list[dict]:
    rows = [
        json.loads(x)
        for f in (GOLD, GOLD_EXTRA)
        for x in f.read_text().splitlines()
        if x.strip()
    ]
    return [r for r in rows if r["split"] == "dev" and r["gold_evidence"]]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cost", type=float, default=0.05)
    ap.add_argument("--n", type=int, default=30)
    args = ap.parse_args()
    if os.environ.get("MILO_LIVE") != "1":
        raise SystemExit("needs MILO_LIVE=1 (the answers come from the live model)")

    from milo.agent_app import AgentApp
    from milo.embed import OpenRouterEmbedder
    from milo.llm import live_agent_model, live_chat_model, local_chat_model
    from milo.serve import load_documents
    from milo.store import MemoryStore
    from milo.tools import Backend

    store = MemoryStore()
    app = AgentApp(
        live_chat_model(),
        OpenRouterEmbedder(max_cost_usd=args.max_cost),
        Backend(store=store),
        agent_model=live_agent_model(),
        fallback_chat=local_chat_model(),
        store=store,
    )
    app.ingest(load_documents())
    chosen = random.Random(5).sample(dev_questions(), args.n)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as f:
        for n, r in enumerate(chosen, 1):
            reply = app.ask(r["question"], user_id="batch5", thread_id=f"b5-{n:02d}")
            passages = [
                {"n": i + 1, "doc_id": s.doc_id, "text": s.text}
                for i, s in enumerate(reply.sources)
            ]
            row = {
                "id": f"a{n:02d}",
                "question": r["question"],
                "answer": reply.answer,
                "passages": passages,
                "stopped": reply.stopped,
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(
                row["id"], len(passages), "passages,", "error" if reply.error else "ok"
            )


if __name__ == "__main__":
    main()
