# Kit location: the course's project kit, three levels up from sprint2/milo-v2 (override with KIT_SRC=...).
KIT_SRC ?= ../../../project-kit

.PHONY: check lint test kit-sync contract

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
