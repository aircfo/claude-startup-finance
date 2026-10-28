---
name: new-skill
description: "Turn one recurring finance task someone knows cold into a reusable skill. Rebuilds last month's version in testing/, compares it to the real one until they match, then writes the skill from what worked. Use when someone says \"automate my monthly [task],\" \"make this a skill,\" \"turn this rec or JE into something repeatable,\" or \"add a new skill.\""
---

# Create a new skill

**Purpose:** go from "I do this by hand every month" to a skill anyone on the team can run.
The trick is to start from a finished example: Claude rebuilds last month's version, and the
real one is the answer key.

## Pick the right first task

Good first tasks:

- You know it cold and could explain every number.
- It happens every month, the same way.
- Last month's finished, reviewed version exists.
- The inputs are a report you can export or a system Claude can read.

Bad first tasks: anything new, anything that changes shape every month, or your most complex
reconciliation. Start simple. The goal of the first session is one skill that works.

## Steps

### 1. Gather the example

Ask the user for:

- Last month's finished workpaper for this task. If you just ran the task together in this
  conversation and the user confirmed the result, that result can be the answer key instead.
- The inputs it was built from: exports, or which connected system and report.
- Where the final version gets saved.

Read the handbook pages the task touches: `workpaper-standard.md` always, then
`accounting-policies.md` and `chart-of-accounts.md` for a JE, or `cash.md` for a rec.

### 2. Explain it back, then ask

Study the example: tabs, columns, formulas, where each number comes from, how the result
becomes a journal entry or a sign-off. Then explain the task back to the user in plain
language, step by step, and ask about anything you couldn't infer:

> "Here's how I think this works: [steps]. A few things I can't tell from the file: [questions]."

You can usually figure out more than the user expects. Ask only about the gaps. When an
answer is a policy (a threshold, a reversal convention, which account something maps to),
write it into the handbook page it belongs on and have the skill read it from there, so the
policy lives in one place.

### 3. Recreate last month

Using last month's inputs, rebuild the workpaper from scratch following
`handbook/workpaper-standard.md`. Save it to
`testing/` with " - TEST" at the end of the file name.

### 4. Compare to the real one

Compare your version to the real one, number by number. Show a table of every difference and
explain each one. Then fix the method, not the numbers, and rebuild. Repeat until it matches,
or until every remaining difference is one the user agrees the original got wrong.

### 5. Write the skill

First check `skills/` for an existing skill that covers the same task. If one is close, extend
it instead of adding a second. Otherwise pick a short, specific name in lowercase with hyphens,
for example `software-accrual`, whose description doesn't overlap another skill's, and
create `skills/{name}/SKILL.md` from the closest template in this skill's folder:
`skills/new-skill/templates/journal-entry-skill.md` or
`skills/new-skill/templates/reconciliation-skill.md`. For anything else, use the same
sections. Fill in every section: purpose, read first, inputs, steps, output, checks, never.
Write steps specific enough that a new hire running it gets the same answer.

The frontmatter `name` must match the folder name. Write the `description` as what the skill
does plus the phrases someone would actually say to ask for it ("book the software accrual,"
"accrue SaaS for September"). It's how Claude decides when to use the skill.

Add a row to the Skills table in `CLAUDE.md` and in `skills/README.md`, and a Changelog line.

### 6. Run it for real, into testing

Run the new skill for the current period. Save the output to `testing/`. Someone other than
the person who ran it reviews it.

When it has passed review (we suggest two clean months), change the skill's output location
from `testing/` to the real close folder.

Once it has passed review and saves time or catches mistakes, add a line to Wins under
"Level-up progress" in `CLAUDE.md`, for example "2026-11: software accrual skill, 90 minutes to
15 minutes." Keep the five most recent. If the folder is a GitHub repository, make every change
from step 5 on (the new skill, its table rows, and this Wins line) on a branch and open a pull request, so someone other than you approves it.

## Never

- Never skip the comparison in step 4. A skill that hasn't matched a known-good result isn't
  done.
- Never hardcode a number the source data should drive.
- Never write to a connected system.
