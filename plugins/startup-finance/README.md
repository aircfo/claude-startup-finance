# startup-finance (plugin)

The bundled plugin behind the **(Un)official Claude for Startup Finance** marketplace. It wires up the four connectors a typical startup back office runs on and adds finance skills that work *across* them.

## Connectors

| Connector | Transport | Auth |
| --- | --- | --- |
| Stripe | Remote (HTTP) | Per-user OAuth in your browser |
| Ramp | Remote (HTTP) | Per-user OAuth in your browser |
| Mercury | Remote (HTTP) | Per-user OAuth in your browser |
| QuickBooks | Remote (HTTP) | Per-user OAuth in your browser |

You authenticate into **your own** accounts in your browser. Authentication is per-user OAuth; API keys and OAuth tokens are not stored in this repository. During beta, QuickBooks requests route through an airCFO-operated MCP server — see [Data handling & security](#data-handling--security).

## Skills

- **finance-context-builder** — build the company's finance semantic map (`finance-profile.md`): draft an account map (`account-map.csv`) from your QuickBooks Account List (you review), then resolve how Mercury, Ramp, and Stripe accounts map onto the GL. **Run this first.**
- **runway-and-burn** — net monthly burn and months of cash (Mercury + Ramp, offset by revenue).
- **revenue-reconciliation** — tie Stripe revenue to QuickBooks recognized revenue and explain the gap.
- **board-metrics** — a board-ready KPI pack (ARR/MRR, cash, burn, runway, AR/AP aging).

Every workflow reads `finance-profile.md` first — using the saved airCFO Finance Context pointer when available and falling back to the default Desktop folder — so they all share one consistent model of the company.

### Build your own

The shipped workflows are starting points — every finance team runs its own. Two **meta-skills** let you turn *your* workflow into a reusable skill that follows the same house conventions (loads the finance profile first, read-only, computation-checked math, confirms the period, paste-ready output):

- **finance-skill-builder** — author a new skill, either by capturing a workflow you just ran in the conversation ("save what we just did") or through a short interview ("build me a skill for our monthly flux review"). Generates a copy-ready skill for your own workspace (`.claude/skills/` in the project, or `~/.claude/skills/` to use everywhere) — you choose where to save it; it never writes into the installed plugin, so it survives updates.
- **finance-skill-tuner** — fix a skill that isn't behaving: won't trigger, fires when it shouldn't, skips a confirmation, or returns the wrong format. It diagnoses the cause and explains the fix in plain language.

## Reporting framework (the account map)

`finance-context-builder` drafts a single **account map** (`account-map.csv`) straight from your QuickBooks Account List — one row per account — then has you review it:

- Every account carries its QuickBooks **type** and **detail type** (verbatim) plus a short **description**.
- **P&L accounts** also get a management-reporting **group** (`reporting_group`) — `Revenue`, `Cost of Goods Sold`, or an OpEx department (G&A, Engineering, Sales, Marketing, …) — classified with judgment from the name, the parent account, or what the account is for.
- **Balance-sheet accounts** instead get a cash-flow mapping — a `cf_section` (Operating / Investing / Financing) and `cf_line` — so each account's period-over-period change feeds the right cash-flow line.

You only correct the judgment calls (the OpEx departments and the odd treasury-as-investing call). The blank template and full column spec live in [`skills/finance-context-builder/templates/`](./skills/finance-context-builder/templates/).

## Using it

Just ask in plain English — the right skill runs automatically (e.g. "what's our runway?" → `runway-and-burn`). Each skill is also invocable by name (e.g. `/finance-context-builder`). **Run finance-context-builder first** — every other skill reads the profile it produces.

Recommended first session: install → `/finance-context-builder` → share a finance artifact if you have one → review the drafted account map → finalize the profile (placeholders are fine) → ask "what's our runway?" → ask "give me board metrics for last month." You should come away with `finance-profile.md`, `account-map.csv`, a list of open questions, and at least one workflow output.

Setup expectations:
- **Best experience:** QuickBooks + Stripe + Ramp + Mercury.
- **Minimum useful setup:** QuickBooks plus at least one operating system (Stripe, Ramp, or Mercury).
- Missing connectors aren't blockers — their profile sections and workflows stay as explicit placeholders until connected, never guesses.

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

What the beta QuickBooks connection stores and logs:
- **Your financial data is never stored.** Reports, ledgers, and balances are pulled fresh from QuickBooks each time you ask a question and shown to you — never saved or copied anywhere on the server.
- **Only the connection itself is kept** — your QuickBooks login (stored encrypted, so it's unreadable even if someone got hold of the file), your company name, and the email you enter when connecting. Nothing else.
- **You stay in control.** Tell Claude to "disconnect QuickBooks" anytime and the server immediately cuts off access and erases what it kept.
- **Records are activity-only** — which tool ran, when, and whether it worked — kept only to keep the service healthy. They never include your financial data or report contents.

## Disclaimer

Unofficial. Not affiliated with, endorsed by, or sponsored by Stripe, Ramp, Mercury, Intuit (QuickBooks), or Anthropic. All trademarks belong to their respective owners.
