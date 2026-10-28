# Finance Brain Starter Kit

A folder that turns Claude into a finance teammate who knows how *your* company works.

Most finance teams use AI the same way: open a chat, paste the chart of accounts, explain the
policy again, get a decent answer, close the tab. Next month, start over. Everyone on the team
explains the same things in their own way, and none of it compounds.

This kit fixes that with three pieces:

| Piece | Where it lives | What it does |
| --- | --- | --- |
| **Context** | `CLAUDE.md` + `handbook/` | How your company works, written once. Claude reads it before any finance work. |
| **Commands** | `commands/` | One file per recurring task (a JE, a rec, a tie-out). Anyone on the team runs it and gets the same workpaper. |
| **Review** | `testing/` + the workpaper standard | Claude prepares, a person approves. Nothing Claude builds hits the books until someone else signs off. |

It's plain markdown in a folder you own. No plugin to install, no connector required to start.

> **Unofficial.** Built by [airCFO](https://aircfo.com). Not affiliated with, endorsed by, or
> sponsored by Anthropic, Intuit (QuickBooks), Oracle (NetSuite), or any other vendor named
> here. Provided as-is under the MIT license. Nothing here is accounting, tax, or legal
> advice; your policies are yours to set.

---

## Where this fits on the ladder

The kit is built around the five-rung ladder for AI in finance. Find your rung, then use the
part of the kit that gets you to the next one.

| Rung | What it looks like | Start with |
| --- | --- | --- |
| **0 · Chat** | Asking Claude questions one at a time. | `commands/setup/new-command.md` |
| **1 · Skills** | A monthly task Claude can repeat on demand. | `commands/setup/new-command.md`, then `commands/_templates/` |
| **2 · Clean, connected data** | Claude reads your systems, and the inputs look the same every month. | `handbook/systems-and-data.md` |
| **3 · Shared context & workflows** | One place your policies and processes live, so the whole team works from the same playbook. | `CLAUDE.md`, `handbook/`, `commands/setup/build-handbook.md` |
| **4 · Finance engineering** | Version control, review before anything hits the books. | `testing/`, the workpaper standard in `commands/_templates/` |
| **5 · The frontier** | New work finance couldn't do before. | Everything above, running. |

---

## Get started

### 1. Put the folder where Claude can see it

**Claude Cowork (recommended):** download this folder, move it somewhere permanent (for
example `~/Documents/Finance Brain/`), and add it to Cowork with **Work in a folder**. Cowork
reads `CLAUDE.md` automatically every time you work there.

**Claude Code:** open the folder as your project. To get `/slash-commands`, copy the files in
`commands/` into `.claude/commands/` (keep the subfolders; skip `_templates/`).

### 2. Pick a path

**30 minutes: your first command.** Say:

> "Run `commands/setup/new-command.md`. I want to automate [one rec, JE, or report you know cold]."

Claude has you hand it last month's finished version, rebuilds it, compares the two, and
saves the method as a new command. You end the session with something you'll run again next
month.

**An afternoon: your handbook.** Say:

> "Run `commands/setup/build-handbook.md`."

Claude reads whatever you share (a close checklist, a policy doc, last month's reporting
package) and any finance systems you've connected, drafts every page in `handbook/`, then
interviews you only on the things no document or system could tell it. Gaps stay marked as
`[PLACEHOLDER: ...]`, never guessed. Then run `commands/setup/follow-up-interview.md` with
whoever owns the numbers to define your metrics, burn, and runway.

**This month: make it the team's.** Run the worked examples in `commands/jes/` and
`commands/recs/` on your own books, add your recurring tasks, and publish the handbook as a
website your whole team can browse (`commands/publish/build-handbook-site.md`).

### 3. Keep it current

When a policy changes, update the page. When a command gets something wrong, fix the command,
not the output. The folder gets smarter every month, and so does every session that reads it.

---

## What's in the folder

```
finance-brain/
├── CLAUDE.md                 Read by Claude every session: rules + a map of everything below
├── handbook/                 How your company works (fill in once, keep current)
│   ├── company-overview.md   Entities, business model, systems, who approves what
│   ├── chart-of-accounts.md  Account structure, naming, and reporting rollups
│   ├── accounting-policies.md  Capitalization, prepaids, accruals, revenue, and more
│   ├── close-process.md      Close calendar, checklist, flux thresholds, sign-off
│   ├── cash.md               Bank and card accounts, what counts as cash, transfers
│   ├── metrics-and-reporting.md  Metric definitions, burn and runway, plan, audiences
│   └── systems-and-data.md   What Claude can read, and the clean-inputs checklist
├── commands/                 One file per recurring task
│   ├── README.md             How commands work and how to add one
│   ├── setup/                build-handbook.md, follow-up-interview.md, new-command.md
│   ├── _templates/           journal-entry.md, reconciliation.md (the workpaper standard)
│   ├── jes/                  prepaid-amortization.md, usage-accrual.md
│   ├── recs/                 bank-reconciliation.md
│   └── publish/              build-handbook-site.md
├── testing/                  Where drafts live until a command is trusted
├── site-template/            The look of your handbook website
└── examples/                 A sample Claude-prepared JE workpaper (synthetic data)
```

## Ground rules baked into the kit

- **Read-only.** Commands read your systems and produce workpapers and import files. A person
  posts entries. Nothing in this kit writes to your accounting system, bank, or card platform.
- **Placeholder, never guess.** Anything Claude doesn't know is marked
  `[PLACEHOLDER: what's needed and why]` and listed as an open question.
- **The author is never the approver.** Claude prepares. Someone other than the person who ran
  the command reviews it before it's posted.
- **Fix the method, not the output.** If a workpaper is wrong, change the command so next month
  is right too.

## Want to see a finished one?

The [example handbook](https://aircfo.github.io/claude-startup-finance/handbook-example/) shows
this kit filled in for a fictional Series A company, Honestly Just Spreadsheets, Inc., published
with `commands/publish/build-handbook-site.md`.

---

Built by [airCFO](https://aircfo.com), the finance and accounting team behind 300+
venture-backed startups. More playbooks like this ship in
[The AI CFO newsletter](https://www.aircfo.com/the-ai-cfo). Questions or feedback:
[alex@aircfo.com](mailto:alex@aircfo.com).
