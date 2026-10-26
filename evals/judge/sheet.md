# Judge labelling sheet (30 items)

For each item, read the question, the answer and the passages. Then fill two labels in `labels.csv` (same id):
- **faithful**: 1 if every claim in the answer is supported by the passages, 0 if not.
- **relevant**: 1 if the answer addresses the question, 0 if not.

## 1. q001 (identifier)
**Question:** What does C01 say about merging requests that look alike?

**Answer:** C01 says never to merge requests just because they look alike. The rule is that you should never merge "solely on school name or textual similarity" [1: C01-R01]. Textual similarity alone is not enough.

Before merging, C01 suggests checking whether the visits are truly the same job. Ask whether both were for the same device and fault, using evidence such as a serial-number photo and visit notes [2: C01-Q01]. If both assignments were visible and intentionally needed different skills, merging would be wrong, so you should examine the assignment reasons first [2: C01-Q01].

If you do merge, C01 requires preserving the original reports and their reporters [1: C01-R02].

- passage `cases/C01#013`: ## Business rules  - C01-R01: Never merge solely on school name or textual similarity. - C01-R02: Preserve original reports and their reporters after a merge. - C01-R03: Commit assignments with an incident version check; a second worker requires an explicit reason. - C01-R04: Unknown asset identity 
- passage `cases/C01#004`: ### C01-Q01: Were both visits for the same device and fault?  **Example answer in this fictional case:** A serial-number photo and visit notes identify the same printer; both describe an offline queue.  **Why ask:** Distinguishes an unnecessary duplicate from legitimate parallel work.  **If the answ
- passage `cases/C05#013`: ## Business rules  - C05-R01: Negative deltas block ordinary billing unless an approved reset or replacement segment explains them. - C05-R02: Pool allowance is applied once per defined group and period. - C05-R03: OCR confidence never authorizes invoice sending. - C05-R04: Corrected readings retain
- passage `cases/C09#013`: ## Business rules  - C09-R01: Do not embed credentials in readiness documents. - C09-R02: A post-signoff configuration change triggers impact review. - C09-R03: A blocked project cannot be silently labeled ready to meet a date.
- passage `cases/C01#006`: ### C01-Q03: Who can accept a direct request?  **Example answer in this fictional case:** Technicians promise a visit without informing the coordinator.  **Why ask:** Reveals missing commitment ownership.

## 2. q003 (identifier)
**Question:** According to C04, how is available stock worked out?

**Answer:** According to C04, available stock equals the physical quantity minus valid reservations at that location (C04-R01) [2]. The case treats this as a stock calculation distinct from ownership: the "Why ask" note says available-to-promise differs from ownership, so reserved and van stock should not simply be counted as available warehouse stock [1].

This is a synthetic teaching case, so the rule describes that fictional business and may not apply to yours without checking.

- passage `cases/C04#005`: ### C04-Q02: What does stock count include?  **Example answer in this fictional case:** Reservations and van stock are mixed with warehouse stock.  **Why ask:** Available-to-promise differs from ownership.
- passage `cases/C04#013`: ## Business rules  - C04-R01: Available stock equals physical quantity minus valid reservations at that location. - C04-R02: An incompatible or uncertain SKU blocks picking. - C04-R03: A retry with the same movement ID cannot decrement twice. - C04-R04: Reorder proposals include lead time and confid
- passage `cases/C04#000`: # C04: Toner stock exists but cannot be found  > Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.
- passage `cases/C04#007`: ### C04-Q04: Are deliveries recorded immediately?  **Example answer in this fictional case:** Often at the end of the week.  **Why ask:** Stock freshness is a root issue.
- passage `cases/C04#008`: ## Evidence in the fictional case  - C04-E01: A simulated stock audit separates warehouse, reserved and van quantities. - C04-E02: A simulated delivery receipt is absent from the stock sheet. - C04-E03: A simulated customer check finds two unopened spares.

## 3. q005 (identifier)
**Question:** What does C06 say about coverage that is uncertain?

**Answer:** C06 says that uncertain coverage cannot silently become a billable authorization [1, C06-R01].

Related guidance from the same case:
- A customer match alone is not enough to establish coverage. Coverage may be organization-wide or asset-specific, depending on the agreement [2, C06-Q01].
- An asset missing from the list is not proof of exclusion. An unlisted device may be covered by a site-wide agreement, so it should never be classified as excluded only because the asset list is incomplete [2, C06-Q01].

- passage `cases/C06#013`: ## Business rules  - C06-R01: Uncertain coverage cannot silently become a billable authorization. - C06-R02: Approval binds to amount, scope and version. - C06-R03: A scope change invalidates an inadequate prior approval. - C06-R04: Goodwill is recorded separately from contractual inclusion.
- passage `cases/C06#004`: ### C06-Q01: Is coverage organization-wide or asset-specific?  **Example answer in this fictional case:** Both exist, depending on the agreement.  **Why ask:** A customer match alone is insufficient.  **If the answer differs:** An unlisted device may be covered by a site-wide agreement; never classi
- passage `cases/C06#000`: # C06: Contract coverage discovered after repair  > Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.
- passage `cases/C10#006`: ### C10-Q03: What evidence is mandatory?  **Example answer in this fictional case:** Requirements are not included consistently.  **Why ask:** Standardize instructions before measuring compliance.
- passage `cases/C06#007`: ### C06-Q04: Can goodwill exceptions be made?  **Example answer in this fictional case:** The owner allows small exceptions but records no reason.  **Why ask:** Formalize discretion without claiming coverage.

## 4. q007 (identifier)
**Question:** What does C08 require before remote control is started?

**Answer:** C08 requires **applicable authorization** before remote control is started. [1] Consent and access are prerequisites, and some customers require a named on-site contact to authorize a session. [3]

The passages don't define what counts as applicable authorization for a specific customer, so you would need to confirm that with the service owner.

Related rules:
- Disconnected or obvious physical faults may skip remote support. [1]
- The time-box for remote attempts is set with the service owner, not by the model. [1][2]

These cases are synthetic, so the example answers may not apply to your business. [5]

- passage `cases/C08#013`: ## Business rules  - C08-R01: Do not initiate control without applicable authorization. - C08-R02: Disconnected or obvious physical faults may bypass remote support. - C08-R03: Time-box is configured with the service owner, not invented by the model.
- passage `cases/C08#006`: ### C08-Q03: Are remote attempts time-boxed?  **Example answer in this fictional case:** No; technicians keep troubleshooting connection setup.  **Why ask:** Avoid an unbounded extra stage.
- passage `cases/C08#005`: ### C08-Q02: Who may authorize a session?  **Example answer in this fictional case:** Some customers require a named on-site contact.  **Why ask:** Consent and access are prerequisites.
- passage `cases/C08#007`: ### C08-Q04: Do dispatch notes contain remote findings?  **Example answer in this fictional case:** They usually say remote failed.  **Why ask:** Negative results must transfer.
- passage `cases/C08#000`: # C08: Remote-first support creates another delay  > Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.

## 5. q009 (identifier)
**Question:** What does C16 say about patient records in routine IT triage?

**Answer:** C16 says not to collect patient records for routine IT triage (C16-R01, passage [1]).

Related points from the same case:
- The example answer to the evidence question is that time, workstation and error code help, and patient screenshots are unnecessary. The stated reason is to minimize sensitive collection (passage [4]).
- If a patient-bearing screenshot does arrive, the acceptance test is that it is flagged for controlled handling and not indexed (C16-AT01, passage [3]).

The case is a synthetic teaching case, and its example answers apply only to that fictional business. Passage [5] says to ask the owner rather than assume they apply to a real one.

- passage `cases/C16#013`: ## Business rules  - C16-R01: Do not collect patient records for routine IT triage. - C16-R02: Disruptive changes require current scope-specific approval. - C16-R03: Not reproduced remains distinct from confirmed resolution. - C16-R04: Clinical advice and clinical-device procedures stay outside this
- passage `cases/C16#004`: ### C16-Q01: Which service is in our scope?  **Example answer in this fictional case:** Reception PCs and network, not clinical equipment.  **Why ask:** Avoid unsupported responsibility.  **If the answer differs:** A vendor outage or clinical-device failure needs routing to the responsible supplier,
- passage `cases/C16#014`: ## Acceptance tests  - C16-AT01: A patient-bearing screenshot is flagged for controlled handling, not indexed. - C16-AT02: No restart is scheduled outside the approved window. - C16-AT03: A recurring symptom reopens investigation with prior evidence.
- passage `cases/C16#006`: ### C16-Q03: What evidence reproduces the fault?  **Example answer in this fictional case:** Time, workstation and error code help; patient screenshots are unnecessary.  **Why ask:** Minimize sensitive collection.
- passage `cases/C16#000`: # C16: Clinic support must respect operational windows  > Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.

## 6. q011 (paraphrase)
**Question:** How do we stop two engineers turning up for one broken machine?

**Answer:** The request and dispatch area prevents double dispatch in two ways. It uses one queue for every service request, whichever channel it came from, and each request shows who accepted it. It also flags likely duplicates so two technicians are not sent to the same fault [5]. The dispatcher still reviews each flag and makes the final decision [5].

The passages do not say how duplicates are detected or how accurate the flagging is.

- passage `cases/C10#011`: ## Interventions  **Process first:** Send a concise work order with scope, escalation contact and evidence requirements; separate technical completion from customer acceptance.  **Automation and bounded AI help:** Provide authenticated, job-scoped mobile reporting; record acceptance, agreed window, 
- passage `cases/C15#001`: ## Business and opening narrative  Maintenance provider for multi-site retail and education groups; one customer has 28 branches.  “Head office pays and approves parts, but branches call and control access. Branches expect appointments before approval arrives. Equipment moves between similar-named l
- passage `cases/C15#002`: ## Current workflow  1. Branch reports 2. Site and asset identified 3. Diagnosis 4. Head-office approval sought 5. Branch appointment arranged 6. Work reported centrally and locally
- passage `cases/C07#011`: ## Interventions  **Process first:** Assign one repair owner; require exact part verification before purchase; separate waiting for information, approval, supplier and customer.  **Automation and bounded AI help:** Track dependency states, deadline reminders and linked loan/return obligations; prepa
- passage `solutions/request-dispatch#001`: ## What it does  The request and dispatch area gives the business one queue for every service request, whichever channel it came from. Each request shows who accepted it, and likely duplicates are flagged so two technicians are not sent to the same fault. When the day changes, it suggests schedule r

## 7. q013 (paraphrase)
**Question:** Does the rescheduling advice consider when a customer's building can be entered?

**Answer:** Yes. The case pattern treats the access window as a constraint on rescheduling.

- **Access constraints come first:** "Access and skill constraints take precedence over distance." [1]
- **Access window is collected before replanning:** The process step is to "Collect impact, access window and required skills before replanning." [4]
- **Access-window errors are a tested failure mode:** The minimum evidence includes "A simulated route log shows an avoidable arrival outside the access window." [5]

These passages come from a fictional case (C02). They describe the pattern's intended design, not a verified result for your business.

- passage `cases/C02#013`: ## Business rules  - C02-R01: Access and skill constraints take precedence over distance. - C02-R02: Dispatcher confirms any displaced appointment. - C02-R03: Unacknowledged changes escalate; do not assume delivery equals acceptance. - C02-R04: Retain original promised time separately from revised e
- passage `cases/C02#006`: ### C02-Q03: Are skills and parts considered?  **Example answer in this fictional case:** The dispatcher remembers skills but cannot see van stock.  **Why ask:** A distance-only optimizer is insufficient.
- passage `cases/C02#007`: ### C02-Q04: Do technicians acknowledge revised schedules?  **Example answer in this fictional case:** A message can arrive while driving and go unread.  **Why ask:** Schedule publication is not acceptance.
- passage `cases/C02#011`: ## Interventions  **Process first:** Collect impact, access window and required skills before replanning; freeze a near-term travel window unless the dispatcher explicitly overrides it.  **Automation and bounded AI help:** Rank feasible assignments; display travel, skills, stock and access tradeoffs
- passage `cases/C02#010`: ## Minimum evidence before reusing this pattern  - A simulated route log shows an avoidable arrival outside the access window. - A simulated assignment review finds the required part in a different van. - Simulated call notes record urgency without impact.

## 8. q015 (paraphrase)
**Question:** Will it buy more supplies when we run low?

**Answer:** No. The consumables and stock solution does not place purchase orders automatically, and it does not negotiate with suppliers [1].

It can suggest restocking, though. One case recommends suggesting replenishment for human approval until the stock counts are reliable [3]. Someone would still need to review and approve any reorder.

- passage `solutions/consumables-stock#003`: ## What it does not do  It does not place purchase orders automatically. It does not negotiate with suppliers.
- passage `solutions/consumables-stock#000`: # Consumables and stock management
- passage `cases/C04#011`: ## Interventions  **Process first:** Count high-use stock; assign device IDs; log transfers at handover; ask about usable on-site spare stock before urgent delivery.  **Automation and bounded AI help:** Maintain a location ledger and compatibility table; reserve stock atomically; suggest replenishme
- passage `cases/C04#002`: ## Current workflow  1. Customer reports toner warning 2. Office identifies device 3. Spreadsheet checked 4. Cartridge picked 5. Delivery made 6. Stock updated later
- passage `solutions/consumables-stock#001`: ## What it does  The consumables and stock area shows where each consumable, part and loan device is: the store, a vehicle or a customer site. Anyone can see, before a visit, whether the item is already on hand and which devices it fits. Items that need serial or warranty tracking are kept apart fro

## 9. q017 (paraphrase)
**Question:** Does it bill customers on its own once the numbers are ready?

**Answer:** No. The usage and billing preparation area does not send invoices without review [2]. It turns readings into figures that are ready to check, and it holds readings that do not fit in an exception queue for a person to decide [4][3]. It also does not set customer prices or give legal advice on contract terms [2].

The case workflow lists "Send billing data" as the final step after a person reviews exceptions [5]. That passage does not say whether sending is automatic, so I can't confirm more than the review requirement above.

- passage `solutions/usage-billing-prep#000`: # Usage and billing preparation
- passage `solutions/usage-billing-prep#003`: ## What it does not do  It does not send invoices without review. It does not set customer prices or give legal advice on contract terms.
- passage `solutions/usage-billing-prep#002`: ## What is included  - Reading capture with a reference to the photo or source note. - Counter-order checks: a reading must not be lower than the one before, unless a replacement was recorded. - Usage calculation for each agreement, including colour and monochrome allowances. - An exception queue fo
- passage `solutions/usage-billing-prep#001`: ## What it does  The usage and billing area turns meter and usage readings into figures that are ready to check. Each reading is matched to the right device and agreement, checked against the device's history, and held in an exception queue when it does not fit. Before work starts, it also shows whe
- passage `cases/C05#002`: ## Current workflow  1. Collect reading 2. Match machine 3. Enter counters 4. Apply contract terms 5. Review exceptions 6. Send billing data

## 10. q019 (paraphrase)
**Question:** Can the board work out what is wrong with a broken machine?

**Answer:** The passages don't answer this question. Each of the five (C09, C11, C12, C16, C19) contains only the heading "Diagnostic questions" and no text, so I can't tell what the board can or can't diagnose, or whether these cases involve a machine at all.

If you share the case content, or describe the machine and the symptoms, I can work from that. I can also search the knowledge base for other cases or consultation notes on machine faults.

- passage `cases/C09#003`: ## Diagnostic questions
- passage `cases/C11#003`: ## Diagnostic questions
- passage `cases/C12#003`: ## Diagnostic questions
- passage `cases/C16#003`: ## Diagnostic questions
- passage `cases/C19#003`: ## Diagnostic questions

## 11. q021 (paraphrase)
**Question:** How wide is the band around the estimate when I have not supplied my own bounds?

**Answer:** When you haven't given your own bounds, the band runs from 0.8 times the central value to 1.2 times it, so it is about 20% either side of the estimate [1].

- passage `consultation/effect-estimate#003`: ## How the range is shown  The answer gives a central value and a range. The low end is 0.8 times the central value and the high end is 1.2 times it, unless the owner gave a range. The answer names which input moves the result most.
- passage `consultation/effect-estimate#000`: # How the effect of an automation is estimated
- passage `consultation/effect-estimate#005`: ## Limits  Time saved is not the same as money saved, and it does not show that staff can be reduced. The estimate measures time on a task. It does not measure quality or customer outcomes.
- passage `consultation/effect-estimate#002`: ## Where each input comes from  Each input has a unit, a period and a source. A value the owner gave is marked as reported. A value the bot assumed is marked as assumed, and the answer says so. A value that is not known stays empty; it is never counted as zero.
- passage `solutions/usage-billing-prep#004`: ## Effect inputs  The estimate uses readings per month and the minutes it takes to check and enter one reading today. The new figure assumes the checks run automatically and only exceptions need a person. The answer then names how many readings currently need a correction after billing.

## 12. q023 (paraphrase)
**Question:** If three tasks happen in the same minutes, are the savings tripled?

**Answer:** No. Stages that overlap are measured once. For example, intake, ticket creation and transcription done in the same minutes are not counted as three separate savings [1].

- passage `consultation/effect-estimate#004`: ## What is not added together  Stages that overlap are measured once. Intake, ticket creation and transcription done in the same minutes are not counted as three savings.
- passage `consultation/effect-estimate#005`: ## Limits  Time saved is not the same as money saved, and it does not show that staff can be reduced. The estimate measures time on a task. It does not measure quality or customer outcomes.
- passage `consultation/effect-estimate#001`: ## The formula  The net time saved per period is the number of events multiplied by the minutes saved per event, divided by 60, minus the extra review time and the upkeep time:  net hours per period = events × (baseline minutes − new minutes) ÷ 60 − extra review hours − maintenance hours
- passage `solutions/usage-billing-prep#004`: ## Effect inputs  The estimate uses readings per month and the minutes it takes to check and enter one reading today. The new figure assumes the checks run automatically and only exceptions need a person. The answer then names how many readings currently need a correction after billing.
- passage `consultation/effect-estimate#000`: # How the effect of an automation is estimated

## 13. q025 (paraphrase)
**Question:** What does the bot do when I cannot answer something?

**Answer:** The passages say I mark the unknown explicitly instead of guessing or filling it in with a figure from a fictional case [2]. An unknown then becomes either an open question in the summary or a condition attached to a proposal, such as "if the service software offers an API" [2].

I also don't keep questioning you about a topic just to fill every field. Once there is enough evidence for a bounded proposal, I stop and keep the remaining unknowns visible [1]. Questions about contract interpretation, conflicting approval authority, or irreversible actions are passed to the responsible person rather than decided in our conversation [1].

- passage `consultation/interview-approach#006`: ## When to stop  The assistant stops asking about a topic once there is enough evidence for a bounded proposal, and keeps the remaining unknowns visible. It does not prolong the interview to fill every field. Contract interpretation, conflicting approval authority and irreversible actions are passed
- passage `consultation/interview-approach#005`: ## Mark unknowns  Some answers will not be known, and that is fine. The assistant marks unknowns explicitly instead of filling them with a guess or a figure from a synthetic case. An unknown becomes an open question in the summary, or a condition attached to a proposal, for example "if the service s
- passage `cases/C01#007`: ### C01-Q04: Can staff record an incomplete request?  **Example answer in this fictional case:** The current sheet expects a device model, which callers often do not know.  **Why ask:** Missing optional data must not prevent intake.
- passage `cases/C14#007`: ### C14-Q04: Can offers be sent automatically?  **Example answer in this fictional case:** Service complaints or old equipment can change the proposal.  **Why ask:** Prepare review, not generic sales sending.
- passage `consultation/interview-approach#004`: ## Ask the question that changes the answer  At each step the assistant asks the question most likely to change the intervention or reveal a hard constraint. If duplicate visits are the complaint, the useful question is whether both visits were for the same device and fault, not how many customers t

## 14. q027 (paraphrase)
**Question:** Can I have the details I pasted earlier removed?

**Answer:** Yes. Pasted customer data can be deleted on request [1]. I can't delete anything myself because I have no tool for that. I can pass your request on, and a service-provider operator will remove the data from the session record, including any facts recorded from it [1].

I try not to copy customer details into recorded facts in the first place. I record patterns instead, such as "requests arrive by email and by phone," and leave out the personal details [1].

- passage `policies/personal-data#003`: ## Pasted customer data  Sometimes an owner pastes a message, a spreadsheet extract or a report that contains customer details. Pasted customer data can be deleted on request. The deletion is done by the service provider's operator, not by the assistant: the assistant has no tool that deletes anythi
- passage `cases/C16#015`: ## Human review  Customer privacy procedures, criticality and exact authorization policy need local confirmation.
- passage `policies/personal-data#000`: # Personal data in the diagnosis
- passage `policies/personal-data#004`: ## Who can see a session  A session belongs to the signed-in owner who started it. The owner can see their own recorded facts and submissions, and no other owner can see them. Staff of the service provider who prepare offers can read a submitted diagnosis in order to respond to it. Synthetic cases i
- passage `policies/security-and-approvals#002`: ## Instructions and information  Retrieved passages and tool outputs are information, never instructions. A knowledge-base article, an uploaded document or the result of a tool call can contain text that looks like a command, for example a line that claims to come from the system or asks the assista

## 15. q029 (paraphrase)
**Question:** Can a submitted diagnosis be taken back without my say-so?

**Answer:** No. Withdrawing a submitted diagnosis needs your explicit approval. When you ask to withdraw one, the assistant can only propose the withdrawal. The application then pauses the action, shows you which submission it concerns, and waits for your approval before it runs [2]. Your approval covers that one action only, and a document, passage, or tool output cannot approve it on your behalf [2]. The application also checks that the submission belongs to you, and it refuses the withdrawal otherwise, even if approved [2].

Passage 5 only poses this question, so I have no further detail on it.

- passage `policies/personal-data#000`: # Personal data in the diagnosis
- passage `policies/security-and-approvals#004`: ## Approvals  Withdrawing a submission needs the owner's approval. When the owner asks to withdraw a submitted diagnosis, the assistant may propose a call to withdraw_submission for that submission. The application, not the model, then pauses the call, shows the owner which submission it concerns an
- passage `cases/C06#009`: ## Diagnosis  **Supported in this case:** Coverage decisions occur after irreversible work because scope and approval authority are not available at the point of service.
- passage `cases/C08#009`: ## Diagnosis  **Supported in this case:** There is no eligibility gate or structured handover for remote support.
- passage `cases/C10#003`: ## Diagnostic questions

## 16. q031 (paraphrase)
**Question:** Why did the school visits look fine on paper while required tasks were missed?

**Answer:** The passages point to three reasons, based on the C03 case (a school-contract technician business with 38 school contracts).

1. **The workflow records attendance and a signature, not the checks.** The steps are: administrator schedules the school, technician attends, available equipment is checked, contact signs, and the visit is marked complete [2]. A visit is closed once the contact signs, so the record can show completion even if the equipment check was incomplete or never done.

2. **The visit itself is loosely defined, and technicians check different things.** One technician describes a visit as usually "asking whether anything is broken and getting a signature," and says different technicians check different things [3]. Without a common checklist, two visits can look the same on paper but cover different equipment.

3. **Attendance is not evidence that the tasks were done.** In an emergency visit, the technician fixed one printer but did not inspect the lab [1]. Scheduled maintenance can also be missed after an emergency call, and "a signed sheet can hide an inaccessible computer room" [3]. The passages say attendance cannot substitute for task evidence [1].

A related check from a different case, C02, asks whether access is confirmed before travel, because a school contact may not have been asked whether a room would be available [5]. The passages do not show whether this owner's visits have the same access problem. That case is only an analogy.

These passages describe the C03 case in general. They do not contain this owner's own visit records, so I cannot confirm which of these causes applies to your schools.

- passage `cases/C03#005`: ### C03-Q02: Did emergency work satisfy those checks?  **Example answer in this fictional case:** The technician fixed one printer but did not inspect the lab.  **Why ask:** Attendance cannot substitute for task evidence.
- passage `cases/C03#002`: ## Current workflow  1. Administrator schedules school 2. Technician attends 3. Available equipment checked 4. Contact signs 5. Visit marked complete
- passage `cases/C03#001`: ## Business and opening narrative  11 staff; 38 school contracts with regular visits and reactive support.  “A visit usually means asking whether anything is broken and getting a signature. Different technicians check different things. We sometimes return for scheduled maintenance days after an emer
- passage `cases/C09#004`: ### C09-Q01: Who signs off the deployment configuration?  **Example answer in this fictional case:** Sales and the school discussed it, but no version was approved.  **Why ask:** Rework originates before imaging.  **If the answer differs:** A late customer change after a documented sign-off is chang
- passage `cases/C02#005`: ### C02-Q02: Is access confirmed before travel?  **Example answer in this fictional case:** A school contact was not asked whether the room would be available.  **Why ask:** Identifies a feasibility constraint.

## 17. q033 (unanswerable)
**Question:** Does the diagnosis chatbot support voice calls in Korean?

**Answer:** The passages don't say whether the diagnosis chatbot supports voice calls in Korean.

Passage [1] says the diagnosis is a plain-language conversation, but it does not mention voice or any language other than plain language. Passage [2] covers remote support eligibility, and passages [3], [4] and [5] are section headings with no content. None of them mention Korean or voice calls.

- passage `consultation/interview-approach#001`: ## Conversation, not a form  The diagnosis is a conversation in plain language. The assistant does not present the owner with a long form, and it reuses answers the owner has already given instead of asking again. It opens with the business goal: what the owner wants to be different in six months.
- passage `cases/C08#009`: ## Diagnosis  **Supported in this case:** There is no eligibility gate or structured handover for remote support.
- passage `cases/C13#003`: ## Diagnostic questions
- passage `cases/C16#003`: ## Diagnostic questions
- passage `cases/C19#003`: ## Diagnostic questions

## 18. q035 (unanswerable)
**Question:** What uptime guarantee does the service give?

**Answer:** The passages don't state an uptime guarantee for this service. None of them gives an uptime percentage or a contractual availability commitment.

Passage [2] (cases/C16) defines a metric for a different case: unplanned service interruption minutes caused by maintenance, tracked for recurrence and time to supplier engagement. That is a measurement suggestion, not a guarantee. Passage [1] (cases/C17) says supplier support windows vary by agreement, and passage [5] (cases/C14) lists agreement fields such as `service_summary` and `version`, but neither gives the uptime terms. The actual figure would need to come from the customer's service agreement.

- passage `cases/C17#015`: ## Human review  Supplier support windows and permissible diagnostic data vary by agreement.
- passage `cases/C16#016`: ## How to measure  **Primary metric:** Unplanned service interruption minutes caused by maintenance; track recurrence and time to appropriate supplier engagement.
- passage `cases/C02#015`: ## Human review  Travel estimates, availability freshness and contractual response definitions require validation.
- passage `cases/C05#015`: ## Human review  Proration, taxes, minimum charges, resets and rounding rules must come from the customer’s approved terms.
- passage `cases/C14#012`: ## Data fields  `agreement_id`, `version`, `amendment_ref`, `effective_date`, `end_date`, `notice_deadline`, `account_owner`, `service_summary`, `equipment_condition`, `renewal_stage`

## 19. q037 (unanswerable)
**Question:** Is there a mobile app for technicians?

**Answer:** The passages don't say whether there is a technician mobile app.

The request-and-dispatch area description [5] covers one request queue, duplicate flagging, and schedule suggestions that the dispatcher approves. It doesn't mention a technician app.

Passage [2] is from a different case study (C10). It recommends "authenticated, job-scoped mobile reporting" for technicians, but it describes an intervention in that case, not a feature of this service.

- passage `cases/C02#012`: ## Data fields  `job_id`, `impact`, `workaround`, `access_window`, `skill_tags`, `required_parts`, `technician_id`, `acknowledged_version`, `travel_start`, `arrived_at`, `work_start`, `work_end`
- passage `cases/C10#011`: ## Interventions  **Process first:** Send a concise work order with scope, escalation contact and evidence requirements; separate technical completion from customer acceptance.  **Automation and bounded AI help:** Provide authenticated, job-scoped mobile reporting; record acceptance, agreed window, 
- passage `cases/C01#002`: ## Current workflow  1. Customer reports by phone or message 2. Recipient records selectively 3. Coordinator assigns in chat 4. Technician travels 5. Repair reported informally
- passage `cases/C03#002`: ## Current workflow  1. Administrator schedules school 2. Technician attends 3. Available equipment checked 4. Contact signs 5. Visit marked complete
- passage `solutions/request-dispatch#001`: ## What it does  The request and dispatch area gives the business one queue for every service request, whichever channel it came from. Each request shows who accepted it, and likely duplicates are flagged so two technicians are not sent to the same fault. When the day changes, it suggests schedule r

## 20. q039 (unanswerable)
**Question:** How many weeks does a typical pilot take to roll out?

**Answer:** The passages don't say how many weeks a typical pilot takes to roll out, so I can't give a number.

They do describe pilot practices. Passage [4] recommends running proposed rules in shadow mode, starting with one consenting customer group, and using comparable operating periods. Passages [1], [2], [3] and [5] describe process changes from fictional rollouts but give no timelines.

- passage `cases/C08#017`: ## Fictional rollout  **What happened in the fiction:** In this fictional case, MILO introduced the process change: Ask connectivity, authorization and symptom questions first; agree a limited remote attempt and a clear escalation point.
- passage `cases/C07#017`: ## Fictional rollout  **What happened in the fiction:** In this fictional case, MILO introduced the process change: Assign one repair owner; require exact part verification before purchase; separate waiting for information, approval, supplier and customer.
- passage `cases/C12#017`: ## Fictional rollout  **What happened in the fiction:** In this fictional case, MILO introduced the process change: Capture symptoms, environment, tests, result and exceptions; assign review owners and retirement dates.
- passage `consultation/method-notes#005`: quire a person. - Run the proposed rules in shadow mode; record disagreements and missed exceptions. - Start with one consenting customer group and the staff who own its handoffs; include a normal case and each listed exception. - The team adopted the proposed workflow for the pilot scope. - Use a s
- passage `cases/C02#017`: ## Fictional rollout  **What happened in the fiction:** In this fictional case, MILO introduced the process change: Collect impact, access window and required skills before replanning; freeze a near-term travel window unless the dispatcher explicitly overrides it.

## 21. S01 (owner story)
**Question:** The same printer problem reaches three people, and we send two technicians.

**Answer:** The passages suggest this is a duplicate-dispatch problem, but you should confirm it before merging anything.

In the closest analogous case, two technicians attended the same printer after different teachers described the problem differently [1]. Requests also disappeared because each person assumed someone else had accepted them [1]. That matches your situation, where one fault reaches three people and two technicians go out.

Before treating the second visit as a duplicate, check whether both visits were for the same device and fault. A serial-number photo and visit notes can confirm this [4]. If both assignments were visible and intentionally needed different skills, deduplicating them would be wrong, so look at the assignment reasons first [4].

The passages don't say how many of your requests are duplicates or how much time they cost. I haven't recorded any facts or estimated any effect, since you didn't give me your own figures.

Sources: [1], [4]

- passage `cases/C01#001`: ## Business and opening narrative  14 staff; nine field technicians; approximately 90 office and school customers; monthly maintenance with some parts extra.  “Teachers contact our office, their usual technician, or me. Our office uses spreadsheet and group chat. Two technicians attended the same pr
- passage `cases/C10#001`: ## Business and opening narrative  Eight internal staff plus regional external service partners.  “We send partners addresses and symptoms by message. Some return detailed reports; others only say done. One replaced a part with branch permission, but head office refused to pay. Assignment time was m
- passage `cases/C05#001`: ## Business and opening narrative  Managed print provider; approximately 420 devices with usage-based agreements.  “Our administrator collects meter photos, remote readings and technician notes. Contracts have different color and monochrome allowances; some pool machines. A replacement device’s open
- passage `cases/C01#004`: ### C01-Q01: Were both visits for the same device and fault?  **Example answer in this fictional case:** A serial-number photo and visit notes identify the same printer; both describe an offline queue.  **Why ask:** Distinguishes an unnecessary duplicate from legitimate parallel work.  **If the answ
- passage `cases/C15#001`: ## Business and opening narrative  Maintenance provider for multi-site retail and education groups; one customer has 28 branches.  “Head office pays and approves parts, but branches call and control access. Branches expect appointments before approval arrives. Equipment moves between similar-named l

## 22. S02 (owner story)
**Question:** Our daily schedule falls apart before the technicians reach their first appointment.

**Answer:** Your description matches a pattern in the passages, though they come from other businesses, so they don't confirm your cause.

In the closest case, a dispatcher planned the next day in a spreadsheet, and urgent morning calls broke the route. The nearest technician might lack the skill, part, or customer authorization, and one redirect sent someone to a site whose key holder was absent, so the urgent visit and the original slot were both lost [1]. The workflow shows the break point: urgent requests arrive after the route is planned, and then appointments change and technicians wait or work out of sequence [2].

The passages suggest two kinds of response:

- **Process first:** Before replanning, collect the impact, access window, and required skills. Freeze a near-term travel window unless the dispatcher explicitly overrides it [3].
- **Bounded automation:** Rank feasible assignments, show the travel, skill, stock, and access tradeoffs, and issue versioned schedule changes that require acknowledgement [3]. A request-dispatch area would give one queue for all channels, flag likely duplicates, and suggest schedule revisions that respect access windows and skills, with the dispatcher making the final decision [5].

I haven't recorded any facts about your business, so I can't tell which of these applies to you. To assess your situation, I would need to know how many urgent requests arrive before the first appointment, how they reach the dispatcher, and how often a same-day change means a technician loses time or makes a wasted trip.

- passage `cases/C02#001`: ## Business and opening narrative  22 staff; 15 field technicians covering a city and surrounding towns.  “Our dispatcher plans tomorrow in a spreadsheet, but urgent morning calls dismantle the route. The nearest worker may lack the skill, part or customer authorization. We redirected someone to a s
- passage `cases/C02#002`: ## Current workflow  1. Dispatcher plans route 2. Urgent request arrives 3. Dispatcher calls technicians 4. Appointment changes 5. Technician waits or works 6. Times recorded inconsistently
- passage `cases/C02#011`: ## Interventions  **Process first:** Collect impact, access window and required skills before replanning; freeze a near-term travel window unless the dispatcher explicitly overrides it.  **Automation and bounded AI help:** Rank feasible assignments; display travel, skills, stock and access tradeoffs
- passage `cases/C01#001`: ## Business and opening narrative  14 staff; nine field technicians; approximately 90 office and school customers; monthly maintenance with some parts extra.  “Teachers contact our office, their usual technician, or me. Our office uses spreadsheet and group chat. Two technicians attended the same pr
- passage `solutions/request-dispatch#001`: ## What it does  The request and dispatch area gives the business one queue for every service request, whichever channel it came from. Each request shows who accepted it, and likely duplicates are flagged so two technicians are not sent to the same fault. When the day changes, it suggests schedule r

## 23. S03 (owner story)
**Question:** We promise a monthly visit, but nobody agrees on what that visit should accomplish.

**Answer:** The passages suggest the disagreement starts in the contracts themselves, and a shared checklist can fix the day-to-day inconsistency.

- **Check what each agreement says.** In one fictional school-contract case, "several agreements list checks; others only specify frequency," so obligations have to be interpreted per agreement [5].
- **Don't merge trips without agreement.** If an agreement requires a distinct scheduled attendance, combining it with another visit needs the customer's agreement, even when the checks overlap [5].
- **Standardise what the visit covers.** In that same case, the typical visit was "asking whether anything is broken and getting a signature," and different technicians checked different things [4]. A short on-site checklist aligned to the required evidence is the suggested fix [2].
- **Track completion separately from acceptance.** Record completed work and accepted work as separate items [2].
- **Measure the outcome.** The primary metric is visits completed within agreed windows divided by scheduled visits. Report travel minutes, waiting minutes and overdue backlog separately [1]. For repeat trips caused by missing approval or incorrect location, track those separately too [3].

The passages don't say how to reach agreement with a customer on what the monthly visit should accomplish. If you share the agreement wording and the checks you currently perform, I can help you map them against these points.

- passage `cases/C02#016`: ## How to measure  **Primary metric:** Visits completed within agreed windows / scheduled visits; separately report travel minutes, waiting minutes and overdue backlog.
- passage `cases/C13#011`: ## Interventions  **Process first:** Use a short on-site checklist aligned to required evidence; represent completed work and accepted work separately.  **Automation and bounded AI help:** Capture structured notes and evidence once; render reviewed customer templates; queue missing acceptance for fo
- passage `cases/C15#016`: ## How to measure  **Primary metric:** Repeat trips caused by missing approval or incorrect location / branch service visits.
- passage `cases/C03#001`: ## Business and opening narrative  11 staff; 38 school contracts with regular visits and reactive support.  “A visit usually means asking whether anything is broken and getting a signature. Different technicians check different things. We sometimes return for scheduled maintenance days after an emer
- passage `cases/C03#004`: ### C03-Q01: Does the contract require a visit or named checks?  **Example answer in this fictional case:** Several agreements list checks; others only specify frequency.  **Why ask:** Obligations must be interpreted per agreement.  **If the answer differs:** Where the agreement explicitly requires 

## 24. S04 (owner story)
**Question:** We have enough toner overall, but the right cartridge is never in the right place.

**Answer:** Your statement matches the symptom in the C04 teaching case: stock exists, but the spreadsheet does not show where it is. In that case, "the spreadsheet says five cartridges, but some are in vans, reserved or already delivered" [2]. The workflow also updates stock only after delivery, so the record lags behind the physical location [1].

The case suggests tracking this with three measures, not just stock levels: emergency toner trips per toner fulfilment, stock accuracy, and stockout days. Stockout days matter because overstocking can reduce trips while creating its own problem [4]. The case also notes that leaving spare toner at some sites helped, but at others it led to stockpiling [2].

The case's diagnostic question is whether the low-toner warning appears while a spare is already on site [5]. If physical counts are accurate but consumption outruns replenishment lead time, the main issue is reorder policy rather than data capture [5].

This is a fictional case, so its answers don't apply to your business without checking [3]. To find out which problem you have, I'd need to know:

1. When a low-toner warning comes in, is a spare cartridge often already at that site?
2. Is your stock count accurate when someone physically checks it?
3. How long does it take to replace a cartridge from the moment you reorder?
4. How many toner requests do you handle per week, and how many are emergencies?

I haven't recorded anything yet, because your statement doesn't give me specific values. If you share numbers for these, I can record them and run a diagnosis.

- passage `cases/C04#002`: ## Current workflow  1. Customer reports toner warning 2. Office identifies device 3. Spreadsheet checked 4. Cartridge picked 5. Delivery made 6. Stock updated later
- passage `cases/C04#001`: ## Business and opening narrative  Printer rental and consumables provider; approximately 650 managed devices.  “The spreadsheet says five cartridges, but some are in vans, reserved or already delivered. Customers identify a printer by its location and sometimes photograph the wrong one. Leaving spa
- passage `cases/C04#000`: # C04: Toner stock exists but cannot be found  > Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.
- passage `cases/C04#016`: ## How to measure  **Primary metric:** Emergency toner trips / toner fulfillments; also track stock accuracy and stockout days to avoid improving trips by overstocking.
- passage `cases/C04#004`: ### C04-Q01: Is the warning an empty cartridge?  **Example answer in this fictional case:** Some callers report the first low-toner warning while a spare is already on-site.  **Why ask:** Demand needs verification.  **If the answer differs:** If physical counts are accurate but consumption exceeds r

## 25. S05 (owner story)
**Question:** Every month, invoicing turns into a search for printer meter photographs.

**Answer:** The passages don't say how long the monthly invoicing search takes, so I can't size it. What they do show is a similar pattern and a possible fix.

- **Wrong photo, wrong machine:** In the C04 case, a printer rental provider with about 650 devices reports that customers identify a printer by location and sometimes photograph the wrong one [5]. That is the likely source of a meter-photo search, but the passage doesn't say it causes the monthly invoicing delay.
- **Analogous billing failure:** In the C05 case, a managed print provider with about 420 devices collects meter photos, remote readings and technician notes. A replacement device's opening reading was attached to the old machine, which produced a disputed bill [1]. Its workflow runs collect reading, match machine, enter counters, apply contract terms, review exceptions, send billing data [2].
- **Possible fix:** The usage-billing-prep solution includes reading capture linked to the photo or source note, a check that a reading is not lower than the previous one unless a replacement was recorded, and an exception queue for readings a person must decide [3].

Caveat: C04 and C05 are synthetic teaching cases, so their details may not apply to your business [4]. To estimate what this would save, I would need your numbers: how many devices or requests you handle, how many minutes you spend finding each photo, and how often a reading is disputed. I can record those if you share them.

- passage `cases/C05#001`: ## Business and opening narrative  Managed print provider; approximately 420 devices with usage-based agreements.  “Our administrator collects meter photos, remote readings and technician notes. Contracts have different color and monochrome allowances; some pool machines. A replacement device’s open
- passage `cases/C05#002`: ## Current workflow  1. Collect reading 2. Match machine 3. Enter counters 4. Apply contract terms 5. Review exceptions 6. Send billing data
- passage `solutions/usage-billing-prep#002`: ## What is included  - Reading capture with a reference to the photo or source note. - Counter-order checks: a reading must not be lower than the one before, unless a replacement was recorded. - Usage calculation for each agreement, including colour and monochrome allowances. - An exception queue fo
- passage `cases/C05#000`: # C05: Meter readings delay and corrupt invoices  > Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.
- passage `cases/C04#001`: ## Business and opening narrative  Printer rental and consumables provider; approximately 650 managed devices.  “The spreadsheet says five cartridges, but some are in vans, reserved or already delivered. Customers identify a printer by its location and sometimes photograph the wrong one. Leaving spa

## 26. S06 (owner story)
**Question:** We only discover whether equipment is covered after we have repaired it.

**Answer:** I recorded your statement as the incident story: coverage for equipment is only found out after the repair work is done.

The knowledge base has a similar synthetic case (C06) with the same pattern. It concludes that coverage decisions happen after irreversible work because scope and approval authority are not available at the point of service [2]. Suggested process fixes are to define covered, excluded and uncertain states, and to set up a pre-work approval path and documented goodwill authority. Automation could retrieve the effective agreement and asset scope, surface coverage evidence, and create approval requests when scope changes [3].

The case also says that before reusing this pattern, you would need evidence such as a device record showing ownership, a contract that excludes replacement parts, and a work report that contains no charge approval [4]. The case's example answer is that serial lists are incomplete, and it notes that unknown is different from excluded [5]. The passages are from a fictional teaching case, so they don't tell us how your business works. I haven't recorded anything about that yet.

To go further, I'd need your answers on how coverage is currently checked, whether technicians know when a device is not on the list, and what your approval process looks like. Once I have those, I can draft a diagnosis for the request or dispatch area.

- passage `cases/C06#000`: # C06: Contract coverage discovered after repair  > Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.
- passage `cases/C06#009`: ## Diagnosis  **Supported in this case:** Coverage decisions occur after irreversible work because scope and approval authority are not available at the point of service.
- passage `cases/C06#011`: ## Interventions  **Process first:** Define covered, excluded and uncertain states; provide a pre-work approval path and documented goodwill authority.  **Automation and bounded AI help:** Retrieve the effective agreement and asset scope; surface coverage evidence; create approval requests when scop
- passage `cases/C06#010`: ## Minimum evidence before reusing this pattern  - A simulated device record identifies personal ownership. - A simulated contract excludes replacement parts. - A simulated work report contains no charge approval.
- passage `cases/C06#006`: ### C06-Q03: Do technicians know a device is unlisted?  **Example answer in this fictional case:** Serial lists are incomplete.  **Why ask:** Unknown is different from excluded.

## 27. S07 (owner story)
**Question:** A ten-minute diagnosis turns into a two-week repair because nobody owns the parts follow-up.

**Answer:** The passages don't include a question, so I'm not sure what you want answered. Here is what they cover.

**Case C07 (synthetic teaching case):** Repairs stall between diagnosis and parts arrival. The example is a nine-person PC and laptop repair provider where technicians identify a part, office staff ask suppliers, and customers approve quotes. The gaps between those steps last days. An approval sent to a technician never reached purchasing, shelves and spreadsheets disagree, and warranty return dates get missed [4]. The current workflow has eight steps: diagnose, identify exact part, request supplier quote, seek customer approval, order, receive, repair, and return loaner and close [2].

**Suggested interventions in C07:**
- Process first: assign one repair owner, require exact part verification before purchase, and separate waiting for information, approval, supplier, and customer [1].
- Bounded automation and AI help: track dependency states, send deadline reminders, track linked loan and return obligations, and prepare customer updates from verified status [1].

**Related case C20:** A short diagnosis became a two-week repair because nobody owned the parts follow-up. The example answer is that nobody could see the pending part dependency, which points to missing next-action visibility rather than technician competence [5].

The passages say the example answers belong to these fictional businesses and that you should ask the owner rather than assume they apply to yours [3].

What would you like to do? For example, I could record facts about your own repair workflow, estimate the effect of automating one service area, or draft a diagnosis for request dispatch, consumables stock, usage billing prep, or operations overview. Any of these would need your own numbers and descriptions first.

- passage `cases/C07#011`: ## Interventions  **Process first:** Assign one repair owner; require exact part verification before purchase; separate waiting for information, approval, supplier and customer.  **Automation and bounded AI help:** Track dependency states, deadline reminders and linked loan/return obligations; prepa
- passage `cases/C07#002`: ## Current workflow  1. Diagnose 2. Identify exact part 3. Request supplier quote 4. Seek customer approval 5. Order 6. Receive 7. Repair 8. Return loaner and close
- passage `cases/C07#000`: # C07: Repairs stall between diagnosis and parts arrival  > Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.
- passage `cases/C07#001`: ## Business and opening narrative  Nine-person business PC and laptop repair provider.  “Technicians identify a part, office staff ask suppliers, and customers approve quotes. The gaps between those steps last days. An approval sent to a technician never reached purchasing. Shelves and spreadsheets 
- passage `cases/C20#006`: ### C20-Q03: Why did the premature visit happen?  **Example answer in this fictional case:** Nobody could see the pending part dependency.  **Why ask:** Missing next-action visibility, not technician competence.

## 28. S08 (owner story)
**Question:** We send technicians for problems we could solve remotely, but remote support can also waste time.

**Answer:** The passages don't include a question, so I haven't recorded any facts or run any tools. Here is what they cover:

- **Case C08 (remote support):** A fictional firm with 12 staff supporting about 75 small businesses. Technicians often visit for simple settings problems, and a failed remote attempt can waste 25 minutes before the visit. The remote tool may be missing, the internet may be down, or the caller may not be authorized. Customers also repeat their symptoms to several staff members. The current workflow is: call received, ask for a visit, optional remote attempt, connection fails or diagnosis proceeds, dispatch, customer repeats the story [2]. Before reusing this pattern, the case expects evidence of loss of internet before the remote attempt, an attended-access policy, and repeated checks missing from the ticket [3]. In C08-Q03, the example answer is that remote attempts are not time-boxed, so technicians keep troubleshooting connection setup [5]. [1][2][3][5]
- **Case C10 (interventions):** Process comes first. Send a concise work order with scope, escalation contact and evidence requirements, and separate technical completion from customer acceptance. Automation and bounded AI help should provide authenticated, job-scoped mobile reporting that records acceptance, agreed window, actual arrival, parts and approval requests [4].

What would you like to do next? For example, I could draft a diagnosis for one of your service areas (request dispatch, consumables stock, usage billing prep, or operations overview), or record facts about your own operations so I can estimate the effect of automating an area. If you share your business details, I'll record them only as you state them.

- passage `cases/C08#001`: ## Business and opening narrative  12 staff supporting approximately 75 small businesses.  “We visit for simple settings problems, but attempted remote support can also waste 25 minutes before a visit. The remote tool may be absent, the internet down or the caller unauthorized. Customers repeat symp
- passage `cases/C08#002`: ## Current workflow  1. Call received 2. Ask for visit 3. Optional remote attempt 4. Connection fails or diagnosis proceeds 5. Dispatch 6. Customer repeats story
- passage `cases/C08#010`: ## Minimum evidence before reusing this pattern  - A simulated call records loss of internet before the remote attempt. - A simulated customer policy requires attended access. - A simulated visit repeats checks absent from the ticket.
- passage `cases/C10#011`: ## Interventions  **Process first:** Send a concise work order with scope, escalation contact and evidence requirements; separate technical completion from customer acceptance.  **Automation and bounded AI help:** Provide authenticated, job-scoped mobile reporting; record acceptance, agreed window, 
- passage `cases/C08#006`: ### C08-Q03: Are remote attempts time-boxed?  **Example answer in this fictional case:** No; technicians keep troubleshooting connection setup.  **Why ask:** Avoid an unbounded extra stage.

## 29. S09 (owner story)
**Question:** School holidays are our busiest period, and we discover missing information on installation day.

**Answer:** Your situation matches a pattern in the knowledge base, but the passages don't tell me anything about your business specifically, so I can't say how big the problem is or what fix would work.

The closest analogue is a synthetic teaching case, C09, a school-maintenance and computer-room business. It shows the same sequence: a sales survey, then a quote, then equipment purchased and PCs prepared, then the team attends and finds missing prerequisites, then rework [4]. Its survey information is scattered across photos and messages, so installation-day surprises include missing ports, unexpected software and data-migration expectations. Its holiday-period technicians are also pulled away by maintenance emergencies [1]. The case itself notes that its example evidence belongs to a fictional business and that you should ask the owner rather than assume it applies to you [2].

Another case, C15, shows a related pattern where several apparently separate failures traced back to one central configuration change [3]. That is less directly relevant here.

Before any diagnosis, the knowledge base requires real evidence from your business. Passage [5] lists only simulated examples, so it doesn't settle whether your situation fits. To move forward, tell me about:
- How many installations or requests you handle per week, and how many arrive during school holidays.
- How you currently collect site information (for example, a survey form, photos, or messages).
- How often installation day reveals a missing prerequisite, and roughly how much rework that causes.
- How long it takes to assign a job or prepare equipment.

I haven't recorded anything yet. Once you give me those details, I can record them and draft a diagnosis.

- passage `cases/C09#001`: ## Business and opening narrative  17 staff; school maintenance plus holiday computer-room projects.  “Sales surveys are scattered across photos and messages. On installation day we discover missing ports, unexpected software or data migration expectations. Maintenance emergencies pull technicians a
- passage `cases/C09#000`: # C09: Installation readiness discovered on site  > Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.
- passage `cases/C15#001`: ## Business and opening narrative  Maintenance provider for multi-site retail and education groups; one customer has 28 branches.  “Head office pays and approves parts, but branches call and control access. Branches expect appointments before approval arrives. Equipment moves between similar-named l
- passage `cases/C09#002`: ## Current workflow  1. Sales survey 2. Quote accepted 3. Equipment purchased 4. PCs prepared 5. Team attends 6. Missing prerequisites discovered 7. Rework
- passage `cases/C02#010`: ## Minimum evidence before reusing this pattern  - A simulated route log shows an avoidable arrival outside the access window. - A simulated assignment review finds the required part in a different van. - Simulated call notes record urgency without impact.

## 30. S10 (owner story)
**Question:** We use subcontractors to cover distant customers, but I cannot see what happened until there is a complaint.

**Answer:** The passages suggest the gap is missing evidence from subcontractors, and they point to two fixes.

**What the passages describe:** In a similar case, partners were sent addresses and symptoms by message. Some returned detailed reports, while others only said "done" [1]. A complaint also arose because assignment time was mistaken for an agreed arrival time [1].

**Suggested fixes:**
- **Send a concise work order** that states the scope, an escalation contact, and what evidence is required. Keep technical completion separate from customer acceptance [3].
- **Use job-scoped mobile reporting** so partners record acceptance, the agreed window, actual arrival, parts used, and approval requests [3]. This gives you the record before a complaint arrives.

**Limits:** Passage [5] says this is a synthetic teaching case, not a real customer record, and that it should not be assumed to apply to your business. The passages don't tell me how your subcontractors currently report, what evidence you need, or how your arrival windows are agreed. If you tell me those details, I can record them as facts and draft a diagnosis for your operation.

- passage `cases/C10#001`: ## Business and opening narrative  Eight internal staff plus regional external service partners.  “We send partners addresses and symptoms by message. Some return detailed reports; others only say done. One replaced a part with branch permission, but head office refused to pay. Assignment time was m
- passage `cases/C15#001`: ## Business and opening narrative  Maintenance provider for multi-site retail and education groups; one customer has 28 branches.  “Head office pays and approves parts, but branches call and control access. Branches expect appointments before approval arrives. Equipment moves between similar-named l
- passage `cases/C10#011`: ## Interventions  **Process first:** Send a concise work order with scope, escalation contact and evidence requirements; separate technical completion from customer acceptance.  **Automation and bounded AI help:** Provide authenticated, job-scoped mobile reporting; record acceptance, agreed window, 
- passage `cases/C06#001`: ## Business and opening narrative  18 staff; approximately 110 mixed PC, printer and network maintenance customers.  “We dispatch when the customer is under contract, but that does not mean the device or work is covered. A personal laptop was repaired at an office, and a part replacement was waived 
- passage `cases/C10#000`: # C10: Subcontractor work lacks acceptance evidence  > Synthetic teaching case: invented for learning, not a customer record. Example answers and evidence belong to this fictional business only; ask the owner rather than assume they apply.
