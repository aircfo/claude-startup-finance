---
name: board-metrics
description: Assemble a board-ready financial metrics pack for a startup — MRR/ARR and growth from Stripe, net burn and runway from Mercury + Ramp, cash on hand, and AR/AP aging from QuickBooks. Use when someone asks for "board metrics," "the numbers for the board deck," "our key financial metrics," "a KPI summary," or is preparing a monthly investor update.
---

# Board Metrics Pack

Produce a concise, board-ready financial summary by pulling the key metrics from each connector.

## When to use this
Trigger when the user is preparing a board deck, investor update, or monthly metrics summary and wants the core financial KPIs in one place.

## Step 0 — Load the finance profile
Read `finance-profile.md` first (the company's semantic map). Use its pinned definitions (MRR, revenue recognition, burn, internal transfers), the cash account set, and the AR/AP account mappings so every metric here is consistent with the other workflows.

Find the profile in this order:
1. If this session's instructions (e.g. a workspace `CLAUDE.md`) include an **airCFO Finance Context** pointer, use the profile path it names.
2. Else if `.aircfo-finance-context.json` exists in the current workspace, read `financeProfile` from it.
3. Else check the default location: `~/Desktop/airCFO Finance Context/finance-profile.md`.
4. Else check the current workspace for `finance-profile.md`.
5. If you still can't find it, run `finance-context-builder` first (or tell the user to). **Do not guess** the metric definitions or account set — without the profile they're guesswork.

## Metrics to assemble (confirm the reporting month with the user first)
1. **Revenue (Stripe)**: MRR and ARR, new vs. churned MRR if available, month-over-month growth %.
2. **Cash (Mercury)**: total cash across operating and treasury accounts, as of period end.
3. **Burn & runway (Mercury + Ramp)**: net monthly burn and months of runway — reuse the `runway-and-burn` logic.
4. **AR aging (QuickBooks)**: total receivables and amount past due (current / 30 / 60 / 90+).
5. **AP aging (QuickBooks)**: total payables and amount past due.
6. **Spend highlights (Ramp)**: top spend categories or vendors for the month, if useful context.

## Always
- Use a computation step for all aggregates; never eyeball totals.
- State the reporting period and as-of date once at the top.
- Keep it tight — board readers want the number and the trend, not the raw transactions.
- Where a prior period is available, show the month-over-month change.

## Output format
A clean summary the user can paste into a deck:

> **[Company] — Financial Metrics, [Month Year]**
> - **ARR / MRR**: $X ARR ($Y MRR), +Z% MoM
> - **Cash**: $X (as of <date>)
> - **Net burn**: $X/mo
> - **Runway**: X months (cash-out ≈ <date>)
> - **AR**: $X total ($Y past due)
> - **AP**: $X total ($Y past due)

Follow with a 2–3 sentence narrative on the most important trend or risk.

## Never
- Read-only — never write to Stripe, Mercury, Ramp, or QuickBooks.
- Never store secrets, tokens, or full account numbers — names, last-4, and internal IDs only.
