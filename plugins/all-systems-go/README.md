# all-systems-go (plugin)

Cross-system finance workflows, named for airCFO's *All Systems Go* series on the startup
back-office stack. This plugin connects Stripe, Ramp, and Mercury and adds workflows that
read your company's definitions before they touch a number.

**Pairs with the [Finance Brain Starter Kit](https://aircfo.github.io/claude-startup-finance/finance-brain.html).**
Every workflow here reads your Finance Brain first: the `CLAUDE.md` and `handbook/` folder
the free kit helps you build. Without one, the workflows say so and won't guess at your
definitions.

## Connectors

| Connector | Transport | Auth |
| --- | --- | --- |
| Stripe | Remote (HTTP) | Per-user OAuth in your browser |
| Ramp | Remote (HTTP) | Per-user OAuth in your browser |
| Mercury | Remote (HTTP) | Per-user OAuth in your browser |

You authenticate into **your own** accounts in your browser. API keys and OAuth tokens are
not stored in this repository.

**QuickBooks** isn't bundled here. Revenue reconciliation and board metrics read it through
a QuickBooks connector you add in Claude's connector settings (for example, Intuit's), with
your own login. Without one, those workflows ask for the specific QuickBooks export they
need instead.

Connected these systems after building your Finance Brain? Re-run the kit's
`setup-finance-brain` skill and it folds each bank account, card, and payout stream
into `handbook/cash.md` and `handbook/systems-and-data.md`.

## Skills

- **runway-and-burn** — net monthly burn and months of cash (Mercury + Ramp, offset by revenue).
- **revenue-reconciliation** — tie Stripe revenue to QuickBooks recognized revenue and explain the gap.
- **board-metrics** — a board-ready KPI pack (ARR/MRR, cash, burn, runway, AR/AP aging).

Every workflow reads your Finance Brain first (the folder you're working in, or the one
you point it to), so they all share one consistent model of the company: your definitions
of burn and MRR, your reporting rollups, your judgment calls.

### Build your own

The shipped workflows are starting points — every finance team runs its own. Two
**meta-skills** turn *your* workflow into a reusable skill that follows the same house
conventions (reads the Finance Brain first, read-only, computation-checked math, confirms the
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
- **Best experience:** a built Finance Brain plus Stripe, Ramp, Mercury, and QuickBooks.
- Missing connectors aren't blockers: whatever a workflow couldn't read stays an explicit
  open question until connected, never a guess.

## Data handling & security

- The plugin connects to your finance systems through the providers' remote MCP servers
  using per-user OAuth.
- Designed for read-only analysis: workflow skills must not write to Stripe, Ramp, or
  Mercury.
- Outputs are analysis for human review; every number cites its source, and unsourced
  values are flagged rather than filled.
- Do not place secrets, tokens, or full account numbers in your Finance Brain files.

## Disclaimer

Unofficial. Not affiliated with, endorsed by, or sponsored by Stripe, Ramp, Mercury,
Intuit (QuickBooks), or Anthropic. All trademarks belong to their respective owners.

---

Part of [(Un)official Claude for Startup Finance](https://github.com/aircfo/claude-startup-finance)
by [airCFO](https://aircfo.com) · [Docs](https://aircfo.github.io/claude-startup-finance/) ·
[The AI CFO Newsletter](https://www.aircfo.com/the-ai-cfo) ·
[Report an issue](https://github.com/aircfo/claude-startup-finance/issues)
