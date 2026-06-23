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

- **finance-context-builder** — build the company's finance semantic map (`finance-profile.md`): draft an account map (`account-map.csv`) from your QuickBooks Account List (you review), then resolve how Mercury, Ramp, and Stripe accounts map onto the GL. **Run this first.**
- **runway-and-burn** — net monthly burn and months of cash (Mercury + Ramp, offset by revenue).
- **revenue-reconciliation** — tie Stripe revenue to QuickBooks recognized revenue and explain the gap.
- **board-metrics** — a board-ready KPI pack (ARR/MRR, cash, burn, runway, AR/AP aging).

Every workflow reads `finance-profile.md` first, so they all share one consistent model of the company.

### Build your own

The shipped workflows are starting points — every finance team runs its own. Two **meta-skills** let you turn *your* workflow into a reusable skill that follows the same house conventions (loads the finance profile first, read-only, computation-checked math, confirms the period, paste-ready output):

- **finance-skill-builder** — author a new skill, either by capturing a workflow you just ran in the conversation ("save what we just did") or through a short interview ("build me a skill for our monthly flux review"). Writes it to your own workspace (`.claude/skills/` in the project, or `~/.claude/skills/` to use everywhere) — never into the installed plugin, so it survives updates.
- **finance-skill-tuner** — fix a skill that isn't behaving: won't trigger, fires when it shouldn't, skips a confirmation, or returns the wrong format. It diagnoses the cause and explains the fix in plain language.

## Reporting framework (the account map)

`finance-context-builder` drafts a single **account map** (`account-map.csv`) straight from your QuickBooks Account List — one row per account — then has you review it:

- **Income-statement accounts** → a `class` (Revenue / COGS / Expense / Other Income / Other Expense, from the QBO account type) and a `department` (classified with judgment — from the name, the parent account, or what the account is for).
- **Balance-sheet accounts** → a `bs_group` (current / non-current assets, current / non-current liabilities, equity) and a cash-flow `cf_section` and `cf_line`.

You only correct the judgment calls (departments, treasury-as-investing, and the like). The blank template and full column spec live in [`templates/`](./templates/).

## Using it

Just ask in plain English — the right skill runs automatically (e.g. "what's our runway?" → `runway-and-burn`). Each skill is also invocable by name (e.g. `/finance-context-builder`). **Run finance-context-builder first** — every other skill reads the profile it produces.

## Disclaimer

Unofficial. Not affiliated with, endorsed by, or sponsored by Stripe, Ramp, Mercury, Intuit (QuickBooks), or Anthropic. All trademarks belong to their respective owners.
