"""The vector index: Chroma, cosine distance, in memory. The embeddings are computed by the caller."""

from __future__ import annotations

import uuid

import chromadb

from milo.chunk import Chunk


class Index:
    def __init__(self, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        if len(chunks) != len(vectors):
            raise ValueError("one vector per chunk")
        client = chromadb.EphemeralClient()
        self._col = client.create_collection(
            name=f"kb-{uuid.uuid4().hex}", metadata={"hnsw:space": "cosine"}
        )
        self._col.add(
            ids=[c.chunk_id for c in chunks],
            embeddings=vectors,
            documents=[c.text for c in chunks],
            metadatas=[
                {"doc_id": c.doc_id, "section": c.section, "product": c.product}
                for c in chunks
            ],
        )

    def search(self, vector: list[float], k: int) -> list[tuple[str, str, float]]:
        """Top-k as (chunk_id, text, score), best first. Score = 1 - cosine distance."""
        res = self._col.query(query_embeddings=[vector], n_results=k)
        ids, docs, dists = res["ids"][0], res["documents"][0], res["distances"][0]
        return [(i, d, 1.0 - dist) for i, d, dist in zip(ids, docs, dists)]
