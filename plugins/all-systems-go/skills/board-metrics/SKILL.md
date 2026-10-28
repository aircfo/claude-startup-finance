---
name: board-metrics
description: Assemble a board-ready financial metrics pack for a startup — MRR/ARR and growth from Stripe, net burn and runway from Mercury + Ramp, cash on hand, and AR/AP aging from QuickBooks. Use when someone asks for "board metrics," "the numbers for the board deck," "our key financial metrics," "a KPI summary," or is preparing a monthly investor update.
---

# Board Metrics Pack

Produce a concise, board-ready financial summary by pulling the key metrics from each connector.

## When to use this
Trigger when the user is preparing a board deck, investor update, or monthly metrics summary and wants the core financial KPIs in one place.

## Step 0: Read the Finance Brain
Read the company's Finance Brain first: the folder from the airCFO Finance Brain Starter Kit (a `CLAUDE.md` plus `handbook/`). Use its definitions so every metric here is consistent with the other workflows:
- `handbook/metrics-and-reporting.md` (The numbers we run on, Burn and runway, Who reads the numbers): the company's exact metric definitions (MRR and its boundary cases), the burn and runway method, and what the board expects to see.
- `handbook/cash.md`: which accounts count as cash on hand and runway cash, and how internal transfers are recorded.
- `handbook/chart-of-accounts.md` (Reporting rollups): which accounts add up to recurring revenue and contra-revenue, and which are excluded from burn.

Find it in this order:
1. The current workspace, if it holds a `CLAUDE.md` and a `handbook/` folder. In Cowork the user usually works in that folder, so `CLAUDE.md` is already loaded.
2. Otherwise, ask the user where their Finance Brain folder is. Don't search the disk at random.
3. If there's no Finance Brain, say so and point the user to the free kit (https://aircfo.github.io/claude-startup-finance/finance-brain.html), where its `build-handbook` skill builds one.

**Do not guess** the metric definitions or account set. Without the Finance Brain, or where a page you need still says `[PLACEHOLDER`, treat that definition as unknown: either stop, or label every number that depends on it as an assumption the user must confirm, and list it as an open question.

## Metrics to assemble (confirm the reporting month with the user first)
1. **Revenue (Stripe)**: MRR and ARR, new vs. churned MRR if available, month-over-month growth %.
2. **Cash (Mercury)**: total cash across operating and treasury accounts, as of period end.
3. **Burn & runway (Mercury + Ramp)**: net monthly burn and months of runway — reuse the `runway-and-burn` logic.
4. **AR aging (QuickBooks)**: total receivables and amount past due (current / 30 / 60 / 90+).
5. **AP aging (QuickBooks)**: total payables and amount past due.
   - QuickBooks comes from a QuickBooks connector the user adds in Claude's connector settings (for example, Intuit's), read-only with their own login. If it isn't connected, ask for the specific export instead: the report name and the exact date range.
6. **Spend highlights (Ramp)**: top spend categories or vendors for the month, and the biggest movers vs. the prior month.

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
