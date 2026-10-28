# The ladder, for a team

Six rungs, from asking Claude one question at a time to work finance couldn't do before.
Each rung lists what "done" looks like for a team, the moves to the next rung, and what
usually gets in the way. A solo founder can follow the same ladder and skip the team moves.

## Rung 0: Chat

**Done looks like:** a few people ask Claude one-off questions ("explain this variance,"
"draft this email"). Nothing is saved, and everyone explains the same context their own way.

**Moves to rung 1:**
- **Each person picks one task they know cold** and turns it into a skill with `new-skill`.
  Start with something monthly and boring: a recurring accrual, a simple rec, a tie-out.
- **Share the first win** in a team meeting: the task, the time before and after, and what the
  reviewer caught. One real example persuades more than any pitch.

**Blockers:** "I don't trust it with numbers." Answer: every skill is checked against last
month's real result before anyone relies on it, and the person who ran it never approves it.

## Rung 1: Skills

**Done looks like:** two or three people each run a skill or two every month. The skills work,
but each person keeps their own, and the same policy is written down three different ways.

**Moves to rung 2:**
- **Connect the core systems read-only,** each person with their own login: accounting system
  and bank first, then card platform and billing. Check with whoever manages your Claude
  workspace whether connectors need an admin to turn them on.
- **Run the clean-inputs checklist** in `handbook/systems-and-data.md`: same file names, one
  folder per period, one schedule of record. A skill can only repeat a task whose inputs look
  the same every month.

**Blockers:** IT or security approval for connectors. Bring the read-only rule and the
connector list to that conversation.

## Rung 2: Clean, connected data

**Done looks like:** Claude reads the books and bank directly, and the monthly inputs land in
the same place and shape every time.

**Moves to rung 3:**
- **Build one Finance Brain for the team** with `setup-finance-brain`. Run it with the person
  who owns the close, then the follow-up with whoever owns the numbers.
- **Give every handbook page an owner** (write it in the page's "Last reviewed" line). The
  owner keeps that page current.
- **Put the folder where the whole team works from it:** a shared drive folder is fine for
  now. Everyone opens the same folder in Cowork.
- **Move personal skills into the shared `skills/` folder** and retire the duplicates.

**Blockers:** nobody has time for the interview. Book 60 minutes after a close, and use the
follow-up's "take the questions to them" option for the CEO.

## Rung 3: Shared context and workflows

**Done looks like:** one handbook and one set of skills that everyone uses. When a policy
changes, one page changes.

**The problem rung 3 leaves:** anyone can edit a skill or policy page, and nobody reviews the
change. A wrong threshold edited in on Tuesday quietly changes every workpaper after it. That's
what rung 4 fixes.

**Moves to rung 4:**
- **Pick a champion,** usually the controller or senior accountant, to set up the tools and the
  repository first. One person going first beats everyone installing at once.
- **Follow `github-setup.md` with the champion:** install Git, Node.js, Python, VS Code, and
  Claude Code, put the Finance Brain in a private GitHub repository, and turn on review.
- **Then onboard the team one person at a time** with the "Add a teammate" part of
  `github-setup.md`. Pair the first time.

**Blockers:** fear of the terminal. Every command in `github-setup.md` is explained and
checked, and after setup most of the daily work is saying what you want to Claude.

## Rung 4: Finance engineering

**Done looks like:** the Finance Brain lives in a private GitHub repository. Every change to a
skill or policy goes through a pull request (a proposed change someone else reviews), and the
author never approves their own. The history shows who changed what, when, and why.

**Moves to rung 5:**
- **Hold a monthly skills review** after each close, 30 minutes: what broke, which skill to fix
  (in a pull request), which task to automate next.
- **Track the wins** in `CLAUDE.md` ("Level-up progress"): time before and after, and mistakes
  caught. It's the evidence for the next investment.
- **Raise the bar on review:** a code owners file so the controller must approve changes to
  policy pages (see `github-setup.md`).

**Blockers:** pull requests pile up unreviewed. Name a reviewer for each area and review at the
monthly skills review.

## Rung 5: The frontier

**Done looks like:** the close runs mostly on skills, and the team's time goes to work it
couldn't do before.

**Ideas to try,** each built with `new-skill` and reviewed like any other change:
- flux commentary drafted for every line over the threshold, for a person to edit;
- a rolling forecast refreshed from the books each month;
- a close dashboard that shows which skills ran, which passed review, and what's still open;
- vendor and contract reviews that flag renewals and price increases before they hit.

## Rolling out to a team: the short version

1. **Start with one person and one task.** A visible win beats a training session.
2. **Write it down once.** The Finance Brain is the shared playbook.
3. **One champion sets up the tools,** then brings people on one at a time.
4. **Review every change.** The author is never the approver, for workpapers and for skills.
5. **Meet monthly after close** to fix what broke and pick the next task.
6. **Count the wins.** Time saved and mistakes caught, in `CLAUDE.md`.
