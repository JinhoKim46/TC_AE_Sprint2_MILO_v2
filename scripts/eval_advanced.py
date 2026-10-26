"""M2 A/B on the dev gold set, against the M1 baseline. Paired by question.

Arms (all use the offline lexical embedder, so no key is needed):
  baseline   the question as asked (M1)
  translate  the keyword translation of the question
  selfquery  the question, filtered by the validated self-query (falls back to no filter when invalid).
             Revision 2: a case id (C04) maps to its article's area. Revision 1 used area words only and filtered
             2 of 16 dev questions; the change was made after looking at dev, so the dev A/B is not held out.
  both       translation plus the self-query filter

Decision rule, fixed before the run: an arm is ADOPTED when the paired 95% bootstrap interval of its nDCG@5 difference
from the baseline lies entirely above zero; otherwise it is REJECTED. Replay recomputes everything from stored ranks.
Run:     uv run python scripts/eval_advanced.py
Replay:  uv run python scripts/eval_advanced.py --replay evals/results/advanced/dev_ab.json
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from eval_retrieval import K, dev_rows, load_chunks, norm

from milo.advanced import self_query, translate_keywords
from milo.embed import LexicalEmbedder
from milo.index import Index
from milo.metrics import ndcg_at_k

RESULTS = ROOT / "evals" / "results" / "advanced" / "dev_ab.json"
ARMS = ["baseline", "translate", "selfquery", "both"]


def paired_ci(
    diffs: list[float], n_boot: int = 2000, seed: int = 0
) -> tuple[float, float, float]:
    rng = random.Random(seed)
    n = len(diffs)
    means = sorted(
        sum(diffs[rng.randrange(n)] for _ in range(n)) / n for _ in range(n_boot)
    )
    return (sum(diffs) / n, means[int(0.025 * n_boot)], means[int(0.975 * n_boot) - 1])


def decide(diffs: list[float]) -> str:
    _, lo, _ = paired_ci(diffs)
    return "ADOPTED" if lo > 0 else "REJECTED"


def run() -> dict:
    embedder = LexicalEmbedder()
    chunks = load_chunks()
    index = Index(chunks, embedder.embed([c.text for c in chunks]))
    rows = dev_rows()
    case_products = {
        doc.rsplit("/", 1)[1].upper(): meta
        for doc, meta in (
            (c.doc_id, c.product) for c in chunks if c.doc_id.startswith("cases/")
        )
    }
    per_arm: dict[str, list[float]] = {a: [] for a in ARMS}
    filter_used = 0
    for r in rows:
        quotes = [norm(e["quote"]) for e in r["gold_evidence"]]
        flt = self_query(r["question"], case_products)
        filter_used += bool(flt)
        queries = {
            "baseline": (r["question"], None),
            "translate": (translate_keywords(r["question"]), None),
            "selfquery": (r["question"], flt),
            "both": (translate_keywords(r["question"]), flt),
        }
        for arm, (text, where) in queries.items():
            hits = index.search(embedder.embed([text])[0], K, where=where)
            if where and not hits:  # the fallback: unfiltered search
                hits = index.search(embedder.embed([text])[0], K)
            rank = next(
                (
                    p
                    for p, (_, t, _) in enumerate(hits, 1)
                    if any(q in norm(t) for q in quotes)
                ),
                None,
            )
            per_arm[arm].append(ndcg_at_k(rank, K))
    base = per_arm["baseline"]
    summary = {}
    for arm in ARMS:
        mean = sum(per_arm[arm]) / len(per_arm[arm])
        if arm == "baseline":
            summary[arm] = {"ndcg5": round(mean, 4)}
            continue
        diffs = [a - b for a, b in zip(per_arm[arm], base)]
        m, lo, hi = paired_ci(diffs)
        summary[arm] = {
            "ndcg5": round(mean, 4),
            "diff_vs_baseline": {
                "mean": round(m, 4),
                "ci": [round(lo, 4), round(hi, 4)],
            },
            "decision": decide(diffs),
        }
    return {
        "embedder": embedder.name,
        "split": "dev",
        "n_questions": len(rows),
        "self_query_filter_used_on": filter_used,
        "self_query_revision": 2,
        "rule": "adopt when the paired 95% CI of the nDCG@5 difference lies above zero",
        "summary": summary,
        "per_question": {a: per_arm[a] for a in ARMS},
    }


def replay(path: Path) -> None:
    stored = json.loads(path.read_text())
    recomputed = {}
    for arm in ARMS:
        vals = stored["per_question"][arm]
        recomputed[arm] = round(sum(vals) / len(vals), 4)
    ok = all(stored["summary"][a]["ndcg5"] == recomputed[a] for a in ARMS)
    for arm in ARMS[1:]:
        diffs = [
            a - b
            for a, b in zip(
                stored["per_question"][arm], stored["per_question"]["baseline"]
            )
        ]
        ok = ok and stored["summary"][arm]["decision"] == decide(diffs)
    print(
        f"replay {path.name}: {'OK, identical to stored results' if ok else 'MISMATCH'}"
    )
    for arm in ARMS:
        print(f"  {arm:<10} {json.dumps(stored['summary'][arm])}")
    if not ok:
        sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--replay", type=Path)
    args = ap.parse_args()
    if args.replay:
        replay(args.replay)
        return
    result = run()
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(json.dumps(result, indent=2) + "\n")
    replay(RESULTS)


if __name__ == "__main__":
    main()
