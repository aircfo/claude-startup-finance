---
name: revenue-reconciliation
description: Reconcile Stripe revenue against QuickBooks recognized revenue and explain the gap. Use when someone asks "do our Stripe and QuickBooks numbers match," "why is Stripe revenue different from our books," "reconcile revenue," "tie out Stripe to the GL," or is preparing for month-end close or an audit and needs payments-to-books agreement.
---

# Revenue Reconciliation (Stripe ↔ QuickBooks)

Tie Stripe activity to the revenue recorded in QuickBooks and explain any differences.

## When to use this
Trigger when the user wants to compare Stripe to their books, tie out revenue, or chase down why the two don't match — typically during month-end close, board prep, or audit prep.

## Step 0 — Load the finance profile
Read `finance-profile.md` first (the company's semantic map). It gives you the prebuilt bridge structure: which Stripe revenue maps to which QBO revenue account, how processing fees and refunds book, the recognition method (cash vs. ratable), and how deferred revenue, annual prepays, and coupons are treated — so you reconcile against known mappings instead of rediscovering them each time.

Find the profile in this order:
1. If this session's instructions (e.g. a workspace `CLAUDE.md`) include an **airCFO Finance Context** pointer, use the profile path it names.
2. Else if `.aircfo-finance-context.json` exists in the current workspace, read `financeProfile` from it.
3. Else check the default location: `~/Desktop/airCFO Finance Context/finance-profile.md`.
4. Else check the current workspace for `finance-profile.md`.
5. If you still can't find it, run `finance-context-builder` first (or tell the user to). **Do not guess** the revenue mappings or recognition method — without the profile they're guesswork.

## Data to gather (for the same period — confirm the month or range with the user first)
1. **Stripe**: gross volume, refunds, disputes, processing fees, and **net** payout volume for the period.
2. **QuickBooks**: recognized revenue for the period (P&L revenue accounts), plus any deferred-revenue movement if the company recognizes ratably.

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
