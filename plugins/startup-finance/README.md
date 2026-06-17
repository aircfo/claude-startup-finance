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

- **runway-and-burn** — net monthly burn and months of cash (Mercury + Ramp, offset by revenue).
- **revenue-reconciliation** — tie Stripe revenue to QuickBooks recognized revenue and explain the gap.
- **board-metrics** — a board-ready KPI pack (ARR/MRR, cash, burn, runway, AR/AP aging).

## Slash command

- `/finance` — entry point that routes you to the workflow you want.

## Disclaimer

Unofficial. Not affiliated with, endorsed by, or sponsored by Stripe, Ramp, Mercury, Intuit (QuickBooks), or Anthropic. All trademarks belong to their respective owners.
