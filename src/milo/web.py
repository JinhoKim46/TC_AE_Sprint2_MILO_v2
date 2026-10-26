"""M6: a Flask chat page. The owner id is bound to the browser session on the server; the page never sends one.

Routes:
  GET  /           the chat page: answer, sources panel, tool-call panel with policy decision, progress, cost
  POST /api/ask    JSON in {"question": "..."}; JSON out with answer, error, sources, tool_results, cost_usd, stopped
"""

from __future__ import annotations

import os
import secrets
import uuid
from dataclasses import asdict
from typing import Any

from flask import Flask, jsonify, render_template_string, request, session

from milo.app import App

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MILO diagnosis chat</title>
<style>
:root{--bg:#fafaf8;--fg:#1d1d1b;--mut:#6b6b66;--line:#dcdcd6;--ok:#2c6b3f;--warn:#8a5a00;--bad:#9b2c2c}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#161615;--fg:#ecece8;--mut:#9a9a94;--line:#3a3a36;--ok:#7bc08f;--warn:#e0b060;--bad:#e08080}}
:root[data-theme="dark"]{--bg:#161615;--fg:#ecece8;--mut:#9a9a94;--line:#3a3a36;--ok:#7bc08f;--warn:#e0b060;--bad:#e08080}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif}
main{max-width:960px;margin:0 auto;padding:16px}
h1{font-size:20px;margin:8px 0 12px}
#log{border:1px solid var(--line);border-radius:8px;padding:12px;min-height:160px;white-space:pre-wrap}
form{display:flex;gap:8px;margin:12px 0}
textarea{flex:1;min-height:56px;font:inherit;color:inherit;background:transparent;border:1px solid var(--line);border-radius:8px;padding:8px}
button{font:inherit;padding:8px 16px;border-radius:8px;border:1px solid var(--line);background:transparent;color:inherit;cursor:pointer}
.grid{display:grid;grid-template-columns:2fr 1fr;gap:12px}
@media (max-width:720px){.grid{grid-template-columns:1fr}}
.panel{border:1px solid var(--line);border-radius:8px;padding:10px;font-size:14px}
.panel h2{font-size:14px;margin:0 0 6px;color:var(--mut)}
.src{margin-bottom:8px}.src code{color:var(--mut)}
.tool{margin-bottom:8px}.allowed{color:var(--ok)}.needs_approval{color:var(--warn)}.denied{color:var(--bad)}
#status{color:var(--mut);min-height:1.5em;font-size:14px}
#cost{color:var(--mut);font-size:13px}
</style></head>
<body><main>
<h1>MILO: diagnosis chat</h1>
<div id="log" aria-live="polite">Describe how your business handles one kind of work. MILO answers from its knowledge base.</div>
<form id="ask"><textarea id="q" placeholder="Ask a question" aria-label="Question"></textarea><button type="submit">Send</button></form>
<div id="status" role="status"></div>
<div id="cost"></div>
<div class="grid">
  <section class="panel"><h2>Sources</h2><div id="sources">None yet.</div></section>
  <section class="panel"><h2>Tool calls</h2><div id="tools">None yet.</div></section>
</div>
</main>
<script>
const form = document.getElementById("ask");
const esc = s => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
form.addEventListener("submit", async e => {
  e.preventDefault();
  const q = document.getElementById("q").value.trim();
  if (!q) return;
  const status = document.getElementById("status");
  status.textContent = "Thinking...";
  const res = await fetch("/api/ask", {method: "POST", headers: {"Content-Type": "application/json"},
                                       body: JSON.stringify({question: q})});
  const data = await res.json();
  status.textContent = "";
  document.getElementById("log").textContent += "\\n\\nYou: " + q + "\\nMILO: " + (data.answer || "");
  document.getElementById("cost").textContent = "Cost of this answer: " + (data.cost_usd || 0).toFixed(6) + " USD";
  document.getElementById("sources").innerHTML = (data.sources || []).map(s =>
    `<div class="src"><code>${esc(s.chunk_id)}</code><br>${esc(s.doc_id)} (score ${s.score.toFixed(3)})<br>${esc(s.text.slice(0, 160))}</div>`
  ).join("") || "None.";
  document.getElementById("tools").innerHTML = (data.tool_results || []).map(t =>
    `<div class="tool"><b>${esc(t.name)}</b> <span class="${esc(t.policy_decision)}">${esc(t.policy_decision)}</span><br>` +
    `arguments: <code>${esc(JSON.stringify(t.arguments))}</code><br>result: <code>${esc(JSON.stringify(t.output))}</code></div>`
  ).join("") || "None.";
  if (data.error) status.textContent = "Something went wrong. Please try again.";
  document.getElementById("q").value = "";
});
</script>
</body></html>
"""


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
    def index() -> str:
        owner()
        return render_template_string(PAGE)

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
            }
        )

    return web
