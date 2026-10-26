"""System status for the owner's monitor: database, models and spend. Reads only; never prints a secret."""

from __future__ import annotations

import os
import time
from typing import Any

import httpx


def _ping_database(url: str) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        import psycopg

        with psycopg.connect(url, connect_timeout=5) as conn, conn.cursor() as cur:
            counts = {}
            for table in ("threads", "turns", "facts", "diagnoses", "flows", "users"):
                cur.execute(f"select count(*) from milo_v2.{table}")
                counts[table] = cur.fetchone()[0]
        return {
            "reachable": True,
            "latency_ms": round((time.perf_counter() - started) * 1000),
            "threads": counts["threads"],
            "turns": counts["turns"],
            "facts": counts["facts"],
            "diagnoses": counts["diagnoses"],
            "flows": counts["flows"],
            "accounts": counts["users"],
        }
    except Exception as e:  # noqa: BLE001 - a status page must report failure, not crash
        return {"reachable": False, "error": type(e).__name__}


def _ping_local_model() -> dict[str, Any]:
    try:
        r = httpx.get("http://localhost:11434/api/tags", timeout=3)
        names = [m["name"] for m in r.json().get("models", [])]
        return {"reachable": True, "models": names}
    except Exception as e:  # noqa: BLE001
        return {"reachable": False, "error": type(e).__name__}


def snapshot(
    store_kind: str,
    database_url: str | None,
    flows: list[dict[str, Any]],
    chat_model: str,
) -> dict[str, Any]:
    spend = round(sum(float(f.get("cost_usd", 0) or 0) for f in flows), 6)
    key_set = bool(os.environ.get("OPENROUTER_API_KEY", "").strip())
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
                "key_set": key_set,
                "live_enabled": os.environ.get("MILO_LIVE") == "1",
            },
            "fallback": _ping_local_model(),
        },
        "spend": {
            "web_answers": len(flows),
            "web_cost_usd": spend,
            "course_cap_usd": 3.00,
            "note": "Counts every answer made in the web app, for all accounts. Evaluation runs are logged in their own result files.",
        },
    }
