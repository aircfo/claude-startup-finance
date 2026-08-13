# all-systems-go (plugin)

The **enrichment pack** for your ContextOS — named for airCFO's *All Systems Go* series on
the startup back-office stack. Where [`finance-contextos`](../finance-contextos/) builds
your finance context from QuickBooks, this plugin connects the rest of that stack and adds
cross-system workflows that read your ContextOS first.

**Install [`finance-contextos`](../finance-contextos/) first** — every workflow here reads
the finance profile it produces. Without one, the workflows will tell you to build it.

## Connectors

| Connector | Transport | Auth |
| --- | --- | --- |
| Stripe | Remote (HTTP) | Per-user OAuth in your browser |
| Ramp | Remote (HTTP) | Per-user OAuth in your browser |
| Mercury | Remote (HTTP) | Per-user OAuth in your browser |

You authenticate into **your own** accounts in your browser. API keys and OAuth tokens are
not stored in this repository. The QuickBooks connector ships with `finance-contextos`,
not here — the two plugins never double-register a connector.

Connecting these systems enriches your ContextOS: re-run the context builder after
authorizing and it maps each Mercury account, Ramp clearing account, and Stripe payout
stream onto your GL (the money-flow graph), and fills the revenue, spend, and cash
sections that QuickBooks alone can't.

## Skills

- **runway-and-burn** — net monthly burn and months of cash (Mercury + Ramp, offset by revenue).
- **revenue-reconciliation** — tie Stripe revenue to QuickBooks recognized revenue and explain the gap.
- **board-metrics** — a board-ready KPI pack (ARR/MRR, cash, burn, runway, AR/AP aging).

Every workflow reads your ContextOS first — using the saved pointer when available and
falling back to the default Desktop folder — so they all share one consistent model of
the company: your definitions of burn and MRR, your account map, your judgment calls.

### Build your own

The shipped workflows are starting points — every finance team runs its own. Two
**meta-skills** turn *your* workflow into a reusable skill that follows the same house
conventions (loads the ContextOS first, read-only, computation-checked math, confirms the
period, paste-ready output):

- **finance-skill-builder** — author a new skill, either by capturing a workflow you just
  ran in the conversation ("save what we just did") or through a short interview ("build me
  a skill for our monthly flux review"). Generates a copy-ready skill for your own workspace
  (`.claude/skills/` in the project, or `~/.claude/skills/` to use everywhere) — it never
  writes into the installed plugin, so it survives updates.
- **finance-skill-tuner** — fix a skill that isn't behaving: won't trigger, fires when it
  shouldn't, skips a confirmation, or returns the wrong format. It diagnoses the cause and
  explains the fix in plain language.

## Using it

Just ask in plain English — the right skill runs automatically (e.g. "what's our runway?"
→ `runway-and-burn`). Each skill is also invocable by name (e.g. `/board-metrics`).

Setup expectations:
- **Best experience:** a built ContextOS plus Stripe, Ramp, and Mercury.
- Missing connectors aren't blockers — their workflows and profile sections stay as
  explicit placeholders until connected, never guesses.

## Data handling & security

- The plugin connects to your finance systems through the providers' remote MCP servers
  using per-user OAuth.
- Designed for read-only analysis: workflow skills must not write to Stripe, Ramp, or
  Mercury.
- Outputs are analysis for human review; every number cites its source, and unsourced
  values are flagged rather than filled.
- Do not place secrets, tokens, or full account numbers in your ContextOS files.

## Disclaimer

Unofficial. Not affiliated with, endorsed by, or sponsored by Stripe, Ramp, Mercury, or
Anthropic. All trademarks belong to their respective owners.

---

Part of [(Un)official Claude for Startup Finance](https://github.com/aircfo/claude-startup-finance)
by [airCFO](https://aircfo.com) · [Docs](https://aircfo.github.io/claude-startup-finance/) ·
[The AI CFO Newsletter](https://www.aircfo.com/the-ai-cfo) ·
[Report an issue](https://github.com/aircfo/claude-startup-finance/issues)
