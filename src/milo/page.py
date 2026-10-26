"""The MILO pages: the chat and the overview. One HTML document each, with its CSS and script.

Design rules (for the people who will read it, not for developers):
- The default view answers three questions in plain words: what MILO did, where the answer came from, and how sure it is.
- Technical details (arguments, raw scores, identifiers) exist, but only behind a "Show details" control.
- All text from the server is inserted with textContent, never as HTML.
"""

_BASE_CSS = """
:root{--bg:#F5F4EF;--card:#FFFFFF;--line:#E2DFD6;--ink:#1F1E1B;--mut:#6B6860;--accent:#2F6B5E;--accent-soft:#E7F0EC;
  --ok:#2F6B5E;--ok-bg:#E7F0EC;--mid:#8A5A12;--mid-bg:#FBF1DF;--low:#8A2F2F;--low-bg:#F8E6E6;--step:#EFEDE6}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif;color-scheme:light}
h1,h2,h3{margin:0;line-height:1.25}
.muted{color:var(--mut);font-size:14px}
button,.button{font:inherit;cursor:pointer;border:1px solid var(--line);background:var(--card);color:var(--ink);
  padding:9px 14px;border-radius:10px;text-decoration:none;display:inline-block}
button:hover,.button:hover{border-color:var(--accent)}
button.primary{background:var(--accent);border-color:var(--accent);color:#fff}
button:disabled{opacity:.5;cursor:default}
.pill{display:inline-flex;align-items:center;gap:6px;font-size:13px;padding:4px 10px;border-radius:999px;background:var(--step);color:var(--ink)}
.pill.ok{background:var(--ok-bg);color:var(--ok)}
.pill.mid{background:var(--mid-bg);color:var(--mid)}
.pill.low{background:var(--low-bg);color:var(--low)}
.pill.wait{background:var(--accent-soft);color:var(--accent)}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
details summary{cursor:pointer;color:var(--accent);font-size:14px;list-style:none}
details summary::-webkit-details-marker{display:none}
details[open] summary{margin-bottom:8px}
.tech{font:12px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--bg);border-radius:8px;padding:8px;word-break:break-all;white-space:pre-wrap}
"""

PAGE = (
    """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MILO · Diagnosis chat</title>
<style>
"""
    + _BASE_CSS
    + """
.layout{display:grid;grid-template-columns:240px minmax(0,1fr);height:100vh}
.side{background:var(--card);border-right:1px solid var(--line);padding:20px 16px;display:flex;flex-direction:column;gap:18px}
.brand{font-size:18px;font-weight:700}
.brand span{display:block;font-size:13px;font-weight:400;color:var(--mut)}
.how h3{font-size:13px;color:var(--mut);text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px}
.how ol{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:10px}
.how li{display:flex;gap:10px;font-size:14px}
.how b{display:block}
.how small{color:var(--mut)}
.num{flex:0 0 26px;height:26px;border-radius:50%;background:var(--accent-soft);color:var(--accent);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px}
.side .spacer{flex:1}
.main{display:flex;flex-direction:column;min-width:0;min-height:0}
.topbar{padding:14px 24px;background:var(--card);border-bottom:1px solid var(--line);display:flex;align-items:center;gap:12px}
.topbar h1{font-size:17px}
.topbar .spacer{flex:1}
.thread{flex:1;overflow-y:auto;padding:28px 24px 12px}
.inner{max-width:780px;margin:0 auto;display:flex;flex-direction:column;gap:22px}
.hello{text-align:center;margin:56px auto 8px;max-width:560px;display:flex;flex-direction:column;gap:14px}
.hello h2{font-size:24px}
.starters{display:grid;gap:10px;margin-top:8px}
.starters button{text-align:left;padding:14px 16px;line-height:1.45}
.you{align-self:flex-end;max-width:78%;background:var(--accent);color:#fff;padding:11px 16px;border-radius:18px 18px 4px 18px;white-space:pre-wrap;word-break:break-word}
.answer{background:var(--card);border:1px solid var(--line);border-radius:18px 18px 18px 4px;padding:18px 20px;display:flex;flex-direction:column;gap:14px}
.answer .text{white-space:pre-wrap;word-break:break-word;font-size:16px}
.trust{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.trust .label{font-size:14px;color:var(--mut)}
.found{background:var(--bg);border-radius:12px;padding:12px 14px;display:flex;flex-direction:column;gap:8px}
.found h3{font-size:13px;color:var(--mut);text-transform:uppercase;letter-spacing:.05em}
.found ul{margin:0;padding-left:18px;font-size:15px}
.found li{margin:3px 0}
.stages{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.stage{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px;font-size:13px;display:flex;flex-direction:column;gap:4px}
.stage b{font-size:13px}
.stage .n{font-size:18px;font-weight:700;color:var(--accent)}
.notice{border-radius:12px;padding:12px 14px;background:var(--low-bg);color:var(--low);font-size:15px}
.approval{border-radius:12px;padding:12px 14px;background:var(--mid-bg);color:var(--mid);font-size:15px}
.composer-wrap{border-top:1px solid var(--line);background:var(--card);padding:14px 24px 18px}
.composer{max-width:780px;margin:0 auto;display:flex;gap:10px;align-items:flex-end}
.composer textarea{flex:1;resize:none;font:inherit;font-size:16px;padding:12px 14px;border:1px solid var(--line);border-radius:14px;outline:none;min-height:50px;max-height:180px;background:var(--bg);color:var(--ink)}
.composer textarea:focus{border-color:var(--accent)}
.working{max-width:780px;margin:0 auto 10px;display:flex;align-items:center;gap:12px;font-size:14px;color:var(--mut);min-height:22px}
.dot{width:9px;height:9px;border-radius:50%;background:var(--accent);animation:pulse 1.1s ease-in-out infinite}
.dot:nth-child(2){animation-delay:.15s}.dot:nth-child(3){animation-delay:.3s}
@keyframes pulse{0%,100%{opacity:.25}50%{opacity:1}}
.details-panel{display:flex;flex-direction:column;gap:14px;font-size:14px}
.details-panel h3{font-size:14px}
.row{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.src{border-top:1px solid var(--line);padding-top:10px}
.src:first-child{border-top:0;padding-top:0}
.src p{margin:4px 0 0;color:var(--mut);font-size:13px}
.step{display:grid;grid-template-columns:24px 1fr;gap:10px;align-items:start;padding:6px 0}
.step .i{width:24px;height:24px;border-radius:50%;background:var(--accent-soft);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700}
@media (max-width:860px){
  .layout{grid-template-columns:1fr}
  .side{display:none}
  .stages{grid-template-columns:repeat(2,minmax(0,1fr))}
}
</style>
</head>
<body>
<div class="layout">
  <aside class="side">
    <div class="brand">MILO<span>Diagnosis assistant</span></div>
    <a class="button" href="/?new=1" id="new">New conversation</a>
    <div class="how">
      <h3>How MILO works</h3>
      <ol>
        <li><span class="num">1</span><div><b>You describe your work</b><small>In your own words.</small></div></li>
        <li><span class="num">2</span><div><b>MILO finds the right passages</b><small>From its knowledge base of service areas and past cases.</small></div></li>
        <li><span class="num">3</span><div><b>It checks and records</b><small>Saves what you tell it and works out savings with a calculation, not a guess.</small></div></li>
        <li><span class="num">4</span><div><b>It answers from the passages</b><small>Each answer shows where it came from and how sure it is.</small></div></li>
      </ol>
    </div>
    <div class="spacer"></div>
    <p class="muted">Your conversation is kept for this browser. Clearing cookies starts a new one.</p>
  </aside>

  <main class="main">
    <header class="topbar">
      <h1>Diagnosis chat</h1>
      <span class="spacer"></span>
      <span class="muted" id="cost">Session cost: $0.0000</span>
    </header>

    <section class="thread" id="thread" aria-live="polite" aria-label="Conversation"></section>

    <div class="composer-wrap">
      <div class="working" id="working" role="status"></div>
      <form class="composer" id="composer">
        <label class="sr" for="question">Your message</label>
        <textarea id="question" rows="1" maxlength="4000" placeholder="Describe one kind of work in your business, or ask a question"></textarea>
        <button class="primary" id="send" type="submit">Send</button>
      </form>
    </div>
  </main>
</div>

<script>
(() => {
  const thread = document.getElementById("thread");
  const form = document.getElementById("composer");
  const input = document.getElementById("question");
  const send = document.getElementById("send");
  const working = document.getElementById("working");
  const costEl = document.getElementById("cost");

  const TOOL = {
    search_knowledge: "Searched the knowledge base",
    record_fact: "Saved something you told me",
    get_recorded_facts: "Checked what you have told me so far",
    estimate_effect: "Calculated the time saving",
    draft_diagnosis: "Drafted a diagnosis for this area",
    reset_diagnosis: "Asked to reset a diagnosis",
  };
  const DECISION = {
    allowed: ["ok", "Done"],
    needs_approval: ["mid", "Needs your approval"],
    denied: ["low", "Not allowed"],
  };
  const AREA = {
    "request-dispatch": "Request and dispatch",
    "consumables-stock": "Consumables and stock",
    "usage-billing-prep": "Usage and billing preparation",
    "operations-overview": "Operations overview",
  };
  const STARTERS = [
    "We get about 40 service requests a week, and each takes about 12 minutes to assign. What could a shared queue save us?",
    "We read printer meters by photo and check the bills by hand. Where does the time go?",
    "How do we know where our toner and spare parts are right now?",
  ];

  const el = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined && text !== null) n.textContent = String(text);
    return n;
  };
  const money = (v) => "$" + Number(v || 0).toFixed(4);

  // A passage's document id becomes a readable title: "solutions/request-dispatch" -> "Solution: Request dispatch".
  function docTitle(docId) {
    const [kind, name] = String(docId).split("/");
    const kinds = {solutions: "Service area", cases: "Past case", consultation: "Method note", policies: "Policy", general: "Note"};
    const words = String(name || docId).replace(/-/g, " ");
    const label = AREA[name] || words.charAt(0).toUpperCase() + words.slice(1);
    return (kinds[kind] || "Document") + ": " + label;
  }

  // Confidence from the best passage score. A plain indicator, explained on hover; not a probability.
  function confidence(sources) {
    if (!sources.length) return {level: "low", text: "No matching passage"};
    const best = Math.max(...sources.map((s) => Number(s.score)));
    if (best >= 0.75) return {level: "ok", text: "Strong match to the knowledge base"};
    if (best >= 0.5) return {level: "mid", text: "Partial match: check the sources"};
    return {level: "low", text: "Weak match: treat this answer with care"};
  }

  function stageSummary(m) {
    const sources = m.sources || [];
    const docs = [...new Set(sources.map((s) => s.doc_id))];
    const tools = m.tool_results || [];
    const turns = m.history_turns || 0;
    return [
      {title: "Read the conversation", n: turns ? turns : "New", note: turns ? "earlier messages used" : "first message"},
      {title: "Found passages", n: sources.length, note: docs.length ? "from " + docs.length + " document" + (docs.length === 1 ? "" : "s") : "none"},
      {title: "Used tools", n: tools.length, note: tools.length ? "steps taken" : "none needed"},
      {title: "Wrote the answer", n: m.error ? "-" : "1", note: m.error ? "could not answer" : "from the passages"},
    ];
  }

  function toolLine(t) {
    const label = TOOL[t.name] || t.name;
    const d = DECISION[t.policy_decision] || ["", t.policy_decision];
    const row = el("div", "step");
    row.appendChild(el("span", "i", "✓"));
    const body = el("div");
    body.appendChild(el("div", "", label));
    const badge = el("span", "pill " + d[0], d[1]);
    body.appendChild(badge);
    row.appendChild(body);
    return row;
  }

  function answerCard(m) {
    const card = el("article", "answer");
    if (m.error) {
      card.appendChild(el("div", "notice", m.text));
      return card;
    }
    card.appendChild(el("div", "text", m.text));

    const c = confidence(m.sources || []);
    const trust = el("div", "trust");
    trust.appendChild(el("span", "label", "How sure:"));
    const pill = el("span", "pill " + c.level, c.text);
    pill.title = "Based on how closely the best passage matches your question. It is not a probability that the answer is right.";
    trust.appendChild(pill);
    card.appendChild(trust);

    if (m.stopped) card.appendChild(el("div", "approval", "MILO needs your approval before it changes anything. Nothing was changed."));

    const stages = el("div", "stages");
    stageSummary(m).forEach((s) => {
      const box = el("div", "stage");
      box.append(el("b", "", s.title), el("span", "n", s.n), el("span", "muted", s.note));
      stages.appendChild(box);
    });
    card.appendChild(stages);

    if ((m.sources || []).length) {
      const found = el("div", "found");
      found.appendChild(el("h3", "", "Where this came from"));
      const list = el("ul");
      [...new Set(m.sources.map((s) => s.doc_id))].forEach((d) => list.appendChild(el("li", "", docTitle(d))));
      found.appendChild(list);
      card.appendChild(found);
    }

    if ((m.tool_results || []).length) {
      const steps = el("div", "found");
      steps.appendChild(el("h3", "", "What MILO did"));
      m.tool_results.forEach((t) => steps.appendChild(toolLine(t)));
      card.appendChild(steps);
    }

    const more = el("details");
    more.appendChild(el("summary", "", "Show technical details"));
    const panel = el("div", "details-panel");
    const srcs = el("div");
    srcs.appendChild(el("h3", "", "Passages (" + (m.sources || []).length + ")"));
    (m.sources || []).forEach((s) => {
      const row = el("div", "src");
      row.appendChild(el("div", "", docTitle(s.doc_id)));
      row.appendChild(el("p", "", s.text.slice(0, 260) + (s.text.length > 260 ? "..." : "")));
      row.appendChild(el("div", "tech", "chunk " + s.chunk_id + " · relevance " + Number(s.score).toFixed(3)));
      srcs.appendChild(row);
    });
    panel.appendChild(srcs);
    const tools = el("div");
    tools.appendChild(el("h3", "", "Tool calls (" + (m.tool_results || []).length + ")"));
    (m.tool_results || []).forEach((t) => {
      tools.appendChild(el("div", "tech", t.name + " " + JSON.stringify(t.arguments)));
    });
    panel.appendChild(tools);
    const steps = el("div");
    steps.appendChild(el("h3", "", "Timing"));
    (m.trace || []).forEach((st) => {
      const label = {history_read: "Read conversation", retrieve: "Searched passages", model: "Model call", tool: "Tool call", answer: "Wrote answer"}[st.step] || st.step;
      steps.appendChild(el("div", "tech", label + (st.ms !== undefined ? " · " + st.ms + " ms" : "")));
    });
    panel.appendChild(steps);
    panel.appendChild(el("div", "muted", "Cost of this answer: " + money(m.cost_usd)));
    more.appendChild(panel);
    card.appendChild(more);
    return card;
  }

  function render() {
    thread.replaceChildren();
    const inner = el("div", "inner");
    if (!messages.length) {
      const hello = el("div", "hello");
      hello.appendChild(el("h2", "", "What would you like to look at first?"));
      hello.appendChild(el("p", "muted", "Describe one kind of work in your business. MILO will ask follow-up questions when it needs more facts."));
      const list = el("div", "starters");
      STARTERS.forEach((s) => {
        const b = el("button", "", s);
        b.type = "button";
        b.addEventListener("click", () => { input.value = s; autosize(); input.focus(); });
        list.appendChild(b);
      });
      hello.appendChild(list);
      inner.appendChild(hello);
    }
    messages.forEach((m) => {
      if (m.role === "user") inner.appendChild(el("div", "you", m.text));
      else inner.appendChild(answerCard(m));
    });
    thread.appendChild(inner);
    thread.scrollTop = thread.scrollHeight;
  }

  const messages = [];
  let sessionCost = 0;
  let busy = false;

  function setBusy(on) {
    busy = on;
    send.disabled = on;
    input.disabled = on;
    working.replaceChildren();
    if (on) {
      working.append(el("span", "dot"), el("span", "dot"), el("span", "dot"), el("span", "", "MILO is reading your question, finding passages and checking the numbers"));
    }
  }

  function autosize() {
    input.style.height = "auto";
    input.style.height = Math.min(input.scrollHeight, 180) + "px";
  }

  async function ask(question) {
    messages.push({role: "user", text: question});
    render();
    setBusy(true);
    try {
      const res = await fetch("/api/ask", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({question})});
      const data = await res.json();
      const reply = {
        role: "assistant",
        text: data.answer || "",
        sources: data.sources || [],
        tool_results: data.tool_results || [],
        cost_usd: data.cost_usd || 0,
        stopped: !!data.stopped,
        trace: data.trace || [],
        history_turns: ((data.trace || []).find((x) => x.step === "history_read") || {turns: 0}).turns,
        error: data.error ? "Something went wrong on our side. Please try again in a moment." : null,
      };
      messages.push(reply);
      sessionCost += reply.cost_usd;
      costEl.textContent = "Session cost: " + money(sessionCost);
    } catch (err) {
      messages.push({role: "assistant", text: "", error: "The connection to MILO failed. Check that the server is running and try again."});
    } finally {
      setBusy(false);
      render();
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

  async function loadHistory() {
    try {
      const res = await fetch("/api/history");
      const data = await res.json();
      (data.turns || []).forEach((t) => messages.push({role: t.role === "user" ? "user" : "assistant", text: t.content, sources: [], tool_results: [], cost_usd: 0, trace: []}));
    } catch (err) {
      /* history is optional */
    }
    render();
  }
  loadHistory();
})();
</script>
</body>
</html>
"""
)

DASHBOARD = (
    """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MILO · How it works, with your data</title>
<style>
"""
    + _BASE_CSS
    + """
header{padding:18px 28px;background:var(--card);border-bottom:1px solid var(--line);display:flex;align-items:center;gap:14px;flex-wrap:wrap}
header h1{font-size:19px}
header .spacer{flex:1}
main{max-width:1100px;margin:0 auto;padding:24px 20px 48px;display:flex;flex-direction:column;gap:22px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px}
.card h2{font-size:17px;margin-bottom:6px}
.card .sub{color:var(--mut);font-size:14px;margin-bottom:14px}
.flow{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;align-items:stretch}
.flow .box{background:var(--bg);border-radius:14px;padding:14px;display:flex;flex-direction:column;gap:6px;border:1px solid var(--line)}
.flow .box b{font-size:14px}
.flow .box .n{font-size:26px;font-weight:700;color:var(--accent)}
.flow .box small{color:var(--mut);font-size:13px}
.flow .arrow{align-self:center;color:var(--mut);font-size:20px;text-align:center}
.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.kpi{background:var(--bg);border-radius:14px;padding:14px}
.kpi .v{font-size:24px;font-weight:700}
.kpi .l{font-size:13px;color:var(--mut)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.bars .bar{display:grid;grid-template-columns:170px 1fr 36px;gap:10px;align-items:center;font-size:14px;margin:8px 0}
.bars .track{background:var(--bg);border-radius:8px;height:14px;overflow:hidden}
.bars .fill{background:var(--accent);height:100%;border-radius:8px}
.legend{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}
.list{display:flex;flex-direction:column;gap:8px}
.item{display:flex;align-items:center;gap:12px;padding:12px 14px;border:1px solid var(--line);border-radius:12px;background:var(--card);text-align:left;width:100%}
.item .when{flex:1;font-size:15px}
.item .meta{color:var(--mut);font-size:13px}
.timeline{display:flex;flex-direction:column;gap:0}
.tl{display:grid;grid-template-columns:30px 1fr;gap:12px;padding:10px 0;border-left:2px solid var(--line);margin-left:14px;padding-left:0}
.tl:last-child{border-left-color:transparent}
.tl .dot{width:28px;height:28px;border-radius:50%;background:var(--accent-soft);color:var(--accent);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;margin-left:-15px}
.tl b{font-size:15px}
.tl p{margin:3px 0 0;color:var(--mut);font-size:14px}
.empty{color:var(--mut);padding:18px 0;font-size:15px}
@media (max-width:860px){.flow{grid-template-columns:1fr}.flow .arrow{display:none}.kpis{grid-template-columns:1fr 1fr}.two{grid-template-columns:1fr}.bars .bar{grid-template-columns:120px 1fr 30px}}
</style>
</head>
<body>
<header>
  <h1>How MILO works, using your conversation</h1>
  <span class="spacer"></span>
  <a class="button" href="/">Back to the chat</a>
  <button id="refresh" type="button">Refresh</button>
</header>
<main>
  <section class="card">
    <h2>The path every question takes</h2>
    <p class="sub">Counts are for your conversation in this browser. Each step is a real part of the system.</p>
    <div class="flow" id="flow"></div>
  </section>

  <section class="kpis" id="kpis"></section>

  <section class="two">
    <div class="card">
      <h2>How sure the answers were</h2>
      <p class="sub">Based on how closely the best passage matched each question.</p>
      <div class="bars" id="confidence"></div>
    </div>
    <div class="card">
      <h2>What MILO did with tools</h2>
      <p class="sub">Each tool call and what it was allowed to do.</p>
      <div class="bars" id="tools"></div>
    </div>
  </section>

  <section class="card">
    <h2>Your questions</h2>
    <p class="sub">Choose one to see, step by step, what MILO did with it.</p>
    <div class="list" id="list"></div>
    <div class="empty" id="empty" hidden>No questions yet. Ask one in the chat, then come back here.</div>
  </section>

  <section class="card" id="detail" hidden>
    <h2 id="detail-title">Step by step</h2>
    <p class="sub" id="detail-sub"></p>
    <div class="timeline" id="timeline"></div>
  </section>
</main>
<script>
(() => {
  const el = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined && text !== null) n.textContent = String(text);
    return n;
  };
  const TOOL = {
    search_knowledge: "Searched the knowledge base",
    record_fact: "Saved a fact you told it",
    get_recorded_facts: "Checked the facts so far",
    estimate_effect: "Calculated the time saving",
    draft_diagnosis: "Drafted a diagnosis",
    reset_diagnosis: "Asked to reset a diagnosis",
  };
  const DECISION = {allowed: "done", needs_approval: "waiting for your approval", denied: "not allowed"};
  const money = (v) => "$" + Number(v || 0).toFixed(4);

  function bars(target, obj, labelOf, empty) {
    target.replaceChildren();
    const entries = Object.entries(obj || {}).sort((a, b) => b[1] - a[1]);
    if (!entries.length) { target.appendChild(el("div", "empty", empty)); return; }
    const max = Math.max(...entries.map((e) => e[1]), 1);
    entries.forEach(([k, v]) => {
      const row = el("div", "bar");
      const track = el("div", "track");
      const fill = el("div", "fill");
      fill.style.width = Math.max(4, Math.round((v / max) * 100)) + "%";
      track.appendChild(fill);
      row.append(el("span", "", labelOf(k)), track, el("b", "", v));
      target.appendChild(row);
    });
  }

  function confidenceCounts(flows) {
    const out = {"Strong match": 0, "Partial match": 0, "Weak match": 0, "No passage": 0};
    flows.forEach((f) => {
      const hits = ((f.steps || []).find((s) => s.step === "retrieve") || {hits: []}).hits || [];
      if (!hits.length) { out["No passage"] += 1; return; }
      const best = Math.max(...hits.map((h) => Number(h.score)));
      if (best >= 0.75) out["Strong match"] += 1;
      else if (best >= 0.5) out["Partial match"] += 1;
      else out["Weak match"] += 1;
    });
    return out;
  }

  function flowBoxes(summary) {
    const tools = Object.values(summary.tool_calls || {}).reduce((a, b) => a + b, 0);
    const passages = summary.table_access ? (summary.table_access["chunks (in-memory index)"] || 0) : 0;
    const items = [
      {t: "Your question", n: summary.questions, s: "messages asked"},
      {t: "Conversation read", n: summary.table_access ? (summary.table_access["turns (read)"] || 0) : 0, s: "earlier context used"},
      {t: "Passages found", n: passages, s: "searches of the knowledge base"},
      {t: "Tools used", n: tools, s: "steps that checked or saved something"},
      {t: "Answers", n: summary.questions - summary.errors, s: summary.errors ? summary.errors + " could not be answered" : "all answered"},
    ];
    const flow = document.getElementById("flow");
    flow.replaceChildren();
    items.forEach((it, i) => {
      const box = el("div", "box");
      box.append(el("b", "", it.t), el("span", "n", it.n), el("small", "", it.s));
      flow.appendChild(box);
      if (i < items.length - 1) flow.appendChild(el("div", "arrow", "→"));
    });
  }

  function kpis(summary) {
    const k = document.getElementById("kpis");
    k.replaceChildren();
    [["Average time per answer", Math.round(summary.avg_total_ms / 100) / 10 + " s"],
     ["Cost so far", money(summary.cost_usd)],
     ["Questions with an error", summary.errors],
     ["Words the model read and wrote", ((summary.tokens.input + summary.tokens.output) / 1000).toFixed(1) + "k tokens"]]
      .forEach(([l, v]) => {
        const c = el("div", "kpi");
        c.append(el("div", "v", v), el("div", "l", l));
        k.appendChild(c);
      });
  }

  function timeline(flow) {
    const t = document.getElementById("timeline");
    t.replaceChildren();
    document.getElementById("detail").hidden = false;
    document.getElementById("detail-title").textContent = "What happened to this question";
    document.getElementById("detail-sub").textContent = "Recorded " + flow.ts + ", took " + Math.round(flow.total_ms / 100) / 10 + " seconds.";
    const say = {
      history_read: (s) => ["Read the conversation so far", s.turns ? s.turns + " earlier messages were used." : "This was the first message."],
      retrieve: (s) => ["Looked for matching passages", (s.hits || []).length + " passages found in the knowledge base."],
      model: (s) => ["Wrote a response", "Model call " + (s.tool_calls && s.tool_calls.length ? "that asked for " + s.tool_calls.length + " tool step(s)." : "that answered directly.")],
      tool: (s) => [TOOL[s.name] || s.name, "Result: " + (DECISION[s.decision] || s.decision) + "."],
      answer: (s) => [s.stopped ? "Stopped and asked for your approval" : "Gave the answer", s.error ? "It could not be completed." : "The answer was shown in the chat."],
    };
    (flow.steps || []).forEach((st) => {
      const [title, body] = (say[st.step] || (() => [st.step, ""]))(st);
      const row = el("div", "tl");
      row.appendChild(el("div", "dot", ""));
      const text = el("div");
      text.append(el("b", "", title), el("p", "", body));
      row.appendChild(text);
      t.appendChild(row);
    });
    document.getElementById("detail").scrollIntoView({behavior: "smooth", block: "start"});
  }

  async function load() {
    const res = await fetch("/api/flows");
    const data = await res.json();
    const s = data.summary;
    flowBoxes(s);
    kpis(s);
    bars(document.getElementById("confidence"), confidenceCounts(data.flows), (k) => k, "No answers yet.");
    bars(document.getElementById("tools"), s.tool_calls, (k) => TOOL[k] || k, "No tool was used yet.");
    const list = document.getElementById("list");
    list.replaceChildren();
    document.getElementById("empty").hidden = data.flows.length > 0;
    data.flows.forEach((f) => {
      const b = el("button", "item");
      const when = el("span", "when", "Question at " + f.ts);
      const meta = el("span", "meta", (f.error ? "Could not answer" : "Answered") + " · " + Math.round(f.total_ms / 100) / 10 + " s");
      b.append(when, meta);
      b.addEventListener("click", () => timeline(f));
      list.appendChild(b);
    });
  }
  document.getElementById("refresh").addEventListener("click", load);
  load();
})();
</script>
</body>
</html>
"""
)
