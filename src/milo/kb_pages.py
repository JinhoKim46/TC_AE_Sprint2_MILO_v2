"""Pages that show the knowledge base: an index of the documents and one page per document.

Only files under data/kb can be read; the requested id is checked against that folder before anything is opened.
"""

from __future__ import annotations

import re
from html import escape
from pathlib import Path

from milo.chunk import front_matter
from milo.shell import FAVICON, SHELL_CSS, site_header

KB = Path(__file__).resolve().parents[2] / "data" / "kb"
SECTION_LABEL = {
    "solutions": "Service areas",
    "cases": "Past cases",
    "consultation": "Method notes",
    "policies": "Policies",
}
PAGE_CSS = (
    """
:root{--bg:#F5F4EF;--card:#FFFFFF;--line:#E2DFD6;--ink:#1F1E1B;--mut:#6B6860;--accent:#2F6B5E;--accent-soft:#E7F0EC}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.pagehead-unused{display:flex;align-items:center;gap:16px;flex-wrap:wrap;padding:14px 0;border-bottom:1px solid var(--line);background:var(--card);margin:0 -16px;padding-left:16px;padding-right:16px}
header .sp{flex:1}
main{max-width:860px;margin:0 auto;padding:24px 0 56px;display:flex;flex-direction:column;gap:18px}
h1{font-size:28px;margin:0;line-height:1.2}
h2{font-size:17px;margin:20px 0 8px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px}
.muted{color:var(--mut);font-size:14px}
.pill{display:inline-block;font-size:12px;padding:3px 9px;border-radius:999px;background:var(--accent-soft);color:var(--accent)}
.doc p{max-width:70ch;margin:0 0 12px}
.doc h2{font-size:18px}
.doc h3{font-size:16px}
.list a{display:block;padding:10px 0;border-top:1px solid var(--line);color:var(--ink);text-decoration:none}
.list a:first-child{border-top:0}
.list a:hover b{color:var(--accent)}
.note{background:var(--accent-soft);border-radius:10px;padding:10px 12px;font-size:14px}
"""
    + SHELL_CSS
)


def _paragraphs(body: str) -> str:
    out = []
    for block in re.split(r"\n\s*\n", body.strip()):
        lines = [ln.rstrip() for ln in block.split("\n") if ln.strip()]
        if not lines:
            continue
        if lines[0].startswith("#"):
            level = min(len(lines[0]) - len(lines[0].lstrip("#")), 3)
            text = lines[0].lstrip("#").strip()
            rest = " ".join(lines[1:])
            out.append(f"<h{level + 1}>{escape(text)}</h{level + 1}>")
            if rest:
                out.append(f"<p>{escape(rest)}</p>")
            continue
        if all(ln.lstrip().startswith(("-", "*")) for ln in lines):
            items = "".join(
                f"<li>{escape(ln.lstrip()[1:].strip())}</li>" for ln in lines
            )
            out.append(f"<ul>{items}</ul>")
            continue
        out.append(f"<p>{escape(' '.join(lines))}</p>")
    return "\n".join(out)


def _documents() -> list[dict[str, str]]:
    docs = []
    for p in sorted(KB.rglob("*.md")):
        meta, body = front_matter(p.read_text())
        doc_id = p.relative_to(KB).with_suffix("").as_posix()
        docs.append(
            {
                "id": doc_id,
                "title": meta.get("title", doc_id),
                "section": meta.get("section", ""),
                "meta": meta,
                "body": body,
            }
        )
    return docs


def index_page(user=None) -> str:
    groups: dict[str, list[dict[str, str]]] = {}
    for d in _documents():
        groups.setdefault(d["section"], []).append(d)
    sections = []
    for section, items in groups.items():
        rows = "".join(
            f'<a href="/kb/{escape(d["id"])}"><b>{escape(d["title"])}</b><br><span class="muted">{escape(d["id"])}</span></a>'
            for d in items
        )
        label = SECTION_LABEL.get(section, section.title())
        sections.append(
            f'<section class="card"><h2>{escape(label)} ({len(items)})</h2><div class="list">{rows}</div></section>'
        )
    body = (
        f"{site_header('kb', user)}"
        "<main><h1>Knowledge base</h1>"
        '<p class="muted">The passages MILO can use. All documents are fictional. Open one to read the text that an answer may cite.</p>'
        + "".join(sections)
        + "</main>"
    )
    return _page("MILO knowledge base", body)


def document_page(doc_id: str, user=None) -> str | None:
    path = (KB / f"{doc_id}.md").resolve()
    if KB.resolve() not in path.parents or not path.is_file():
        return None
    meta, body = front_matter(path.read_text())
    title = meta.get("title", doc_id)
    facts = " · ".join(
        x
        for x in [
            SECTION_LABEL.get(meta.get("section", ""), meta.get("section", "")),
            f"product {meta['product']}" if meta.get("product") else "",
            f"updated {meta['updated']}" if meta.get("updated") else "",
            meta.get("review_status", "").replace("_", " "),
        ]
        if x
    )
    note = (
        '<div class="note">Synthetic teaching document, written for this project. It is not a real customer record.</div>'
        if meta.get("synthetic", "").lower() == "true"
        else ""
    )
    body_html = (
        f"{site_header('kb', user)}"
        "<main>"
        '<p><a href="/kb">Knowledge base</a> / ' + escape(doc_id) + "</p>"
        f"<h1>{escape(title)}</h1>"
        f'<p class="muted"><span class="pill">{escape(doc_id)}</span> {escape(facts)}</p>'
        f"{note}"
        f'<section class="card doc">{_paragraphs(body)}</section>'
        "</main>"
    )
    return _page(title, body_html)


def _page(title: str, body: str) -> str:
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        f"<title>{escape(title)} · MILO</title>{FAVICON}<style>{PAGE_CSS}</style></head>"
        f"<body>{body}</body></html>"
    )
