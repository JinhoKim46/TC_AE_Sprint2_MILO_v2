---
title: Dispatch planning
section: solutions
updated: 2026-10-23
doc_id: solutions/dispatch-planning
product: dispatch-planning
synthetic: true
review_status: author_written_for_milo_v2
---
# Dispatch planning

## What it does

The Dispatch planning module helps the dispatcher rebuild the day when something changes: a technician is ill, an urgent job arrives or a site cannot be entered until the afternoon. It looks at each technician's skills, the parts in each van, the access windows of each site and notes on whether a job can be handled remotely, and it proposes a revised schedule. The dispatcher reads the proposal and decides; nothing moves on its own.

## What is included

- Schedule revision suggestions that show which visits could move and why.
- Site access windows, such as a clinic that only allows work before opening or a school that closes at four.
- A remote-suitability check that asks whether a fault can really be solved without a visit before a remote attempt is planned.
- Skill and stock constraints, so a job is not proposed for a technician who lacks the training or the part.
- Dispatcher override, which lets the dispatcher reject or change any suggestion and records the reason.

## What it does not do

The dispatch-planning module does not reassign jobs automatically without the dispatcher. The dispatch-planning module does not provide route navigation; technicians keep the map application they already use. The dispatch-planning module does not include remote-control software, and it only records whether a remote session is a sensible first step.

## Connecting it to your tools

- Spreadsheet import: a schedule kept in spreadsheets can feed dispatch planning through CSV files going in and out, with no live link between the two. There is no monthly surcharge for it.
- Service software API: dispatch planning can read jobs from the business's service management application when that application offers an API with an access key, and the connection takes two working days to set up. Its surcharge for dispatch planning is 300 USD a month.

## Price

The base monthly price for dispatch-planning is 560 USD. A one-time setup fee of 1200 USD applies when dispatch planning is switched on. The dispatch planning base price is scaled by the technician factor, which is 1.00 for up to 5 field technicians, 1.30 for up to 15 and 1.60 for up to 30. Because dispatch planning is about the field team, a correct technician count matters most here.

## Related synthetic material

Dispatch planning draws on cases C02, C08 and C16, whose articles include the matching diagnostic playbook and implementation blueprint. These cover a day disrupted by access constraints, a remote-first rule that added delay, and clinic work that had to respect operating hours.
