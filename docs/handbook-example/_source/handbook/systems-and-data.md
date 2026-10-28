# Systems and data

**What this page is for:** what Claude can read directly, and the habits that keep inputs
consistent enough for a command to run the same way every month.

**Last reviewed:** 2026-10-15, by Head of Finance

## What Claude is connected to

| System | Connected? | Access | What Claude uses it for |
| --- | --- | --- | --- |
| QuickBooks Online | Yes | Read-only | GL detail, trial balance, account list |
| Mercury | Yes | Read-only | Balances and transactions for recs |
| Ramp | Yes | Read-only | Card transactions, receipts, vendors |
| Stripe | Yes | Read-only | Invoices, subscriptions, payouts |
| Google Drive | Yes | Read and write to `Finance/Close/` only | Prior-period workpapers, saving new ones |
| Gusto | No | Export | Payroll journal report, saved to the period folder |
| Stratus Cloud, Lattice Inference | No | Export | Monthly usage CSV from each vendor's billing page |

**Read-only is the rule.** Commands never post, pay, or edit records. A person posts what Claude
prepares.

## The clean-inputs checklist

- [x] Last month's version of every automated task exists and has been reviewed.
- [x] Same workpaper shape every month (the standard in `commands/_templates/`).
- [x] Predictable file names: `{GL} - {account} - {description} {YYYY.MM}.xlsx`.
- [x] One folder per period: `Finance/Close/YYYY-MM/` with `JEs/`, `Recs/`, `Statements/`.
- [x] Schedules live in one place: `Finance/Schedules/`.
- [ ] Chart of accounts current. 6990 Ask My Accountant still has a $412 balance to clear.
- [x] Exports are saved into the period folder, not pasted.

## Same thing, different names

| In QuickBooks Online | In another system | Notes |
| --- | --- | --- |
| Stratus Cloud | `STRATUS*CLOUD SVCS` on the Ramp card feed | Same vendor. Production and staging split by project tag. |
| Lattice Inference | `LATTICE AI INC` on the Ramp card feed | Same vendor. |
| Gusto | `GUSTO NET`, `GUSTO TAX` in Mercury transactions | Net pay and payroll taxes debit separately. |
| Customer legal names | Stripe customer display names | Stripe is the customer list of record. Match on the Stripe customer ID in the QuickBooks customer notes. |

## Known data issues

- Ramp occasionally syncs a refund twice. The card rec catches it; delete the duplicate in QuickBooks after review.
- Stratus Cloud's usage export splits production and staging by project tag. Untagged usage goes to production until someone tags it.
