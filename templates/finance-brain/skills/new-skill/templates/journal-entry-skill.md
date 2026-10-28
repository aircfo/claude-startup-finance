# Journal entry skill template

Copy everything in the block below into `skills/{name}/SKILL.md` (the folder name and `name`
must match: lowercase, hyphens) and fill it in. The workbook it produces follows
`handbook/workpaper-standard.md`.

```markdown
---
name: {name, matching the folder}
description: {What entry this prepares and when, in one or two sentences. Then the phrases someone would actually say, e.g. "Use when someone asks to book the monthly {X} entry, run the {X} accrual, or prepare the {X} JE for a close."}
---

# {Name of the entry}

**Purpose:** {What this entry records and why. When it runs in the close.}

**Period:** use the period the user named (YYYY-MM). Otherwise ask.

## Read first
- `handbook/workpaper-standard.md` (Journal entries)
- `handbook/accounting-policies.md`, section {name}
- `handbook/chart-of-accounts.md`
- {any other page}

## Inputs
| Input | Source | Notes |
| --- | --- | --- |
| {e.g. prepaid schedule} | {connected system and report, or export file name} | {date range, filters} |

## Steps
1. {Specific step.}
2. {Specific step.}

## Output
A workbook following `handbook/workpaper-standard.md`, named
`{GL} - {account} - {description} {YYYY.MM}.xlsx`, saved to {testing/ or the close folder}.

## Checks before handoff
The five standard JE checks, plus: {anything specific to this entry}.

## Never
- Never post the entry. A person posts it after approval.
- {Anything specific.}
```
