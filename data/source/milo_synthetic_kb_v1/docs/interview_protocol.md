# Interview guide

Ask in natural language and avoid presenting the owner with a large form. Reuse answers already supplied. Open with the business goal, then follow a concrete incident.

## Minimum discovery

- Service model: recurring contract, rental, usage billing, project or chargeable repair; identify combinations.
- Operating unit: organization, site, asset, reporter, incident, visit and contract. Confirm what counts as a request.
- Trigger and intake: who reports, through which channels, who acknowledges and what can bypass intake.
- Work flow: normal sequence, responsible person, source of truth and completion condition for each handoff.
- Decisions: who may authorize cost, access, downtime, scope change, acceptance and billing release.
- Constraints: skills, parts, customer access, geographic coverage, connectivity, vendor dependencies and contractual obligations.
- Failures: one recent example with dates, records, recurrence and consequences; distinguish actual loss from frustration or a rough estimate.
- Existing tools: what is configured, what staff avoid, what integration is supported, and whether exports can be written back.
- Outcomes: desired operational change, usable baseline, adoption burden and acceptable pilot scope.

## Branching

Duplicate visits → verify same incident, device and intention before searching C01/C03.
Late arrivals → distinguish access, skills, stock, schedule acknowledgement and insufficient capacity using C02.
Inventory shortage → distinguish availability, location, reservation, compatibility and supply lead time using C04/C18.
Billing errors → separate identity/readings, effective terms, arithmetic and acceptance using C05/C06/C13.
Waiting work → identify the exact dependency and next-action owner using C07/C17/C20.
Knowledge gaps → distinguish missing documentation, obsolete context and expertise/training using C12.
Poor adoption → observe real work and duplicate entry before proposing more software using C19.

## Stop and escalate

Stop asking a branch once enough evidence supports a bounded proposal; keep remaining unknowns explicit. Escalate contractual interpretation, conflicting approval authority, out-of-scope technical work or irreversible actions to the relevant responsible person. Do not prolong interviews just to populate every field. Do not promise a final automation specification while blocking authority, scope or integration questions remain unanswered.
