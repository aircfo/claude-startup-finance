# Mapping tables — your reporting framework

Two maps turn the raw QuickBooks general ledger into your management financials. The `finance-context-builder` skill **drafts both of them automatically from your QuickBooks Account List**, then walks you through the judgment calls — you don't fill them from scratch. The confirmed maps get baked into `finance-profile.md`, which every finance workflow reads.

QuickBooks owns the account list and the dollar amounts; these maps decide how each account classifies and rolls up.

## The two maps

Both live in `finance/mappings/` and are keyed on **`account_number` + `account_name`** (matched against QuickBooks exactly).

### `pnl-mapping.csv` — income statement
`account_number, account_name, class, department`

- **`class`** — one of `Revenue`, `COGS`, `Expense`, `Other Income`, `Other Expense`. The skill fills this *deterministically* from the QuickBooks account type (Income → Revenue, Cost of Goods Sold → COGS, and so on), so it rarely needs correction.
- **`department`** — the cost-center. The skill *classifies* this with judgment — from the account name, its parent account, or what the account is for (e.g. "Advertising & Paid Media" → `Marketing`, "Legal Fees" → `G&A`). Genuine G&A is booked to G&A; only accounts that look irregular or whose purpose is unclear are left blank and flagged. It's the column most worth a review.

| account_number | account_name | class | department |
| --- | --- | --- | --- |
| 4000 | Subscription Revenue | Revenue | |
| 5000 | Stripe Processing Fees | COGS | |
| 6010 | Salaries & Wages — Engineering | Expense | Engineering |
| 6400 | Advertising & Paid Media | Expense | Marketing |
| 7100 | Legal Fees | Expense | G&A |

### `balance-sheet-mapping.csv` — balance-sheet grouping + cash-flow classification
`account_number, account_name, bs_group, cf_section, cf_line`

- **`bs_group`** — one of `Current Assets`, `Non-current Assets`, `Current Liabilities`, `Non-current Liabilities`, `Equity`. The skill fills this *deterministically* from the QuickBooks account type.
- **`cf_section`** — one of `Operating`, `Investing`, `Financing`.
- **`cf_line`** — the cash-flow line that the account's period-over-period movement feeds.

The skill fills all three from standard rules by account type; review the judgment calls — most often a **treasury / investment** account that QuickBooks lists as a current asset but that you may want under **Non-current Assets** and **Investing**.

| account_number | account_name | bs_group | cf_section | cf_line |
| --- | --- | --- | --- | --- |
| 1010 | Operating Checking | Current Assets | | |
| 1200 | Accounts Receivable | Current Assets | Operating | Change in accounts receivable |
| 2300 | Deferred Revenue | Current Liabilities | Operating | Change in deferred revenue |
| 2000 | Accounts Payable | Current Liabilities | Operating | Change in accounts payable |
| 1020 | Treasury | Non-current Assets | Investing | Treasury / investments |
| 3000 | Preferred Stock — Series A | Equity | Financing | Equity issuance |

> Every balance-sheet account gets a `bs_group`. Cash / bank accounts and retained-earnings / accumulated-deficit are left with **blank `cf_section` / `cf_line`** — the first *is* the ending cash the statement explains, the second rolls from net income.

## Notes
- `class` here means the **P&L statement section** — it is *not* QuickBooks "class tracking."
- The column names above are the contract the `finance-context-builder` skill reads. Rename a column and you must tell Claude to update the skill.
- These are blank templates that ship with the plugin. Your filled-in copies belong in your working directory's `finance/mappings/`, not here.
