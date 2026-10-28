---
description: A 30-minute follow-up with whoever owns the numbers. Fills the metrics, plan, reporting, and people sections the books can't answer.
argument-hint: "[optional: who you're interviewing, e.g. 'our CEO']"
---

# Follow-up interview

**Purpose:** fill the parts of the handbook that live in someone's head: what the metrics mean,
what the plan is, how reporting should work, and how people get paid. Run it after
`commands/setup/build-handbook.md`, with whoever owns the numbers (founder, CEO, controller).
The person running the session can also take the questions to that person and bring answers
back.

## Before asking anything

1. Read `CLAUDE.md` and every page in `handbook/`.
2. Drop every question below that the handbook already answers. Never re-ask.
3. Never ask for a number that's in the books. Ask only for definitions, rulings, and context.
4. Tell the user how many questions are left and that the first ten minutes matter most. They
   can stop at any point.

Write each answer into the page shown in brackets as soon as it's given, replacing the matching
placeholder and citing it, for example "(CEO, follow-up interview 2026-10-28)". "I don't know"
is a fine answer: record who does know as an open question in `CLAUDE.md` and move on.

## The metrics (about 8 minutes)

1. "When someone asks how the business is doing, what three to five numbers do you reach for
   first?" Ask this before suggesting any metric. [metrics-and-reporting: The numbers we run on]
2. "What counts as recurring revenue here?" Name the boundary cases you saw in their books:
   trials, annual prepays, usage, services. [metrics-and-reporting; chart-of-accounts: Reporting
   rollups]
3. "Where's the customer list of record?" [metrics-and-reporting: Customers and revenue]
4. "What profitability lens matters most: burn and runway, gross margin, EBITDA? Is there a
   target?" [metrics-and-reporting]
5. "Gross margin came out at [computed from the books]%. Is that what you expect?" Compute it in
   a calculation step first. [metrics-and-reporting: target or benchmark]

## Plan and what's coming (about 6 minutes)

6. "Is there a budget or forecast? Where does it live, and is it the version to measure
   against?" [metrics-and-reporting: Plan and forecast]
7. "What's the hiring plan for the rest of the year?" [metrics-and-reporting: Plan and forecast]
8. "Any one-time costs or step changes coming: a price change, a big customer starting or
   ending, a migration?" [metrics-and-reporting: Known changes coming]
9. "Anything seasonal I should expect, and roughly how big is the swing?" [metrics-and-reporting:
   Seasonality]

## How reporting works (about 6 minutes)

10. "Who reads the monthly numbers, in what format, and what do they always ask about?"
    [metrics-and-reporting: Who reads the numbers]
11. "Can you share the last monthly package or board deck you liked?" Save it to
    `handbook/sources/`. [metrics-and-reporting: Preferred format]
12. "What size of month-over-month change deserves a sentence of explanation?" Skip if
    `handbook/close-process.md` already has a flux threshold. [close-process: Flux review]

## People (about 5 minutes)

13. "How do bonuses and commissions work, and when do they pay out?" [metrics-and-reporting:
    People and payroll]
14. "How are contractors and any international team engaged and paid?" [metrics-and-reporting:
    People and payroll]

## The last question, always

15. "What do you know about this business that the books would never tell me?"
    [company-overview: Things the books won't tell you]

## Finish

- Update "Last reviewed" on each page you changed.
- Add a Changelog line to `CLAUDE.md`: who was interviewed, which pages changed, and how many
  questions are still open.
- Show the user what's still a placeholder, grouped by owner.

## Never

- Never fill a definition or target with a "typical" value. If they don't answer, it stays a
  placeholder.
- Never ask for tax or legal advice, or offer it. Record facts only.
