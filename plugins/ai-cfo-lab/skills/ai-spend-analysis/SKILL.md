---
name: ai-spend-analysis
description: >
  Build an org-wide Anthropic/Claude spend dashboard — person, department,
  product, and model breakdowns across three cost surfaces (committed seats /
  variable seat-overage / API-platform cash). Fires when the operator says
  "run the AI spend analysis", "refresh the AI spend dashboard", "how much are
  we spending on Claude / AI", "set up AI spend tracking", or "set up a daily
  AI spend dashboard for my team". First run walks a conversational SETUP
  (company, plan tier, seat prices, roster, org id) and scaffolds a local
  workspace; monthly runs pull the surfaces, rebuild the workbooks + interactive
  HTML dashboard, and draft (never send) a summary. Optionally it keeps a shared
  Claude Dashboard current every day through two scheduled jobs (a cloud
  routine reading API cost from Ramp, and a Mac job pulling the claude.ai spend
  export with a fixed script). It
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

## Three paths: first run, monthly run, or the daily dashboard?

- **`config/pipeline.json` does not exist, or the doctor reports failures → run SETUP** (below).
- **It exists → run the MONTHLY pipeline** (below).
- **The operator wants a shared, daily-refreshed Claude Dashboard, or a
  scheduled job is running this skill** → follow
  [`references/daily-refresh.md`](references/daily-refresh.md). It builds on
  the same workspace and pipeline; read it in full first.

Throughout: `$SKILL` = this skill's directory (the folder holding this file; its
`scripts/` subdir holds the pipeline). `$ROOT` = the operator's **workspace**
folder (e.g. `AI-Spend-Analytics/`), which holds `config/`, `raw/`, `workbooks/`,
`artifacts/`, `.secrets/`. The workspace is separate from the skill — it holds
the org's data and is never committed anywhere.

## Setup (first run, or resuming one) — doctor-driven

**Always start with the doctor**, whether setup is new, half-done, or something
broke: `python3 $SKILL/scripts/doctor.py "$ROOT" --json`. It runs every check in
setup order, reads the state from the workspace itself, and returns the next
step with its fix and **who can do it**. Work through `next`, run the doctor
again, repeat until it reports no failures. Never keep your own list of what's
done; the doctor is the record, and its log (`logs/setup.jsonl`) measures how
long setup took.

Talk to the operator in plain language, one step at a time; they mostly
confirm. The checks and how to clear each one:

| Check | How to clear it |
|---|---|
| `workspace` | Agree a folder **outside any git repo** (suggest `~/Desktop/AI-Spend-Analytics`), then `python3 $SKILL/scripts/scaffold.py "$ROOT"`. |
| `config_complete` | `doctor.py "$ROOT" --fix-config` (adds settings from newer versions; changes nothing existing). |
| `company`, `seat_prices_confirmed` | Ask for the company name and each seat type's monthly price (claude.ai → Settings → Billing); write `company_name`, `seat_rates`, and `standard_seat_rate_usd` in `thresholds.json`. Ask for the plan tier (`team` / `enterprise`) at the same time. |
| `org_id` | Team only. A claude.ai Owner copies it from Settings → Organization (or the `…/organizations/<id>/…` address). |
| `admin_key` | Optional. The **Console admin** creates an Admin key and pastes it into `$ROOT/PASTE_ADMIN_KEY_HERE.txt`; the next pipeline run (or `secure_key.py`) moves it to `.secrets/`. **Never accept a key in chat** — if one appears, refuse it, tell them to revoke it, and point at the file. |
| `admin_key_org` | When `api_cost_source` is `"ramp"`: call `ramp_get_ai_token_spend_connections` and compare its Anthropic `organization_id` with the id the doctor printed. **A mismatch is the single most damaging silent failure** (API cost reads near $0 with no error): the **Ramp admin** re-adds the right org's key in Ramp's AI-spend settings. |
| `claude_code_visibility` | A warning that the report sees API keys only is normal when the Team workspace and Console org are separate — explain it; nothing to fix. |
| `export_login` | Team only. A **claude.ai Owner** runs the `--login` command the doctor prints and signs in once in the window that opens. Claude must not drive claude.ai itself: unattended export sessions are refused by Claude Code's safety checks, so this is a fixed script. |
| `first_export` | `uv run --with playwright python $SKILL/scripts/fetch_surface_b_browser.py "$ROOT"` (or the manual export, saved to `raw/<YYYY-MM>/overage_spend.csv`). |
| `roster_real`, `roster_complete` | `bootstrap_roster.py "$ROOT" <YYYY-MM>` creates `config/roster.xlsx` from the export. Then ask for an HR/payroll export and run `match_roster.py "$ROOT" <file> --premium "<names>"`; resolve what it reports with `--set` by **asking the operator**, then `--write`. When two people could own an email, present both neutrally: don't suggest which is likelier (from department, products used or anything else) and don't pre-fill either name in a command; a wrong guess files that person's spend under the wrong department. |
| `roster_departments` | Show the one-person departments and ask whether any are typos. |
| `dashboard` | References `daily-refresh.md` → One-time setup. Ask about `dashboard_visibility` first (see Hard rules). |
| `mac_job` | `install_mac_job.py "$ROOT"` prints exactly what will run; show it, get a yes, then `--load`. |
| `data_fresh` | Read `logs/daily.log`; the doctor's detail says what failed. |

**When a step needs someone else** (the doctor's `role` isn't `Operator`), say
so plainly, offer a short message the operator can forward to that person
(what to do, where, and why it's needed), and carry on with the steps that
don't depend on it. Setup resumes from the doctor whenever they're back.

Two more settings to confirm before the first dashboard: the model-family
patterns in `config/models.json` (they drive the model tab and the routing
what-if) and `dashboard_visibility`.

To remove the setup from a machine: `uninstall.py "$ROOT"` lists what it would
remove; add `--yes` (and `--remove-login`, `--remove-key`, `--purge-data` as
wanted). The dashboard and any cloud routine are deleted on claude.ai.

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

*Optional automation (Team):* for unattended daily pulls use the fixed script
`fetch_surface_b_browser.py` (see `references/daily-refresh.md`) — an unattended
Claude session is refused this by Claude Code's safety checks. Interactively, with
Claude-in-Chrome: an authenticated in-page
fetch of the same export over an **unofficial** endpoint (`org_id` + pattern in
`pipeline.json`). It is the operator's own Owner session pulling their own export
— same data as the button — but undocumented, so it can drift. Use only if a
browser is available; fail loud (the validator + banner catch drift); never
treat it as required. Details in `references/dashboard-guide.md`; the daily
version (scheduled on the operator's Mac) is in `references/daily-refresh.md`.

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

In order: register the period (writes `raw/<period>/meta.json` if nothing has,
so a month with no export still shows — flagged); `secure_key.py` (ingest a
dropped `PASTE_ADMIN_KEY_HERE.txt`, if present); `ingest_ramp.py` (only when
`api_cost_source` or `card_charges_source` is `"ramp"` — parses the Ramp answers
saved into `raw/<period>/`); (Enterprise only) `fetch_surface_b_enterprise.py`;
then `fetch_surface_c.py` (Admin API via key, when `api_cost_source` is
`"admin_api"`, the default; gracefully `not_configured` if unset),
`fetch_claude_code.py` (the Admin API's Claude Code usage report → per-person
or per-key Claude Code usage; `not_configured` without a key),
`validate_surface_b.py` (schema + sanity → `surface_b_status.json`),
`apply_roster.py` (only when a `config/roster.xlsx|csv` exists — regenerates
`config/org_chart.csv` + `config/seats.csv` from it),
`build_workbooks.py` (rebuilds both `.xlsx` from **all** periods in `raw/`; writes
`build_summary.json`), `build_artifact.py` (writes `artifacts/<period>_ai_spend.html`),
`draft_slack.py` (writes `artifacts/<period>_slack_draft.txt`),
`build_dashboard_datasets.py` (writes `dashboard/<id>.json` + `manifest.json`
for the Claude Dashboard; `--datasets` on `run_pipeline.py` limits which).

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
- **Secrets never leak — the operator places them, not the assistant.** API keys
  live only in env vars or `$ROOT/.secrets/` (gitignored). The friendly path is the
  `PASTE_ADMIN_KEY_HERE.txt` drop file → `secure_key.py` (file → file, never through
  chat or a command). Never solicit a key in chat; if one appears there, refuse it
  and tell the operator to rotate. Never write a key to config, workbook, artifact,
  log, or chat.
- **Three surfaces stay visually distinct** everywhere. Overage is usage-credit
  spend beyond allotments; in-allotment usage is tokens-only by design (not a bug).
- **Fail loud.** A missing surface produces a banner + first-line summary alert,
  never a silent gap. Empty months never pollute flag lookbacks.
- **Config, not workbooks.** New hires / seat changes go in the roster
  (`config/roster.xlsx|csv`) — or edit `config/*.csv` directly; new API keys go in
  `config/api_key_map.csv`. The workbooks and artifact fully regenerate every run.
- **The shared dashboard follows `dashboard_visibility`.** `"department"` (the
  default) means no name or email is uploaded; `"person"` only when the operator
  says their organization has decided to share per-person spend. The filter
  runs before upload, because anyone who can open the dashboard can download
  its rows. Never change the setting on your own.
- **Scheduled jobs are proposals until approved.** Show the full routine or
  launchd configuration and get a yes before creating either. Keys never go to
  a cloud job: the cloud routine reads API cost through Ramp's connector and
  holds no secret; anything needing the Admin key or a claude.ai login runs on
  the operator's Mac.
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
| `scripts/bootstrap_roster.py` | Seed a fill-in `config/roster.xlsx` (or `.csv`) from the first spend export |
| `scripts/apply_roster.py` | Turn the roster into `config/org_chart.csv` + `config/seats.csv` (rates from `pipeline.json` `seat_rates`) |
| `scripts/fetch_claude_code.py` | Admin API Claude Code usage report → `raw/<period>/claude_code_usage.csv` (per person or API key, per day, per model) |
| `scripts/ingest_ramp.py` | Parse saved Ramp answers into `api_usage_cost.csv` (Surface C) and `card_charges.csv` |
| `scripts/build_dashboard_datasets.py` | The Claude Dashboard's datasets (`dashboard/*.json` + manifest), filtered by `dashboard_visibility` |
| `scripts/dashboard_page.html` | The Claude Dashboard's page (written once to the dashboard's `files/index.html`) |
| `references/daily-refresh.md` | Daily refresh runbook: dashboard setup, publishing datasets, the cloud routine, the Mac job, the Chrome export step, failure handling |
| `scripts/doctor.py` | Setup checks in order, each with its fix and who can do it; the next step; `--fix-config`; logs setup time |
| `scripts/match_roster.py` | Fill the roster from an HR/payroll export (email or name matching; reports ambiguity, never guesses) |
| `scripts/fetch_surface_b_browser.py` | Team-plan spend export by fixed script (`--login` once, `--check`, daily fetch with month-end catch-up) |
| `scripts/install_mac_job.py` | Preview, then install, the daily launchd job (generated commands, nothing typed) |
| `scripts/uninstall.py` | Remove the job, login, key or data — lists first, acts only with `--yes` |
| `references/setup-pitfalls.md` | Every failure seen in real installs, mapped to the doctor check that catches it; the roles setup needs |
| `references/security-overview.md` | One page for an IT/security reviewer: what data goes where, who can see it, what holds credentials |
| `scripts/secure_key.py` | Move an Admin key from the `PASTE_ADMIN_KEY_HERE.txt` drop file into `.secrets/` (600), then delete the drop |
| `scripts/artifact_template.html` | The dashboard template (config-driven; single file, no external calls) |
| `config.example/` | Templated config (fake values) — the shape setup fills in |
| `fixtures/` | Synthetic 3-month dataset + `make_fixtures.py` (seeded) for tests |
| `references/dashboard-guide.md` | Three-surface framing, plan-tier matrix, security model, data traps, roadmap |
| `USER_GUIDE.md` | Friendly end-user walkthrough (setup → export → roster → optional key → reading the dashboard) |

## Maintenance notes

- Seat prices in `seats.csv` are list-rate assumptions; update if actual invoices differ.
- **Endpoint drift (Team automation):** if the in-page spend-report fetch 404s,
  rediscover the endpoint via DevTools/network capture on the export modal and
  update `pipeline.json`. The manual export is always the safe fallback.
- **Model lines evolve:** update `config/models.json` patterns — no code change needed.
