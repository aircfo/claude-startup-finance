# The 30-Minute Intake — the questions your connectors can't answer

Connectors fill most of a ContextOS: the account map, the balances, the vendor list, the
revenue mix. What they *can't* fill is anything that lives in someone's head — definitions,
policies, intents, and rulings. This template turns those gaps into one timeboxed
conversation with whoever owns the numbers (founder, CFO, controller). Every question
targets a specific profile section, so the answers fill the map instead of generating notes.

**Ground rule for the interviewer (human or Claude):** the systems data is already pulled —
never ask for a number that's in the books. Ask only for *rulings, definitions, and
context*. Front-load: the first ten minutes carry the most value.

**How to use it:** Claude adapts this template after a build — Block 1 is generated from
the actual flagged judgment calls in *your* account map and open questions, and any question
the build already answered (from your context docs or systems) gets skipped, never re-asked.

---

## Block 1 — Rulings the books can't make for themselves (0:00–0:07)

*Generated per company from the build's `needs-review` queue and §13 Open Questions. Each is
a 30-second answer that unblocks automated reporting; without a ruling, every future report
has to hedge. Typical shapes:*

1. **The identity check** — "The systems disagree about your legal name / entity type.
   What's current?" *Entity type drives how draws, distributions, and 'net income' should
   be read.* → §1
2. **The cash-perimeter ruling** — "Does [your treasury / brokerage / sweep account] count
   as cash-on-hand, or is it a reserve you deliberately don't touch?" *Every cash and
   runway number hinges on this yes/no.* → §6
3. **The odd-account walkthrough** — "Walk me through [the account whose mechanics are
   visible but whose intent isn't — a manual accrual layer, a clearing account that doesn't
   clear, a negative asset]." *The answer determines how reports should read it and whether
   a reclass is wanted.* → §7/§12
4. **The unlabeled-bucket ruling** — "A material amount posts straight to [a parent
   account / a catch-all]. Deliberate bucket, or should it get sub-accounts?" *Decides
   whether reporting shows it as-is or flags it monthly.* → §12, account map
5. **The unexplained number** — "What is [the largest unexplained line in the books]?"
   *Could be a one-time to exclude from run-rate, or misclassified revenue.* → §13 → §12
6. **The invisible rail** — "What goes on [the card/account with no connector], and why
   keep it?" *Tells Claude what category of spend or cash it's blind to, so analyses carry
   an accurate caveat instead of silently under-reporting.* → §8

## Block 2 — The metrics you actually run the business on (0:07–0:15)

*Definitions are conventions, not data — no connector can answer these. The heart of the call.*

7. **"When you tell someone how the business is doing, what 3–5 numbers do you reach for
   first?"** *Open-ended on purpose — it reveals the real KPI set before anchoring them
   with candidates.* → §3
8. **"What counts as recurring revenue here?"** — name the boundary cases from their own
   books (trials? annual prepays? seasonal-but-recurring lines? usage?). *This defines
   their MRR/ARR — the single most-quoted metric — and the `mrr` tag set in the account
   map.* → §3
9. **"Where's the customer list of record?"** (billing system, the GL, CRM, a
   spreadsheet?) *Revenue-per-customer and concentration metrics need a source of truth
   before anyone pulls customer-level data.* → §3, §4
10. **"Is there a per-unit or utilization metric you watch?"** (utilization for services;
    per-seat or usage economics for software). *Usually the #1 driver of gross margin —
    and often lives in a system that isn't connected yet.* → §3, §4
11. **"What's the profitability lens you actually care about?"** — burn and runway? EBITDA?
    owner earnings after draws? Is there a target? *Tells Claude what 'good' looks like in
    every report it writes.* → §3, §6
12. **"Your gross margin came out at [computed]% — is that where you expect it, and is
    there a target?"** *Converts a computed number into a benchmark, and the monthly P&L
    into an exceptions report instead of a data dump.* → §3, §10

## Block 3 — Plan, forecast, and what's coming (0:15–0:21)

*Cheap questions, huge leverage: variance-vs-plan is the core of monthly reporting.*

13. **"Is there a budget or forecast? Where does it live, and is it still the version
    you'd want variance measured against?"** *If yes, every monthly report gains a plan
    column. If no, that's a finding in itself.* → §10
14. **"What's the hiring plan for the rest of the year — roles, teams, rough timing?"**
    *In a people-cost-heavy business, headcount adds ARE the forecast.* → §9, §10
15. **"Any known one-times or step-changes coming — price changes, a big customer starting
    or ending, an offsite, a system migration?"** *Forward-looking exceptions make trend
    commentary honest ("the spike is the offsite, not a run-rate change").* → §10, §12
16. **"Anything seasonal I should expect? Roughly how big is the swing?"** *Prevents
    normal patterns from being flagged as anomalies every year.* → §2

## Block 4 — How reporting should work here (0:21–0:26)

*These answers configure every future deliverable's shape, timing, and threshold.*

17. **"Walk me through your month-end close: who does it, what's the target day, and what
    does 'done' mean?"** *Tells Claude when monthly numbers are trustworthy — reporting
    off a half-closed month is the classic automation failure.* → §11
18. **"What variance size is worth a sentence of explanation — a dollar amount, a
    percentage, or both?"** *The materiality threshold is the single setting that most
    controls report length and usefulness.* → §11
19. **"Who reads the monthly numbers, in what format, and what do they always ask
    about?"** *The audience, the template, and the recurring questions a report should
    pre-answer.* → §11
20. **"Show me (or send me) the last monthly package or dashboard you liked."** *One
    artifact beats ten style questions — it goes straight into `context/`.* → context/, §11

## Block 5 — People mechanics & the last blind spots (0:26–0:30)

21. **"How do bonuses / commissions / profit-sharing work, and when do they pay out?"**
    *Lets Claude accrue and forecast comp instead of treating it as noise.* → §9
22. **"How do contractors and any international team get engaged and paid?"** *Explains
    FX lines, timing quirks, and where headcount data lives outside payroll.* → §9
23. **"Last one: what do you know about this business that the books would never tell
    me?"** *The deliberate catch-all — every finance function has two or three of these
    ("that customer always pays 60 days late," "we under-bill X on purpose"). They go
    straight to Known Exceptions — the section that makes AI-assisted reporting
    trustworthy instead of merely plausible.* → §12

---

## What this call deliberately skips

- **Anything already in the systems** (balances, spend, revenue mix, vendor lists) —
  pulled and verified; asking wastes the 30 minutes.
- **Tax strategy and entity-restructuring advice** — out of scope for a reporting context;
  noted only as facts.
- **Deep process documentation** (full SOPs, customer-level detail) — follow-up material
  for `context/`, not call time.

**After the call:** answers get folded into the profile (placeholders replaced), rulings
land in §12 Known Exceptions, artifacts go to `context/`, and the changelog records the
ingestion.
