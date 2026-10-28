# Skills

A skill is a folder holding a `SKILL.md` file that tells Claude how to do one recurring task the
way your team does it. Anyone on the team can run it and get the same workpaper.

## Running a skill

**Claude Cowork:** in a session working in this folder, ask for the task or name the skill.
`CLAUDE.md` lists every skill, so Claude knows where to find it:

> "Use the `prepaid-amortization` skill for September 2026."

**Claude Code:** copy the folders in `skills/` into `.claude/skills/`. Claude then uses each
skill when a request matches its description, and you can run one directly as a slash command
named after its folder, for example `/prepaid-amortization 2026-09`.

Every skill asks for what it needs (a period, an account) if you don't say.

## The skills, by workflow

Each skill is its own folder, named for what it does. Grouped by workflow:

| Workflow | Skill | What it does |
| --- | --- | --- |
| Setup | `build-handbook/` | Drafts the handbook from your docs and systems, then asks only what they can't answer |
| Setup | `follow-up-interview/` | 30 minutes with whoever owns the numbers: metrics, plan, reporting, people |
| Setup | `new-skill/` | Turns a task you know cold into a new skill. Holds the JE and rec skill templates |
| Journal entries | `prepaid-amortization/` | Monthly prepaid amortization JE |
| Journal entries | `usage-accrual/` | Month-end accrual for usage-billed vendors |
| Reconciliations | `bank-reconciliation/` | Bank or card account to its statement |
| Publish | `build-handbook-site/` | Publishes the handbook as an internal website. Holds the site template |

When you add a skill, add its row here and in `CLAUDE.md`.

## Anatomy of a skill

Every `SKILL.md` has the same sections, so anyone can read one and know what it does:

1. **Frontmatter:** `name` (the folder name: lowercase, hyphens) and `description`. The
   description says what the skill does and the phrases someone would actually say to ask for
   it. It's how Claude decides when to use the skill, so make it specific.
2. **Purpose:** what it produces and when it runs in the close.
3. **Read first:** the handbook pages it depends on.
4. **Inputs:** what it needs and where each input comes from (a connected system, or a named
   export with a date range).
5. **Steps:** numbered, specific enough that two people get the same result.
6. **Output:** the workpaper, following `handbook/workpaper-standard.md`, with its file name
   and save location.
7. **Checks before handoff:** the tests the output must pass.
8. **Never:** the lines it doesn't cross.

Files a skill needs (a template, a reference) live inside its own folder.

## Adding a skill

Don't write one from scratch. Use the `new-skill` skill: Claude recreates last month's version
of the task, compares it to the real one until they match, and writes the skill from what
worked.

## Changing a skill

Skills are how the team's method improves. When a reviewer catches a problem:

1. Fix the skill (or the handbook page it reads), not just this month's output.
2. Rerun into `testing/` and compare to a known-good result.
3. Add a line to the changelog in `CLAUDE.md`: what changed, why, and who approved it.

If you keep this folder in Git, make each change a pull request and require someone other than
the author to approve it. That's the same review rule as the workpapers, applied to the method.
