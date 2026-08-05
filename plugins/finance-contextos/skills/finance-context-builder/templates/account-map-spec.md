# Account Map Specification — tech-startup edition

The account map is the **source-of-truth mapping file every finance workflow extracts
from**: the join table between the company's general ledger and its management-reporting
language. One map per company, drafted by the `finance-context-builder` skill from the
QuickBooks Account List, confirmed by the finance pro, and read by every other workflow.

## The mental model: a cube, not a tree

Every account carries a small set of **independent axes**. No axis outranks another in
the data; each is MECE on its own. A report hierarchy is something a *deliverable* builds
at render time by choosing a nesting order — the map itself never encodes an outline.

| Axis | Question it answers | Where it lives |
|---|---|---|
| **Class** | Where does it sit on the statements? | Derived from `account_type` — never stored |
| **Expense Category** | What kind of money is it? | `expense_category` column |
| **Department** | Whose money is it? | `department` column |
| Cash flow | How does it move cash? | `cf_section` + `cf_line` columns |
| Analysis groups | What cross-cutting analyses does it feed? | `tags` column |

Standard renderings (defined per deliverable, never in the data):
- **Monthly package:** Class → Expense Category → Department
- **Department P&L:** Class → Department → Expense Category
- **Cash walk:** `cf_section` → `cf_line`
- **KPI extracts:** filter on `tags` (e.g., sum `mrr`-tagged accounts for P&L-based MRR)
- **Anomaly sweep:** filter on `tags` (every `clearing` account must net to zero)

## Columns

### Group 1 — Ledger facts (from QuickBooks verbatim; overwritten on refresh, never hand-edited)
| Column | Source |
|---|---|
| `gl_account_id` | QuickBooks' internal account **Id** — the primary key; survives renames and renumbers |
| `account_number` | verbatim |
| `account_name` | verbatim |
| `account_type` | verbatim (⇒ Class) |
| `detail_type` | verbatim (seeds `expense_category`) |
| `parent_account` | parent's number + name (exposes header-vs-postable accounts) |
| `active` | verbatim |

### Group 2 — Reporting mappings (human-owned after confirmation)
| Column | Rules |
|---|---|
| `expense_category` | One value from the **Expense Category vocabulary** (below; the name is legacy but the column applies to *all* Classes — revenue and balance sheet included). Auto-seeded from `detail_type` + account-name keywords on first draft; the human's override always wins on refresh. |
| `department` | One value from the **company's department vocabulary**. The *kind* of value follows Class: revenue → product / revenue stream · COGS → cost-of-revenue function · OpEx → operating department · balance sheet → cash bucket (Operating cash / Treasury). Blank only where genuinely unattributable. |
| `cf_section` | `Operating` / `Investing` / `Financing`. Balance-sheet accounts only. |
| `cf_line` | One value from the cash-flow line list (below). Balance-sheet accounts only; the (`cf_section`, `cf_line`) pair must appear in the list. |
| `tags` | Zero or more values from the **tag registry** (below), semicolon-separated. Tags bucket accounts for analyses that **cross the other axes** — groupings no single Class/Category/Department slice can produce (KPI inputs, behavioral flags). New tags are added to the registry first. |

### Group 3 — Governance
| Column | Rules |
|---|---|
| `mapping_status` | `auto` (rule-drafted, unreviewed) · `needs-review` (a judgment call awaiting the human) · `confirmed` (human-verified). **Refreshes never overwrite a `confirmed` row's Group-2 values.** Workflows must disclose any non-`confirmed` rows a deliverable relied on. |
| `review_note` | Why the row needs review — cleared when the row is confirmed |
| `confirmed_by` / `confirmed_date` | Who signed off, when |

## Expense Category vocabulary (tech-startup default)

Fixed vocabulary; values double as management-package line labels. Adjust with the
finance pro if their reporting package uses different words — then keep it stable.

**Revenue:** Subscription revenue · Usage & transaction revenue · Professional services revenue · Other revenue · Discounts & credits *(always also tagged `contra-revenue`)* · Uncategorized revenue *(should trend to zero)*

**COGS:** Hosting & infrastructure · Third-party APIs & data · Payment processing · Cost of labor — support & services · Delivery software & tools

**Operating expenses:** Payroll & benefits *(salaries, payroll taxes, bonus, commissions, benefits & stipends, 401k fees, severance)* · Contractors & consulting · Software & tools · Marketing & advertising · Business development & events *(partnerships, referral fees, conferences)* · Travel · Meals & team events · Rent & facilities *(incl. utilities, telecom)* · Office & equipment · Professional services *(legal, accounting, audit)* · Insurance · Recruiting · Training & development · Bank & payment fees · Taxes & licenses *(non-income: franchise, filing fees)* · Bad debt · FX gain/loss · Other operating expenses *(use sparingly)* · Uncategorized / suspense *(should trend to zero)*

**Below the line:** Interest income · Other income · Interest expense · Depreciation & amortization · Income & franchise taxes · Reconciliation & suspense *(should be zero)*

**Balance sheet:** Cash & equivalents · Accounts receivable & reserves · Prepaid expenses · Undeposited funds · Other current assets · Fixed assets & accumulated depreciation · Capitalized software · Deposits · Other assets · Accounts payable · Credit cards · Accrued payroll & benefits · Deferred revenue · Taxes payable · Other current liabilities · Debt · SAFEs & convertible notes · Equity — stock & APIC · Equity — contributions & distributions · Retained earnings · Other equity

## Department vocabulary (tech-startup default)

Per-company values; the canonical starter set (match to the company's own reporting
package before confirming):
- **Revenue accounts** → product line / revenue stream (single-product companies may leave this blank or use one value).
- **COGS accounts** → cost-of-revenue function: Infrastructure · Support · Services.
- **OpEx accounts** → Engineering (R&D) · Sales · Marketing · Customer Success · G&A. (Companies that report Sales & Marketing as one department use `S&M`.)
- **Balance sheet** → Operating cash · Treasury (cash accounts only; other BS accounts blank).

## Tag registry (initial)

| Tag | Grouping it defines | Used by |
|---|---|---|
| `mrr` | Revenue accounts that count as monthly recurring revenue | P&L-based MRR/ARR (where Stripe/contract-level detail exists, that source is authoritative and the tag is the fast proxy) |
| `cac` | Spend forming the CAC numerator when it crosses departments | CAC / LTV:CAC / Magic Number |
| `contra-revenue` | Discounts/credits netted against revenue | Revenue analyses (gross vs net) |
| `pass-through` | Client-reimbursed / billable; excluded from margin math | Margin & KPI workflows |
| `clearing` | Should net to zero | Anomaly sweep (alert if ≠ 0) |
| `non-operating` | Owner draws and similar; excluded from ops analyses | Cash walk, burn calcs |

## Cash-flow classification (`cf_section` + `cf_line`)

Balance-sheet accounts only. Cash accounts themselves carry no `cf_line` — they are the
subject of the statement, not a line on it. Retained earnings carries none (rolls from
net income).

| cf_section | cf_line |
|---|---|
| Operating | Change in accounts receivable |
| Operating | Change in prepaid expenses |
| Operating | Change in other current assets |
| Operating | Change in accounts payable |
| Operating | Change in credit cards |
| Operating | Change in accrued payroll & benefits |
| Operating | Change in deferred revenue |
| Operating | Change in taxes payable |
| Operating | Change in other current liabilities |
| Operating | Depreciation & amortization add-back |
| Investing | Purchases of fixed assets |
| Investing | Capitalized software development |
| Investing | Proceeds from asset sales |
| Investing | Treasury & investment transfers |
| Investing | Deposits paid / returned |
| Financing | Equity issuance (stock, SAFEs, convertible notes) |
| Financing | Owner contributions |
| Financing | Owner draws & distributions |
| Financing | Debt proceeds & repayments (net) |

Debt is one *net* line by design: an account-level map classifies an account's net
balance change; splitting proceeds from repayments needs transaction-level data — a
deliverable's job, not the map's.

## Refresh workflow

1. Re-pull the full Account List (with QuickBooks account Ids).
2. Diff against the map on `gl_account_id`: update Group-1 columns in place; new accounts enter as `auto`/`needs-review` with rule-seeded mappings; disappeared accounts are marked inactive, never deleted.
3. The human works the `needs-review` queue → rows graduate to `confirmed`.
4. Stamp the CHANGELOG.

## Boundaries (what this file is and is not)

- **Account-level KPI definitions live here** — via tags, when a KPI is a sum over GL accounts. **Contract-level machinery does not** — cohort churn, waterfalls, per-customer MRR stay with Stripe / the planning model; where both exist, the contract-level source is authoritative and the tag-based figure is the P&L proxy.
- **Not the report outline.** Nesting orders live with the deliverable templates.
- **Not a notes file.** Judgment calls and tribal knowledge live in `finance-profile.md`.
