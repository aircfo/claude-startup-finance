# Finance Profile — <Company>

<!--
The airCFO finance-profile.md is a SEMANTIC CONTROL FILE, not a data dump. It holds
definitions, mappings, conventions, and judgment calls so every finance workflow reasons
with the same financial brain. The finance-context-builder skill drafts it from (a) the
context docs you share and (b) a read-only pass over your connected systems — filling what
it can and leaving a [PLACEHOLDER: …] wherever it doesn't yet know, so gaps stay visible
instead of becoming silent guesses. Replace each placeholder as the information arrives;
references account-map.csv for the per-account detail, never duplicates it.
-->

## 1 · Company Snapshot
- **Legal / company name:** [PLACEHOLDER: registered entity name]
- **Fiscal year:** [PLACEHOLDER: e.g. calendar Jan–Dec]
- **Accounting basis:** [PLACEHOLDER: cash or accrual]
- **Reporting currency:** [PLACEHOLDER: e.g. USD]
- **Current stage:** [PLACEHOLDER: e.g. Seed / Series A]
- **Primary business model:** [PLACEHOLDER: one line]
- **As-of date:** [PLACEHOLDER: date this profile reflects]
- **Connected systems read:** [PLACEHOLDER: e.g. QuickBooks, Stripe, Ramp, Mercury, plus any payroll/headcount source you connect separately]

## 2 · Business Model
*Plain-English: how the company makes money, and the main operating drivers.*
- **How we make money:** [PLACEHOLDER: subscription / services / usage-based / marketplace / hardware / transaction fees / hybrid — describe]
- **Operating drivers:** [PLACEHOLDER: customers, units, headcount, usage, gross margin, sales cycle, seasonality, …]

## 3 · KPI Definitions
*The canonical definition for each metric we live by — "when we say X, here is exactly how we calculate it." Include only what applies to this business.*
- **<metric>:** [PLACEHOLDER: exact definition + formula]
- *Candidates: revenue, bookings, billings, gross / contribution margin, gross / net burn, runway, CAC, LTV, active customers, retention, utilization, pipeline, ARR / MRR.*

## 4 · Source-of-Truth Map
*Which system owns which number — and whether it's authoritative or only directional.*

| Number | System of record | Authoritative / directional |
| --- | --- | --- |
| Cash balances | [PLACEHOLDER] | [PLACEHOLDER] |
| Recognized revenue | [PLACEHOLDER] | [PLACEHOLDER] |
| Customer / subscription detail | [PLACEHOLDER] | [PLACEHOLDER] |
| Card / vendor spend | [PLACEHOLDER] | [PLACEHOLDER] |
| Payroll / headcount | [PLACEHOLDER] | [PLACEHOLDER] |
| Forecast / budget | [PLACEHOLDER] | [PLACEHOLDER] |

## 5 · Chart of Accounts / Reporting Framework
*Points to `account-map.csv` — do not duplicate the table.*
- **P&L categories:** [PLACEHOLDER: revenue / COGS / OpEx structure]
- **Departments / cost centers:** [PLACEHOLDER]
- **Balance-sheet groups:** [PLACEHOLDER]
- **Cash-flow classifications:** see `account-map.csv` (`cf_section` / `cf_line`)
- **Accounts needing review:** [PLACEHOLDER]
- **Accounts excluded from certain metrics:** [PLACEHOLDER]

## 6 · Cash, Burn, and Runway Rules
- **Which accounts count as cash:** [PLACEHOLDER]
- **Does treasury / investment count as runway cash?:** [PLACEHOLDER: yes/no + which accounts]
- **Gross burn:** [PLACEHOLDER: definition]
- **Net burn:** [PLACEHOLDER: definition]
- **Internal-transfer exclusions:** [PLACEHOLDER]
- **Financing inflows:** [PLACEHOLDER: how treated]
- **Default lookback window:** [PLACEHOLDER: e.g. trailing 3 full months]
- **Trailing average vs. current run-rate:** [PLACEHOLDER: when to use each]

## 7 · Revenue and Collections Rules
- **Revenue recognition:** [PLACEHOLDER]
- **Collections vs. revenue:** [PLACEHOLDER: how cash-in differs from recognized]
- **Refunds / credits:** [PLACEHOLDER]
- **Deferred revenue:** [PLACEHOLDER]
- **Non-core revenue:** [PLACEHOLDER]
- **AR / collections conventions:** [PLACEHOLDER]
- **Customer aliases across systems:** [PLACEHOLDER]

## 8 · Spend, AP, and Vendor Rules
- **Vendor aliases (Ramp / QBO / …):** [PLACEHOLDER]
- **Recurring vendors:** [PLACEHOLDER]
- **One-time vs. recurring treatment:** [PLACEHOLDER]
- **Card spend vs. bills vs. payroll:** [PLACEHOLDER]
- **Capitalization rules:** [PLACEHOLDER: if any]
- **Excluded / non-operating spend:** [PLACEHOLDER]

## 9 · People and Payroll Model
- **Headcount source of truth:** [PLACEHOLDER]
- **Departments:** [PLACEHOLDER]
- **Loaded-payroll assumptions:** [PLACEHOLDER: burden %, what's included]
- **Contractor treatment:** [PLACEHOLDER]
- **Commissions / bonuses:** [PLACEHOLDER]
- **Hiring-plan source:** [PLACEHOLDER: if available]

## 10 · Planning and Forecast Assumptions
- **Current budget / forecast source:** [PLACEHOLDER]
- **Approved hiring plan:** [PLACEHOLDER]
- **Revenue forecast logic:** [PLACEHOLDER]
- **Major planned investments:** [PLACEHOLDER]
- **Fundraising assumptions:** [PLACEHOLDER]
- **Board-approved plan vs. latest estimate:** [PLACEHOLDER]

## 11 · Reporting Cadence and Materiality
- **Monthly close cadence:** [PLACEHOLDER]
- **Board reporting cadence:** [PLACEHOLDER]
- **Investor update cadence:** [PLACEHOLDER]
- **Materiality threshold:** [PLACEHOLDER]
- **Variance-explanation threshold:** [PLACEHOLDER]
- **Preferred output style:** [PLACEHOLDER]

## 12 · Known Exceptions and Judgment Calls
*"Don't rediscover this every time." One line per call.*
- [PLACEHOLDER: e.g. "Mercury Savings ••5737 is a savings account but counts as runway cash"]
- [PLACEHOLDER: e.g. "Vendor X maps to COGS, not G&A"]

## 13 · Open Questions
*Unresolved items — each with a suggested next step. Unfilled placeholders land here so uncertainty stays visible instead of becoming a silent assumption.*
- [PLACEHOLDER: question → suggested next step]

## 14 · Provenance and Changelog
- **Last updated:** [PLACEHOLDER: date]
- **Systems read:** [PLACEHOLDER]
- **Docs ingested:** [PLACEHOLDER: files in context/]
- **What changed:** [PLACEHOLDER]
- **Still needs confirmation:** [PLACEHOLDER: which sections remain placeholder]
