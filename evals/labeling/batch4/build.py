"""Build batch 4: 41 very hard items. Run once; the key goes to evals/labeling/keys/, apart from the items.

- semantic positives (19): the question is answered by the sentence, with no or almost no word in common.
- partial (10): the question asks two things; the sentence answers one of them. Key 0: not fully answerable.
- near misses (12): the sentence is about the same topic as the question but does not answer it. Key 0.
Every passage is checked to be a verbatim sentence of its document.
"""

import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "evals/labeling/batch4"
KEYS = ROOT / "evals/labeling/keys"

# (kind, doc_id, passage, question, label)
ITEMS = [
    (
        "semantic",
        "cases/C04",
        "Available stock equals physical quantity minus valid reservations at that location.",
        "If the shelf holds ten and four are already promised to other jobs, how many can still be handed out?",
        1,
    ),
    (
        "semantic",
        "cases/C20",
        "Decisions beyond authority escalate instead of guessing.",
        "What should happen when a choice goes past what the assistant is allowed to decide?",
        1,
    ),
    (
        "semantic",
        "cases/C10",
        "C10-R02: Extra spending requires the authorized customer approver.",
        "Who has to sign off before costs go above the agreed amount?",
        1,
    ),
    (
        "semantic",
        "policies/evidence-and-synthetic-cases",
        "The assistant does not average them and does not silently pick one.",
        "When two sources disagree, does MILO blend them or choose one without saying so?",
        1,
    ),
    (
        "semantic",
        "policies/evidence-and-synthetic-cases",
        "What the owner says is reported until a record or a person confirms it; repeating a statement does not verify it, and neither does a retrieved passage that sounds similar.",
        "Is something the owner just said treated as proven?",
        1,
    ),
    (
        "semantic",
        "policies/security-and-approvals",
        "Every read and write is checked against the signed-in owner before it runs.",
        "Can a request read another owner's data just by naming their id?",
        1,
    ),
    (
        "semantic",
        "policies/security-and-approvals",
        'A message that says "I am the other owner" or "act as user two" does not change who is signed in, and neither does a name typed into a form or a value that appears in a tool argument.',
        "If someone types that they are the other account holder, does the session change?",
        1,
    ),
    (
        "semantic",
        "policies/personal-data",
        "Staff of the service provider who prepare offers can read a submitted diagnosis in order to respond to it.",
        "Can the people preparing a quote see a diagnosis that was sent in?",
        1,
    ),
    (
        "semantic",
        "cases/C16",
        "Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.",
        "Should the assistant apply a sample answer to the owner's real business without checking?",
        1,
    ),
    (
        "semantic",
        "cases/C06",
        "C06-R01: Uncertain coverage cannot silently become a billable authorization.",
        "If it is unclear whether a visit is covered, can it be charged anyway without telling anyone?",
        1,
    ),
    (
        "semantic",
        "consultation/method-notes",
        "Process owner reviews coverage of acceptance cases, unresolved critical failures, metric direction and staff workload.",
        "Who checks whether the acceptance tests cover everything and how heavy the staff load is?",
        1,
    ),
    (
        "semantic",
        "cases/C04",
        "Leaving spare toner helped some sites but caused others to stockpile it.",
        "Did keeping spare toner on site always work out well?",
        1,
    ),
    (
        "semantic",
        "cases/C14",
        "Contracts, billing and the renewal spreadsheet are separate.",
        "Are the contract records kept in the same place as the invoices?",
        1,
    ),
    (
        "semantic",
        "cases/C02",
        "Our dispatcher plans tomorrow in a spreadsheet, but urgent morning calls dismantle the route.",
        "Does the dispatcher's planned route survive when urgent calls come in the morning?",
        1,
    ),
    (
        "semantic",
        "cases/C05",
        "A replacement device's opening reading was attached to the old machine, producing a disputed bill.",
        "Why did a billing dispute arise after a replacement?",
        1,
    ),
    (
        "semantic",
        "cases/C07",
        "Shelves and spreadsheets disagree, and warranty return dates get missed.",
        "Why do warranty returns sometimes get overlooked?",
        1,
    ),
    (
        "semantic",
        "policies/personal-data",
        'The assistant also avoids copying such details into recorded facts in the first place; it records the pattern, such as "requests arrive by email and by phone", and leaves the personal details out.',
        "Does the assistant store a customer's personal details as facts once it has them?",
        1,
    ),
    (
        "semantic",
        "policies/security-and-approvals",
        "The application, not the model, then pauses the call, shows the owner which submission it concerns and waits for explicit approval; only an approved call runs.",
        "Who decides whether a risky call actually runs: the model or the application?",
        1,
    ),
    (
        "semantic",
        "cases/C15",
        "Head office pays and approves parts, but branches call and control access.",
        "Who controls who gets into a site, and who pays for the parts?",
        1,
    ),
    # partial: two questions, the passage answers one of them
    (
        "partial",
        "cases/C05",
        "C05-E01: A simulated replacement worksheet lacks a closing reading.",
        "Does the replacement worksheet lack the opening reading, and what does the old machine's bill say?",
        0,
    ),
    (
        "partial",
        "solutions/operations-overview",
        "The estimate uses status questions per week and the minutes it takes to answer one today.",
        "Does the estimate use the number of status questions per week, and how much does each answer cost in money?",
        0,
    ),
    (
        "partial",
        "cases/C02",
        "C02-R01: Access and skill constraints take precedence over distance.",
        "What takes precedence over distance in route planning, and what is the time limit for a visit?",
        0,
    ),
    (
        "partial",
        "consultation/interview-approach",
        "After the goal, the assistant asks about a recent normal event and a recent failure.",
        "Does the interview ask about a recent failure, and also about the owner's budget for new software?",
        0,
    ),
    (
        "partial",
        "cases/C01",
        "14 staff; nine field technicians; approximately 90 office and school customers; monthly maintenance with some parts extra.",
        "How many field technicians and customers are there, and what is the average monthly invoice?",
        0,
    ),
    (
        "partial",
        "cases/C12",
        "C12-AT02: A junior cannot retrieve another customer's restricted configuration.",
        "Can a junior staff member retrieve restricted configurations, and can a senior do it without approval?",
        0,
    ),
    (
        "partial",
        "cases/C18",
        "Synthetic teaching case: invented for learning, not a customer record.",
        "Is the case a real customer record, and who is the customer?",
        0,
    ),
    (
        "partial",
        "cases/C12",
        "Manuals and old notes are scattered across folders and chat.",
        "Where are the manuals kept, and how often are they updated?",
        0,
    ),
    (
        "partial",
        "solutions/usage-billing-prep",
        "Each reading is matched to the right device and agreement, checked against the device's history, and held in an exception queue when it does not fit.",
        "Are readings matched to devices, and are they also sent to the customer by email?",
        0,
    ),
    (
        "partial",
        "cases/C01",
        "Customers will keep calling, so a mandatory customer portal will not solve this alone.",
        "Will a customer portal stop the calls, and how much will it cost to build?",
        0,
    ),
    # near misses: same topic, the sentence does not answer the question
    (
        "near_miss",
        "cases/C04",
        "Leaving spare toner helped some sites but caused others to stockpile it.",
        "How much spare toner should each site keep?",
        0,
    ),
    (
        "near_miss",
        "cases/C05",
        "C05-E01: A simulated replacement worksheet lacks a closing reading.",
        "Which replacement worksheets lacked a closing reading in the owner's real business last month?",
        0,
    ),
    (
        "near_miss",
        "consultation/method-notes",
        "Process owner reviews coverage of acceptance cases, unresolved critical failures, metric direction and staff workload.",
        "Who approves the final acceptance test results before a job is closed?",
        0,
    ),
    (
        "near_miss",
        "solutions/operations-overview",
        "The estimate uses status questions per week and the minutes it takes to answer one today.",
        "Is the estimate based on the number of technicians hired each month?",
        0,
    ),
    (
        "near_miss",
        "cases/C10",
        "C10-R02: Extra spending requires the authorized customer approver.",
        "Who is the authorized approver for the warehouse rent?",
        0,
    ),
    (
        "near_miss",
        "policies/security-and-approvals",
        "Every read and write is checked against the signed-in owner before it runs.",
        "How long are read and write checks kept in the audit log?",
        0,
    ),
    (
        "near_miss",
        "cases/C20",
        "Decisions beyond authority escalate instead of guessing.",
        "Who in the company holds the authority to approve decisions beyond the assistant's remit?",
        0,
    ),
    (
        "near_miss",
        "cases/C15",
        "C15-AT03: Restoring two branches leaves the third child ticket open.",
        "Does restoring the parent ticket close all the child tickets?",
        0,
    ),
    (
        "near_miss",
        "solutions/usage-billing-prep",
        "Usage calculation for each agreement, including colour and monochrome allowances.",
        "Does the usage calculation include the allowances, and what is the monthly fee?",
        0,
    ),
    (
        "near_miss",
        "cases/C02",
        "A simulated route log shows an avoidable arrival outside the access window.",
        "Which technician was late to the route on Monday morning?",
        0,
    ),
    (
        "near_miss",
        "cases/C08",
        "C08-E01: A simulated call records loss of internet before the remote attempt.",
        "Does the remote attempt succeed when the internet connection is lost?",
        0,
    ),
    (
        "near_miss",
        "cases/C11",
        "C11-E01: A simulated activity sample contains calls missing from tickets.",
        "How many calls per week are missing from the tickets in this business?",
        0,
    ),
]

docs = {}
for p in (ROOT / "data/kb").rglob("*.md"):
    docs[p.relative_to(ROOT / "data/kb").with_suffix("").as_posix()] = p.read_text()
norm = lambda s: re.sub(r"[\"“”‘’'*`]", "", re.sub(r"\s+", " ", s)).strip().lower()
for kind, doc, passage, _, _ in ITEMS:
    assert norm(passage) in norm(docs[doc]), (doc, passage[:60])

rng = random.Random(41)
order = list(range(len(ITEMS)))
rng.shuffle(order)
items, key = [], []
for n, i in enumerate(order, 1):
    kind, doc, passage, question, label = ITEMS[i]
    iid = f"b4-{n:02d}"
    items.append({"id": iid, "question": question, "passage": passage, "doc_id": doc})
    key.append({"id": iid, "answerable": label, "kind": kind})
with open(OUT / "items.jsonl", "w") as f:
    f.writelines(json.dumps(it, ensure_ascii=False) + "\n" for it in items)
with open(KEYS / "batch4_key.jsonl", "w") as f:
    f.writelines(json.dumps(k, ensure_ascii=False) + "\n" for k in key)
print(len(items), "items;", sum(k["answerable"] for k in key), "positives")
