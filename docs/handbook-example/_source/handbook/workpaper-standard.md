# Workpaper standard

**What this page is for:** what every journal entry and reconciliation workpaper looks like, so a
reviewer can open any one, from any month, and know where to look. Every JE and rec skill in
`skills/` follows it.

**Last reviewed:** 2026-10-15, by Head of Finance

The September 2026 usage accrual, `2101 - Accrued Expenses - Usage Accrual 2026.09.xlsx`, is the reference JE workpaper.

## Rules for every workpaper

- **File name:** `{GL account number} - {account name} - {description} {YYYY.MM}.xlsx`, for
  example `2101 - Accrued Expenses - Usage Accrual 2026.09.xlsx` or
  `1010 - Operating Checking - Rec 2026.09.xlsx`.
- **Formulas, never hardcoded results.** If the source data changes, the result changes.
- **Source tabs are never edited.** Inputs stay exactly as pulled or exported.
- **Accounts must exist** in the chart of accounts. Never invent one.
- **Blue text for inputs, black for formulas.**
- **Sign-off block** at the bottom of the Summary tab:

  > Prepared by: Claude (run by [name]) on [date]
  > Reviewed and approved by: ______________ Date: ________
  > Requires approval by someone other than the preparer, per `handbook/company-overview.md`.

- **Save to** `testing/` while a skill is new or changed. After it has passed review, Google
  Drive, `Finance/Close/YYYY-MM/JEs/` or `Finance/Close/YYYY-MM/Recs/`.

If any check below fails, say so plainly and stop. Don't hand off a workpaper with a failed check.

## Journal entries

**Tabs, in this order:**

| Tab | What's on it |
| --- | --- |
| **Summary** | Purpose, period, the handbook policy it follows, where each input came from (system and report, or export file name, with date range), the result in one sentence, and the sign-off block. |
| **Source Data** | The raw inputs exactly as pulled or exported. |
| **Calculation** | The math, as live formulas that reference Source Data. Every assumption (a rate, a threshold, a useful life) in its own labeled cell, with where it came from. |
| **JE** | The entry: post date, reversal date (if any), account, debit, credit, memo, department or class. Totals row. A balance check that reads BALANCED or OUT OF BALANCE. |
| **Prior Period** (optional) | Last month's entry beside this month's, with the change explained if it's material. |

- Debits equal credits, and the balance check is a formula, not a typed word.
- Memo format: `{description} - {vendor or contract} - {YYYY.MM}`.
- **Optional import file:** if the accounting system accepts a journal entry import, also save a
  CSV in its import format beside the workbook. A person imports it after approval. Claude never
  posts.

**Checks before handoff,** shown to the user as a short table:

1. **Balanced:** total debits equal total credits.
2. **Ties to source:** the Calculation total equals the JE amount.
3. **Ties to the schedule or balance:** for entries that roll a balance (prepaids, accruals,
   deferred revenue), opening + additions - releases = closing, and closing matches what the GL
   will show after the entry.
4. **Reasonable vs. last month:** if the amount moved more than the flux threshold in
   `handbook/close-process.md`, explain why.
5. **Accounts valid:** every account exists and is active.

## Reconciliations

The same shape works for a bank account, a credit card, a clearing account, or a balance-sheet
account tied to a schedule.

**Tabs, in this order:**

| Tab | What's on it |
| --- | --- |
| **Summary** | The account, the period, the statement date, the GL balance, the independent balance (statement or schedule), total reconciling items, and the **unreconciled difference**, which must be zero. Sources and the sign-off block. |
| **GL Detail** | The account's GL activity for the period, as pulled. |
| **Statement** | The independent source: bank or card statement lines, or the supporting schedule. |
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

- The unreconciled difference is a formula, and it must be zero. If it isn't, the rec isn't done.
- Every reconciling item has a type and a next step. "Unknown" is not a type.
- Items older than 60 days get flagged on the Summary tab.

**Checks before handoff:**

1. **Unreconciled difference is zero.**
2. **GL balance matches the trial balance** for the account at the statement date (the month
   end for most bank accounts; cards often close mid-month).
3. **Statement ending balance matches the statement** (not a running total Claude computed).
4. **Last month's items are accounted for:** every prior open item is cleared or carried forward
   with its age.
5. **Proposed JEs listed:** any bank-only item or error has a proposed entry for a person to book.
