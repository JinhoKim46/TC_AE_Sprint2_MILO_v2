---
title: How we price
section: pricing
updated: 2026-10-23
doc_id: pricing/how-we-price
product: general
synthetic: true
review_status: author_written_for_milo_v2
---
# How we price

## What an estimate is built from

An estimate has four parts. The first is the base monthly price of each chosen module. The second is the technician factor, which scales the module prices by the size of the field team. The third is the integration surcharge, a monthly amount for each connection to the business's own tools. The fourth is the one-time setup fee charged for each module.

The monthly figure is the sum of the chosen modules' base prices, multiplied by the technician factor, plus the surcharges for the integrations the business needs. The setup fee is shown separately because it is paid once, not every month. Every figure is shown in USD and is indicative: it describes the likely cost of the work discussed, not a signed offer.

## Base monthly prices

| Module | Base monthly price (USD) |
| --- | --- |
| request-intake | 420 |
| dispatch-planning | 560 |
| contract-management | 480 |
| stock-control | 390 |
| meter-billing | 450 |
| service-reports | 340 |
| work-tracking | 360 |

These are the prices before the technician factor and before any integration surcharge. A business that chooses two modules pays both base prices; there is no bundle discount in the rate card.

## Where the numbers come from

The estimate is computed in code from the recorded facts, never typed by the assistant. During the diagnosis the assistant records what the owner says, for example how many field technicians the business has and which tools it already uses. When the owner asks what something would cost, the assistant asks the estimate tool for the chosen modules, and the tool reads the rate card and the recorded facts and does the arithmetic.

This matters for two reasons. A language model can make arithmetic mistakes or round a number to something that sounds plausible, and a price that was never computed can still look confident. Keeping the calculation in code means the same facts always give the same estimate, and anyone can check it against the rate card.

If a fact the estimate needs is missing, such as the technician count, the assistant asks for it instead of guessing. If the owner later corrects a fact, the estimate is computed again from the corrected value.

## What the estimate does not cover

The estimate covers the modules, their setup and their connections. It does not price work outside the catalogue, and it never extends the rate card by analogy to a synthetic case. When a request falls outside these rules, the assistant says so and a person prepares the offer.
