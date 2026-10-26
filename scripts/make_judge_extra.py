"""Second batch of judge items: owner-story headlines S11 to S20 (demo data), answered by the live app.

Writes evals/judge/answers_extra.json and evals/judge/sheet_extra.md, and an empty labels_extra.csv for labelling.
Run: MILO_LIVE=1 uv run python scripts/make_judge_extra.py   (paid, small)
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from milo.app import App
from milo.embed import OpenRouterEmbedder
from milo.llm import live_chat_model
from milo.serve import load_documents
from milo.store import MemoryStore
from milo.tools import Backend

OUT = ROOT / "evals" / "judge"
STORIES = ROOT / "data" / "stories" / "owner_stories.md"


def main() -> None:
    if os.environ.get("MILO_LIVE") != "1":
        raise SystemExit("this script makes paid calls: set MILO_LIVE=1")
    heads = re.findall(r'^## (S\d{2})\. "(.+?)"', STORIES.read_text(), re.MULTILINE)[
        10:20
    ]
    store = MemoryStore()
    app = App(
        live_chat_model(), OpenRouterEmbedder(0.05), Backend(store=store), store=store
    )
    app.ingest(load_documents())
    results = []
    for sid, q in heads:
        r = app.ask(q, f"judge-{sid}", "judge-extra")
        results.append(
            {
                "id": sid,
                "question": q,
                "kind": "owner story",
                "answer": r.answer,
                "error": r.error,
                "passages": [
                    {"doc_id": s.doc_id, "chunk_id": s.chunk_id, "text": s.text}
                    for s in r.sources
                ],
                "tools": [t.name for t in r.tool_results],
            }
        )
    (OUT / "answers_extra.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    lines = [
        "# Judge labelling sheet, second batch (10 items)",
        "",
        "Read each question, answer and full passage set. Label faithful (1 if every claim is supported) and relevant (1 if the answer addresses the question).",
        "",
    ]
    for n, r in enumerate(results, 1):
        lines += [
            f"## {n}. {r['id']}",
            f"**Question:** {r['question']}",
            "",
            f"**Answer:** {r['answer']}",
            "",
        ]
        lines += [
            f"- passage `{p['chunk_id']}`: {p['text']}" for p in r["passages"]
        ] or ["- (no passage was retrieved)"]
        lines.append("")
    (OUT / "sheet_extra.md").write_text("\n".join(lines))
    (OUT / "labels_extra.csv").write_text(
        "id,faithful,relevant,notes\n" + "".join(f"{r['id']},,,\n" for r in results)
    )
    print(f"wrote {len(results)} items")


if __name__ == "__main__":
    main()
