# Evaluation: development set, not a sealed test

These 30 author-generated scenarios are deliberately visible and were authored alongside the knowledge base. They are useful regression and review cases, not an independent test of generalization. Never put this directory into retrieval or fine-tuning inputs for a claimed held-out test.

Score each dimension 0 (missing/wrong), 1 (partial), or 2 (specific and justified): evidence separation, question quality, causal discrimination, intervention fit, specification controls. Maximum 10. An output can satisfy a question by explicitly identifying the missing evidence and withholding the dependent conclusion. Do not require a literal wording match.

Use the per-case forbidden behaviors as critical failures. A proposed development gate is at least 8/10 with no critical failure per case; the product owner must ratify the gate. Record all scores, including failures. No model has been evaluated with this package yet.

Retrieval: on records with relevant_case_ids, collapse chunks to distinct source case IDs before recall@5. Skip the out-of-domain case in recall and assess rejection separately. Relevant IDs are author labels, not an exhaustive expert gold set. Review them before publishing a benchmark.

To build a real held-out test: have a separate domain reviewer create new cases after freezing the KB; vary mechanism, company size, channel, authority and constraints, not just company names. Keep prompts and answers outside indexing and development access. Evaluate only after selecting the model/prompt/configuration; report uncertainty, failure types and the exact KB hash. Do not call these 30 cases held-out.
