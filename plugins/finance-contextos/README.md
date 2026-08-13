# finance-contextos (plugin)

**Build your company's ContextOS** — the finance context Claude loads before touching your
numbers. This is the flagship plugin of the **(Un)official Claude for Startup Finance**
marketplace: one connector, one guided build, one review — and every finance conversation
after starts from your definitions instead of generic ones.

## What a ContextOS is

AI on finance data doesn't fail on *access* — connectors solve that. It fails on
*semantics*: which accounts count as cash for runway, what "MRR" means in your board deck,
which vendors are COGS, which one-time costs to exclude from run-rate burn. Those answers
live in close checklists, board decks, and your head — not in any one system.

A ContextOS captures them once, in files you own:

- **`finance-profile.md`** — your finance function's operating manual: KPI definitions,
  cash and burn rules, source-of-truth mappings, known exceptions and judgment calls,
  open questions. Every workflow reads it first.
- **`account-map.csv`** — every QuickBooks account classified for management reporting,
  editable in any spreadsheet.
- **`context/`** — the source docs you've shared, kept as a record of what's been ingested.
- **`CHANGELOG.md`** — a dated log of what changed each run.

**A ContextOS isn't done until it ties.** The build ends by proving the model against your
live books — cash to the bank balance, revenue coverage to the penny. Unexplained
differences become open questions, never silent assumptions.

## Connector

| Connector | Transport | Auth |
| --- | --- | --- |
| QuickBooks | Remote (HTTP) | Per-user OAuth in your browser — **your own** QuickBooks login, read-only |

One sign-in. The connector routes through an airCFO-operated MCP server
([source, MIT-licensed](https://github.com/aircfo/qbo-mcp) — you can also
[self-host it](https://aircfo.github.io/claude-startup-finance/)); see
[Data handling & security](#data-handling--security) for exactly what it stores.

## The skill

**finance-context-builder** — a guided ~15–20 minute session:

1. Pick where your ContextOS folder lives (default: your Desktop).
2. Authorize QuickBooks (one OAuth pop-up; Claude confirms the company name it connected to).
3. Tell Claude about your business — paste a board deck, an SOP, or just talk.
4. Claude drafts your account map from the full QuickBooks account list; **you review only
   the judgment calls**, not hundreds of rows.
5. Claude writes your finance profile — what it can't know becomes an explicit
   `[PLACEHOLDER]`, never a guess.
6. The tie-out: the freshly built ContextOS is checked against your live books before
   you're told it's done.

Run it again anytime to refresh: re-pulls the account list, diffs it against your map
(rows you've confirmed are never overwritten), folds in new context, and logs the changes.

## The account map (the cube)

The map is drafted one row per GL account, keyed on QuickBooks' internal account Id, and
it's a **cube, not a tree** — independent axes any report can pivot:

- **Ledger facts** — QuickBooks type, detail type, parent, active flag, verbatim.
- **`expense_category`** — what *kind* of money (Subscription revenue, Hosting &
  infrastructure, Payroll & benefits, …), from a fixed vocabulary.
- **`department`** — *whose* money (Engineering, Sales, Marketing, G&A, …).
- **`cf_section` / `cf_line`** — how each balance-sheet account's change feeds the
  cash-flow statement.
- **`tags`** — cross-cutting analysis groups from a small registry: `mrr` (defines your
  P&L-based MRR/ARR), `cac`, `contra-revenue`, `clearing`, and friends.
- **Governance** — every row is `auto`, `needs-review`, or `confirmed`; refreshes never
  overwrite what you've confirmed.

The blank template and full spec — vocabularies, tag registry, cash-flow lines, refresh
rules — live in [`skills/finance-context-builder/templates/`](./skills/finance-context-builder/templates/).

## Using it

Say **"build my ContextOS"** (or `/finance-context-builder`). When it's done, your
ContextOS is a folder you can open, edit, and version like any other files you own.

**Grow it from here:** install the **all-systems-go** plugin from this same marketplace to
connect Stripe, Ramp, and Mercury (they enrich the profile's revenue, spend, and cash
sections) and to add cross-system workflows — runway & burn, revenue reconciliation, board
metrics — plus meta-skills for authoring your own. Every one of them reads your ContextOS
first.

## Data handling & security

- Read-only by design: the skill never writes to QuickBooks — no journal entries, no
  writeback of any kind.
- Per-user OAuth: you authenticate into your own QuickBooks in your browser. No API keys
  or tokens are stored in this repository.
- **Your financial data is never stored on the server.** Reports and balances are pulled
  fresh from QuickBooks each time and shown to you — never saved server-side.
- **Only the connection itself is kept** — your QuickBooks tokens (encrypted at rest),
  your company name, and the email you enter when connecting.
- **You stay in control.** Tell Claude to "disconnect QuickBooks" anytime; the server
  revokes access and erases what it kept.
- Local files are written only to the ContextOS folder you approve (plus, with your OK,
  a small pointer file so workflows can find it).
- Don't place secrets, tokens, or full account numbers in your ContextOS files.
- Prefer not to route through airCFO's server? The connector is MIT-licensed —
  [deploy your own](https://github.com/aircfo/qbo-mcp) and point the plugin at it.

## Disclaimer

Unofficial. Not affiliated with, endorsed by, or sponsored by Intuit (QuickBooks) or
Anthropic. All trademarks belong to their respective owners.

---

Part of [(Un)official Claude for Startup Finance](https://github.com/aircfo/claude-startup-finance)
by [airCFO](https://aircfo.com) · [Docs](https://aircfo.github.io/claude-startup-finance/) ·
[The AI CFO Newsletter](https://www.aircfo.com/the-ai-cfo) ·
[Report an issue](https://github.com/aircfo/claude-startup-finance/issues)
