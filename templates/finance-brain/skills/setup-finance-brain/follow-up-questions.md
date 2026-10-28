# Stage 2: Follow-up interview

**Purpose:** fill the parts of the handbook that live in someone's head: what the metrics mean,
what the plan is, how reporting should work, and how people get paid. Run it after
the interview (stage 1), with whoever owns the numbers (founder, CEO, controller).
**If that person isn't in the room,** write the questions that are still open (after the
filtering below), each with its bracketed target, to
`handbook/sources/follow-up-questions-YYYY-MM-DD.md` for the user to take to them. When the
answers come back, fold each one into its page as below.

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

## Burn and runway (about 6 minutes)

6. "What counts as burn here: all cash out of the operating accounts, or something narrower?
   And is net burn that less what customers pay?" [metrics-and-reporting: Burn and runway]
7. "When you raise money or take on debt, do those deposits stay out of net burn? Are there
   one-time costs you leave out of run-rate burn, like a legal bill or an offsite?"
   [metrics-and-reporting: Burn and runway]
8. "Which accounts count as runway cash? Does a treasury or savings account count, or is it a
   reserve you don't touch?" Skip if `handbook/cash.md` already says. [cash: Rules]
9. "How do you calculate runway: runway cash divided by average net burn over how many closed
   months?" [metrics-and-reporting: Burn and runway]

## Plan and what's coming (about 6 minutes)

10. "Is there a budget or forecast? Where does it live, and is it the version to measure
   against?" [metrics-and-reporting: Plan and forecast]
11. "What's the hiring plan for the rest of the year?" [metrics-and-reporting: Plan and forecast]
12. "Any one-time costs or step changes coming: a price change, a big customer starting or
   ending, a migration?" [metrics-and-reporting: Known changes coming]
13. "Anything seasonal I should expect, and roughly how big is the swing?" [metrics-and-reporting:
   Seasonality]

## How reporting works (about 6 minutes)

14. "Who reads the monthly numbers, in what format, and what do they always ask about?"
    [metrics-and-reporting: Who reads the numbers]
15. "Can you share the last monthly package or board deck you liked?" Save it to
    `handbook/sources/`. [metrics-and-reporting: Preferred format]
16. "What size of month-over-month change deserves a sentence of explanation?" Skip if
    `handbook/close-process.md` already has a flux threshold. [close-process: Flux review]

## People (about 5 minutes)

17. "How do bonuses and commissions work, and when do they pay out?" [metrics-and-reporting:
    People and payroll]
18. "How are contractors and any international team engaged and paid?" [metrics-and-reporting:
    People and payroll]

## The last question, always

19. "What do you know about this business that the books would never tell me?"
    [company-overview: Things the books won't tell you]

## Finish

- Update "Last reviewed" on each page you changed.
- Add a Changelog line to `CLAUDE.md`: who was interviewed, which pages changed, and how many
  questions are still open.
- Show the user what's still a placeholder, grouped by owner.
- During first setup, add "Setup stage 2 (follow-up) done. Next: publish (optional)." to the
  Changelog and offer the next stage as `SKILL.md` describes.

## Never

- Never write to a connected system. Read the books only to check an answer or compute a number.
- Never guess. A definition or target the user doesn't give stays `[PLACEHOLDER: ...]`, listed
  under Open questions with an owner. Never fill one with a "typical" value.
- Never ask for tax or legal advice, or offer it. Record facts only.
