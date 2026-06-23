# (Un)official Claude for Startup Finance

A Claude Code plugin marketplace for the startup back-office stack. One install wires up the connectors most early-stage companies already run on — **Stripe, Ramp, Mercury, and QuickBooks** — and adds finance skills that work *across* all of them — runway & burn, revenue reconciliation, and a board-ready metrics pack — built on a one-time onboarding that maps how your accounts relate across systems.

> **Unofficial.** Not affiliated with, endorsed by, or sponsored by Stripe, Ramp, Mercury, Intuit (QuickBooks), or Anthropic. All trademarks belong to their respective owners. Provided as-is under the MIT license.

## Install

In Claude Code:

```
/plugin marketplace add aircfo/claude-startup-finance
/plugin install startup-finance@claude-startup-finance
```

On first use, Claude will walk you through logging into **your own** Stripe, Ramp, Mercury, and QuickBooks accounts in your browser. Authentication is per-user and handled by each provider's OAuth — no API keys live in this repo, and nothing is shared with airCFO.

## What you get

**Connectors** (remote MCP servers, per-user OAuth):
- Stripe
- Ramp
- Mercury
- QuickBooks

**Skills** (finance workflows across the connectors):
- **Finance context builder** (`finance-context-builder`) — build your company's finance semantic map: draft an account map from your QuickBooks Account List (classifying each account and inferring departments for you to review), then resolve how Mercury, Ramp, and Stripe accounts map onto the GL. Run this first; every other workflow reads the map it produces.
- **Runway & burn** — net monthly burn and months of cash on hand.
- **Revenue reconciliation** — tie Stripe to QuickBooks recognized revenue and explain the gap.
- **Board metrics** — ARR/MRR, cash, burn, runway, and AR/AP aging in one board-ready summary.
- **Build your own** — two meta-skills, **finance-skill-builder** and **finance-skill-tuner**, help you turn *your* workflows into reusable skills (and fix them when they misbehave). They write skills into your own workspace, never the plugin, so they survive updates.

**How to use:** just ask in plain English ("what's our runway?") and the right skill runs automatically; each skill is also invocable by name (e.g. `/runway-and-burn`). Run **finance-context-builder** first — the other workflows read the profile it produces.

## First run — build your finance context

Before the workflows can reason *across* your systems, they need to know how your accounts relate — which Mercury account is your operating cash in QuickBooks, how Ramp spend and Stripe revenue land in the GL, and how your general ledger rolls up into your management financials — plus what's unique about *your* business.

Run the **finance-context-builder** skill once. It:
1. invites you to share any docs or notes about your business — your monthly reporting package, an SOP, or just a few sentences on what's unique — and reads them into the profile;
2. pulls your QuickBooks Account List and **drafts an account map** (`account-map.csv`) — every account classified: income-statement accounts get a `class` + `department`, balance-sheet accounts get a `bs_group` + cash-flow section/line;
3. walks you through the judgment calls and saves your corrections, then resolves how Mercury, Ramp, and Stripe accounts map onto the GL;
4. saves everything to an **airCFO Finance Context folder** (default `~/Desktop/airCFO Finance Context/`) — the profile, the account map, your shared docs, and a changelog — and wires the profile into `CLAUDE.md` so every session and every workflow uses it.

It's read-only against your systems, confirms anything uncertain before saving, and you can drop new docs into the folder (or say "add this to my finance context") to refresh it anytime.

## Requirements

- A recent version of [Claude Code](https://claude.com/claude-code).
- Accounts on whichever of Stripe / Ramp / Mercury / QuickBooks you want to use. You can install the plugin even if you only use some of them — Claude only prompts for auth on the connectors you actually invoke.

## Updating

This plugin uses explicit versioning. To get the latest version:

```
/plugin marketplace update claude-startup-finance
```

## Repository layout

```
claude-startup-finance/
├── .claude-plugin/marketplace.json   # the marketplace (storefront)
└── plugins/
    └── startup-finance/              # the bundled plugin
        ├── .claude-plugin/plugin.json
        ├── .mcp.json                 # connector wiring
        ├── skills/                   # finance-context-builder + the finance workflows
        ├── templates/                # fillable mapping tables (your reporting framework)
        └── README.md
```

## License

[MIT](./LICENSE) © airCFO
