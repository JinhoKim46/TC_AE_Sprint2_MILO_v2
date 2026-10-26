"""Turns the trace file into per-request flows and an overview. Reads only; nothing here calls a model or a database.

A flow is one question and its steps: history read, retrieval, each model call, each tool call, and the answer.
The overview counts across one owner's flows: questions, errors, latency, cost, tool use, and table access.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


def owner_hash(owner_id: str) -> str:
    return hashlib.sha256(owner_id.encode()).hexdigest()[:12]


def read_flows(
    trace_path: Path | None, owner_id: str, limit: int = 50
) -> list[dict[str, Any]]:
    """This owner's most recent flows, newest first. Other owners' lines are skipped."""
    if trace_path is None or not trace_path.exists():
        return []
    me = owner_hash(owner_id)
    rows = []
    for line in trace_path.read_text().splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if record.get("owner") == me:
            rows.append(record)
    return rows[-limit:][::-1]


def summarize(flows: list[dict[str, Any]]) -> dict[str, Any]:
    tools: Counter[str] = Counter()
    decisions: Counter[str] = Counter()
    tables: Counter[str] = Counter()
    models: Counter[str] = Counter()
    scores: list[float] = []
    latencies: list[float] = []
    errors = 0
    cost = 0.0
    tokens_in = tokens_out = 0
    for f in flows:
        latencies.append(float(f.get("total_ms", 0)))
        cost += float(f.get("cost_usd", 0) or 0)
        if f.get("error"):
            errors += 1
        for step in f.get("steps", []):
            kind = step.get("step")
            if kind == "tool":
                tools[step["name"]] += 1
                decisions[step.get("decision", "")] += 1
                if step.get("table", "none") != "none":
                    tables[step["table"]] += 1
            elif kind == "model":
                models[step.get("model", "unknown")] += 1
                tokens_in += int(step.get("input_tokens", 0) or 0)
                tokens_out += int(step.get("output_tokens", 0) or 0)
            elif kind == "retrieve":
                scores.extend(float(h["score"]) for h in step.get("hits", []))
                if step.get("table"):
                    tables[step["table"]] += 1
            elif kind == "history_read":
                tables["turns (read)"] += 1
    n = len(flows)
    return {
        "questions": n,
        "errors": errors,
        "error_rate": round(errors / n, 3) if n else 0.0,
        "avg_total_ms": round(sum(latencies) / n, 1) if n else 0.0,
        "cost_usd": round(cost, 6),
        "tokens": {"input": tokens_in, "output": tokens_out},
        "model_calls": dict(models),
        "tool_calls": dict(tools),
        "tool_decisions": dict(decisions),
        "table_access": dict(tables),
        "avg_top_score": round(sum(scores) / len(scores), 3) if scores else None,
    }
