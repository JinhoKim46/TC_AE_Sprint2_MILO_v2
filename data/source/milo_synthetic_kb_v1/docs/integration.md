# Integration with TC_AE_Sprint2_MILO

Repository reviewed through GitHub on 2026-10-23:

- README.md, blob SHA `7d83c1e2e2544384791b87f353c27554715ff733`
- data/source/catalogue.yaml, blob SHA `5ada880ff0d286a77edaccdb034c06fd09a1830b`
- src/milo/report/build.py, blob SHA `6d01e87dcec50e8c811f7ccd5134a574591036ed`

These are individual file hashes, not a single pinned repository commit. This package has not changed repository code and has not been tested against the full application.

## Observed boundaries

The catalogue defines phone-intake, email-triage, ticket-creation, staff-assignment, document-data-entry and customer-status-updates. The report builder selects candidates using MODULE_SIGNALS keyword matches and produces deterministic figures with constrained source identifiers. Richer retrieved text alone will not replace this recommendation logic.

The catalogue’s ticket module excludes billing and closing without a person; staff-assignment suggests from skills and availability and excludes automatic shift changes; email drafts require approval. Some case fields and workflows therefore describe new capabilities, not current product behavior. Existing fixed integration notes are fictional catalogue content, not demonstrated lead times for these extensions.

## Suggested integration sequence

1. Store this versioned package as a separate knowledge source; preserve the existing catalogue and rate card.
2. Add an explicit loader for `rag/knowledge_chunks.jsonl`, preserving chunk_id, doc_id, kind, source_path, synthetic, evidence_origin, review_status and split. Do not recursively index the package.
3. Retrieve by symptom plus workflow context. Group repeated sections by case; consider diversity across cases and counterexamples. Retrieve a full source section when a chunk alone lacks the qualifying conditions.
4. Introduce a diagnosis layer that consumes fresh customer facts plus retrieved references and outputs the proposed diagnostic output schema. Validate referenced case IDs and customer evidence independently. This layer is not implemented here.
5. Keep current fact-status, conflict, permission and numerical guards. Do not pass new schema fields into the old snapshot parser without an explicit migration; it rejects unknown protocol fields.
6. Map supported recommendations to existing catalogue IDs only where the inclusion/exclusion boundaries match. Return proposed extensions with pricing unavailable until approved catalogue and rate-card entries exist.
7. Extend report provenance deliberately. Current resolve_source accepts fact, rate_card, protocol and derived sources; arbitrary C01/P01 references will need a separately validated citation structure. Never spoof case references as factual customer evidence.
8. Review savings for overlapping task stages. The current return section notes modules_may_overlap; the new knowledge base does not remove that limitation automatically.
9. Run the package’s development scenarios, the project’s existing tests and retrieval evaluations after implementation. Obtain a separately authored held-out evaluation before claiming improved accuracy.

## Local demonstration

The included search script is a dependency-free BM25-style lexical baseline over the explicit JSONL corpus. It is intended to inspect retrieval and provenance, not replace the project’s dense/hybrid stack. It makes no model calls and does not perform diagnosis or tool actions. No embeddings, API keys or vendor model assumptions are embedded in the ZIP.

## Sources

https://github.com/JinhoKim46/TC_AE_Sprint2_MILO/blob/main/README.md

https://github.com/JinhoKim46/TC_AE_Sprint2_MILO/blob/main/data/source/catalogue.yaml

https://github.com/JinhoKim46/TC_AE_Sprint2_MILO/blob/main/src/milo/report/build.py
