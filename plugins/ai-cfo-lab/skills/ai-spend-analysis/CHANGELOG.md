# Changelog — ai-spend-analysis

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
- Standard seat rate lives in `thresholds.json` (`standard_seat_rate_usd`); the
  shipped `pipeline.json` template ships `org_id: null`.
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
  most content scanners.

**Fixtures:** `fixtures/make_fixtures.py` (seeded) generates a synthetic
3-month, ~20-user `@example.com` dataset engineered to exercise every flag and
panel (concentration, a partial month, a zero-usage seat, a departed user,
frontier-heavy chatters, a product spike, an unowned API key).

**Roadmap:** non-Anthropic vendor surfaces (OpenAI/ChatGPT); live Enterprise-org
validation of `fetch_surface_b_enterprise.py` (currently built from docs, untested
against a live org).
