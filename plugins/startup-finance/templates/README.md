# Mapping table — your account map

One table turns the raw QuickBooks general ledger into your management financials: `account-map.csv` classifies every GL account. The `finance-context-builder` skill **drafts it automatically from your QuickBooks Account List**, then walks you through the judgment calls — you don't fill it from scratch. The confirmed map lives in your airCFO Finance Context folder and every finance workflow reads it (via `finance-profile.md`).

QuickBooks owns the account list and the dollar amounts; this table decides how each account classifies and rolls up.

## `account-map.csv`
`account_number, account_name, account_type, class, department, bs_group, cf_section, cf_line`

One row per GL account, keyed on **`account_number` + `account_name`** (matched against QuickBooks exactly). Each account fills only the columns that apply to it — income-statement accounts fill `class` + `department`; balance-sheet accounts fill `bs_group` + `cf_section` + `cf_line`; the rest stay blank.

**Income-statement accounts**
- **`class`** — `Revenue`, `COGS`, `Expense`, `Other Income`, or `Other Expense`. Filled *deterministically* from the QuickBooks account type, so it rarely needs correction.
- **`department`** — the cost-center, classified with judgment (account name → parent account → what the account is for; e.g. "Advertising & Paid Media" → `Marketing`, "Legal Fees" → `G&A`). Genuine G&A is booked to G&A; only irregular or unclear accounts are left blank and flagged. The column most worth a review.

**Balance-sheet accounts**
- **`bs_group`** — `Current Assets`, `Non-current Assets`, `Current Liabilities`, `Non-current Liabilities`, or `Equity`. Filled *deterministically* from the account type.
- **`cf_section`** — `Operating`, `Investing`, or `Financing`.
- **`cf_line`** — the cash-flow line the account's period-over-period movement feeds.

Filled from standard indirect-method rules; review the judgment calls — most often a **treasury / investment** account QuickBooks lists as a current asset but that you may want under **Non-current Assets** and **Investing**. Cash/bank and retained-earnings get a `bs_group` but blank `cf_section`/`cf_line`.

Example (abridged):

| account_number | account_name | account_type | class | department | bs_group | cf_section | cf_line |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4000 | Subscription Revenue | Income | Revenue | | | | |
| 6010 | Salaries & Wages — Engineering | Expense | Expense | Engineering | | | |
| 6400 | Advertising & Paid Media | Expense | Expense | Marketing | | | |
| 1010 | Operating Checking | Bank | | | Current Assets | | |
| 1200 | Accounts Receivable | Accounts Receivable | | | Current Assets | Operating | Change in accounts receivable |
| 2300 | Deferred Revenue | Other Current Liability | | | Current Liabilities | Operating | Change in deferred revenue |
| 1020 | Treasury | Other Current Asset | | | Non-current Assets | Investing | Treasury / investments |

## Notes
- `class` means the **P&L statement section** — it is *not* QuickBooks "class tracking."
- The column names above are the contract the `finance-context-builder` skill reads. Rename a column and you must tell Claude to update the skill.
- This is a blank-header template that ships with the plugin. Your actual map lives in your airCFO Finance Context folder (default `~/Desktop/airCFO Finance Context/account-map.csv`), written by the skill — not here.
