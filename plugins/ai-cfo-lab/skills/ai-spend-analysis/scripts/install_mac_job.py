#!/usr/bin/env python3
"""Install (or preview) the daily Mac job that refreshes the AI spend dashboard.

Usage: python3 install_mac_job.py <workspace root> [--hour 7] [--minute 15] [--load]

Without --load it prints the three files it would install and changes nothing,
so the operator can approve exactly what will run. With --load it writes them,
registers the job with launchd, and records its label in config/pipeline.json.

The job runs in two stages (references/daily-refresh.md → The Mac job):
  1. fetch_surface_b_browser.py — the spend export, a fixed script with no AI;
  2. a headless Claude run, limited to the tools listed below, that saves Ramp
     answers, runs the pipeline and publishes to the dashboard.

Commands are generated rather than typed because they're easy to get subtly
wrong (a space-separated --allowedTools list swallows the prompt). Whether the
job also refreshes API cost follows `api_cost_refreshed_by` in pipeline.json:
"mac" (the default) or "cloud" when a scheduled cloud routine owns it.
"""
import argparse, json, os, plistlib, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", (text or "workspace").lower()).strip("-") or "workspace"


def datasets(cfg, mac_owns_api_cost):
    ids = ["periods", "seats", "overage", "claude_code", "flags", "status"]
    if cfg.get("card_charges_source") == "ramp":
        ids.insert(4, "card_charges")
    if mac_owns_api_cost:
        ids.insert(3, "api_cost")
    return ids


def allowed_tools(cfg, mac_owns_api_cost):
    tools = ["Bash(python3:*)", "Bash(date:*)", "Read", "Write", "ToolSearch", "Artifact", "ArtifactData"]
    if cfg.get("card_charges_source") == "ramp":
        tools.append("mcp__claude_ai_Ramp__ramp_get_transactions")
    if mac_owns_api_cost and cfg.get("api_cost_source") == "ramp":
        tools.append("mcp__claude_ai_Ramp__ramp_get_ai_token_spend_aggregates")
    return tools


def prompt_text(root, cfg, mac_owns_api_cost):
    runbook = os.path.join(SKILL, "references", "daily-refresh.md")
    steps = [
        f"Read every {root}/raw/*/meta.json written today by the export script. Each period it touched "
        "(normally one; two when it finished last month first) gets the steps below, oldest first. "
        "START is the period's first day; END is its `end`.",
    ]
    if cfg.get("card_charges_source") == "ramp":
        steps.append("Card charges: call ramp_get_transactions (all_transactions_across_entire_business, merchant "
                     "filter Anthropic, from_date START, to_date END, page_size 200), following next_page_cursor. "
                     f"Save the pages to {root}/raw/PERIOD/ramp_card_transactions.json as described under "
                     "\"Saved Ramp answers\" in the runbook.")
    if mac_owns_api_cost and cfg.get("api_cost_source") == "ramp":
        steps.append("API cost: call ramp_get_ai_token_spend_aggregates (metric cost, providers [ANTHROPIC], "
                     "group_by [model], rollup daily, start_at START, end_at the day after END), then the same with "
                     f"rollup all. Save them to {root}/raw/PERIOD/ramp_api_cost.json and ramp_api_cost_total.json as "
                     "described under \"Saved Ramp answers\".")
    steps.append(f"Run: python3 {HERE}/run_pipeline.py {root} PERIOD --datasets {','.join(datasets(cfg, mac_owns_api_cost))}")
    steps.append(f"Publish what {root}/dashboard/manifest.json lists to {cfg.get('dashboard_url')}, following "
                 "\"Publishing datasets\" in the runbook, with job name \"Daily Mac refresh\".")
    steps.append(f"Reply with one line per dataset (published, or failed and why) and each source's state from "
                 f"{root}/dashboard/status.json. Nothing else; it goes to the log.")
    numbered = "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1))
    return (f"Daily refresh of the {cfg.get('company_name') or 'AI'} spend dashboard. Nobody is watching. Runbook: "
            f"{runbook}. Follow these steps exactly, then stop. Never retry a failed step. Do not open a browser or "
            f"visit claude.ai: the spend export was already fetched by script.\n\n{numbered}\n")


def script_text(root, claude, uv, tools):
    return f"""#!/bin/zsh -l
# Daily AI spend refresh (written by install_mac_job.py; re-run it to change this file).
# Stage 1 is a fixed script with no AI; stage 2 a headless Claude run limited to the listed tools.
cd "{root}" || exit 1
echo "=== $(date) ==="
"{uv}" run --with playwright python "{HERE}/fetch_surface_b_browser.py" "{root}"
"{claude}" -p --permission-mode dontAsk --allowedTools "{','.join(tools)}" < "{root}/daily_prompt.txt"
"""


def plist_data(label, root, hour, minute):
    log = os.path.join(root, "logs", "daily.log")
    return {"Label": label, "ProgramArguments": [os.path.join(root, "daily_refresh.sh")],
            "StartCalendarInterval": {"Hour": hour, "Minute": minute},
            "StandardOutPath": log, "StandardErrorPath": log}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    parser.add_argument("--hour", type=int, default=7)
    parser.add_argument("--minute", type=int, default=15)
    parser.add_argument("--load", action="store_true", help="write the files and register the job with launchd")
    args = parser.parse_args()
    root = os.path.abspath(os.path.expanduser(args.root))
    if sys.platform != "darwin":
        print("The daily Mac job uses macOS launchd. On other systems, schedule daily_refresh.sh with cron.")
        return 1
    cfg_path = os.path.join(root, "config", "pipeline.json")
    cfg = json.load(open(cfg_path))
    missing = [k for k in ("company_name", "dashboard_url", "org_id") if not cfg.get(k)]
    claude, uv = shutil.which("claude"), shutil.which("uv")
    if missing or not claude or not uv:
        problems = [f"{k} not set in config/pipeline.json" for k in missing]
        problems += [f"{name} not found on PATH" for name, path in (("claude", claude), ("uv", uv)) if not path]
        print("Not ready to install:\n  " + "\n  ".join(problems) + "\nRun doctor.py to see each fix.")
        return 1

    mac_owns_api_cost = cfg.get("api_cost_refreshed_by", "mac") == "mac"
    tools = allowed_tools(cfg, mac_owns_api_cost)
    label = f"com.aispend.{slug(cfg.get('company_name'))}"
    plist_path = os.path.expanduser(f"~/Library/LaunchAgents/{label}.plist")
    files = {
        os.path.join(root, "daily_refresh.sh"): script_text(root, claude, uv, tools),
        os.path.join(root, "daily_prompt.txt"): prompt_text(root, cfg, mac_owns_api_cost),
        plist_path: plistlib.dumps(plist_data(label, root, args.hour, args.minute)).decode(),
    }

    if not args.load:
        for path, text in files.items():
            print(f"──── {path}\n{text}")
        print(f"Runs daily at {args.hour:02d}:{args.minute:02d} (and on wake, if the Mac was asleep then).")
        print("Nothing installed. Re-run with --load to install exactly the above.")
        return 0

    os.makedirs(os.path.join(root, "logs"), exist_ok=True)
    os.makedirs(os.path.dirname(plist_path), exist_ok=True)
    for path, text in files.items():
        with open(path, "w") as fh:
            fh.write(text)
    os.chmod(os.path.join(root, "daily_refresh.sh"), 0o755)
    domain = f"gui/{os.getuid()}"
    subprocess.run(["launchctl", "bootout", f"{domain}/{label}"], capture_output=True)
    result = subprocess.run(["launchctl", "bootstrap", domain, plist_path], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"launchd refused the job: {result.stderr.strip()}")
        return 1
    cfg["mac_job_label"] = label
    open(cfg_path, "w").write(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    print(f"Installed {label}: daily at {args.hour:02d}:{args.minute:02d}. Log: {root}/logs/daily.log")
    print(f"Run it now to test: launchctl kickstart {domain}/{label}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
