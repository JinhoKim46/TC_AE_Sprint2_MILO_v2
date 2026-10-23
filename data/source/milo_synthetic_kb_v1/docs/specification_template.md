# Customer automation specification contract

An implementation-ready specification is completed only after customer review. The case blueprints are reusable starting material.

1. **Goal and boundary:** process, included sites and actors, exclusions, measurable change and baseline limitations.
2. **Evidence map:** each customer fact → source → supported diagnosis → intervention → requirement → acceptance test. List counterevidence separately.
3. **Current workflow:** trigger, handoffs, systems, timing, rework, dependencies and completion definitions.
4. **Future workflow:** actions, system of record, human approval, exceptions and override authority.
5. **Data contract:** field name, business meaning, type, unit, nullable condition, source, validation, ownership, retention and permissions. Stable entity IDs replace display-name matching.
6. **State machine:** explicit allowed transitions, actor, guard, side effect, retry behavior and audit event. Terminal states cannot erase unresolved related obligations.
7. **Integrations:** supported API/import/export, authentication owner, mapping, rate/error behavior, idempotency and reconciliation. Unknown capabilities block confident estimates.
8. **AI scope:** extraction or suggestion input, output schema, evidence requirements, forbidden actions and review trigger. Deterministic controls must remain effective if the model is wrong.
9. **Acceptance:** Given relevant state and evidence, When action occurs, Then expected state and external effect; include denied actions, concurrent updates, missing evidence, retries and partial outages.
10. **Delivery:** data cleanup, migration validation, shadow run, pilot, named support owner, fallback, rollout criteria and training.
11. **Commercial assumptions:** separately approved prices and effort; never derive a new extension’s price from a loosely similar catalogue entry.
12. **Measurement:** numerator, denominator, time window, attribution, case mix, missingness, overhead and failure metrics.

Generic request lifecycle to adapt: draft → triaged → waiting_for_approval / ready → assigned → in_progress → technically_complete → acceptance_pending → accepted → closed. Waiting for parts, vendor or access are explicit blockers with owner and review time. This is an illustrative lifecycle, not a mandatory universal state model; meter billing, stock movement and renewals need their own domain transitions.
