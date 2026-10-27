# Checkpoint answers: to be written by the owner

Source: the course checkpoints (`project-kit/CHECKPOINTS.md`). Answer each question in your own words, two or three
sentences each, then rehearse the reviewer prompt aloud in two minutes. The milestone is not done if you cannot answer.
The assistant has not written any of these answers, and should not.

## M0 Domain and data

1. Which question types in your gold set are the hardest to retrieve, and why did you include them?

Draft (rewrite in your own words): Hardest to retrieve: paraphrased questions, which the owner would really ask. On dev the offline embeddings gave recall@5 0.09 on paraphrases, and Gemini gave 0.73 (`evals/results/retrieval/`). Identifier and unanswerable questions were included so the set covers the case ids and the refusals.


2. How do you know no gold quote was written after looking at what your retriever returns?

Draft (rewrite in your own words): The quotes were copied from the documents, and a script checks every quote is verbatim (`scripts/check_project_data.py`, `tests/test_data.py`). The 40 extra dev items were written by a model from the knowledge base, which is a weaker guarantee than writing them by hand, and the notes say so.


3. Which of your 10 attacks could really happen in this domain, and which are decoration?

Draft (rewrite in your own words): Realistic: the direct requests and the knowledge-base injections (atk02, atk05, atk06), because a service-business owner could paste a document that contains instructions. Decoration: anything that needs a power the app does not have, such as a second user's session (atk09 is only meaningful with the owner's approval). Check `data/attacks.jsonl` for the wording.


**Explain to a reviewer:** why this domain, and how your data lets you measure instead of guess (Understanding).

Draft (rewrite in your own words): 


## M1 Retrieval baseline

1. What does recall@5 miss that nDCG@5 shows, on your data?

Draft (rewrite in your own words): recall@5 only asks whether the right chunk is in the top five. nDCG@5 also rewards a higher position. On the held-out set the dense arm had recall 0.78 and nDCG 0.60, so the right chunk is often found but not always near the top.


2. Which chunking choice did you make and what evidence supports it?

Draft (rewrite in your own words): Heading-aware chunks of 800 characters with 100 overlap. The evidence: no gold quote is split across chunks (`quotes_not_whole_in_a_chunk` is 0 in every result file), and each chunk keeps its section heading. I did not compare other chunk sizes, so say that plainly.


3. How wide is the CI on the `test` split, and what does that say about differences smaller than it?

Draft (rewrite in your own words): On the test split the nDCG@5 is 0.72 with a 95% interval of about 0.52 to 0.90 (16 items). A difference smaller than about 0.2 cannot be told apart from noise at this size.


**Explain to a reviewer:** how a question becomes an answer, stage by stage, and where each stage can fail (Understanding).

Draft (rewrite in your own words): Explain to a reviewer: a question is embedded, the nearest chunks are taken from the index, the top five are numbered and given to the model, the model answers with the numbers it used, and the answer is refused when nothing matches. It fails when a paraphrase misses the embedding, when a quote is split across chunks, or when the model claims more than the passages say.


## M2 Advanced RAG

1. When does your query translation hurt? Show one question.

Draft (rewrite in your own words): Query translation hurts when the rewrite drops a case id or a rare word that the lexical search needs. Pick one question from `data/gold.jsonl` (dev split) and check the translated query yourself; I did not record a single worked example.


2. What happens when the self-query returns an invalid filter, and where is that tested?

Draft (rewrite in your own words): The self-query output is checked against a schema (only the allowed keys and values). An invalid output is discarded and the search runs unfiltered. This is tested in `tests/test_advanced.py` (`test_invalid_self_query_output_falls_back_to_unfiltered_search`).


3. Does the paired CI of the A/B exclude zero? If not, what do you conclude?

Draft (rewrite in your own words): Yes, on dev: the filter arm gained 0.110 nDCG@5 with a paired interval of 0.016 to 0.222. But I revised the rule once after looking at dev, so the conclusion is that it is adopted on dev and unconfirmed on test. The test split was already read once, so it has not been checked.


**Explain to a reviewer:** why one change helped and where its ceiling is (Understanding, Reflection).

Draft (rewrite in your own words): Explain to a reviewer: the self-query narrows the search to one service area when the question names one, which helped the case-id questions. Its ceiling: it only helps when the question names an area or case, and it was validated on dev only.


## M3 Tools

1. Which tool is the riskiest and which tier did you give it?

Draft (rewrite in your own words): `reset_diagnosis`. It is destructive: the app runs it only after the owner approves, and the agent path pauses it with a human-in-the-loop step (`src/milo/agent_app.py`).


2. What does the model see when a tool fails, and what does it do next?

Draft (rewrite in your own words): The tool returns a JSON result with `ok` and an error text, and the model sees it as a tool message. The model can then ask the owner for the missing argument or answer without the tool. The loop stops after a fixed number of steps.


3. In your 15 cases, how many calls were over-eager, and what would you change?

Draft (rewrite in your own words): In the app's own loop, none of the 20 cases produced an over-eager call. With the `create_agent` engine, four calls came from one greeting-type question (case tc04). The change I would make: tighten the `search_knowledge` description so it is not used for questions about the assistant itself.


**Explain to a reviewer:** the loop from a tool call to the tool result and back, including `tool_call_id` (Understanding).

Draft (rewrite in your own words): Explain to a reviewer: the model proposes a tool call with an id, the code validates the arguments and runs the tool, and the result goes back to the model as a tool message with the same id, until the model answers.


## M4 Domain security

1. Which control stops a destructive call after an injected instruction, and is it code or prompt?

Draft (rewrite in your own words): A destructive call stops in code. The app's policy layer and the approval step (`src/milo/web.py` and `src/milo/agent_app.py`) decide it, not the prompt. The prompt only says what to do.


2. What is your ASR and false-refusal rate, and what is the trade-off between them?

Draft (rewrite in your own words): Attack success rate 0 of 10 and destructive success 0; false refusals 0 of 5 benign inputs. The trade-off: a stricter gate would block more benign requests, and this benign set is small.


3. Where does the identity come from at the moment a tool runs?

Draft (rewrite in your own words): The web session holds the owner id, set at sign-in. Tools receive the owner from the calling code, never from a model argument. The MCP server reads it from the bearer token.


**Explain to a reviewer:** defence in depth for injection in your system, with the measured numbers (Technical implementation, security).

Draft (rewrite in your own words): Explain to a reviewer: input is validated first, the policy decides each tool call, identity comes from the session, and destructive actions need an approval recorded on the server. The measured numbers are the attack table in M4.


## M5 LangChain integration and errors

1. Which errors are typed, and what does the user see for each?

Draft (rewrite in your own words): Input errors (`invalid_input`) show the owner a plain message. A provider failure shows a short generic message, and the exception type goes only into the trace, not to the user. No traceback reaches the screen.


2. What are your retry and timeout limits, and why those values?

Draft (rewrite in your own words): Two retries for the chat model and a 30-second request timeout. The retries are bounded so an outage cannot hang a question, and the timeout is short enough for the owner to see the failure. Both values are guesses that were checked only in the offline tests.


3. What does one trace tell you that the logs did not?

Draft (rewrite in your own words): The trace records each step with its time, the tool calls, the policy decision and the fallback. The logs did not carry the question text, which keeps the trace free of owner content.


**Explain to a reviewer:** what happens, step by step, when the provider times out in the middle of a tool loop (Understanding, Technical implementation).

Draft (rewrite in your own words): Explain to a reviewer: when the provider times out in the middle of a tool loop, the attempt is retried up to the limit, then the app falls back to the local model without tools, and the trace shows which step failed.


## M6 UI

1. Can a user tell, from the screen alone, why the answer says what it says?

Draft (rewrite in your own words): Partly. The answer shows numbered citations, the sources panel with the passage text, the steps taken and a confidence line. It does not show the model's reasoning, so the owner can see what was used but not why the model chose the words.


2. What does the user see when a tool is blocked?

Draft (rewrite in your own words): The step shows "Needs your approval", and the answer says "This action needs your approval first. Nothing was changed." The recording shows this.


3. Which of the manual checklist items failed the first time?

Draft (rewrite in your own words): The empty-message check. It failed in the first browser check because an empty send did nothing, so a hint was added. It still needs a browser re-check (see `docs/lessons/M6.md`).


**Explain to a reviewer:** how the UI shows context, sources, tool results and progress (Technical implementation).

Draft (rewrite in your own words): Explain to a reviewer: the answer comes with its numbered sources in a side panel; each tool call is listed with its arguments, result and policy decision; a progress line shows while the answer is made.


## M7 Evaluation and reflection

1. Against how many hand labels did you calibrate the judge, and what was the agreement?

Draft (rewrite in your own words): The judge was calibrated against 40 labels written by a model (Astra), not a human. Agreement 0.825 and kappa 0.595 with a lower bound of 0.29, which is below the rule (kappa at least 0.60 and lower bound at least 0.30). So the judge was not usable. (`evals/judge/judge_result_40_opus_vs_astra.json`.)


2. Which metric would you not trust for a decision, and why?

Draft (rewrite in your own words): Relevance. Every hand label was 1, so the agreement says nothing about relevance; it is not a usable metric. The judge's faithfulness numbers are the ones I would not trust for a decision either.


3. Which limit in your report would surprise a user?

Draft (rewrite in your own words): That only 16 answerable questions are in the test split, so every interval is wide, and that the M2 filter is still unconfirmed on test. Also that all the labels were written by models, not people.


**Explain to a reviewer:** your limits section, with numbers and intervals, and what you would try next (Reflection).

Draft (rewrite in your own words): Explain to a reviewer: the limits section lists each number with its interval, and the next step would be a fresh answer batch with human labels for a sample, plus a fixed rule for when a label set is accepted.


## Notes for the owner

- `docs/lessons/M7.md` already has an answer under question 1 (30 labels, agreement 63 per cent, kappa 0.16). That text was written earlier and does not match the current numbers (the judge on 40 labels: agreement 0.825, kappa 0.595). Replace it with your own answer after checking the figures in `evals/judge/`.
- `docs/lessons/M6.md` still says the screen recording has not been made. The recording now exists: `docs/video/demo-recording/`.
