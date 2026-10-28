---
name: bank-reconciliation
description: "Reconcile a bank or card account's GL balance to its statement, classify every reconciling item, roll forward last month's open items, and propose entries for anything unrecorded. Use when someone asks to reconcile a bank or card account, do the bank recs, or tie the GL to a statement for a month-end close."
---

# Bank and card reconciliation

**Purpose:** prove each bank and card account's GL balance matches its statement, and explain
every difference. Runs for every account in `handbook/cash.md` during the close.

**Period:** use the period the user named. If no account is named, run every account in
`handbook/cash.md`, one workbook each.

> This is a worked example. Adjust the matching window and aging threshold to your policy, then
> test it on a month you've already reconciled.

## Read first

- `handbook/workpaper-standard.md` (Reconciliations)
- `handbook/cash.md` (the accounts, their GL accounts, statement timing, transfer rules)
- `handbook/close-process.md` (when recs are due, who signs off)

## Inputs

| Input | Source | Notes |
| --- | --- | --- |
| Statement | Connected bank or card platform, or the statement PDF saved in the period folder | Through the statement's closing date. Cards often close mid-month. |
| GL detail for the mapped account | Accounting system, GL detail report | Same date range as the statement |
| GL balance at the statement date | Accounting system, balance sheet or trial balance | |
| Last month's rec | Close folder | For the rollforward |

## Steps

1. **Get both balances.** The statement's ending balance (as printed, not recomputed) and the GL
   balance at the same date.
2. **Match transactions.** Match GL lines to statement lines on amount and sign, within a few days
   of each other. One GL line can match several statement lines (a batch deposit) and the
   reverse. Show every match you weren't sure about.
3. **Classify what's left.** Every unmatched item gets a type from the reconciliation standard:
   deposit in transit, outstanding payment, bank-only item, error, or timing. Never "unknown."
   If you can't tell, ask.
4. **Roll forward last month.** For each item open on last month's rec: cleared this month, or
   still open with its age.
5. **Propose entries.** For bank-only items (fees, interest, unrecorded transfers) and errors,
   propose a JE: date, accounts, amount, memo. A person books it.
6. **Prove it.** GL balance +/- reconciling items = statement balance. The unreconciled difference
   must be zero. If it isn't, keep looking; report what you found and what's still unexplained.
7. **Flag aging.** Any reconciling item older than the threshold in the reconciliation standard
   goes on the Summary tab.

## Output

A workbook per account following `handbook/workpaper-standard.md`:

- **Name:** `{GL number} - {account name} - Rec {YYYY.MM}.xlsx`
- **Save to:** `testing/` until this skill has passed review; then the close folder in `CLAUDE.md`
- A short summary in chat: each account, unreconciled difference, count of open items, any proposed JEs.

## Checks before handoff

The five standard rec checks. If the unreconciled difference isn't zero, say so first, before
anything else.

## Never

- Never mark items cleared in the accounting system, post an entry, or move money.
- Never plug a difference.
- Never store full account numbers. Last four digits only.
