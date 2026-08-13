---
name: REPLACE-skill-name
description: "REPLACE: what this skill produces, then the phrases that should trigger it. Pattern to follow: <One sentence on the outcome, naming the systems it reads.> Use when someone says \"REPLACE phrase one,\" \"REPLACE phrase two,\" \"REPLACE phrase three,\" or is doing REPLACE-the-task-context. This description is the trigger surface — an agent decides whether to run the skill from this text alone, so be specific about both the outcome and the wording a real user would use."
---

# REPLACE: Skill Title — what it produces

REPLACE: one short paragraph naming the deliverable and who reads it.

## What this produces

REPLACE: describe the concrete output — a file, a table in chat, a workbook, a drafted
summary. Be specific about where it's written and what it's named.

## Principles

REPLACE: the non-negotiables for this skill. Keep the ones that apply:

- **Read-only.** Never create, modify, send, or delete anything in a financial system.
- **Evidence or silence.** Every number cites where it came from. Never present an estimate
  as a figure from the books.
- **Fill or placeholder — never guess.** Mark gaps explicitly and surface them; don't invent
  a value to complete a section.
- **Confirm before anything outward-facing.** Draft; never send.
- **Degrade gracefully on partial access.** A blocked endpoint is partial, not failed: read
  what you can and mark the rest.
- **Always pass explicit date ranges** on dated report pulls — both a start and an end date.

## Step 0 · Load the ContextOS

REPLACE or delete. If this skill reasons about company-specific finance definitions, load
the finance profile first so it uses the company's own definitions of burn, runway, and
revenue:

> Look for the pointer file `.aircfo-finance-context.json` in the workspace; fall back to
> `~/Desktop/ContextOS/finance-profile.md`, then to the legacy
> `~/Desktop/airCFO Finance Context/finance-profile.md`. If no profile exists, say so and
> offer to run `/finance-context-builder` first — then continue with stated assumptions
> rather than silently inventing definitions.

## Steps

### 1 · REPLACE: first step

REPLACE: what to do, which tools to call, what to show the user.

### 2 · REPLACE: second step

REPLACE.

### 3 · REPLACE: present the result

REPLACE: the exact output shape. If there's a review gate, say what the user is ruling on
and wait for their answer before continuing.

## Output format

REPLACE: show the literal shape of the deliverable — a sample table, file tree, or section
headings — so runs are consistent.

## Failure modes

REPLACE: what to do when a connector isn't authorized, returns no data, or returns numbers
that look implausible. Never fabricate a result to complete the run; report what's missing.
