---
title: How the effect of an automation is estimated
section: consultation
updated: 2026-10-26
doc_id: consultation/effect-estimate
product: general
synthetic: true
review_status: author_written_for_milo_v2
---
# How the effect of an automation is estimated

## The formula

The net time saved per period is the number of events multiplied by the minutes saved per event, divided by 60, minus the extra review time and the upkeep time:

net hours per period = events × (baseline minutes − new minutes) ÷ 60 − extra review hours − maintenance hours

## Where each input comes from

Each input has a unit, a period and a source. A value the owner gave is marked as reported. A value the bot assumed is marked as assumed, and the answer says so. A value that is not known stays empty; it is never counted as zero.

## How the range is shown

The answer gives a central value and a range. The low end is 0.8 times the central value and the high end is 1.2 times it, unless the owner gave a range. The answer names which input moves the result most.

## What is not added together

Stages that overlap are measured once. Intake, ticket creation and transcription done in the same minutes are not counted as three savings.

## Limits

Time saved is not the same as money saved, and it does not show that staff can be reduced. The estimate measures time on a task. It does not measure quality or customer outcomes.
