---
description: The reconciliation workpaper standard, plus a skeleton to copy when writing a new rec command.
argument-hint: "(template, not run directly)"
---

# Reconciliation: workpaper standard and command template

Every rec command in this folder produces a workpaper that looks like this, whether it's a
bank account, a credit card, a clearing account, or a balance-sheet account tied to a schedule.

## The workbook

**File name:** `{GL account number} - {account name} - Rec {YYYY.MM}.xlsx`
For example: `1010 - Operating Checking - Rec 2026.09.xlsx`

**Tabs, in this order:**

| Tab | What's on it |
| --- | --- |
| **Summary** | The account, the period, the statement date, the GL balance, the independent balance (statement or schedule), total reconciling items, and the **unreconciled difference**, which must be zero. Sources and the sign-off block. |
| **GL Detail** | The account's GL activity for the period, as pulled. Never edited. |
| **Statement** | The independent source: bank or card statement lines, or the supporting schedule. Never edited. |
| **Reconciling Items** | Every item on one side but not the other, each with a type, date, amount, age in days, and what happens next. |
| **Rollforward** | Last month's open reconciling items: cleared this month, or still open (with age). |

**Reconciling item types:**

| Type | Meaning | What happens next |
| --- | --- | --- |
| Deposit in transit | In the GL, not yet on the statement | Should clear in the first days of next month |
| Outstanding payment | In the GL, not yet on the statement | Should clear when the payee cashes or the payment settles |
| Bank-only item | On the statement, not in the GL (fees, interest, unrecorded transfers) | Propose a JE for a person to book |
| Error | Recorded wrong in the GL (amount, account, or duplicate) | Propose a correcting JE |
| Timing | Statement and GL cut off on different dates (common for cards) | Explain the cutoff |

**Rules for the workbook:**

- The unreconciled difference is a formula, and it must be zero. If it isn't, the rec isn't done.
- Every reconciling item has a type and a next step. "Unknown" is not a type.
- Items older than [PLACEHOLDER: e.g. 60] days get flagged on the Summary tab.
- Sign-off block at the bottom of the Summary tab:

  > Prepared by: Claude (run by [name]) on [date]
  > Reviewed and approved by: ______________ Date: ________

**Save to:** `testing/` while the command is new or changed. After it has passed review, the
close folder named in `CLAUDE.md`.

## Checks before handoff

1. **Unreconciled difference is zero.**
2. **GL balance matches the trial balance** for the account at the period end.
3. **Statement ending balance matches the statement** (not a running total Claude computed).
4. **Last month's items are accounted for:** every prior open item is cleared or carried forward
   with its age.
5. **Proposed JEs listed:** any bank-only item or error has a proposed entry for a person to book.

---

## Command skeleton

Copy everything below into `commands/recs/{name}.md` and fill it in.

```markdown
---
description: {One line: which account this reconciles and to what.}
argument-hint: "[period as YYYY-MM] [optional: account]"
---

# {Account} reconciliation

**Purpose:** {What this proves, and when it runs in the close.}

**Period:** use `$ARGUMENTS` if given. Otherwise ask.

## Read first
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
A workbook following `commands/_templates/reconciliation.md`, saved to {testing/ or the close folder}.

## Checks before handoff
The five standard rec checks, plus: {anything specific}.

## Never
- Never mark items cleared in the accounting system or post a JE. Propose; a person books.
```
