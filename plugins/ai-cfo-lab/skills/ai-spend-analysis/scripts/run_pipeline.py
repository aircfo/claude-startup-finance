#!/usr/bin/env python3
"""Orchestrate the scriptable pipeline steps.

Usage: run_pipeline.py <workspace root> <YYYY-MM> [--datasets id,id,...]

Order:
  - Register the period (write raw/<period>/meta.json if nothing has yet), so a
    month with no export still shows up — flagged — instead of vanishing.
  - Ramp (config `api_cost_source` / `card_charges_source` = "ramp"): parse the
    Ramp answers Claude saved into raw/<period>/ (ingest_ramp.py).
  - plan_tier == "enterprise": fetch Surface B via the documented Analytics API
    (fetch_surface_b_enterprise.py) — fully scripted, no browser.
  - plan_tier == "team" (default): Surface B (the seat-overage export) is NOT
    fetched here. The operator — or the daily browser step in
    references/daily-refresh.md — drops it at raw/<period>/overage_spend.csv first.
  Then, for both tiers: Surface C via the Admin API (skipped when Ramp supplies
  API cost) -> Claude Code usage report -> validate Surface B -> (apply roster if
  a config/roster.xlsx|csv is present) -> workbooks -> artifact -> Slack draft ->
  dashboard datasets (--datasets limits which are written).

Never sends anything; read-only against every financial surface."""
import argparse, datetime, json, os, subprocess, sys
from calendar import monthrange

HERE = os.path.dirname(os.path.abspath(__file__))


def run(script, *args):
    r = subprocess.run([sys.executable, os.path.join(HERE, script), *args], capture_output=True, text=True)
    if r.stdout.strip():
        print(r.stdout.strip())
    if r.stderr.strip():
        print(r.stderr.strip()[:2000], file=sys.stderr)
    return r.returncode


def pipeline_config(root):
    path = os.path.join(root, "config", "pipeline.json")
    return json.load(open(path)) if os.path.exists(path) else {}


def register_period(outdir, period, today):
    """Write meta.json for a period that has none. The current month counts through
    yesterday, because every source is a day behind."""
    meta_path = os.path.join(outdir, "meta.json")
    if os.path.exists(meta_path):
        return
    year, month = map(int, period.split("-"))
    days_in_month = monthrange(year, month)[1]
    current = today.strftime("%Y-%m")
    if period == current:
        days_covered, partial = max(today.day - 1, 0), True
    else:
        days_covered, partial = (days_in_month, False) if period < current else (0, True)
    with open(meta_path, "w") as fh:
        json.dump({"period": period, "days_covered": days_covered, "partial": partial,
                   "source": "registered by run_pipeline (no export meta yet)"}, fh, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    parser.add_argument("period")
    parser.add_argument("--datasets", default="", help="comma-separated dashboard dataset ids (default: all)")
    args = parser.parse_args()
    root, period = args.root, args.period
    cfg = pipeline_config(root)
    outdir = os.path.join(root, "raw", period)
    os.makedirs(outdir, exist_ok=True)
    register_period(outdir, period, datetime.date.today())
    run("secure_key.py", root)  # ingest a dropped PASTE_ADMIN_KEY_HERE.txt into .secrets/ (no-op if none)
    if "ramp" in (cfg.get("api_cost_source"), cfg.get("card_charges_source")):
        run("ingest_ramp.py", root, period)
    if (cfg.get("plan_tier") or "team").lower() == "enterprise":
        run("fetch_surface_b_enterprise.py", root, period)  # writes overage_spend.csv (scripted path)
    if cfg.get("api_cost_source", "admin_api") == "admin_api":
        run("fetch_surface_c.py", root, period)
    run("fetch_claude_code.py", root, period)  # graceful not_configured without an Admin key
    run("validate_surface_b.py", os.path.join(outdir, "overage_spend.csv"), period)  # fail-loud is via the status file
    cfg_dir = os.path.join(root, "config")
    if os.path.exists(os.path.join(cfg_dir, "roster.xlsx")) or os.path.exists(os.path.join(cfg_dir, "roster.csv")):
        run("apply_roster.py", root)  # roster is the source of truth when present; regenerates org_chart.csv + seats.csv
    if run("build_workbooks.py", root):
        return 1
    if run("build_artifact.py", root):
        return 1
    run("draft_slack.py", root)
    dataset_args = ["--only", args.datasets] if args.datasets else []
    if run("build_dashboard_datasets.py", root, *dataset_args):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
