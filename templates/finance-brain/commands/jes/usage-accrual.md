---
description: Prepare the month-end accrual for usage-billed vendors (cloud, APIs, data) whose invoice hasn't arrived yet, as a reversing JE.
argument-hint: "[period as YYYY-MM] [optional: vendor]"
---

# Usage accrual

**Purpose:** record expense for services used this month but not yet invoiced, for vendors that
bill in arrears based on usage: cloud hosting, AI and API providers, data vendors. Runs at month
end; reverses on the first day of the next month so the real invoice books cleanly.

**Period:** use `$ARGUMENTS` if given. Otherwise ask.

> This is a worked example. A finished workpaper built on synthetic data is in
> `examples/workpapers/2101 - Accrued Expenses - Usage Accrual 2026.09.xlsx`. Adjust the accounts
> and vendors to match your handbook, then test against a month you've already closed.

## Read first

- `handbook/accounting-policies.md`, Accruals (threshold, which vendors, reversal convention)
- `handbook/chart-of-accounts.md` (the accrued expenses account, and which expense account each
  vendor maps to: cost of revenue for product infrastructure, operating expense for internal use)

## Inputs

| Input | Source | Notes |
| --- | --- | --- |
| Usage for the period, by vendor | The vendor's usage dashboard or billing export, or a connected system | Units and dates for the full calendar month |
| Contract rates | `handbook/accounting-policies.md`, or the contract | Rate per unit, tiers, minimums, committed spend |
| Invoices already received | Accounting system, bills for the period | Anything already billed is not accrued |
| Last month's accrual and the invoice that replaced it | Close folder and accounting system | For the true-up check |

## Steps

1. **List the vendors to accrue.** Start from the list in the policy. Add any vendor with usage
   this month and no bill yet. Skip anything under the accrual threshold, and say so.
2. **Pull usage.** For each vendor, the units used in the period, split by however the expense is
   split (product vs. internal, department, class). Save the raw export to Source Data.
3. **Price it.** Units x contract rate, applying tiers, minimums, and credits. Every rate sits in
   its own labeled cell with its source.
4. **Build the JE.** Debit each expense account, credit accrued expenses. Post date is the last day
   of the period; reversal date is the first day of the next month. Memo:
   `Usage Accrual - {vendor} - {YYYY.MM}`.
5. **True up last month.** Compare last month's accrual to the invoice that arrived for that month.
   If the difference is material, explain it and suggest whether the method or the rates need
   updating. Fix the command, not just the number.

## Output

A workbook following `commands/_templates/journal-entry.md`:

- **Name:** `{accrued expenses GL number} - Accrued Expenses - Usage Accrual {YYYY.MM}.xlsx`
- **Tabs:** Summary, Source Data, Calculation, JE, Prior Period (with the true-up)
- **Save to:** `testing/` until this command has passed review; then the close folder in `CLAUDE.md`

## Checks before handoff

The five standard JE checks, plus:

- Nothing accrued that has already been invoiced.
- Reversal date set to the first day of the next month.
- Last month's true-up shown, with an explanation if it's over the flux threshold.

## Never

- Never post the entry. A person posts it after approval.
- Never estimate usage without a source. If usage isn't available, say so and ask.
