# Finance Brain: Honestly Just Spreadsheets, Inc.

This folder is the finance team's shared brain. It holds how the company does its accounting
(`handbook/`) and the recurring tasks Claude runs (`commands/`). Read this file first, then the
handbook pages a task needs, before doing any finance work here.

> **Sample.** Honestly Just Spreadsheets, Inc. is a fictional company. Every name, number, and
> policy here is synthetic, written to show what a filled-in handbook looks like. Your policies
> are yours to set.

## Company at a glance

- **Company:** Honestly Just Spreadsheets, Inc. Makes Honestly, per-seat software for finance teams that live in spreadsheets.
- **Entities:** One. Honestly Just Spreadsheets, Inc. (Delaware), USD.
- **Fiscal year / basis:** Calendar year, accrual.
- **Accounting system:** QuickBooks Online.
- **Close target:** Books closed by business day 8.
- **Materiality:** Explain any P&L line that moves more than $5,000 and 10% month over month.
- **Finance owner:** Head of Finance. Day-to-day bookkeeping by an outsourced accounting firm.

## How to work in this folder

1. **Read before you work.** Before any task, read the handbook pages it touches. A report, metric, burn, or runway question reads `handbook/metrics-and-reporting.md`.
2. **Read-only.** Read connected systems. Never post, approve, pay, transfer, or edit records.
3. **Placeholder, never guess.** Mark unknowns `[PLACEHOLDER: ...]` and list them below.
4. **Follow the workpaper standard** in `commands/_templates/`.
5. **Drafts go to `testing/` first.**
6. **The author is never the approver.**
7. **Fix the method, not the output.**

## Map: where to find more detail

| Topic | File |
| --- | --- |
| Entities, business model, systems, who approves what | `handbook/company-overview.md` |
| Account structure, numbering, reporting rollups | `handbook/chart-of-accounts.md` |
| Capitalization, prepaids, accruals, revenue, other policies | `handbook/accounting-policies.md` |
| Close calendar, checklist, flux thresholds, sign-off | `handbook/close-process.md` |
| Bank and card accounts, what counts as cash, transfers | `handbook/cash.md` |
| Metric definitions, burn and runway, plan, who reads the numbers | `handbook/metrics-and-reporting.md` |
| What Claude can read, and the clean-inputs checklist | `handbook/systems-and-data.md` |

## Commands

| Command | What it does |
| --- | --- |
| `commands/setup/build-handbook.md` | Drafts the handbook from docs and systems, then interviews on the gaps |
| `commands/setup/follow-up-interview.md` | 30 minutes with whoever owns the numbers: metrics, plan, reporting, people |
| `commands/setup/new-command.md` | Turns one task you know cold into a reusable command |
| `commands/jes/prepaid-amortization.md` | Monthly prepaid amortization JE from the prepaid schedule |
| `commands/jes/usage-accrual.md` | Month-end accrual for Stratus Cloud and Lattice Inference usage |
| `commands/recs/bank-reconciliation.md` | Mercury operating, Mercury treasury, and Ramp card recs |
| `commands/publish/build-handbook-site.md` | Publishes this handbook as a website |

## Where outputs go

- **Drafts and tests:** `testing/`
- **Final workpapers:** Google Drive, `Finance/Close/YYYY-MM/` with `JEs/` and `Recs/` subfolders
- **File naming:** `{GL account number} - {account name} - {description} {YYYY.MM}.xlsx`

## Open questions

- [PLACEHOLDER: Stock-based compensation booking cadence: monthly or quarterly? Owner: Head of Finance.]
- [PLACEHOLDER: Capitalize the 2026 website rebuild, or expense it? Owner: Head of Finance, with the outside accountants.]

## Changelog

- 2026-10-15: Metrics and reporting page filled in from a follow-up interview with the CEO and Head of Finance.
- 2026-10-15: usage-accrual command graduated from `testing/` after two clean months (approved by Head of Finance).
- 2026-09-30: Added Lattice Inference to the usage accrual. Product launched AI features in September.
- 2026-09-02: Handbook built with `commands/setup/build-handbook.md`. 9 placeholders open.
