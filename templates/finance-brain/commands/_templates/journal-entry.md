---
description: The journal entry workpaper standard, plus a skeleton to copy when writing a new JE command.
argument-hint: "(template, not run directly)"
---

# Journal entry: workpaper standard and command template

Every JE command in this folder produces a workpaper that looks like this. A reviewer should be
able to open any JE workpaper, from any month, and know where to look.

See `examples/workpapers/` for a finished example built on synthetic data.

## The workbook

**File name:** `{GL account number} - {account name} - {description} {YYYY.MM}.xlsx`
For example: `2101 - Accrued Expenses - Usage Accrual 2026.09.xlsx`

**Tabs, in this order:**

| Tab | What's on it |
| --- | --- |
| **Summary** | Purpose, period, the handbook policy it follows, where each input came from (system and report, or export file name, with date range), the result in one sentence, and the sign-off block. |
| **Source Data** | The raw inputs exactly as pulled or exported. Never edited. |
| **Calculation** | The math, as live formulas that reference Source Data. Every assumption (a rate, a threshold, a useful life) in its own labeled cell, with where it came from. |
| **JE** | The entry: post date, reversal date (if any), account, debit, credit, memo, department or class. Totals row. A balance check that reads BALANCED or OUT OF BALANCE. |
| **Prior Period** (optional) | Last month's entry beside this month's, with the change explained if it's material. |

**Rules for the workbook:**

- Formulas, never hardcoded results. If the source data changes, the JE changes.
- Debits equal credits, and the balance check is a formula, not a typed word.
- Accounts must exist in the chart of accounts. Never invent one.
- Memo format: `{description} - {vendor or contract} - {YYYY.MM}`.
- Blue text for inputs, black for formulas.
- Sign-off block at the bottom of the Summary tab:

  > Prepared by: Claude (run by [name]) on [date]
  > Reviewed and approved by: ______________ Date: ________
  > Requires approval by someone other than the preparer, per `handbook/company-overview.md`.

**Optional import file:** if the accounting system accepts a journal entry import, also save a
CSV in its import format beside the workbook. A person imports it after approval. Claude never
posts.

**Save to:** `testing/` while the command is new or changed. After it has passed review, the
close folder named in `CLAUDE.md`.

## Checks before handoff

Every JE command ends with these, shown to the user as a short table:

1. **Balanced:** total debits equal total credits.
2. **Ties to source:** the Calculation total equals the JE amount.
3. **Ties to the schedule or balance:** for entries that roll a balance (prepaids, accruals,
   deferred revenue), opening + additions - releases = closing, and closing matches what the GL
   will show after the entry.
4. **Reasonable vs. last month:** if the amount moved more than the flux threshold in
   `handbook/close-process.md`, explain why.
5. **Accounts valid:** every account exists and is active.

If any check fails, say so plainly and stop. Don't hand off a workpaper with a failed check.

---

## Command skeleton

Copy everything below into `commands/jes/{name}.md` and fill it in.

```markdown
---
description: {One line: what entry this prepares and when.}
argument-hint: "[period as YYYY-MM]"
---

# {Name of the entry}

**Purpose:** {What this entry records and why. When it runs in the close.}

**Period:** use `$ARGUMENTS` if given (YYYY-MM). Otherwise ask.

## Read first
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
A workbook following `commands/_templates/journal-entry.md`, named
`{GL} - {account} - {description} {YYYY.MM}.xlsx`, saved to {testing/ or the close folder}.

## Checks before handoff
The five standard JE checks, plus: {anything specific to this entry}.

## Never
- Never post the entry. A person posts it after approval.
- {Anything specific.}
```
