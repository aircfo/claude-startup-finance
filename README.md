# (Un)official Claude for Startup Finance

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Docs](https://img.shields.io/badge/docs-aircfo.github.io-132c3a.svg)](https://aircfo.github.io/claude-startup-finance/)
[![Built for Claude Cowork](https://img.shields.io/badge/built%20for-Claude%20Cowork-ff971e.svg)](https://claude.com/product/cowork)
[![The AI CFO Newsletter](https://img.shields.io/badge/newsletter-The%20AI%20CFO-132c3a.svg)](https://www.aircfo.com/the-ai-cfo)

## Start here: the Finance Brain Starter Kit

A free folder that turns Claude into a finance teammate who knows how your company works.

- **Context.** A handbook of your policies, chart of accounts, close process, cash rules, and
  metric definitions that Claude reads before any finance work.
- **Commands.** One file per recurring task. Anyone on the team runs it and gets the same
  workpaper.
- **Review.** Claude prepares, a person approves. Nothing hits the books until someone other
  than the preparer signs off.

Plain markdown, no plugin to install, works in Claude Cowork or Claude Code. From our
October 28, 2026 session, *The Startup Operator's Playbook for AI in Finance*.

**[Download the kit (.zip)](https://aircfo.github.io/claude-startup-finance/downloads/finance-brain-starter-kit.zip)** ·
[Browse the folder](./templates/finance-brain/) ·
[See a finished handbook](https://aircfo.github.io/claude-startup-finance/handbook-example/) ·
[Kit guide](https://aircfo.github.io/claude-startup-finance/finance-brain.html)

---

The home of the Claude tools that ship with **[The AI CFO](https://www.aircfo.com/the-ai-cfo)**
newsletter: a library for building an AI-powered startup finance function, built around one
idea. Before AI touches your numbers, it should read **your Finance Brain**: what your
metrics mean, how your accounts roll up, and the judgment calls your team carries in its
head.

**→ [Browse the tool library](https://aircfo.github.io/claude-startup-finance/#tools)**:
every tool, grouped by the job it does, each with its own page saying exactly what to
install.

| Theme | Tools |
| --- | --- |
| **Start here** | [Finance Brain Starter Kit](https://aircfo.github.io/claude-startup-finance/finance-brain.html): a free download, no install |
| **Connected stack** | [All Systems Go](https://aircfo.github.io/claude-startup-finance/tools/all-systems-go/): the Stripe, Ramp, and Mercury connectors every other tool shares |
| **Cash & runway** | [Runway & burn](https://aircfo.github.io/claude-startup-finance/tools/runway-and-burn/) |
| **Revenue & close** | [Revenue reconciliation](https://aircfo.github.io/claude-startup-finance/tools/revenue-reconciliation/) |
| **Reporting** | [Board metrics](https://aircfo.github.io/claude-startup-finance/tools/board-metrics/) |
| **Build your own** | [Finance skill builder](https://aircfo.github.io/claude-startup-finance/tools/finance-skill-builder/) · [Finance skill tuner](https://aircfo.github.io/claude-startup-finance/tools/finance-skill-tuner/) |

The tools ship in one plugin, **`all-systems-go`**, named for airCFO's *All Systems Go*
series on the startup back-office stack. It holds the Stripe, Ramp, and Mercury connectors
every tool shares, plus the cross-system workflows above and the meta-skills to author your
own, all reading your Finance Brain first.

> **Unofficial.** Not affiliated with, endorsed by, or sponsored by Stripe, Ramp, Mercury,
> Intuit (QuickBooks), or Anthropic. All trademarks belong to their respective owners.
> Provided as-is under the MIT license. Nothing here is accounting, tax, or legal advice.

## Contents

- [Start here: the Finance Brain Starter Kit](#start-here-the-finance-brain-starter-kit)
- [What's in this repo](#whats-in-this-repo)
- [Get started](#get-started)
- [Data handling & security](#data-handling--security)
- [Requirements](#requirements)
- [Updating](#updating)
- [Repository layout](#repository-layout)
- [Contributing](#contributing)
- [License](#license)

## What's in this repo

| Type | Name | Theme | What it does | Install method | Docs |
| --- | --- | --- | --- | --- | --- |
| Template | **`finance-brain`** | Start here | The Finance Brain Starter Kit: a handbook Claude reads every session, a setup interview that drafts it from your docs and books, commands for recurring JEs and recs, a workpaper standard, and a review step. | [Download (.zip)](https://aircfo.github.io/claude-startup-finance/downloads/finance-brain-starter-kit.zip) or copy [`templates/finance-brain/`](./templates/finance-brain/) | [Kit guide](https://aircfo.github.io/claude-startup-finance/finance-brain.html) · [Example handbook](https://aircfo.github.io/claude-startup-finance/handbook-example/) |
| Plugin | **`all-systems-go`** | Connected stack, plus the workflows that use it | Provides the shared Stripe, Ramp, and Mercury connectors, plus cross-system workflows: runway & burn, revenue reconciliation, board metrics, and the skill builder and tuner. | Cowork marketplace ([below](#get-started)) | [Tool page](https://aircfo.github.io/claude-startup-finance/tools/all-systems-go/) · [Plugin README](./plugins/all-systems-go/README.md) |

Anything airCFO publishes publicly for Claude (templates, plugins, standalone skills) is
indexed in this table, even when the code lives in its own repository. This table is the
index for the repo; the [tool library](https://aircfo.github.io/claude-startup-finance/#tools)
is the index for readers, with one page per tool.

### Not using Claude Cowork?

The kit works in Claude Code as-is: open the folder as a project and copy `commands/` into
`.claude/commands/` for slash commands. The skills in `all-systems-go` are plain
[Agent Skills](https://code.claude.com/docs/en/skills), so they also install into Claude Code
and other skill-aware agents via the [`skills` CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add aircfo/claude-startup-finance --list          # see what's available
npx skills add aircfo/claude-startup-finance --skill runway-and-burn
```

Skills installed this way arrive **without** the plugin's bundled connectors, so you supply
your own connector configuration for Stripe, Ramp, Mercury, or QuickBooks.

## Get started

**1. Build your Finance Brain.** Download the kit, unzip it somewhere permanent, and add the
folder in Claude Cowork with **Work in a folder**. Then say:

> "Run `commands/setup/build-handbook.md`."

Claude drafts every handbook page from the documents you share and any systems you've
connected, then asks you only what they can't answer. Gaps stay marked as placeholders, never
guessed. The [kit guide](https://aircfo.github.io/claude-startup-finance/finance-brain.html)
has a 30-minute, an afternoon, and a this-month path.

**2. Add the tools (optional).** In Claude Cowork:

1. Click **Customize** in the left sidebar, then **Browse plugins**.
2. Select **Personal**, click the **+** button, and choose **Add marketplace from GitHub**.
3. Enter the repository URL: `https://github.com/aircfo/claude-startup-finance`
4. Click **Install** on **all-systems-go**, and authorize the systems you use.
5. For QuickBooks, add a QuickBooks connector in Claude's connector settings (for example,
   Intuit's), read-only with your own login.

Then, working in your Finance Brain folder: "what's our runway?" · "give me board metrics for
last month."

## Data handling & security

- **Read-only by design.** Commands and tools read your systems and prepare workpapers and
  analysis. They never post, pay, transfer, or edit records. A person posts.
- **Your Finance Brain is a folder on your machine.** Nothing in the kit sends it anywhere.
- **Every connector is the vendor's own**, authorized with your own login in your browser.
  airCFO runs no server in between, and no API keys or tokens are stored in this repository.
- Not ready to authorize production data? Use a sandbox or test company while evaluating.

Full detail: [docs/data-handling-security.md](docs/data-handling-security.md). To report a
vulnerability, see [SECURITY.md](./SECURITY.md). Please email rather than opening a public
issue.

## Requirements

- **The kit:** Claude Cowork or Claude Code. No connectors required to start; commands ask
  for exports when a system isn't connected.
- **The tools:** [Claude Cowork](https://claude.com/product/cowork), in the Claude desktop
  app ([download](https://claude.com/download)), on Pro, Max, Team, and Enterprise plans,
  plus Stripe, Ramp, Mercury, or QuickBooks accounts for the systems you use. Missing systems
  aren't blockers: they become open questions, never guesses.

## Updating

- **The kit** is yours once downloaded. To pick up a newer version, compare it to the
  [folder on GitHub](./templates/finance-brain/) and copy over what you want; your handbook
  pages are never overwritten.
- **The plugin** uses explicit versioning. Open **Customize → Browse plugins**, find the
  airCFO marketplace, and click **Update** to re-sync from GitHub.

Released versions are tagged and listed in [CHANGELOG.md](./CHANGELOG.md).

## Repository layout

```
claude-startup-finance/
├── .claude-plugin/marketplace.json   # the marketplace (storefront)
├── plugins/
│   └── all-systems-go/               # Stripe/Ramp/Mercury connectors + workflows
│       ├── .claude-plugin/plugin.json
│       ├── .mcp.json                 # Stripe, Ramp, Mercury
│       ├── skills/                   # runway-and-burn, revenue-reconciliation,
│       │                             # board-metrics, finance-skill-builder/tuner
│       └── README.md
├── templates/
│   ├── finance-brain/                # the Finance Brain Starter Kit (copy or download)
│   └── skill-plugin/                 # copy-ready scaffold for a new skill plugin
└── docs/                             # the published docs site (GitHub Pages)
    ├── finance-brain.md              # the kit's guide page
    ├── handbook-example/             # the kit filled in for a fictional company
    ├── downloads/                    # the kit as a .zip (rebuilt by _build_zip.py)
    ├── _tools/                       # one page per tool in the library
    └── _data/                        # library themes + where each connector comes from
```

## Contributing

Ideas, bug reports, and skill requests are welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md).
If you're adding a skill or plugin, the house rules (naming, required files, versioning, and
when a skill gets its own plugin) are in
[docs/authoring-conventions.md](./docs/authoring-conventions.md). If you change the kit, run
`python3 docs/downloads/_build_zip.py` so the download matches the folder.

## Follow along

New skills and workflows ship alongside **[The AI CFO Newsletter](https://www.aircfo.com/the-ai-cfo)**:
practical, tested playbooks for startup finance in the age of AI, written by airCFO's CEO
every two weeks. Skills that accompany an issue land in this repo, versioned so a piece you
read still matches what you install.

**→ [Subscribe to The AI CFO](https://www.aircfo.com/the-ai-cfo)** ·
**[Read the docs](https://aircfo.github.io/claude-startup-finance/)** ·
**[airCFO](https://aircfo.com)** · Questions or feedback: [alex@aircfo.com](mailto:alex@aircfo.com)

## License

[MIT](./LICENSE) © airCFO
