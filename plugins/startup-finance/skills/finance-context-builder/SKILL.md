---
name: finance-context-builder
description: Build the company's finance semantic map — a persistent profile that resolves how Stripe, Ramp, Mercury, and QuickBooks accounts relate. It drafts the P&L and balance-sheet maps automatically from the QuickBooks Account List, then has you review them. Use on first-time setup, or when someone says "set up the finance plugin," "onboard my company," "build my finance profile," "map my accounts across systems," "create the semantic layer," or when another finance workflow can't find finance-profile.md.
---

# Finance Context Builder — build the company semantic map

Produce `finance-profile.md`: the single map every other finance workflow reads first, so Claude reasons across Stripe, Ramp, Mercury, and QuickBooks with one shared model instead of re-deriving the topology every conversation.

## What this produces
`finance-profile.md` at the working-directory root, plus an `@finance-profile.md` reference in `CLAUDE.md` so it loads in every session. The profile binds two layers:

- **Reporting framework** — two maps that turn the raw general ledger into management financials:
  - **P&L map** — every income-statement account → its `class` (Revenue / COGS / Expense / Other Income / Other Expense) and `department`.
  - **Balance-sheet map** — every balance-sheet account → its `bs_group` (Current Assets / Non-current Assets / Current Liabilities / Non-current Liabilities / Equity), and its cash-flow `cf_section` (Operating / Investing / Financing) and `cf_line`.
- **Money-flow graph (discovered)** — how each Mercury account, Ramp clearing account, and Stripe payout/revenue stream maps onto a QuickBooks GL account.

Together: any transaction → GL account → its statement classification and dimensions.

## Principles
- **Draft, then confirm.** This skill builds a *first draft* of both maps from the QuickBooks Account List, then has the human review it — it never finalizes a mapping without confirmation.
- **QuickBooks is the source of truth for the account list and the amounts.** The maps decide how those accounts classify and roll up.
- **Read-only** against every connector.

## Build sequence

### 1 · Detect connected systems
Check which of QuickBooks, Mercury, Ramp, and Stripe are authenticated. QuickBooks is required to draft the maps — if it isn't connected, stop and ask the user to connect it (it's the canonical chart of accounts).

### 2 · Pull the QuickBooks Account List
Get company info (legal name, fiscal year, accounting basis, reporting currency) and run the **Account List** report / chart of accounts. For every account, capture: number, name, **AccountType**, **DetailType (subtype)**, the **parent account** (`ParentRef` and the parent's name — needed for department inference), and balance. This is what the draft is built from.

### 3 · Draft the P&L map
For every account whose type is an income-statement type, write a row to `finance/mappings/pnl-mapping.csv`:

- **`class`** — deterministic, from the QuickBooks AccountType:

  | QuickBooks AccountType | class |
  | --- | --- |
  | Income | Revenue |
  | Cost of Goods Sold | COGS |
  | Expense | Expense |
  | Other Income | Other Income |
  | Other Expense | Other Expense |

- **`department`** — make a judgment call and classify every account you reasonably can, working down this list and stopping at the first that fits:
  1. **In the account name** — a department after a dash / em-dash or an embedded keyword (e.g. "Salaries & Wages — Engineering" → `Engineering`).
  2. **Parent account** — if the account is a QBO sub-account, use its parent (header) account's name when that reads like a department or function (e.g. children of a "Marketing" parent → `Marketing`).
  3. **Judgment from what the account is for** — assign the owning team from the account's purpose. For example: advertising, paid media, events, conferences, marketing agency, content, brand, website, demand gen → **Marketing**; sales commissions, CRM, sales tooling → **Sales**; hosting, cloud / infrastructure, engineering tools, R&D → **Engineering**; support / success tooling → **Customer Success**; rent, insurance, legal, audit, accounting, bank & merchant fees, office supplies, company-wide software → **G&A**.

  **G&A is a legitimate home** for genuinely general-and-administrative accounts — book those there. The only accounts to leave blank (and flag for review) are ones that look **irregular** or whose purpose you genuinely can't determine — don't force a guess there, and don't use G&A as a catch-all for accounts you simply couldn't place.

### 4 · Draft the balance-sheet map
For every balance-sheet account, write a row to `finance/mappings/balance-sheet-mapping.csv`:

- **`bs_group`** — deterministic, from the QuickBooks AccountType:

  | QuickBooks AccountType | bs_group |
  | --- | --- |
  | Bank | Current Assets |
  | Accounts Receivable | Current Assets |
  | Other Current Asset | Current Assets |
  | Fixed Asset | Non-current Assets |
  | Other Asset | Non-current Assets |
  | Accounts Payable | Current Liabilities |
  | Credit Card | Current Liabilities |
  | Other Current Liability | Current Liabilities |
  | Long Term Liability | Non-current Liabilities |
  | Equity | Equity |

- **`cf_section`** + **`cf_line`** — from the indirect-method defaults. Every balance-sheet account still gets a `bs_group`; the rows marked "—" simply get a **blank** `cf_section`/`cf_line`:

  | QuickBooks AccountType (DetailType) | cf_section | cf_line |
  | --- | --- | --- |
  | Bank / cash on hand | — *(blank: this is the ending cash)* | — |
  | Accounts Receivable | Operating | Change in accounts receivable |
  | Other Current Asset — prepaids | Operating | Change in other current assets |
  | Other Current / Other Asset — investments, treasury | Investing | Treasury / investments |
  | Fixed Asset | Investing | Capital expenditures |
  | Accounts Payable | Operating | Change in accounts payable |
  | Credit Card | Operating | Change in credit card payable |
  | Other Current Liability — deferred revenue / accrued / payroll / sales tax | Operating | Change in *(that liability)* |
  | Long Term Liability | Financing | Debt proceeds / (repayments) |
  | Equity — common / preferred / APIC | Financing | Equity issuance |
  | Equity — retained earnings / accumulated deficit | — *(blank: rolls from net income)* | — |

### 5 · Review the drafts with the human (the gate)
Present both drafts, separated by confidence:
- **Deterministic** (class and `bs_group` from AccountType; AR / AP / deferred-revenue → Operating) — show for a quick confirm.
- **Heuristic — needs review**: the `department` calls (briefly show how each was derived — name, parent account, or judgment — and surface anything you flagged as irregular or couldn't place), plus the judgment calls — a treasury / investment account that QuickBooks lists as a current asset but that you may want under **Non-current Assets** and **Investing**, contra accounts, and anything whose name fights its type.

Don't finalize until the human signs off. Save their corrections back to the two CSVs.

### 6 · Map the other systems onto the GL (money-flow graph)
For each connected system, bind its money containers to GL accounts (match on names, last-4, amounts; confirm anything low-confidence):
- **Mercury** — accounts (operating vs treasury, name, last-4, balance) → the QBO bank GL account each represents; mark which count as cash for runway.
- **Ramp** — the funding/clearing account → its QBO liability/clearing account; how spend categories roll up to expense accounts; the top recurring vendors.
- **Stripe** — the payout destination → which Mercury account → which GL account; how gross revenue, processing fees, and refunds book; the recognition method and treatment of annual prepays, coupons, and trials.

### 7 · Capture conventions
Pin: fiscal year, accounting basis (cash/accrual), reporting currency, the internal-transfer rule (excluded from burn), the treasury-vs-operating split, the materiality threshold, the MRR and revenue-recognition definitions, and the close cadence.

### 8 · Write
On confirmation, write `finance-profile.md` (schema below) and add `@finance-profile.md` to `CLAUDE.md` (create it if absent; never duplicate the line). Record provenance: as-of date, connectors read, and a changelog entry.

## Re-running (refresh)
A re-run re-pulls the Account List and diffs against the saved maps: it **keeps human-confirmed rows**, drafts only genuinely new accounts, and flags accounts that disappeared or changed type. New accounts are marked "needs review."

## The maps (schema)
Both live in `finance/mappings/`, keyed on `account_number` + `account_name` (must match QuickBooks exactly). Blank-header templates ship in the plugin's `templates/`.
- `pnl-mapping.csv` — `account_number, account_name, class, department`
- `balance-sheet-mapping.csv` — `account_number, account_name, bs_group, cf_section, cf_line`

`class` ∈ {Revenue, COGS, Expense, Other Income, Other Expense}. `bs_group` ∈ {Current Assets, Non-current Assets, Current Liabilities, Non-current Liabilities, Equity}. `cf_section` ∈ {Operating, Investing, Financing}.

## `finance-profile.md` schema
1. **Header** — company, as-of date, connectors read, accounting basis, fiscal year, currency.
2. **Reporting framework** — where the two maps live + a coverage summary (X of Y accounts classified; how many departments still blank).
3. **Account map** — master table: GL account | type | class | department | bs_group | cf_section | cf_line | also-appears-as (Mercury / Ramp / Stripe).
4. **Money-flow** — short narrative + table: Stripe → bank → GL, Ramp → clearing → GL, Mercury accounts → GL.
5. **Conventions** — the pinned definitions.
6. **Entity aliases** — customer (Stripe ↔ QBO) and vendor (Ramp ↔ QBO) matches, each with a confidence flag. Grows over time.
7. **Open questions** — unresolved or low-confidence items, each with a suggested next step.
8. **Provenance & changelog**.

## Never
- Never store secrets, tokens, or full account numbers — names, last-4, and internal IDs only.
- Never write to a connected system.
- Never finalize the draft maps or overwrite human-confirmed rows without confirmation.
