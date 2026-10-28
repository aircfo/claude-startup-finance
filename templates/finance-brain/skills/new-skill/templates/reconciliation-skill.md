# Reconciliation skill template

Copy everything in the block below into `skills/{name}/SKILL.md` (the folder name and `name`
must match: lowercase, hyphens) and fill it in. The workbook it produces follows
`handbook/workpaper-standard.md`.

```markdown
---
name: {name, matching the folder}
description: {Which account this reconciles and to what, in one or two sentences. Then the phrases someone would actually say, e.g. "Use when someone asks to reconcile {account}, tie {account} to its statement, or do the {account} rec for a close."}
---

# {Account} reconciliation

**Purpose:** {What this proves, and when it runs in the close.}

**Period:** use the period the user named (YYYY-MM). Otherwise ask.

## Read first
- `handbook/workpaper-standard.md` (Reconciliations)
- `handbook/cash.md` (or the page that describes this account)
- `handbook/close-process.md`

## Inputs
| Input | Source | Notes |
| --- | --- | --- |
| GL detail for {account} | {accounting system report} | {statement-period date range} |
| {Statement or schedule} | {connected system, or saved statement file} | {date range} |
| Last month's rec | {close folder} | for the rollforward |

## Steps
1. {Specific step.}

## Output
A workbook following `handbook/workpaper-standard.md`, saved to {testing/ or the close folder}.

## Checks before handoff
The five standard rec checks, plus: {anything specific}.

## Never
- Never mark items cleared in the accounting system or post a JE. Propose; a person books.
```
