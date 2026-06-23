---
name: finance-skill-builder
description: Turn a finance workflow into a reusable skill that fits this plugin's house style. Two ways in — capture a workflow you just ran in this conversation, or build one from scratch through a short interview. Use when someone says "make this a skill," "save what we just did," "turn this into a workflow," "build me a skill for [X]," "automate my monthly [X]," or wants to repeat an analysis without re-explaining it each time.
---

# Finance Skill Builder — author a workflow skill that fits the house

Write a new finance workflow skill into the user's own workspace, so a finance professional can capture *their* workflow — not a one-size-fits-all template — and have it follow the same conventions as the built-in skills (`runway-and-burn`, `revenue-reconciliation`, `board-metrics`).

The hard part of authoring a skill isn't the markdown — it's pinning down the tacit steps a finance person runs on autopilot. This skill does that extraction for them, then bakes in the non-negotiables so they never have to know those rules exist.

## What this produces
A new skill at `.claude/skills/<name>/SKILL.md` in the current working directory — committable to the company's finance repo, and it loads automatically in that project. Offer `~/.claude/skills/<name>/` instead if the user wants it available in every project, not just this one.

Whichever location, the new skill inherits the house rubric below whether or not the user mentions any of it.

## The house rubric (always injected)
Every finance skill this builder writes must:
1. **Load `finance-profile.md` as Step 0** — read the company's semantic map before pulling data, so the skill never re-derives the account topology, the operating-vs-treasury split, or the pinned definitions. If the profile is missing, the skill tells the user to run `finance-context-builder` first.
2. **Be read-only** against every connector — never write to QuickBooks, Stripe, Ramp, or Mercury.
3. **Use a computation step for aggregates** — never eyeball totals across many transactions.
4. **Confirm the reporting period** before pulling data, and **state the as-of date** in the output.
5. **Show its work** — the inputs and sub-totals behind any headline number.
6. **Never store secrets** — names, last-4, and internal IDs only.

The user supplies *their* logic; the builder wraps it in these guardrails.

## Two on-ramps

### A · Capture what we just did (the fast path)
Use when the user just ran an analysis in this conversation and wants to keep it. Reconstruct the skill from what actually happened — don't re-interview:
- **Triggers** ← what the user originally asked, in their own words (plus a couple of natural paraphrases).
- **Data to gather** ← which connectors/tools were called, which reports, and over what window.
- **Logic** ← the actual steps taken, in order — then generalized: replace the specific month and figures with parameters, keep the structure.
- **Gates** ← any point where you paused to confirm something with the user.
- **Output format** ← the shape of the answer you gave, turned into a reusable template.

Show the reconstructed draft and confirm before writing.

### B · Build from scratch (the interview)
Use when there's no prior run to capture. Ask in small clusters — not all at once — because the user is putting tacit work into words for the first time:
1. **Trigger** — "What would you *say* to kick this off?" Capture their exact phrasing → the `description`.
2. **Inputs** — "Which systems does it pull from, and over what period?" → data to gather.
3. **Logic** — "Walk me through it step by step, the way you'd do it by hand." → the deterministic steps. Probe for the decisions they skip past.
4. **Gates** — "Is there anything a human should confirm before this is final?" → the gate(s).
5. **Output** — "What does the finished thing look like? Paste an example if you have one." → output template.
6. **Guardrails** — "Anything it should never do?" → Never rules, on top of the defaults.

## Skill template (what gets written)
Mirror the built-in skills exactly:

```markdown
---
name: <kebab-case-name>
description: <what it does + concrete trigger phrases in the user's own words: "Use when someone asks ...">
---

# <Title>

<One-line purpose.>

## When to use this
<Trigger conditions.>

## Step 0 — Load the finance profile
Read `finance-profile.md` first (the company's semantic map). <Name the specific definitions/accounts this skill relies on.> If it doesn't exist, run `finance-context-builder` first.

## Data to gather
<Connectors, reports, window.>

## Logic / Calculation
<Deterministic, numbered steps.>

## Gate (if any)
<What to confirm with the human before finalizing.>

## Always
- Use a computation step for aggregates.
- State the reporting period and as-of date.
- Show your work.

## Output format
<Concrete template the user can reuse.>

## Never
- Read-only — never write to a connector.
- Never store secrets, tokens, or full account numbers.
```

## Before writing — the quality bar
- **Name**: kebab-case, distinct from existing skills. Check `.claude/skills/`, `~/.claude/skills/`, and the plugin's own skills so the new one doesn't collide with or shadow another.
- **The description is the make-or-break field** — it's the only thing Claude sees when deciding whether to trigger this skill. Spend real effort here: lead with what it does, then several concrete trigger phrases in the user's own words. A vague description is the #1 reason a skill never fires.
- **Steps must be deterministic** — a stranger could follow them and reach the same answer. If a step is fuzzy, ask; don't paper over it.
- Show the full draft and get an explicit yes before writing the file.

## After writing
- Confirm the path, and tell the user it loads automatically next session (project skill) or in every project (personal skill).
- Offer to **test it now** against the connectors for a recent period, so they watch it work before relying on it.
- If it misbehaves later, point them to `finance-skill-tuner`.

## Never
- Never write the new skill into the installed plugin directory — it belongs in the user's workspace, where it survives plugin updates.
- Never invent the user's logic — if a step is unclear, ask. A wrong skill is worse than no skill.
- Read-only against all connectors, including during any test run.
