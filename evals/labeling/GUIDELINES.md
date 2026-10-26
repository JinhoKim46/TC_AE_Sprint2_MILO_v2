# Labeling guidelines for the LLM labeler

These rules are for the LLM that labels MILO's evaluation items. No human labels are used anywhere. The goal is that
two labelers following these rules agree closely; agreement is measured, not assumed.

## 1. Retrieval gold (no judgement needed)
- A gold item names one document and one quote. The quote must appear word for word in that document. A script checks this.
- A question is only valid if the quote answers it. If you are unsure, mark the item `doubtful` instead of guessing.

## 2. Question writing (paraphrase items)
- Write the question as a person at a service business would ask it. Do not copy the quote's wording; use other words.
- The question must be answerable from the quoted sentence alone. If it needs a second passage, it is not a paraphrase item.
- Do not put the answer inside the question. Do not name the document, the case number, or the section.
- Identifier items may name a case (for example C07) but still must not copy the quote.
- Unanswerable items are questions about something the knowledge base does not cover (prices, a named competitor, a
  customer's own system). Their gold evidence is empty.

## 3. Faithfulness and relevance of an answer (answer labels)
- `faithful = 1` only if every factual claim in the answer is supported by the passages the answer was given.
  A claim that goes beyond the passages makes it 0. A cautious statement such as "the passages do not say" is fine.
- `relevant = 1` if the answer addresses the question, even if it is incomplete.
- Judge only what is written. Do not reward a correct answer that the passages do not support.

## 4. Consistency
- Label the same item the same way every time. Quote the passage sentence that supports your decision.
- When in doubt between two labels, choose the one that counts the claim as unsupported and say why.

## 5. Agreement check
- Two labelers (different models) label the same sample of items with these rules.
- Report Cohen's kappa and raw agreement. Use a fixed rule: a label set is accepted when kappa >= 0.60 and the lower
  end of the 95% bootstrap interval is >= 0.30. If it is not accepted, change the guidelines, not the numbers.
- Items marked `doubtful` by either labeler are excluded from the agreement figure and reported separately.
