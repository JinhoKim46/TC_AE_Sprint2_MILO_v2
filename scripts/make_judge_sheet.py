"""Builds the labelling sheet for the LLM judge: 30 answers from the live app, with their passages, for hand labels.

Items: the 20 dev gold questions (16 answerable, 4 unanswerable) and the headlines of owner stories S01 to S10 (demo
data, not evaluation data). No test-split question is used.
Run: MILO_LIVE=1 uv run python scripts/make_judge_sheet.py   (about 0.05 USD, paid)
Output: evals/judge/sheet.md (for you to label) and evals/judge/answers.json (the app's outputs, for the judge later).
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


def items() -> list[dict[str, str]]:
    gold = [
        json.loads(x)
        for x in (ROOT / "data" / "gold.jsonl").read_text().splitlines()
        if x.strip()
    ]
    out = [
        {"id": r["qid"], "question": r["question"], "kind": r["type"]}
        for r in gold
        if r["split"] == "dev"
    ]
    heads = re.findall(r'^## (S\d{2})\. "(.+?)"', STORIES.read_text(), re.MULTILINE)
    out += [{"id": sid, "question": q, "kind": "owner story"} for sid, q in heads[:10]]
    return out


def main() -> None:
    if os.environ.get("MILO_LIVE") != "1":
        raise SystemExit("this script makes paid calls: set MILO_LIVE=1")
    store = MemoryStore()
    app = App(
        live_chat_model(), OpenRouterEmbedder(0.05), Backend(store=store), store=store
    )
    app.ingest(load_documents())
    results = []
    for item in items():
        r = app.ask(item["question"], f"judge-{item['id']}", "judge-sheet")
        results.append(
            {
                **item,
                "answer": r.answer,
                "error": r.error,
                "passages": [
                    {"doc_id": s.doc_id, "chunk_id": s.chunk_id, "text": s.text}
                    for s in r.sources
                ],
                "tools": [t.name for t in r.tool_results],
            }
        )
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "answers.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    lines = [
        "# Judge labelling sheet (30 items)",
        "",
        "For each item, read the question, the answer and the passages. Then fill two labels in `labels.csv` (same id):",
        "- **faithful**: 1 if every claim in the answer is supported by the passages, 0 if not.",
        "- **relevant**: 1 if the answer addresses the question, 0 if not.",
        "",
    ]
    for n, r in enumerate(results, 1):
        lines += [
            f"## {n}. {r['id']} ({r['kind']})",
            f"**Question:** {r['question']}",
            "",
            f"**Answer:** {r['answer']}",
            "",
        ]
        for p in r["passages"][:5]:
            lines.append(
                f"- passage `{p['chunk_id']}`: {p['text'][:300].replace(chr(10), ' ')}"
            )
        if not r["passages"]:
            lines.append("- (no passage was retrieved)")
        lines.append("")
    (OUT / "sheet.md").write_text("\n".join(lines))
    (OUT / "labels.csv").write_text(
        "id,faithful,relevant,notes\n" + "".join(f"{r['id']},,,\n" for r in results)
    )
    print(f"wrote {len(results)} items to {OUT}")


if __name__ == "__main__":
    main()
