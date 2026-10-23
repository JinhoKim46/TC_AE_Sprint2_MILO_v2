---
title: Setup fees, surcharges and the estimate range
section: pricing
updated: 2026-10-23
doc_id: pricing/setup-and-range
product: general
synthetic: true
review_status: author_written_for_milo_v2
---
# Setup fees, surcharges and the estimate range

## Setup fee

Each chosen module carries a one-time setup fee of 1200 USD per module. The fee covers configuring the module for the business, importing its starting data and a short handover with the staff who will use it. Two modules cost 2400 USD to set up, three cost 3600 USD, and so on. The setup fee is shown apart from the monthly figure and is not multiplied by the technician factor.

## Integration surcharges

Connecting a module to the business's own tools adds a monthly surcharge for each integration:

| Integration | Monthly surcharge (USD) |
| --- | --- |
| spreadsheet-import | 0 |
| email-capture | 150 |
| service-software-api | 300 |
| accounting-export | 100 |

Spreadsheet import is free because it only exchanges CSV files. Email capture reads a shared mailbox, the service software API connects to the business's service management application with an access key, and the accounting export prepares a file for the accounts team.

A surcharge is counted once per integration, however many modules share it. If request intake and work tracking both read the same shared mailbox, email capture is charged once, at 150 USD a month, not twice. The integrations that apply come from the facts recorded during the diagnosis, not from the module descriptions alone.

## The low, base and high range

Every estimate is shown as a range rather than a single number. The range factors are 0.90 for the low figure, 1.00 for the base figure and 1.20 for the high figure, applied to the monthly total.

The base figure is the estimate computed directly from the rate card and the recorded facts. The low figure, at 0.90, shows what the work could cost if the setup turns out simpler than the diagnosis suggests, for example clean data and few exceptions. The high figure, at 1.20, shows what it could cost if the diagnosis uncovers more exceptions, messier data or extra configuration. The range is wider on the high side on purpose, because surprises in service businesses more often add work than remove it.

## Limits

An estimate can include at most 7 modules, which is the whole catalogue. Asking for the same module twice does not count it twice. A module id that is not in the catalogue is rejected rather than priced by guess, and the assistant asks which module the owner meant.
