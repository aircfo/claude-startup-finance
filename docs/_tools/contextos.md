---
title: Build your ContextOS
theme: foundation
order: 1
summary: Teach Claude what your numbers mean — your definitions of burn, runway, and MRR, and where every QuickBooks account rolls up — captured once, proven against your live books, and read by every other tool here.
plugin: finance-contextos
plugin_home: true
skill: finance-context-builder
ask: Build my ContextOS
reads: [QuickBooks]
needs_contextos: false
time: About 20 minutes, once. Refreshes are faster.
---

## Why start here

Claude can already read your finance systems. What it can't know is how *your* company
defines the numbers: which bank accounts count as runway cash, whether board-deck MRR matches
the Stripe dashboard, which vendors are COGS, which one-time costs to leave out of burn.
Those answers live in board decks, close checklists, and someone's head. Without them, every
AI answer is a generic one.

The ContextOS captures them once. Every other tool in this library reads it before it
touches a number, so they all share one consistent model of your company.

## What you get

A folder you own (default `~/Desktop/ContextOS/`), in plain files:

- **`finance-profile.md`**: Claude's operating manual for your finance function. KPI
  definitions, cash and burn rules, source-of-truth mappings, known exceptions, open
  questions.
- **`account-map.csv`**: every QuickBooks account classified for management reporting and
  cash flow, editable in any spreadsheet. Rows you confirm are never overwritten by a refresh.
- **`context/`**: the docs you shared, kept as a record of what Claude has read.
- **`CHANGELOG.md`**: a dated log of what changed each run.

## How it works

1. **Connect QuickBooks.** One sign-in pop-up with your own login, read-only. Claude confirms
   the company name it connected to.
2. **Build.** Claude drafts the account map from your QuickBooks account list and reads
   anything you share about the business. You review only the judgment calls (department
   assignments, unusual accounts), not hundreds of rows.
3. **Prove it ties.** The build ends by checking itself against your live books: cash to the
   bank, revenue to the penny. Differences become open questions, never silent assumptions.

Connected Stripe, Ramp, or Mercury through [All Systems Go]({{ '/tools/all-systems-go/' | relative_url }})?
Re-run the build and it maps those systems onto your ledger too.

## Keep it current

```text
Add this board deck to my ContextOS.
```

```text
Review the account map and show me which classifications still need a human decision.
```

Go deeper: [What is a ContextOS?]({{ '/finance-profile-explainer.html' | relative_url }}) ·
[First-session guide]({{ '/first-session-guide.html' | relative_url }}) ·
[Data handling and security]({{ '/data-handling-security.html' | relative_url }}) ·
[Self-host the QuickBooks connector]({{ '/self-hosting.html' | relative_url }})
