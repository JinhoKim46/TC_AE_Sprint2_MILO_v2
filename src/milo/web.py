"""M6: a Flask chat page. The owner id is bound to the browser session on the server; the page never sends one.

Routes:
  GET  /           the chat page: answer, sources panel, tool-call panel with policy decision, progress, cost
  POST /api/ask    JSON in {"question": "..."}; JSON out with answer, error, sources, tool_results, cost_usd, stopped
"""

from __future__ import annotations

import json
import os
import secrets
import uuid
from dataclasses import asdict
from pathlib import Path
from typing import Any

from flask import Flask, Response, jsonify, request, session

from milo.app import App
from milo.page import DASHBOARD, PAGE


def create_app(milo_app: App, secret_key: str | None = None) -> Flask:
    web = Flask(__name__)
    web.secret_key = (
        secret_key or os.environ.get("MILO_SECRET_KEY") or secrets.token_hex(32)
    )

    def owner() -> str:
        """The owner id lives in the server-side session. The page cannot choose it."""
        if "owner" not in session:
            session["owner"] = uuid.uuid4().hex
            session["thread"] = uuid.uuid4().hex
        return session["owner"]

    @web.get("/")
    def index() -> Response:
        if request.args.get("new"):
            session["thread"] = (
                uuid.uuid4().hex
            )  # a fresh conversation for the same owner
        owner()
        return Response(PAGE, mimetype="text/html")

    @web.get("/api/flows")
    def flows() -> Any:
        from milo.flows import read_flows, summarize

        rows = read_flows(milo_app.trace_path, owner())
        return jsonify({"flows": rows, "summary": summarize(rows)})

    @web.get("/dashboard")
    def dashboard() -> Response:
        return Response(DASHBOARD, mimetype="text/html")

    @web.get("/api/status")
    def status() -> Any:
        from milo.status import snapshot

        kind = (
            "postgres" if type(milo_app.store).__name__ == "PostgresStore" else "memory"
        )
        url = os.environ.get("MILO_DATABASE_URL")
        model = os.environ.get("MILO_CHAT_MODEL", "anthropic/claude-haiku-5.5")
        return jsonify(snapshot(kind, url, milo_app.trace_path, model))

    @web.get("/api/demo")
    def demo() -> Any:
        return jsonify(
            json.loads(
                (
                    Path(__file__).resolve().parents[2]
                    / "data"
                    / "demo_storylines.json"
                ).read_text()
            )
        )

    @web.get("/api/history")
    def history() -> Any:
        owner_id = owner()
        turns = milo_app.store.history(owner_id, session["thread"], limit=40)
        return jsonify({"turns": turns})

    @web.post("/api/ask")
    def ask() -> Any:
        body = request.get_json(silent=True) or {}
        question = body.get("question", "")
        if not isinstance(question, str):
            return jsonify(
                {"answer": "", "error": "invalid_input: question must be text"}
            ), 400
        owner_id = owner()
        response = milo_app.ask(question, user_id=owner_id, thread_id=session["thread"])
        return jsonify(
            {
                "answer": response.answer,
                "error": response.error,
                "cost_usd": response.cost_usd,
                "stopped": response.stopped,
                "sources": [asdict(s) for s in response.sources],
                "tool_results": [asdict(t) for t in response.tool_results],
                "trace": response.trace,
            }
        )

    return web
