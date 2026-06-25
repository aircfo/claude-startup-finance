---
title: Beta Tester Brief
---

# Beta Tester Brief

Thank you for testing airCFO Claude for Startup Finance.

This beta is testing a simple but important idea: finance analysis gets dramatically better when Claude has a durable understanding of your company's finance context before it pulls numbers.

The plugin builds that context once, stores it locally, and then uses it across repeatable finance workflows.

## What You Are Testing

You are testing a **Claude Cowork** plugin that connects to common startup finance systems and creates an airCFO Finance Context folder you can open anytime.

That folder includes:

- `finance-profile.md` - Claude's finance operating manual for your company;
- `account-map.csv` - a spreadsheet-editable mapping of QuickBooks accounts into reporting categories;
- `context/` - source materials you shared during setup;
- `CHANGELOG.md` - a record of what changed during setup or refreshes.

The goal is not just to answer one question. The goal is to make future finance questions easier because Claude has already learned how your company defines and maps the numbers.

## Best-Fit Testers

This beta is currently best for teams that:

- use QuickBooks as the accounting system;
- use at least one of Stripe, Ramp, or Mercury;
- have recurring finance questions around runway, revenue, board reporting, or monthly close;
- can review account mappings and finance assumptions during setup;
- are comfortable testing with sandbox or non-sensitive data if they are not ready to authorize production systems.

## What You Will Do

In a typical first session, you will:

1. Install the plugin in Claude Cowork.
2. Authenticate relevant finance systems.
3. Run `/finance-context-builder`.
4. Share one helpful finance artifact or business description.
5. Review the drafted account map.
6. Finalize a first version of `finance-profile.md`.
7. Run one or two sample workflows, such as runway or board metrics.
8. Tell us where the product was useful, confusing, or untrustworthy.

## Time Commitment

Expected first-session timing:

- install/auth: 5-10 minutes;
- finance context build: 15-30 minutes;
- first useful workflow: immediately after profile creation.

The setup may take longer if your chart of accounts is complex or if several connectors need to be authorized.

## What Good Feedback Looks Like

We are especially interested in:

- where setup felt clear or confusing;
- where the account map looked right or wrong;
- where Claude guessed instead of asking;
- whether the first workflow output matched how you would calculate the number;
- what missing workflow would make this worth using weekly;
- what trust, security, or control questions came up.

The most helpful feedback is specific: what you tried, what happened, whether you trusted it, and what you expected instead. Email it to alex@aircfo.com after your test session.

## Beta Expectations

This is an early product.

You should expect:

- some profile sections to remain placeholders;
- some connector combinations to be incomplete;
- some workflows to require human review;
- rough edges around auth, missing data, and source-system differences.

You should not expect:

- writeback to finance systems;
- audit-ready conclusions without review;
- perfect account classification without human confirmation;
- support for every finance stack.

## Helpful Materials To Have Ready

Any one of these will improve the first setup:

- board deck;
- investor update;
- KPI dashboard;
- monthly reporting package;
- close checklist;
- revenue recognition memo;
- chart of accounts notes;
- a short written description of how the business makes money.

You can still proceed without these. The plugin will leave explicit placeholders where context is missing.

## Next Step

Start with the [First-Session Guide](first-session-guide.md).
