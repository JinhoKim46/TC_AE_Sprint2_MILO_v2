# MILO synthetic consulting knowledge base — v1.0.0

Created 2026-10-23 for TC_AE_Sprint2_MILO. English-language foundational data for B2B IT maintenance, school support, office equipment rental and field service.

## Start here

1. Read `docs/knowledge_policy.md` and `docs/integration.md`.
2. Read `cases/C01.md` for a worked case; all 20 stories have Markdown and JSON versions.
3. From this directory run `python3 scripts/validate.py`.
4. Try `python3 scripts/search.py "two technicians same printer" --top-k 5`.
5. Ingest only `rag/knowledge_chunks.jsonl`, retaining metadata and enforcing access policies in the application.
6. Use `evaluation/dev_scenarios.jsonl` for development review; never index it.

## Contents

| Directory | Purpose |
|---|---|
| cases | 20 detailed case dossiers, readable Markdown and structured JSON |
| playbooks | 20 reusable diagnostic patterns with alternative explanations |
| blueprints | 20 proposed implementation blueprints plus shared controls |
| rag | 120 source-linked retrieval records and an explicit ingestion allowlist |
| evaluation | 30 development scenarios with expected reasoning and critical failures |
| schemas | JSON Schema contracts for cases, retrieval chunks and diagnostic output |
| docs | Governance, interviewing, specification, measurement and integration guidance |
| scripts | Dependency-free package validator and lexical retrieval demonstration |
| examples | Example diagnostic output illustrating missing evidence; excluded from RAG |

## What is synthetic

All business scenarios are fictional. Initial narratives are condensed adaptations of the 20 supplied owner stories. Follow-up answers, observations, causal explanations and fictional resolutions are author-created examples. No historical customer record, production deployment, measured outcome, domain expert review or externally validated causal effect is claimed. Numerical context such as staff counts and device counts belongs only to the fictional business. All baseline, post-pilot, target and savings values remain null.

This is a proposed v1 knowledge foundation, not a trained model or a working integration. Retrieval alone does not implement diagnosis. Proposed capabilities do not extend the app’s catalogue, pricing or permissions automatically. The package does not modify the GitHub repository or the user’s workstation.

## Review before operational use

Have a field-service owner review domain realism and exceptions; a consultant review evidence and interventions; and an engineer review data contracts and controls. Mark corrections by stable ID and version. Add real validated cases as a separate evidence class after appropriate permission and redaction. Never relabel a synthetic case as measured customer history.
