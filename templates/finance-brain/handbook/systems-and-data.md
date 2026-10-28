# Systems and data

**What this page is for:** what Claude can read directly, and the habits that keep your inputs
consistent enough for a command to run the same way every month. This is rung 2 of the
ladder: clean, connected data.

**Last reviewed:** [PLACEHOLDER: YYYY-MM-DD, by whom]

## What Claude is connected to

Connect your systems in Claude's connector settings, each with your own login. Start with
read-only access to your books and your bank, then add the rest.

| System | Connected? | Access | What Claude uses it for |
| --- | --- | --- | --- |
| [PLACEHOLDER: accounting system] | [PLACEHOLDER: yes / no] | Read-only | GL detail, trial balance, account list |
| [PLACEHOLDER: bank] | | Read-only | Balances and transactions for recs |
| [PLACEHOLDER: spend platform] | | Read-only | Card transactions, receipts, vendors |
| [PLACEHOLDER: billing] | | Read-only | Invoices, subscriptions, payouts |
| [PLACEHOLDER: shared drive] | | Read and write to the close folder only | Prior-period workpapers, saving new ones |

**For anything not connected,** commands ask for an export and say exactly which report and
date range they need.

**Read-only is the rule.** Even when a connector offers write access, commands in this folder
never post, pay, or edit records. A person posts what Claude prepares.

## The clean-inputs checklist

A command can only repeat a task if the inputs look the same every month. Before automating
anything, check:

- [ ] **Last month's version exists and is right.** The best spec for a command is a finished,
      reviewed workpaper from the prior period.
- [ ] **Same shape every month.** Same tabs, same columns, same order. If the format changes,
      update the command first.
- [ ] **Predictable file names.** `{GL account number} - {account name} - {description} {YYYY.MM}.xlsx`,
      so Claude can find last month's file without asking.
- [ ] **One folder per period.** [PLACEHOLDER: e.g. Finance/Close/2026-09/] with the same
      subfolders each month.
- [ ] **Schedules live in one place.** Prepaids, fixed assets, and accruals each have one
      schedule of record, not copies.
- [ ] **The chart of accounts is current.** No new activity on legacy accounts; clearing
      accounts actually clear.
- [ ] **Exports are saved, not pasted.** When a system isn't connected, save the export into the
      period folder so the workpaper has a source.

## Same thing, different names

Customers and vendors often appear under different names in different systems. List the ones
that matter so Claude matches them instead of treating them as two.

| In [PLACEHOLDER: accounting system] | In [PLACEHOLDER: other system] | Notes |
| --- | --- | --- |
| [PLACEHOLDER: e.g. Amazon Web Services] | [PLACEHOLDER: e.g. AWS on the card feed] | |

## Known data issues

Things that trip up automation and how to handle them.

- [PLACEHOLDER: e.g. card feed duplicates refunds; processor payouts are net of fees]
