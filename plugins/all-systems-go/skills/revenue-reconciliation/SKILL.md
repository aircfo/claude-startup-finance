---
name: revenue-reconciliation
description: Reconcile Stripe revenue against QuickBooks recognized revenue and explain the gap. Use when someone asks "do our Stripe and QuickBooks numbers match," "why is Stripe revenue different from our books," "reconcile revenue," "tie out Stripe to the GL," or is preparing for month-end close or an audit and needs payments-to-books agreement.
---

# Revenue Reconciliation (Stripe ↔ QuickBooks)

Tie Stripe activity to the revenue recorded in QuickBooks and explain any differences.

## When to use this
Trigger when the user wants to compare Stripe to their books, tie out revenue, or chase down why the two don't match — typically during month-end close, board prep, or audit prep.

## Step 0: Read the Finance Brain
Read the company's Finance Brain first: the folder from the airCFO Finance Brain Starter Kit (a `CLAUDE.md` plus `handbook/`). It gives you the prebuilt bridge structure, so you reconcile against known mappings instead of rediscovering them each time:
- `handbook/accounting-policies.md` (Revenue recognition): cash vs. ratable, annual prepays, deferred revenue, discounts, credits, and refunds.
- `handbook/chart-of-accounts.md` (Reporting rollups): which QuickBooks accounts are recurring revenue and which are contra-revenue.
- `handbook/systems-and-data.md` (Same thing, different names): customers that appear under different names in Stripe and QuickBooks, and known data issues such as payouts landing net of fees.

Find it in this order:
1. The current workspace, if it holds a `CLAUDE.md` and a `handbook/` folder. In Cowork the user usually works in that folder, so `CLAUDE.md` is already loaded.
2. Otherwise, ask the user where their Finance Brain folder is. Don't search the disk at random.
3. If there's no Finance Brain, say so and point the user to the free kit (https://aircfo.github.io/claude-startup-finance/finance-brain.html), where its `setup-finance-brain` skill builds one.

**Do not guess** the revenue mappings or recognition method. Without the Finance Brain, or where a page you need still says `[PLACEHOLDER`, treat that definition as unknown: either stop, or label every number that depends on it as an assumption the user must confirm, and list it as an open question.

## Data to gather (for the same period — confirm the month or range with the user first)
1. **Stripe**: gross volume, refunds, disputes, processing fees, and **net** payout volume for the period.
2. **QuickBooks**: recognized revenue for the period (P&L revenue accounts), plus any deferred-revenue movement if the company recognizes ratably.
   - QuickBooks comes from a QuickBooks connector the user adds in Claude's connector settings (for example, Intuit's), read-only with their own login. If it isn't connected, ask for the specific export instead: the report name and the exact date range.

## Why they differ (check each)
- **Timing**: Stripe is cash-in; QBO revenue may be accrual or recognized over time — deferred revenue is the bridge.
- **Fees**: Stripe nets fees out of payouts; QBO usually books gross revenue with a separate processing-fee expense.
- **Refunds / chargebacks**: may post in different periods.
- **Non-revenue Stripe activity**: transfers, top-ups, or balance adjustments that aren't revenue.
- **Other revenue in QBO** not flowing through Stripe (ACH, wires, invoices paid outside Stripe).

## Method
1. Start from **Stripe gross revenue** for the period.
2. Walk to **QBO recognized revenue** with an explicit bridge: gross − fees − refunds ± deferred-revenue movement ± non-Stripe revenue = recognized revenue.
3. Quantify each reconciling item. Flag anything you can't explain as an open item.

## Always
- Use a computation step for the math; present the bridge as a waterfall (start → adjustments → end).
- Confirm the exact period and whether the company recognizes revenue ratably before starting.

## Output format
1. **Headline**: matched within $X, or a $Y unexplained gap.
2. **Reconciliation bridge** (table): Stripe gross → each adjustment → QBO recognized.
3. **Open items**: anything unexplained, each with a suggested next step to investigate.

## Never
- Read-only — never write to Stripe, QuickBooks, Ramp, or Mercury.
- Never store secrets, tokens, or full account numbers — names, last-4, and internal IDs only.
