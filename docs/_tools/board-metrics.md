---
title: Board metrics
theme: reporting
order: 1
summary: A paste-ready monthly metrics pack (ARR and MRR, cash, burn, runway, and AR/AP aging) with a short narrative on the trend that matters most.
plugin: all-systems-go
skill: board-metrics
ask: Give me board metrics for last month.
reads: [Stripe, Mercury, Ramp, QuickBooks]
needs_contextos: true
time: A few minutes per month
---

## What you get

A summary you can paste straight into a board deck or investor update:

> **[Company] — Financial Metrics, [Month Year]**
> - **ARR / MRR:** $X ARR ($Y MRR), +Z% MoM
> - **Cash:** $X (as of <date>)
> - **Net burn:** $X/mo
> - **Runway:** X months (cash-out ≈ <date>)
> - **AR:** $X total ($Y past due)
> - **AP:** $X total ($Y past due)

Followed by two or three sentences on the most important trend or risk, plus spend
highlights from Ramp and month-over-month changes wherever a prior period exists.

## Where each number comes from

| Metric | Source |
| --- | --- |
| ARR, MRR, growth | Stripe |
| Cash | Mercury |
| Net burn and runway | Mercury, using the same logic as [Runway & burn]({{ '/tools/runway-and-burn/' | relative_url }}) |
| AR and AP aging | QuickBooks |
| Spend highlights | Ramp |

Every metric uses your ContextOS definitions, so board MRR means what *you* mean by MRR,
and it matches the other tools.

## Try asking

```text
Format this so I can paste it into a board deck.
```
