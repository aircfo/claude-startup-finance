---
description: Turn one recurring task you know cold into a reusable command. Recreates last month's version, compares it to the real one until it matches, then writes the command.
argument-hint: "[the task, e.g. 'monthly software accrual']"
---

# Create a new command

**Purpose:** go from "I do this by hand every month" to a command anyone on the team can run.
The trick is to start from a finished example: Claude rebuilds last month's version, and the
real one is the answer key.

## Pick the right first task

Good first tasks:

- You know it cold and could explain every number.
- It happens every month, the same way.
- Last month's finished, reviewed version exists.
- The inputs are a report you can export or a system Claude can read.

Bad first tasks: anything new, anything that changes shape every month, or your most complex
reconciliation. Start simple. The goal of the first session is one command that works.

## Steps

### 1. Gather the example

Ask the user for:

- Last month's finished workpaper for this task.
- The inputs it was built from: exports, or which connected system and report.
- Where the final version gets saved.

Read the handbook pages the task touches (`accounting-policies.md` and `chart-of-accounts.md`
for a JE, `cash.md` for a rec).

### 2. Explain it back, then ask

Study the example: tabs, columns, formulas, where each number comes from, how the result
becomes a journal entry or a sign-off. Then explain the task back to the user in plain
language, step by step, and ask about anything you couldn't infer:

> "Here's how I think this works: [steps]. A few things I can't tell from the file: [questions]."

You can usually figure out more than the user expects. Ask only about the gaps.

### 3. Recreate last month

Using last month's inputs, rebuild the workpaper from scratch following
`commands/_templates/journal-entry.md` or `commands/_templates/reconciliation.md`. Save it to
`testing/` with " - TEST" at the end of the file name.

### 4. Compare to the real one

Compare your version to the real one, number by number. Show a table of every difference and
explain each one. Then fix the method, not the numbers, and rebuild. Repeat until it matches,
or until every remaining difference is one the user agrees the original got wrong.

### 5. Write the command

Copy the closest template from `commands/_templates/` into the right workflow folder
(`commands/jes/`, `commands/recs/`, or a new folder) with a short, specific file name, for
example `commands/jes/software-accrual.md`. Fill in every section: purpose, read first, inputs,
steps, output, checks, never. Write steps specific enough that a new hire running it gets the
same answer.

Add a row to the Commands table in `CLAUDE.md` and a Changelog line.

### 6. Run it for real, into testing

Run the new command for the current period. Save the output to `testing/`. Someone other than
the person who ran it reviews it.

When it has passed review (we suggest two clean months), change the command's output location
from `testing/` to the real close folder.

## Never

- Never skip the comparison in step 4. A command that hasn't matched a known-good result isn't
  done.
- Never hardcode a number the source data should drive.
- Never write to a connected system.
