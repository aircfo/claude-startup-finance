---
name: finance-context-builder
description: Build the company's finance context — an airCFO Finance Context folder (default on the Desktop) holding a finance-profile.md semantic map that resolves how Stripe, Ramp, Mercury, and QuickBooks accounts relate. It first invites the finance pro to share any docs or notes about their business, then drafts an account map from the QuickBooks Account List for review. Use on first-time setup or to refresh, or when someone says "set up the finance plugin," "build my finance context," "build my finance profile," "map my accounts across systems," "add this to my finance context," or when another finance workflow can't find finance-profile.md.
---

# Finance Context Builder — build the company's finance context

Produce the **airCFO Finance Context**: a folder the finance pro can open anytime (default `~/Desktop/airCFO Finance Context/`) holding `finance-profile.md` (the semantic map), `account-map.csv` (how every account classifies), the source docs they've shared, and a changelog. Every other finance workflow reads the profile first, so Claude reasons across Stripe, Ramp, Mercury, and QuickBooks with one shared model — grounded in how *this* company actually reports.

## What this produces
An **airCFO Finance Context folder** (default `~/Desktop/airCFO Finance Context/`; confirm the location with the user on the first run):

```
~/Desktop/airCFO Finance Context/
├── finance-profile.md     # the semantic map (narrative + summary) — the main read
├── account-map.csv        # every GL account × its classification — the editable source of truth
├── context/               # source docs the pro shares (written here after they're ingested)
└── CHANGELOG.md           # dated log of what changed each run
```

Each finance workflow reads this profile at its own Step 0 — so it loads when finance work actually runs, not globally on every session. The profile binds three layers:
- **Business context (from the pro)** — what's true and unique about this company, captured from whatever docs and notes they share.
- **Reporting framework** — the account map (below).
- **Money-flow graph (discovered)** — how each Mercury account, Ramp clearing account, and Stripe payout/revenue stream maps onto a QuickBooks GL account.

`account-map.csv` is the canonical, spreadsheet-editable classification; `finance-profile.md` is the human-readable layer that **references** it — never duplicate the full per-account table in the profile.

## Principles
- **Draft, then confirm.** Build a *first draft* of the account map from the QuickBooks Account List, then have the human review it — never finalize a mapping without confirmation.
- **QuickBooks is the source of truth for the account list and the amounts.** The map decides how those accounts classify and roll up.
- **Read-only** against every connector.
- **The folder is the finance pro's.** Keep it human-readable and easy to open; never move or delete files in `context/` without asking.

## Build sequence

### 1 · Locate or create the airCFO Finance Context folder
On the first run, propose `~/Desktop/airCFO Finance Context/` and confirm it (let the user pick another spot); create it with the structure above. On later runs, use the existing folder.

### 2 · Gather the finance pro's context (in the session)
Before touching the numbers, invite the pro to tell you — **right here in the conversation** — what's important or unique about their business. They can paste it, attach a file, or just talk it through; *they* decide what matters. Offer a few examples to prompt them, but don't run a questionnaire:

> "Tell me what would help me understand your business — paste it here, attach a file, or just talk it through. A few ideas (include whatever *you* think matters):
> - your monthly reporting package, board deck, or KPI dashboard (the most useful single thing);
> - an SOP or two — your month-end close checklist, your revenue-recognition policy;
> - or a few sentences (a ramble is fine) on your revenue model, the metrics you live by, how you think about departments, or anything unusual about your books."

Read whatever they share, then **persist it**: save the source material (and a short distilled summary) into the `context/` subfolder, and fold the salient points into the profile's **Business context** section, citing the saved file. `context/` is a *record of what's been ingested* — the pro never has to manage it. If they share nothing, proceed; they can add context later just by telling you.

### 3 · Pull the QuickBooks Account List
Get company info (legal name, fiscal year, accounting basis, reporting currency) and run the **Account List** report / chart of accounts. For every account, capture: number, name, **Type**, **Detail Type**, the account **description** (if any), the **parent account** (`ParentRef` and the parent's name — needed for department inference), and balance. This is what the draft is built from.

### 4 · Draft the account map
Write one row per GL account to `account-map.csv` in the airCFO Finance Context folder. Columns: `account_number, account_name, account_type, detail_type, department, cf_section, cf_line, description`.

**Most columns come straight from QuickBooks — no judgment:**

- **`account_number`** + **`account_name`** — the QBO account number and name, exactly as QuickBooks has them (this pair is the key).
- **`account_type`** — the QuickBooks **Type** field, verbatim. P&L accounts: `Income`, `Cost of Goods Sold`, `Expense`, `Other Income`, `Other Expense`. Balance-sheet accounts: `Bank`, `Accounts Receivable`, `Other Current Asset`, `Fixed Asset`, `Other Asset`, `Accounts Payable`, `Credit Card`, `Other Current Liability`, `Long Term Liability`, `Equity`.
- **`detail_type`** — the QuickBooks **Detail Type** field, verbatim (e.g. `Checking`, `Savings`, `Service/Product Income`, `Cost of Sales`, `Payroll`, `Legal & Professional`).
- **`description`** — a short, plain-language note on what the account is for. Use the QuickBooks account description if it has one; otherwise write a one-liner.

The two remaining columns are the **reporting maps** — **`department`** for P&L accounts, **`cf_section` + `cf_line`** for balance-sheet accounts. Each account fills one or the other, never both.

**`department` — P&L accounts only** (leave blank for every balance-sheet account). The management-reporting grouping:

- **Income → `Revenue`.** Every income account is grouped as `Revenue` — whether the company runs a single revenue account or several revenue sub-accounts.
- **Cost of Goods Sold → `Cost of Goods Sold`.** All COGS accounts group together above the gross-margin line — never folded into an operating department.
- **Expense → an OpEx department.** Classify every operating-expense account to the team that owns it, working down this list and stopping at the first that fits (lean on the pro's context docs — their reporting package usually names the canonical departments):
  1. **In the account name** — a department after a dash / em-dash or an embedded keyword (e.g. "Salaries & Wages — Engineering" → `Engineering`).
  2. **Parent account** — if the account is a QBO sub-account, use its parent (header) account's name when that reads like a department or function (e.g. children of a "Marketing" parent → `Marketing`).
  3. **Judgment from what the account is for** — advertising, paid media, events, conferences, marketing agency, content, brand, website, demand gen → **Marketing**; sales commissions, CRM, sales tooling → **Sales**; cloud / infrastructure or engineering tooling booked as operating expense, R&D → **Engineering**; support / success tooling → **Customer Success**; rent, insurance, legal, audit, accounting, bank & merchant fees, office supplies, company-wide software → **G&A**.

  **G&A is a legitimate home** for genuinely general-and-administrative accounts — book those there. Leave `department` blank (and flag for review) only for an expense account that looks **irregular** or whose purpose you genuinely can't determine — don't force a guess, and don't use G&A as a catch-all.
- **Other Income / Other Expense → blank.** These sit below operating income, so they don't take a management department.

**`cf_section` + `cf_line` — balance-sheet accounts only** (leave blank for every P&L account). The cash-flow-statement mapping (indirect method): each account's period-over-period **change** feeds a cash-flow line. Mostly deterministic from the account type — the rows marked "—" stay blank:

| QuickBooks account type (detail type) | cf_section | cf_line |
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

The one judgment call to surface: a **treasury / investment** account QuickBooks lists as a current asset that you may instead treat as **Investing** (above).

### 5 · Review the draft with the human (the gate)
Present the account map, separated by confidence:
- **Straight from QuickBooks** (`account_type`, `detail_type`, the `Revenue` / `Cost of Goods Sold` department groupings, and the deterministic `cf_section` / `cf_line` defaults) — show for a quick confirm.
- **Needs review** — the **OpEx `department`** calls (briefly show how each was derived — name, parent account, or judgment — and surface anything you flagged as irregular or couldn't place); any **`cf_section`** judgment call (e.g. a treasury / investment account QuickBooks lists as a current asset that you may want under **Investing**); plus any `description` you wrote yourself and anything whose name fights its type.

Don't finalize until the human signs off. Save their corrections back to `account-map.csv`.

### 6 · Map the other systems onto the GL (money-flow graph)
For each connected system, bind its money containers to GL accounts (match on names, last-4, amounts; confirm anything low-confidence):
- **Mercury** — accounts (operating vs treasury, name, last-4, balance) → the QBO bank GL account each represents; mark which count as cash for runway.
- **Ramp** — the funding/clearing account → its QBO liability/clearing account; how spend categories roll up to expense accounts; the top recurring vendors.
- **Stripe** — the payout destination → which Mercury account → which GL account; how gross revenue, processing fees, and refunds book; the recognition method and treatment of annual prepays, coupons, and trials.

### 7 · Capture conventions
Pin: fiscal year, accounting basis (cash/accrual), reporting currency, the internal-transfer rule (excluded from burn), the treasury-vs-operating split, the materiality threshold, the MRR and revenue-recognition definitions, and the close cadence. Some of these may already be answered by the context docs from step 2 — don't re-ask what they already told you.

### 8 · Write the airCFO Finance Context
- Write `finance-profile.md` (schema below) and `account-map.csv` into the folder; make sure the docs the pro shared are saved in `context/`.
- Append a dated entry to `CHANGELOG.md` describing what changed.
- Record provenance: as-of date, connectors read, and the docs ingested.

## Updating & adding context over time
This skill is **build-or-refresh** — run it again anytime to refresh:
- **New context anytime** — the pro shares more in the session (or says *"add this to my finance context"*); ingest it, persist it to `context/`, fold it into the **Business context** section, and note it in the changelog.
- **Refresh the map** — re-pull the Account List and diff against `account-map.csv`: keep human-confirmed rows, draft only genuinely new accounts, and flag accounts that disappeared or changed type.
- **Always** append a dated `CHANGELOG.md` entry describing what changed, and update the profile's as-of date.

## The account map (schema)
`account-map.csv` lives in the airCFO Finance Context folder root (default `~/Desktop/airCFO Finance Context/account-map.csv`), one row per GL account, keyed on `account_number` + `account_name` (must match QuickBooks exactly). A blank-header template ships in the plugin's `templates/`.

`account_number, account_name, account_type, detail_type, department, cf_section, cf_line, description`

- `account_type` — the QuickBooks **Type** field, verbatim (P&L: Income / Cost of Goods Sold / Expense / Other Income / Other Expense; balance sheet: Bank / Accounts Receivable / Other Current Asset / Fixed Asset / Other Asset / Accounts Payable / Credit Card / Other Current Liability / Long Term Liability / Equity).
- `detail_type` — the QuickBooks **Detail Type** field, verbatim.
- `department` — **P&L accounts only** (blank for balance-sheet accounts): the management-reporting grouping — `Revenue` (income), `Cost of Goods Sold` (COGS), or an OpEx department (G&A, Engineering, Sales, Marketing, …); blank for Other Income / Other Expense.
- `cf_section` ∈ {Operating, Investing, Financing} and `cf_line` — **balance-sheet accounts only** (blank for P&L accounts, and blank for cash/bank and retained earnings): the indirect-method cash-flow line each account's period-over-period change feeds.
- `description` — a short, plain-language note on what the account is for.

## `finance-profile.md` schema
1. **Header** — company, as-of date, connectors read, docs ingested, accounting basis, fiscal year, currency.
2. **Business context** — what's true and unique about the company, distilled from the docs and notes the pro shared (reporting structure, KPI definitions, revenue model, departments, quirks). Cite the source file in `context/` for each point.
3. **Reporting framework** — points to `account-map.csv` and gives a coverage summary (X of Y accounts classified, the department breakdown, anything left blank/flagged). Do **not** duplicate the full per-account table here.
4. **Money-flow** — short narrative + table: Stripe → bank → GL, Ramp → clearing → GL, Mercury accounts → GL.
5. **Conventions** — the pinned definitions.
6. **Entity aliases** — customer (Stripe ↔ QBO) and vendor (Ramp ↔ QBO) matches, each with a confidence flag. Grows over time.
7. **Open questions** — unresolved or low-confidence items, each with a suggested next step.
8. **Provenance & changelog** — mirrors `CHANGELOG.md`.

## Never
- Never store secrets, tokens, or full account numbers — names, last-4, and internal IDs only.
- Never write to a connected system.
- Never finalize the account map or overwrite human-confirmed rows without confirmation.
- Never move or delete files the pro placed in `context/` without asking.
