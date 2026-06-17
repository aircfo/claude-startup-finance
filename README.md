# (Un)official Claude for Startup Finance

A Claude Code plugin marketplace for the startup back-office stack. One install wires up the connectors most early-stage companies already run on — **Stripe, Ramp, Mercury, and QuickBooks** — and adds finance skills that work *across* all of them: runway & burn, revenue reconciliation, and a board-ready metrics pack.

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
- **Runway & burn** — net monthly burn and months of cash on hand.
- **Revenue reconciliation** — tie Stripe to QuickBooks recognized revenue and explain the gap.
- **Board metrics** — ARR/MRR, cash, burn, runway, and AR/AP aging in one board-ready summary.

**Slash command:**
- `/finance` — pick a workflow, or pass a request directly (e.g. `/finance what's our runway?`).

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
        ├── skills/                   # the finance workflows
        ├── commands/                 # /finance entry point
        └── README.md
```

## License

[MIT](./LICENSE) © airCFO
