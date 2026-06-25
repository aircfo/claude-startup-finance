---
title: What Is finance-profile.md?
---

# What Is `finance-profile.md`?

`finance-profile.md` is Claude's operating manual for your finance function.

It is not your books. It is not a data warehouse. It is not a replacement for QuickBooks, Stripe, Ramp, or Mercury.

It is the context Claude needs to interpret your books correctly.

## Why It Exists

Most finance analysis depends on company-specific context.

For example:

- You may define MRR differently from the Stripe dashboard.
- You may count some savings accounts as runway cash and exclude others.
- You may treat some vendors as COGS even though their names look like software spend.
- You may exclude financing inflows from net burn.
- You may have one-time legal or recruiting costs that should not be treated as run-rate expense.

Claude cannot reliably infer those rules from raw transactions alone.

The finance profile stores those definitions, mappings, and judgment calls in one place.

## What It Contains

The beta profile uses a 14-section structure:

1. Company Snapshot
2. Business Model
3. KPI Definitions
4. Source-of-Truth Map
5. Chart of Accounts / Reporting Framework
6. Cash, Burn, and Runway Rules
7. Revenue and Collections Rules
8. Spend, AP, and Vendor Rules
9. People and Payroll Model
10. Planning and Forecast Assumptions
11. Reporting Cadence and Materiality
12. Known Exceptions and Judgment Calls
13. Open Questions
14. Provenance and Changelog

You do not need to fill every section perfectly on day one. The first profile can contain placeholders.

## What It References

The profile references `account-map.csv` for per-account detail.

`account-map.csv` is the spreadsheet-editable source for:

- QuickBooks account names;
- account types and detail types;
- management reporting groupings;
- cash-flow mappings;
- short account descriptions.

The profile should summarize the reporting framework, not duplicate the full account table.

## How Claude Builds It

During `/finance-context-builder`, Claude drafts the profile from:

- context you share in the session;
- QuickBooks account data;
- connected system mappings;
- discovered money flows between Stripe, Mercury, Ramp, and QuickBooks;
- conventions you confirm.

Claude should fill what it knows and leave explicit placeholders where it does not know enough.

Example:

```text
[PLACEHOLDER: Confirm whether Mercury Savings accounts count as runway cash.]
```

## Why Placeholders Matter

Placeholders prevent fake certainty.

If a workflow depends on a missing definition, Claude should surface the gap instead of inventing an assumption.

Examples:

- missing revenue recognition method;
- unknown payroll/headcount source;
- unclear treatment of treasury accounts;
- unsupported connector;
- unconfirmed account classification.

Those gaps are also mirrored into Open Questions so they can be resolved later.

## How Workflows Use It

Before running finance workflows, Claude reads the profile to understand:

- which accounts to include;
- how metrics are defined;
- which source system is authoritative;
- which assumptions have already been confirmed;
- which questions remain open.

That is what lets a runway workflow use your burn definition instead of a generic one.

## How It Gets Updated

Run `/finance-context-builder` again when:

- you add a new system;
- your chart of accounts changes;
- you update KPI definitions;
- you want to add a new board deck, SOP, or reporting package;
- a workflow surfaces a placeholder you want to resolve.

The profile should become more useful over time.

## A Simple Mental Model

Your systems hold the data.

Your finance profile holds the meaning.

Claude needs both.

