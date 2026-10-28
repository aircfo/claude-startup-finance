---
name: setup-finance-brain
description: "Set up, refresh, or publish the company's Finance Brain handbook (formerly the build-handbook, follow-up-interview, and build-handbook-site skills). Interviews you after reading your documents and connected finance systems, runs a follow-up with whoever owns the numbers to define metrics, burn, and runway, and can publish the handbook as an internal website. Use on first setup, or when someone says \"set up my finance brain,\" \"continue setup,\" \"refresh the handbook,\" \"add this to the handbook,\" \"define our metrics,\" \"do the follow-up,\" \"finish the handbook questions,\" \"publish the handbook,\" or \"build the handbook site.\""
---

# Set up the Finance Brain

**Purpose:** get the handbook built and keep it current. One flow, three stages, each in its
own file in this folder. Read a stage's file when you reach it, not before.

| Stage | File | What it does | Time |
| --- | --- | --- | --- |
| 1. Interview | `interview.md` | Reads the docs you share and your connected systems (or exports), drafts every page in `handbook/` and the at-a-glance section of `CLAUDE.md`, then asks only what they couldn't answer | 30 to 60 minutes |
| 2. Follow-up | `follow-up-questions.md` | With whoever owns the numbers: metric definitions, burn and runway, the plan, reporting, people | About 30 minutes |
| 3. Publish (optional) | `publish-site.md` | Turns the handbook into a small internal website using `site-template/` | A few minutes |

These stages used to be three separate skills: `build-handbook` (stage 1),
`follow-up-interview` (stage 2), and `build-handbook-site` (stage 3). A request that names one
of those means that stage.

## Pick where to start

Go by what the user asked for first. Look at the state of the folder only when the request is
general.

- **"Add this to the handbook," a shared document, "refresh" or "update the handbook":** run
  the refresh in `interview.md` ("Refreshing later"), then stop.
- **"Define our metrics," "interview our CEO," "do the follow-up," "finish the handbook
  questions":** stage 2.
- **"Publish the handbook," "build" or "rebuild the handbook site," "share the handbook with
  the team":** stage 3. If the Company at a glance section of `CLAUDE.md` is still mostly
  placeholders, say the site would be mostly empty and offer stage 1 first.
- **A general request** ("set me up," "help me get started," "continue setup"): check the
  Changelog in `CLAUDE.md` for "Setup stage" lines. None yet: stage 1. Stage 1 done but not
  stage 2: offer stage 2. Both done: ask what they'd like to do.

If it still isn't clear which stage the user wants, ask in one line.

## Between stages

During first setup, or when the user says "continue setup":

- When a stage finishes, add a Changelog line to `CLAUDE.md`, for example
  "YYYY-MM-DD: Setup stage 1 (interview) done. Next: follow-up." That line is how a later
  session knows where to pick up.
- After stage 1, offer stage 2 two ways: now, with whoever owns the numbers in the room, or as
  a list of questions to take to them (`follow-up-questions.md` explains both).
- After stage 2, offer stage 3.
- After stage 3, suggest a first monthly task: "Pick one task you know cold and use the
  `new-skill` skill." For a plan for the whole team, mention the `level-up` skill.
- If the user stops partway, tell them how to come back: "Say 'continue setup' any time."

After a refresh, or a single stage the user asked for by name, don't push them into other
stages. Confirm what changed, and if a `site/` folder exists, offer to rebuild it.

## Rules for every stage

- **Read-only.** Read connected systems. Never write to them.
- **Placeholder, never guess.** Anything you can't support stays `[PLACEHOLDER: ...]` and is
  listed under Open questions in `CLAUDE.md` with an owner.
- **Log it.** Every stage that changes the handbook adds a Changelog line to `CLAUDE.md`.
- **The folder belongs to the user.** Never delete or move their files.
