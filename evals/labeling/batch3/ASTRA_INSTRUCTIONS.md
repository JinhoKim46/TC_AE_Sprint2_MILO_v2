# Batch 3: question labels for Astra (60 items, mixed difficulty, positives and negatives)

## What to do
1. Read `../GUIDELINES.md` completely. Follow it exactly. Do not add your own rules.
2. Open `items.jsonl` (60 items; some pair a question with a sentence that does not answer it, some are hard to tell apart). Each line is one item with a `question` and a `passage` (one sentence from a document).
3. For each item decide one label:
   - `1` if the question can be answered from the passage alone (the passage is enough, no other passage needed).
   - `0` if the passage does not answer the question.
   - `"doubtful"` if you cannot decide with the guidelines.
4. Write one line per item into `labels_astra.jsonl (in this folder)`, in the same order:
   `{"id": "q101", "answerable": 1, "reason": "one short sentence"}`
   Do not change the `id`. The reason must quote a few words of the passage that support your label.
5. Do not look at any other file in the repo or at other labels. Do not use the passage's document beyond this one sentence.

## What to send back
- The file `labels_astra.jsonl` in this folder, with 60 lines (one per item).
