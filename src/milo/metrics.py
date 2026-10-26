"""Retrieval metrics on one query at a time, with bootstrap confidence intervals over queries.

Each query has one gold quote. `rank` is the 1-based position of the first retrieved chunk that contains the quote,
or None when no chunk in the top k does.
"""

from __future__ import annotations

import math
import random


def recall_at_k(rank: int | None, k: int = 5) -> float:
    return 1.0 if rank is not None and rank <= k else 0.0


def ndcg_at_k(rank: int | None, k: int = 5) -> float:
    """Binary relevance with one relevant chunk: DCG = 1 / log2(rank + 1); ideal DCG = 1."""
    if rank is None or rank > k:
        return 0.0
    return 1.0 / math.log2(rank + 1)


def mean_ci(
    values: list[float], n_boot: int = 2000, seed: int = 0
) -> tuple[float, float, float]:
    """Mean with a percentile bootstrap 95% interval. Deterministic for a given seed."""
    if not values:
        return (math.nan, math.nan, math.nan)
    rng = random.Random(seed)
    n = len(values)
    means = sorted(
        sum(values[rng.randrange(n)] for _ in range(n)) / n for _ in range(n_boot)
    )
    lo, hi = means[int(0.025 * n_boot)], means[int(0.975 * n_boot) - 1]
    return (sum(values) / n, lo, hi)
