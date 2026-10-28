# (Un)official Claude for Startup Finance

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Docs](https://img.shields.io/badge/docs-aircfo.github.io-132c3a.svg)](https://aircfo.github.io/claude-startup-finance/)
[![Built for Claude Cowork](https://img.shields.io/badge/built%20for-Claude%20Cowork-ff971e.svg)](https://claude.com/product/cowork)
[![The AI CFO Newsletter](https://img.shields.io/badge/newsletter-The%20AI%20CFO-132c3a.svg)](https://www.aircfo.com/the-ai-cfo)

**Point Claude at your startup's finance stack — and have it actually understand your
numbers.**

- **A ContextOS you own.** Your definitions of burn, runway, and MRR, plus every account's
  classification, captured once into plain files on your machine.
- **Read-only everywhere.** Every connector reads with your own login. Nothing in this repo
  can write to, move, or send your money.
- **It isn't done until it ties.** The build ends by verifying itself against your live
  books — cash to the bank, revenue to the penny.

<!-- HUMAN follow-up: record a ~20s ContextOS build demo, save as assets/demo-contextos.gif,
     and embed it here with descriptive alt text. Intentionally left as a comment rather
     than a broken image reference. -->

The home of the Claude tools that ship with **[The AI CFO](https://www.aircfo.com/the-ai-cfo)**
newsletter: a library for building an AI-powered startup finance function, built around one
idea. Before AI touches your numbers, it should load **your ContextOS**, your company's
finance context: what your metrics mean, how your accounts map into reporting, and the
judgment calls your team carries in its head.

**→ [Browse the tool library](https://aircfo.github.io/claude-startup-finance/#tools)**:
every tool, grouped by the job it does, each with its own page saying exactly what to
install.

| Theme | Tools |
| --- | --- |
| **Foundation** | [Build your ContextOS](https://aircfo.github.io/claude-startup-finance/tools/contextos/), *start here* |
| **Connected stack** | [All Systems Go](https://aircfo.github.io/claude-startup-finance/tools/all-systems-go/): the Stripe, Ramp, and Mercury connectors every other tool shares |
| **Cash & runway** | [Runway & burn](https://aircfo.github.io/claude-startup-finance/tools/runway-and-burn/) |
| **Revenue & close** | [Revenue reconciliation](https://aircfo.github.io/claude-startup-finance/tools/revenue-reconciliation/) |
| **Reporting** | [Board metrics](https://aircfo.github.io/claude-startup-finance/tools/board-metrics/) |
| **Build your own** | [Finance skill builder](https://aircfo.github.io/claude-startup-finance/tools/finance-skill-builder/) · [Finance skill tuner](https://aircfo.github.io/claude-startup-finance/tools/finance-skill-tuner/) |

Two plugins deliver all of it, installed in order:

1. **`finance-contextos`**, *start here.* Build your ContextOS from QuickBooks: a guided
   session drafts your account map, captures your definitions into a durable finance
   profile, and **proves the result ties to your live books**. One connector, one review,
   files you own.
2. **`all-systems-go`**, the connected stack, named for airCFO's *All Systems Go* series on
   the startup back-office stack. It holds the Stripe, Ramp, and Mercury connectors that
   every tool shares, plus the cross-system workflows above and the meta-skills to author
   your own, all reading your ContextOS first.

> **Unofficial.** Not affiliated with, endorsed by, or sponsored by Stripe, Ramp, Mercury,
> Intuit (QuickBooks), or Anthropic. All trademarks belong to their respective owners.
> Provided as-is under the MIT license.

## Contents

- [What's in this repo](#whats-in-this-repo)
- [Install](#install)
- [What a ContextOS is](#what-a-contextos-is)
- [Recommended first session](#recommended-first-session)
- [Data handling & security](#data-handling--security)
- [Requirements](#requirements)
- [Updating](#updating)
- [Repository layout](#repository-layout)
- [Contributing](#contributing)
- [License](#license)

## What's in this repo

| Type | Name | Theme | What it does | Install method | Docs |
| --- | --- | --- | --- | --- | --- |
| Plugin | **`finance-contextos`** | Foundation | Builds your ContextOS from QuickBooks — account map, finance profile, tie-out. Start here. | Cowork marketplace ([below](#install)) | [Tool page](https://aircfo.github.io/claude-startup-finance/tools/contextos/) · [Plugin README](./plugins/finance-contextos/README.md) |
| Plugin | **`all-systems-go`** | Connected stack, plus the workflows that use it | Provides the shared Stripe, Ramp, and Mercury connectors, plus cross-system workflows: runway & burn, revenue reconciliation, board metrics, and the skill builder and tuner. | Cowork marketplace ([below](#install)) | [Tool page](https://aircfo.github.io/claude-startup-finance/tools/all-systems-go/) · [Plugin README](./plugins/all-systems-go/README.md) |
| MCP server | **`qbo-mcp`** | Foundation | The read-only QuickBooks MCP server behind `finance-contextos`. Runs on airCFO infrastructure by default; self-host it if you'd rather your books never touch ours. | Separate repo — [`aircfo/qbo-mcp`](https://github.com/aircfo/qbo-mcp) | [Self-hosting guide](https://aircfo.github.io/claude-startup-finance/self-hosting.html) |

Anything airCFO publishes publicly for Claude — plugins, MCP servers, standalone skills —
is indexed in this table, even when the code lives in its own repository. This table is the
index for the repo; the [tool library](https://aircfo.github.io/claude-startup-finance/#tools)
is the index for readers, with one page per tool.

### Not using Claude Cowork?

The skills in this repo are plain [Agent Skills](https://code.claude.com/docs/en/skills),
so they also install into Claude Code and other skill-aware agents via the
[`skills` CLI](https://github.com/vercel-labs/skills) — no marketplace required:

```bash
npx skills add aircfo/claude-startup-finance --list          # see what's available
npx skills add aircfo/claude-startup-finance --skill runway-and-burn
```

Note that skills installed this way arrive **without** the plugin's bundled connectors —
you supply your own MCP configuration for QuickBooks, Stripe, Ramp, or Mercury. The Cowork
install path is the supported one for a working end-to-end setup.

## Install

In **Claude Cowork** (in the Claude desktop app, select the **Cowork** tab from the mode
selector):

1. Click **Customize** in the left sidebar, then **Browse plugins**.
2. Select **Personal**, click the **+** button, and choose **Add marketplace from GitHub**.
3. Enter the repository URL: `https://github.com/aircfo/claude-startup-finance`
4. Click **Install** on the **finance-contextos** plugin. It activates automatically.
   (Install **all-systems-go** too if you want the extra connectors and workflows now —
   you can always add it later.)

Then say **"build my ContextOS"** (or run `/finance-context-builder`). You'll get one
QuickBooks sign-in pop-up — your own login, read-only — and a guided ~20-minute build with
two quick review points.

> **Upgrading from the old `startup-finance` plugin?** It was split into the two plugins
> above (QuickBooks moved to `finance-contextos`; everything else is in `all-systems-go`).
> Uninstall `startup-finance`, update the marketplace, and install the new plugin(s). Your
> existing context folder keeps working — nothing about your files changed.

## What a ContextOS is

Finance analysis breaks when the model doesn't know your company's definitions: which
accounts count as cash for runway, whether your board-deck MRR matches the Stripe
dashboard, which vendors are COGS, which one-time costs to exclude from run-rate burn.
Those answers rarely live cleanly in one system — they live in board decks, close
checklists, and CFO judgment.

The ContextOS captures them once, in a folder you own:

- **`finance-profile.md`** — the operating manual: KPI definitions, cash and burn rules,
  source-of-truth mappings, known exceptions, open questions.
- **`account-map.csv`** — every QuickBooks account classified on independent axes
  (expense category, department, cash-flow line, tags like `mrr`), with governance —
  rows are `auto`, `needs-review`, or `confirmed`, and refreshes never overwrite what
  you've confirmed. Editable in any spreadsheet.
- **`context/`** — the docs you've shared, kept as a record of what's been ingested.
- **`CHANGELOG.md`** — a dated log of what changed each run.

**And it isn't done until it ties.** The build ends with a verification pass against your
live systems — cash to the bank, revenue coverage to the penny. Differences become open
questions, never silent assumptions.

Every workflow reads the profile first (via a saved pointer, falling back to the default
Desktop folder), so the context loads when you do finance work — not on every session.

## Recommended first session

1. Install **finance-contextos**.
2. Say "build my ContextOS".
3. Share one finance artifact if you have it: a board deck, monthly reporting package,
   close checklist, or a short description of the business.
4. Review the judgment calls in the account map Claude drafts (you review the
   `needs-review` queue, not hundreds of rows).
5. Finalize the profile — placeholders are fine; they're listed as open questions.
6. Check the tie-out results Claude shows you.

Then, with **all-systems-go** installed: "what's our runway?" · "give me board metrics for
last month."

Expected timing: install/auth 5–10 minutes · context build 15–30 minutes · first workflow
immediately after.

## Data handling & security

- Read-only by design across every connector. No write tools; Claude can read your books
  and change nothing.
- Per-user OAuth everywhere — you authenticate into your own accounts in your browser.
  API keys and tokens are not stored in this repository.
- Local files are written only to the ContextOS folder you approve (plus, with your OK, a
  small pointer file so workflows can find it).
- The QuickBooks connector is an airCFO-operated MCP server
  ([source, MIT](https://github.com/aircfo/qbo-mcp)): your financial data is fetched live
  per question and **never stored server-side**; only encrypted connection tokens
  (AES-256-GCM), your company name, and your sign-up email are kept. Disconnect anytime
  ("disconnect QuickBooks") to revoke and erase. Prefer not to route through airCFO's
  instance? **Self-host it** — the deploy guide ships with the source.
- Not ready to authorize production data? Use a QuickBooks sandbox company while evaluating.

Full detail: [docs/data-handling-security.md](docs/data-handling-security.md). To report a
vulnerability, see [SECURITY.md](./SECURITY.md) — please email rather than opening a public
issue.

## Requirements

- [Claude Cowork](https://claude.com/product/cowork), in the Claude desktop app
  ([download](https://claude.com/download)) — available on Pro, Max, Team, and Enterprise
  plans.
- A QuickBooks Online account (for `finance-contextos`); Stripe / Ramp / Mercury accounts
  only if you install `all-systems-go` and use them. Missing systems aren't blockers —
  their profile sections stay as explicit placeholders, never guesses.

## Updating

Explicit versioning. Open **Customize → Browse plugins**, find the airCFO marketplace,
and click **Update** to re-sync from GitHub.

Released versions are tagged and listed in [CHANGELOG.md](./CHANGELOG.md).

## Repository layout

```
claude-startup-finance/
├── .claude-plugin/marketplace.json   # the marketplace (storefront)
├── plugins/
│   ├── finance-contextos/            # the flagship: build your ContextOS
│   │   ├── .claude-plugin/plugin.json
│   │   ├── .mcp.json                 # QuickBooks connector only
│   │   ├── skills/finance-context-builder/   # + its templates/
│   │   └── README.md
│   ├── all-systems-go/               # enrichment: Stripe/Ramp/Mercury + workflows
│   │   ├── .claude-plugin/plugin.json
│   │   ├── .mcp.json                 # Stripe, Ramp, Mercury
│   │   ├── skills/                   # runway-and-burn, revenue-reconciliation,
│   │   │                             # board-metrics, finance-skill-builder/tuner
│   │   └── README.md
├── templates/skill-plugin/           # copy-ready scaffold for a new skill plugin
└── docs/                             # the published docs site (GitHub Pages)
    ├── _tools/                       # one page per tool in the library
    └── _data/                        # library themes + which plugin provides each connector
```

## Contributing

Ideas, bug reports, and skill requests are welcome — see
[CONTRIBUTING.md](./CONTRIBUTING.md). If you're adding a skill or plugin, the house rules
(naming, required files, versioning, and when a skill gets its own plugin) are in
[docs/authoring-conventions.md](./docs/authoring-conventions.md).

## Follow along

New skills and workflows ship alongside **[The AI CFO Newsletter](https://www.aircfo.com/the-ai-cfo)**
— practical, tested playbooks for startup finance in the age of AI, written by airCFO's CEO
every two weeks. Skills that accompany an issue land in this repo, versioned so a piece you
read still matches what you install.

**→ [Subscribe to The AI CFO](https://www.aircfo.com/the-ai-cfo)** ·
**[Read the docs](https://aircfo.github.io/claude-startup-finance/)** ·
**[airCFO](https://aircfo.com)** · Questions or feedback: [alex@aircfo.com](mailto:alex@aircfo.com)

## License

[MIT](./LICENSE) © airCFO
