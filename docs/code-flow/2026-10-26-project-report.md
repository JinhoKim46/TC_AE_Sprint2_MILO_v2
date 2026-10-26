# MILO v2: project overview

## Goal and scope

MILO is an onboarding chatbot for a small service business. A prospective owner describes how their work runs. MILO answers from a knowledge base of past cases and four service areas, records the facts the owner gives, estimates the time an automation would save as a range, and shows every step it took. Prices are out of scope. The data is fictional.

## Requirements and where they are met

| Requirement (Sprint 2 kit) | Where | Status |
|---|---|---|
| Knowledge base, embeddings, chunking, similarity search | M0b data, M1 retrieval | Met |
| Advanced RAG: query translation and metadata filters | M2: self-query filter with fallback; translation tested and rejected | Met |
| At least 3 tool calls | M3: six tools with schemas and risk tiers | Met |
| Security, error handling, input validation | M4 attack harness, M5 typed errors and fallback | Met |
| UI showing context, sources, tool results, progress | M6 chat page; Flask, which the project owner accepted | Met |
| Bonus: prompt-injection protection, cost display, logging | M4, M6, status endpoint and traces | Met (three medium items) |
| Bonus: RAG evaluation | M7: retrieval on the test split read once | Partly: judge not validated |
| Bonus: hybrid search, remote MCP, tools as MCP | Not built | Not done |

## Architecture

The code has two layers. `src/milo` holds the application: a question reaches the Flask route, the answer loop retrieves passages, calls the model, runs tools and writes the result. `scripts` holds offline evaluation and maintenance. Storage sits behind one interface, with an in-memory implementation and a PostgreSQL implementation on Supabase (schema `milo_v2`). The primary model is reached through OpenRouter; a local Ollama model is the fallback, and it can answer only from passages.

## Main processes

1. **Ask a question**: a request enters the web route, the app reads the conversation so far, retrieves up to five scored passages, calls the model, executes any tool calls, saves the turn and writes a trace line.
2. **Open the chat**: the page loads and fetches earlier turns for the same browser session.
3. **Monitor**: the status endpoint reports database reachability, row counts, the fallback model and spend against the course cap.
4. **Start up**: the knowledge base is loaded, chunked and indexed before the first question.
5. **Estimate an effect**: the model asks for an estimate; the code reads the owner's recorded facts and computes a range. The model never supplies the number.
6. **Evaluate**: scripts run retrieval, tool, attack and judge evaluations on the gold sets and write result files.

## Results

- 78 offline tests pass, with 3 database tests skipped unless enabled. The kit contract passes 9 of 9 groups.
- Retrieval on the dev split: recall@5 0.81, nDCG@5 0.68 (live embedding). On the test split, read once: recall@5 0.81, nDCG@5 0.72.
- Filter (M2): nDCG@5 rose from 0.16 to 0.27 on dev, interval 0.02 to 0.22. Adopted on dev only; not confirmed on test.
- Tools (M3): correct tool selection 0.55 to 0.60 across two runs; no over-eager calls.
- Attacks (M4): 0 of 10 succeeded, 0 of 5 benign questions refused. The sample is small.
- Judge (M7): not usable. Agreement with 40 labels from a model was 82.5%, kappa 0.60, lower bound 0.29, just below the rule of 0.30.

## Risks and limits

- The database uses the admin role. A least-privilege role is needed before any real data.
- The judge labels were written by a model, so judge agreement measures model-to-model agreement, not agreement with a person.
- The M2 filter was chosen after looking at the dev questions, and its test confirmation is outstanding.
- The status endpoint reports a course cap hard-coded at 3 USD, and the eval script `scripts/eval_tools.py` accepts a cost cap it does not enforce.

## Next steps

1. Decide whether the judge is a reported metric. If so, label items with a person and re-run.
2. Create a least-privilege database role.
3. Review and merge the stacked pull requests #15 to #23, and open one for the UI branch.
4. Record a browser walk-through of the manual checklist in `docs/lessons/M6.md`.
