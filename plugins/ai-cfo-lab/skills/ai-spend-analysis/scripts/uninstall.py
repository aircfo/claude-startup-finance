#!/usr/bin/env python3
"""Undo the AI spend setup on this machine, step by step.

Usage: python3 uninstall.py <workspace root> [--remove-login] [--remove-key] [--purge-data] [--yes]

Without --yes it lists what it would remove and changes nothing. By default it
removes only the scheduled Mac job. Each flag adds one thing:
  --remove-login  the export's signed-in browser profile (.browser-profile/)
  --remove-key    the stored Admin API key (.secrets/anthropic_admin_key);
                  also revoke it in platform.claude.com, since a copy may exist
  --purge-data    raw exports, workbooks, artifacts and dashboard uploads (the
                  per-person spend history); config and the roster stay

It never touches the claude.ai dashboard or a cloud routine — those live in the
operator's account: delete the dashboard from its menu on claude.ai and any
routine at claude.ai/code/routines.
"""
import argparse, json, os, shutil, subprocess, sys

DATA_DIRS = ("raw", "workbooks", "artifacts", "dashboard")


def plan(root, cfg, args):
    steps = []
    label = cfg.get("mac_job_label")
    if label:
        steps.append(("Scheduled Mac job " + label, ("job", label)))
    for name in ("daily_refresh.sh", "daily_prompt.txt"):
        if os.path.exists(os.path.join(root, name)):
            steps.append((name, ("file", os.path.join(root, name))))
    if args.remove_login and os.path.isdir(os.path.join(root, ".browser-profile")):
        steps.append(("Signed-in export browser profile", ("dir", os.path.join(root, ".browser-profile"))))
    if args.remove_key and os.path.exists(os.path.join(root, ".secrets", "anthropic_admin_key")):
        steps.append(("Stored Admin API key", ("file", os.path.join(root, ".secrets", "anthropic_admin_key"))))
    if args.purge_data:
        steps += [(f"{d}/ (spend data)", ("dir", os.path.join(root, d)))
                  for d in DATA_DIRS if os.path.isdir(os.path.join(root, d))]
    return steps


def remove(cfg_path, cfg, kind, target):
    if kind == "job":
        subprocess.run(["launchctl", "bootout", f"gui/{os.getuid()}/{target}"], capture_output=True)
        plist = os.path.expanduser(f"~/Library/LaunchAgents/{target}.plist")
        if os.path.exists(plist):
            os.remove(plist)
        cfg.pop("mac_job_label", None)
        open(cfg_path, "w").write(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    elif kind == "file":
        os.remove(target)
    else:
        shutil.rmtree(target)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    parser.add_argument("--remove-login", action="store_true")
    parser.add_argument("--remove-key", action="store_true")
    parser.add_argument("--purge-data", action="store_true")
    parser.add_argument("--yes", action="store_true", help="actually remove; without it, only list")
    args = parser.parse_args()
    root = os.path.abspath(os.path.expanduser(args.root))
    cfg_path = os.path.join(root, "config", "pipeline.json")
    cfg = json.load(open(cfg_path)) if os.path.exists(cfg_path) else {}
    steps = plan(root, cfg, args)
    if not steps:
        print("Nothing to remove.")
    for title, (kind, target) in steps:
        if args.yes:
            remove(cfg_path, cfg, kind, target)
            print(f"Removed: {title}")
        else:
            print(f"Would remove: {title}")
    if not args.yes and steps:
        print("Nothing removed. Re-run with --yes to remove the above.")
    if args.remove_key:
        print("Also revoke the key in platform.claude.com → Settings → Admin keys.")
    print("Not touched: the claude.ai dashboard and any cloud routine (delete those on claude.ai).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
