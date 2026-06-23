# Mapping table — your account map

One table turns the raw QuickBooks general ledger into your management financials: `account-map.csv` classifies every GL account. The `finance-context-builder` skill **drafts it automatically from your QuickBooks Account List**, then walks you through the judgment calls — you don't fill it from scratch. The confirmed map lives in your airCFO Finance Context folder and every finance workflow reads it (via `finance-profile.md`).

QuickBooks owns the account list and the dollar amounts; this table decides how each account classifies and rolls up.

## `account-map.csv`
`account_number, account_name, account_type, detail_type, department, cf_section, cf_line, description`

One row per GL account, keyed on **`account_number` + `account_name`** (matched against QuickBooks exactly). **Most columns come straight from QuickBooks; the two reporting maps — `department` (P&L) and `cf_section` / `cf_line` (balance sheet) — take a little judgment.**

- **`account_type`** — the QuickBooks **Type** field, verbatim. P&L: `Income`, `Cost of Goods Sold`, `Expense`, `Other Income`, `Other Expense`. Balance sheet: `Bank`, `Accounts Receivable`, `Other Current Asset`, `Fixed Asset`, `Other Asset`, `Accounts Payable`, `Credit Card`, `Other Current Liability`, `Long Term Liability`, `Equity`.
- **`detail_type`** — the QuickBooks **Detail Type** field, verbatim (e.g. `Checking`, `Service/Product Income`, `Payroll`, `Legal & Professional`).
- **`department`** — the management-reporting grouping, **P&L accounts only** (blank for balance-sheet accounts): `Revenue` for income, `Cost of Goods Sold` for COGS, and an OpEx department (G&A, Engineering, Sales, Marketing, …) for operating expense — classified with judgment (account name → parent account → what the account is for; e.g. "Advertising & Paid Media" → `Marketing`, "Legal Fees" → `G&A`). Other Income / Other Expense are left blank. The column most worth a review.
- **`cf_section`** + **`cf_line`** — the cash-flow-statement mapping (indirect method), **balance-sheet accounts only** (blank for P&L accounts): each account's period-over-period change feeds a cash-flow line. `cf_section` ∈ `Operating` / `Investing` / `Financing`. Mostly deterministic from the account type (e.g. AR → `Operating`, "Change in accounts receivable"); cash/bank and retained earnings stay blank. The judgment call worth a review is a **treasury / investment** account QuickBooks lists as a current asset that you may want under **Investing**.
- **`description`** — a short plain-language note on what the account is for (the QuickBooks description if it has one).

Example (abridged):

| account_number | account_name | account_type | detail_type | department | cf_section | cf_line | description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4000 | Subscription Revenue | Income | Service/Product Income | Revenue | | | Per-seat SaaS subscription revenue |
| 5000 | Hosting & Infrastructure | Cost of Goods Sold | Cost of Sales | Cost of Goods Sold | | | Cloud hosting & infra serving the product |
| 6000 | Salaries & Wages — Engineering | Expense | Payroll | Engineering | | | Engineering team salaries |
| 6100 | Advertising & Paid Media | Expense | Advertising/Promotional | Marketing | | | Paid acquisition spend |
| 1000 | Mercury Checking ••0736 | Bank | Checking | | | | Primary operating cash account |
| 1200 | Accounts Receivable | Accounts Receivable | AR | | Operating | Change in accounts receivable | Customer invoices outstanding |
| 2200 | Deferred Revenue | Other Current Liability | Deferred | | Operating | Change in deferred revenue | Annual prepayments not yet recognized |

## Notes
- `account_type` and `detail_type` are copied **verbatim from QuickBooks** (the QBO **Type** and **Detail Type** fields) — not derived.
- `department` is a **management-reporting** grouping (Revenue / Cost of Goods Sold / OpEx department) — it is *not* QuickBooks "class tracking."
- `cf_section` / `cf_line` are **balance-sheet only** — they map each account's *change* to the indirect-method cash-flow statement. P&L accounts leave them blank.
- The column names above are the contract the `finance-context-builder` skill reads. Rename a column and you must tell Claude to update the skill.
- This is a blank-header template that ships with the plugin. Your actual map lives in your airCFO Finance Context folder (default `~/Desktop/airCFO Finance Context/account-map.csv`), written by the skill — not here.

## `finance-profile-template.md`
The folder's other template is the **finance-profile skeleton** — the 14-section structure the `finance-context-builder` skill drafts your `finance-profile.md` from (Company Snapshot, Business Model, KPI Definitions, Source-of-Truth Map, Reporting Framework, the cash / revenue / spend / people rules, Planning, Cadence & Materiality, Known Exceptions, Open Questions, Provenance). The skill fills what it can from your context docs and a read-only pass over your systems, and leaves a `[PLACEHOLDER: …]` wherever it doesn't yet know — so you can see and fill the gaps before finalizing. It's a starting skeleton; your real profile lives in the airCFO Finance Context folder.
