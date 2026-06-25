---
title: Give Claude Your Finance Context Once
---

# Give Claude Your Finance Context Once

airCFO Claude for Startup Finance helps Claude understand how your startup's finance stack actually works: your chart of accounts, cash rules, revenue definitions, system mappings, and the judgment calls your team normally carries in its head.

Once that context is built, Claude can reuse it across finance workflows like runway, revenue reconciliation, board metrics, and monthly reporting without asking you to re-explain the business every time.

This is a private beta for finance leaders, founders, and operators who want to test a new way of giving Claude durable finance context. It runs in **Claude Cowork**.

## The Problem

Claude can read financial data, but finance work breaks when it does not know your company's definitions.

For example:

- Which Mercury accounts count as cash for runway?
- Does treasury count as available runway cash?
- Is Stripe MRR the same definition you use in the board deck?
- Which vendors are COGS instead of G&A?
- Which QuickBooks accounts roll into each management reporting line?
- Which one-time costs should be excluded from run-rate burn?

Those answers rarely live cleanly in one system. They live in board decks, close checklists, reporting packages, spreadsheets, and CFO judgment.

## The Idea

The plugin first builds a local `finance-profile.md` file. Think of it as Claude's operating manual for your finance function.

It is not your books. It is the context Claude needs to interpret your books.

The profile captures:

- how your company makes money;
- which systems own which numbers;
- how accounts map into management reporting;
- how you define burn, runway, revenue, ARR, MRR, and other KPIs;
- known exceptions and judgment calls;
- open questions that still need human review.

## What It Does Today

The beta plugin connects Claude to:

- QuickBooks
- Stripe
- Ramp
- Mercury

It includes workflows to:

- build a company-specific finance profile;
- draft and review an account map from QuickBooks;
- calculate runway and burn;
- reconcile Stripe revenue to QuickBooks;
- assemble a board-ready financial metrics summary.

## Who This Is For

This beta is best for:

- early-stage startups using QuickBooks plus at least one of Stripe, Ramp, or Mercury;
- finance leaders who already have recurring reporting workflows;
- founders or operators who want Claude to understand their finance model before analysis;
- teams comfortable reviewing AI-generated finance outputs before relying on them.

The full experience is strongest with QuickBooks, Stripe, Ramp, and Mercury connected. Partial setups are supported, but missing systems will create placeholders and open questions in the finance profile.

## What It Is Not

This beta is not:

- an accounting system;
- a replacement for your source-of-truth systems;
- an audit tool;
- a writeback automation;
- a substitute for CFO review.

The plugin is designed for read-only finance analysis. You should review outputs before using them in board materials, investor updates, audits, or operational decisions.

## Start Here

1. Read the [Beta Tester Brief](beta-tester-brief.md).
2. Review the [Data Handling and Security FAQ](data-handling-security.md) before you connect anything.
3. Follow the [First-Session Guide](first-session-guide.md).
4. Learn how the [Finance Profile](finance-profile-explainer.md) works.
5. Try the prompts in [Use Cases](use-cases.md).
6. Know the [Known Limitations](known-limitations.md) of the beta.

## Install

You'll need access to **Claude Cowork**. The plugin installs from inside Cowork — there is no command line. You add the airCFO marketplace once, then install the plugin from it.

1. Open Claude Cowork, click **Customize** in the left sidebar, then **Browse plugins**.
2. Select **Personal**, click the **+** button, and choose **Add marketplace from GitHub**.
3. Enter the repository URL: `https://github.com/aircfo/claude-startup-finance`
4. Click **Install** on the **startup-finance** plugin. It activates automatically.

Then, in a Cowork session, start setup:

```text
/finance-context-builder
```

You can also just ask in plain English — "set up the finance plugin."

Questions or feedback during the beta: alex@aircfo.com

---

*Unofficial. Not affiliated with, endorsed by, or sponsored by Stripe, Ramp, Mercury, Intuit (QuickBooks), or Anthropic. All trademarks belong to their respective owners.*
