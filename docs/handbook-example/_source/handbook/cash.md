# Cash

**What this page is for:** every place the company holds or spends money, how each maps to the
general ledger, and what counts as cash for runway.

**Last reviewed:** 2026-10-15, by Head of Finance

## Accounts

| Account | Institution | Last 4 | GL account | Purpose | Counts as runway cash? |
| --- | --- | --- | --- | --- | --- |
| Operating checking | Mercury | 4821 | 1010 | Payroll, bills, Ramp payments, Stripe payouts | Yes |
| Treasury | Mercury | 7710 | 1020 | Excess cash | Yes |
| Corporate card | Ramp | n/a | 2010 Ramp Card Payable | Employee spend | n/a |
| Stripe balance | Stripe | n/a | 1960 Stripe Clearing | Pending payouts | No (in transit) |

## Rules

- **Runway cash:** Operating plus treasury. Funds in transit from Stripe don't count until they land.
- **Restricted cash:** None.
- **Transfers between our own accounts:** Recorded as transfers between 1010 and 1020. They never count as spend or revenue.
- **Card and processor clearing:** Ramp is paid in full from operating checking every week. Stripe payouts land net of fees; fees are grossed up through 1960 Stripe Clearing.

## Statement timing

| Account | Statement period | Where statements are saved |
| --- | --- | --- |
| Mercury operating and treasury | Calendar month | `Finance/Close/YYYY-MM/Statements/` |
| Ramp card | Calendar month | Same folder |

## Reconciliations

Every account above gets reconciled monthly with `commands/recs/bank-reconciliation.md`.
