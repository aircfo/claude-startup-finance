---
title: Known Limitations
---

# Known Limitations

The Finance Brain Starter Kit and the tools here are intentionally narrow. This is the honest
list of what they don't do yet.

## The Handbook Is Only As Good As Its Inputs

The kit's setup interview drafts your handbook from your documents and any systems you've
connected. It gets better when you share:

- a close checklist or SOP;
- policy documents;
- last month's reporting package or board deck;
- a few finished workpapers.

Without them, more of the handbook stays as placeholders until someone answers the questions.
That's by design: a placeholder is better than a guess.

## Worked Examples Are Starting Points

The kit ships three worked commands (prepaid amortization, a usage accrual, a bank
reconciliation), and the tool library ships runway and burn, revenue reconciliation, and board
metrics. Expect to adjust each one to match how your team works. Test a changed command in
`testing/` against a known-good result before you rely on it.

## Best With A Connected Stack

Commands and tools work from exports, but they work best when Claude can read your accounting
system, bank, card platform, and billing system directly. The tools in this library are built
around QuickBooks, Stripe, Ramp, and Mercury. Other systems work through exports.

## Connector Sessions Expire

Connector sessions lapse after a few idle days. On a later run, a connector that worked before
may ask you to sign in again. That's normal, not a failure: re-authorize and continue.

## Payroll And Forecasting May Be Manual

The handbook has sections for people, payroll, and the plan, but no tool here connects to a
payroll or planning system. Those sections are filled from documents or the follow-up
interview.

## No Writeback

Everything here is read-only. Nothing creates journal entries, updates accounts, changes
customers or subscriptions, or writes to a connected system. A person posts.

## Human Review Is Required

Claude can misread account names, misunderstand how a system behaves, or work from incomplete
data. Review classifications, metric definitions, revenue recognition assumptions, which
accounts count as cash, and anything board-ready. Don't use outputs in board, investor, audit,
or lender materials without review by someone other than the person who ran the command.

Review the [Data Handling and Security]({{ '/data-handling-security.html' | relative_url }}) page before connecting
sensitive finance data.

## Report Problems

Please report sign-in issues, wrong account mappings, outputs that feel overconfident, and
commands or tools that ignored your handbook. Email alex@aircfo.com or
[open an issue](https://github.com/aircfo/claude-startup-finance/issues).
