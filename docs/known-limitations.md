---
title: Known Limitations
---

# Known Limitations

This beta is intentionally narrow. The goal is to learn whether a persistent finance context makes Claude more useful for startup finance workflows.

## Best With A Specific Stack

The full beta experience is best with:

- QuickBooks
- Stripe
- Ramp
- Mercury

You can continue with a partial stack, but missing connectors will create placeholders and open questions.

## QuickBooks Is Important For Setup

The account map is drafted from the QuickBooks chart of accounts.

If QuickBooks is missing, disconnected, or poorly configured, the initial finance profile will be much less complete.

## Some Workflows Are Early Examples

The beta includes workflows for:

- runway and burn;
- revenue reconciliation;
- board metrics.

These are starting points, not final packaged finance products. Expect them to improve based on tester feedback.

## Human Review Is Required

Claude can misread account names, misunderstand source-system behavior, or surface incomplete data.

Review:

- account classifications;
- KPI definitions;
- revenue recognition assumptions;
- cash account inclusions;
- any board-ready output.

Do not use outputs in final board, investor, audit, or lender materials without human review.

## Missing Connectors Mean Missing Context

If a connector is not available:

- related sections in `finance-profile.md` may stay placeholder;
- workflows that rely on that connector may be incomplete;
- Claude should tell you what is missing instead of guessing.

Example:

```text
Ramp is not connected, so vendor recurrence and card spend rules are still unresolved.
```

## The Finance Profile Is Only As Good As Its Inputs

The profile improves when you share:

- board materials;
- KPI definitions;
- close procedures;
- revenue policies;
- account mapping decisions;
- known exceptions.

If none of that context is available, Claude will rely more heavily on system data and placeholders.

## No Writeback Workflows

This beta is designed for read-only analysis.

The plugin should not create journal entries, update accounts, change customers, modify subscriptions, or write back to connected finance systems.

## Payroll And Forecasting May Be Manual

The profile includes sections for people, payroll, planning, and forecast assumptions.

The bundled connector set does not include every payroll or planning system. Those sections may need to be filled from documents, spreadsheets, or user-provided context.

## Security And Data Policies Are Still Beta-Specific

Use sandbox or test-company data if you are not ready to authorize production systems.

Review the [Data Handling and Security](data-handling-security.md) page before connecting sensitive finance data.

## Unsupported Or Unclear Behavior

Please report:

- auth issues;
- stale or missing profile location;
- incorrect account mappings;
- unsupported connector combinations;
- outputs that feel overconfident;
- workflows that do not use the finance profile.

Email these to alex@aircfo.com.

