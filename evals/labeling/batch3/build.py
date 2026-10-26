"""Build batch 3: 60 items, mixed difficulty, positives and negatives. Run once; the key is written apart from the items.

Positives: the question's own quote (answerable from that sentence), chosen so that the question shares few words with it
(hard positives) and some that share many (easy positives).
Negatives: a sentence from another document of the same folder that does not answer the question. Hard negatives share
the most content words with the question; easy negatives are random.
"""
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "evals/labeling/batch3"
STOP = set("a an the of to in on for and or is are be with by at from that this it as do does what how which who your our we you my i me can could would should about into over than then there their them they its not no".split())


def words(t):
    return {w for w in re.findall(r"[a-z0-9]+", t.lower()) if w not in STOP}


def overlap(q, s):
    wq, ws = words(q), words(s)
    return len(wq & ws) / max(1, len(wq))


rng = random.Random(11)
gold = [json.loads(l) for l in open(ROOT / "data/gold_dev_extra.jsonl")]
qs = [r for r in gold if r["type"] in ("paraphrase", "identifier") and r["gold_evidence"]]
# every sentence of the knowledge base, as a candidate negative
sentences = []
for p in sorted((ROOT / "data/kb").rglob("*.md")):
    doc = p.relative_to(ROOT / "data/kb").with_suffix("").as_posix()
    body = re.sub(r"^---.*?---", "", p.read_text(), flags=re.S)
    for line in body.splitlines():
        line = re.sub(r"^[#>\-\*\s]+", "", line).strip()
        for sent in re.split(r"(?<=[.!?])\s+", line):
            if 40 <= len(sent) <= 220:
                sentences.append((doc, sent.strip()))

items, key = [], []


def add(kind, qid, question, doc, passage, label, difficulty):
    iid = f"b3-{len(items) + 1:02d}"
    items.append({"id": iid, "question": question, "passage": passage, "doc_id": doc})
    key.append({"id": iid, "answerable": label, "kind": kind, "difficulty": difficulty, "source_qid": qid})


# positives: 30. Take the 15 with the lowest word overlap (hard) and the 15 with the highest (easy).
scored = sorted(qs, key=lambda r: overlap(r["question"], r["gold_evidence"][0]["quote"]))
hard_pos = scored[:15]
easy_pos = scored[-15:]
for r in hard_pos:
    e = r["gold_evidence"][0]
    add("positive", r["qid"], r["question"], e["doc_id"], e["quote"], 1, "hard")
for r in easy_pos:
    e = r["gold_evidence"][0]
    add("positive", r["qid"], r["question"], e["doc_id"], e["quote"], 1, "easy")

# negatives: 30. Each one is paired with a question from another item; the sentence is from another document of the
# same folder, and it must not be the question's own quote. Hard: the most overlapping sentence in that folder.
used_q = [r for r in qs]
neg_plan = [("hard", 15), ("easy", 15)]
for diff, count in neg_plan:
    for _ in range(count):
        r = rng.choice(used_q)
        folder = r["gold_evidence"][0]["doc_id"].split("/")[0]
        own = r["gold_evidence"][0]["doc_id"]
        pool = [(d, s) for d, s in sentences if d.split("/")[0] == folder and d != own and overlap(r["question"], s) < 0.8]
        if diff == "hard":
            pool.sort(key=lambda ds: -overlap(r["question"], ds[1]))
            doc, sent = rng.choice(pool[:10])
        else:
            doc, sent = rng.choice(pool)
        add("negative", r["qid"], r["question"], doc, sent, 0, diff)

order = list(range(len(items)))
rng.shuffle(order)
items = [items[i] for i in order]
key = [key[i] for i in order]
# renumber after the shuffle so ids are neither grouped nor in difficulty order
for n, (it, k) in enumerate(zip(items, key), 1):
    new = f"b3-{n:02d}"
    it["id"] = new
    k["id"] = new
with open(OUT / "items.jsonl", "w") as f:
    for it in items:
        f.write(json.dumps(it, ensure_ascii=False) + "\n")
with open(ROOT / "evals/labeling/keys/batch3_key.jsonl", "w") as f:  # the answer key: for the owner only, never given to a labeler
    for k in key:
        f.write(json.dumps(k, ensure_ascii=False) + "\n")
print(len(items), "items;", sum(k["answerable"] for k in key), "positives")
