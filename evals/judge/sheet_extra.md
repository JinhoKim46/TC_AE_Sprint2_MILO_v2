# Judge labelling sheet, second batch (10 items)

Read each question, answer and full passage set. Label faithful (1 if every claim is supported) and relevant (1 if the answer addresses the question).

## 1. S11
**Question:** Our busiest customer might actually be our least profitable one.

**Answer:** The passages don't say whether your busiest customer is your least profitable one, because they don't contain your data. They do show how this kind of mismatch can happen and what to check.

In the analogous case C11, the business knew revenue and payroll but not service cost by account. Short remote calls looked as heavy as long on-site repairs because both counted as one ticket, and driving, repeat visits and van parts were not tracked [3]. Telephone and travel activity were usually not recorded, so ticket totals understated resource use [1]. A busy account can therefore look costly or cheap depending on what is counted.

The same case also warns against acting on a profitability ranking alone. High service cost may reflect an intentional strategic account or a temporary project [1].

To test your question, you would need to know, for each customer:
- Contract revenue.
- Staff time, including calls, travel and on-site work, not only tickets.
- Repeat visits and parts used.

I can record these facts if you share them, then estimate the effect of automating request handling or draft a diagnosis for your operations.

- passage `cases/C11#004`: ### C11-Q01: Are telephone and travel activities recorded?

**Example answer in this fictional case:** Usually not.

**Why ask:** Ticket totals underestimate resource use.

**If the answer differs:** High service cost may reflect an intentional strategic account or temporary project; profitability ranking alone does not dictate termination.
- passage `cases/C11#000`: # C11: Contract revenue hides service burden

> Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.
- passage `cases/C11#001`: ## Business and opening narrative

20 staff; approximately 100 recurring contracts.

“We know revenue and payroll but not service cost by account. Short remote calls look like long on-site repairs when both count as one ticket. Driving, repeat visits and van parts are missing. Renewal prices follow intuition.”

**Typical symptom:** We know revenue and payroll but not service cost by account. Renewal prices follow intuition.
- passage `cases/C15#001`: ## Business and opening narrative

Maintenance provider for multi-site retail and education groups; one customer has 28 branches.

“Head office pays and approves parts, but branches call and control access. Branches expect appointments before approval arrives. Equipment moves between similar-named locations. Several apparently separate failures turned out to follow one central configuration change.”

**Typical symptom:** Head office pays and approves parts, but branches call and control access. Several apparently separate failures turned out to follow one central configuration change.
- passage `cases/C06#001`: ## Business and opening narrative

18 staff; approximately 110 mixed PC, printer and network maintenance customers.

“We dispatch when the customer is under contract, but that does not mean the device or work is covered. A personal laptop was repaired at an office, and a part replacement was waived because nobody warned the customer about the charge. Lists are outdated.”

**Typical symptom:** We dispatch when the customer is under contract, but that does not mean the device or work is covered. Lists are outdated.

## 2. S12
**Question:** When our senior technician is absent, the rest of the company slows down.

**Answer:** The passages support the pattern you describe, but only as analogous cases from other businesses. None of them measures how much the company slows down.

- **C12 (passages 1 and 3)** is the closest match. Its business has 13 staff, and two long-serving technicians carry most customer-specific knowledge. Juniors call seniors while both are on jobs, and manuals and notes are scattered, so a recurring configuration gets rediscovered repeatedly [3]. The case's own summary is that senior technicians are the only knowledge base [1].
- **C20 (passage 2)** shows a similar dependency on one person. When the owner was away for three days, someone revisited a customer before the part arrived, and invoices stopped because nobody knew what had been promised [2].

The passages don't give figures for how much work slows or for how long, so I can't estimate the effect from them.

I haven't recorded anything, because your message doesn't say which of your business facts it corresponds to. If you tell me about a recent absence, such as what stalled and for how long, I can record it as your incident story. I can also draft a diagnosis for an area such as request dispatch once I have enough of your facts.

- passage `cases/C12#000`: # C12: Senior technicians are the only knowledge base

> Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.
- passage `cases/C20#001`: ## Business and opening narrative

Six staff: owner, four technicians and administrator; plans to hire two more technicians.

“I coordinate everything through messages and memory. When I took three days away, someone revisited a customer before the part arrived, and invoices stopped because nobody knew what I promised. We have spreadsheets and calendars, but I connect them in my head.”

**Typical symptom:** I coordinate everything through messages and memory. We have spreadsheets and calendars, but I connect them in my head.
- passage `cases/C12#001`: ## Business and opening narrative

13 staff; two long-serving technicians carry most customer-specific knowledge.

“Juniors call seniors while both are on jobs. Manuals and old notes are scattered across folders and chat. A recurring school printer configuration is repeatedly rediscovered. End-of-day notes just say fixed, and seniors worry about procedures being applied without their exceptions.”

**Typical symptom:** Juniors call seniors while both are on jobs. End-of-day notes just say fixed, and seniors worry about procedures being applied without their exceptions.
- passage `cases/C07#001`: ## Business and opening narrative

Nine-person business PC and laptop repair provider.

“Technicians identify a part, office staff ask suppliers, and customers approve quotes. The gaps between those steps last days. An approval sent to a technician never reached purchasing. Shelves and spreadsheets disagree, and warranty return dates get missed.”

**Typical symptom:** Technicians identify a part, office staff ask suppliers, and customers approve quotes. Shelves and spreadsheets disagree, and warranty return dates get missed.
- passage `cases/C02#001`: ## Business and opening narrative

22 staff; 15 field technicians covering a city and surrounding towns.

“Our dispatcher plans tomorrow in a spreadsheet, but urgent morning calls dismantle the route. The nearest worker may lack the skill, part or customer authorization. We redirected someone to a school whose key holder was absent, losing both the urgent visit and the original slot.”

**Typical symptom:** Our dispatcher plans tomorrow in a spreadsheet, but urgent morning calls dismantle the route. We redirected someone to a school whose key holder was absent, losing both the urgent visit and the original slot.

## 3. S13
**Question:** The technician finishes the repair, but our office still has half the job left.

**Answer:** The passages describe a similar pattern, but they come from fictional teaching cases, so they don't establish what happens in your office.

In case C13, "Completed work waits for paperwork." The workflow runs: repair completed, paper notes captured, office transcribes, missing information chased, customer report prepared, acceptance obtained, invoice released [5][2]. The office's half of the job is the stretch after the repair, when notes are transcribed, gaps are chased, and the report, acceptance, and invoice are handled [2].

Case C19 shows a related pattern, where the office rekeys updates from technicians and the manager asks for a spreadsheet afterward [3].

The passages don't tell me your steps, timings, or volumes. To see where your half of the job goes, I'd need to know:
- What the technician hands back after a repair (paper notes, a message, a verbal update)?
- What the office re-enters or chases before the job can be closed and invoiced?
- How many jobs a week go through this, and roughly how long the office step takes?

If you share those, I can record them as facts and draft a diagnosis for your situation.

- passage `cases/C03#005`: ### C03-Q02: Did emergency work satisfy those checks?

**Example answer in this fictional case:** The technician fixed one printer but did not inspect the lab.

**Why ask:** Attendance cannot substitute for task evidence.
- passage `cases/C13#002`: ## Current workflow

1. Repair completed
2. Paper notes captured
3. Office transcribes
4. Missing information chased
5. Customer report prepared
6. Acceptance obtained
7. Invoice released
- passage `cases/C19#002`: ## Current workflow

1. Office opens ticket
2. Office duplicates assignment in chat
3. Technician works
4. Update sent in chat
5. Office rekeys
6. Manager asks for spreadsheet
- passage `cases/C01#002`: ## Current workflow

1. Customer reports by phone or message
2. Recipient records selectively
3. Coordinator assigns in chat
4. Technician travels
5. Repair reported informally
- passage `cases/C13#000`: # C13: Completed work waits for paperwork

> Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.

## 4. S14
**Question:** We remember renewals only when a customer asks why nobody has contacted them.

**Answer:** The passages don't include a question for me to answer, so I can only summarize what they cover.

They describe two fictional cases about follow-up ownership:

- **C14 (renewals, rental and maintenance provider, about 140 active agreements):** Contracts, billing and the renewal spreadsheet are kept separately, and email extensions and added equipment stay in messages [3]. The workflow runs from sales agreeing terms, to storing the signed file, to billing setup, to changes exchanged by email, to a selectively updated renewal sheet, and the customer is often contacted late [2]. A customer arranged a competitor's copier while the provider thought renewal was months away [3]. The suggested fixes are process first: review the agreement and amendments, assign an account owner, and separate notice, review and end dates. Automation and bounded AI would extract date candidates for review, maintain effective terms, and prepare account summaries and internal renewal tasks [4].
- **C07 (overdue items):** The example answer is that whoever receives a customer complaint checks overdue items, which shows follow-up ownership is absent [5]. The case notes that renewals are remembered only when a customer asks why nobody has contacted them [5].

Both cases point to the same gap: no one is explicitly responsible for follow-up, so problems surface through customer complaints.

If you meant to ask something specific, such as how to assign renewal ownership or what the diagnosis would look like for your business, tell me and I'll work from these passages or from facts you give me. I have not recorded any facts about your business, since none were stated in the passages.

- passage `cases/C14#005`: ### C14-Q02: Who owns renewal follow-up?

**Example answer in this fictional case:** Sales and accounts each assumed the other was tracking it.

**Why ask:** Ownership is explicit work.
- passage `cases/C14#002`: ## Current workflow

1. Sales agrees terms
2. Signed file stored
3. Billing configured
4. Changes exchanged by email
5. Renewal sheet updated selectively
6. Customer contacted late
- passage `cases/C14#001`: ## Business and opening narrative

Rental and maintenance provider; approximately 140 active agreements.

“Contracts, billing and the renewal spreadsheet are separate. Email extensions and added equipment remain in messages. A customer arranged a competitor’s copier while we thought renewal was months away. Sales lacks a reliable service history before discussing the next agreement.”

**Typical symptom:** Contracts, billing and the renewal spreadsheet are separate. Sales lacks a reliable service history before discussing the next agreement.
- passage `cases/C14#011`: ## Interventions

**Process first:** Review the current agreement and amendments; assign an account owner and separate notice, review and end dates.

**Automation and bounded AI help:** Extract date candidates for review; maintain effective terms; prepare account summaries and internal renewal tasks.
- passage `cases/C07#006`: ### C07-Q03: Who checks overdue items?

**Example answer in this fictional case:** Whoever receives a customer complaint.

**Why ask:** Follow-up ownership is absent.

## 5. S15
**Question:** The customer's head office approves the work, but the branches control whether we can do it.

**Answer:** The passages suggest treating cost approval and site access as two separate permissions, and confirming both with the actual customer.

In the teaching case, head office approves cost and the branch agrees access [3]. The case flags this as a question to ask because these are separate permissions [3]. The general guidance is the same: separate site access from spending authority [4].

Your workflow has the conflict built in. Head-office approval is sought at step 4, and the branch appointment is arranged at step 5 [5]. The case describes branches expecting appointments before approval arrives [2], so the branch may be waiting on approval that has not yet come through, or the appointment may be fixed before cost is approved.

The passages also describe related patterns to check:
- Similar symptoms across branches may be independent hardware faults. Common timing across sites is a hypothesis, not proof [3].
- In the case, several apparently separate failures followed one central configuration change [2]. Equipment also moved between similar-named locations [2].

If the same instructions are repeatedly ignored, the case suggests partner performance management may be needed beyond software [4].

I have not recorded anything about your business, because the passages describe a fictional case. Before designing anything, you would need to confirm with your customer who approves spend, who controls access, and whether appointments can be booked before approval. The passages do not say how your customer handles these, so I can't answer that from them.

- passage `cases/C15#000`: # C15: Branch access and head-office approval conflict

> Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.
- passage `cases/C15#001`: ## Business and opening narrative

Maintenance provider for multi-site retail and education groups; one customer has 28 branches.

“Head office pays and approves parts, but branches call and control access. Branches expect appointments before approval arrives. Equipment moves between similar-named locations. Several apparently separate failures turned out to follow one central configuration change.”

**Typical symptom:** Head office pays and approves parts, but branches call and control access. Several apparently separate failures turned out to follow one central configuration change.
- passage `cases/C15#004`: ### C15-Q01: Who approves expenditure and access?

**Example answer in this fictional case:** Head office approves cost; the branch agrees access.

**Why ask:** These are separate permissions.

**If the answer differs:** Similar symptoms across branches may be independent hardware faults; common timing is a hypothesis, not proof.
- passage `cases/C10#004`: ### C10-Q01: Who may approve additional cost?

**Example answer in this fictional case:** Head office, not the branch contact.

**Why ask:** Separate site access from spending authority.

**If the answer differs:** If detailed instructions were acknowledged and repeatedly ignored, partner performance management may be needed beyond software.
- passage `cases/C15#002`: ## Current workflow

1. Branch reports
2. Site and asset identified
3. Diagnosis
4. Head-office approval sought
5. Branch appointment arranged
6. Work reported centrally and locally

## 6. S16
**Question:** Our medical-office customers need fast support, but we cannot interrupt their work whenever we like.

**Answer:** The passages don't give a direct answer for your business, but the closest analogue is case C16, a synthetic clinic-support case. Its approach is to respect operating windows rather than interrupt work whenever a problem appears.

- **Interruptions need authorization.** The C16 workflow has a step to "Seek authorization" before diagnosis begins [5]. In that fictional case, the practice manager coordinates acceptable downtime [4]. That is an example from one invented business, so you would need to confirm who approves interruptions in your customers' offices.
- **Diagnosis happens inside an agreed window.** The workflow is: report the disruption, determine the affected service, seek authorization, attempt diagnosis within the window, then escalate to a vendor or schedule the work, and confirm restoration [5].
- **Urgency is real but timing is constrained.** Reception problems are urgent when patients are waiting, but staff cannot restart systems whenever they like [2].
- **Intermittent faults need good notes.** One intermittent problem disappeared during a short visit and came back the next morning, so the case stresses useful notes without patient details [2].
- **Remote attempts can waste time.** In a different case (C08), attempted remote support wasted about 25 minutes before a visit, and customers repeated symptoms to several staff [3]. A single intake record could reduce that repetition, though the passages don't show that solution in detail.

To apply this to your business, I'd need to know who authorizes downtime for your customers, what hours they can accept interruptions, and which systems are clinical or vendor-managed. I can record those as facts if you share them.

- passage `cases/C16#000`: # C16: Clinic support must respect operational windows

> Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.
- passage `cases/C16#001`: ## Business and opening narrative

Seven staff supporting clinic office IT, printers, networks and backups; clinical devices excluded.

“Reception problems are urgent when patients are waiting, but we cannot restart systems whenever we like. Vendors handle clinical software and devices. An intermittent problem disappeared during a short visit and returned next morning. We need useful notes without patient details.”

**Typical symptom:** Reception problems are urgent when patients are waiting, but we cannot restart systems whenever we like. We need useful notes without patient details.
- passage `cases/C08#001`: ## Business and opening narrative

12 staff supporting approximately 75 small businesses.

“We visit for simple settings problems, but attempted remote support can also waste 25 minutes before a visit. The remote tool may be absent, the internet down or the caller unauthorized. Customers repeat symptoms to several staff members.”

**Typical symptom:** We visit for simple settings problems, but attempted remote support can also waste 25 minutes before a visit. Customers repeat symptoms to several staff members.
- passage `cases/C16#005`: ### C16-Q02: Who authorizes interruption?

**Example answer in this fictional case:** The practice manager coordinates acceptable downtime.

**Why ask:** Work timing is an approval constraint.
- passage `cases/C16#002`: ## Current workflow

1. Clinic reports disruption
2. Determine affected service
3. Seek authorization
4. Attempt diagnosis within window
5. Escalate vendor or schedule work
6. Confirm restoration

## 7. S17
**Question:** Everyone says the fault belongs to another supplier, and we become the messenger.

**Answer:** The passages don't directly answer this, but two analogous cases describe the same pattern.

- **Case C17 (a ten-person Wi-Fi and IT provider)** describes a similar situation. The internet provider wants wired tests and the application vendor wants logs, and the notes rarely record where or when tests occurred, so second technicians repeat them. Waiting for the vendor can last indefinitely [2]. The case's diagnosis says the evidence lacks reproducible context and escalations lose accountable ownership [5].
- **Case C10 (a partner-based service provider)** shows a related gap. Partners return reports of varying detail, and one complaint confused assignment time with an agreed arrival time [1].

Taken together, the pattern in these cases is that when a fault is passed between parties, the record of what was tested, where, and when goes missing, and no one owns the escalation. The passages suggest that tracking reproducible context and a named owner for each escalation are what the cases point to. They don't give a step-by-step fix, and they describe other businesses, so they don't confirm what would work for yours.

If you share your own details (who you escalate to, how faults are recorded, and where the delays occur), I can record them and draft a diagnosis for your business.

- passage `cases/C10#001`: ## Business and opening narrative

Eight internal staff plus regional external service partners.

“We send partners addresses and symptoms by message. Some return detailed reports; others only say done. One replaced a part with branch permission, but head office refused to pay. Assignment time was mistaken for an agreed arrival time during another complaint.”

**Typical symptom:** We send partners addresses and symptoms by message. Assignment time was mistaken for an agreed arrival time during another complaint.
- passage `cases/C17#001`: ## Business and opening narrative

Ten-person office network, Wi-Fi and general IT service provider.

“The internet provider wants wired tests; the application vendor wants logs. Our notes rarely say where or when tests occurred. Second technicians repeat them. An access point replacement did not fix a meeting-room problem that returned during busy events. Waiting for vendor can last indefinitely.”

**Typical symptom:** The internet provider wants wired tests; the application vendor wants logs. Waiting for vendor can last indefinitely.
- passage `cases/C07#001`: ## Business and opening narrative

Nine-person business PC and laptop repair provider.

“Technicians identify a part, office staff ask suppliers, and customers approve quotes. The gaps between those steps last days. An approval sent to a technician never reached purchasing. Shelves and spreadsheets disagree, and warranty return dates get missed.”

**Typical symptom:** Technicians identify a part, office staff ask suppliers, and customers approve quotes. Shelves and spreadsheets disagree, and warranty return dates get missed.
- passage `cases/C15#001`: ## Business and opening narrative

Maintenance provider for multi-site retail and education groups; one customer has 28 branches.

“Head office pays and approves parts, but branches call and control access. Branches expect appointments before approval arrives. Equipment moves between similar-named locations. Several apparently separate failures turned out to follow one central configuration change.”

**Typical symptom:** Head office pays and approves parts, but branches call and control access. Several apparently separate failures turned out to follow one central configuration change.
- passage `cases/C17#009`: ## Diagnosis

**Supported in this case:** Evidence lacks reproducible context and escalations lose accountable ownership.

## 8. S18
**Question:** Our warehouse, our vans, and our customer sites behave like three separate companies.

**Answer:** Your description matches the pattern in the passages, though the passages only describe it. They don't tell me how your business actually works.

The closest analogue is case C18, a 24-person business with 16 field technicians, a central warehouse, and customer-held loan equipment. Its owner said that "purchases, warehouse counts and van notes never agree," and that technicians bought parts another technician already had [2]. The case is labelled as a synthetic teaching example, so its details don't apply to you. Ask your owner rather than assume the same answers [4].

Two other cases show related symptoms:
- C04 (printer rental, about 650 devices): stock "says five cartridges, but some are in vans, reserved or already delivered" [3].
- C07 (nine-person PC repair): "shelves and spreadsheets disagree," and an approval never reached purchasing [5].

Across these cases, the warehouse, vans, and customer sites each keep their own record, and nothing links a part's movement from one to another. That is why the counts never reconcile.

To test whether this applies to you, I'd need specifics, such as how many staff work in operations, how stock is tracked and where, how many stock lookups or stockouts happen each month, and how often a van or customer site holds parts the system doesn't show. I have not recorded any figures yet, because you haven't given me any. If you share these, I can record them and draft a diagnosis for the stock area.

- passage `cases/C15#001`: ## Business and opening narrative

Maintenance provider for multi-site retail and education groups; one customer has 28 branches.

“Head office pays and approves parts, but branches call and control access. Branches expect appointments before approval arrives. Equipment moves between similar-named locations. Several apparently separate failures turned out to follow one central configuration change.”

**Typical symptom:** Head office pays and approves parts, but branches call and control access. Several apparently separate failures turned out to follow one central configuration change.
- passage `cases/C18#001`: ## Business and opening narrative

24 staff; 16 field technicians, central warehouse and customer-held loan equipment.

“Purchases, warehouse counts and van notes never agree. We buy parts that another technician already has. Faulty items return without job references, losing warranty credits. Cheap cables should not require the same administration as expensive serialized components.”

**Typical symptom:** Purchases, warehouse counts and van notes never agree. Cheap cables should not require the same administration as expensive serialized components.
- passage `cases/C04#001`: ## Business and opening narrative

Printer rental and consumables provider; approximately 650 managed devices.

“The spreadsheet says five cartridges, but some are in vans, reserved or already delivered. Customers identify a printer by its location and sometimes photograph the wrong one. Leaving spare toner helped some sites but caused others to stockpile it.”

**Typical symptom:** The spreadsheet says five cartridges, but some are in vans, reserved or already delivered. Leaving spare toner helped some sites but caused others to stockpile it.
- passage `cases/C18#000`: # C18: Warehouse, van and customer stock diverge

> Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.
- passage `cases/C07#001`: ## Business and opening narrative

Nine-person business PC and laptop repair provider.

“Technicians identify a part, office staff ask suppliers, and customers approve quotes. The gaps between those steps last days. An approval sent to a technician never reached purchasing. Shelves and spreadsheets disagree, and warranty return dates get missed.”

**Typical symptom:** Technicians identify a part, office staff ask suppliers, and customers approve quotes. Shelves and spreadsheets disagree, and warranty return dates get missed.

## 9. S19
**Question:** We already bought service software. The staff still run the business through chat.

**Answer:** The passages suggest this is a common pattern, but they describe other businesses, so they don't tell us what is happening in yours.

In the C19 case, a 19-person business introduced service management software eight months earlier, yet the office still ran work through chat. The office opened a ticket, then duplicated the assignment in chat. Technicians sent updates by chat, the office rekeyed them, and managers still asked for spreadsheet totals because the dashboard was incomplete [1][5]. The case calls this "service software increases duplicate work" [4].

The C01 case, a 14-person business, shows a related failure. Requests were recorded selectively, and others were lost because everyone assumed someone else had accepted them. Two technicians once attended the same printer because customers described the problem differently. The case also notes that a mandatory customer portal would not solve this alone [2][3].

The passages are synthetic teaching cases, and their examples belong only to those fictional businesses. Your situation needs to be checked with you directly [4].

To assess your case, I need to know how work currently moves through your business. For example: how requests arrive, who assigns them, how technicians report back, and what the software is supposed to record. I can then record those facts and draft a diagnosis.

- passage `cases/C19#001`: ## Business and opening narrative

19 staff; service management software introduced eight months ago.

“The office creates tickets then messages technicians because chat gets noticed. Updates return by chat and are copied back. Long mobile forms and poor connectivity push reporting into the evening. Management asks for separate spreadsheet totals because the dashboard is incomplete.”

**Typical symptom:** The office creates tickets then messages technicians because chat gets noticed. Management asks for separate spreadsheet totals because the dashboard is incomplete.
- passage `cases/C01#001`: ## Business and opening narrative

14 staff; nine field technicians; approximately 90 office and school customers; monthly maintenance with some parts extra.

“Teachers contact our office, their usual technician, or me. Our office uses spreadsheet and group chat. Two technicians attended the same printer after different teachers described the problem differently. Other requests disappear because everybody assumes somebody else accepted them. Customers will keep calling, so a mandatory customer portal will not solve this alone.”

**Typical symptom:** Teachers contact our office, their usual technician, or me. Customers will keep calling, so a mandatory customer portal will not solve this alone.
- passage `cases/C01#002`: ## Current workflow

1. Customer reports by phone or message
2. Recipient records selectively
3. Coordinator assigns in chat
4. Technician travels
5. Repair reported informally
- passage `cases/C19#000`: # C19: Service software increases duplicate work

> Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.
- passage `cases/C19#002`: ## Current workflow

1. Office opens ticket
2. Office duplicates assignment in chat
3. Technician works
4. Update sent in chat
5. Office rekeys
6. Manager asks for spreadsheet

## 10. S20
**Question:** The business works because I personally remember everything, and I cannot keep doing that.

**Answer:** The passages don't include a question, so I can't tell what you want done with them. Here is what they say, with citations.

**Case C20 (fictional teaching case, per passage 2):** A six-person business with an owner, four technicians and an administrator, plus plans to hire two more technicians. The owner coordinates through messages and memory. When they were away for three days, a customer was revisited before a part arrived, and invoices stopped because nobody knew what the owner had promised [1]. The diagnosis is that commitments, dependencies and delegated authority are tied to one person rather than recorded in a shared workflow [5]. Example questions ask which commitments exist only in the owner's head, such as call-before-visit rules, parts approvals and invoice holds [4].

**Case C12 (also a teaching case):** A 13-staff business where two long-serving technicians hold most customer-specific knowledge. Juniors call seniors while both are on jobs, manuals and notes are scattered, and a recurring printer configuration keeps being rediscovered. End-of-day notes just say "fixed," and seniors worry that procedures are applied without their exceptions [3].

**Points to note:**
- Passage 2 says the example answers belong to the fictional case and should not be assumed to apply to your business [2]. Passage 4 adds that some escalations need the owner's commercial judgement, so full delegation may not be the goal [4].
- Neither case gives numbers for your business, so I can't estimate hours saved from these passages alone.

What would you like to do? For example, I could:
1. Record facts about your own business (for instance, how many staff, how many requests per week, or where information is kept). I'd only record what you tell me.
2. Draft a diagnosis for one of the service areas (request dispatch, consumables stock, usage billing prep, or operations overview) once enough facts are recorded.
3. Summarise either case in more detail.

- passage `cases/C20#001`: ## Business and opening narrative

Six staff: owner, four technicians and administrator; plans to hire two more technicians.

“I coordinate everything through messages and memory. When I took three days away, someone revisited a customer before the part arrived, and invoices stopped because nobody knew what I promised. We have spreadsheets and calendars, but I connect them in my head.”

**Typical symptom:** I coordinate everything through messages and memory. We have spreadsheets and calendars, but I connect them in my head.
- passage `cases/C20#000`: # C20: Owner memory is the operating system

> Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.
- passage `cases/C12#001`: ## Business and opening narrative

13 staff; two long-serving technicians carry most customer-specific knowledge.

“Juniors call seniors while both are on jobs. Manuals and old notes are scattered across folders and chat. A recurring school printer configuration is repeatedly rediscovered. End-of-day notes just say fixed, and seniors worry about procedures being applied without their exceptions.”

**Typical symptom:** Juniors call seniors while both are on jobs. End-of-day notes just say fixed, and seniors worry about procedures being applied without their exceptions.
- passage `cases/C20#004`: ### C20-Q01: Which commitments exist only in your head?

**Example answer in this fictional case:** Call-before-visit rules, parts approvals and invoice holds.

**Why ask:** Capture operational exceptions first.

**If the answer differs:** Some decisions legitimately require the owner’s commercial judgement; do not automate every escalation or assume full delegation is desired.
- passage `cases/C20#009`: ## Diagnosis

**Supported in this case:** Commitments, dependencies and delegated authority are person-bound rather than recorded in a shared workflow.
