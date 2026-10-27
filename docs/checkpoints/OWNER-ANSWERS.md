# Checkpoint answers: to be written by the owner

Source: the course checkpoints (`project-kit/CHECKPOINTS.md`). Answer each question in your own words, two or three
sentences each, then rehearse the reviewer prompt aloud in two minutes. The milestone is not done if you cannot answer.
The assistant has not written any of these answers, and should not.

## M0 Domain and data

1. Which question types in your gold set are the hardest to retrieve, and why did you include them?

Answer:


2. How do you know no gold quote was written after looking at what your retriever returns?

Answer:


3. Which of your 10 attacks could really happen in this domain, and which are decoration?

Answer:


**Explain to a reviewer:** why this domain, and how your data lets you measure instead of guess (Understanding).

Answer:


## M1 Retrieval baseline

1. What does recall@5 miss that nDCG@5 shows, on your data?

Answer:


2. Which chunking choice did you make and what evidence supports it?

Answer:


3. How wide is the CI on the `test` split, and what does that say about differences smaller than it?

Answer:


**Explain to a reviewer:** how a question becomes an answer, stage by stage, and where each stage can fail (Understanding).

Answer:


## M2 Advanced RAG

1. When does your query translation hurt? Show one question.

Answer:


2. What happens when the self-query returns an invalid filter, and where is that tested?

Answer:


3. Does the paired CI of the A/B exclude zero? If not, what do you conclude?

Answer:


**Explain to a reviewer:** why one change helped and where its ceiling is (Understanding, Reflection).

Answer:


## M3 Tools

1. Which tool is the riskiest and which tier did you give it?

Answer:


2. What does the model see when a tool fails, and what does it do next?

Answer:


3. In your 15 cases, how many calls were over-eager, and what would you change?

Answer:


**Explain to a reviewer:** the loop from a tool call to the tool result and back, including `tool_call_id` (Understanding).

Answer:


## M4 Domain security

1. Which control stops a destructive call after an injected instruction, and is it code or prompt?

Answer:


2. What is your ASR and false-refusal rate, and what is the trade-off between them?

Answer:


3. Where does the identity come from at the moment a tool runs?

Answer:


**Explain to a reviewer:** defence in depth for injection in your system, with the measured numbers (Technical implementation, security).

Answer:


## M5 LangChain integration and errors

1. Which errors are typed, and what does the user see for each?

Answer:


2. What are your retry and timeout limits, and why those values?

Answer:


3. What does one trace tell you that the logs did not?

Answer:


**Explain to a reviewer:** what happens, step by step, when the provider times out in the middle of a tool loop (Understanding, Technical implementation).

Answer:


## M6 UI

1. Can a user tell, from the screen alone, why the answer says what it says?

Answer:


2. What does the user see when a tool is blocked?

Answer:


3. Which of the manual checklist items failed the first time?

Answer:


**Explain to a reviewer:** how the UI shows context, sources, tool results and progress (Technical implementation).

Answer:


## M7 Evaluation and reflection

1. Against how many hand labels did you calibrate the judge, and what was the agreement?

Answer:


2. Which metric would you not trust for a decision, and why?

Answer:


3. Which limit in your report would surprise a user?

Answer:


**Explain to a reviewer:** your limits section, with numbers and intervals, and what you would try next (Reflection).

Answer:


## Notes for the owner

- `docs/lessons/M7.md` already has an answer under question 1 (30 labels, agreement 63 per cent, kappa 0.16). That text was written earlier and does not match the current numbers (the judge on 40 labels: agreement 0.825, kappa 0.595). Replace it with your own answer after checking the figures in `evals/judge/`.
- `docs/lessons/M6.md` still says the screen recording has not been made. The recording now exists: `docs/video/demo-recording/`.
