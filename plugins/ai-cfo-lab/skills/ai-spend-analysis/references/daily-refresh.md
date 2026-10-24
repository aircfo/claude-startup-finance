# Daily refresh into a Claude Dashboard

The runbook for keeping a shared Claude Dashboard current every day. `SKILL.md`
says when to use it; this file is the procedure. Read it in full before setting
up a refresh or before running one as a scheduled job.

Throughout: `$SKILL` is this skill's folder, `$ROOT` the workspace, `<dashboard>`
the dashboard's claude.ai link (stored in `config/pipeline.json` as
`dashboard_url`).

## What refreshes where

Two scheduled jobs share one dashboard. Each owns different datasets, so they
never overwrite each other, and the split keeps per-person data and keys off
the cloud.

| Dataset | What it is | Refreshed by | Needs |
|---|---|---|---|
| `api_cost` | API (Console) cost per day and model | **Cloud job**, daily | Ramp connector (`api_cost_source: "ramp"`) — no key, no people |
| `overage` | Per-person seat overage from the claude.ai spend export | **Mac job**, daily | A Chrome profile signed into claude.ai as an Owner (fixed script, no AI) |
| `claude_code` | Claude Code usage and estimated cost, per person or API key | Mac job, daily | Admin key in `$ROOT/.secrets/` (see the note below) |
| `card_charges` | Anthropic charges on employee cards | Mac job, daily | Ramp connector (`card_charges_source: "ramp"`) |
| `seats`, `periods`, `flags`, `status` | Roster cost, month coverage, flags, source health | Mac job, daily | The workspace |
| `api_status` | Whether API cost refreshed cleanly | Cloud job, with `api_cost` | — (only when a cloud routine owns API cost) |

**What the Claude Code report can see.** The Admin key belongs to a Console
(developer-platform) organization, and the report covers Claude Code usage in
*that* organization. Where a company's claude.ai Team workspace is a separate
organization — common when the API account was opened on its own — the report
shows only Claude Code run on API keys, with no Team-seat users at all. Probe
once before relying on it: if every row's `customer_type` is `api`, the
per-person view comes from the spend export alone.

Every source is a day behind (the spend export and the reports refresh
overnight), so a daily run covers **through yesterday**. The **target period**
is the month that contains yesterday. That one rule also closes out each month:
the run on the 1st pulls the full previous month, and the run on the 2nd moves
on.

If the Mac is off, the Mac-owned sections go stale on the page (each dataset
says how old it is, and shows as stale after 48 hours) while the cloud-owned
API cost keeps refreshing. Nothing is silently zeroed.

Orgs without the cloud job let the Mac job own `api_cost` too
(`api_cost_refreshed_by: "mac"`, the default); with a cloud job, set it to
`"cloud"` so the Mac job neither saves nor reports API cost. Orgs on Enterprise can move everything to the
cloud: the Analytics API replaces the export script.

## One-time setup

1. **Create the dashboard.** Publish from the Dashboard Artifact type with the
   title "<company> AI spend". Then, in one `ArtifactData` batch on it:
   - `dash/meta` = `{"title": "<company> AI spend"}`
   - `files/index.html` = `{"text": <the contents of $SKILL/scripts/dashboard_page.html>}`
2. **Record it** in `$ROOT/config/pipeline.json`: `dashboard_url`, and
   `dashboard_visibility` — `"department"` (the default; no names leave the
   workspace) or `"person"` (only if the organization has decided everyone with
   the link may see each person's spend). Set `api_cost_source` and
   `card_charges_source` to `"ramp"` when Ramp's AI-spend connection holds the
   Anthropic admin key and Anthropic charges go through Ramp cards.
3. **First full run** from an interactive session: run the Mac job's steps
   below once (the export step will prompt for Chrome) and publish every
   dataset, `api_cost` included. Then do the dashboard type's own check (read
   `data/users/me` doc `check` until it settles).
4. **Share it.** The dashboard is private until the owner shares it from its
   Share menu; the assistant cannot change sharing. Anyone it is shared with
   can download every dataset's rows from Sources.
5. **Schedule the two jobs** (below). Both are proposals for the operator to
   approve: show the full routine body and the launchd file before creating
   either.

## Publishing datasets (both jobs)

After `run_pipeline.py` (or `build_dashboard_datasets.py`) writes
`$ROOT/dashboard/`, publish what `dashboard/manifest.json` lists under
`datasets` — and only that. Datasets under `skipped` failed at their source
this run (the reason is beside each); leave them as they are on the dashboard,
which then shows their true age, and mention them in the job's reply. For each `datasets.<id>` entry:

1. Upload the file: `Artifact` publish with `url` = `<dashboard>`,
   `file_path` = `$ROOT/dashboard/<file>`, `asset: true`. Keep the returned
   `/_blob/<asset id>` url.
2. Read the current `datasets/<id>` document with `ArtifactData` get (note its
   `version` and its old `source.url`, if any).
3. Write the document — `set` when it doesn't exist yet, otherwise `update`
   with `if_version` — with:
   - `title`, `description`, `schedule` — from the manifest entry
   - `staleAfterHours` — the manifest's `stale_after_hours`
   - `source` = `{"kind": "file", "url": "/_blob/<asset id>", "name": "<file>"}`
   - `updated` = `{"at": <now, ISO UTC>, "by": "<job name>"}`
   - `request` — only when the manifest entry has one (the Ramp call behind
     the file, kept so an editor can see the query)
   - `lastAttempt` = `{"at": <now>, "ok": true, "by": "<owner's name>"}` when it
     has a `request`
4. Delete the asset the old `source.url` pointed at (`Artifact` delete with
   `url` = `<dashboard>` and `path` = its 32-character id), so daily uploads
   don't pile up. Delete only that one asset, and only after step 3 succeeded.

**Saved Ramp answers are checked before anything is published.** A model writes
each answer to disk, so a dropped page or a mistyped figure is possible; the
import compares the card pages with Ramp's `total_count` and each model's daily
API cost with Ramp's own total, and marks the source `error` (publishing nothing
new for it) on any mismatch. Ramp's answers are mostly empty fields, so save
only the ones the import reads — for API cost `period_start_at`, `model`,
`total_cost` (under `cost.data`); for transactions `spent_by_user`, `amount`,
`original_amount`, `original_currency`, `state`, `transaction_time`,
`spend_allocation_name`, and each page's `total_count` — copied exactly. Never
round, reformat or summarize. A page set without `total_count`, a charge
without its amount, or a non-USD charge without its dollar `amount`, is
rejected. Each saved answer is imported once and then renamed
`<name>.imported.json`, so it has to be saved fresh every run.

If an upload or write fails, leave that dataset as it was — the page keeps the
last good file and its age shows — and say which one failed in the job's final
reply. Never retry a failed write in the same run.

## The cloud job (scheduled routine, daily)

Holds no keys and touches no per-person data. Create it with the schedule
skill: daily at a fixed hour, the Ramp connector attached, and this repo (or
the operator's copy of the skill) as its source. Allowed tools: `Bash`,
`Read`, `Write`, `ToolSearch`, `Artifact`, `ArtifactData`, and the Ramp tool
`ramp_get_ai_token_spend_aggregates`. Prompt template (fill the `<…>`):

```text
Scheduled daily refresh of the API cost on an AI spend dashboard. Nobody is
watching. Follow these steps exactly, then stop. Never retry a failed step,
and never create, change or delete a routine.

Dashboard: <dashboard>
Skill folder in this checkout: <path to ai-spend-analysis>
Company: <company>

1. Run: date -u +%Y-%m-%d. Yesterday's month is PERIOD (YYYY-MM). START is the
   first day of the month <history months, e.g. 5> months before PERIOD. END is
   today's date (exclusive, so data runs through yesterday).
2. Run: python3 <skill>/scripts/scaffold.py /tmp/ws ; then set
   /tmp/ws/config/pipeline.json keys company_name="<company>",
   api_cost_source="ramp", dashboard_url="<dashboard>".
3. Load the Ramp tool ramp_get_ai_token_spend_aggregates with ToolSearch and
   call it once: metric "cost", providers ["ANTHROPIC"], group_by ["model"],
   rollup "daily", start_at START, end_at END. Save its `cost.data` buckets
   (`period_start_at`, `model`, `total_cost`, copied exactly) as
   {"cost": {"data": [...]}} to /tmp/ws/raw/PERIOD/ramp_api_cost.json. Then make the same call
   with rollup "all" and save its `model` and `total_cost` the same way to
   /tmp/ws/raw/PERIOD/ramp_api_cost_total.json
   (the import checks the daily rows add up to it). If either call fails, stop
   and report it.
4. Run: python3 <skill>/scripts/run_pipeline.py /tmp/ws PERIOD --datasets api_cost,api_status --no-reports
5. Publish the datasets in /tmp/ws/dashboard/manifest.json to the dashboard,
   following "Publishing datasets" in <skill>/references/daily-refresh.md, with
   job name "Daily cloud refresh".
6. Reply with what you published and anything that failed, and nothing else.
```

## The Mac job (local, daily)

Runs on the operator's Mac in two stages, started by macOS `launchd`:

1. **The spend export — a fixed script, no AI.** `fetch_surface_b_browser.py`
   opens a dedicated Chrome profile (kept in `$ROOT/.browser-profile`, signed
   into claude.ai once by an Owner or Primary Owner) and makes the one GET
   request behind the Export spend report button, saving the bytes as received.
2. **Everything else — a headless Claude run.** Card charges from Ramp, the
   pipeline (including the Claude Code report with the stored Admin key), and
   publishing to the dashboard.

Why the split: Team plans have no spend API, and Claude Code's safety checks
refuse to let an unattended Claude session drive an Owner's claude.ai session
to export per-person data — even with `--permission-mode dontAsk` and a narrow
tool list. That refusal is reasonable, so the export runs as plain code that can
only do that one read, and Claude never touches claude.ai.

**One-time login** (and again whenever the dashboard says the session signed
out):

```bash
cd $ROOT && uv run --with playwright python $SKILL/scripts/fetch_surface_b_browser.py $ROOT --login
```

A Chrome window opens on the claude.ai login page; sign in, then close it.

**`$ROOT/daily_refresh.sh`** (the job `launchd` runs):

```bash
#!/bin/zsh -l
# Daily AI spend refresh: stage 1 is a fixed script, stage 2 a headless Claude run.
set -u
ROOT="<$ROOT>"
SKILL="<$SKILL>"
cd "$ROOT"
echo "=== $(date) ==="
uv run --with playwright python "$SKILL/scripts/fetch_surface_b_browser.py" "$ROOT"
claude -p --permission-mode dontAsk \
  --allowedTools "Bash(python3:*),Read,Write,ToolSearch,Artifact,ArtifactData,mcp__claude_ai_Ramp__ramp_get_transactions" \
  < "$ROOT/daily_prompt.txt"
```

**`~/Library/LaunchAgents/com.<org>.ai-spend-refresh.plist`:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.<org>.ai-spend-refresh</string>
  <key>ProgramArguments</key><array><string><$ROOT>/daily_refresh.sh</string></array>
  <key>StartCalendarInterval</key><dict><key>Hour</key><integer>7</integer><key>Minute</key><integer>15</integer></dict>
  <key>StandardOutPath</key><string><$ROOT>/logs/daily.log</string>
  <key>StandardErrorPath</key><string><$ROOT>/logs/daily.log</string>
</dict></plist>
```

`launchd` runs a missed job when the Mac next wakes, so a laptop that was
asleep at 7:15 still refreshes that morning (a Mac that was shut down skips the
day; the fetch script's catch-up covers month ends). `--allowedTools` takes one
comma-separated list, and the prompt arrives on stdin.

**`$ROOT/daily_prompt.txt`:**

```text
Daily refresh of the AI spend dashboard. Nobody is watching. Follow
<skill>/references/daily-refresh.md, section "The Mac job", stage 2 steps 1–6,
for the workspace <$ROOT>, then stop. Never retry a failed step. Do not open a
browser or visit claude.ai: the spend export was already fetched by script.
```

Stage 2 steps:

1. **Period.** Read `$ROOT/raw/*/meta.json` written by stage 1 this morning:
   each period it touched (normally one; two when it finished last month
   first) gets steps 2–3, oldest first. START is the period's first day, END
   its `end` from meta.json.
2. **Card charges** (when `card_charges_source` is `"ramp"`). Call
   `ramp_get_transactions` with `transactions_to_retrieve`
   `"all_transactions_across_entire_business"`, merchant filter `Anthropic`,
   `from_date` START, `to_date` END, `page_size` 200; follow
   `next_page_cursor` until there is none. Save the pages as a list to
   `$ROOT/raw/PERIOD/ramp_card_transactions.json`, keeping the fields listed
   under "Saved Ramp answers" and each page's `total_count`: the import rejects
   the file if the pages don't hold exactly that many transactions.
3. **API cost** (only when this job owns it: `api_cost_refreshed_by` is
   `"mac"` and `api_cost_source` is `"ramp"`). Call
   `ramp_get_ai_token_spend_aggregates` with metric `cost`, providers
   `["ANTHROPIC"]`, group_by `["model"]`, rollup `daily`, start_at START, end_at
   the day after END; then the same with rollup `all`. Save them to
   `$ROOT/raw/PERIOD/ramp_api_cost.json` and `ramp_api_cost_total.json` as
   described under "Saved Ramp answers".
4. **Pipeline.** `python3 <skill>/scripts/run_pipeline.py $ROOT PERIOD
   --datasets periods,seats,overage,claude_code,card_charges,flags,status --no-reports`
   (leave out `card_charges` when it isn't configured; add `api_cost` when this
   job owns it).
5. **Publish** per "Publishing datasets", job name "Daily Mac refresh".
6. **Reply** with one line per dataset (published / failed and why) and the
   status of each source from `$ROOT/dashboard/status.json`. It goes to the
   log; never send it anywhere.

## The spend export script

Team plans have no API for the spend report, so `fetch_surface_b_browser.py`
reads it the way the Export button does: an authenticated GET from the Owner's
own claude.ai session, through the dedicated profile. **The endpoint is
undocumented** (`surface_b_endpoint` in `pipeline.json`) and can change without
notice. Containment:

- The script can make only that request; there is no code path that clicks,
  posts or changes anything.
- A response is saved only if it is HTTP 200 and its header row holds
  `user_email` and `total_net_spend_usd` — a login page or an error page never
  becomes the export.
- Every failure is written to the period's `meta.json` as `fetch_error` (signed
  out, HTTP status, wrong content), and the dashboard's banner shows it.
- The manual export (Settings → Analytics → "How much is Claude costing?" →
  Export spend report) always works as a fallback: save it to
  `raw/<period>/overage_spend.csv`.

The export sums each person's spend over the requested range, so a
month-to-date pull gives month-to-date per person; earlier months stay as they
were left on their final run.

## When something fails

| Symptom | What the page shows | Fix |
|---|---|---|
| Mac asleep or off for days | Mac-owned sections marked stale; API cost current | Next wake runs the missed job |
| claude.ai login expired | Banner: "claude.ai session signed out" | Run the fetch script with `--login` once; the next run recovers the whole month |
| Export endpoint changed | Banner: seat overage invalid or missing | Do a manual export for the month; rediscover the endpoint from the export button's network request and update `surface_b_endpoint` |
| Admin key revoked | Banner: Claude Code usage error | Drop a new key in `PASTE_ADMIN_KEY_HERE.txt` |
| Ramp call failed (cloud) | API cost stale | Check the routine's run log; Ramp's AI-spend connection may need re-validating |
| Ramp's API cost looks too low | Low API figures | Ramp's admin key must belong to the Console org the API traffic runs under; check the org id in Ramp's connection |

The 90-day export window matters less once the Mac job runs daily: each
month is captured in full on the 1st of the next month. A Mac that is off for
the whole first day of a month still has 89 more days to catch up with a
manual export.
