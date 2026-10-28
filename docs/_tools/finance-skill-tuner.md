---
title: Finance skill tuner
theme: build-your-own
order: 2
summary: Fix a skill that isn't behaving (won't trigger, fires when it shouldn't, skips a check, or returns the wrong format) with a plain-language diagnosis and a minimal fix.
plugin: all-systems-go
skill: finance-skill-tuner
ask: My runway skill didn't fire. Can you fix it?
reads: []
needs_contextos: false
time: A few minutes
---

## Common symptoms, and what it changes

| Symptom | Usual cause | Fix |
| --- | --- | --- |
| Didn't trigger when expected | The description is vague or missing the phrase you actually say | Rewrite it around what the skill does and the words you use |
| Triggers when it shouldn't | The description overlaps another skill | Narrow it, and say what it's *not* for |
| Used the wrong accounts | It doesn't read your ContextOS first | Add the step that loads your finance profile |
| Totals look wrong | Aggregates were eyeballed | Require a computation step |
| Finalized without checking | No confirmation step | Add one before the output |
| Wrong output shape | The output format is vague | Pin a concrete format |

## How it works

It reads your skill end to end, matches your symptom to a cause, and shows a before-and-after
of only the lines that change, with one sentence each on why. Nothing changes until you
confirm. Then it offers to re-run the skill against a recent period to prove the fix holds.

It never rewrites a working skill wholesale. Your logic and your voice stay intact.

## Try asking

```text
My board metrics skill keeps returning the wrong format. Fix it.
```
