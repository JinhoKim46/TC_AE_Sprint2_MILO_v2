"""Embedders: the same interface for an offline baseline and for the chosen live model.

- `LexicalEmbedder` is deterministic and needs no network. It is a baseline for tests and for the offline replay, not the
  model the project chose. It hashes words and word pairs into a fixed vector and normalises it.
- `OpenRouterEmbedder` calls `google/gemini-embedding-2` through OpenRouter. It refuses to run unless `MILO_LIVE=1`, a key is
  set, and the estimated cost is under the cap. Building it sends nothing; the first `embed` call does.
"""

from __future__ import annotations

import itertools
import math
import os
import re
import zlib
from typing import Protocol

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
EMBED_MODEL = "google/gemini-embedding-2"
EMBED_PRICE_USD_PER_TOKEN = (
    2e-7  # listed price, from the earlier project's comparison (2026-10-22)
)
DIM = 512
TOKEN = re.compile(r"[a-z0-9]+")


class Embedder(Protocol):
    name: str

    def embed(self, texts: list[str]) -> list[list[float]]: ...


class LexicalEmbedder:
    """Hashed unigrams and bigrams, L2-normalised. Deterministic across runs (zlib.crc32, not hash())."""

    name = "lexical-hash-512"

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._one(t) for t in texts]

    def _one(self, text: str) -> list[float]:
        words = TOKEN.findall(text.lower())
        grams = words + [f"{a} {b}" for a, b in itertools.pairwise(words)]
        vec = [0.0] * DIM
        for g in grams:
            vec[zlib.crc32(g.encode()) % DIM] += 1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]


class OpenRouterEmbedder:
    name = EMBED_MODEL

    def __init__(self, max_cost_usd: float) -> None:
        if os.environ.get("MILO_LIVE") != "1":
            raise PermissionError("a live embedding needs MILO_LIVE=1 (paid call)")
        key = os.environ.get("OPENROUTER_API_KEY", "")
        if not key:
            raise PermissionError("OPENROUTER_API_KEY is not set")
        self.max_cost_usd = max_cost_usd
        self.spent_usd = 0.0
        from langchain_openai import OpenAIEmbeddings

        self._client = OpenAIEmbeddings(
            model=EMBED_MODEL,
            api_key=key,
            base_url=OPENROUTER_BASE_URL,
            check_embedding_ctx_length=False,
        )

    def embed(self, texts: list[str]) -> list[list[float]]:
        est = (
            sum(len(t) for t in texts) / 4 * EMBED_PRICE_USD_PER_TOKEN
        )  # about 4 characters per token
        if self.spent_usd + est > self.max_cost_usd:
            raise RuntimeError(
                f"estimated cost {est:.6f} USD would exceed the cap {self.max_cost_usd} USD"
            )
        vectors = self._client.embed_documents(texts)
        self.spent_usd += est
        return vectors
