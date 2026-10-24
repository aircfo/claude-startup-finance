# Running a first-install test

How to watch someone set this up for the first time and turn what they hit
into fixes. Use it for each new operator and each outside beta tester; every
real install so far has found something.

## Who and what

- **The tester** is the person who will actually own setup (an Ops lead, not
  whoever wrote or configured the skill). They get only the repository README
  and `USER_GUIDE.md` — no walkthrough, no hints.
- **The observer** watches (screen share or over the shoulder) and says
  nothing unless the tester is stuck for more than five minutes, and then only
  enough to unstick them. Every intervention is written down: it is the most
  important data from the session.
- **The other roles** (claude.ai Owner, Console admin, Ramp admin) are
  reachable by message, as they would be in real life. Their response time is
  part of the result, not something to hide.

## Before the session

1. A Mac with the prerequisites in the user guide's "Before you start", and
   the skill installed from the marketplace (not a repository checkout).
2. A brand-new workspace path the tester chooses. Don't reuse an existing one.
3. Ask the tester to talk aloud: what they think each step wants, what they
   expect to happen, what surprises them.

## During

Note, with the time:

- each time they stop to work out what a message means;
- each time they leave the chat (to find a setting, a file, a person);
- each hand-off message they send to another role, and when it was answered;
- anything they do that the docs didn't tell them to;
- every observer intervention, verbatim.

## Measures

| Measure | Where it comes from | Target |
|---|---|---|
| Time to first green checkup | `doctor.py` prints it ("Setup took N minutes"), computed from `logs/setup.jsonl` | Under 45 minutes of the tester's own time, not counting waits on other roles |
| Observer interventions | Session notes | Zero |
| Questions to the person who built it | Session notes | Zero |
| First dashboard correct | `reconcile.py` against the month's invoices once it closes | Every surface within $1.00 or 0.5% |

Waiting on other roles is reported separately: it measures how clear the
hand-off messages were, not how hard setup is.

## After

1. Add a row to `references/setup-pitfalls.md` for every stop, intervention or
   surprise, with its root cause.
2. For each, decide what catches it next time: a doctor check, a clearer fix
   message, a script that removes the step, or a doc change. Prefer the first
   three; a doc change only helps people who read it.
3. If the skill (Claude) said or did something wrong, add an eval case under
   `plugins/ai-cfo-lab/evals/` that reproduces it, then fix the skill until it
   passes.
4. Share the timing and the list with the tester; ask what they'd change.
