# Finance Brain: Honestly Just Spreadsheets, Inc.

This folder is the finance team's shared brain. It holds how the company does its accounting
(`handbook/`) and the recurring tasks Claude runs (`skills/`). Read this file first, then the
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

1. **Read before you work.** Before any task, read the handbook pages it touches. A JE or rec reads `handbook/workpaper-standard.md`. A report, metric, burn, or runway question reads `handbook/metrics-and-reporting.md`.
2. **Read-only.** Read connected systems. Never post, approve, pay, transfer, or edit records.
3. **Placeholder, never guess.** Mark unknowns `[PLACEHOLDER: ...]` and list them below.
4. **Follow the workpaper standard** in `handbook/workpaper-standard.md`.
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
| JE and rec workpaper standard: tabs, naming, checks, sign-off | `handbook/workpaper-standard.md` |
| How skills work and how to add one | `skills/README.md` |

## Skills

Each skill is a folder in `skills/` with a `SKILL.md` that says how to do one recurring task.
When the user asks for one of these tasks, or names a skill, read its `SKILL.md` and follow it.

| Skill | What it does |
| --- | --- |
| `skills/setup-finance-brain/` | Sets up and refreshes this handbook: interview, follow-up with whoever owns the numbers, publishing it as a website |
| `skills/new-skill/` | Turns one task you know cold into a reusable skill |
| `skills/prepaid-amortization/` | Monthly prepaid amortization JE from the prepaid schedule |
| `skills/usage-accrual/` | Month-end accrual for Stratus Cloud and Lattice Inference usage |
| `skills/bank-reconciliation/` | Mercury operating, Mercury treasury, and Ramp card recs |
| `skills/level-up/` | Coaches the team up the AI-in-finance ladder, including the GitHub and Claude Code setup |

## Level-up progress

- **Rung:** 3, shared context and workflows. One handbook and one set of skills for the team.
- **Last step:** 2026-10-15, follow-up interview done with the CEO and Head of Finance.
- **Next step:** Head of Finance (champion) runs the GitHub and Claude Code setup in the
  `level-up` skill, then onboards the accounting firm's lead.
- **Wins:**
  - 2026-10: usage accrual skill, about 2 hours to 25 minutes, two clean months in review.
  - 2026-09: bank recs for three accounts, prepared before BD3 instead of BD5.

## Where outputs go

- **Drafts and tests:** `testing/`
- **Final workpapers:** Google Drive, `Finance/Close/YYYY-MM/` with `JEs/` and `Recs/` subfolders
- **File naming:** `{GL account number} - {account name} - {description} {YYYY.MM}.xlsx`

## Open questions

- [PLACEHOLDER: Stock-based compensation booking cadence: monthly or quarterly? Owner: Head of Finance.]
- [PLACEHOLDER: Capitalize the 2026 website rebuild, or expense it? Owner: Head of Finance, with the outside accountants.]

## Changelog

- 2026-10-15: Metrics and reporting page filled in from a follow-up interview with the CEO and Head of Finance.
- 2026-10-15: usage-accrual skill graduated from `testing/` after two clean months (approved by Head of Finance).
- 2026-09-30: Added Lattice Inference to the usage accrual. Product launched AI features in September.
- 2026-09-02: Handbook built with the `setup-finance-brain` skill. 9 placeholders open.
