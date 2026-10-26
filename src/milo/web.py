"""The MILO web app: landing page, accounts, the chat, the knowledge base, and the owner's overview.

Access rules:
- Visitors see the product page, sign-up and sign-in.
- Customers (registered with an ID and a password) use the chat and the knowledge base.
- The owner (role "admin") also sees the overview, the status and the user list.

The owner id that the chat uses is the signed-in user's id, kept in the server-side session. The page cannot choose it.
"""

from __future__ import annotations

import json
import os
import secrets
import uuid
from dataclasses import asdict
from pathlib import Path
from typing import Any

from flask import Flask, Response, jsonify, redirect, request, session, url_for

from milo.app import App
from milo.auth_pages import login_page, password_page, signup_page, users_page
from milo.flows import summarize
from milo.page import DASHBOARD, PAGE
from milo.shell import FAVICON, SHELL_CSS, site_header
from milo.users import (
    MemoryUserStore,
    check_new_account,
    hash_password,
    verify_password,
)

REASONS = ("wrong", "outdated", "missing_source", "hard_to_follow")
DEMO_FILE = Path(__file__).resolve().parents[2] / "data" / "demo_storylines.json"


def create_app(
    milo_app: App, secret_key: str | None = None, users: Any = None
) -> Flask:
    web = Flask(__name__)
    web.secret_key = (
        secret_key or os.environ.get("MILO_SECRET_KEY") or secrets.token_hex(32)
    )
    user_store = users if users is not None else MemoryUserStore()

    def current_user():
        uid = session.get("user_id")
        return user_store.by_id(uid) if uid else None

    def owner() -> str:
        return str(session["user_id"])

    def ensure_thread() -> None:
        if "thread" not in session:
            session["thread"] = uuid.uuid4().hex

    def sign_in(user) -> None:
        session.clear()
        session["user_id"] = user.id
        session["thread"] = uuid.uuid4().hex

    def wants_json() -> bool:
        return request.path.startswith("/api/")

    def login_needed(admin: bool = False):
        """Decorator: a page redirects to sign-in; an API answers 401; a customer on an admin page gets 403."""

        def wrap(view):
            def inner(*args, **kwargs):
                user = current_user()
                if user is None:
                    if wants_json():
                        return jsonify({"error": "sign in first"}), 401
                    return redirect(
                        url_for("login", next=request.full_path.rstrip("?"))
                    )
                if admin and user.role != "admin":
                    if wants_json():
                        return jsonify({"error": "owner only"}), 403
                    return Response(
                        "This page is for the owner.", status=403, mimetype="text/plain"
                    )
                return view(*args, **kwargs)

            inner.__name__ = view.__name__
            return inner

        return wrap

    def html(page: str) -> Response:
        return Response(page, mimetype="text/html")

    def chat_page(user) -> str:
        return (
            PAGE.replace("<!--HEADER-->", site_header("chat", user))
            .replace("<!--FAVICON-->", FAVICON)
            .replace("<style>", "<style>" + SHELL_CSS, 1)
        )

    # ---- public pages --------------------------------------------------------------------------------------

    @web.get("/")
    def index() -> Response:
        from milo.landing import landing_page

        return html(landing_page(current_user()))

    @web.get("/signup")
    def signup() -> Response:
        return html(signup_page())

    @web.post("/signup")
    def signup_submit() -> Any:
        name = (request.form.get("name") or "").strip()
        login_id = (request.form.get("login_id") or "").strip()
        password = request.form.get("password") or ""
        problem = check_new_account(login_id, name, password)
        if problem is None and user_store.by_login(login_id) is not None:
            problem = "That ID is already registered. Choose another, or log in."
        if problem:
            return html(signup_page(problem, name, login_id))
        user = user_store.create(login_id, name, hash_password(password), "customer")
        sign_in(user)
        return redirect("/")

    @web.get("/login")
    def login() -> Response:
        return html(login_page(next_url=request.args.get("next", "/")))

    @web.post("/login")
    def login_submit() -> Any:
        login_id = (request.form.get("login_id") or "").strip()
        password = request.form.get("password") or ""
        next_url = request.form.get("next") or "/"
        found = user_store.by_login(login_id)
        if found is None or not verify_password(password, found[1]):
            return html(
                login_page("The ID or password is not correct.", login_id, next_url)
            )
        sign_in(found[0])
        if hasattr(user_store, "record_login"):
            user_store.record_login(found[0].id)
        return redirect(next_url if next_url.startswith("/") else "/")

    @web.post("/logout")
    def logout() -> Any:
        session.clear()
        return redirect("/")

    @web.get("/api/me")
    def me() -> Any:
        user = current_user()
        if user is None:
            return jsonify({"signed_in": False})
        return jsonify(
            {
                "signed_in": True,
                "name": user.display_name,
                "role": user.role,
                "login_id": user.login_id,
            }
        )

    @web.get("/account/password")
    @login_needed()
    def password_form() -> Response:
        return html(password_page(current_user()))

    @web.post("/account/password")
    @login_needed()
    def password_submit() -> Any:
        user = current_user()
        current = request.form.get("current") or ""
        new = request.form.get("new") or ""
        again = request.form.get("again") or ""
        found = user_store.by_login(user.login_id)
        if found is None or not verify_password(current, found[1]):
            return html(password_page(user, "The current password is not correct."))
        if new != again:
            return html(password_page(user, "The two new passwords do not match."))
        problem = check_new_account(user.login_id, user.display_name, new)
        if problem:
            return html(password_page(user, problem))
        if new == current:
            return html(
                password_page(user, "Choose a password different from the current one.")
            )
        user_store.set_password(user.id, hash_password(new))
        return html(password_page(user, saved=True))

    @web.get("/kb")
    def kb_index() -> Response:
        from milo.kb_pages import index_page

        return html(index_page(current_user()))

    @web.get("/kb/<path:doc_id>")
    def kb_document(doc_id: str) -> Any:
        from milo.kb_pages import document_page

        page = document_page(doc_id, current_user())
        if page is None:
            return Response("Document not found", status=404, mimetype="text/plain")
        return html(page)

    @web.get("/api/kb/<path:doc_id>")
    def kb_text(doc_id: str) -> Any:
        from milo.kb_pages import document_json

        doc = document_json(doc_id)
        if doc is None:
            return jsonify({"error": "not found"}), 404
        return jsonify(doc)

    @web.get("/api/demo")
    def demo() -> Any:
        return jsonify(json.loads(DEMO_FILE.read_text()))

    # ---- signed-in customers ---------------------------------------------------------------------------------

    @web.get("/chat")
    @login_needed()
    def chat() -> Response:
        if request.args.get("new"):
            session["thread"] = uuid.uuid4().hex
        ensure_thread()
        return html(chat_page(current_user()))

    @web.get("/api/history")
    @login_needed()
    def history() -> Any:
        ensure_thread()
        turns = milo_app.store.history(owner(), session["thread"], limit=40)
        return jsonify({"turns": turns})

    @web.post("/api/ask")
    @login_needed()
    def ask() -> Any:
        ensure_thread()
        body = request.get_json(silent=True) or {}
        question = body.get("question", "")
        if not isinstance(question, str):
            return jsonify(
                {"answer": "", "error": "invalid_input: question must be text"}
            ), 400
        response = milo_app.ask(question, user_id=owner(), thread_id=session["thread"])
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

    @web.post("/api/feedback")
    @login_needed()
    def feedback() -> Any:
        """One thumbs vote on an answer. Stores the rating, a reason from a fixed list and a hashed owner. No text."""
        body = request.get_json(silent=True) or {}
        rating = body.get("rating")
        reason = body.get("reason", "")
        if rating not in ("up", "down"):
            return jsonify(
                {"ok": False, "error": "invalid_input: rating must be up or down"}
            ), 400
        if reason and reason not in REASONS:
            return jsonify({"ok": False, "error": "invalid_input: unknown reason"}), 400
        milo_app.store.add_feedback(owner(), rating, reason)
        return jsonify({"ok": True})

    # ---- the owner only -------------------------------------------------------------------------------------

    @web.get("/dashboard")
    @login_needed(admin=True)
    def dashboard() -> Response:
        page = (
            DASHBOARD.replace("<!--HEADER-->", site_header("overview", current_user()))
            .replace("<!--FAVICON-->", FAVICON)
            .replace("<style>", "<style>" + SHELL_CSS, 1)
        )
        return html(page)

    @web.get("/admin/users")
    @login_needed(admin=True)
    def admin_users() -> Response:
        return html(users_page(current_user(), user_store.all()))

    @web.get("/api/flows")
    @login_needed(admin=True)
    def flows() -> Any:
        scope = None if request.args.get("scope") != "mine" else owner()
        rows = milo_app.store.flows(scope, limit=200)
        return jsonify({"flows": rows, "summary": summarize(rows)})

    @web.get("/api/status")
    @login_needed(admin=True)
    def status() -> Any:
        from milo.status import snapshot

        kind = (
            "postgres" if type(milo_app.store).__name__ == "PostgresStore" else "memory"
        )
        url = os.environ.get("MILO_DATABASE_URL")
        model = os.environ.get("MILO_CHAT_MODEL", "anthropic/claude-haiku-5.5")
        return jsonify(
            snapshot(kind, url, milo_app.store.flows(None, limit=100000), model)
        )

    return web
