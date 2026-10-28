# Finance Brain: [PLACEHOLDER: company name]

This folder is the finance team's shared brain. It holds how the company does its accounting
(`handbook/`) and the recurring tasks Claude runs (`skills/`). Read this file first, then the
handbook pages a task needs, before doing any finance work here.

> **First time here?** If the Company at a glance section below is still mostly
> `[PLACEHOLDER` lines, the handbook isn't set up yet. Offer to run the `build-handbook` skill
> before anything else. A few open placeholders elsewhere are normal after setup; they're
> listed under Open questions.

## Company at a glance

Keep this section short. Detail lives in the handbook.

- **Company:** [PLACEHOLDER: legal name and what the company does, one line]
- **Entities:** [PLACEHOLDER: legal entities and their functional currency]
- **Fiscal year / basis:** [PLACEHOLDER: e.g. calendar year, accrual]
- **Accounting system:** [PLACEHOLDER: e.g. QuickBooks Online, NetSuite]
- **Close target:** [PLACEHOLDER: e.g. books closed by business day 8]
- **Materiality:** [PLACEHOLDER: e.g. explain any P&L line that moves more than $X or Y% month over month]
- **Finance owner:** [PLACEHOLDER: who owns the close and signs off]

## How to work in this folder

1. **Read before you work.** Before any task, read the handbook pages it touches. A JE reads
   `handbook/workpaper-standard.md`, `handbook/accounting-policies.md`, and
   `handbook/chart-of-accounts.md`. A rec reads `handbook/workpaper-standard.md` and
   `handbook/cash.md`. A report, metric, burn, or runway question reads
   `handbook/metrics-and-reporting.md`. If a page says something different from what the user just told you,
   ask which is right, then update the page.
2. **Read-only.** You may read connected systems. You never post, approve, pay, transfer, or
   edit records in them. You prepare workpapers and import files; a person posts.
3. **Placeholder, never guess.** If you don't know something, write
   `[PLACEHOLDER: what's needed and why it matters]` and list it under Open questions below.
   If the user doesn't know, record who does.
4. **Follow the workpaper standard.** Every JE and rec follows
   `handbook/workpaper-standard.md`: same tabs, same naming, the standard checks, and a
   sign-off block.
5. **Drafts go to `testing/` first.** A new or changed skill saves its output to `testing/`
   until a reviewer has compared it to a known-good result. Only then does it save to the real
   close folder.
6. **The author is never the approver.** Mark every workpaper "Prepared by Claude (run by
   [name])". Someone other than that person approves it.
7. **Fix the method, not the output.** If a reviewer finds a problem, change the skill or the
   handbook page so the same mistake can't happen next month. Note the change in the changelog
   below.

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
| `skills/build-handbook/` | Drafts the handbook from your docs and systems, then interviews you on the gaps |
| `skills/follow-up-interview/` | 30 minutes with whoever owns the numbers: metrics, plan, reporting, people |
| `skills/new-skill/` | Turns one task you know cold into a reusable skill |
| `skills/prepaid-amortization/` | Monthly prepaid amortization JE from the prepaid schedule |
| `skills/usage-accrual/` | Month-end accrual for usage-billed vendors not yet invoiced |
| `skills/bank-reconciliation/` | Bank rec: GL to statement, reconciling items, sign-off |
| `skills/build-handbook-site/` | Publishes `handbook/` as a browsable website |

Add a row whenever a new skill is created.

## Where outputs go

- **Drafts and tests:** `testing/`
- **Final workpapers:** [PLACEHOLDER: the close folder, e.g. "Finance/Close/YYYY-MM/JEs and Recs" in Google Drive]
- **File naming:** `{GL account number} - {account name} - {description} {YYYY.MM}.xlsx`

## Open questions

Gaps that need an owner. Move each one into the right handbook page once it's answered.

- [PLACEHOLDER: anything unresolved, with who can answer it]

## Changelog

Newest first. One line per change to the handbook or a skill.

- [PLACEHOLDER: YYYY-MM-DD: created from the airCFO Finance Brain Starter Kit]
