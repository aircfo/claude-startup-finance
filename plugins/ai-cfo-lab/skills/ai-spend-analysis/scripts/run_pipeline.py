#!/usr/bin/env python3
"""Orchestrate the scriptable pipeline steps.

Usage: run_pipeline.py <workspace root> <YYYY-MM>

Order:
  - plan_tier == "enterprise": fetch Surface B via the documented Analytics API
    (fetch_surface_b_enterprise.py) — fully scripted, no browser.
  - plan_tier == "team" (default): Surface B (the seat-overage export) is NOT
    fetched here. On Team, the operator drops the manual/browser export into
    raw/<period>/overage_spend.csv per SKILL.md Step 1 before running this.
  Then, for both tiers: Surface C pull -> validate Surface B -> workbooks ->
  artifact -> Slack draft.

Never sends anything; read-only against every financial surface."""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def run(script, *args):
    r = subprocess.run([sys.executable, os.path.join(HERE, script), *args], capture_output=True, text=True)
    if r.stdout.strip():
        print(r.stdout.strip())
    if r.stderr.strip():
        print(r.stderr.strip()[:2000], file=sys.stderr)
    return r.returncode


def plan_tier(root):
    path = os.path.join(root, "config", "pipeline.json")
    if not os.path.exists(path):
        return "team"
    return (json.load(open(path)).get("plan_tier") or "team").lower()


def main():
    root, period = sys.argv[1], sys.argv[2]
    outdir = os.path.join(root, "raw", period)
    os.makedirs(outdir, exist_ok=True)
    if plan_tier(root) == "enterprise":
        run("fetch_surface_b_enterprise.py", root, period)  # writes overage_spend.csv (scripted path)
    run("fetch_surface_c.py", root, period)
    run("validate_surface_b.py", os.path.join(outdir, "overage_spend.csv"), period)  # fail-loud is via the status file
    if run("build_workbooks.py", root):
        return 1
    if run("build_artifact.py", root):
        return 1
    run("draft_slack.py", root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
