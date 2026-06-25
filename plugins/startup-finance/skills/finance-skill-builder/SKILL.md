---
name: finance-skill-builder
description: Turn a finance workflow into a reusable skill that fits this plugin's house style. Two ways in — capture a workflow you just ran in this conversation, or build one from scratch through a short interview. Use when someone says "make this a skill," "save what we just did," "turn this into a workflow," "build me a skill for [X]," "automate my monthly [X]," or wants to repeat an analysis without re-explaining it each time.
---

# Finance Skill Builder — author a workflow skill that fits the house

Generate a new finance workflow skill for the user to save into their own workspace, so a finance professional can capture *their* workflow — not a one-size-fits-all template — and have it follow the same conventions as the built-in skills (`runway-and-burn`, `revenue-reconciliation`, `board-metrics`).

The hard part of authoring a skill isn't the markdown — it's pinning down the tacit steps a finance person runs on autopilot. This skill does that extraction for them, then bakes in the non-negotiables so they never have to know those rules exist.

## What this produces
A complete, house-style `SKILL.md`, **presented in the chat** for the finance pro to take — they can download it or drop it into their own skills folder. Don't write it to their disk for them; hand over the finished file and tell them exactly where it goes:
- **`~/.claude/skills/<name>/SKILL.md`** — available in every project (the usual home for a personal workflow).
- **`.claude/skills/<name>/SKILL.md`** in a project — scoped to that repo and committable to the company's finance repo.

Either way, the skill inherits the house rubric below whether or not the user mentions any of it.

## The house rubric (always injected)
Every finance skill this builder writes must:
1. **Load `finance-profile.md` as Step 0** — read the company's semantic map before pulling data, so the skill never re-derives the account topology, the operating-vs-treasury split, or the pinned definitions. The skill should locate it via the saved **airCFO Finance Context** pointer (a workspace `CLAUDE.md` note or `.aircfo-finance-context.json`), then the default `~/Desktop/airCFO Finance Context/` folder, then the current workspace. If it still can't be found, the skill tells the user to run `finance-context-builder` first and does not guess.
2. **Be read-only** against every connector — never write to QuickBooks, Stripe, Ramp, or Mercury.
3. **Use a computation step for aggregates** — never eyeball totals across many transactions.
4. **Cite the source of every figure** — name the connector, report, and pull date behind each number, so it traces back to the system of record.
5. **Tie out to a control total** — where a control exists, reconcile to it (detail sums to the summary; a cross-system tie like Stripe ↔ QBO) and report the match or the variance. Never present a number that doesn't foot.
6. **Flag gaps, never fabricate** — if a figure can't be sourced or reconciled, flag it as an open item with a suggested next step; never fill the hole with a plausible-looking guess.
7. **Show its work** — the inputs and sub-totals behind any headline number.
8. **Confirm the reporting period** before pulling data, and **state the as-of date** in the output.
9. **Never store secrets** — names, last-4, and internal IDs only.

The user supplies *their* logic; the builder wraps it in these guardrails.

## The build sequence
Always run in this order — **scope → dry-run → deliver**:
1. **Scope** the workflow (via an on-ramp below): pin the trigger, inputs, logic, gates, and output shape.
2. **Dry-run** the drafted logic against the live connectors for a real recent period — *before* writing anything — and confirm with the user that the output is correct and ties out.
3. **Deliver** the finished `SKILL.md` in chat for the user to save — don't write it to disk for them.

## Two on-ramps

### A · Capture what we just did (the fast path)
Use when the user just ran an analysis in this conversation and wants to keep it. Reconstruct the skill from what actually happened — don't re-interview:
- **Triggers** ← what the user originally asked, in their own words (plus a couple of natural paraphrases).
- **Data to gather** ← which connectors/tools were called, which reports, and over what window.
- **Logic** ← the actual steps taken, in order — then generalized: replace the specific month and figures with parameters, keep the structure.
- **Gates** ← any point where you paused to confirm something with the user.
- **Output format** ← the shape of the answer you gave, turned into a reusable template.

Show the reconstructed draft and confirm before finalizing.

### B · Build from scratch (the interview)
Use when there's no prior run to capture. Ask in small clusters — not all at once — because the user is putting tacit work into words for the first time:
1. **Trigger** — "What would you *say* to kick this off?" Capture their exact phrasing → the `description`.
2. **Inputs** — "Which systems does it pull from, and over what period?" → data to gather.
3. **Logic** — "Walk me through it step by step, the way you'd do it by hand." → the deterministic steps. Probe for the decisions they skip past.
4. **Gates** — "Is there anything a human should confirm before this is final?" → the gate(s).
5. **Output** — "What does the finished thing look like? Paste an example if you have one." → output template.
6. **Guardrails** — "Anything it should never do?" → Never rules, on top of the defaults.

## Dry-run before you deliver it (don't skip this)
A finance pro won't trust a skill whose math they've never seen work — so once the workflow is scoped, **run it**, don't just describe it:
- Execute the drafted logic against the **live connectors** for a concrete recent period (read-only).
- Show the user the actual output and **how each figure ties out** to its source.
- Refine the logic with them until the result is right. *This* validated run is what the `SKILL.md` will encode.

On-ramp A (capture): the analysis already ran, so re-run the **generalized** version (period and figures parameterized) to confirm it reproduces what you just did. On-ramp B (interview): this is the skill's first real execution — treat a wrong or unverifiable result as a sign the logic isn't pinned down yet.

Only once the dry-run is correct and the user has confirmed it do you finalize the file.

## Skill template (what you'll hand over)
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
Read `finance-profile.md` first (the company's semantic map). <Name the specific definitions/accounts this skill relies on.> Find it in this order: (1) an **airCFO Finance Context** pointer in this session's instructions (e.g. a workspace `CLAUDE.md`); (2) `.aircfo-finance-context.json` in the current workspace (`financeProfile`); (3) the default `~/Desktop/airCFO Finance Context/finance-profile.md`; (4) the current workspace. If you still can't find it, run `finance-context-builder` first — do not guess.

## Data to gather
<Connectors, reports, window.>

## Logic / Calculation
<Deterministic, numbered steps.>

## Gate (if any)
<What to confirm with the human before finalizing.>

## Always
- Cite the source of every figure (connector, report, pull date).
- Tie out to a control total where one exists; report the match or the variance.
- Flag anything you can't source or reconcile as an open item — never fabricate.
- Use a computation step for aggregates.
- State the reporting period and as-of date.
- Show your work.

## Output format
<Concrete template the user can reuse.>

## Never
- Read-only — never write to a connector.
- Never store secrets, tokens, or full account numbers.
```

## Before you hand it over — the quality bar
- **Name**: kebab-case, distinct from existing skills. Check `.claude/skills/`, `~/.claude/skills/`, and the plugin's own skills so the new one doesn't collide with or shadow another.
- **The description is the make-or-break field** — it's the only thing Claude sees when deciding whether to trigger this skill. Spend real effort here: lead with what it does, then several concrete trigger phrases in the user's own words. A vague description is the #1 reason a skill never fires.
- **Steps must be deterministic** — a stranger could follow them and reach the same answer. If a step is fuzzy, ask; don't paper over it.
- **The dry-run passed** and the user confirmed the numbers tie out — never hand over logic you haven't watched work.
- Show the full draft and get an explicit yes before you hand over the file.

## Deliver the skill (in chat)
Present the finished `SKILL.md` **in the chat** — as a copy-ready block or a downloadable file — so the finance pro can take it. Don't write it to their disk for them.
- Tell them where to save it: `~/.claude/skills/<name>/SKILL.md` (every project) or `.claude/skills/<name>/SKILL.md` (this project, committable to the finance repo), and that it loads automatically once saved.
- Remind them the dry-run they just watched is the behavior the skill will repeat.
- If it misbehaves later, point them to `finance-skill-tuner`.

## Never
- Never write the skill to disk on the user's behalf — present it in chat so they choose where it lives; in particular never write into the installed plugin directory (it would be lost on update).
- Never ship a skill you haven't dry-run — logic that was never executed is a guess, not a workflow.
- Never invent the user's logic — if a step is unclear, ask. A wrong skill is worse than no skill.
- Read-only against all connectors, including during the dry-run.
