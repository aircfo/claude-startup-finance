---
name: setup-finance-brain
description: "Set up, refresh, or publish the company's Finance Brain handbook. Interviews you after reading your documents and connected finance systems, runs a follow-up with whoever owns the numbers to define metrics, burn, and runway, and can publish the handbook as an internal website. Use on first setup (when the Company at a glance section of CLAUDE.md is still placeholders), or when someone says \"set up my finance brain,\" \"build the handbook,\" \"refresh the handbook,\" \"add this to the handbook,\" \"define our metrics,\" \"interview our CEO,\" or \"publish the handbook.\""
---

# Set up the Finance Brain

**Purpose:** get the handbook built and keep it current. One flow, three stages, each in its
own file in this folder. Read a stage's file when you reach it, not before.

| Stage | File | What it does | Time |
| --- | --- | --- | --- |
| 1. Interview | `interview.md` | Reads the docs you share and your connected systems, drafts every page in `handbook/` and the at-a-glance section of `CLAUDE.md`, then asks only what they couldn't answer | 30 to 60 minutes |
| 2. Follow-up | `follow-up-questions.md` | About 30 minutes with whoever owns the numbers: metric definitions, burn and runway, the plan, reporting, people | About 30 minutes |
| 3. Publish (optional) | `publish-site.md` | Turns the handbook into a small internal website using `site-template/` | A few minutes |

## Pick where to start

- **First setup** (the Company at a glance section of `CLAUDE.md` is still mostly
  placeholders): start at stage 1. When it finishes, offer stage 2, then stage 3.
- **Refresh, or "add this to the handbook":** stage 1, following its "Refreshing later" section.
- **"Define our metrics," "interview our CEO,"** or `handbook/metrics-and-reporting.md` is mostly
  placeholders: stage 2.
- **"Publish the handbook," "rebuild the site":** stage 3.

If it isn't clear which stage the user wants, ask in one line. Each stage can be run on its own,
and the user can stop between stages and pick up later.

## Between stages

At the end of each stage, say in one or two lines what was done and what's still open, then
offer the next stage:

- After stage 1: "Want to do the follow-up now? It's best with whoever owns the numbers, and you
  can also take the questions to them and bring the answers back."
- After stage 2: "Want me to publish the handbook as an internal website?"
- After stage 3, or if the user stops: "Next, pick one task you know cold and use the
  `new-skill` skill."

## Rules for every stage

- **Read-only.** Read connected systems. Never write to them.
- **Placeholder, never guess.** Anything you can't support stays `[PLACEHOLDER: ...]` and is
  listed under Open questions in `CLAUDE.md` with an owner.
- **Log it.** Every stage that changes the handbook adds a Changelog line to `CLAUDE.md`.
- **The folder belongs to the user.** Never delete or move their files.
