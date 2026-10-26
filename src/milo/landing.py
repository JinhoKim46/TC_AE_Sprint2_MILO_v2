"""The MILO product page at the root address: what MILO is, how it works, the demo, and how to start.

Honest by design: no invented customers, logos or testimonials. The data is fictional and the page says so.
"""

from __future__ import annotations

from milo.shell import FAVICON, SHELL_CSS, site_header

CSS = """
:root{--bg:#F5F4EF;--card:#FFFFFF;--line:#E2DFD6;--ink:#1F1E1B;--mut:#67645B;--accent:#2C6B5C;--accent-soft:#E6F0EC;--warn:#8A5418;--warn-soft:#FBF1DF}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
a{color:inherit}
.pagehead-unused{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;display:flex;align-items:center;gap:16px;flex-wrap:wrap;
  padding:12px 0;background:var(--card);border-bottom:1px solid var(--line);margin:0 -16px;padding-left:16px;padding-right:16px}
header.top .sp{flex:1}
.btn{display:inline-block;font:inherit;padding:11px 18px;border-radius:12px;border:1px solid var(--line);background:var(--card);color:var(--ink);text-decoration:none;cursor:pointer}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.btn:hover{border-color:var(--accent)}
.wrap{max-width:1080px;margin:0 auto}
section{padding:56px 0}
section+section{border-top:1px solid var(--line)}
.eyebrow{font-size:13px;text-transform:uppercase;letter-spacing:.08em;color:var(--accent);font-weight:600;margin:0 0 10px}
h1{font-size:clamp(30px,5vw,50px);line-height:1.1;margin:0 0 16px;letter-spacing:-.02em;text-wrap:balance}
h2{font-size:clamp(24px,3.4vw,34px);line-height:1.2;margin:0 0 12px;text-wrap:balance}
h3{font-size:18px;margin:0 0 6px}
p{margin:0 0 12px;max-width:66ch}
.lede{font-size:19px;color:var(--mut)}
.muted{color:var(--mut)}
.hero{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:40px;align-items:center;padding-top:64px;max-width:1080px;margin:0 auto}
.hero .ctas{display:flex;gap:12px;flex-wrap:wrap;margin-top:22px}
.hero-art{display:flex;flex-direction:column;gap:14px;align-items:center}
.hero-art img{width:min(240px,60vw);height:auto}
.mock{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px;width:100%;box-shadow:0 12px 30px rgba(31,30,27,.06)}
.mock .you{align-self:flex-end;background:var(--accent);color:#fff;border-radius:14px 14px 4px 14px;padding:8px 12px;font-size:14px;margin:0 0 10px 30%}
.mock .ans{font-size:14px;margin:0 0 10px}
.mock .cite{display:inline-block;font-size:11px;min-width:20px;text-align:center;border:1px solid var(--line);border-radius:999px;color:var(--accent);padding:0 5px;margin:0 1px}
.mock .chips{display:flex;gap:6px;flex-wrap:wrap}
.mock .chip{font-size:12px;padding:3px 9px;border-radius:999px;background:var(--accent-soft);color:var(--accent)}
.mock .chip.warn{background:var(--warn-soft);color:var(--warn)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-top:24px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}
.stat b{display:block;font-size:17px;margin-bottom:4px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;counter-reset:s;margin:0;padding:0;list-style:none}
.steps li{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;counter-increment:s}
.steps li::before{content:counter(s);display:inline-flex;width:30px;height:30px;border-radius:50%;background:var(--accent-soft);color:var(--accent);align-items:center;justify-content:center;font-weight:700;margin-bottom:10px}
.features{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.feature{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px}
.feature .tag{font-size:12px;color:var(--accent);background:var(--accent-soft);border-radius:999px;padding:2px 9px;display:inline-block;margin-bottom:10px}
.roles{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.role{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px}
.stories{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.story{display:flex;flex-direction:column;gap:8px;text-decoration:none;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px}
.story:hover{border-color:var(--accent)}
.story span{font-size:13px;color:var(--accent);font-weight:600}
.video{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:12px}
.video video{width:100%;height:auto;border-radius:12px;display:block;background:#1F1E1B}
.video .fallback{padding:40px 16px;text-align:center;color:var(--mut)}
.faq details{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 18px;margin-bottom:10px}
.faq summary{cursor:pointer;font-weight:600}
.faq details p{margin:10px 0 0}
.final{background:var(--accent);color:#fff;border-radius:22px;padding:40px 28px;text-align:center}
.final p{margin:0 auto 18px;color:#E6F0EC}
.final .btn{background:#fff;border-color:#fff;color:var(--accent)}
.toc{display:none}
@media (min-width:1360px){.toc{display:flex;flex-direction:column;align-items:flex-end;gap:14px;position:fixed;right:16px;top:50%;transform:translateY(-50%);z-index:5}}
.toc ol{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;align-items:flex-end;gap:6px}
.toc a{position:relative;display:flex;align-items:center;justify-content:flex-end;height:14px;text-decoration:none;color:var(--mut)}
.toc a::after{content:"";display:block;width:calc(16px + 16px * var(--k,0));height:calc(3px + 2px * var(--k,0));border-radius:3px;background:var(--line);transition:width .12s ease-out,height .12s ease-out}
.toc a.on::after{background:var(--accent)}
.toc a.on::after,.toc a.mag::after{background:var(--accent)}
.toc a.mag::after{background:var(--mut)}
.toc .label{position:absolute;right:40px;top:50%;transform:translateY(-50%) translateX(6px);opacity:0;pointer-events:none;white-space:nowrap;font-size:13px;background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:4px 10px;box-shadow:0 4px 14px rgba(31,30,27,.08);transition:opacity .15s ease,transform .15s ease}
.toc a.mag .label,.toc a:focus-visible .label{opacity:1;transform:translateY(-50%)}
.toc .top{height:auto;color:var(--accent);font-size:18px;line-height:1}
.toc .top::after{display:none}
footer{padding:28px 0 40px;color:var(--mut);font-size:14px;border-top:1px solid var(--line)}
footer a{margin-right:14px}
.note{background:var(--warn-soft);color:var(--warn);border-radius:12px;padding:12px 14px;font-size:14px}
.pagelinks{display:flex;gap:4px;flex-wrap:wrap}
.pagelinks a{color:var(--mut);text-decoration:none;font-size:14px;padding:6px 10px;border-radius:8px}
.pagelinks a:hover{color:var(--ink);background:var(--bg)}
@media (max-width:820px){.hero{grid-template-columns:1fr;padding-top:36px}.stats{grid-template-columns:1fr 1fr}.pagelinks,.sitenav{display:none}header.top{flex-wrap:nowrap}}
@media (max-width:520px){.stats{grid-template-columns:1fr}}
"""


def _mock() -> str:
    return (
        '<div class="mock" role="img" aria-label="Example MILO answer with numbered sources and step chips">'
        '<p class="you">We get about 40 service requests a week, 12 minutes each to assign. What could a shared queue save?</p>'
        '<p class="ans">A shared queue could save about <b>5.3 hours a week</b>, likely between 4.3 and 6.4 hours.'
        ' The estimate uses today\'s 40 requests and 12 minutes each, and assumes 4 minutes with one queue <span class="cite">1</span>.</p>'
        '<div class="chips"><span class="chip">Sources · 3</span><span class="chip">Tools · 2</span>'
        '<span class="chip">Partial match</span></div>'
        '<p class="muted" style="font-size:12px;margin:10px 0 0">Source 1: Request and dispatch management · Source 2: Past case C01</p>'
        "</div>"
    )


SECTIONS = [
    ("how", "How it works"),
    ("features", "Features"),
    ("video", "Video"),
    ("who", "Who it is for"),
    ("stories", "Demo"),
    ("faq", "FAQ"),
    ("final", "Start"),
]


def _toc() -> str:
    """The section index at the right edge (wide screens only). It marks the section in view and links back to the top."""
    items = "".join(
        f'<li><a href="#{sid}"><span class="label">{label}</span></a></li>'
        for sid, label in SECTIONS
    )
    return (
        '<nav class="toc" aria-label="On this page"><ol>' + items + "</ol>"
        '<a class="top" href="#top" aria-label="Back to top"><span class="label">Back to top</span>&uarr;</a></nav>'
        "<script>"
        "(() => {const links = [...document.querySelectorAll('.toc a[href^=\"#\"]')];"
        "const map = new Map(links.map((a) => [a.getAttribute('href').slice(1), a]));"
        "const io = new IntersectionObserver((entries) => {"
        "entries.forEach((e) => { if (e.isIntersecting && map.has(e.target.id)) {"
        "links.forEach((a) => a.classList.remove('on')); map.get(e.target.id).classList.add('on'); } });"
        "}, {rootMargin: '-40% 0px -55% 0px'});"
        "document.querySelectorAll('main section[id]').forEach((s) => io.observe(s));"
        "const nav = document.querySelector('.toc');"
        "const items = [...nav.querySelectorAll('li a')];"
        "nav.addEventListener('mousemove', (e) => {"
        "const ks = items.map((a) => { const r = a.getBoundingClientRect(); return Math.max(0, 1 - Math.abs(e.clientY - (r.top + r.height / 2)) / 90); });"
        "const best = ks.indexOf(Math.max(...ks));"
        "items.forEach((a, i) => { a.style.setProperty('--k', ks[i].toFixed(3)); a.classList.toggle('mag', i === best && ks[i] > 0.3); }); });"
        "nav.addEventListener('mouseleave', () => items.forEach((a) => { a.style.setProperty('--k', '0'); a.classList.remove('mag'); }));"
        "})();"
        "</script>"
    )


def landing_page(user=None) -> str:
    how = [
        ("Describe your work", "Tell MILO about one kind of work, in your own words."),
        (
            "It finds the passages",
            "The answer is built from matching passages in a knowledge base of service areas and past cases.",
        ),
        (
            "It checks and records",
            "Facts you state are saved. Savings are calculated in code and shown as a range.",
        ),
        (
            "You see where it came from",
            "Every answer lists its sources, and each source opens the document it came from.",
        ),
    ]
    features = [
        (
            "Sources",
            "Every claim points to a numbered passage",
            "Open any source to read the document it came from. No hidden references.",
        ),
        (
            "Estimates",
            "Ranges, calculated in code",
            "The model never invents the number. Assumed inputs are labelled, and the range is shown.",
        ),
        (
            "Control",
            "Approval before any change",
            "A tool that changes a record needs your approval first. Nothing changes silently.",
        ),
        (
            "Honesty",
            "It says when it does not know",
            "When the knowledge base has no answer, MILO says so and lists what to add.",
        ),
        (
            "Transparency",
            "Every step is shown",
            "The steps, the tools and the cost of each answer can be opened from the answer itself.",
        ),
        (
            "Resilience",
            "A local model takes over",
            "If the main model is down, a local model answers from the passages only, and cannot act.",
        ),
    ]
    roles = [
        (
            "Owners",
            "See what automation would save, in a range, before you commit to anything.",
        ),
        (
            "Dispatchers",
            "Find where requests are lost or sent twice, and which area to fix first.",
        ),
        (
            "Technicians",
            "Find the right passage for a recurring fault, with its source one click away.",
        ),
    ]
    faq = [
        (
            "Is this a real service with real customers?",
            "No. MILO is a course project. All businesses, figures and documents are fictional and written for the project.",
        ),
        (
            "Does it use my data?",
            "Only what you type in the chat, and only for your own browser session. There is no account to create.",
        ),
        (
            "Which AI model answers?",
            "The main answers come from a hosted model through OpenRouter. A local model answers when the main one is unavailable.",
        ),
        (
            "Where is the conversation stored?",
            "In a PostgreSQL database in its own schema, or in memory for demos. Each owner's data is kept apart.",
        ),
        (
            "How do I see how it works?",
            "Open the Overview. It shows the path a question takes, the cost so far, and the health of the database and models.",
        ),
        (
            "Does it give prices?",
            "No. MILO estimates time and effort only. Prices are out of scope for this project.",
        ),
    ]
    stories = [
        (
            "dispatch",
            "The same printer, two technicians",
            "Duplicate dispatch and a shared queue",
        ),
        (
            "toner",
            "We have toner, but nobody can find it",
            "Stock location and search time",
        ),
        (
            "limits",
            "When MILO should not answer",
            "A question the knowledge base cannot answer",
        ),
        (
            "approval",
            "A change that needs your approval",
            "A destructive tool waits for you",
        ),
    ]
    body = (
        site_header("home", user) + "<main>"
        '<section class="hero" id="top" style="border-top:0">'
        '<div><p class="eyebrow">Diagnosis assistant for service businesses</p>'
        "<h1>Find where your work loses time, and what to automate first.</h1>"
        '<p class="lede">MILO listens to how your team works, finds the matching passages from past cases and service areas, '
        "and shows you the savings as a range, with every source and step visible.</p>"
        '<div class="ctas"><a class="btn primary" href="/chat?new=1">Start a conversation</a>'
        '<a class="btn" href="#stories">Try a demo storyline</a></div>'
        '<div class="stats"><div class="stat"><b>Cited answers</b>Every claim names its passage</div>'
        '<div class="stat"><b>Ranges, not guesses</b>Estimates are computed in code</div></div></div>'
        '<div class="hero-art"><img src="/static/milo-mascot.svg" alt="Milo, the MILO mascot, waving" width="240" height="264">'
        f"{_mock()}</div></section>"
        '<section id="how"><div class="wrap"><p class="eyebrow">How it works</p><h2>Four steps from a conversation to a plan</h2>'
        '<ol class="steps">'
        + "".join(f'<li><h3>{t}</h3><p class="muted">{d}</p></li>' for t, d in how)
        + "</ol></div></section>"
        '<section id="features"><div class="wrap"><p class="eyebrow">Features</p><h2>Built to be checked, not just trusted</h2>'
        '<div class="features">'
        + "".join(
            f'<article class="feature"><span class="tag">{t}</span><h3>{h}</h3><p class="muted">{d}</p></article>'
            for t, h, d in features
        )
        + "</div></div></section>"
        '<section id="video"><div class="wrap"><p class="eyebrow">Video</p><h2>MILO in 40 seconds</h2>'
        '<div class="video"><video controls preload="metadata" poster="/static/milo-brag-poster.jpg" aria-label="MILO product video">'
        '<source src="/static/milo-brag.mp4" type="video/mp4">'
        '<div class="fallback">The video could not be played in this browser. Download it from the project folder.</div></video></div></div></section>'
        '<section id="who"><div class="wrap"><p class="eyebrow">Who it is for</p><h2>Three people, one shared picture</h2>'
        '<div class="roles">'
        + "".join(
            f'<article class="role"><h3>{t}</h3><p class="muted">{d}</p></article>'
            for t, d in roles
        )
        + "</div></div></section>"
        '<section id="stories"><div class="wrap"><p class="eyebrow">Demo</p><h2>Four storylines to try</h2>'
        '<p class="muted">Each storyline runs a short, scripted conversation in the chat. Try one, then open its sources.</p>'
        '<div class="stories">'
        + "".join(
            f'<a class="story" href="/chat?new=1&story={sid}"><span>Storyline</span><b>{t}</b><span class="muted" style="color:var(--mut);font-weight:400">{d}</span></a>'
            for sid, t, d in stories
        )
        + "</div></div></section>"
        '<section id="faq"><div class="wrap"><p class="eyebrow">FAQ</p><h2>Questions people ask first</h2><div class="faq">'
        + "".join(
            f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq
        )
        + "</div></div></section>"
        '<section id="final"><div class="wrap"><div class="final"><h2>See how one answer is made</h2>'
        "<p>Ask a question about your work, then open the steps and the sources behind the answer.</p>"
        '<a class="btn" href="/chat?new=1">Open the chat</a> <a class="btn" href="/dashboard" style="margin-left:8px">Open the overview</a>'
        "</div></div></section>"
        "</main>"
        + _toc()
        + '<footer class="wrap"><div class="note">A course project. All businesses, figures and documents are fictional.</div>'
        '<p style="margin-top:14px"><a href="/chat?new=1">Chat</a><a href="/dashboard">Overview</a><a href="/kb">Knowledge base</a></p></footer>'
    )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="claude:viewport-fit-sides" content="cover">'
        f"<title>MILO · Diagnosis assistant</title>{FAVICON}"
        f"<style>{SHELL_CSS}{CSS}</style></head><body>{body}</body></html>"
    )
