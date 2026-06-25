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

Each finance workflow reads this profile at its own Step 0 — so it loads when finance work actually runs, not globally on every session. The profile follows the **14-section template** (schema below; a fill-in skeleton ships in `templates/finance-profile-template.md`) and is populated from three input layers:
- **Business context (from the pro)** — what's true and unique about this company, captured from whatever docs and notes they share.
- **Reporting framework** — the account map (below).
- **Money-flow graph (discovered)** — how each Mercury account, Ramp clearing account, and Stripe payout/revenue stream maps onto a QuickBooks GL account.

`account-map.csv` is the canonical, spreadsheet-editable classification; `finance-profile.md` is the human-readable layer that **references** it — never duplicate the full per-account table in the profile.

## Principles
- **Draft, then confirm.** Build a *first draft* of the account map from the QuickBooks Account List, then have the human review it — never finalize a mapping without confirmation.
- **Fill or placeholder — never guess.** Draft the profile from what you actually know (the context docs + the system analysis); mark every gap with an explicit `[PLACEHOLDER: …]` and surface it for the human — never invent a value to fill a section.
- **QuickBooks is the source of truth for the account list and the amounts.** The map decides how those accounts classify and roll up.
- **Read-only** against every connector.
- **The folder is the finance pro's.** Keep it human-readable and easy to open; never move or delete files in `context/` without asking.

## Build sequence

### 1 · Locate or create the airCFO Finance Context folder
On the first run, propose `~/Desktop/airCFO Finance Context/` and confirm it (let the user pick another spot); create it with the structure above. On later runs, use the existing folder.

**Then persist a lightweight pointer**, so future workflows can find the profile without loading it into every session. Write the machine-readable pointer to the current workspace (if writable), and offer to add a short note to the workspace `CLAUDE.md`:

- **`.aircfo-finance-context.json`** in the current workspace:

  ```json
  {
    "contextFolder": "/absolute/path/to/airCFO Finance Context",
    "financeProfile": "/absolute/path/to/airCFO Finance Context/finance-profile.md",
    "accountMap": "/absolute/path/to/airCFO Finance Context/account-map.csv",
    "lastUpdated": "YYYY-MM-DD"
  }
  ```

- **`CLAUDE.md` pointer — only with the user's OK.** Adding to `CLAUDE.md` changes their workspace instructions, so ask in plain English first:

  > "I can add a tiny pointer to this workspace's CLAUDE.md so future finance workflows know where your finance profile lives. I will not import the profile itself, so it will not load into every session."

  If they agree, add (or update) a bounded block so re-runs replace it instead of duplicating:

  ```md
  <!-- airCFO Finance Context:start -->
  airCFO Finance Context folder: /absolute/path/to/airCFO Finance Context
  airCFO finance profile: /absolute/path/to/airCFO Finance Context/finance-profile.md
  <!-- airCFO Finance Context:end -->
  ```

  If they decline, skip the `CLAUDE.md` write — the JSON pointer and the default folder still let workflows find the profile.

- **Never add an `@import` of the full profile** to `CLAUDE.md`. That would load the entire profile into every session — exactly what the pointer avoids.

Also drop a human-readable `LOCATION.md` inside the Finance Context folder noting its own path — a convenience for the user. Don't rely on it for discovery: workflows find the folder via the pointer or the default path, not this file.

### 2 · Connector preflight — see which systems are live
Before pulling any numbers, check which connectors are actually connected by running **one lightweight read against each** (read-only): QuickBooks (company info), Stripe (account/balance), Ramp (current user), Mercury (accounts). Detect connection status from what responds — **don't ask the user to list their systems.**

If a connector isn't authorized yet, that read surfaces the provider's normal browser sign-in. Set expectations up front: authorize the systems you use; for any you don't, decline and the connector is marked **Not connected** and its profile sections stay as explicit placeholders. **Never block setup on a missing connector.**

Show a short status table and the impact of anything missing:

| Connector | Status | Impact |
| --- | --- | --- |
| QuickBooks | Connected | I can draft the account map and reporting framework. |
| Stripe | Connected | I can map subscription/customer revenue rules. |
| Ramp | Not connected | Vendor/spend rules will stay placeholder. |
| Mercury | Connected | I can map cash accounts and runway cash. |

Then continue with the connected systems. Missing systems become explicit placeholders and open questions, not guesses. **QuickBooks is the backbone** — it owns the account list everything else maps onto — so if QuickBooks isn't connected, say so plainly and focus on what the other systems can still provide.

### 3 · Gather the finance pro's context (in the session)
Before touching the numbers, invite the pro to tell you — **right here in the conversation** — what's important or unique about their business. They can paste it, attach a file, or just talk it through; *they* decide what matters. Offer a few examples to prompt them, but don't run a questionnaire:

> "Tell me what would help me understand your business — paste it here, attach a file, or just talk it through. A few ideas (include whatever *you* think matters):
> - your monthly reporting package, board deck, or KPI dashboard (the most useful single thing);
> - an SOP or two — your month-end close checklist, your revenue-recognition policy;
> - or a few sentences (a ramble is fine) on your revenue model, the metrics you live by, how you think about departments, or anything unusual about your books."

Read whatever they share, then **persist it**: save the source material (and a short distilled summary) into the `context/` subfolder, and fold the salient points into the relevant profile sections (Business Model, KPI Definitions, the cash / revenue / spend / people rules, Known Exceptions), citing the saved file. `context/` is a *record of what's been ingested* — the pro never has to manage it. If they share nothing, proceed; they can add context later just by telling you.

### 4 · Pull the QuickBooks Account List
Get company info (legal name, fiscal year, accounting basis, reporting currency) and run the **Account List** report / chart of accounts. For every account, capture: number, name, **Type**, **Detail Type**, the account **description** (if any), the **parent account** (`ParentRef` and the parent's name — needed for department inference), and balance. This is what the draft is built from.

### 5 · Draft the account map
Write one row per GL account to `account-map.csv` in the airCFO Finance Context folder. Columns: `account_number, account_name, account_type, detail_type, reporting_group, cf_section, cf_line, description`.

**Most columns come straight from QuickBooks — no judgment:**

- **`account_number`** + **`account_name`** — the QBO account number and name, exactly as QuickBooks has them (this pair is the key).
- **`account_type`** — the QuickBooks **Type** field, verbatim. P&L accounts: `Income`, `Cost of Goods Sold`, `Expense`, `Other Income`, `Other Expense`. Balance-sheet accounts: `Bank`, `Accounts Receivable`, `Other Current Asset`, `Fixed Asset`, `Other Asset`, `Accounts Payable`, `Credit Card`, `Other Current Liability`, `Long Term Liability`, `Equity`.
- **`detail_type`** — the QuickBooks **Detail Type** field, verbatim (e.g. `Checking`, `Savings`, `Service/Product Income`, `Cost of Sales`, `Payroll`, `Legal & Professional`).
- **`description`** — a short, plain-language note on what the account is for. Use the QuickBooks account description if it has one; otherwise write a one-liner.

The two remaining columns are the **reporting maps** — **`reporting_group`** for P&L accounts, **`cf_section` + `cf_line`** for balance-sheet accounts. Each account fills one or the other, never both.

**`reporting_group` — P&L accounts only** (leave blank for every balance-sheet account). The management-reporting grouping:

- **Income → `Revenue`.** Every income account is grouped as `Revenue` — whether the company runs a single revenue account or several revenue sub-accounts.
- **Cost of Goods Sold → `Cost of Goods Sold`.** All COGS accounts group together above the gross-margin line — never folded into an operating department.
- **Expense → an OpEx department.** Classify every operating-expense account to the team that owns it, working down this list and stopping at the first that fits (lean on the pro's context docs — their reporting package usually names the canonical departments):
  1. **In the account name** — a department after a dash / em-dash or an embedded keyword (e.g. "Salaries & Wages — Engineering" → `Engineering`).
  2. **Parent account** — if the account is a QBO sub-account, use its parent (header) account's name when that reads like a department or function (e.g. children of a "Marketing" parent → `Marketing`).
  3. **Judgment from what the account is for** — advertising, paid media, events, conferences, marketing agency, content, brand, website, demand gen → **Marketing**; sales commissions, CRM, sales tooling → **Sales**; cloud / infrastructure or engineering tooling booked as operating expense, R&D → **Engineering**; support / success tooling → **Customer Success**; rent, insurance, legal, audit, accounting, bank & merchant fees, office supplies, company-wide software → **G&A**.

  **G&A is a legitimate home** for genuinely general-and-administrative accounts — book those there. Leave `reporting_group` blank (and flag for review) only for an expense account that looks **irregular** or whose purpose you genuinely can't determine — don't force a guess, and don't use G&A as a catch-all.
- **Other Income / Other Expense → blank.** These sit below operating income, so they don't take a reporting group.

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

### 6 · Review the draft with the human (the gate)
Present the account map, separated by confidence:
- **Straight from QuickBooks** (`account_type`, `detail_type`, the `Revenue` / `Cost of Goods Sold` groupings, and the deterministic `cf_section` / `cf_line` defaults) — show for a quick confirm.
- **Needs review** — the **OpEx `reporting_group`** calls (briefly show how each was derived — name, parent account, or judgment — and surface anything you flagged as irregular or couldn't place); any **`cf_section`** judgment call (e.g. a treasury / investment account QuickBooks lists as a current asset that you may want under **Investing**); plus any `description` you wrote yourself and anything whose name fights its type.

Don't finalize until the human signs off. Save their corrections back to `account-map.csv`.

### 7 · Map the other systems onto the GL (money-flow graph)
For each connected system, bind its money containers to GL accounts (match on names, last-4, amounts; confirm anything low-confidence):
- **Mercury** — accounts (operating vs treasury, name, last-4, balance) → the QBO bank GL account each represents; mark which count as cash for runway.
- **Ramp** — the funding/clearing account → its QBO liability/clearing account; how spend categories roll up to expense accounts; the top recurring vendors.
- **Stripe** — the payout destination → which Mercury account → which GL account; how gross revenue, processing fees, and refunds book; the recognition method and treatment of annual prepays, coupons, and trials.

### 8 · Capture conventions
Pin: fiscal year, accounting basis (cash/accrual), reporting currency, the internal-transfer rule (excluded from burn), the treasury-vs-operating split, the materiality threshold, the MRR and revenue-recognition definitions, and the close cadence. Some of these may already be answered by the context docs from step 3 — don't re-ask what they already told you.

### 9 · Draft the profile from the template (fill what you know, placeholder the rest)
Start from the **finance-profile template** (`templates/finance-profile-template.md`; the 14 sections are detailed under the schema below) and write a *first draft* of `finance-profile.md`. Fill every section you can from two sources: the **context docs** the pro shared (step 3) and the **system analysis** (steps 4–8 — the account map, the money-flow graph, and the pinned conventions).

Wherever you don't yet know something, **don't guess and don't silently drop the line** — leave an explicit placeholder so the gap is visible:

> `[PLACEHOLDER: <what's needed, and why it matters>]`

A section may come out fully filled, partly filled, or all placeholder — that's expected on a first run; the profile fills in over time.

### 10 · Surface the gaps and invite input (the gate before finalizing)
Show the pro **which sections still contain placeholders**, as a short checklist (section → what's missing). Then offer the choice — don't force it:

> "Here's your draft profile. These sections are still incomplete: [list]. Want to fill any in now? Paste it, point me at a doc, or just tell me — or we can finalize as-is and complete them later. Placeholders stay in the file, so nothing gets silently assumed."

Fold in whatever they give you, re-surface anything still open, and repeat until they're ready. Anything left unfilled is mirrored into **Open Questions** (§13) with a suggested next step, so the uncertainty stays visible.

### 11 · Finalize & write the airCFO Finance Context
- Write `finance-profile.md` and `account-map.csv` into the folder; make sure the docs the pro shared are saved in `context/`. Remaining placeholders stay in the file and are listed in Open Questions.
- Confirm the pointer is current: update `.aircfo-finance-context.json` (`lastUpdated`) and the `CLAUDE.md` block if one was added.
- Append a dated entry to `CHANGELOG.md` describing what changed and what's still open.
- Record provenance (§14): as-of date, connectors read, docs ingested, and which sections remain placeholder.

## Updating & adding context over time
This skill is **build-or-refresh** — run it again anytime to refresh:
- **New context anytime** — the pro shares more in the session (or says *"add this to my finance context"*); ingest it, persist it to `context/`, fold it into the relevant profile sections (**replacing any matching placeholders**), and note it in the changelog.
- **Refresh the map** — re-pull the Account List and diff against `account-map.csv`: keep human-confirmed rows, draft only genuinely new accounts, and flag accounts that disappeared or changed type.
- **Always** append a dated `CHANGELOG.md` entry describing what changed, and update the profile's as-of date and the pointer's `lastUpdated`.

## The account map (schema)
`account-map.csv` lives in the airCFO Finance Context folder root (default `~/Desktop/airCFO Finance Context/account-map.csv`), one row per GL account, keyed on `account_number` + `account_name` (must match QuickBooks exactly). A blank-header template ships in the plugin's `templates/`.

`account_number, account_name, account_type, detail_type, reporting_group, cf_section, cf_line, description`

- `account_type` — the QuickBooks **Type** field, verbatim (P&L: Income / Cost of Goods Sold / Expense / Other Income / Other Expense; balance sheet: Bank / Accounts Receivable / Other Current Asset / Fixed Asset / Other Asset / Accounts Payable / Credit Card / Other Current Liability / Long Term Liability / Equity).
- `detail_type` — the QuickBooks **Detail Type** field, verbatim.
- `reporting_group` — **P&L accounts only** (blank for balance-sheet accounts): the management-reporting grouping — `Revenue` (income), `Cost of Goods Sold` (COGS), or an OpEx department (G&A, Engineering, Sales, Marketing, …); blank for Other Income / Other Expense.
- `cf_section` ∈ {Operating, Investing, Financing} and `cf_line` — **balance-sheet accounts only** (blank for P&L accounts, and blank for cash/bank and retained earnings): the indirect-method cash-flow line each account's period-over-period change feeds.
- `description` — a short, plain-language note on what the account is for.

## `finance-profile.md` schema
`finance-profile.md` is a **semantic control file, not a data dump** — it holds definitions, mappings, conventions, and judgment calls so every workflow reasons with the same financial brain. It *references* `account-map.csv` (never duplicates it). A fill-in skeleton ships in `templates/finance-profile-template.md`; draft from it, filling what you know and placeholdering the rest (steps 9–11). The 14 sections:

1. **Company Snapshot** — legal name, fiscal year, accounting basis (cash/accrual), reporting currency, current stage, primary business model, as-of date, connected systems read.
2. **Business Model** — plain-English how the company makes money (subscription / services / usage / marketplace / hardware / transaction fees / hybrid) and the main operating drivers (customers, units, headcount, usage, gross margin, sales cycle, seasonality).
3. **KPI Definitions** — the company's canonical definition for every metric it lives by ("when we say X, here's exactly how we calculate it"): e.g. revenue, bookings, billings, gross / contribution margin, gross / net burn, runway, CAC, LTV, active customers, retention, utilization, pipeline, ARR / MRR — whichever apply.
4. **Source-of-Truth Map** — which system owns which number (e.g. cash → Mercury, recognized revenue → QBO, subscription detail → Stripe, card/vendor spend → Ramp, payroll/headcount → payroll system or user-provided roster, forecast → planning tool), and which sources are authoritative vs. directional.
5. **Chart of Accounts / Reporting Framework** — points to `account-map.csv` (no full table): P&L categories, departments / cost centers, balance-sheet groups, cash-flow classifications, accounts needing review, and accounts intentionally excluded from certain metrics.
6. **Cash, Burn, and Runway Rules** — which bank accounts count as cash; whether treasury/investment counts as runway cash; gross-burn and net-burn definitions; internal-transfer exclusions; treatment of financing inflows; default lookback window; trailing-average vs. current run-rate.
7. **Revenue and Collections Rules** — how revenue is recognized; how collections differ from revenue; refund / credit treatment; deferred revenue; non-core revenue; AR / collections conventions; customer aliases across systems.
8. **Spend, AP, and Vendor Rules** — vendor aliases across Ramp / QBO; recurring-vendor list; one-time vs. recurring; card vs. bills vs. payroll; capitalization rules (if any); excluded / non-operating spend.
9. **People and Payroll Model** — headcount source of truth; departments; loaded-payroll assumptions; contractor treatment; commissions / bonuses; hiring-plan source.
10. **Planning and Forecast Assumptions** — current budget / forecast source; approved hiring plan; revenue-forecast logic; major planned investments; fundraising assumptions; board-approved plan vs. latest estimate.
11. **Reporting Cadence and Materiality** — monthly close cadence; board / investor cadence; materiality threshold; variance-explanation threshold; preferred output style.
12. **Known Exceptions and Judgment Calls** — the "don't rediscover this every time" list (e.g. "this savings account counts as runway cash"; "this vendor maps to COGS, not G&A"; "Stripe dashboard MRR ≠ board MRR because of trials/prepaids"; "this legal bill is one-time, exclude from run-rate burn").
13. **Open Questions** — anything unresolved, each with a suggested next step (this is where unfilled placeholders land, so uncertainty stays visible).
14. **Provenance and Changelog** — last updated, systems read, docs ingested, what changed, what still needs confirmation.

## Never
- Never store secrets, tokens, or full account numbers — names, last-4, and internal IDs only.
- Never write to a connected system.
- Never add an `@import` of the full profile to `CLAUDE.md` (or write the `CLAUDE.md` pointer without the user's OK).
- Never finalize the account map or overwrite human-confirmed rows without confirmation.
- Never move or delete files the pro placed in `context/` without asking.
