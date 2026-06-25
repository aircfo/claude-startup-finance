---
title: Use Cases And Prompts
---

# Use Cases And Prompts

Use these prompts after you have created a first version of `finance-profile.md`.

Each use case lists the connectors that make the workflow strongest. If a connector is missing, Claude should say what is incomplete and leave open questions rather than guessing.

Some of these map to a dedicated workflow that ships with the plugin — runway and burn, board metrics, revenue reconciliation, and the account-map review. Others, like explaining a burn change or finding recurring vendors, are ad-hoc analyses Claude runs using your finance profile and connected systems. Either way you just ask; the ad-hoc ones are marked below.

## 1. Runway And Burn

Prompt:

```text
What is our runway?
```

Best with:

- Mercury
- Ramp
- Stripe
- QuickBooks

Expected output:

- current cash included in runway;
- trailing burn calculation;
- runway in months;
- estimated cash-out date;
- caveats and open questions.

Try asking:

```text
Use the trailing three full months and show the monthly burn table.
```

## 2. Board Metrics

Prompt:

```text
Give me board metrics for last month.
```

Best with:

- Stripe
- Mercury
- Ramp
- QuickBooks

Expected output:

- ARR / MRR;
- cash;
- net burn;
- runway;
- AR and AP;
- short narrative for a board deck.

Try asking:

```text
Format this so I can paste it into a board deck.
```

## 3. Revenue Reconciliation

Prompt:

```text
Do Stripe and QuickBooks revenue tie out for last month?
```

Best with:

- Stripe
- QuickBooks

Expected output:

- Stripe gross activity;
- QuickBooks recognized revenue;
- timing, fees, refunds, deferred revenue, and non-Stripe adjustments;
- unexplained variance, if any.

Try asking:

```text
Show me the bridge from Stripe gross revenue to QuickBooks recognized revenue.
```

## 4. Add Context To The Finance Profile

Prompt:

```text
Add this board deck to my finance context.
```

Best with:

- any shared document or pasted context;
- existing Finance Context folder.

Expected output:

- source material saved in `context/`;
- relevant profile sections updated;
- open questions reduced where possible;
- changelog entry added.

Try sharing:

- investor update;
- close checklist;
- KPI sheet;
- revenue policy;
- finance team notes.

## 5. Review The Account Map

Prompt:

```text
Review the account map and show me which classifications still need a human decision.
```

Best with:

- QuickBooks
- existing `account-map.csv`

Expected output:

- deterministic mappings;
- judgment calls;
- blank or irregular rows;
- accounts whose name conflicts with their type;
- recommended questions for review.

## 6. Explain A Burn Change

*Ad-hoc — no dedicated workflow yet; Claude runs this using your profile.*

Prompt:

```text
Why did burn change this month?
```

Best with:

- QuickBooks
- Ramp
- Mercury

Expected output:

- month-over-month change;
- biggest drivers;
- recurring vs. one-time items;
- open questions where vendor/account treatment is unclear.

## 7. Find Recurring Vendor Themes

*Ad-hoc — no dedicated workflow yet; Claude runs this using your profile.*

Prompt:

```text
What recurring vendors should I review before the next close?
```

Best with:

- Ramp
- QuickBooks

Expected output:

- recurring vendors;
- likely department or reporting group;
- unusual increases;
- potential duplicate or stale tools;
- suggested follow-up questions.

## 8. Build A Custom Workflow

Prompt:

```text
Turn our monthly flux review into a reusable skill.
```

Best with:

- a workflow you just ran successfully;
- clear expected output format;
- connected systems needed for the dry run.

Expected output:

- a scoped workflow;
- a dry run against a recent period;
- a copy-ready `SKILL.md` if the workflow is validated.

Note: this beta may revamp or remove meta-skills before launch. Treat this use case as experimental.

## What To Watch For

Good outputs should:

- use your finance profile;
- name missing assumptions;
- avoid inventing values;
- show enough work for you to review;
- produce something you could refine into a board or operating deliverable.

If an answer feels generic, ask:

```text
Which part of finance-profile.md did you use for this answer?
```

