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
from milo.shell import FAVICON, SHELL_CSS, brand_html, nav_html

REASONS = ("wrong", "outdated", "missing_source", "hard_to_follow")


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

    def chat_page(active: str) -> str:
        return (
            PAGE.replace("<!--BRAND-->", brand_html("/"))
            .replace("<!--NAV-->", nav_html(active))
            .replace("<!--FAVICON-->", FAVICON)
            .replace("<style>", "<style>" + SHELL_CSS, 1)
        )

    @web.get("/chat")
    def chat() -> Response:
        if request.args.get("new"):
            # a fresh conversation for the same owner
            session["thread"] = uuid.uuid4().hex
        owner()
        return Response(chat_page("chat"), mimetype="text/html")

    @web.get("/")
    def index() -> Response:
        from milo.landing import landing_page

        return Response(landing_page(), mimetype="text/html")

    @web.get("/api/flows")
    def flows() -> Any:
        from milo.flows import read_flows, summarize

        rows = read_flows(milo_app.trace_path, owner())
        return jsonify({"flows": rows, "summary": summarize(rows)})

    @web.get("/dashboard")
    def dashboard() -> Response:
        page = (
            DASHBOARD.replace("<!--BRAND-->", brand_html("/"))
            .replace("<!--NAV-->", nav_html("overview"))
            .replace("<!--FAVICON-->", FAVICON)
            .replace("<style>", "<style>" + SHELL_CSS, 1)
        )
        return Response(page, mimetype="text/html")

    @web.post("/api/feedback")
    def feedback() -> Any:
        """One thumbs vote on an answer. Stores the rating, a reason from a fixed list and a hashed owner. No text."""
        from milo.flows import owner_hash

        body = request.get_json(silent=True) or {}
        rating = body.get("rating")
        reason = body.get("reason", "")
        if rating not in ("up", "down"):
            return jsonify(
                {"ok": False, "error": "invalid_input: rating must be up or down"}
            ), 400
        if reason and reason not in REASONS:
            return jsonify({"ok": False, "error": "invalid_input: unknown reason"}), 400
        if milo_app.trace_path is None:
            return jsonify(
                {"ok": False, "error": "feedback is not stored in this run"}
            ), 503
        from datetime import datetime

        record = {
            "ts": datetime.now().isoformat(timespec="seconds"),
            "owner": owner_hash(owner()),
            "rating": rating,
            "reason": reason,
        }
        path = milo_app.trace_path.parent / "feedback.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a") as f:
            f.write(json.dumps(record) + "\n")
        return jsonify({"ok": True})

    @web.get("/kb")
    def kb_index() -> Response:
        from milo.kb_pages import index_page

        return Response(index_page(), mimetype="text/html")

    @web.get("/kb/<path:doc_id>")
    def kb_document(doc_id: str) -> Any:
        from milo.kb_pages import document_page

        page = document_page(doc_id)
        if page is None:
            return Response("Document not found", status=404, mimetype="text/plain")
        return Response(page, mimetype="text/html")

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
