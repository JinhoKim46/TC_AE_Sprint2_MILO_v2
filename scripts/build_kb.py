"""Render the synthetic knowledge package into knowledge-base articles (M0).

    uv run python scripts/build_kb.py            write data/kb/cases/ and the method article
    uv run python scripts/build_kb.py --check    exit 1 when the written files differ from a fresh render

Input: the owner's package in data/source/milo_synthetic_kb_v1/ (cases, playbooks and blueprints as JSON). The
package's own Markdown mirrors and pre-made retrieval records are not used here.

What the render changes, and why:
- JSON becomes prose with headings, so embeddings see sentences, not keys and quotes.
- Each case family (case, playbook and blueprint of one number) becomes one article: the package repeats most of a
  case's text in its playbook and blueprint, so three files would compete for the same questions. A sentence is
  written once per article, in its most natural section.
- Text that repeats in BOILERPLATE_MIN or more families (method notes, rollout steps, cautions) is written once in
  consultation/method-notes.md and left out of the cases, so cases do not look alike.
- The package's mapping to MILO v1 modules (`capability_boundary`) and its status flags are dropped; each document's
  `product` is the v2 module from data/catalogue.yaml.
- Labels stay: every article says it is synthetic and carries the package's review status.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "data" / "source" / "milo_synthetic_kb_v1"
KB = ROOT / "data" / "kb"
CATALOGUE = ROOT / "data" / "catalogue.yaml"
UPDATED = "2026-10-23"
BOILERPLATE_MIN = 4
NOTE = (
    "> Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong "
    "to this fictional business only; ask the owner rather than assume they apply."
)


def load_families() -> list[dict[str, dict[str, Any]]]:
    """The 20 case families: case, playbook and blueprint of the same number."""
    out = []
    for i in range(1, 21):
        out.append(
            {
                kind: json.loads((PKG / kind / f"{prefix}{i:02d}.json").read_text())
                for kind, prefix in (
                    ("cases", "C"),
                    ("playbooks", "P"),
                    ("blueprints", "B"),
                )
            }
        )
    return out


def strings(obj: Any) -> list[str]:
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, dict):
        return [s for v in obj.values() for s in strings(v)]
    if isinstance(obj, list):
        return [s for v in obj for s in strings(v)]
    return []


# Product names in the package text, replaced so the knowledge base stays brand-free.
BRAND_WORDS = {"Excel": "spreadsheet"}


def debrand(text: str) -> str:
    for brand, generic in BRAND_WORDS.items():
        text = re.sub(rf"\b{brand}\b", generic, text)
    return text


def sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]


def boilerplate(families: list[dict[str, dict[str, Any]]]) -> set[str]:
    """Sentences of more than three words that appear in at least BOILERPLATE_MIN case families."""
    seen: Counter[str] = Counter()
    for fam in families:
        seen.update(
            {s for text in strings(fam) for s in sentences(text) if len(s.split()) > 3}
        )
    return {s for s, n in seen.items() if n >= BOILERPLATE_MIN}


def module_of(catalogue: dict[str, Any]) -> dict[str, str]:
    """Family number (01 to 20) to v2 module id."""
    return {b: m["id"] for m in catalogue["modules"] for b in m["blueprints"]}


def front(meta: dict[str, str]) -> str:
    return "---\n" + "".join(f"{k}: {v}\n" for k, v in meta.items()) + "---\n"


class Writer:
    """Markdown with three rules: shared sentences are left out (they live in the method notes), a sentence already
    written in this article is not written again, and a heading appears only when something follows it."""

    def __init__(self, shared: set[str]) -> None:
        self.shared = shared
        self.written: set[str] = set()
        self.lines: list[str] = []
        self.pending: list[str] = []

    def strip(self, s: str | None) -> str:
        if not s:
            return ""
        s = debrand(s)
        return " ".join(
            x for x in sentences(s) if x not in self.shared and x not in self.written
        )

    def _emit(self, lines: list[str], text: str) -> None:
        self.lines += self.pending + lines
        self.pending = []
        self.written.update(sentences(text))

    def h(self, level: int, text: str) -> None:
        if level <= 2:
            self.pending = []  # a section with nothing in it is dropped
        self.pending += [f"{'#' * level} {text}", ""]

    def p(self, text: str | None, label: str = "") -> None:
        text = self.strip(text)
        if text:
            self._emit([f"**{label}** {text}" if label else text, ""], text)

    def items(self, values: list[str], numbered: bool = False) -> None:
        kept = [k for k in (self.strip(v) for v in values) if k]
        if kept:
            self._emit(
                [f"{i}. {v}" if numbered else f"- {v}" for i, v in enumerate(kept, 1)]
                + [""],
                " ".join(kept),
            )

    def raw(self, line: str) -> None:
        self.lines += [line, ""]

    def text(self) -> str:
        return "\n".join(self.lines).rstrip() + "\n"


def questions(w: Writer, qs: list[dict[str, Any]], done: set[str]) -> None:
    for q in qs:
        if q["id"] in done or q["question"] in done:
            continue
        q = {**q, "question": debrand(q["question"])}
        done.update((q["id"], q["question"]))
        level_pending = len(w.pending)
        w.pending += [f"### {q['id']}: {q['question']}", ""]
        before = len(w.lines)
        w.p(q.get("synthetic_answer"), "Example answer in this fictional case:")
        w.p(q.get("diagnostic_value"), "Why ask:")
        w.p(q.get("branch_if_answer_differs"), "If the answer differs:")
        if (
            len(w.lines) == before
        ):  # nothing new under this question: keep the question itself
            del w.pending[level_pending:]
            w._emit([f"### {q['id']}: {q['question']}", ""], q["question"])


def render_family(fam: dict[str, dict[str, Any]], w: Writer) -> None:
    c, pb, b = fam["cases"], fam["playbooks"], fam["blueprints"]
    w.raw(f"# {c['case_id']}: {c['title']}")
    w.raw(NOTE)
    w.h(2, "Business and opening narrative")
    w.p(c["business_context"])
    w.p(f"\u201c{c['owner_narrative']}\u201d")
    w.p(pb["retrieve_on"]["symptom_narrative"], "Typical symptom:")
    w.p(pb["retrieve_on"]["workflow_context"], "Typical context:")
    w.h(2, "Current workflow")
    w.items(c["current_workflow"], numbered=True)
    w.h(2, "Diagnostic questions")
    done: set[str] = set()
    questions(w, c["diagnostic_interview"], done)
    questions(w, pb["discriminating_questions"], done)
    w.h(2, "Evidence in the fictional case")
    w.items([f"{e['id']}: {e['description']}" for e in c["evidence"]])
    w.h(2, "Diagnosis")
    for d in c["diagnoses"]:
        w.p(d["hypothesis"], "Supported in this case:")
        w.p(d["counterhypothesis"], "Competing explanation:")
    w.p(pb["positive_mechanism"], "Mechanism:")
    w.p(pb["counterexample"], "Counterexample:")
    w.h(2, "Minimum evidence before reusing this pattern")
    w.items(pb["minimum_evidence"])
    iv = c["interventions"]
    w.h(2, "Interventions")
    w.p(iv["process_first"], "Process first:")
    w.p(iv["deterministic_and_assisted_automation"], "Automation and bounded AI help:")
    w.p(pb["process_intervention"], "Process:")
    w.p(pb["automation_candidate"], "Automation candidate:")
    w.p(iv.get("rejected_default"), "Rejected as the default:")
    w.h(2, "Implementation blueprint")
    w.p(b["trigger"], "Trigger:")
    w.items(b["preconditions"])
    w.h(2, "Data fields")
    w.p(", ".join(f"`{f}`" for f in b["data_fields"]))
    spec = c["automation_spec"]
    w.h(2, "Business rules")
    w.items(
        [f"{r['id']}: {r['statement']} {r['rationale']}" for r in b["business_rules"]]
    )
    w.items(
        [f"{r['id']}: {r['statement']} {r['rationale']}" for r in spec["requirements"]]
    )
    w.h(2, "Acceptance tests")
    w.items(
        [
            f"{s['id']}: {s['scenario_and_expected_result']}"
            for s in b["acceptance_scenarios"]
        ]
    )
    w.items(
        [
            f"{t['id']}: {t['scenario_and_expected_result']}"
            for t in spec["acceptance_tests"]
        ]
    )
    w.h(2, "Human review")
    w.p(b["human_review"])
    ev = c["evaluation"]
    w.h(2, "How to measure")
    w.p(ev["primary_metric_definition"], "Primary metric:")
    w.items(ev["measurement_cautions"])
    im = c["implementation"]
    w.h(2, "Fictional rollout")
    w.p(im.get("simulated_resolution"), "What happened in the fiction:")
    w.p(im.get("simulated_lesson"), "Lesson:")
    w.p(im.get("rollback"), "Rollback:")
    w.p(im.get("go_no_go"), "Go or no-go:")
    w.h(2, "Unknowns and open questions")
    w.items(pb["unknowns"])
    w.items(c["open_questions"])
    w.h(2, "Stop rule")
    w.p(pb["stop_rule"])


def render_method(shared: set[str]) -> str:
    w = Writer(set())
    w.raw("# Method notes shared by every synthetic case")
    w.raw(
        "These notes apply to all the synthetic cases. They are kept here once instead of repeated in each case."
    )
    w.h(2, "Notes")
    w.items(sorted(shared))
    return w.text()


def render_all() -> dict[Path, str]:
    families = load_families()
    shared = boilerplate(families)
    modules = module_of(yaml.safe_load(CATALOGUE.read_text()))
    out: dict[Path, str] = {}
    for i, fam in enumerate(families, 1):
        num = f"{i:02d}"
        w = Writer(shared)
        render_family(fam, w)
        meta = {
            "title": fam["cases"]["title"],
            "section": "cases",
            "updated": UPDATED,
            "doc_id": f"cases/C{num}",
            "product": modules[num],
            "synthetic": "true",
            "review_status": "author_generated_not_domain_validated",
            "source": f"milo_synthetic_kb_v1 cases/C{num}, playbooks/P{num}, blueprints/B{num}",
        }
        out[KB / "cases" / f"C{num}.md"] = front(meta) + w.text()
    meta = {
        "title": "Method notes shared by every synthetic case",
        "section": "consultation",
        "updated": UPDATED,
        "doc_id": "consultation/method-notes",
        "product": "general",
        "synthetic": "true",
        "review_status": "author_generated_not_domain_validated",
        "source": "milo_synthetic_kb_v1 (text repeated across cases)",
    }
    out[KB / "consultation" / "method-notes.md"] = front(meta) + render_method(shared)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    files = render_all()
    if args.check:
        bad = [p for p, t in files.items() if not p.exists() or p.read_text() != t]
        for p in bad:
            print(f"stale: {p.relative_to(ROOT)}")
        print(
            "kb render OK"
            if not bad
            else f"{len(bad)} stale file(s); run scripts/build_kb.py"
        )
        return 1 if bad else 0
    for p, t in files.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(t)
    print(f"wrote {len(files)} articles under {KB.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
