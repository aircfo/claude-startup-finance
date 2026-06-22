# startup-finance (plugin)

The bundled plugin behind the **(Un)official Claude for Startup Finance** marketplace. It wires up the four connectors a typical startup back office runs on and adds finance skills that work *across* them.

## Connectors

| Connector | Transport | Auth |
| --- | --- | --- |
| Stripe | Remote (HTTP) | Per-user OAuth in your browser |
| Ramp | Remote (HTTP) | Per-user OAuth in your browser |
| Mercury | Remote (HTTP) | Per-user OAuth in your browser |
| QuickBooks | Remote (HTTP) | Per-user OAuth in your browser |

You authenticate into **your own** accounts on first use. No API keys or secrets are stored in this repo, and nothing is shared with airCFO.

## Skills

- **onboarding** — build the company's finance semantic map (`finance-profile.md`): draft the P&L and balance-sheet maps from your QuickBooks Account List (you review), then resolve how Mercury, Ramp, and Stripe accounts map onto the GL. **Run this first.**
- **runway-and-burn** — net monthly burn and months of cash (Mercury + Ramp, offset by revenue).
- **revenue-reconciliation** — tie Stripe revenue to QuickBooks recognized revenue and explain the gap.
- **board-metrics** — a board-ready KPI pack (ARR/MRR, cash, burn, runway, AR/AP aging).

Every workflow reads `finance-profile.md` first, so they all share one consistent model of the company.

## Reporting framework (the P&L and balance-sheet maps)

`onboarding` drafts two maps straight from your QuickBooks Account List, then has you review them:

- **P&L map** — each income-statement account → its `class` (Revenue / COGS / Expense / Other Income / Other Expense, from the QBO account type) and `department` (parsed from the account name).
- **Balance-sheet map** — each balance-sheet account → its `bs_group` (current / non-current assets, current / non-current liabilities, equity — from the QBO account type) and its cash-flow `cf_section` and `cf_line`.

You only correct the judgment calls (parsed departments, treasury-as-investing, and the like). Blank-header templates and the full column spec live in [`templates/`](./templates/).

## Slash command

- `/finance` — entry point that routes you to the workflow you want.

## Disclaimer

Unofficial. Not affiliated with, endorsed by, or sponsored by Stripe, Ramp, Mercury, Intuit (QuickBooks), or Anthropic. All trademarks belong to their respective owners.
