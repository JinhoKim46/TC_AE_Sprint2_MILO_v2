# Location of the project kit (override with KIT_SRC=<path>).
KIT_SRC ?= ../../../project-kit

.PHONY: check lint test kit-sync contract eval-retrieval eval-retrieval-replay eval-advanced eval-advanced-replay

check: lint test

lint:
	uv run ruff check .
	uv run ruff format --check .

test:
	uv run pytest -q

# Copy the kit's contract tests and data checker in (untracked; see .gitignore).
kit-sync:
	test -d $(KIT_SRC)/contract || { echo "kit not found at $(KIT_SRC); pass KIT_SRC=<path>"; exit 1; }
	rm -rf contract && cp -r $(KIT_SRC)/contract contract && rm -rf contract/__pycache__
	mkdir -p scripts && cp $(KIT_SRC)/scripts/check_project_data.py scripts/

# The kit's contract suite against this app.
contract:
	test -d contract || { echo "run make kit-sync first"; exit 1; }
	PROJECT_APP=milo.app:build_app uv run pytest contract -p no:cacheprovider

# M1: offline lexical baseline on the dev gold set, and the replay of its stored result (no model call).
eval-retrieval:
	uv run python scripts/eval_retrieval.py --embedder lexical

eval-retrieval-replay:
	uv run python scripts/eval_retrieval.py --replay evals/results/retrieval/dev_lexical.json

# M2: the A/B against the baseline on dev (offline lexical arms) and its replay.
eval-advanced:
	uv run python scripts/eval_advanced.py

eval-advanced-replay:
	uv run python scripts/eval_advanced.py --replay evals/results/advanced/dev_ab.json
