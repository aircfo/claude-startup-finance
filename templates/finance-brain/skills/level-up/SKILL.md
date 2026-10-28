---
name: level-up
description: "Coach a finance team up the ladder for AI in finance: work out where the team is today, pick the next one or two moves, walk through the first one step by step, and keep track of progress in CLAUDE.md. Covers rolling the Finance Brain out to a team and the full GitHub and Claude Code setup for reviewing changes. Use when someone says \"help me level up,\" \"what's our next rung,\" \"what should our team do next with Claude,\" \"how do I get my team using this,\" \"roll this out to the team,\" \"set up GitHub,\" \"install Claude Code,\" or asks how to get better at using Claude for finance work."
---

# Level up

**Purpose:** help a finance team get more out of Claude, one rung at a time, without assuming
anyone is technical. Work out where the team is, do the next move with them, and record
progress so the next session picks up where this one stopped.

Two files in this folder hold the detail. Read them when you need them, not up front:

- `ladder.md`: each rung for a team, what "done" looks like, the moves to the next rung, and
  common blockers.
- `github-setup.md`: the step from rung 3 to rung 4. Installing Git, Node.js, Python, VS Code,
  and Claude Code, putting the Finance Brain in a private GitHub repository, and setting up
  review so the author is never the approver.

## How to teach

The people using this are accountants, controllers, and founders, not engineers.

- **Big picture first.** Before any step, say in two sentences what it gets them and why it
  matters for their work.
- **One step at a time.** Give one step, wait for them to do it, then check it worked before
  the next one.
- **Explain every term the first time you use it,** in plain words (for example, "a
  repository, or repo, is a folder that keeps every version of every file").
- **Anything they type goes in a code block,** with one line on what it does. Say where to type
  it: their computer's Terminal (Mac) or PowerShell (Windows), not this chat. Ask them to paste
  back what it printed.
- **If something breaks, fix it before moving on.** Read the error with them and explain it in
  plain words.
- **Recommend the simpler path** when one exists, even if they asked for the harder one, and
  say why.

## Steps

### 1. Read where they are

If this folder is a GitHub repository (the team is on rung 4 or above), get the latest first
(`git pull`), so you read the team's current progress, not an old copy.

Read the "Level-up progress" section of `CLAUDE.md` and the Changelog. "Setup stage" lines
tell you how far the handbook setup has got. If Rung says "not assessed yet," go to step 2.
Otherwise say it back in one line ("Last time you were on rung 1, and the next step was
connecting the bank. Pick up there?"), use the Team line instead of asking again, and go to
step 4. If the last step was partway through `github-setup.md`, pick up at the next step there.

### 2. Check in (first time only)

Ask these, a couple at a time, in plain words:

1. How does the team use Claude today? Not yet, one-off questions, a few repeat tasks, or
   connected to your systems?
2. How many people are on the finance team, and who reviews whose work?
3. Which systems hold the numbers (accounting system, bank, card platform, billing,
   spreadsheets)?
4. Mac or Windows? And do you use Claude Cowork (the desktop app's Cowork tab), Claude Code
   (Claude working in a folder from the terminal or VS Code), or both? It's fine not to know
   yet.
5. Which task eats the most time every month?

### 3. Place the team on a rung

Read `ladder.md` and pick the rung whose "done" list best matches the answers. Tell them the
rung in one sentence and what the next rung would change for them ("Right now each of you
explains the chart of accounts to Claude every time. On rung 3 you write it down once, and
everyone's Claude reads it.").

### 4. Pick the next one or two moves

From `ladder.md`, choose at most two moves toward the next rung, starting with the one that
helps with the task they named in question 5. Say what each move takes (time, who's needed,
any accounts or installs).

### 5. Do the first move together

Run it now if they have the time. Many moves hand off to another skill:

- turn a task into a skill: `new-skill`
- write down how the team works: `setup-finance-brain`
- version control and review (rung 3 to 4): follow `github-setup.md` step by step

If they can't do it now, write the move as the next step in progress and stop.

### 6. Record progress

Update the "Level-up progress" section of `CLAUDE.md`:

- **Team:** size, Mac or Windows, Cowork or Claude Code, and the task that takes the most
  time, from the check-in, so nobody has to answer twice.
- **Rung:** the rung the team is on now.
- **Last step:** what you just did, with the date.
- **Next step:** the one thing to do next, specific enough that anyone on the team could start
  it.
- **Wins:** when a move saved time or caught a mistake, add one line, for example
  "2026-10: usage accrual skill, 2 hours to 20 minutes." Keep the five most recent.

Add a Changelog line too. If the folder is a GitHub repository, make these updates on a
branch and open a pull request (or add them to the pull request for the change you just made),
so the team's copy stays the one source of truth. During `github-setup.md` itself, leave
progress edits uncommitted until step 12's practice pull request, which carries them. Then
tell them how to come back: "Say 'help me level up' any time,
and I'll pick up from here."

## Never

- Never ask anyone to paste a password, token, or full account number into the chat. Sign-ins
  happen in their browser.
- Never write to a connected system. Connections stay read-only.
- Never put real financial data in a GitHub repository unless the company has decided that's
  allowed. `github-setup.md` keeps workpapers and exports out by default.
- Never skip a check because the person seems confident. Confirm each install worked before
  the next one.
