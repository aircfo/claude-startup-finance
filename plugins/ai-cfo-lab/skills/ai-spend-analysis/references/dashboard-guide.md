# AI Spend Dashboard — reference guide

Deeper context for `ai-spend-analysis`. The operational runbook is in
[`../SKILL.md`](../SKILL.md); this file is the "why" behind it.

## The three-surface model (the core idea)

Most AI-spend confusion comes from treating one number as "the AI bill." There
are three genuinely different pools of money, and mixing them hides the levers:

- **A — Committed seats (cash).** What you pay per seat every month regardless of
  usage. Constant until you add/remove/downgrade seats. Source: your seat roster
  × list rate (`config/seats.csv`).
- **B — Variable overage (usage credits).** Spend *beyond* what a seat's
  allotment covers. **In-allotment usage costs $0** — so a heavy user fully
  inside their allotment shows large token counts but $0 overage. That is by
  design, not a gap; the token columns capture the consumption. Source: the
  monthly seat-overage export.
- **C — API-platform cash.** Console / Developer-platform usage billed as cash,
  entirely separate from seats. Source: the Anthropic Admin API. Cost records are
  workspace-keyed (no user dimension), so department attribution runs
  workspace → key owners (`config/api_key_map.csv`) → department; mixed-owner
  workspaces surface as such rather than being guessed.

The dashboard keeps these three visually distinct in every view (color-coded in
the trend chart, separate columns in the department table). Collapsing them is
the one thing not to do.

## Plan-tier matrix — where Surface B comes from

| | **Team plan** | **Enterprise plan** |
|---|---|---|
| Surface B source | claude.ai spend-report export | documented Analytics API |
| Primary method | **Manual export** (Settings → Analytics → "How much is Claude costing?") | `fetch_surface_b_enterprise.py` (scripted, no browser) |
| Optional automation | authenticated fetch of the same export (unofficial endpoint): daily via the fixed script `fetch_surface_b_browser.py` in `daily-refresh.md` | n/a — the API is the path |
| Window | trailing ~90 days (export monthly or lose it) | programmatic, no 90-day trap |
| User dimension | per-user in the export | per-user via the API |
| Status | validated in production | **built from docs, untested live (see roadmap)** |

Set `plan_tier` in `config/pipeline.json`. Everything downstream of the fetch is
identical for both tiers.

### The unofficial endpoint disclaimer (Team automation)

The optional in-page fetch hits `/api/organizations/{org_id}/analytics/spend-report-export`
— an **undocumented** endpoint. It is the operator's own Owner session pulling
their own export (the same data as the export button), so it is defensible, but
undocumented means it can change without notice. Containment: `validate_surface_b.py`
checks schema + sanity and writes a status file; a drift or failure raises a loud
banner on the dashboard and the first line of the summary. If it 404s,
rediscover the endpoint via DevTools on the export modal and update
`pipeline.json`. The manual export is always the safe fallback, so the automation
is a convenience, never a dependency.

## Security & privacy model

- **This tool produces per-employee spend data.** The dashboard and workbooks
  name individuals and their spend. Decide your access model *before* circulating
  the artifact — treat inputs and outputs as admin-only.
- **The roster comes from your own data.** The people list is seeded from your
  spend export (`bootstrap_roster.py` → `config/roster.xlsx|csv`) and never leaves
  the workspace; you only add department + seat type. `apply_roster.py` maps it to
  `org_chart.csv`/`seats.csv`, deriving each seat's cash from `pipeline.json`
  `seat_rates`.
- **Admin-only inputs.** The seat/overage/API data all require org-admin access
  to obtain. The pipeline is **read-only** on every surface — it never modifies
  seats, billing, or org settings.
- **Key handling.** The Admin API key (`ANTHROPIC_ADMIN_API_KEY`) and the
  Enterprise Analytics key (`ANTHROPIC_ANALYTICS_API_KEY`) live only in env vars
  or `$ROOT/.secrets/` (gitignored). They are never written to config, workbooks,
  the artifact, logs, or chat. The operator supplies the Admin key via the
  `PASTE_ADMIN_KEY_HERE.txt` drop file (`secure_key.py` moves it into `.secrets/`
  and deletes the drop) or an env var — **never by pasting it into chat**; if a key
  ever lands in chat, treat it as compromised and rotate it.
- **Cowork secret caveat.** Claude on the web has no secrets store yet (its env-var
  field warns against secrets), and file-upload transcript privacy isn't documented.
  So on Cowork, run Surface C from a local/CLI session, or leave it "not configured"
  until a platform secrets store lands (tracking: `anthropics/claude-code#32733`).
  Surfaces A and B need no key and work fully on Cowork.
- **The shared Claude Dashboard is a different exposure.** Unlike the local
  HTML file, a dashboard lives at a link, and everyone it is shared with can
  download every dataset's rows from its Sources panel. So
  `dashboard_visibility` filters people out *before* upload: `"department"`
  (the default) uploads no names or emails at all; `"person"` uploads
  per-person rows and is for organizations that have decided to share them.
- **No keys in the cloud.** The daily cloud routine reads API cost through
  Ramp's AI-spend connector, where Ramp holds the Anthropic admin key; the
  routine itself holds no secret. Anything that needs the Admin key or a
  claude.ai login runs on the operator's Mac (`references/daily-refresh.md`).
- **The artifact is self-contained.** Single HTML file, data embedded as JSON at
  build time — no external calls, no CDN, no secrets. Safe to open offline.
- **Nothing is ever sent.** `draft_slack.py` writes a `.txt` and prints it; the
  operator delivers it. There is no auto-send path anywhere.

## Data traps (read before interpreting the numbers)

1. **Overage-only dollars.** Surface B dollars are *overage*, not total usage.
   A $0 overage row with millions of tokens means "fully inside allotment," not
   "no usage."
2. **Tokens ≠ cost.** The token columns measure consumption; the dollar columns
   measure billed overage. They move together only past the allotment line.
3. **Partial months.** The latest month is often partial (you export before it
   ends). The dashboard marks it and adds a dashed run-rate forecast bar that
   disappears once the full month lands. Flag lookbacks exclude partial/empty
   months so they don't distort trends.
4. **API department attribution needs owners.** API cash only maps to a
   department when the workspace's keys have an `owner_email` in
   `api_key_map.csv`. Unowned keys surface as an "(API — unassigned keys)" bucket
   and an `unowned_api_key` flag, not a silent miss.
5. **Three kinds of Claude Code and API dollars.** Seat overage (Surface B)
   is billed. The Claude Code usage report's cost is Anthropic's *estimate at
   list price*, including usage still inside a seat's allowance. Ramp's API
   cost is Ramp's estimate from token counts. The dashboard labels each and
   never adds the estimates to billed totals.
6. **The Claude Code report sees one organization.** It reports on the Admin
   key's Console organization. When the claude.ai Team workspace is a separate
   organization, it shows only Claude Code run on API keys (`customer_type`
   `api`) — no Team-seat users. Probe once before counting on it.
7. **Card charges sit beside the totals.** Anthropic charges on company cards
   (from Ramp) are actual cash, but a seat invoice paid by card is already in
   committed seats, so the card figure is a cross-check, not a fourth surface
   to add.
8. **Routing what-if is a model, not advice.** The what-if panel estimates
   savings from shifting frontier-model traffic to a cheaper family at the
   observed cost/request. It assumes comparable request counts and does not judge
   quality — that call is the operator's.

## Roadmap

- **Cross-vendor.** OpenAI/ChatGPT workspace + API surfaces (and later
  Gemini/Copilot). The three-surface framing generalizes; the fetchers don't
  exist yet. This is the biggest open item.
- **Enterprise validation.** `fetch_surface_b_enterprise.py` is built
  against the public Analytics API docs but has not run against a live Enterprise
  org. The exact endpoint path and field names are overridable from
  `pipeline.json` (`surface_b_enterprise_path` / `surface_b_enterprise_fields`)
  so a tester can correct them without editing code; it fails loud on any shape
  mismatch. Validation from an Enterprise org is welcome.
- **Team-plan export without a browser.** The daily per-person export runs
  through a fixed script and a signed-in browser profile against an
  undocumented endpoint, because Team plans have no spend API. If Anthropic
  opens the Analytics API (or an equivalent) to Team plans, the Mac job's
  browser step becomes a plain API call and the whole
  refresh can move to the cloud.
- **Not planned:** any form of auto-send (never).

## Design decisions

- **2026-10 — daily refresh into a Claude Dashboard (v0.2.0).** Reversed two
  earlier "not planned" items: Ramp is now an optional source (API cost from
  its AI-spend connection; Anthropic card charges), and the skill documents
  scheduled jobs. Why: teams asked for a current, shared view, and a monthly
  file couldn't give one. How it is bounded:
  - *Two jobs, split by sensitivity.* A cloud routine refreshes only org-wide
    API cost (no people, no keys). A Mac job handles everything per-person or
    key-bearing (spend export, Claude Code report, card charges). Each owns its
    own datasets, so they never overwrite each other.
  - *Pushed files, not live queries.* The dashboard's live queries run with each
    reader's own connector access, so teammates without Ramp would see errors.
    The jobs upload pre-computed files instead, each keeping its Ramp query on
    record so an editor can see what produced it.
  - *Visibility filtered before upload,* defaulting to department level.
  - *Browser automation accepted for the export, with no AI in it.* Claude
    Code's safety checks refuse to let an unattended Claude session export
    per-person data from an Owner's claude.ai session (tested with
    `dontAsk` and a four-tool allowlist). Rather than loosen that, the export
    is a fixed script: one read-only GET through a dedicated browser profile,
    bytes saved as received, schema-checked, failures shown on the dashboard,
    and the manual export as the fallback.
  - *Copied data is verified.* Ramp answers reach the scripts through a model
    writing them to disk, so each is checked against Ramp's own transaction
    count or per-model total before anything is published.
- **2026-10 — the Claude Code report as a supporting source.** It is the only
  documented per-person feed on a Team plan, but it covers Claude Code only,
  reports estimated (not billed) cost, and only sees the Admin key's own Console
  organization. It sits beside the export rather than replacing it.
