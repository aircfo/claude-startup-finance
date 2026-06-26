# (Un)official Claude for Startup Finance

A Claude Cowork plugin marketplace for the startup back-office stack. One install wires up the connectors most early-stage companies already run on — **Stripe, Ramp, Mercury, and QuickBooks** — and adds finance skills that work *across* all of them — runway & burn, revenue reconciliation, and a board-ready metrics pack — built on a one-time onboarding that maps how your accounts relate across systems.

> **Unofficial.** Not affiliated with, endorsed by, or sponsored by Stripe, Ramp, Mercury, Intuit (QuickBooks), or Anthropic. All trademarks belong to their respective owners. Provided as-is under the MIT license.

## Install

In **Claude Cowork** (in the Claude desktop app, select the **Cowork** tab from the mode selector):

1. Click **Customize** in the left sidebar, then **Browse plugins**.
2. Select **Personal**, click the **+** button, and choose **Add marketplace from GitHub**.
3. Enter the repository URL: `https://github.com/aircfo/claude-startup-finance`
4. Click **Install** on the **startup-finance** plugin. It activates automatically.

Then start setup by running `/finance-context-builder` (type **/** or click **+** to see every skill the plugin adds), or just ask in plain English — "set up the finance plugin."

As workflows invoke each connector, Claude prompts you to sign in to that system in **your own** browser — on the first run, `finance-context-builder` checks all four connectors up front, so you'll authorize the ones you use then (decline any you don't). Authentication is per-user OAuth. API keys and OAuth tokens are not stored in this repository. During beta, QuickBooks requests route through an airCFO-operated MCP server — see [Data handling & security](#data-handling--security).

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
- **Build your own** — two meta-skills, **finance-skill-builder** and **finance-skill-tuner**, help you turn *your* workflows into reusable skills (and fix them when they misbehave). They generate copy-ready skills for your own workspace, so you choose where to save them and they survive plugin updates.

**How to use:** just ask in plain English ("what's our runway?") and the right skill runs automatically; each skill is also invocable by name (e.g. `/runway-and-burn`). Run **finance-context-builder** first — the other workflows read the profile it produces.

## Recommended first session

1. Install the plugin.
2. Run `/finance-context-builder`.
3. Share one finance artifact if you have it: a board deck, monthly reporting package, close checklist, KPI sheet, or a short description of the business.
4. Review the account map Claude drafts from QuickBooks.
5. Finalize the finance profile, leaving placeholders where information is still unknown.
6. Run: "What is our runway?"
7. Run: "Give me board metrics for last month."

Expected timing:
- Install/auth: 5–10 minutes
- First context build: 15–30 minutes
- First useful workflow: immediately after profile creation

After setup, you should have:
- `finance-profile.md`
- `account-map.csv`
- a list of open questions
- at least one successful finance workflow output

## First run — build your finance context

Before the workflows can reason *across* your systems, they need to know how your accounts relate — which Mercury account is your operating cash in QuickBooks, how Ramp spend and Stripe revenue land in the GL, and how your general ledger rolls up into your management financials — plus what's unique about *your* business.

Run the **finance-context-builder** skill once. It:
1. checks which connectors are live (a quick read against each) so you can see what will work now and what stays placeholder;
2. invites you to share any docs or notes about your business — your monthly reporting package, an SOP, or just a few sentences on what's unique — and reads them into the profile;
3. pulls your QuickBooks Account List and **drafts an account map** (`account-map.csv`) — one row per account with its QuickBooks **type**, **detail type**, and a short **description**, plus a management-reporting **group** (`reporting_group`) for P&L accounts (`Revenue`, `Cost of Goods Sold`, or an OpEx department) and a **cash-flow mapping** (`cf_section` / `cf_line`) for balance-sheet accounts;
4. walks you through the judgment calls and saves your corrections, then resolves how Mercury, Ramp, and Stripe accounts map onto the GL;
5. saves everything to an **airCFO Finance Context folder** (default `~/Desktop/airCFO Finance Context/`) — the profile, the account map, your shared docs, and a changelog — and records a lightweight pointer to that folder so future workflows can find it.

Every workflow reads `finance-profile.md` first, using the saved airCFO Finance Context pointer when available and falling back to the default Desktop folder — so the context loads only when you're actually doing finance work, not on every session.

It's read-only against your systems, confirms anything uncertain before saving, and you can drop new docs into the folder (or say "add this to my finance context") to refresh it anytime.

## Data handling & security

- The plugin connects to your finance systems through MCP servers using per-user OAuth.
- The plugin is designed for read-only analysis. Workflow skills must not write to QuickBooks, Stripe, Ramp, or Mercury.
- API keys and OAuth tokens are not stored in this repository.
- The plugin writes local context files only to the airCFO Finance Context folder you approve (plus, with your OK, a small pointer file/note so workflows can find that folder).
- Do not place secrets, tokens, or full account numbers in `finance-profile.md`, `account-map.csv`, or shared context docs.

Connector note for beta:
- Stripe, Ramp, and Mercury use their configured remote MCP endpoints.
- QuickBooks uses an airCFO-operated MCP server during beta.
- If you are not ready to authorize production finance data, use a sandbox or test company file while evaluating the plugin.

The beta QuickBooks connector is a multi-user, remote MCP server (verified against its source and deployment on 2026-06-25):
- **Read-only.** No write tools exist — Claude can read your books and change nothing.
- **Your financial data is never stored.** It's fetched live from QuickBooks for each question, used to answer, and not kept in the connector's database. Only your connection tokens and minimal metadata are stored, and each connection reaches only the one company tied to that login.
- **Encrypted everywhere.** All traffic is TLS/HTTPS in transit on every hop; the Intuit tokens held at rest are encrypted with AES-256-GCM.
- **Hosting & subprocessors.** Runs on Railway (US East, Virginia). The only third parties that touch your data are Railway (hosting), Intuit/QuickBooks (the source you authorize), and Anthropic (Claude, which receives the data to answer you).
- **AI training.** Your data is never used to train any AI model — not by us. It's sent to Claude (Anthropic) only to answer your question; how Anthropic handles it is governed by the terms of your own Claude account.
- **Logs & control.** Operational logs (never financial data or tokens) are kept up to 30 days. You can disconnect anytime, which deletes the stored connection and attempts to revoke the Intuit token. Security questions: alex@aircfo.com (subject "Security").

Full detail: [docs/data-handling-security.md](docs/data-handling-security.md).

## Requirements

- [Claude Cowork](https://claude.com/product/cowork), in the Claude desktop app ([download](https://claude.com/download)) — available on Pro, Max, Team, and Enterprise plans.
- Accounts on whichever of Stripe / Ramp / Mercury / QuickBooks you want to use. You can install the plugin even if you only use some of them — Claude only prompts for auth on the connectors you actually invoke.

What to expect from full vs. partial setup:
- **Best experience:** QuickBooks + Stripe + Ramp + Mercury.
- **Minimum useful setup:** QuickBooks plus at least one operating system (Stripe, Ramp, or Mercury).
- Missing connectors are not blockers, but the related profile sections and workflows stay incomplete until you connect them — Claude leaves them as explicit placeholders, never guesses.

## Updating

This plugin uses explicit versioning. To get the latest version, open **Customize → Browse plugins**, find the airCFO marketplace, and click **Update** to re-sync it from GitHub.

## Repository layout

```
claude-startup-finance/
├── .claude-plugin/marketplace.json   # the marketplace (storefront)
└── plugins/
    └── startup-finance/              # the bundled plugin
        ├── .claude-plugin/plugin.json
        ├── .mcp.json                 # connector wiring
        ├── skills/                   # finance-context-builder (+ its templates/) + the finance workflows
        └── README.md
```

## License

[MIT](./LICENSE) © airCFO
