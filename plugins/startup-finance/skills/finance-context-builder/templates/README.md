# Mapping table — your account map

One table turns the raw QuickBooks general ledger into your management financials: `account-map.csv` classifies every GL account. The `finance-context-builder` skill **drafts it automatically from your QuickBooks Account List**, then walks you through the judgment calls — you don't fill it from scratch. The confirmed map lives in your airCFO Finance Context folder and every finance workflow reads it (via `finance-profile.md`).

QuickBooks owns the account list and the dollar amounts; this table decides how each account classifies and rolls up. The full schema — column rules, the Expense Category and department vocabularies, the tag registry, the cash-flow line list, and the refresh workflow — lives in **`account-map-spec.md`** alongside this file. This README is the orientation; the spec is the contract.

## The mental model: a cube, not a tree

Every account carries a few **independent labels** (axes). Reports are built by *pivoting* those axes into whatever nesting a deliverable needs — the map itself never hard-codes an outline:

| Axis | Question it answers | Column |
| --- | --- | --- |
| **Class** | Where does it sit on the statements? | derived from `account_type` (never stored) |
| **Expense Category** | What *kind* of money is it? (Subscription revenue, Payroll & benefits, Software & tools, …) | `expense_category` |
| **Department** | *Whose* money is it? (Engineering, Sales, Marketing, CS, G&A, …) | `department` |
| Cash flow | How does its change move cash? | `cf_section` + `cf_line` (balance sheet only) |
| Analysis groups | What cross-cutting analyses does it feed? (`mrr`, `cac`, `clearing`, …) | `tags` |

The same map renders a monthly package (Class → Category → Department), a department P&L (Class → Department → Category), a cash walk (`cf_section` → `cf_line`), or a P&L-based MRR (sum of `mrr`-tagged accounts) — no restructuring required.

## `account-map.csv`

`gl_account_id, account_number, account_name, account_type, detail_type, parent_account, active, expense_category, department, cf_section, cf_line, tags, mapping_status, review_note, confirmed_by, confirmed_date`

One row per GL account, keyed on **`gl_account_id`** — QuickBooks' internal account Id, which survives renames and renumbers, so refreshes can diff safely. Three column groups:

- **Ledger facts** (`gl_account_id` → `active`) — copied verbatim from QuickBooks, overwritten on every refresh, never hand-edited.
- **Reporting mappings** (`expense_category`, `department`, `cf_section`, `cf_line`, `tags`) — drafted by rule, owned by you after confirmation. Values come from the vocabularies in `account-map-spec.md`.
- **Governance** (`mapping_status`, `review_note`, `confirmed_by`, `confirmed_date`) — every row is `auto`, `needs-review`, or `confirmed`. **A refresh never overwrites a confirmed row's mappings**, and workflows disclose any non-confirmed rows a deliverable relied on.

Example (abridged — a typical SaaS chart):

| account_name | account_type | expense_category | department | cf_line | tags | mapping_status |
| --- | --- | --- | --- | --- | --- | --- |
| Subscription Revenue | Income | Subscription revenue | | | mrr | confirmed |
| Implementation Fees | Income | Professional services revenue | | | | confirmed |
| Promotional Credits | Income | Discounts & credits | | | contra-revenue | confirmed |
| AWS Hosting | Cost of Goods Sold | Hosting & infrastructure | Infrastructure | | | confirmed |
| Salaries — Engineering | Expense | Payroll & benefits | Engineering | | | confirmed |
| Advertising & Paid Media | Expense | Marketing & advertising | Marketing | | cac | confirmed |
| Mercury Checking ••0736 | Bank | Cash & equivalents | Operating cash | | | confirmed |
| Mercury Treasury | Bank | Cash & equivalents | Treasury | | | needs-review |
| Accounts Receivable | Accounts Receivable | Accounts receivable & reserves | | Change in accounts receivable | | confirmed |
| Deferred Revenue | Other Current Liability | Deferred revenue | | Change in deferred revenue | | confirmed |
| SAFE Notes | Long Term Liability | SAFEs & convertible notes | | Equity issuance (stock, SAFEs, convertible notes) | | confirmed |

## Notes
- `account_type` / `detail_type` are copied **verbatim from QuickBooks** — not derived. `detail_type` *seeds* the `expense_category` draft; the human's override always wins.
- `department` is a **management-reporting** grouping — it is *not* QuickBooks "class tracking." What kind of value it holds follows the account's Class (see the spec).
- `tags` are **registry-controlled** (see the spec) — they encode account-level KPI inputs (`mrr`, `cac`) and behaviors (`clearing`, `contra-revenue`); they are not free-form labels.
- The column names are the contract every finance workflow reads. Rename a column and you must tell Claude to update the skills.
- This is a blank-header template that ships with the plugin. Your actual map lives in your airCFO Finance Context folder (default `~/Desktop/airCFO Finance Context/account-map.csv`), written by the skill — not here.

## `finance-profile-template.md`
The folder's other template is the **finance-profile skeleton** — the 14-section structure the `finance-context-builder` skill drafts your `finance-profile.md` from (Company Snapshot, Business Model, KPI Definitions, Source-of-Truth Map, Reporting Framework, the cash / revenue / spend / people rules, Planning, Cadence & Materiality, Known Exceptions, Open Questions, Provenance). The skill fills what it can from your context docs and a read-only pass over your systems, and leaves a `[PLACEHOLDER: …]` wherever it doesn't yet know — so you can see and fill the gaps before finalizing. It's a starting skeleton; your real profile lives in the airCFO Finance Context folder.
