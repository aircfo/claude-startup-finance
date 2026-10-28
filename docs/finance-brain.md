---
title: Finance Brain Starter Kit
description: A free starter kit for building a finance brain that turns Claude into a finance teammate who knows how your company works. Context, skills, and review in one folder you own.
---

<div class="hero" markdown="0">
  <p class="eyebrow">Free starter kit from airCFO</p>
  <h1>Build your finance brain.</h1>
  <p class="lede">Most finance teams use AI one chat at a time: paste the chart of accounts, explain the policy again, start over next month. This kit gives Claude a <strong>handbook</strong> it reads every session, <strong>skills</strong> anyone on your team can run to get the same workpaper, and a <strong>review</strong> step so nothing Claude prepares hits the books until someone else approves it. One folder. Plain markdown. Yours to keep.</p>
  <div class="hero-ctas">
    <a class="btn btn-primary" href="downloads/finance-brain-starter-kit.zip">Download the kit (.zip)</a>
    <a class="btn btn-secondary" href="handbook-example/">See a finished handbook</a>
  </div>
</div>

<p class="credibility" markdown="0">From <em>The Startup Operator's Playbook for AI in Finance</em>, a live session on October 28, 2026. Built by <a href="https://aircfo.com">airCFO</a>, the finance and accounting team behind 300+ venture-backed startups.</p>

## What's in the folder

<div class="card-grid" markdown="0">
  <div class="card">
    <span class="step-no">1</span>
    <h3>Context</h3>
    <p><code>CLAUDE.md</code> and a <code>handbook/</code> of eight pages: company overview, chart of accounts, accounting policies, close process, cash, metrics and reporting, systems, and the workpaper standard. Written once, read automatically every session.</p>
  </div>
  <div class="card">
    <span class="step-no">2</span>
    <h3>Skills</h3>
    <p>One Claude skill per recurring task, each in its own folder. A setup skill that builds your handbook, plus worked examples for prepaid amortization, a usage accrual, and a bank reconciliation.</p>
  </div>
  <div class="card">
    <span class="step-no">3</span>
    <h3>Review</h3>
    <p>New skills save to <code>testing/</code> until they match a known-good result. Every workpaper carries a balance check and a sign-off block. The person who ran it never approves it.</p>
  </div>
</div>

## Start where you are

The kit follows the five-rung ladder for AI in finance. Find your rung and start there.

| Rung | What it looks like | Start with |
| --- | --- | --- |
| **0 · Chat** | Asking Claude questions one at a time | `new-skill` skill |
| **1 · Skills** | A monthly task Claude can repeat on demand | `new-skill` skill |
| **2 · Clean, connected data** | Claude reads your systems, and the inputs look the same every month | `handbook/systems-and-data.md` |
| **3 · Shared context & workflows** | One place your policies and processes live | `setup-finance-brain` skill |
| **4 · Finance engineering** | Version control and review before anything hits the books | `testing/` and `handbook/workpaper-standard.md` |
| **5 · The frontier** | New work finance couldn't do before | Everything above, running |

## Get started in Claude Cowork

1. **Download** the kit and unzip it somewhere permanent, for example `Documents/Finance Brain`.
2. **Add the folder** in Cowork with **Work in a folder**. Cowork reads `CLAUDE.md` automatically.
3. **Pick a path:**
   - *30 minutes:* "Use the `new-skill` skill. I want to automate [one rec or JE you know cold]." Claude rebuilds last month's version, compares it to the real one until it matches, and saves the method as a new skill.
   - *An afternoon:* "Use the `setup-finance-brain` skill." Claude drafts every handbook page from your docs and any connected systems, asks you only what they couldn't answer, then runs a short follow-up with whoever owns the numbers.
   - *This month:* run the worked examples on your own books, add your recurring tasks, and publish the handbook as an internal website (say "publish the handbook").

Using Claude Code instead? Open the folder as a project and link `skills/` as `.claude/skills` so Claude Code runs the same files you edit. The full instructions are in the kit's [README](https://github.com/aircfo/claude-startup-finance/tree/main/templates/finance-brain).

## Ground rules baked in

- **Read-only.** Skills read your systems and prepare workpapers. A person posts.
- **Placeholder, never guess.** Anything Claude doesn't know is marked `[PLACEHOLDER: ...]` and listed as an open question with an owner.
- **The author is never the approver.**
- **Fix the method, not the output.** When a reviewer catches something, the skill changes so next month is right too.

## See it finished

The [example handbook](handbook-example/) is this kit filled in for Honestly Just Spreadsheets, Inc., a fictional Series A company, and published with the kit's own publish step. The kit also includes a finished, synthetic usage-accrual workpaper in `examples/workpapers/`.

---

Nothing in the kit is accounting, tax, or legal advice. Your policies are yours to set with your team and advisors. Unofficial: not affiliated with, endorsed by, or sponsored by Anthropic, Intuit, Oracle, or any other vendor named here. MIT license. Questions or feedback: [alex@aircfo.com](mailto:alex@aircfo.com). More playbooks ship in [The AI CFO newsletter](https://www.aircfo.com/the-ai-cfo).
