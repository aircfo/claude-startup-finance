---
name: finance-skill-tuner
description: Diagnose and fix a finance skill that isn't behaving — one that won't trigger, fires when it shouldn't, skips a confirmation, eyeballs the math, or returns the wrong format. Use when someone says "my skill didn't fire," "fix my [X] skill," "it gave the wrong format," "it didn't ask me first," "improve my [X] workflow," or "this skill keeps doing the wrong thing."
---

# Finance Skill Tuner — diagnose and repair an authored skill

Finance workflows get refined over time. This skill takes a skill the user already authored (usually with `finance-skill-builder`) and fixes why it's misbehaving — in plain language, because the cause is almost always one of a handful of known ones.

## 1 · Find the skill
Look in `.claude/skills/` (this project), `~/.claude/skills/` (personal), and, when the session is working in a Finance Brain folder (a `CLAUDE.md` plus `handbook/` and `skills/`), that folder's `skills/`. A fix to a Finance Brain skill is made in its own `SKILL.md`, rerun into `testing/`, and logged in the folder's `CLAUDE.md` changelog. If the name is ambiguous, list the candidates and let the user pick. Read its `SKILL.md` end to end before changing anything.

## 2 · Diagnose against the common failure modes
Match the symptom the user describes to its usual cause:

| Symptom | Usual cause | Fix |
| --- | --- | --- |
| Didn't trigger when expected | `description` is too vague, or missing the phrase the user actually says | Rewrite the description: lead with what it does, add concrete trigger phrases in the user's words |
| Triggers when it shouldn't | `description` overlaps another skill or is too broad | Narrow it; spell out what it's *not* for |
| Re-derived the account setup / used the wrong accounts | Missing (or naive) **Step 0: read the Finance Brain** | Add the Step 0 block (current workspace's `CLAUDE.md` plus `handbook/`, otherwise ask the user for the folder), and name the handbook pages it depends on |
| Couldn't find the Finance Brain and guessed instead | Step 0 has no fallback | Have it ask the user where the Finance Brain folder is, and say so plainly (pointing to the kit) when there isn't one |
| Totals look wrong or inconsistent | Aggregates were eyeballed | Add the computation-step rule to **Always** |
| Finalized without checking | Missing a **Gate** | Add a confirmation gate before the output |
| Output is the wrong shape | Output template is vague or absent | Pin a concrete **Output format** |
| Touched a connector / leaked detail | Missing **Never** rules | Add the read-only + no-secrets guardrails |

If the symptom doesn't match the table, read the skill closely and find where its instructions are ambiguous — the spot where a careful reader could reasonably do two different things. That ambiguity is usually the bug.

## 3 · Propose the fix
Show the before/after for only the lines that change, and explain **why** in one sentence each — the user is non-technical, so say what the change does, not just that you made it. Leave everything that already works untouched.

## 4 · Apply and re-test
On confirmation, edit the file in place. Offer to re-run the skill against the connectors for a recent period to confirm the fix holds.

## Never
- Don't rewrite a skill wholesale to "clean it up" — change only what's broken, and preserve the user's logic and voice.
- Read-only against all connectors, including during any test run.
- Never store secrets, tokens, or full account numbers.
