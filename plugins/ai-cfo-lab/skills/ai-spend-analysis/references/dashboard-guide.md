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
| Optional automation | authenticated in-page fetch (Claude-in-Chrome, unofficial endpoint) | n/a — the API is the path |
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
5. **Routing what-if is a model, not advice.** The what-if panel estimates
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
- **Not planned:** card-feed ingestion (Ramp), scheduled-task auto-setup, and any
  form of auto-send (never).
