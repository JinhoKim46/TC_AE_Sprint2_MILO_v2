# M0b lesson: data for the onboarding diagnosis

## Context

M0 built data for a seven-module IT-maintenance catalogue with prices. The project's purpose changed: the bot is an onboarding entry chatbot. A prospective owner describes an operation, the bot collects the data a diagnosis needs, and it estimates how much time an automation of one area would save, as a range. Prices are out of scope because no price data exists. M0b rebuilds the data for that purpose before any code is written against it.

## What was built

| Data | Where | Count |
|---|---|---|
| Service areas (fictional catalogue) | `data/catalogue.yaml` | 4 areas, with scope, effect inputs and the 20 blueprints regrouped |
| Area articles | `data/kb/solutions/` | 4 |
| Effect method note | `data/kb/consultation/effect-estimate.md` | 1 |
| Case articles (re-tagged to the areas) | `data/kb/cases/` | 20 |
| Intake harness (must-have data per area) | `data/intake_harness.yaml` | 5 common items and 4 to 5 per area |
| Tool definitions for M3 | `data/tools.yaml` | 6 tools, with risk tiers |
| Gold set | `data/gold.jsonl` | 40 (22 paraphrase, 10 identifier, 8 unanswerable; 16 with a filter; 20 dev and 20 test) |
| Tool cases | `data/tool_cases.jsonl` | 20 (4 where no tool should run) |
| Attacks | `data/attacks.jsonl` | 10 (6 direct, 3 in a retrieved passage, 1 in a tool output) |
| Intake scenarios, held out | `data/intake_scenarios.jsonl` | 16 (4 per area; 8 complete, 8 conditional) |

Removed: the rate card, the pricing articles and the seven old solution articles. `scripts/build_kb.py` re-renders the case articles from the owner's package and rewords the package's phrases about a rate card.

## Three lessons from this milestone

1. **A harness is a list of questions with a stop rule.** The intake harness marks which data is must-have and which feeds the estimate. A missing must-have item is asked again, at most twice; if it is still missing, the diagnosis is conditional and names the gap. Writing the list first made it clear which questions the bot must be able to ask.
2. **A rule against prices has to be tested on the data, not stated in a comment.** The test `test_no_prices_anywhere_in_the_data` searches the data for currency amounts and the words "rate card". It deliberately does not ban the word "price" as a concept, because the owners' own stories use it. Banning the concept would have failed on fictional owner speech.
3. **Repeated sentences are a data problem, not a prompt problem.** Four area articles ended with the same closing sentence, which the repeated-sentence test caught. Each closing sentence now names something specific to its area. Retrieval would otherwise pull the same passage for every area.

## How to read the result

- `make check`: 27 tests pass, offline.
- `uv run python scripts/check_project_data.py data`: OK, 0 problems.
- The gold set meets the kit's minimums (30 questions, 6 unanswerable, 6 identifier, 4 with a filter).
- Intake scenarios are held out. No retrieval input reads them, and a test checks that.

## Decision for you

Checkpoint questions (answer in your own words, two or three sentences each):

1. Which gold questions do you expect the retriever to find hardest, and why did you include them?
2. How do you know no gold quote was written after looking at what the retriever returns?
3. Which of the 10 attacks could really happen in an owner's conversation, and which are decoration?

Explain to a reviewer, in two minutes: why these four areas, and how the harness stops the bot from guessing.
