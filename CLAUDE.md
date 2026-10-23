# CLAUDE.md

MILO v2: a RAG diagnosis chatbot for B2B IT-maintenance and office-equipment service businesses, built milestone by
milestone (M0 to M7 of the Sprint 2 project kit) so the owner can follow and learn every step. Learning first: each
milestone implements the kit minimum; extras only when they teach something.

## Rules

- Independent of MILO v1 (`sprint2/project`): no imports from it and no copied modules. Reading it for reference is
  fine; every line here is written fresh in this repo.
- Fictional data only. The companies, people and figures in `data/` are invented. No real business, customer or
  person is named anywhere in this repo.
- Secrets live in the untracked `.env` only (`.env.example` lists the names). Never print a key.
- Python 3.12 with `uv`. `make check` (lint, format check, offline tests) passes before every push.
- Tests run offline. A test or command that calls a paid model needs an explicit `--live` (or `MILO_LIVE=1`), a cost
  cap and a reason; the default path never spends.
- Models: chat `anthropic/claude-haiku-5.5` through LangChain `ChatOpenAI` with the OpenRouter base URL; local
  fallback Ollama `qwen3:8b`. Each milestone issue states its spend cap.

## Workflow

- One GitHub issue per milestone, a sub-issue of the spec issue. One branch per issue, `m<N>-<slug>`.
- Each PR: tests first where behaviour changes, `make check` green, a review, `Closes #<issue>` and
  `Part of #<spec>`. The integrator squash-merges after checks and review.
- Each milestone adds `docs/lessons/M<N>.md`: context, what was built, how to read the result, the owner's decision.
  The owner gets a checkpoint after every milestone before the next starts.
- Commit messages: `<scope>: <imperative summary>`, scope = the milestone (`m1`) or `docs`, `chore`.

## Agent skills

### Issue tracker

Issues and specs live in this repo's GitHub Issues (`gh`). See `docs/agents/issue-tracker.md`.

### Domain docs

Single-context: `GLOSSARY.md` and `docs/adr/` at the root, created when terms or decisions settle. See
`docs/agents/domain.md`.
