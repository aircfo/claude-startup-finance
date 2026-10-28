# Chart of accounts

**What this page is for:** how the chart of accounts is organized, so Claude codes things the
way your team would and never invents an account.

**Last reviewed:** [PLACEHOLDER: YYYY-MM-DD, by whom]

## Source of truth

The full account list lives in [PLACEHOLDER: the accounting system, or an export saved at
`handbook/chart-of-accounts.csv`]. Claude reads the list from there. This page explains the
structure and the judgment calls; it doesn't duplicate every account.

**Rule:** Claude only uses accounts that exist in the source of truth. If a task seems to need
an account that doesn't exist, stop and ask. Never create or rename accounts.

## Numbering

| Range | Type | Notes |
| --- | --- | --- |
| [PLACEHOLDER: e.g. 1000-1999] | Assets | |
| [PLACEHOLDER: e.g. 2000-2999] | Liabilities | |
| [PLACEHOLDER: e.g. 3000-3999] | Equity | |
| [PLACEHOLDER: e.g. 4000-4999] | Revenue | |
| [PLACEHOLDER: e.g. 5000-5999] | Cost of revenue | |
| [PLACEHOLDER: e.g. 6000-7999] | Operating expenses | |
| [PLACEHOLDER: e.g. 8000-9999] | Other income and expense | |

## Departments, classes, and other dimensions

[PLACEHOLDER: how the company tags transactions by department, class, location, or project,
and which ones are required on a JE.]

## The judgment calls

Accounts where the right answer isn't obvious from the name. Write the rule once so nobody
has to rediscover it.

| Spend or activity | Account | Why |
| --- | --- | --- |
| [PLACEHOLDER: e.g. cloud hosting for the product] | [PLACEHOLDER: e.g. 5100 Hosting (COGS)] | [PLACEHOLDER: e.g. serves customers, so it's cost of revenue, not R&D] |
| [PLACEHOLDER: e.g. cloud hosting for internal tools] | [PLACEHOLDER] | |
| [PLACEHOLDER: e.g. contractors] | [PLACEHOLDER] | |

## Reporting rollups

Groups of accounts that metrics and reports depend on. Write them down once so every report
adds up the same accounts. The definitions themselves live in
`handbook/metrics-and-reporting.md`.

| Rollup | What it's for | Accounts |
| --- | --- | --- |
| Recurring revenue (MRR) | The accounts that add up to recurring revenue | [PLACEHOLDER: e.g. 4000 Subscription revenue] |
| Contra-revenue | Discounts, credits, and refunds netted against revenue | [PLACEHOLDER] |
| Excluded from burn | One-time or non-operating activity left out of run-rate burn | [PLACEHOLDER: e.g. 8100 Interest income] |
| Sales and marketing spend (for CAC) | What counts as acquisition cost | [PLACEHOLDER] |
| Clearing | Accounts money passes through, which should net to zero (also listed below) | [PLACEHOLDER] |

## Accounts that should always be zero

Clearing accounts, payroll holding accounts, and anything else that should net to zero at
month end. The close checks these.

- [PLACEHOLDER]

## Accounts to leave alone

Legacy or inactive accounts that should not receive new activity.

- [PLACEHOLDER]
