---
title: Use Cases And Prompts
---

# Use Cases And Prompts

Use these prompts after you've built a first version of your [Finance Brain]({{ '/finance-brain.html' | relative_url }}) and opened its folder in Cowork.

Each use case lists the connectors that make the workflow strongest. If a connector is missing, Claude should say what is incomplete and leave open questions rather than guessing.

Some of these map to a dedicated workflow: runway and burn, board metrics, and revenue reconciliation. Others, like explaining a burn change or finding recurring vendors, are ad-hoc analyses Claude runs using your handbook and connected systems. Either way you just ask; the ad-hoc ones are marked below.

Each dedicated workflow also has its own page in the [tool library]({{ '/' | relative_url }}#tools), with what it reads and exactly what to install.

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

## 4. Add Context To Your Handbook

Prompt:

```text
Add this board deck to the handbook.
```

Best with:

- any shared document or pasted context;
- your Finance Brain folder open in Cowork.

Expected output:

- the source saved in `handbook/sources/`;
- the relevant handbook pages updated, placeholders replaced where the document answers them;
- a changelog line in `CLAUDE.md`.

Try sharing:

- investor update;
- close checklist;
- KPI sheet;
- revenue policy;
- finance team notes.

## 5. Define Your Metrics

Prompt:

```text
Use the follow-up-interview skill with me.
```

Best with:

- whoever owns the numbers (founder, CEO, or controller);
- a past board deck or monthly package.

Expected output:

- `handbook/metrics-and-reporting.md` filled in: your metric definitions, burn and runway rules,
  plan, and who reads the numbers;
- anything unanswered listed as an open question with an owner.

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
- likely department and expense category;
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

## What To Watch For

Good outputs should:

- use your handbook's definitions;
- name missing assumptions;
- avoid inventing values;
- show enough work for you to review;
- produce something you could refine into a board or operating deliverable.

If an answer feels generic, ask:

```text
Which handbook pages did you use for this answer?
```

