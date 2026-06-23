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
- **Finance context builder** (`finance-context-builder`) — build your company's finance semantic map: draft your P&L and balance-sheet maps from your QuickBooks Account List (classifying each account and inferring departments for you to review), then resolve how Mercury, Ramp, and Stripe accounts map onto the GL. Run this first; every other workflow reads the map it produces.
- **Runway & burn** — net monthly burn and months of cash on hand.
- **Revenue reconciliation** — tie Stripe to QuickBooks recognized revenue and explain the gap.
- **Board metrics** — ARR/MRR, cash, burn, runway, and AR/AP aging in one board-ready summary.

**Slash command:**
- `/finance` — pick a workflow, or pass a request directly (e.g. `/finance what's our runway?`).

## First run — build your finance profile

Before the workflows can reason *across* your systems, they need to know how your accounts relate — which Mercury account is your operating cash in QuickBooks, how Ramp spend and Stripe revenue land in the GL, and how your general ledger rolls up into your management financials.

Run the **finance-context-builder** skill once. It:
1. pulls your QuickBooks Account List and **drafts two maps** — a P&L map (each account's `class` + `department`) and a balance-sheet map (each account's `bs_group` + cash-flow section + line);
2. walks you through the judgment calls (parsed departments, treasury-as-investing, anything ambiguous) and saves your corrections;
3. resolves how your Mercury, Ramp, and Stripe accounts map onto the GL;
4. writes it all to `finance-profile.md` and references it from your `CLAUDE.md`, so every session and every workflow uses the same map.

It's read-only against your systems, and it confirms anything uncertain with you before saving.

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
        ├── commands/                 # /finance entry point
        └── README.md
```

## License

[MIT](./LICENSE) © airCFO
