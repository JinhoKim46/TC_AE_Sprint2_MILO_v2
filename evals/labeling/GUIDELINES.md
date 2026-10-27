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

## 6. Decision rules for answer labels (added after batch 5)
These rules were added after the first answer batch, where the two labelers disagreed on 7 of 30 faithfulness labels.
They make the existing section 3 concrete. They do not change the threshold in section 5.

- **Overstatement:** an answer that strengthens a passage (for example "categorically", "automatically", "a hard
  constraint", "always") is unsupported when the passage says less. Write the stronger word in your reason.
- **Claims about the knowledge base:** "the knowledge base has no passage about X" is a claim about the whole knowledge
  base. With the passages given, judge it against those passages only. With no passages at all, it is unsupported (0),
  unless the answer is the plain abstention "I do not know" with a request for detail.
- **Procedures and purposes not in the passages:** a step, a deadline, a reason or a purpose that the passages do not state
  makes the answer unsupported (0), even if it sounds sensible. The answer may say the passages give no procedure.
- **Restrictions:** if the passage limits a claim (for example to staff who prepare offers), an answer that drops the
  limit is unsupported (0).
- **Cautious wording is fine:** "the passages do not say" and "this is only what the passages support" are not claims.
- **Relevance is separate:** an answer that addresses the question is relevant even if it is wrong. An answer that only
  asks for detail, and does not address the question, is not relevant (0).
