---
title: Stock control
section: solutions
updated: 2026-10-23
doc_id: solutions/stock-control
product: stock-control
synthetic: true
review_status: author_written_for_milo_v2
---
# Stock control

## What it does

The Stock control module answers a simple question that many service businesses cannot: where is the toner, the fuser or the loan printer right now? It tracks consumables, parts and loan devices by location, whether they sit in the warehouse, in a technician's van or at a customer site. It also marks which items must be tracked by serial number and warranty, so a returned part can be traced to the device it came from.

## What is included

- Stock by location, covering the warehouse, each van and each customer site.
- Device-to-consumable compatibility, so the right cartridge is picked for the model on site.
- Customer-held stock, for supplies left at a customer's premises under a contract.
- Serialized and warranty items, recorded one by one instead of as a count.
- Simple replenishment rules for cheap items, such as a minimum quantity per van.

## What it does not do

The stock-control module does not raise automatic purchase orders; it can show that stock is low, and a person orders. The stock-control module does not negotiate supplier prices or compare suppliers.

## Connecting it to your tools

- Spreadsheet import: where stock lists live in spreadsheets, stock control takes them in and gives them back as CSV files, with no live connection. This one is free of surcharge.
- Service software API: stock control can follow parts used on jobs in the business's service management application if it offers an API with an access key, after a two-working-day setup. Stock control pays a 300 USD monthly surcharge for this link.

## Price

The base monthly price for stock-control is 390 USD. Stock control carries the same one-time setup fee as every module, 1200 USD. The stock control base is then multiplied by the technician factor, at 1.00 for up to 5 field technicians, 1.30 for up to 15 and 1.60 for up to 30, since every van is another location to track.

## Related synthetic material

Stock control comes from cases C04 and C18, with their playbook and blueprint parts kept inside those case articles. One describes toner that existed but could not be found; the other describes warehouse, van and customer stock figures that no longer agreed.
