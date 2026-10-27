"""M1 retrieval baseline on the dev gold set.

Live run (embeds the knowledge base and the questions with the chosen model; paid, capped):
    MILO_LIVE=1 uv run python scripts/eval_retrieval.py --embedder gemini --max-cost 0.02
Offline run (no network, free; the lexical baseline):
    uv run python scripts/eval_retrieval.py --embedder lexical
Replay (recomputes every metric from the stored ranks; no model call):
    uv run python scripts/eval_retrieval.py --replay evals/results/retrieval/<name>.json

Each stored row keeps the rank of the first top-5 chunk that contains the gold quote, so the replay is exact.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from milo.chunk import chunk_article
from milo.embed import LexicalEmbedder, OpenRouterEmbedder
from milo.index import Index
from milo.metrics import mean_ci, ndcg_at_k, recall_at_k

K = 5
KB = ROOT / "data" / "kb"
GOLD = ROOT / "data" / "gold.jsonl"
GOLD_EXTRA = (
    ROOT / "data" / "gold_dev_extra.jsonl"
)  # 40 more dev items, kept apart so the dev/test counts stay balanced
RESULTS = ROOT / "evals" / "results" / "retrieval"


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().casefold()


def load_chunks():
    chunks = []
    for p in sorted(KB.rglob("*.md")):
        doc_id = p.relative_to(KB).with_suffix("").as_posix()
        chunks.extend(chunk_article(doc_id, p.read_text()))
    return chunks


ACCESS_LOG = ROOT / "evals" / "results" / "test_access.log"


HELDOUT = (
    ROOT / "data" / "gold_heldout.jsonl"
)  # a fresh set, written after the dev and test sets; read once
HELDOUT_LOG = ROOT / "evals" / "results" / "retrieval" / "heldout_access.log"


def read_heldout_once() -> list[dict]:
    """The held-out rows. Read once: the read is logged, and a second read is refused."""
    reads = (
        HELDOUT_LOG.read_text().count("read heldout split")
        if HELDOUT_LOG.exists()
        else 0
    )
    if reads >= 1 and os.environ.get("MILO_HELDOUT_REREAD") != "1":
        raise SystemExit(
            "the held-out split was already read once; see " + str(HELDOUT_LOG)
        )
    HELDOUT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with HELDOUT_LOG.open("a") as f:
        f.write(
            f"read heldout split by eval_retrieval at {datetime.now().isoformat(timespec='seconds')}\n"
        )
    return [json.loads(x) for x in HELDOUT.read_text().splitlines() if x.strip()]


def split_rows(split: str) -> list[dict]:
    """The rows of one split. The test split is read once: every read is logged, and a second read is refused."""
    if split == "test":
        reads = (
            ACCESS_LOG.read_text().count("read test split")
            if ACCESS_LOG.exists()
            else 0
        )
        if reads >= 1 and os.environ.get("MILO_TEST_REREAD") != "1":
            raise SystemExit(
                "the test split was already read once; see evals/results/test_access.log"
            )
        ACCESS_LOG.parent.mkdir(parents=True, exist_ok=True)
        with ACCESS_LOG.open("a") as f:
            f.write(
                f"read test split by eval_retrieval at {datetime.now().isoformat(timespec='seconds')}\n"
            )
    rows = [
        json.loads(x)
        for f in (GOLD, GOLD_EXTRA)
        for x in f.read_text().splitlines()
        if x.strip()
    ]
    return [r for r in rows if r["split"] == split and r["gold_evidence"]]


def dev_rows() -> list[dict]:
    return split_rows("dev")


def metrics(rows: list[dict]) -> dict:
    out = {}
    for kind in sorted({r["type"] for r in rows}) + ["all"]:
        subset = rows if kind == "all" else [r for r in rows if r["type"] == kind]
        ranks = [r["rank"] for r in subset]
        out[kind] = {"n": len(subset)}
        for name, fn in (("recall5", recall_at_k), ("ndcg5", ndcg_at_k)):
            mean, lo, hi = mean_ci([fn(rank, K) for rank in ranks])
            out[kind][name] = {
                "mean": round(mean, 4),
                "ci": [round(lo, 4), round(hi, 4)],
            }
    return out


def run(embedder_name: str, max_cost: float, split: str = "dev") -> dict:
    embedder = (
        OpenRouterEmbedder(max_cost) if embedder_name == "gemini" else LexicalEmbedder()
    )
    chunks = load_chunks()
    index = Index(chunks, embedder.embed([c.text for c in chunks]))
    rows = split_rows(split)
    vectors = embedder.embed([r["question"] for r in rows])
    stored = []
    unlanded = 0
    for r, vec in zip(rows, vectors):
        quotes = [norm(e["quote"]) for e in r["gold_evidence"]]
        hits = index.search(vec, K)
        rank = None
        for pos, (_, text, _) in enumerate(hits, start=1):
            if any(q in norm(text) for q in quotes):
                rank = pos
                break
        if not any(q in norm(c.text) for c in chunks for q in quotes):
            unlanded += 1  # the gold quote never sits whole in one chunk: a chunking problem, reported
        stored.append(
            {
                "qid": r["qid"],
                "type": r["type"],
                "rank": rank,
                "top5": [h[0] for h in hits],
            }
        )
    return {
        "embedder": embedder.name,
        "chunk_size": 800,
        "overlap": 100,
        "top_k": K,
        "split": split,
        "chunk_count": len(chunks),
        "quotes_not_whole_in_a_chunk": unlanded,
        "metrics": metrics(stored),
        "rows": stored,
    }


def replay(path: Path) -> None:
    stored = json.loads(path.read_text())
    recomputed = metrics(stored["rows"])
    ok = recomputed == stored["metrics"]
    print(
        f"replay {path.name}: {'OK, identical to stored metrics' if ok else 'MISMATCH'}"
    )
    for kind, m in recomputed.items():
        r5, n5 = m["recall5"], m["ndcg5"]
        print(
            f"  {kind:<12} n={m['n']:<3} recall@5 {r5['mean']:.3f} {r5['ci']}  nDCG@5 {n5['mean']:.3f} {n5['ci']}"
        )
    if not ok:
        sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--embedder", choices=["lexical", "gemini"], default="lexical")
    ap.add_argument("--max-cost", type=float, default=0.02)
    ap.add_argument("--replay", type=Path)
    ap.add_argument("--split", choices=["dev", "test"], default="dev")
    args = ap.parse_args()
    if args.replay:
        replay(args.replay)
        return
    result = run(args.embedder, args.max_cost, args.split)
    RESULTS.mkdir(parents=True, exist_ok=True)
    name = f"{args.split}_{args.embedder}.json"
    (RESULTS / name).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(
        f"wrote {RESULTS / name}: {result['chunk_count']} chunks, {result['quotes_not_whole_in_a_chunk']} quotes split"
    )
    replay(RESULTS / name)


if __name__ == "__main__":
    main()
