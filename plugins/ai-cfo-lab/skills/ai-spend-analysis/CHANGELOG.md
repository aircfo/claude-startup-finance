# Changelog — ai-spend-analysis

## v0.4.0 — Unreleased

The skill becomes a thin layer over the open-source engine,
[aircfo/aicfo-spend-analysis](https://github.com/aircfo/aicfo-spend-analysis). The math
moved there; the skill gathers the inputs and shows the answers.

- `scripts/aicfo_spend.py` is the launcher. The first run downloads the pinned engine
  release into the company's folder and checks its SHA-256. Later runs use it offline.
  Nothing is installed.
- Built on Ramp. API spend for Anthropic and OpenAI, and the people list, come through the
  Ramp connector. Ramp holds the Admin keys.
- `scripts/fetch_spend_export.py` replaces `fetch_surface_b_browser.py`. It hands each
  export to the engine's `save`, and finishes last month first when its newest export
  stops short.
- The daily refresh is a Cowork scheduled task working in the company's folder.
- Removed the v0.3.0 pipeline: the doctor, the roster matcher, the workbooks, the HTML
  dashboard, the Admin API fetchers, reconciliation, the Mac job installer and the fixtures.
  Its history is in the engine repo's `legacy/` folder until the cut-over deletes it.

## v0.3.0 — Unreleased

Setup a non-technical operator can finish alone, and an outside company can
approve. Built from the friction of the first real install
(`references/setup-pitfalls.md`), not from guesses.

- `doctor.py` — every setup check in order, each with its fix and **who** can
  fix it (operator, claude.ai Owner, Console admin, Ramp admin). The next step
  is the first unfinished check, read from the workspace itself, so setup
  resumes anywhere. Catches the silent failures from the first install: Ramp
  connected to the wrong Console org (prints the Admin key's own org via
  `/v1/organizations/me`), a Claude Code report that can't see seat users,
  template seat prices and sample roster left in place, settings missing after
  an upgrade (`--fix-config`). Logs statuses per run so setup time is measured.
- `match_roster.py` — fills the roster from an HR/payroll export by email or
  name, prefers active rows, handles contractor rows, and reports every
  ambiguity instead of guessing. Reproduced the first install's hand-matched
  roster exactly.
- `install_mac_job.py` — previews, then installs, the daily launchd job; the
  commands are generated, so nobody types them.
- `uninstall.py` — removes the job, saved sign-in, key or data; lists first.
- `reconcile.py` — compares a closed month with the invoices: each surface
  within $1.00 or 0.5%, whichever is larger.
- `fetch_surface_b_browser.py --check` tests the saved sign-in without saving.
- Docs: role-based "Before you start" and doctor-driven setup in the user
  guide and `SKILL.md`; `references/security-overview.md` (one page for an IT
  reviewer); `references/first-install-test.md` (how to run and score a first
  install).
- Evals (`plugins/ai-cfo-lab/evals/`): seven setup decision points. The first
  run caught the skill nudging an operator toward one of two same-named people;
  `SKILL.md` now presents both neutrally.
- CI: the offline tests run on every pull request (`.github/workflows/tests.yml`).
- Hardened after code review: the doctor reads the roster being edited (not the
  generated CSVs), moves a pasted Admin key into `.secrets/`, reports "All set"
  whenever nothing fails (warnings are listed, not blocking), refuses
  `--fix-config` on an unreadable config instead of replacing it, and quotes every
  path it suggests. The roster matcher never separates two different people by
  who is active (same first and last name only), keeps existing seat types unless
  `--premium` is given, reads T/F and Y/N active columns, and finds roster
  columns by header. The job installer handles Enterprise (no org id, no browser
  stage) and quotes paths. New modules pass `mypy --disallow-untyped-defs`.

## v0.2.0 — Unreleased

A daily, shared view. The monthly workflow is unchanged; everything below is
optional and off until configured.

**Daily refresh into a Claude Dashboard** (`references/daily-refresh.md`):
- `build_dashboard_datasets.py` writes the dashboard's datasets (`dashboard/*.json`
  plus a manifest with each one's title, description, refresh schedule and, for
  Ramp data, the query behind it). `run_pipeline.py --datasets` limits which.
- `scripts/dashboard_page.html` is the dashboard page: overview tiles with a
  run-rate projection, spend by month and surface, API cost by day, and tabs for
  people or departments, model families, Claude Code, card charges and flags.
  Every figure is computed from the uploaded datasets in calcs readers can open.
- Two scheduled jobs, split by sensitivity: a cloud routine that refreshes only
  org-wide API cost from Ramp (holds no keys), and a Mac job (`launchd` +
  `claude -p`) that pulls the claude.ai spend export with a fixed script
  (`fetch_surface_b_browser.py`, no AI in the loop, through a dedicated Chrome
  profile signed in once), then runs card charges, the Claude Code report and
  publishing in a headless Claude session. Each job owns its own
  datasets. Both are proposed to the operator before anything is created.
- `dashboard_visibility` in `pipeline.json`: `"department"` (default) uploads no
  names or emails; `"person"` uploads per-person rows. Enforced before upload,
  since dashboard readers can download every dataset.

**New sources:**
- `fetch_surface_b_browser.py` — the Team-plan spend export, unattended: one
  fixed GET request through a dedicated browser profile, saved byte for byte,
  with `--login` for the one-time sign-in and an automatic catch-up of a
  half-captured previous month. Claude Code's safety checks refuse to let an
  unattended Claude session export per-person data from an Owner's claude.ai
  session, so this step deliberately has no AI in it.
- `fetch_claude_code.py` — the Admin API's Claude Code usage report, per person
  or API key, per day, per model, with estimated cost. It only sees the Admin
  key's Console organization; where the Team workspace is a separate
  organization it reports API-key usage only.
- `ingest_ramp.py` — parses Ramp answers Claude saved: API cost from Ramp's
  AI-spend connection (`api_cost_source: "ramp"`, an alternative to the Admin
  API) and Anthropic charges on company cards (`card_charges_source: "ramp"`,
  shown beside the totals, not in them). Each saved Ramp answer is checked
  against Ramp's own transaction count or total before anything is published.

**Hardened after code review** (each has a test in `refresh-robustness.test.js`):
- A failed export no longer leaves the previous file looking current: the last
  good export keeps its own coverage, the month is reported `stale` with the
  reason, and a month whose closing fetch failed is retried the next day.
- A dataset whose source failed this run is left out of the upload
  (`manifest.json` → `skipped`) instead of being republished with a fresh
  timestamp.
- A month first registered mid-month is refreshed once it ends, so its
  projection doesn't stay scaled up.
- A multi-month Ramp API-cost pull is filed under each row's own month, replacing
  that month's table, so months never mix or double count.
- Card charges require Ramp's `total_count`, and non-USD charges use Ramp's
  settled dollar `amount`.
- `api_cost_refreshed_by` ("mac" / "cloud") says which job owns API cost; the
  other neither imports nor flags it.
- One shared month-coverage rule (`periods.py`); the Claude Code fetch asks only
  for new days plus the two still settling (days with no usage are remembered);
  new modules are type-hinted and pass mypy.
- A manual export saved after a failed fetch counts as current; the export script
  records a failure even when it can't start (no network, locked profile).
- Saved Ramp answers are imported once (renamed `.imported.json`); a charge
  without an amount, or an API-cost bucket without a date, is rejected.
- A cloud routine that owns API cost publishes `api_status`, so its failures
  reach the dashboard banner.
- Dashboard datasets are built before the monthly reports, and the daily jobs
  skip those reports (`run_pipeline.py --no-reports`).

**Changed / fixed:**
- `run_pipeline.py` registers a period with no export yet (writes `meta.json`),
  so a missing month is flagged rather than absent.
- `fetch_surface_c.py` ends each month at the next month's first midnight
  (`ending_at` is exclusive); it previously dropped the month's final second.
- Tests: run them with `node --test scripts/__tests__/*.test.js` (Node 26 no
  longer accepts a bare directory). New `daily-dashboard.test.js` covers the
  Ramp importer, the Claude Code flattening and date window, both visibility
  modes, `--only`, period registration, and the page's own arithmetic.
- Fixtures: the partial month gains Claude Code usage and saved Ramp answers,
  generated with a separate seed so every existing fixture file is unchanged.

## v0.1.0 — 2026-07-23

Initial release in the `ai-cfo-lab` plugin. A generalized, org-agnostic tool for
turning an organization's Anthropic/Claude spend into person / department /
product / model visibility across the three-surface model (committed seats /
variable overage / API-platform cash). Any Claude for Work org can run it against
its own spend.

**What it does:**
- **Conversational first-run setup** (company, plan tier, seat prices, roster,
  org id) that scaffolds a local workspace from `config.example/` templates.
  `scaffold.py` also writes a workspace `.gitignore` (covering `.secrets/`,
  `raw/`, `workbooks/`, `artifacts/`, `config/`) so an operator who
  version-controls their workspace can't commit real spend data or keys.
- **Roster bootstrap** — the first spend export seeds a fill-in `config/roster.xlsx`
  (Excel, with a `standard`/`premium` dropdown; `roster.csv` fallback when openpyxl
  is absent). Complete it by editing the sheet or by pasting a roster into the chat
  for Claude to fill; `apply_roster.py` regenerates `org_chart.csv` + `seats.csv`
  from it every run, with per-seat dollars derived from `pipeline.json` `seat_rates`.
- **Secret handling (operator-placed, never chat).** The optional Admin API key is
  supplied via a scaffolded `PASTE_ADMIN_KEY_HERE.txt` drop file; `secure_key.py`
  moves it into `.secrets/anthropic_admin_key` (chmod 600, gitignored) and deletes
  the drop, so the key travels file → file and never enters chat, a command, or a
  log. Env var `ANTHROPIC_ADMIN_API_KEY` still works. (Cowork has no secrets store
  yet — Surface C is cleanest from a local/CLI session.)
- **User guide** — `USER_GUIDE.md` in the skill folder: a non-technical,
  step-by-step walkthrough (setup → monthly export → roster → optional API key →
  reading the three-surface dashboard) with a short troubleshooting FAQ.
- **Monthly pipeline** — pulls the three surfaces, rebuilds two `.xlsx`
  workbooks + `build_summary.json`, regenerates a self-contained interactive HTML
  dashboard (trend + forecast bar, department/person/product/model tabs, model-
  routing what-if, quick-win flags), and drafts (never sends) a summary.
- **Plan-tier aware:** Team plan uses a manual-first seat-overage export (with an
  optional, clearly-labeled unofficial in-page fetch); Enterprise uses the
  documented Analytics API.

**Config-driven (no hardcoded brand anywhere):**
- Company name drives the dashboard title/`<h1>` and workbook header
  (`pipeline.json` `company_name`).
- Model families (regex → `frontier|sonnet|haiku|other`, colors, labels, and the
  Sonnet-class reference cost/request) live in `config/models.json` — update as
  model lines evolve, no code change.
- Standard seat rate lives in `thresholds.json` (`standard_seat_rate_usd`);
  per-seat-type prices live in `pipeline.json` `seat_rates` (drive the
  roster → `seats.csv` dollar fill). The shipped `pipeline.json` template ships
  `org_id: null`.
- `ANTHROPIC_ADMIN_API_KEY` supports a `.secrets/anthropic_admin_key` file
  fallback (env still wins); the Enterprise fetcher uses
  `ANTHROPIC_ANALYTICS_API_KEY` / `.secrets/anthropic_analytics_key`.

**Runtime & tests:**
- `openpyxl` is optional: the summary, dashboard, and Slack draft build with the
  Python stdlib alone; the two `.xlsx` workbooks need `pip install openpyxl`.
- Tests are Node's built-in runner (`node --test`), no dependencies:
  `scripts/__tests__/pipeline.test.js` drives the offline core over the fixtures
  (happy path + missing-export failure path + artifact-embed assertions);
  `scripts/__tests__/data-hygiene.test.js` is the PII/branding gate over
  `fixtures/` + `config.example/`, closing the gap that `.csv` files slip past
  most content scanners; `scripts/__tests__/roster.test.js` covers the
  bootstrap → apply roster flow (rate derivation, department mapping, the
  no-overwrite guard, and the no-op path when no roster is present);
  `scripts/__tests__/secure_key.test.js` covers the key drop-file ingest (extract →
  `.secrets/` at 600 → drop deleted, plus the no-op and no-key-found paths).

**Fixtures:** `fixtures/make_fixtures.py` (seeded) generates a synthetic
3-month, ~20-user `@example.com` dataset engineered to exercise every flag and
panel (concentration, a partial month, a zero-usage seat, a departed user,
frontier-heavy chatters, a product spike, an unowned API key).

**Roadmap:** non-Anthropic vendor surfaces (OpenAI/ChatGPT); live Enterprise-org
validation of `fetch_surface_b_enterprise.py` (currently built from docs, untested
against a live org).
