# Accounting policies

**What this page is for:** the rules behind every entry Claude prepares.

**Last reviewed:** 2026-10-15, by Head of Finance

> Sample policies for a fictional company, shown for format only. Your policies are set by your
> team and your advisors.

## Capitalization

- **Threshold:** Assets over $2,500 with a useful life over one year.
- **Useful lives:** Computers 3 years. Furniture 5 years.
- **Method:** Straight-line, starting the month after the asset is placed in service.
- **Internal-use software:** [PLACEHOLDER: decision pending on the 2026 website rebuild. See Open questions.]

## Prepaid expenses

- **Threshold:** Invoices over $5,000 that cover more than one month.
- **Method:** Straight-line by month over the service period. The final month takes any rounding difference.
- **Where the schedule lives:** Google Drive, `Finance/Schedules/Prepaid Schedule.xlsx`.
- **Command:** `commands/jes/prepaid-amortization.md`

## Accruals

- **Threshold:** Accrue unbilled expenses over $2,500.
- **Recurring accruals:** Stratus Cloud and Lattice Inference usage (billed in arrears); the outsourced accounting firm (billed the 5th of the following month); quarterly bonuses, accrued monthly at target.
- **Reversal:** Auto-reverse on the first day of the next month.
- **Command:** `commands/jes/usage-accrual.md`

## Revenue recognition

- **Model:** Subscriptions recognized ratably over the service period.
- **Annual prepays:** Booked to 2400 Deferred Revenue on invoice, released monthly.
- **Discounts, credits, and refunds:** Recognized as a reduction of revenue in the period granted.
- **Services revenue:** Onboarding fees recognized when onboarding is complete.

## Stock-based compensation

- **Source:** Carta expense report.
- **Booking cadence:** [PLACEHOLDER: monthly or quarterly. Owner: Head of Finance.]

## Formal policy documents

| Policy | Location | Approved by | Date |
| --- | --- | --- | --- |
| Expense and card policy | Ramp, Policy tab | Head of Finance | 2026-01-10 |
| Revenue recognition memo | Google Drive, `Finance/Policies/` | Head of Finance, outside accountants | 2026-02-01 |
