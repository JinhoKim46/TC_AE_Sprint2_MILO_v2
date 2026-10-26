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
<!--FAVICON-->
<style>
"""
    + _BASE_CSS
    + """
.layout{display:grid;grid-template-columns:240px minmax(0,1fr);height:calc(100vh - 57px);min-height:0;overflow:hidden}
.panel{background:var(--card);border-left:1px solid var(--line);position:fixed;top:57px;right:0;bottom:0;width:min(380px,100vw);z-index:12;display:flex;flex-direction:column;min-height:0;transform:translateX(105%);transition:transform .2s ease;box-shadow:-8px 0 24px rgba(31,30,27,.08)}
.panel.open{transform:none}
.panel-head{display:flex;align-items:center;gap:12px;padding:14px 20px;border-bottom:1px solid var(--line)}
.panel-head h2{font-size:16px;flex:1}
.panel-body{flex:1;min-height:0;overflow-y:auto;padding:16px 20px 24px;display:flex;flex-direction:column;gap:16px}
.panel .stages{grid-template-columns:repeat(2,minmax(0,1fr))}
.answer{cursor:pointer}
.answer.is-active{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
.answer-tag{font-size:12px;color:var(--mut);text-transform:uppercase;letter-spacing:.06em}
.answer.is-active .answer-tag{color:var(--accent);font-weight:600}
.src-read{font:inherit;font-size:13px;color:var(--accent);background:none;border:0;padding:0;margin-right:14px;cursor:pointer;text-decoration:underline}
.doc-viewer{width:min(780px,92vw);max-height:82vh;padding:0;border:1px solid var(--line);border-radius:16px;background:var(--card);color:var(--ink);overflow:hidden;display:flex;flex-direction:column}
.doc-viewer::backdrop{background:rgba(31,30,27,.35)}
.doc-head{display:flex;align-items:center;gap:12px;padding:14px 18px;border-bottom:1px solid var(--line)}
.doc-head b{flex:1}
.doc-text{padding:18px 22px 28px;white-space:pre-wrap;font-size:15px;line-height:1.75;overflow:auto;min-height:0}
.doc-text{white-space:normal}
.doc-text p,.doc-text li{max-width:70ch}
.doc-text .hit{background:var(--accent-soft);border-radius:6px;padding:4px 8px;margin-left:-8px;margin-right:-8px}
#sources-toggle{display:none}
@media (max-width:1179px){#sources-toggle{display:inline-block}}
@media (min-width:1180px){
  .layout{grid-template-columns:240px minmax(0,1fr) 380px}
  .panel{position:static;transform:none;width:auto;box-shadow:none;transition:none}
  #panel-close{display:none}
}
.side{background:var(--card);border-right:1px solid var(--line);padding:18px 16px;display:flex;flex-direction:column;gap:20px;min-height:0;overflow-y:auto}
.brand{font-size:18px;font-weight:700}
.brand span{display:block;font-size:13px;font-weight:400;color:var(--mut)}
.how h3{font-size:13px;color:var(--mut);text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px}
.how ol{margin:10px 0 0;padding:0;list-style:none;display:flex;flex-direction:column;gap:8px}
.how li{display:flex;gap:10px;font-size:14px}
.how b{display:block}
.num{flex:0 0 26px;height:26px;border-radius:50%;background:var(--accent-soft);color:var(--accent);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px}
.demo h3{font-size:13px;color:var(--mut);text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px}
.demo-list{display:flex;flex-direction:column;gap:8px}
.demo-list button{text-align:left;font-size:14px;padding:10px 12px;line-height:1.35}
.demo-list button small{display:block;color:var(--mut);font-size:12px;margin-top:2px}
.main{display:flex;flex-direction:column;min-width:0;min-height:0}
.topbar{padding:14px 24px;background:var(--card);border-bottom:1px solid var(--line);display:flex;align-items:center;gap:12px}
.topbar h1{font-size:17px}
.topbar .spacer{flex:1}
.thread{flex:1;overflow-y:auto;padding:28px 24px 12px}
.inner{max-width:780px;margin:0 auto;display:flex;flex-direction:column;gap:22px}
.hello{text-align:center;margin:40px auto 0;max-width:600px;display:flex;flex-direction:column;gap:12px}
.hello h2{font-size:24px}
.starters{display:grid;gap:8px;margin-top:12px;text-align:left}
.starters button{text-align:left;padding:12px 16px;line-height:1.45;border-radius:12px}
.you{align-self:flex-end;max-width:78%;background:var(--accent);color:#fff;padding:11px 16px;border-radius:18px 18px 4px 18px;white-space:pre-wrap;word-break:break-word}
.answer{background:var(--card);border:1px solid var(--line);border-radius:18px 18px 18px 4px;padding:18px 20px;display:flex;flex-direction:column;gap:14px}
.answer .text{white-space:pre-wrap;word-break:break-word;font-size:16px}
.trust{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.trust .label{font-size:14px;color:var(--mut)}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.feedback{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:13px}
.cite{font:inherit;font-size:12px;min-width:22px;height:22px;padding:0 6px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--accent);cursor:pointer;vertical-align:middle;line-height:20px}
.cite:hover{border-color:var(--accent)}
.cite.static{cursor:default}
.sources{margin:0;padding-left:0;list-style:none;display:flex;flex-direction:column;gap:10px}
.source{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.source:focus{outline:none}
.source.flash{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
.src-head{display:flex;gap:8px;align-items:center}
.src-excerpt{margin:6px 0;font-size:14px}
.src-link{font-size:13px;color:var(--accent);text-decoration:none}
.src-link:hover{text-decoration:underline}
.stage-detail{margin-top:4px}
.md-h{font-size:15px;margin:10px 0 4px}
.md-list{margin:6px 0;padding-left:22px}
.text code{font:13px ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--bg);padding:1px 5px;border-radius:4px}
.chip{font:inherit;font-size:13px;padding:6px 12px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}
.chip:hover{border-color:var(--accent)}
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
.composer-wrap{border-top:1px solid var(--line);background:var(--card);padding:12px 24px 16px;flex:0 0 auto}
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
<!--HEADER-->
<div class="layout">
  <aside class="side">

    <div class="demo">
      <h3>Demo storylines</h3>
      <div id="demos" class="demo-list"></div>
    </div>
  </aside>

  <main class="main">
    <header class="topbar">
      <h1>Diagnosis chat</h1>
      <span class="spacer"></span>
      <button class="button" id="sources-toggle" type="button" aria-controls="panel">Sources</button>
      <a class="button" href="/chat?new=1" id="new">New conversation</a>
      <span class="muted" id="cost" hidden></span>
    </header>

    <section class="thread" id="thread" aria-live="polite" aria-label="Conversation"></section>

    <div class="composer-wrap">
      <div class="working" id="working" role="status"></div>
      <form class="composer" id="composer">
        <label class="sr" for="question">Your message</label>
        <textarea id="question" rows="1" maxlength="4000" placeholder="Describe your work or ask"></textarea>
        <button class="primary" id="send" type="submit">Send</button>
      </form>
    </div>
  </main>

  <aside class="panel" id="panel" aria-label="Sources and steps">
    <div class="panel-head">
      <h2>Sources and steps</h2>
      <button class="button" id="panel-close" type="button">Close</button>
    </div>
    <div class="panel-body" id="panel-body"></div>
  </aside>
</div>

<script>
(() => {
  const thread = document.getElementById("thread");
  const form = document.getElementById("composer");
  const input = document.getElementById("question");
  const send = document.getElementById("send");
  const working = document.getElementById("working");
  const costEl = document.getElementById("cost");
  const sourcesPanel = document.getElementById("panel");
  const panelBody = document.getElementById("panel-body");
  const sourcesToggle = document.getElementById("sources-toggle");
  let activeKey = null;

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

  function feedbackRow() {
    const row = el("div", "feedback");
    row.appendChild(el("span", "muted", "Was this answer useful?"));
    const up = el("button", "chip", "Yes");
    const down = el("button", "chip", "No");
    up.type = "button";
    down.type = "button";
    const reasons = el("div", "chips");
    reasons.hidden = true;
    const thanks = el("span", "muted", "");
    thanks.setAttribute("role", "status");
    const send = (rating, reason) => {
      fetch("/api/feedback", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({rating, reason})})
        .then((r) => { thanks.textContent = r.ok ? "Thank you. This goes to the evaluation log, without your question text." : "Feedback could not be saved."; })
        .catch(() => { thanks.textContent = "Feedback could not be saved."; });
      up.disabled = true;
      down.disabled = true;
      reasons.hidden = true;
    };
    up.addEventListener("click", () => send("up", ""));
    down.addEventListener("click", () => { reasons.hidden = false; });
    [["wrong", "Wrong"], ["outdated", "Outdated"], ["missing_source", "Missing source"], ["hard_to_follow", "Hard to follow"]].forEach(([key, label]) => {
      const b = el("button", "chip", label);
      b.type = "button";
      b.addEventListener("click", () => send("down", key));
      reasons.appendChild(b);
    });
    row.append(up, down, thanks, reasons);
    return row;
  }

  // Minimal, safe Markdown: text is added with textContent, and only a fixed set of tags is created.
  function inline(text, m, parent) {
    const parts = String(text).split(/(\\*\\*[^*\\n]+\\*\\*|`[^`\\n]+`|\\*[^*\\n]+\\*|\\[\\d+\\])/g);
    parts.forEach((part) => {
      if (!part) return;
      if (/^\\*\\*[^*]+\\*\\*$/.test(part)) parent.appendChild(el("strong", "", part.slice(2, -2)));
      else if (/^`[^`]+`$/.test(part)) parent.appendChild(el("code", "", part.slice(1, -1)));
      else if (/^\\*[^*]+\\*$/.test(part)) parent.appendChild(el("em", "", part.slice(1, -1)));
      else if (/^\\[\\d+\\]$/.test(part) && m.key !== undefined) {
        const n = Number(part.slice(1, -1));
        const b = el("button", "cite", String(n));
        b.type = "button";
        const src = (m.sources || [])[n - 1];
        b.title = src ? docTitle(src.doc_id) : "Source " + n;
        b.setAttribute("aria-label", "Source " + n + ": " + b.title);
        b.addEventListener("click", () => highlightSource(m, n));
        parent.appendChild(b);
      } else parent.appendChild(document.createTextNode(part));
    });
    return parent;
  }

  function renderMarkdown(m) {
    const wrap = el("div", "text");
    let list = null;
    let para = null;
    String(m.text || "").split("\\n").forEach((raw) => {
      const line = raw.trimEnd();
      const heading = line.match(/^(#{1,3})\\s+(.*)$/);
      const bullet = line.match(/^\\s*[-*]\\s+(.*)$/);
      const ordered = line.match(/^\\s*\\d+[.)]\\s+(.*)$/);
      if (!line.trim()) { list = null; para = null; return; }
      if (heading) {
        list = null; para = null;
        inline(heading[2], m, wrap.appendChild(el("h4", "md-h")));
      } else if (bullet || ordered) {
        const tag = bullet ? "ul" : "ol";
        if (!list || list.tagName.toLowerCase() !== tag) { list = el(tag, "md-list"); wrap.appendChild(list); }
        para = null;
        inline((bullet || ordered)[1], m, list.appendChild(el("li")));
      } else {
        if (!para) { para = wrap.appendChild(el("p")); list = null; }
        inline(line + " ", m, para);
      }
    });
    return wrap;
  }

  function openPanel(on) {
    sourcesPanel.classList.toggle("open", on);
  }

  function activeMessage() {
    const answers = messages.filter((m) => m.role === "assistant" && !m.error);
    return answers.find((m) => m.key === activeKey) || answers[answers.length - 1] || null;
  }

  function setActive(key) {
    activeKey = key;
    thread.querySelectorAll("article.answer").forEach((c) => c.classList.toggle("is-active", c.dataset.key === String(key)));
    renderPanel();
  }

  function renderPanel() {
    const m = activeMessage();
    const count = m ? (m.sources || []).length : 0;
    sourcesToggle.textContent = count ? "Sources (" + count + ")" : "Sources";
    panelBody.replaceChildren();
    if (!m) {
      panelBody.appendChild(el("p", "muted", "The sources and steps behind each answer appear here."));
      return;
    }
    const number = messages.filter((x) => x.role === "assistant" && !x.error).indexOf(m) + 1;
    panelBody.appendChild(el("h3", "", "Answer " + number));
    if (m.question) panelBody.appendChild(el("p", "muted", "To: " + m.question.slice(0, 140)));
    const c = confidence(m.sources || []);
    const trust = el("div", "trust");
    trust.append(el("span", "label", "How sure:"), el("span", "pill " + c.level, c.text));
    panelBody.appendChild(trust);

    const stages = el("div", "stages");
    stageSummary(m).forEach((st, idx) => {
      const box = el("button", "stage");
      box.type = "button";
      box.setAttribute("aria-expanded", m.openStage === idx ? "true" : "false");
      box.append(el("b", "", st.title), el("span", "n", st.n), el("span", "muted", st.note));
      box.addEventListener("click", () => { m.openStage = m.openStage === idx ? null : idx; renderPanel(); });
      stages.appendChild(box);
    });
    panelBody.appendChild(stages);
    if (m.openStage !== undefined && m.openStage !== null) panelBody.appendChild(stageDetail(m, m.openStage));

    if (count) panelBody.appendChild(sourceList(m));
    else panelBody.appendChild(el("p", "muted", "No passage was used for this answer."));

    if ((m.tool_results || []).length) {
      const steps = el("div", "found");
      steps.appendChild(el("h3", "", "What MILO did"));
      m.tool_results.forEach((t) => steps.appendChild(toolLine(t)));
      panelBody.appendChild(steps);
    }
  }

  function highlightSource(m, n) {
    setActive(m.key);
    openPanel(true);
    const target = document.getElementById("src-" + m.key + "-" + n);
    if (!target) return;
    target.scrollIntoView({behavior: "smooth", block: "center"});
    target.classList.remove("flash");
    void target.offsetWidth;
    target.classList.add("flash");
    target.focus({preventScroll: true});
  }

  function sourceList(m) {
    const box = el("div", "found");
    box.appendChild(el("h3", "", "Sources for this answer"));
    const list = el("ol", "sources");
    (m.sources || []).forEach((src, i) => {
      const n = i + 1;
      const item = el("li", "source");
      item.id = "src-" + m.key + "-" + n;
      item.tabIndex = -1;
      const head = el("div", "src-head");
      head.append(el("span", "cite static", String(n)), el("b", "", docTitle(src.doc_id)));
      item.append(head, el("div", "muted", docSection(src.doc_id)));
      const short = src.text.length > 320 ? src.text.slice(0, 320) + "..." : src.text;
      item.appendChild(renderMarkdown({text: short, sources: []}));
      const read = el("button", "src-read", "Read in the full document");
      read.type = "button";
      read.addEventListener("click", () => openDocument(src));
      const link = el("a", "src-link", "Open the page");
      link.href = "/kb/" + src.doc_id;
      link.target = "_blank";
      link.rel = "noopener";
      item.append(read, link);
      list.appendChild(item);
    });
    box.appendChild(list);
    return box;
  }

  function stageDetail(m, idx) {
    const box = el("div", "found stage-detail");
    const sources = m.sources || [];
    const tools = m.tool_results || [];
    if (idx === 0) {
      box.appendChild(el("h3", "", "Read the conversation"));
      box.appendChild(el("p", "", m.history_turns ? "MILO read " + m.history_turns + " earlier messages from this conversation, so that follow-up questions make sense." : "This was the first message, so there was no earlier conversation to read."));
    } else if (idx === 1) {
      box.appendChild(el("h3", "", "Passages found"));
      if (!sources.length) box.appendChild(el("p", "", "No passage matched this question closely enough to be used."));
      sources.forEach((src, i) => box.appendChild(el("p", "", (i + 1) + ". " + docTitle(src.doc_id))));
    } else if (idx === 2) {
      box.appendChild(el("h3", "", "What MILO used tools for"));
      if (!tools.length) box.appendChild(el("p", "", "No tool was needed for this answer."));
      tools.forEach((t) => {
        const d = DECISION[t.policy_decision];
        box.appendChild(el("p", "", (TOOL[t.name] || t.name) + " (" + (d ? d[1] : t.policy_decision) + ")"));
      });
    } else {
      box.appendChild(el("h3", "", "How the answer was written"));
      box.appendChild(el("p", "", "The answer was written only from the passages above. Each number in the text points to a source in the list."));
    }
    return box;
  }

  let viewer = null;

  async function openDocument(src) {
    if (!viewer) {
      viewer = el("dialog", "doc-viewer");
      viewer.setAttribute("aria-label", "Document");
      document.body.appendChild(viewer);
    }
    viewer.replaceChildren(el("p", "muted", "Loading the document..."));
    viewer.showModal();
    try {
      const res = await fetch("/api/kb/" + src.doc_id);
      if (!res.ok) throw new Error("not found");
      const doc = await res.json();
      const head = el("div", "doc-head");
      const close = el("button", "button", "Close");
      close.type = "button";
      close.addEventListener("click", () => viewer.close());
      head.append(el("b", "", doc.title), el("span", "muted", docSection(src.doc_id)), close);
      const body = el("div", "doc-text");
      body.appendChild(renderMarkdown({text: doc.text, sources: []}));
      viewer.replaceChildren(head, body);
      // The blocks that hold the passage are highlighted; the text around them stays visible for context.
      const plain = (t) => t.replace(/^\\s*-\\s+/gm, "").replace(/[*#`]/g, "").replace(/\\s+/g, " ").trim().toLowerCase();
      const lines = src.text.split("\\n").filter((line) => line.trim());
      const blocks = [...body.querySelectorAll("p, li, h2, h3, h4")];
      const first = blocks.findIndex((b) => plain(b.textContent).includes(plain(lines[0])));
      const last = blocks.findIndex((b, i) => i >= Math.max(first, 0) && plain(b.textContent).includes(plain(lines[lines.length - 1])));
      if (lines.length && first >= 0) {
        blocks.slice(first, (last >= first ? last : first) + 1).forEach((b) => b.classList.add("hit"));
        blocks[first].scrollIntoView({block: "center"});
      }
    } catch (err) {
      viewer.replaceChildren(el("p", "muted", "The document could not be loaded."));
    }
  }

  function docSection(docId) {
    const kind = String(docId).split("/")[0];
    return ({solutions: "Service area", cases: "Past case", consultation: "Method note", policies: "Policy"})[kind] || "Document";
  }

  function answerCard(m) {
    const card = el("article", "answer");
    if (m.error) {
      const n = el("div", "notice", m.text);
      n.setAttribute("role", "alert");
      card.appendChild(n);
      return card;
    }
    if (m.unanswered) {
      const box = el("div", "notice");
      box.appendChild(el("b", "", "Not enough information in the knowledge base."));
      box.appendChild(el("div", "", "Nothing in MILO's passages answers this. Next steps: describe the kind of work and the service area it belongs to, or ask about one of the four service areas."));
      card.appendChild(box);
      return card;
    }
    card.dataset.key = String(m.key);
    const number = messages.filter((x) => x.role === "assistant" && !x.error).indexOf(m) + 1;
    card.appendChild(el("div", "answer-tag", "Answer " + number));
    if (activeMessage() && activeMessage().key === m.key) card.classList.add("is-active");
    card.addEventListener("click", (e) => {
      if (!e.target.closest("button, a, details, summary, textarea, input")) setActive(m.key);
    });
    card.appendChild(renderMarkdown(m));

    const c = confidence(m.sources || []);
    const trust = el("div", "trust");
    trust.appendChild(el("span", "label", "How sure:"));
    const pill = el("span", "pill " + c.level, c.text);
    pill.title = "Based on how closely the best passage matches your question. It is not a probability that the answer is right.";
    trust.appendChild(pill);
    card.appendChild(trust);

    if (m.stopped) card.appendChild(el("div", "approval", "MILO needs your approval before it changes anything. Nothing was changed."));

    const follow = el("div", "chips");
    const shorter = el("button", "chip", "Shorter answer");
    shorter.type = "button";
    shorter.addEventListener("click", () => { if (!busy && m.question) ask("In two sentences: " + m.question); });
    const sources = el("button", "chip", "Show the sources");
    sources.type = "button";
    sources.addEventListener("click", () => { setActive(m.key); openPanel(true); });
    follow.append(shorter, sources);
    card.appendChild(follow);
    card.appendChild(feedbackRow());

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
      hello.appendChild(el("h2", "", "Describe one kind of work to start"));
      hello.appendChild(el("p", "muted", "MILO finds the matching passages, saves what you tell it, and gives the saving as a range with every step shown."));
      hello.appendChild(el("p", "muted", "It cannot diagnose your systems from a chat alone, and it does not give prices."));
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
    renderPanel();
  }

  sourcesToggle.addEventListener("click", () => openPanel(!sourcesPanel.classList.contains("open")));
  document.getElementById("panel-close").addEventListener("click", () => openPanel(false));

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
        question,
        unanswered: !data.error && (data.sources || []).length === 0 && String(data.answer || "").startsWith("I do not know"),
        text: data.answer || "",
        sources: data.sources || [],
        tool_results: data.tool_results || [],
        cost_usd: data.cost_usd || 0,
        stopped: !!data.stopped,
        trace: data.trace || [],
        history_turns: ((data.trace || []).find((x) => x.step === "history_read") || {turns: 0}).turns,
        error: data.error ? "Something went wrong on our side. Please try again in a moment." : null,
      };
      reply.key = messages.length;
      activeKey = reply.key;
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
      (data.turns || []).forEach((t, i) => messages.push({role: t.role === "user" ? "user" : "assistant", text: t.content, sources: t.sources || [], tool_results: [], cost_usd: 0, trace: [], key: i}));
    } catch (err) {
      /* history is optional */
    }
    render();
  }
  async function loadDemos() {
    try {
      const res = await fetch("/api/demo");
      const data = await res.json();
      const list = document.getElementById("demos");
      list.replaceChildren();
      (data.storylines || []).forEach((st) => {
        const b = el("button", "");
        b.type = "button";
        b.append(el("span", "", st.title), el("small", "", st.steps.length + (st.steps.length === 1 ? " question" : " questions")));
        b.addEventListener("click", () => { window.location.href = "/chat?new=1&story=" + encodeURIComponent(st.id); });
        list.appendChild(b);
      });
      const wanted = new URLSearchParams(window.location.search).get("story");
      const chosen = (data.storylines || []).find((st) => st.id === wanted);
      if (chosen) {
        const button = [...list.children].find((c) => c.textContent.startsWith(chosen.title));
        history.replaceState(null, "", "/chat");
        if (button) runStory(chosen, button);
      }
    } catch (err) {
      /* demos are optional */
    }
  }

  async function runStory(st, button) {
    if (busy) return;
    button.disabled = true;
    for (const q of st.steps) {
      await ask(q);
    }
    button.disabled = false;
    input.focus();
  }

  loadHistory();
  loadDemos();
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
<title>MILO · Overview</title>
<!--FAVICON-->
<style>
"""
    + _BASE_CSS
    + """
.pagehead-unused{padding:18px 28px;background:var(--card);border-bottom:1px solid var(--line);display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.pagetitle h1{font-size:22px;margin:0}
.pagetitle{margin-bottom:6px}

main{max-width:1100px;margin:0 auto;padding:24px 20px 48px;display:flex;flex-direction:column;gap:22px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px}
.card h2{font-size:17px;margin-bottom:6px}
.card .sub{color:var(--mut);font-size:14px;margin-bottom:14px}
.flow{display:flex;flex-wrap:wrap;gap:8px;align-items:stretch}
.flow .box{background:var(--bg);border-radius:14px;padding:14px;display:flex;flex-direction:column;gap:6px;border:1px solid var(--line);flex:1 1 150px;min-width:0}
.flow .box b{font-size:14px}
.flow .box .n{font-size:26px;font-weight:700;color:var(--accent)}
.flow .box small{color:var(--mut);font-size:13px}
.flow .arrow{align-self:center;color:var(--mut);font-size:22px;padding:0 2px}
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
.status-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.svc{background:var(--bg);border-radius:14px;padding:14px;display:flex;flex-direction:column;gap:4px}
.svc b{font-size:15px}
.svc small{color:var(--mut);font-size:13px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;background:var(--mut);vertical-align:middle}
.dot.ok{background:var(--accent)}
.dot.bad{background:var(--low)}
.spend{margin-top:14px;font-size:14px}
.spend .track{background:var(--bg);border-radius:8px;height:14px;overflow:hidden;margin:6px 0}
.spend .fill{background:var(--accent);height:100%;border-radius:8px}
@media (max-width:860px){.flow{grid-template-columns:1fr}.flow .arrow{display:none}.kpis{grid-template-columns:1fr 1fr}.two{grid-template-columns:1fr}.bars .bar{grid-template-columns:120px 1fr 30px}}
</style>
</head>
<body>
<!--HEADER-->
<main>
  <div class="pagetitle"><h1>Overview: every account, every question</h1><p class="sub">Only the owner sees this page. Figures come from the database.</p></div>
  <section class="card" id="status-card">
    <h2>System status</h2>
    <p class="sub">Live checks of the parts MILO depends on, and spend against the course cap.</p>
    <div class="status-grid" id="status-grid"></div>
    <div class="spend" id="spend"></div>
  </section>

  <section class="card">
    <h2>The path every question takes</h2>
    <p class="sub">Counts cover every account. Each step is a real part of the system.</p>
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
    <h2>Questions from all accounts</h2>
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
      const when = el("span", "when", (f.account || "account") + " · " + f.ts);
      const meta = el("span", "meta", (f.error ? "Could not answer" : "Answered") + " · " + Math.round(f.total_ms / 100) / 10 + " s");
      b.append(when, meta);
      b.addEventListener("click", () => timeline(f));
      list.appendChild(b);
    });
  }
  document.getElementById("refresh").addEventListener("click", load);
  async function loadStatus() {
    try {
      const res = await fetch("/api/status");
      const d = await res.json();
      const grid = document.getElementById("status-grid");
      grid.replaceChildren();
      const db = d.store.database;
      const card = (title, ok, detail) => {
        const c = el("div", "svc");
        const head = el("b", "");
        head.append(el("span", "dot " + (ok ? "ok" : "bad")), title);
        c.append(head, el("small", "", detail));
        grid.appendChild(c);
      };
      if (db) {
        card("Database", db.reachable, db.reachable
          ? "Supabase PostgreSQL, " + db.latency_ms + " ms. " + db.threads + " conversations, " + db.turns + " messages, " + db.facts + " facts, " + db.diagnoses + " diagnoses."
          : "Not reachable (" + (db.error || "error") + ").");
      } else {
        card("Storage", true, "In memory. Lost on restart. Set MILO_STORE=postgres for the database.");
      }
      const m = d.models.primary;
      card("Primary model", m.key_set && m.live_enabled, m.model + (m.key_set && m.live_enabled ? ". Live calls on." : ". Live calls off or key missing."));
      const f = d.models.fallback;
      card("Local fallback", f.reachable, f.reachable ? "Ollama is running. Models: " + (f.models || []).join(", ") + "." : "Ollama is not reachable.");
      const sp = d.spend;
      const pct = Math.min(100, (sp.web_cost_usd / sp.course_cap_usd) * 100);
      const spend = document.getElementById("spend");
      spend.replaceChildren();
      spend.append(el("div", "", "Spend on web answers: " + money(sp.web_cost_usd) + " over " + sp.web_answers + " answers, against a course cap of $" + sp.course_cap_usd.toFixed(2) + "."));
      const track = el("div", "track");
      const fill = el("div", "fill");
      fill.style.width = Math.max(1, pct).toFixed(2) + "%";
      track.appendChild(fill);
      spend.appendChild(track);
      spend.appendChild(el("small", "muted", sp.note));
    } catch (err) {
      document.getElementById("status-grid").replaceChildren(el("div", "empty", "Status could not be read. Is the server running?"));
    }
  }
  document.getElementById("refresh").addEventListener("click", () => { load(); loadStatus(); });
  loadStatus();
  load();
})();
</script>
</body>
</html>
"""
)
