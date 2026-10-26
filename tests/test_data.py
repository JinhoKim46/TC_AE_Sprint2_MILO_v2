"""M0: the data agrees with itself. Offline; reads files only."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
KB = DATA / "kb"
PKG = DATA / "source" / "milo_synthetic_kb_v1"
CATALOGUE = yaml.safe_load((DATA / "catalogue.yaml").read_text())
HARNESS = yaml.safe_load((DATA / "intake_harness.yaml").read_text())
TOOLS = yaml.safe_load((DATA / "tools.yaml").read_text())
MODULE_IDS = [m["id"] for m in CATALOGUE["modules"]]
HARNESS_IDS = {s["id"] for s in HARNESS["common"]} | {
    s["id"] for slots in HARNESS["areas"].values() for s in slots
}
# Prices are out of the project: no money figure, currency or rate card appears in the data or the knowledge base.
MONEY = re.compile(
    r"\$\s?\d|\d[\d,.]*\s?(?:USD|EUR|KRW|won)\b|\brate card\b", re.IGNORECASE
)
V1_NAMES = (
    "phone-intake",
    "email-triage",
    "ticket-creation",
    "staff-assignment",
    "document-data-entry",
    "customer-status-updates",
    "TC_AE_Sprint2_MILO",
)
# Brands and chat apps that the owner stories mention or that an author might reach for; the knowledge base stays
# brand-free so every company, product and person in it is fictional.
BRANDS = (
    "Samsung", "KakaoTalk", "WhatsApp", "Slack", "TeamViewer", "AnyDesk", "Microsoft", "Google", "Apple",
    "Canon", "Ricoh", "Xerox", "Epson", "Kyocera", "Brother printer", "Excel", "Windows",
)  # fmt: skip
FRONT = re.compile(r"\A---\n(.*?)\n---\n(.*)", re.DOTALL)


def articles() -> dict[str, tuple[dict[str, str], str]]:
    out = {}
    for p in sorted(KB.rglob("*.md")):
        m = FRONT.match(p.read_text())
        assert m, f"{p} has no front matter"
        meta = dict(
            line.split(": ", 1) for line in m.group(1).splitlines() if ": " in line
        )
        out[p.relative_to(KB).with_suffix("").as_posix()] = (meta, m.group(2))
    return out


def rows(name: str) -> list[dict]:
    path = DATA / name
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def words(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", s.lower()))


# ---- the converted package --------------------------------------------------------------------------------------


def test_converted_articles_are_reproducible() -> None:
    r = subprocess.run(
        [sys.executable, "scripts/build_kb.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stdout


def test_articles_have_front_matter_and_doc_ids() -> None:
    docs = articles()
    assert len(docs) >= 20
    for doc_id, (meta, _) in docs.items():
        for key in ("title", "section", "updated", "doc_id", "product", "synthetic"):
            assert meta.get(key), f"{doc_id}: front matter lacks {key}"
        assert meta["doc_id"] == doc_id
        assert meta["product"] in (*MODULE_IDS, "general"), doc_id


def test_articles_hold_no_json_and_no_v1_references() -> None:
    for doc_id, (_, body) in articles().items():
        assert '{"' not in body and '": "' not in body, f"{doc_id} holds JSON syntax"
        for name in V1_NAMES:
            assert name not in body, f"{doc_id} mentions {name}"


def test_no_sentence_repeats_across_many_articles() -> None:
    """The render moves repeated text into method-notes; no long sentence appears in four or more articles."""
    seen: Counter[str] = Counter()
    for _, body in articles().values():
        text = "\n".join(
            x for x in body.splitlines() if not x.startswith((">", "#"))
        )  # banner and headings
        text = re.sub(r"\*\*[^*]+\*\*", "", text)  # the renderer's own labels
        sentences = {
            s.strip(" -")
            for s in re.split(r"(?<=[.!?])\s+|\n", text)
            if len(s.split()) > 3
        }
        seen.update(sentences)
    repeated = [s for s, n in seen.items() if n >= 4]
    assert not repeated, repeated[:3]


def test_knowledge_base_and_stories_name_no_brand() -> None:
    texts = {d: body for d, (_, body) in articles().items()}
    texts["stories"] = (DATA / "stories" / "owner_stories.md").read_text()
    for doc_id, body in texts.items():
        for brand in BRANDS:
            # brands are capitalised, so a case-sensitive whole-word match ("access windows" is not a brand)
            assert not re.search(rf"\b{re.escape(brand)}\b", body), (
                f"{doc_id} names {brand}"
            )
        assert not re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", body), (
            f"{doc_id} holds an email"
        )


def test_package_is_stored_unchanged() -> None:
    """The owner's package is the source and the comparison arm: every file still matches its manifest hash."""
    import hashlib

    manifest = json.loads((PKG / "manifest.json").read_text())["sha256"]
    changed = [
        p
        for p, h in manifest.items()
        if hashlib.sha256((PKG / p).read_bytes()).hexdigest() != h
    ]
    assert not changed, changed


def test_evaluation_material_stays_out_of_the_knowledge_base() -> None:
    """The package's pre-made records and its 30 scenarios are never retrieval input."""
    assert (PKG / "rag" / "knowledge_chunks.jsonl").exists()
    scenarios = [
        json.loads(x)
        for x in (PKG / "evaluation" / "dev_scenarios.jsonl").read_text().splitlines()
    ]
    assert len(scenarios) == 30
    corpus = " ".join(body for _, body in articles().values())
    for s in scenarios:
        assert s["input_story"] not in corpus, s["eval_id"]
    assert not list(KB.rglob("*.jsonl"))


# ---- catalogue, rate card and the articles that state them -----------------------------------------------------


def test_every_area_has_an_article_with_its_scope() -> None:
    docs = articles()
    for m in CATALOGUE["modules"]:
        doc_id = f"solutions/{m['id']}"
        assert doc_id in docs, f"missing {doc_id}"
        body = docs[doc_id][1]
        assert m["name"] in body
        assert "## What is included" in body and "## What it does not do" in body, m[
            "id"
        ]


def test_every_effect_input_names_a_harness_item() -> None:
    for m in CATALOGUE["modules"]:
        effect = m["effect_inputs"]
        assert effect["events"] in HARNESS_IDS, m["id"]
        assert effect["baseline_minutes"] in HARNESS_IDS, m["id"]
        assert effect["new_minutes"]["assumed"] > 0, m["id"]


def test_intake_harness_items_are_complete() -> None:
    slots = list(HARNESS["common"]) + [s for v in HARNESS["areas"].values() for s in v]
    assert {m["id"] for m in CATALOGUE["modules"]} == set(HARNESS["areas"])
    assert len(slots) == len({s["id"] for s in slots}), "duplicate harness id"
    for s in slots:
        assert s["question"].endswith("?"), s["id"]
        assert s["unit"], s["id"]
        assert isinstance(s["must"], bool) and isinstance(s["effect"], bool), s["id"]
    for area, items in HARNESS["areas"].items():
        assert any(s["must"] for s in items), area


def test_no_prices_anywhere_in_the_data() -> None:
    """The onboarding bot states scope and effect ranges, never money. No currency or price term in the data."""
    files = [DATA / "catalogue.yaml", DATA / "intake_harness.yaml", DATA / "tools.yaml"]
    files += list(KB.rglob("*.md")) + [DATA / "stories" / "owner_stories.md"]
    for p in files:
        for line in p.read_text().splitlines():
            assert not MONEY.search(line), f"{p.name}: {line[:80]}"


def test_converted_documents_map_to_catalogue_modules() -> None:
    blueprints = sorted(b for m in CATALOGUE["modules"] for b in m["blueprints"])
    assert blueprints == [f"{i:02d}" for i in range(1, 21)]


# ---- gold set, tool cases, attacks ------------------------------------------------------------------------------


def test_gold_quotes_and_question_rules() -> None:
    docs = articles()
    norm = lambda s: re.sub(r"\s+", " ", s).strip().casefold()
    gold = rows("gold.jsonl")
    assert len(gold) >= 30
    quotes = [e["quote"] for r in gold for e in r["gold_evidence"]]
    assert len(quotes) == len(set(quotes)), "two rows share a quote"
    for r in gold:
        for e in r["gold_evidence"]:
            assert norm(e["quote"]) in norm(docs[e["doc_id"]][1]), r["qid"]
        if r["filters"]:
            assert set(r["filters"]) <= {"section", "product"}, r["qid"]
        if r["type"] == "paraphrase":
            q, quote = words(r["question"]), words(r["gold_evidence"][0]["quote"])
            assert len(q & quote) / len(q) <= 0.30, (r["qid"], sorted(q & quote))
            assert not (q & set(MODULE_IDS)), r["qid"]
        if r["type"] == "identifier":
            ids = re.findall(
                r"\b(?:[A-Z]\d{2}(?:-[A-Z]\d{2})?|[a-z]+-[a-z]+(?:-[a-z]+)?)\b",
                r["question"],
            )
            named = [i for i in ids if i in r["gold_evidence"][0]["quote"]]
            assert named, (
                f"{r['qid']}: an identifier question names an id that is in its quote"
            )


def test_gold_splits_are_balanced_by_type() -> None:
    by = Counter((r["type"], r["split"]) for r in rows("gold.jsonl"))
    for t in {k[0] for k in by}:
        assert abs(by[(t, "dev")] - by[(t, "test")]) <= 1, t


def test_unanswerable_questions_are_absent_from_the_knowledge_base() -> None:
    corpus = " ".join(body.lower() for _, body in articles().values())
    for r in rows("gold.jsonl"):
        if r["type"] == "unanswerable":
            assert (
                r["gold_evidence"] == []
                and r["reference_answer"] == "INSUFFICIENT_CONTEXT"
            )
            assert r["question"].lower() not in corpus


def test_tool_cases_use_declared_tools_and_arguments() -> None:
    specs = {t["name"]: t for t in TOOLS["tools"]}
    cases = rows("tool_cases.jsonl")
    assert len(cases) >= 15
    assert sum(not c["expected_calls"] for c in cases) >= 3
    for c in cases:
        for call in c["expected_calls"]:
            assert call["name"] in specs, c["id"]
            assert set(call["args"]) <= set(specs[call["name"]]["args"]), c["id"]
            if call["name"] == "record_fact":
                assert call["args"]["field_id"] in HARNESS_IDS, c["id"]
            if call["name"] in ("estimate_effect", "draft_diagnosis"):
                assert call["args"]["area_id"] in MODULE_IDS, c["id"]
    assert {call["name"] for c in cases for call in c["expected_calls"]} == set(specs)
    for c in cases:
        assert set(c.get("facts", {})) <= HARNESS_IDS, c["id"]


def test_intake_scenarios_are_held_out_and_consistent() -> None:
    """Held-out diagnosis scenarios: four per area, and a conditional diagnosis exactly when must-have items are missing."""
    scenarios = rows("intake_scenarios.jsonl")
    assert len(scenarios) == 16
    for area in MODULE_IDS:
        assert sum(s["area_id"] == area for s in scenarios) == 4, area
    must = {s["id"] for s in HARNESS["common"]}
    for area, items in HARNESS["areas"].items():
        must |= {s["id"] for s in items if s["must"]}
    for s in scenarios:
        assert set(s["harness_facts"]) <= HARNESS_IDS, s["scenario_id"]
        assert set(s["missing_must"]) <= must, s["scenario_id"]
        assert set(s["expected"]["should_ask"]) == set(s["missing_must"]), s[
            "scenario_id"
        ]
        conditional = bool(s["missing_must"])
        assert s["expected"]["diagnosis"] == (
            "conditional" if conditional else "full"
        ), s["scenario_id"]
    assert any(s["missing_must"] for s in scenarios) and any(
        not s["missing_must"] for s in scenarios
    )


def test_attacks_cover_the_three_vectors() -> None:
    attacks = rows("attacks.jsonl")
    assert len(attacks) >= 10
    assert {a["vector"] for a in attacks} == {"direct", "rag", "tool_output"}
    assert any(a["success_check"]["type"] == "output_leak" for a in attacks)
    assert any(a["success_check"].get("name") == "reset_diagnosis" for a in attacks)


@pytest.mark.skipif(
    not (ROOT / "scripts" / "check_project_data.py").exists(),
    reason="kit not synced (make kit-sync)",
)
def test_kit_data_checker_passes() -> None:
    r = subprocess.run(
        [sys.executable, "scripts/check_project_data.py", "data"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stdout + r.stderr


def test_extra_dev_items_follow_the_same_quote_and_unanswerable_rules() -> None:
    corpus = " ".join(body.lower() for _, body in articles().values())
    extra = [
        json.loads(x)
        for x in (ROOT / "data" / "gold_dev_extra.jsonl").read_text().splitlines()
        if x.strip()
    ]
    docs = {doc_id: body for doc_id, (_, body) in articles().items()}
    norm = lambda s: re.sub(r"\s+", " ", s).strip().casefold()
    for r in extra:
        assert r["split"] == "dev", r["qid"]
        if r["type"] == "unanswerable":
            assert (
                r["gold_evidence"] == []
                and r["reference_answer"] == "INSUFFICIENT_CONTEXT"
            ), r["qid"]
            assert r["question"].lower() not in corpus, r["qid"]
        for e in r["gold_evidence"]:
            assert norm(e["quote"]) in norm(docs[e["doc_id"]]), r["qid"]
