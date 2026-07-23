---
name: ai-spend-analysis
description: >
  Build an org-wide Anthropic/Claude spend dashboard — person, department,
  product, and model breakdowns across three cost surfaces (committed seats /
  variable seat-overage / API-platform cash). Fires when the operator says
  "run the AI spend analysis", "refresh the AI spend dashboard", "how much are
  we spending on Claude / AI", or "set up AI spend tracking". First run walks a
  conversational SETUP (company, plan tier, seat prices, roster, org id) and
  scaffolds a local workspace; monthly runs pull the surfaces, rebuild the
  workbooks + interactive HTML dashboard, and draft (never send) a summary. It
  is a generalized, org-agnostic tool — any Claude for Work organization can run
  it against its own spend. It NEVER modifies seats, billing, or org settings,
  NEVER auto-sends anything, and does NOT cover non-Anthropic vendors
  (OpenAI/ChatGPT etc. — roadmap only).
---

# ai-spend-analysis

Turn an organization's Anthropic spend into a person / department / product /
model dashboard. The design rests on a **three-surface model** — three genuinely
separate pools of money that must stay visually distinct everywhere:

| Surface | What it is | Where it comes from |
|---|---|---|
| **A — Committed seats** | Recurring seat cash (constant until seats change) | `config/seats.csv` roster × list rate |
| **B — Variable overage** | Usage-credit spend *beyond* seat allotments (in-allotment usage is $0 by design — tokens capture it) | monthly seat-overage export |
| **C — API-platform cash** | Console/Developer-platform cost records | Anthropic Admin API |

Deeper framing, the plan-tier matrix, the security/privacy model, the data
traps, and the roadmap live in [`references/dashboard-guide.md`](references/dashboard-guide.md) — read it once before the first run.

## Two paths: is this a first run or a monthly run?

- **`config/pipeline.json` does not exist in the workspace → run SETUP** (below).
- **It exists → run the MONTHLY pipeline** (below).

Throughout: `$SKILL` = this skill's directory (the folder holding this file; its
`scripts/` subdir holds the pipeline). `$ROOT` = the operator's **workspace**
folder (e.g. `AI-Spend-Analytics/`), which holds `config/`, `raw/`, `workbooks/`,
`artifacts/`, `.secrets/`. The workspace is separate from the skill — it holds
the org's data and is never committed anywhere.

## Setup (first run — conversational)

Run it as a friendly first-run setup — ask, confirm, write; the operator mostly
confirms rather than types.

1. **Pick / confirm the workspace root** `$ROOT`. Scaffold it:
   `python3 $SKILL/scripts/scaffold.py "$ROOT"` — creates the folder tree and
   seeds `config/` from `$SKILL/config.example/` templates.
2. **Ask** for: company name; **plan tier** (`team` or `enterprise`); seat types
   and their monthly list prices; then write them into `$ROOT/config/pipeline.json`
   (`company_name`, `plan_tier`) and `$ROOT/config/thresholds.json`
   (`standard_seat_rate_usd`).
3. **Org id** — instruct the operator to copy it from their claude.ai admin URL;
   write it to `pipeline.json` `org_id`. (Team plan only; Enterprise does not
   need it for the Analytics API.)
4. **Roster** — accept a pasted/uploaded CSV of `email,name,department` → write
   `config/org_chart.csv` and `config/seats.csv`. If the operator has no roster
   handy, bootstrap the email list from the first spend export and ask only for
   departments.
5. **Model families** — the shipped `config/models.json` classifies models into
   `frontier | sonnet | haiku | other` by regex. Confirm the patterns match the
   org's current model lines; it drives the what-if routing panel's colors and
   labels (no code changes needed to update).
6. **Optional — Surface C key.** If they want API-platform cash, set
   `ANTHROPIC_ADMIN_API_KEY` (or drop it in `$ROOT/.secrets/anthropic_admin_key`).
   Skipping it is fine — the dashboard shows "Surface C not configured".
7. **Validate** by doing a first monthly run (below) and showing the dashboard.

## Monthly run (target period = last full calendar month, `YYYY-MM`)

### Step 1 — Surface B: the seat-overage export

**Team plan (default): manual export is the primary, documented path.** It works
everywhere, including plain Claude Code with no browser. The operator:
claude.ai → **Settings → Analytics → "How much is Claude costing?" → Export spend
report → Last Month**, then drops the CSV at `$ROOT/raw/<YYYY-MM>/overage_spend.csv`
and writes `raw/<YYYY-MM>/meta.json`:
`{"period":"YYYY-MM","days_covered":<n>,"partial":false,"source":"manual export <date>"}`.

> **90-day window — do not skip a month.** claude.ai only exports the trailing
> ~90 days; a missed month is unrecoverable. If a month is missing at run time,
> lead the summary with the gap — never backfill silently later.

*Optional automation (Team, Claude-in-Chrome only):* an authenticated in-page
fetch of the same export over an **unofficial** endpoint (`org_id` + pattern in
`pipeline.json`). It is the operator's own Owner session pulling their own export
— same data as the button — but undocumented, so it can drift. Use only if a
browser is available; fail loud (the validator + banner catch drift); never
treat it as required. Details in `references/dashboard-guide.md`.

**Enterprise plan:** no browser step — `run_pipeline.py` (Step 2) fetches Surface
B via the documented Analytics API (`fetch_surface_b_enterprise.py`). See the
"Enterprise" caveat in the reference guide (built from docs, awaiting a live
validator — see the roadmap).

**On any failure** (not logged in, non-200, non-CSV): do not fabricate or skip
silently. Write `meta.json` anyway so the period registers; validation stamps the
gap; the dashboard and summary lead with the "Surface B missing" banner.

### Step 2 — Scripted remainder

```
python3 $SKILL/scripts/run_pipeline.py "$ROOT" YYYY-MM
```

In order: (Enterprise only) `fetch_surface_b_enterprise.py`; then
`fetch_surface_c.py` (Admin API via key; gracefully `not_configured` if unset),
`validate_surface_b.py` (schema + sanity → `surface_b_status.json`),
`build_workbooks.py` (rebuilds both `.xlsx` from **all** periods in `raw/`; writes
`build_summary.json`), `build_artifact.py` (writes `artifacts/<period>_ai_spend.html`),
`draft_slack.py` (writes `artifacts/<period>_slack_draft.txt`).

> **openpyxl is optional.** Without it, the summary, dashboard, and Slack draft
> still build; only the two `.xlsx` workbooks are skipped. Install it for the
> Excel files: `pip install openpyxl`.

### Step 3 — Verify before reporting

- `workbooks/build_summary.json` — confirm the new period appears with plausible
  row counts and the expected flags.
- If openpyxl is installed, recalculate `ai_spend_output.xlsx` (Excel/LibreOffice
  recalc on open) and require zero formula errors.
- Confirm `artifacts/<period>_ai_spend.html` exists and, if any surface status
  isn't `ok`, carries the right banner.

### Step 4 — Deliver

- Present the artifact file and the Slack draft text **verbatim** to the operator.
- **Never send the Slack message; never auto-send anything.** If a Slack tool is
  connected, you may offer to stage a *draft* only. The operator sends it.

## Hard rules

- **Read-only on every financial surface.** Never modify seats, plans, billing,
  or org settings; sessions/keys are used for GET-equivalent reads only.
- **Secrets never leak.** API keys live only in env vars or `$ROOT/.secrets/`
  (gitignored). Never write a key to config, workbook, artifact, log, or chat.
- **Three surfaces stay visually distinct** everywhere. Overage is usage-credit
  spend beyond allotments; in-allotment usage is tokens-only by design (not a bug).
- **Fail loud.** A missing surface produces a banner + first-line summary alert,
  never a silent gap. Empty months never pollute flag lookbacks.
- **Config, not workbooks.** New hires / seat changes / new keys go in
  `config/*.csv`; the workbooks and artifact fully regenerate every run.
- **No real org data, no other vendors.** This ships with synthetic fixtures only;
  it covers Anthropic/Claude spend, not OpenAI/Gemini (on the roadmap).

## Files

| File | Purpose |
|---|---|
| `scripts/run_pipeline.py` | Orchestrator (plan-tier aware). Runtime entrypoint |
| `scripts/fetch_surface_c.py` | Admin API pull (env / `.secrets` key; graceful-missing) |
| `scripts/fetch_surface_b_enterprise.py` | Enterprise Surface B via the Analytics API (built from docs, untested live — roadmap) |
| `scripts/validate_surface_b.py` | Schema + sanity check → `surface_b_status.json` |
| `scripts/build_workbooks.py` | Both `.xlsx` + `build_summary.json` (openpyxl optional); hosts `load()`/`compute_flags()` |
| `scripts/build_artifact.py` | Self-contained interactive HTML dashboard |
| `scripts/draft_slack.py` | Draft summary `.txt` (never sends) |
| `scripts/scaffold.py` | Create a fresh workspace + seed config from templates |
| `scripts/artifact_template.html` | The dashboard template (config-driven; single file, no external calls) |
| `config.example/` | Templated config (fake values) — the shape setup fills in |
| `fixtures/` | Synthetic 3-month dataset + `make_fixtures.py` (seeded) for tests |
| `references/dashboard-guide.md` | Three-surface framing, plan-tier matrix, security model, data traps, roadmap |

## Maintenance notes

- Seat prices in `seats.csv` are list-rate assumptions; update if actual invoices differ.
- **Endpoint drift (Team automation):** if the in-page spend-report fetch 404s,
  rediscover the endpoint via DevTools/network capture on the export modal and
  update `pipeline.json`. The manual export is always the safe fallback.
- **Model lines evolve:** update `config/models.json` patterns — no code change needed.
