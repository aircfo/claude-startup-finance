# (Un)official Claude for Startup Finance

A Claude Cowork plugin marketplace for the startup back office, built around one idea:
before AI touches your numbers, it should load **your ContextOS** — your company's finance
context: what your metrics mean, how your accounts map into reporting, and the judgment
calls your team carries in its head.

Two plugins, in order:

1. **`finance-contextos`** — *start here.* Build your ContextOS from QuickBooks: a guided
   session drafts your account map, captures your definitions into a durable finance
   profile, and **proves the result ties to your live books**. One connector, one review,
   files you own.
2. **`all-systems-go`** — the enrichment pack, named for airCFO's *All Systems Go* series
   on the startup back-office stack. Adds Stripe, Ramp, and Mercury connectors plus
   cross-system workflows (runway & burn, revenue reconciliation, board metrics) and
   meta-skills to author your own — all reading your ContextOS first.

(A third plugin, **`ai-cfo-lab`**, ships skills from the AI CFO newsletter.)

> **Unofficial.** Not affiliated with, endorsed by, or sponsored by Stripe, Ramp, Mercury,
> Intuit (QuickBooks), or Anthropic. All trademarks belong to their respective owners.
> Provided as-is under the MIT license.

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

Full detail: [docs/data-handling-security.md](docs/data-handling-security.md).

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

## Repository layout

```
claude-startup-finance/
├── .claude-plugin/marketplace.json   # the marketplace (storefront)
└── plugins/
    ├── finance-contextos/            # the flagship: build your ContextOS
    │   ├── .claude-plugin/plugin.json
    │   ├── .mcp.json                 # QuickBooks connector only
    │   ├── skills/finance-context-builder/   # + its templates/
    │   └── README.md
    ├── all-systems-go/               # enrichment: Stripe/Ramp/Mercury + workflows
    │   ├── .claude-plugin/plugin.json
    │   ├── .mcp.json                 # Stripe, Ramp, Mercury
    │   ├── skills/                   # runway-and-burn, revenue-reconciliation,
    │   │                             # board-metrics, finance-skill-builder/tuner
    │   └── README.md
    └── ai-cfo-lab/                   # AI CFO newsletter skills
```

## License

[MIT](./LICENSE) © airCFO
