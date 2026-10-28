---
title: Finance skill builder
theme: build-your-own
order: 1
summary: Turn a workflow your team already runs (a flux review, a vendor check, a monthly tie-out) into a reusable skill of your own, built to the same standards as the tools in this library.
plugin: all-systems-go
skill: finance-skill-builder
ask: Turn what we just did into a skill.
reads: []
needs_contextos: true
time: 10 to 20 minutes per skill
---

## Two ways in

- **Capture what you just did.** Run an analysis with Claude, then say "save what we just
  did." The builder generalizes it, so the period and figures become inputs, and re-runs it
  to confirm it reproduces your result.
- **Start from scratch.** Say "build me a skill for our monthly flux review." A short
  interview pins down the trigger, the inputs, the logic, the checks, and the output, then
  a dry run against a recent period tests it.

## The standards it builds in

Every skill it writes follows the same rules as the tools here:

1. **Reads your ContextOS first**, so it never re-derives your accounts or definitions.
2. **Read-only** against every connected system.
3. **Computes, never eyeballs.** Totals run in a computation step.
4. **Ties out to a control total** wherever one exists, and reports the match or the variance.
5. **Confirms the period** before it runs, and shows its work.
6. **No secrets** in the skill or its output.

## Where your skills live

In your own workspace (`.claude/skills/` in a project, or `~/.claude/skills/` to use
everywhere), never inside the installed plugin. Your skills survive every update.

## Try asking

```text
Build me a skill for our monthly flux review.
```
