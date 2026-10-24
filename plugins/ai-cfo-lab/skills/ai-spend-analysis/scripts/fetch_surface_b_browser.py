#!/usr/bin/env python3
"""Surface B for TEAM plans, unattended: the claude.ai spend export, fetched by a
fixed script (no AI in the loop) through a dedicated browser profile.

Usage:
  uv run --with playwright python fetch_surface_b_browser.py <workspace root> --login
      One-time (and whenever the login expires): opens Chrome on a profile kept in
      <root>/.browser-profile so an Owner or Primary Owner can sign in to claude.ai.
  uv run --with playwright python fetch_surface_b_browser.py <workspace root> --check
      Tests the saved login with the same request, saving nothing (doctor.py uses it).
  uv run --with playwright python fetch_surface_b_browser.py <workspace root> [YYYY-MM]
      Daily: fetches the export through yesterday for the month that contains
      yesterday (or the month given), first finishing the previous month if its
      last fetch was partial. Writes raw/<period>/overage_spend.csv + meta.json.

Why a fixed script: Team plans have no spend API, and Claude Code's safety checks
(rightly) refuse to let an unattended Claude session drive an Owner's claude.ai
session to export per-person data. This script makes exactly one kind of request
— the GET behind the Export spend report button — and saves the bytes as
received, so nothing is retyped and nothing else on claude.ai can be touched.

The endpoint is UNDOCUMENTED and can change. Every failure is written to the
period's meta.json as `fetch_error` (signed out, HTTP status, wrong content), and
validate_surface_b.py surfaces it on the dashboard. The manual export button is
always the fallback. Reads org_id and surface_b_endpoint from config/pipeline.json.
"""
import argparse, datetime, json, os, sys
from calendar import monthrange

PROFILE_DIR = ".browser-profile"
CLAUDE_URL = "https://claude.ai"
REQUIRED_COLUMNS = ("user_email", "total_net_spend_usd")


def export_window(period, today):
    """(start, end, partial) for a period, ending yesterday — every source is a day behind."""
    year, month = map(int, period.split("-"))
    start = datetime.date(year, month, 1)
    last = datetime.date(year, month, monthrange(year, month)[1])
    end = min(last, today - datetime.timedelta(days=1))
    if end < start:
        return None
    return start, end, end < last


def target_periods(root, today, period=None):
    """The month that contains yesterday, preceded by last month when its last fetch
    was partial (the Mac was off on the 1st) so no month is left half-captured."""
    if period:
        return [period]
    current = (today - datetime.timedelta(days=1)).strftime("%Y-%m")
    year, month = map(int, current.split("-"))
    previous = f"{year - 1}-12" if month == 1 else f"{year}-{month - 1:02d}"
    meta_path = os.path.join(root, "raw", previous, "meta.json")
    previous_partial = os.path.exists(meta_path) and json.load(open(meta_path)).get("partial")
    return [previous, current] if previous_partial else [current]


def looks_like_export(text):
    first_line = text.split("\n", 1)[0]
    return all(column in first_line for column in REQUIRED_COLUMNS)


def write_meta(root, period, window, source, fetch_error=None):
    out_dir = os.path.join(root, "raw", period)
    os.makedirs(out_dir, exist_ok=True)
    start, end, partial = window
    meta = {"period": period, "start": start.isoformat(), "end": end.isoformat(),
            "days_covered": end.day, "partial": partial, "source": source}
    if fetch_error:
        meta["fetch_error"] = fetch_error
    with open(os.path.join(out_dir, "meta.json"), "w") as fh:
        json.dump(meta, fh, indent=2)


def open_profile(playwright, root, headless):
    return playwright.chromium.launch_persistent_context(
        os.path.join(root, PROFILE_DIR), channel="chrome", headless=headless, accept_downloads=False)


def login(root):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        context = open_profile(p, root, headless=False)
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(f"{CLAUDE_URL}/login")
        print("Sign in to claude.ai as an Owner or Primary Owner in the window that opened,")
        print("then close that window. The login is kept in .browser-profile for the daily fetch.")
        page.wait_for_event("close", timeout=0)
        context.close()
    return 0


def request_export(context, cfg, start, end):
    """The one request this script makes. Returns (response, error message or None)."""
    url = CLAUDE_URL + cfg["surface_b_endpoint"].format(org_id=cfg["org_id"], start=start.isoformat(), end=end.isoformat())
    response = context.request.get(url)
    if response.status in (401, 403):
        return response, "claude.ai session signed out — run fetch_surface_b_browser.py --login"
    if not response.ok:
        return response, f"HTTP {response.status} from the spend export (endpoint may have changed)"
    if not looks_like_export(response.text()):
        return response, (f"response was not the spend export (content type "
                          f"{response.headers.get('content-type', 'unknown')}) — signed out or endpoint changed")
    return response, None


def load_config(root):
    cfg = json.load(open(os.path.join(root, "config", "pipeline.json")))
    if not cfg.get("org_id") or not cfg.get("surface_b_endpoint"):
        print("[surface_b_browser] org_id and surface_b_endpoint must be set in config/pipeline.json")
        return None
    if not os.path.isdir(os.path.join(root, PROFILE_DIR)):
        print("[surface_b_browser] no browser profile yet — run once with --login")
        return None
    return cfg


def check(root, today):
    cfg = load_config(root)
    if not cfg:
        return 1
    yesterday = today - datetime.timedelta(days=1)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        context = open_profile(p, root, headless=True)
        try:
            _, error = request_export(context, cfg, yesterday, yesterday)
        finally:
            context.close()
    print(f"[surface_b_browser] {error}" if error else "[surface_b_browser] signed in; the export answers")
    return 1 if error else 0


def fetch(root, periods, today):
    cfg = load_config(root)
    if not cfg:
        return 1

    from playwright.sync_api import sync_playwright
    stamp = today.isoformat()
    with sync_playwright() as p:
        context = open_profile(p, root, headless=True)
        try:
            for period in periods:
                window = export_window(period, today)
                if not window:
                    continue
                start, end, _ = window
                response, error = request_export(context, cfg, start, end)
                if error:
                    write_meta(root, period, window, f"daily browser export {stamp} (failed)", error)
                    print(f"[surface_b_browser] {period}: {error}")
                    continue
                os.makedirs(os.path.join(root, "raw", period), exist_ok=True)
                with open(os.path.join(root, "raw", period, "overage_spend.csv"), "wb") as fh:
                    fh.write(response.body())
                write_meta(root, period, window, f"daily browser export {stamp}")
                print(f"[surface_b_browser] {period}: saved export {start}..{end} "
                      f"({response.text().count(chr(10))} lines)")
        finally:
            context.close()
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    parser.add_argument("period", nargs="?", help="YYYY-MM (default: the month containing yesterday)")
    parser.add_argument("--login", action="store_true", help="open Chrome to sign in to claude.ai once")
    parser.add_argument("--check", action="store_true", help="test the saved login without saving anything")
    args = parser.parse_args()
    if args.login:
        return login(args.root)
    today = datetime.date.today()
    if args.check:
        return check(args.root, today)
    return fetch(args.root, target_periods(args.root, today, args.period), today)


if __name__ == "__main__":
    sys.exit(main())
