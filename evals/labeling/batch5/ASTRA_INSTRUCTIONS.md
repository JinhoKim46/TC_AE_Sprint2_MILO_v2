# Batch 5: answer labels for Astra (faithfulness and relevance)

## What to do
1. Read `../GUIDELINES.md` completely, especially section 3. Follow it exactly. Do not add your own rules.
2. Open `items.jsonl`. Each line is one item: a `question`, the system's `answer`, and the `passages` the answer was
   allowed to use (numbered `n`).
3. For each item give two labels:
   - `faithful`: 1 only if every factual claim in the answer is supported by the passages. A claim that goes beyond the
     passages, or says a passage states something it does not, makes it 0. Cautious statements such as "the passages do
     not say" are fine. If there are no passages and the answer makes a factual claim, use 0.
   - `relevant`: 1 if the answer addresses the question asked, even if it is incomplete. Otherwise 0.
   - Use `"doubtful"` for either label only when the guidelines do not let you decide.
4. Write `labels_astra.jsonl` in this folder: one line per item, in the same order:
   `{"id": "a01", "faithful": 1, "relevant": 1, "reason": "one short sentence, quoting a few words of the passage or the answer"}`
5. Do not use any other file in the repository and do not look at other labels.

## What to send back
- `labels_astra.jsonl` with 30 lines (one per item).
