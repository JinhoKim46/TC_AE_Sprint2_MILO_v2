---
title: Meter billing
section: solutions
updated: 2026-10-23
doc_id: solutions/meter-billing
product: meter-billing
synthetic: true
review_status: author_written_for_milo_v2
---
# Meter billing

## What it does

The Meter billing module is for businesses that charge by the page. It collects printer and copier meter readings, whether they come from a photo, a remote reading or a technician's note, and checks each one against the device's history and the contract terms. It then prepares the usage charges. Readings that do not make sense, such as a counter that went backwards or a photo without a serial number, go to an exception queue for a person to review instead of being billed.

## What is included

- Meter reading capture with photo reference, so every reading can be traced to the image or note it came from.
- Chronology and counter checks that catch readings out of order, decreasing counters and readings attached to the wrong device.
- Usage calculation per contract, applying each agreement's colour and monochrome allowances.
- An exception queue for review, where questionable readings wait for a decision.

The module treats a device replacement as two separate segments, one closing reading for the old machine and one opening reading for the new one, which is where many disputed bills begin.

## What it does not do

The meter-billing module does not send invoices without review; prepared charges always pass a person first. The meter-billing module does not set customer tariffs, which remain a commercial decision recorded in the contract.

## Connecting it to your tools

- Spreadsheet import: if readings and contracts are kept in spreadsheets, meter billing exchanges CSV files with them and holds no live connection. No surcharge applies.
- Accounting export: meter billing hands the prepared usage charges to the accounts team as a file for them to import into the accounting software. It adds 100 USD a month.

Meter billing shares integrations with the other chosen modules, and the accounting export surcharge is charged once even when contract management uses the same export.

## Price

The base monthly price for meter-billing is 450 USD. A one-time 1200 USD setup fee covers configuring meter billing. The meter billing base price is multiplied by the technician factor: 1.00 when the business has up to 5 field technicians, 1.30 for up to 15 and 1.60 for up to 30.

## Related synthetic material

Meter billing is based on case C05, whose article also carries the playbook and blueprint material and describes meter readings that delayed and corrupted invoices after a device replacement.
