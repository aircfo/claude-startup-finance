---
name: prepaid-amortization
description: "Prepare the monthly prepaid amortization journal entry from the prepaid schedule, add new prepaids from the month's bills, and tie the schedule to the GL. Use when someone asks to amortize prepaids, book prepaid expense, or prepare the prepaid JE for a month-end close."
---

# Prepaid amortization

**Purpose:** record this month's expense for every prepaid contract, keep the prepaid schedule
current, and prove the schedule ties to the GL. Runs once a month during the close (see
`handbook/close-process.md`).

**Period:** use the period the user named (YYYY-MM). Otherwise ask.

> This is a worked example. Before relying on it, adjust the accounts, threshold, and method to
> match `handbook/accounting-policies.md`, then test it with the `new-skill` skill
> step 4: recreate a month you've already closed and compare.

## Read first

- `handbook/workpaper-standard.md` (Journal entries)
- `handbook/accounting-policies.md`, Prepaid expenses (threshold, method, where the schedule lives)
- `handbook/chart-of-accounts.md` (the prepaid account and the expense accounts each contract maps to)

## Inputs

| Input | Source | Notes |
| --- | --- | --- |
| Prepaid schedule | Location in `accounting-policies.md` | One row per contract: vendor, invoice, start, end, total, expense account |
| Prepaid account GL detail | Accounting system, GL detail report for the prepaid account | Period start to period end |
| Bills over the threshold | Accounting system, bills or GL detail for the period | To catch new prepaids not yet on the schedule |
| Last month's workpaper | Close folder | For the prior period comparison |

## Steps

1. **Read the schedule.** Load every active contract. Confirm each has a start date, end date,
   total, and expense account. Flag any row missing one.
2. **Find new prepaids.** From the period's bills and the prepaid account's GL detail, list any
   invoice over the threshold that covers more than one month and isn't on the schedule. Show
   them to the user and ask which to add. Don't add one without a yes.
3. **Calculate this month's amortization** per contract, using the method in the policy. For
   straight-line by month: total / number of service months, with the final month taking any
   rounding difference so the contract fully amortizes.
4. **Build the JE.** One debit line per contract to its expense account (with department or class
   if required), one credit line to the prepaid account. Post date is the last day of the period.
   No reversal.
5. **Roll the schedule forward.** Opening balance + additions - amortization = closing balance,
   per contract and in total.
6. **Tie to the GL.** Compare the schedule's closing balance to the prepaid account's GL balance
   at period end, adjusted for this entry. Explain any difference: an invoice coded to prepaid
   that isn't on the schedule, a contract that ended early, a manual entry.
7. **Compare to last month.** If total amortization moved more than the flux threshold, name the
   contracts that drove it.

## Output

A workbook following `handbook/workpaper-standard.md`:

- **Name:** `{prepaid GL number} - Prepaid Expenses - Amortization {YYYY.MM}.xlsx`
- **Tabs:** Summary, Source Data (schedule as read, GL detail), Calculation (per-contract amortization and rollforward), JE, Prior Period
- **Save to:** `testing/` until this skill has passed review; then the close folder in `CLAUDE.md`
- Also save the updated schedule, if the schedule is a file you were asked to maintain. Never overwrite it without the user's OK.

## Checks before handoff

The five standard JE checks, plus:

- Every contract that ended this month is fully amortized (closing balance zero).
- No contract has a negative balance.
- Schedule closing balance ties to the GL after this entry, or the difference is explained.

## Never

- Never post the entry. A person posts it after approval.
- Never add a contract to the schedule without the user's confirmation.
- Never change a contract's dates or total without a source document.
