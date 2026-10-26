"""Hybrid retrieval against dense-only on the held-out set, read once.

Dense: the live embeddings (OpenRouter) through milo.index. Sparse: BM25 over the same chunks, written here so no
extra dependency is needed. Hybrid: reciprocal rank fusion of the two rankings (k = 60). The comparison is paired: the
same questions, and a bootstrap interval on the per-question nDCG@5 difference (hybrid minus dense).

Live (embeds the chunks and the questions; small cost): MILO_LIVE=1 uv run python scripts/eval_hybrid.py --max-cost 0.05
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from eval_retrieval import RESULTS, K, load_chunks, norm, read_heldout_once

from milo.embed import OpenRouterEmbedder
from milo.index import Index
from milo.metrics import mean_ci, ndcg_at_k

RRF_K = 60
POOL = 50  # how far down each ranking the fusion looks


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


class BM25:
    def __init__(self, texts: list[str], k1: float = 1.5, b: float = 0.75) -> None:
        self.docs = [tokens(t) for t in texts]
        self.k1, self.b = k1, b
        self.avg = sum(len(d) for d in self.docs) / max(len(self.docs), 1)
        self.df: dict[str, int] = {}
        for d in self.docs:
            for w in set(d):
                self.df[w] = self.df.get(w, 0) + 1
        self.n = len(self.docs)

    def ranking(self, query: str) -> list[int]:
        q = tokens(query)
        scores = []
        for i, d in enumerate(self.docs):
            tf: dict[str, int] = {}
            for w in d:
                tf[w] = tf.get(w, 0) + 1
            s = 0.0
            for w in set(q):
                if w not in tf:
                    continue
                idf = math.log(1 + (self.n - self.df[w] + 0.5) / (self.df[w] + 0.5))
                s += (
                    idf
                    * tf[w]
                    * (self.k1 + 1)
                    / (tf[w] + self.k1 * (1 - self.b + self.b * len(d) / self.avg))
                )
            scores.append(s)
        return sorted(range(self.n), key=lambda i: -scores[i])


def fuse(*rankings: list[int]) -> list[int]:
    score: dict[int, float] = {}
    for ranking in rankings:
        for pos, idx in enumerate(ranking[:POOL], start=1):
            score[idx] = score.get(idx, 0.0) + 1.0 / (RRF_K + pos)
    return sorted(score, key=lambda i: -score[i])


def rank_of_gold(order: list[int], chunks, quotes: list[str]) -> int | None:
    for pos, idx in enumerate(order[:K], start=1):
        if any(q in norm(chunks[idx].text) for q in quotes):
            return pos
    return None


def paired_ci(
    a: list[float], b: list[float], n_boot: int = 2000, seed: int = 0
) -> tuple[float, float, float]:
    diff = [x - y for x, y in zip(a, b)]
    rng = random.Random(seed)
    stats = sorted(
        sum(rng.choice(diff) for _ in diff) / len(diff) for _ in range(n_boot)
    )
    return (
        sum(diff) / len(diff),
        stats[int(0.025 * n_boot)],
        stats[int(0.975 * n_boot) - 1],
    )


def live(max_cost: float) -> None:
    if os.environ.get("MILO_LIVE") != "1":
        raise SystemExit("needs MILO_LIVE=1 (the embeddings are paid)")
    rows = [r for r in read_heldout_once() if r["gold_evidence"]]
    chunks = load_chunks()
    embedder = OpenRouterEmbedder(max_cost)
    index = Index(chunks, embedder.embed([c.text for c in chunks]))
    qvecs = embedder.embed([r["question"] for r in rows])
    bm25 = BM25([c.text for c in chunks])
    per = {"dense": [], "bm25": [], "hybrid": []}
    out_rows = []
    for r, qv in zip(rows, qvecs):
        quotes = [norm(e["quote"]) for e in r["gold_evidence"]]
        hits = index.search(qv, len(chunks))
        ids = [h[0] for h in hits]
        pos_of = {c.chunk_id: i for i, c in enumerate(chunks)}
        dense_order = [pos_of[cid] for cid in ids]
        sparse_order = bm25.ranking(r["question"])
        hybrid_order = fuse(dense_order, sparse_order)
        row = {"qid": r["qid"], "type": r["type"]}
        for name, order in (
            ("dense", dense_order),
            ("bm25", sparse_order),
            ("hybrid", hybrid_order),
        ):
            rank = rank_of_gold(order, chunks, quotes)
            row[name] = rank
            per[name].append(ndcg_at_k(rank, K) if rank else 0.0)
        out_rows.append(row)
    summary = {}
    for name, scores in per.items():
        recalls = [1.0 if r[name] else 0.0 for r in out_rows]
        mean, lo, hi = mean_ci(recalls)
        summary[name] = {
            "recall5": round(mean, 4),
            "recall5_ci": [round(lo, 4), round(hi, 4)],
            "ndcg5": round(sum(scores) / len(scores), 4),
        }
    diff, dlo, dhi = paired_ci(per["hybrid"], per["dense"])
    result = {
        "split": "heldout",
        "n": len(rows),
        "summary": summary,
        "hybrid_minus_dense_ndcg5": {
            "mean": round(diff, 4),
            "ci": [round(dlo, 4), round(dhi, 4)],
        },
        "decision": "adopt hybrid"
        if dlo > 0
        else ("reject hybrid" if dhi < 0 else "no decision: the interval contains 0"),
        "rrf_k": RRF_K,
        "pool": POOL,
        "rows": out_rows,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "heldout_hybrid.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {k: v for k, v in result.items() if k != "rows"},
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cost", type=float, default=0.05)
    args = ap.parse_args()
    live(args.max_cost)
