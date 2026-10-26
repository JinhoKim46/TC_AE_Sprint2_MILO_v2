"""LLM judge for faithfulness and relevance, calibrated against the hand labels in evals/judge/labels.csv.

Decision rule, fixed in issue #11 before this run: the judge is usable for faithfulness only if Cohen's kappa against the
hand labels is at least 0.60 AND the lower end of its 95% bootstrap interval is at least 0.30. Relevance has no variation
in the labels (all 1), so kappa is undefined; only raw agreement is reported for it.

Run (paid, about 0.05 USD): MILO_LIVE=1 uv run python scripts/run_judge.py
Replay (no model call):     uv run python scripts/run_judge.py --replay
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

OUT = ROOT / "evals" / "judge"
PROMPT = (
    "You are checking an answer from a retrieval chatbot. You get a question, the answer, and the passages the answer "
    "was allowed to use.\n\n"
    "faithful = 1 only if every factual claim in the answer is supported by the passages. A claim that goes beyond the "
    "passages, or says a passage states something it does not, makes faithful = 0. Cautious statements such as 'the "
    "passages do not say' are fine.\n"
    "relevant = 1 if the answer addresses the question asked, even if it is incomplete.\n\n"
    'Reply with JSON only: {"faithful": 0 or 1, "relevant": 0 or 1}\n\n'
    "Question: QQQ\n\nAnswer: AAA\n\nPassages:\nPPP\n"
)


def kappa(a: list[int], b: list[int]) -> float:
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pa1, pb1 = sum(a) / n, sum(b) / n
    pe = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def bootstrap(
    a: list[int], b: list[int], n_boot: int = 2000, seed: int = 0
) -> tuple[float, float, float]:
    rng = random.Random(seed)
    idx = range(len(a))
    stats = []
    for _ in range(n_boot):
        s = [rng.choice(idx) for _ in idx]
        stats.append(kappa([a[i] for i in s], [b[i] for i in s]))
    stats.sort()
    return kappa(a, b), stats[int(0.025 * n_boot)], stats[int(0.975 * n_boot) - 1]


def parse(text: str) -> dict[str, int]:
    data = json.loads(re.search(r"\{.*\}", text, re.DOTALL).group(0))
    return {"faithful": int(data["faithful"]), "relevant": int(data["relevant"])}


def judge_all() -> dict[str, dict[str, int]]:
    from milo.llm import live_chat_model

    chat = live_chat_model()
    out = {}
    for item in json.loads((OUT / "answers.json").read_text()):
        passages = (
            "\n\n".join(
                f"[{i + 1}] {p['text']}" for i, p in enumerate(item["passages"])
            )
            or "(none)"
        )
        prompt = (
            PROMPT.replace("QQQ", item["question"])
            .replace("AAA", item["answer"])
            .replace("PPP", passages)
        )
        out[item["id"]] = parse(
            chat.invoke([{"role": "user", "content": prompt}]).content
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--replay", action="store_true")
    args = ap.parse_args()
    labels = {r["id"]: r for r in csv.DictReader((OUT / "labels.csv").open())}
    if args.replay:
        judged = json.loads((OUT / "judge_outputs.json").read_text())
    else:
        judged = judge_all()
        (OUT / "judge_outputs.json").write_text(json.dumps(judged, indent=2) + "\n")
    ids = [i for i in labels if i in judged]
    hf = [int(labels[i]["faithful"]) for i in ids]
    jf = [judged[i]["faithful"] for i in ids]
    hr = [int(labels[i]["relevant"]) for i in ids]
    jr = [judged[i]["relevant"] for i in ids]
    k, lo, hi = bootstrap(hf, jf)
    result = {
        "n": len(ids),
        "faithful": {
            "kappa": round(k, 3),
            "ci": [round(lo, 3), round(hi, 3)],
            "agreement": round(sum(x == y for x, y in zip(hf, jf)) / len(ids), 3),
            "judge_ones": sum(jf),
            "human_ones": sum(hf),
            "usable": k >= 0.60 and lo >= 0.30,
        },
        "relevant": {
            "agreement": round(sum(x == y for x, y in zip(hr, jr)) / len(ids), 3),
            "kappa": None,
            "note": "all human labels are 1, so kappa is undefined",
        },
        "rule": "usable for faithfulness only if kappa >= 0.60 and the CI lower bound >= 0.30",
        "judge_model": "anthropic/claude-haiku-5.5 (same family as the answering model)",
    }
    (OUT / "judge_result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
