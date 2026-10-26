"""System status for the monitor: database, model configuration, stored data and spend. Reads only; never prints a secret."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any


def _ping_database(url: str) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        import psycopg

        with psycopg.connect(url, connect_timeout=5) as conn, conn.cursor() as cur:
            cur.execute("select count(*) from milo_v2.threads")
            threads = cur.fetchone()[0]
            cur.execute("select count(*) from milo_v2.turns")
            turns = cur.fetchone()[0]
            cur.execute("select count(*) from milo_v2.facts")
            facts = cur.fetchone()[0]
            cur.execute("select count(*) from milo_v2.diagnoses")
            diagnoses = cur.fetchone()[0]
        return {
            "reachable": True,
            "latency_ms": round((time.perf_counter() - started) * 1000),
            "threads": threads,
            "turns": turns,
            "facts": facts,
            "diagnoses": diagnoses,
        }
    except Exception as e:  # noqa: BLE001 - a status page must report failure, not crash
        return {"reachable": False, "error": type(e).__name__}


def _ping_local_model() -> dict[str, Any]:
    import httpx

    try:
        r = httpx.get("http://localhost:11434/api/tags", timeout=3)
        names = [m["name"] for m in r.json().get("models", [])]
        return {"reachable": True, "models": names}
    except Exception as e:  # noqa: BLE001
        return {"reachable": False, "error": type(e).__name__}


def _spend(trace_path: Path | None) -> dict[str, Any]:
    if trace_path is None or not trace_path.exists():
        return {"web_answers": 0, "web_cost_usd": 0.0}
    rows = [json.loads(x) for x in trace_path.read_text().splitlines() if x.strip()]
    return {
        "web_answers": len(rows),
        "web_cost_usd": round(sum(float(r.get("cost_usd", 0) or 0) for r in rows), 6),
    }


def snapshot(
    store_kind: str, database_url: str | None, trace_path: Path | None, chat_model: str
) -> dict[str, Any]:
    return {
        "app": {"status": "running", "time": time.strftime("%Y-%m-%d %H:%M:%S")},
        "store": {
            "kind": store_kind,
            "database": _ping_database(database_url)
            if store_kind == "postgres" and database_url
            else None,
        },
        "models": {
            "primary": {
                "model": chat_model,
                "key_set": bool(os.environ.get("OPENROUTER_API_KEY", "").strip()),
                "live_enabled": os.environ.get("MILO_LIVE") == "1",
            },
            "fallback": _ping_local_model(),
        },
        "spend": {
            **_spend(trace_path),
            "course_cap_usd": 3.00,
            "note": "Counts only answers made in the web app. Evaluation runs are logged in their own result files.",
        },
    }
