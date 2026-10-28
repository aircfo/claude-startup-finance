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

## Step 0 · Read the Finance Brain

REPLACE or delete. If this skill reasons about company-specific finance definitions, read
the company's Finance Brain first (the `CLAUDE.md` and `handbook/` folder from the airCFO
Finance Brain Starter Kit) so it uses the company's own definitions of burn, runway, and
revenue. Name the handbook pages this skill depends on:

> Read `CLAUDE.md` and REPLACE: the pages this skill needs, e.g.
> `handbook/metrics-and-reporting.md` and `handbook/cash.md`. Look in the current workspace
> first; if there's no `CLAUDE.md` plus `handbook/` there, ask the user where their Finance
> Brain folder is. If there's none, say so and point to the kit
> (https://aircfo.github.io/claude-startup-finance/finance-brain.html), then continue with
> stated assumptions rather than silently inventing definitions. Treat any
> `[PLACEHOLDER` on a page you need as unknown.

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
