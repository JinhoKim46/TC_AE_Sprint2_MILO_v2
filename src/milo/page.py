"""The MILO chat page: one HTML document with its CSS and script.

Layout follows the recommended option in the earlier project's layout study (docs/design/MILO Layout Options, option D):
a chat first, with sources and tool calls shown inline under each answer, and an inspector for the selected answer.
All text from the server is inserted with textContent, never as HTML.
"""

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MILO · Diagnosis chat</title>
<style>
:root{
  --bg:#F6F5F1; --card:#FFFFFF; --line:#DEDBD2; --side:#FBFAF7; --ink:#1E1D1A; --mut:#6E6B63;
  --user:#E4E1D8; --accent:#2F6B5E; --accent-soft:#EEF3F1; --warn:#8A4B1F; --warn-bg:#FBF1E8; --warn-line:#E9CDB4;
  --bad:#8A2F2F; --bad-bg:#F8E9E9;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#161615; --card:#1F1F1D; --line:#3A3A36; --side:#1A1A18; --ink:#ECECE8; --mut:#9A9A94;
    --user:#2C2C29; --accent:#7BC08F; --accent-soft:#1E2E24; --warn:#E0B060; --warn-bg:#2E2619; --warn-line:#5A4524;
    --bad:#E08080; --bad-bg:#321D1D;
  }
}
:root[data-theme="dark"]{
  --bg:#161615; --card:#1F1F1D; --line:#3A3A36; --side:#1A1A18; --ink:#ECECE8; --mut:#9A9A94;
  --user:#2C2C29; --accent:#7BC08F; --accent-soft:#1E2E24; --warn:#E0B060; --warn-bg:#2E2619; --warn-line:#5A4524;
  --bad:#E08080; --bad-bg:#321D1D;
}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
.app{display:grid;grid-template-columns:230px minmax(0,1fr) 340px;height:100vh}
.app.no-inspector{grid-template-columns:230px minmax(0,1fr)}
.side{background:var(--side);border-right:1px solid var(--line);padding:16px;display:flex;flex-direction:column;gap:12px}
.brand{font-weight:700;letter-spacing:.04em}
.brand small{display:block;font-weight:400;color:var(--mut);letter-spacing:0;font-size:12px}
.side p{margin:0;color:var(--mut);font-size:13px}
.btn{font:inherit;border:1px solid var(--line);background:var(--card);color:var(--ink);padding:8px 12px;border-radius:8px;cursor:pointer;text-decoration:none;display:inline-block}
.btn:hover{border-color:var(--accent)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.btn:disabled{opacity:.55;cursor:default}
.btn.quiet{background:transparent;border-color:transparent;color:var(--mut);padding:4px 8px;font-size:13px}
.main{display:flex;flex-direction:column;min-width:0;min-height:0}
.topbar{height:52px;padding:0 20px;display:flex;align-items:center;gap:12px;background:var(--card);border-bottom:1px solid var(--line)}
.topbar h1{font-size:15px;margin:0;font-weight:600}
.topbar .spacer{flex:1}
.muted{color:var(--mut);font-size:13px}
.thread{flex:1;overflow-y:auto;padding:24px 20px 8px;display:flex;flex-direction:column;gap:18px}
.thread-inner{width:100%;max-width:760px;margin:0 auto;display:flex;flex-direction:column;gap:18px}
.msg{display:flex;flex-direction:column;gap:8px}
.msg.user{align-items:flex-end}
.bubble{padding:10px 14px;border-radius:14px;max-width:92%;white-space:pre-wrap;word-wrap:break-word}
.msg.user .bubble{background:var(--user);border-bottom-right-radius:4px}
.msg.assistant .bubble{background:transparent;padding-left:0;padding-right:0;max-width:100%}
.notice{border:1px solid var(--warn-line);background:var(--warn-bg);color:var(--warn);border-radius:10px;padding:10px 12px;font-size:14px}
.notice.bad{border-color:#E9B7B7;background:var(--bad-bg);color:var(--bad)}
.chips{display:flex;gap:8px;flex-wrap:wrap}
.chip{font:inherit;font-size:12px;padding:4px 10px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}
.chip.on{background:var(--accent-soft);color:var(--accent);border-color:transparent}
.chip.warn{background:var(--warn-bg);color:var(--warn);border-color:var(--warn-line)}
.chip.bad{background:var(--bad-bg);color:var(--bad);border-color:transparent}
.evidence{border:1px solid var(--line);border-radius:10px;background:var(--card);padding:10px 12px;font-size:13px;display:flex;flex-direction:column;gap:6px}
.evidence h3{margin:0;font-size:12px;color:var(--mut);font-weight:600;text-transform:uppercase;letter-spacing:.04em}
.evidence .row{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}
code{font:12px ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--accent-soft);padding:1px 4px;border-radius:4px;word-break:break-all}
.empty{margin:auto;text-align:center;max-width:520px;display:flex;flex-direction:column;gap:12px;align-items:center}
.empty h2{font-size:20px;margin:0}
.suggest{display:flex;flex-direction:column;gap:8px;width:100%}
.suggest button{text-align:left}
.composer-wrap{border-top:1px solid var(--line);background:var(--bg);padding:12px 20px 16px}
.composer{width:100%;max-width:760px;margin:0 auto;display:flex;gap:8px;align-items:flex-end;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:8px}
.composer textarea{flex:1;resize:none;border:0;outline:none;background:transparent;color:var(--ink);font:inherit;max-height:160px;min-height:24px;padding:6px}
.status{min-height:20px;font-size:13px;color:var(--mut);padding:0 2px}
.dots::after{content:"";animation:dots 1.2s steps(4,end) infinite}
@keyframes dots{0%{content:""}25%{content:"."}50%{content:".."}75%{content:"..."}}
.inspector{background:var(--side);border-left:1px solid var(--line);padding:16px;overflow-y:auto;display:flex;flex-direction:column;gap:12px}
.inspector h2{font-size:14px;margin:0}
.tabs{display:flex;gap:6px;flex-wrap:wrap}
.tool-name{font-weight:600}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
@media (max-width:900px){
  .app{grid-template-columns:1fr}
  .side{display:none}
  .inspector{display:none}
  .app.show-inspector .inspector{display:flex;position:fixed;inset:0;z-index:5}
}
</style>
</head>
<body>
<div class="app" id="app">
  <aside class="side">
    <div class="brand">MILO<small>Diagnosis chat</small></div>
    <a class="btn primary" href="/?new=1" id="new">New conversation</a>
    <p>MILO asks about your business, records what you say, and answers from its knowledge base. Each answer shows its sources and tool calls.</p>
    <div class="spacer" style="flex:1"></div>
    <p>Your conversation is kept for this browser. Clearing cookies starts a new one.</p>
  </aside>

  <main class="main">
    <header class="topbar">
      <h1>Diagnosis chat</h1>
      <span class="spacer"></span>
      <span class="muted" id="session-cost">Session cost: $0.0000</span>
      <button class="btn quiet" id="toggle-inspector" type="button" aria-controls="inspector">Details</button>
    </header>

    <section class="thread" id="thread" aria-live="polite" aria-label="Conversation">
      <div class="thread-inner" id="thread-inner"></div>
    </section>

    <div class="composer-wrap">
      <div class="status" id="status" role="status"></div>
      <form class="composer" id="composer">
        <label class="sr" for="question">Your message</label>
        <textarea id="question" rows="1" maxlength="4000" placeholder="Describe your business, or ask a question"></textarea>
        <button class="btn primary" id="send" type="submit">Send</button>
      </form>
    </div>
  </main>

  <aside class="inspector" id="inspector" aria-label="Details of the selected answer">
    <h2>Details</h2>
    <div class="muted" id="inspector-empty">Select an answer to see its sources and tool calls.</div>
    <div id="inspector-body" style="display:flex;flex-direction:column;gap:10px"></div>
  </aside>
</div>

<script>
(() => {
  const thread = document.getElementById("thread-inner");
  const form = document.getElementById("composer");
  const input = document.getElementById("question");
  const send = document.getElementById("send");
  const status = document.getElementById("status");
  const inspectorBody = document.getElementById("inspector-body");
  const inspectorEmpty = document.getElementById("inspector-empty");
  const app = document.getElementById("app");
  const costLabel = document.getElementById("session-cost");

  const messages = [];       // {role, text, sources, tool_results, cost_usd, stopped, error}
  let selected = -1;
  let sessionCost = 0;
  let busy = false;

  const el = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined && text !== null) n.textContent = String(text);
    return n;
  };
  const money = (v) => "$" + Number(v || 0).toFixed(4);
  const decisionClass = (d) => (d === "allowed" ? "on" : d === "needs_approval" ? "warn" : "bad");

  function evidenceCard(title) {
    const card = el("div", "evidence");
    card.appendChild(el("h3", "", title));
    return card;
  }

  function sourcesSummary(m) {
    const n = (m.sources || []).length;
    return n ? "Sources · " + n : "No sources";
  }

  function toolsSummary(m) {
    const n = (m.tool_results || []).length;
    return n ? "Tools · " + n : "No tools";
  }

  function render() {
    thread.replaceChildren();
    if (messages.length === 0) {
      const empty = el("div", "empty");
      empty.appendChild(el("h2", "", "What would you like to look at first?"));
      empty.appendChild(el("p", "muted", "Tell MILO about one kind of work in your business. Try one of these:"));
      const list = el("div", "suggest");
      [
        "We get about 40 service requests a week and each takes about 12 minutes to assign. What could a shared queue save?",
        "How do we work out the billing for printer and copier meter readings?",
        "What does the operations overview include, and what does it leave out?",
      ].forEach((s) => {
        const b = el("button", "btn", s);
        b.type = "button";
        b.addEventListener("click", () => { input.value = s; input.focus(); autosize(); });
        list.appendChild(b);
      });
      empty.appendChild(list);
      thread.appendChild(empty);
      return;
    }
    const inner = el("div", "thread-inner");
    messages.forEach((m, i) => inner.appendChild(messageNode(m, i)));
    thread.replaceChildren(inner);
    thread.scrollTop = thread.scrollHeight;
  }

  function messageNode(m, i) {
    const wrap = el("div", "msg " + m.role);
    if (m.role === "user") {
      wrap.appendChild(el("div", "bubble", m.text));
      return wrap;
    }
    if (m.error) {
      wrap.appendChild(el("div", "notice bad", m.text));
    } else {
      wrap.appendChild(el("div", "bubble", m.text));
    }
    if (!m.error || (m.sources || []).length || (m.tool_results || []).length) {
      const chips = el("div", "chips");
      const src = el("button", "chip " + ((m.sources || []).length ? "on" : ""), sourcesSummary(m));
      src.type = "button";
      src.addEventListener("click", () => select(i));
      const tools = el("button", "chip " + ((m.tool_results || []).length ? "on" : ""), toolsSummary(m));
      tools.type = "button";
      tools.addEventListener("click", () => select(i));
      chips.append(src, tools);
      if (m.stopped) chips.appendChild(el("span", "chip warn", "Waiting for your approval"));
      if (m.error) chips.appendChild(el("span", "chip bad", "Not answered"));
      if (m.cost_usd) chips.appendChild(el("span", "chip", money(m.cost_usd)));
      wrap.appendChild(chips);
      if (i === selected) wrap.appendChild(inlineEvidence(m));
    }
    return wrap;
  }

  function inlineEvidence(m) {
    const box = el("div", "msg-evidence");
    (m.tool_results || []).forEach((t) => {
      const card = evidenceCard("Tool call");
      const row = el("div", "row");
      row.append(el("span", "tool-name", t.name), el("span", "chip " + decisionClass(t.policy_decision), t.policy_decision));
      card.appendChild(row);
      card.appendChild(el("div", "muted", "Arguments"));
      card.appendChild(el("code", "", JSON.stringify(t.arguments)));
      box.appendChild(card);
    });
    if ((m.sources || []).length) {
      const card = evidenceCard("Sources");
      m.sources.forEach((s) => {
        const row = el("div", "row");
        row.append(el("code", "", s.chunk_id), el("span", "", s.doc_id), el("span", "muted", "score " + Number(s.score).toFixed(3)));
        card.appendChild(row);
      });
      box.appendChild(card);
    }
    return box;
  }

  function select(i) {
    selected = i;
    const m = messages[i];
    inspectorBody.replaceChildren();
    if (!m || m.role !== "assistant") {
      inspectorEmpty.hidden = false;
      return;
    }
    inspectorEmpty.hidden = true;
    const title = el("div", "tool-name", "Answer " + (i + 1));
    inspectorBody.appendChild(title);
    const sources = evidenceCard("Sources (" + (m.sources || []).length + ")");
    (m.sources || []).forEach((s) => {
      sources.appendChild(el("div", "", s.doc_id + "  ·  " + s.chunk_id));
      sources.appendChild(el("div", "muted", s.text.slice(0, 220) + (s.text.length > 220 ? "..." : "")));
    });
    if (!(m.sources || []).length) sources.appendChild(el("div", "muted", "No passage was used."));
    inspectorBody.appendChild(sources);
    const tools = evidenceCard("Tool calls (" + (m.tool_results || []).length + ")");
    (m.tool_results || []).forEach((t) => {
      const row = el("div", "row");
      row.append(el("span", "tool-name", t.name), el("span", "chip " + decisionClass(t.policy_decision), t.policy_decision));
      tools.appendChild(row);
      tools.appendChild(el("code", "", JSON.stringify(t.arguments)));
      tools.appendChild(el("code", "", JSON.stringify(t.output)));
    });
    if (!(m.tool_results || []).length) tools.appendChild(el("div", "muted", "No tool was called."));
    inspectorBody.appendChild(tools);
    inspectorBody.appendChild(flowCard(m.trace || []));
    const cost = evidenceCard("Cost");
    cost.appendChild(el("div", "", money(m.cost_usd)));
    inspectorBody.appendChild(cost);
    if (m.error) inspectorBody.appendChild(el("div", "notice bad", m.error));
    render();
  }

  function flowCard(steps) {
    const card = evidenceCard("How this answer was made");
    if (!steps.length) {
      card.appendChild(el("div", "muted", "No trace for this answer."));
      return card;
    }
    steps.forEach((st) => card.appendChild(stepRow(st)));
    return card;
  }

  function stepRow(st) {
    const row = el("div", "row");
    const label = {history_read: "Read history", retrieve: "Retrieve passages", model: "Model call", tool: "Tool call", answer: "Answer"}[st.step] || st.step;
    row.appendChild(el("strong", "", label));
    if (st.step === "retrieve") row.appendChild(el("span", "muted", (st.hits || []).length + " passages from " + (st.table || "index")));
    if (st.step === "history_read") row.appendChild(el("span", "muted", st.turns + " earlier messages from turns"));
    if (st.step === "model") row.appendChild(el("span", "muted", (st.model || "model") + " · " + (st.input_tokens || 0) + " in / " + (st.output_tokens || 0) + " out tokens"));
    if (st.step === "tool") {
      row.appendChild(el("span", "tool-name", st.name));
      row.appendChild(el("span", "chip " + decisionClass(st.decision), st.decision));
      row.appendChild(el("span", "muted", "table: " + (st.table || "none")));
    }
    if (st.step === "answer" && st.error) row.appendChild(el("span", "chip bad", st.error));
    if (st.ms !== undefined) row.appendChild(el("span", "muted", st.ms + " ms"));
    return row;
  }

  function setBusy(on) {
    busy = on;
    send.disabled = on;
    input.disabled = on;
    status.replaceChildren();
    if (on) status.append(el("span", "dots", "MILO is working"));
  }

  function autosize() {
    input.style.height = "auto";
    input.style.height = Math.min(input.scrollHeight, 160) + "px";
  }

  async function ask(question) {
    messages.push({ role: "user", text: question });
    render();
    setBusy(true);
    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      const reply = {
        role: "assistant",
        text: data.answer || "",
        sources: data.sources || [],
        tool_results: data.tool_results || [],
        cost_usd: data.cost_usd || 0,
        stopped: !!data.stopped,
        trace: data.trace || [],
        error: data.error ? "Something went wrong. Please try again in a moment." : null,
      };
      if (reply.error) reply.text = reply.text || "MILO could not answer just now.";
      messages.push(reply);
      sessionCost += reply.cost_usd;
      costLabel.textContent = "Session cost: " + money(sessionCost);
      selected = messages.length - 1;
    } catch (err) {
      messages.push({ role: "assistant", text: "The connection to MILO failed. Check that the server is running.", error: "network", sources: [], tool_results: [] });
    } finally {
      setBusy(false);
      render();
      if (selected >= 0) select(selected);
    }
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const q = input.value.trim();
    if (!q || busy) return;
    input.value = "";
    autosize();
    ask(q);
  });
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      form.requestSubmit();
    }
  });
  input.addEventListener("input", autosize);

  document.getElementById("toggle-inspector").addEventListener("click", () => app.classList.toggle("show-inspector"));

  async function loadHistory() {
    try {
      const res = await fetch("/api/history");
      const data = await res.json();
      (data.turns || []).forEach((t) => messages.push({ role: t.role, text: t.content, sources: [], tool_results: [], cost_usd: 0 }));
    } catch (err) {
      /* history is optional; the page still works without it */
    }
    render();
    inspectorEmpty.hidden = false;
  }
  loadHistory();
})();
</script>
</body>
</html>
"""

DASHBOARD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MILO · Flow dashboard</title>
<style>
:root{--bg:#F6F5F1;--card:#FFFFFF;--line:#DEDBD2;--ink:#1E1D1A;--mut:#6E6B63;--accent:#2F6B5E;--accent-soft:#EEF3F1;--bad:#8A2F2F;--bad-bg:#F8E9E9;--warn:#8A4B1F;--warn-bg:#FBF1E8}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#161615;--card:#1F1F1D;--line:#3A3A36;--ink:#ECECE8;--mut:#9A9A94;--accent:#7BC08F;--accent-soft:#1E2E24;--bad:#E08080;--bad-bg:#321D1D;--warn:#E0B060;--warn-bg:#2E2619}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
header{display:flex;align-items:center;gap:12px;padding:14px 20px;background:var(--card);border-bottom:1px solid var(--line)}
header h1{font-size:16px;margin:0;font-weight:600}
header a{color:var(--accent);text-decoration:none;font-size:14px}
header .spacer{flex:1}
main{padding:20px;display:grid;gap:16px;max-width:1200px;margin:0 auto}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px}
.card h2{font-size:12px;margin:0 0 8px;color:var(--mut);font-weight:600;text-transform:uppercase;letter-spacing:.04em}
.kpi .v{font-size:24px;font-weight:600}
.kpi .l{font-size:12px;color:var(--mut)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media (max-width:820px){.cols{grid-template-columns:1fr}}
.bar{display:grid;grid-template-columns:200px 1fr 46px;gap:8px;align-items:center;font-size:13px;margin:5px 0}
.bar .track{background:var(--accent-soft);border-radius:6px;height:14px;overflow:hidden}
.bar .fill{background:var(--accent);height:100%}
.muted{color:var(--mut);font-size:13px}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{text-align:left;padding:7px 6px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--mut);font-weight:600}
tr.pick{cursor:pointer}
tr.pick:hover{background:var(--accent-soft)}
.chip{display:inline-block;font-size:12px;padding:2px 8px;border-radius:999px;background:var(--accent-soft);color:var(--accent)}
.chip.bad{background:var(--bad-bg);color:var(--bad)}
.chip.warn{background:var(--warn-bg);color:var(--warn)}
.step{display:grid;grid-template-columns:150px 1fr;gap:10px;padding:8px 0;border-bottom:1px dashed var(--line);font-size:13px}
.step .t{font-weight:600}
.empty{color:var(--mut);padding:12px 0}
</style>
</head>
<body>
<header>
  <h1>MILO flow dashboard</h1>
  <span class="muted">How the chatbot retrieves, calls tools and touches the database, for this browser's conversation</span>
  <span class="spacer"></span>
  <a href="/">Back to chat</a>
  <a href="/dashboard">Refresh</a>
</header>
<main>
  <section class="kpis" id="kpis"></section>
  <section class="cols">
    <div class="card"><h2>Tool calls by name</h2><div id="tools"></div></div>
    <div class="card"><h2>Policy decisions</h2><div id="decisions"></div></div>
    <div class="card"><h2>Database and index access</h2><div id="tables"></div></div>
    <div class="card"><h2>Model calls</h2><div id="models"></div></div>
  </section>
  <section class="card">
    <h2>Recent questions (click one to see its flow)</h2>
    <table><thead><tr><th>Time</th><th>Steps</th><th>Total</th><th>Cost</th><th>Status</th></tr></thead><tbody id="flows"></tbody></table>
    <div class="empty" id="flows-empty" hidden>No questions yet in this browser. Ask one in the chat.</div>
  </section>
  <section class="card" id="detail" hidden>
    <h2 id="detail-title">Flow</h2>
    <div id="detail-body"></div>
  </section>
</main>
<script>
(() => {
  const el = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined && text !== null) n.textContent = String(text); return n; };
  const money = (v) => "$" + Number(v || 0).toFixed(5);
  const bars = (target, obj, empty) => {
    target.replaceChildren();
    const entries = Object.entries(obj || {}).sort((a, b) => b[1] - a[1]);
    if (!entries.length) { target.appendChild(el("div", "empty", empty)); return; }
    const max = Math.max(...entries.map((e) => e[1]), 1);
    entries.forEach(([k, v]) => {
      const row = el("div", "bar");
      row.append(el("span", "", k), el("div", "track"), el("span", "", v));
      row.querySelector(".track").appendChild(el("div", "fill"));
      row.querySelector(".fill").style.width = Math.round((v / max) * 100) + "%";
      target.appendChild(row);
    });
  };
  const label = {history_read: "Read history", retrieve: "Retrieve passages", model: "Model call", tool: "Tool call", answer: "Answer"};
  const detail = (st) => {
    const parts = [];
    if (st.step === "retrieve") parts.push((st.hits || []).map((h) => h.doc_id + " (score " + h.score + ")").join("; ") || "no passage");
    if (st.step === "history_read") parts.push(st.turns + " earlier messages read from " + st.table);
    if (st.step === "model") parts.push((st.model || "model") + ", " + (st.input_tokens || 0) + " in / " + (st.output_tokens || 0) + " out, calls: " + ((st.tool_calls || []).join(", ") || "none"));
    if (st.step === "tool") parts.push(st.name + " · " + st.decision + " · table: " + (st.table || "none"));
    if (st.step === "answer") parts.push((st.stopped ? "stopped for approval" : "answered") + (st.error ? " · error: " + st.error : ""));
    return parts.join("");
  };
  const showFlow = (f) => {
    const box = document.getElementById("detail-body");
    box.replaceChildren();
    document.getElementById("detail-title").textContent = "Flow at " + f.ts + " · " + f.total_ms + " ms";
    (f.steps || []).forEach((st) => {
      const row = el("div", "step");
      row.append(el("span", "t", (label[st.step] || st.step) + (st.ms !== undefined ? "  ·  " + st.ms + " ms" : "")), el("span", "", detail(st)));
      box.appendChild(row);
    });
    document.getElementById("detail").hidden = false;
  };
  async function load() {
    const res = await fetch("/api/flows");
    const data = await res.json();
    const s = data.summary;
    const kpis = document.getElementById("kpis");
    kpis.replaceChildren();
    [["Questions", s.questions], ["Average time", s.avg_total_ms + " ms"], ["Cost", money(s.cost_usd)],
     ["Error rate", Math.round(s.error_rate * 100) + "%"], ["Avg top score", s.avg_top_score === null ? "-" : s.avg_top_score],
     ["Tokens in / out", s.tokens.input + " / " + s.tokens.output]].forEach(([l, v]) => {
      const c = el("div", "card kpi"); c.append(el("div", "v", v), el("div", "l", l)); kpis.appendChild(c);
    });
    bars(document.getElementById("tools"), s.tool_calls, "No tool calls yet.");
    bars(document.getElementById("decisions"), s.tool_decisions, "No tool decisions yet.");
    bars(document.getElementById("tables"), s.table_access, "No database access yet.");
    bars(document.getElementById("models"), s.model_calls, "No model calls yet.");
    const body = document.getElementById("flows");
    body.replaceChildren();
    document.getElementById("flows-empty").hidden = data.flows.length > 0;
    data.flows.forEach((f) => {
      const tr = el("tr", "pick");
      const err = f.error ? el("span", "chip bad", f.error.split(":")[0]) : el("span", "chip", "ok");
      tr.append(el("td", "", f.ts), el("td", "", (f.steps || []).length), el("td", "", f.total_ms + " ms"), el("td", "", money(f.cost_usd)));
      const td = el("td", ""); td.appendChild(err); tr.appendChild(td);
      tr.addEventListener("click", () => showFlow(f));
      body.appendChild(tr);
    });
  }
  load();
})();
</script>
</body>
</html>
"""
