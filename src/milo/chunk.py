"""Heading-aware chunking of the knowledge-base articles.

Rules (written down because M1 asks for the choice and its evidence):
- Front matter is metadata, not text. Each chunk keeps its doc_id, title, section and product.
- A chunk never crosses a heading: each heading starts a new chunk.
- Paragraphs are packed into chunks of at most `size` characters. A paragraph that fits is never cut, so a gold quote
  inside one paragraph lands whole in one chunk.
- A paragraph longer than `size` is cut at sentence ends where possible, with `overlap` characters repeated.

The earlier project chose 800 characters with 100 overlap on the same kind of articles (see
sprint2/project/docs/rag-parameters.md). M0b's articles are shorter than 800 characters per section, so one section is
usually one chunk.
"""

from __future__ import annotations

import itertools
import re
from dataclasses import dataclass

SIZE = 800
OVERLAP = 100
FRONT = re.compile(r"\A---\n(.*?)\n---\n(.*)", re.DOTALL)
HEADING = re.compile(r"^#{1,6} ", re.MULTILINE)


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    section: str
    product: str
    text: str


def front_matter(raw: str) -> tuple[dict[str, str], str]:
    m = FRONT.match(raw)
    if not m:
        raise ValueError("article has no front matter")
    meta = dict(line.split(": ", 1) for line in m.group(1).splitlines() if ": " in line)
    return meta, m.group(2)


def _sections(body: str) -> list[str]:
    starts = [m.start() for m in HEADING.finditer(body)]
    if not starts or starts[0] != 0:
        starts = [0, *starts]
    bounds = [*starts, len(body)]
    return [
        body[a:b].strip() for a, b in itertools.pairwise(bounds) if body[a:b].strip()
    ]


def _cut(paragraph: str, size: int, overlap: int) -> list[str]:
    """Cut one long paragraph at sentence ends, repeating `overlap` characters between pieces."""
    sentences = re.split(r"(?<=[.!?])\s+", paragraph)
    pieces: list[str] = []
    current = ""
    for s in sentences:
        if len(s) > size:  # one sentence longer than the window: hard cut
            for i in range(0, len(s), size - overlap):
                pieces.append(s[i : i + size])
            continue
        if current and len(current) + 1 + len(s) > size:
            pieces.append(current)
            current = current[-overlap:] + " " + s if overlap else s
        else:
            current = f"{current} {s}".strip()
    if current:
        pieces.append(current)
    return pieces


def chunk_section(section: str, size: int = SIZE, overlap: int = OVERLAP) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", section) if p.strip()]
    out: list[str] = []
    current = ""
    for p in paragraphs:
        if len(p) > size:
            if current:
                out.append(current)
                current = ""
            out.extend(_cut(p, size, overlap))
            continue
        if current and len(current) + 2 + len(p) > size:
            out.append(current)
            current = p
        else:
            current = f"{current}\n\n{p}" if current else p
    if current:
        out.append(current)
    return out


def chunk_article(
    doc_id: str, raw: str, size: int = SIZE, overlap: int = OVERLAP
) -> list[Chunk]:
    meta, body = front_matter(raw)
    return chunk_body(doc_id, body, meta, size, overlap)


def chunk_body(
    doc_id: str,
    body: str,
    meta: dict[str, str],
    size: int = SIZE,
    overlap: int = OVERLAP,
) -> list[Chunk]:
    chunks: list[Chunk] = []
    for section in _sections(body):
        for text in chunk_section(section, size, overlap):
            chunks.append(
                Chunk(
                    chunk_id=f"{doc_id}#{len(chunks):03d}",
                    doc_id=doc_id,
                    title=meta.get("title", ""),
                    section=meta.get("section", ""),
                    product=meta.get("product", ""),
                    text=text,
                )
            )
    return chunks
