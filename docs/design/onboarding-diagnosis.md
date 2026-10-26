# Onboarding diagnosis chatbot: design draft

Status: draft for approval. Nothing here is built yet. Milestones M1 to M7 keep the kit's structure and grading.

## Intent

MILO is the first conversation a prospective owner of a small service business has with a provider. The bot:

1. learns how the owner's operation works today,
2. diagnoses where time and money are lost, with the evidence for each finding,
3. estimates how much effort an automation of one part would save, with stated assumptions,
4. says which service area fits, or that no build is needed.

The project is a foundation. It must stay small, measurable and extendable. Learning goal: how to build, score and improve such a bot.

## Non-goals

- No prices, quotes or contract terms. The bot never states a cost in money.
- No real company, product, brand or person names anywhere in the repository. Data is fictional and written fresh.
- No live integrations, no real customer data.
- Not every service area is diagnosed, only the ones that are easy to diagnose from conversation.

## Service areas (fictional catalogue)

Four areas are diagnosed in this project. Each has an includes and excludes list, written fresh.

| Area | Typical question it answers |
|---|---|
| Request and dispatch management | Where do requests come from, who takes them, does anything get lost or duplicated? |
| Consumables and stock management | Do we know what is on hand, where, and what is running low? |
| Usage and billing preparation | Are meter or usage readings collected, checked and turned into billable figures without manual rework? |
| Operations overview | Can one person see open work, owners and blockers without asking around? |

Named but not diagnosed in this project: linking processes across tools so that work flows without re-entry, and turning unstructured inputs (photos, messages, forms) into one structured framework. The bot may mention these as "later" but does not diagnose them.

## Conversation flow

1. Business context: size, service type, number of sites, number of staff in operations.
2. One recent incident in the most painful area, walked through step by step.
3. Branch questions for the area the owner picked (from the interview branches of the source package).
4. Stop asking once evidence supports a bounded proposal. Keep the remaining unknowns explicit.
5. Output the diagnosis card.

## Diagnosis card (output)

- **Current workflow:** steps, owner per step, handoffs, volumes. Each fact has a status: reported, conflicting or unknown. Conflicts are stored, not averaged.
- **Bottlenecks:** each has the evidence (quoted from the owner), at least one alternative explanation, and a confidence of low, medium or high based on how many independent facts support it.
- **Automation candidate per bottleneck:** one tier only: process change, existing-tool setup, deterministic automation, AI assistance with human review, or no build.
- **Effect estimate:** `net_hours_per_period = events × (baseline_minutes − new_minutes) / 60 − extra_review_hours − maintenance_hours`. Every input has a unit, a period and a source (owner-reported or assumed). Unknown inputs stay null, never zero. Overlapping stages are never added together. The answer shows a central value and a range: low = 0.8 × central and high = 1.2 × central, unless the owner gives a range. Each answer states which inputs were assumed.
- **Missing must-have data:** the intake harness (`intake-harness-draft.yaml`) lists the data needed per area. A missing must-have is asked again, at most twice. If still missing, the diagnosis is conditional and names the missing item. The bot does not stop with "I don't know".
- **Abstention in retrieval:** an answer is given only when a retrieved passage supports it. There is no similarity-score cutoff, because the earlier project found that scores did not separate answerable from unanswerable questions.
- **Area fit:** which of the four areas applies, or no build.
- **Open questions:** what to ask next to change the recommendation.

## Data

| Data | Use | Status |
|---|---|---|
| Case articles (20, from the synthetic package) | Analogous experience, cited by ID, never as the owner's facts | Exists in M0. Terms may need renaming to the four areas |
| Catalogue of four areas, with includes and excludes | Service fit and the module names in answers | To write (M0b) |
| Effect parameters per area (minutes per event, event volumes) | Effect estimate | To write (M0b), labelled assumed |
| Intake scenarios: 15 to 20 fictional owner conversations | Evaluation of diagnosis | To write (M0b). Held out |
| Development scenarios (30, from the package) | Diagnosis rubric in M7 | Exists. Dev only, never indexed |
| Gold set (48), tool cases (18), attacks (10) | Retrieval, tools, security | Exists. Module names must be remapped to the four areas, which changes tests |

## Milestone mapping (kit structure unchanged)

- **M0 (done) and M0b:** remap the catalogue and the gold set to the four areas. Add the effect parameters and the intake scenarios. Keep the existing checks green.
- **M1 retrieval:** index the case articles and the catalogue. Report recall@5 and nDCG@5 with CIs. The same gold set.
- **M2 advanced RAG:** one query translation, and a self-query on area and section with a fallback to unfiltered search.
- **M3 tools:** `search_knowledge`, `record_fact` (with status, unit and source), `get_recorded_facts`, `estimate_effect` (computed in code, never by the model), `draft_diagnosis` (output validated against a schema), `reset_diagnosis` (destructive, needs approval). Tool eval on 15 cases.
- **M4 security:** no money figures in any output, no numbers the model invents, identity bound in code, approval for the destructive tool, retrieved text treated as data. ASR on the 10 attacks.
- **M5 errors and fallback:** typed errors, bounded retries, a local fallback model, one trace per flow.
- **M6 UI (Flask):** chat, sources panel, tool-call panel with policy decision, progress, and a diagnosis card view.
- **M7 evaluation:** retrieval metrics; a diagnosis rubric on the 30 dev scenarios; the held-out intake scenarios read once; a judge only where it passes calibration; a limits section with intervals and causes.

## Decisions taken in this draft (agent decisions, can be objected to)

1. Four areas replace the seven modules. The seven-module catalogue is rewritten, not patched.
2. Effect numbers are fictional assumptions, labelled as such in every answer.
3. The diagnosis card is produced by a tool with a schema, not free text.
4. The kit's M1 to M7 grading structure is kept as it is.
5. Embedding model: reuse `google/gemini-embedding-2` with 800-character chunks, 100 overlap and top 5, from the earlier project's comparison (dev, about 0.016 USD for the full five-model run). M1 checks it once on the v2 corpus. No new model comparison.
6. Effect shown as a central value with a range (0.8× to 1.2×), not a single number.
7. Missing must-have data is asked again before any conditional diagnosis, using the intake harness.
8. The bot speaks and writes English: the questions, the answers and the repository files. The working conversation with the owner is in Korean.
9. Clients are counted as `customer_accounts` (contracts) and `service_sites` (physical places). They are separate harness items.

## Open for the owner

- Approval of this draft, then an update of the issue #2 spec. Nothing is posted to GitHub until approved.
