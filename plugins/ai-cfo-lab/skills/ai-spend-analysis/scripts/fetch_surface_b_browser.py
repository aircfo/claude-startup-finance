#!/usr/bin/env python3
"""Surface B for TEAM plans, unattended: the claude.ai spend export, fetched by a
fixed script (no AI in the loop) through a dedicated browser profile.

Usage:
  uv run --with playwright python fetch_surface_b_browser.py <workspace root> --login
      One-time (and whenever the login expires): opens Chrome on a profile kept in
      <root>/.browser-profile so an Owner or Primary Owner can sign in to claude.ai.
  uv run --with playwright python fetch_surface_b_browser.py <workspace root> [YYYY-MM]
      Daily: fetches the export through yesterday for the month that contains
      yesterday (or the month given), first finishing the previous month if its
      last fetch was partial or failed. Writes raw/<period>/overage_spend.csv +
      meta.json; a failed fetch keeps the last good export and records the error.

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
from __future__ import annotations

import argparse, datetime, json, os, sys
from typing import TYPE_CHECKING, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from periods import Coverage, coverage, month_of, previous_month, read_meta, record_fetch_error, write_meta

if TYPE_CHECKING:
    from playwright.sync_api import APIResponse, BrowserContext, Playwright

PROFILE_DIR = ".browser-profile"
CLAUDE_URL = "https://claude.ai"
REQUIRED_COLUMNS = ("user_email", "total_net_spend_usd")


def target_periods(root: str, today: datetime.date, period: Optional[str] = None) -> list[str]:
    """The month that contains yesterday, preceded by last month when its last fetch
    was partial (the Mac was off on the 1st) or failed (signed out at month end),
    so no month is left half-captured."""
    if period:
        return [period]
    current = month_of(today - datetime.timedelta(days=1))
    previous = previous_month(current)
    meta = read_meta(os.path.join(root, "raw", previous))
    unfinished = bool(meta) and (meta.get("partial") or meta.get("fetch_error"))
    return [previous, current] if unfinished else [current]


def looks_like_export(text: str) -> bool:
    first_line = text.split("\n", 1)[0]
    return all(column in first_line for column in REQUIRED_COLUMNS)


def open_profile(playwright: Playwright, root: str, headless: bool) -> BrowserContext:
    return playwright.chromium.launch_persistent_context(
        os.path.join(root, PROFILE_DIR), channel="chrome", headless=headless, accept_downloads=False)


def login(root: str) -> int:
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


def load_config(root: str) -> Optional[dict]:
    with open(os.path.join(root, "config", "pipeline.json")) as fh:
        cfg = json.load(fh)
    if not cfg.get("org_id") or not cfg.get("surface_b_endpoint"):
        print("[surface_b_browser] org_id and surface_b_endpoint must be set in config/pipeline.json")
        return None
    if not os.path.isdir(os.path.join(root, PROFILE_DIR)):
        print("[surface_b_browser] no browser profile yet — run once with --login")
        return None
    return cfg


def request_export(context: BrowserContext, cfg: dict, covered: Coverage) -> tuple[APIResponse, Optional[str]]:
    """The one request this script makes. Returns (response, error message or None)."""
    url = CLAUDE_URL + cfg["surface_b_endpoint"].format(
        org_id=cfg["org_id"], start=covered.start.isoformat(), end=covered.end.isoformat())
    response = context.request.get(url)
    if response.status in (401, 403):
        return response, "claude.ai session signed out — run fetch_surface_b_browser.py --login"
    if not response.ok:
        return response, f"HTTP {response.status} from the spend export (endpoint may have changed)"
    if not looks_like_export(response.text()):
        return response, (f"response was not the spend export (content type "
                          f"{response.headers.get('content-type', 'unknown')}) — signed out or endpoint changed")
    return response, None


def fetch(root: str, periods: list[str], today: datetime.date) -> int:
    cfg = load_config(root)
    if not cfg:
        return 1
    stamp = today.isoformat()
    pending = [p for p in periods if coverage(p, today)]
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            context = open_profile(p, root, headless=True)
            try:
                while pending:
                    period = pending[0]
                    fetch_period(context, cfg, root, period, today, stamp)
                    pending.pop(0)
            finally:
                context.close()
    except Exception as err:  # no network, a locked profile, Playwright missing: record it, don't vanish
        message = f"the export script couldn't run ({type(err).__name__}: {err})"
        for period in pending:
            record_fetch_error(os.path.join(root, "raw", period), period, today, message,
                               f"daily browser export {stamp} (failed)")
        print(f"[surface_b_browser] {message}")
        return 1
    return 0


def fetch_period(context: BrowserContext, cfg: dict, root: str, period: str,
                 today: datetime.date, stamp: str) -> None:
    covered = coverage(period, today)
    if not covered:
        return
    out_dir = os.path.join(root, "raw", period)
    response, error = request_export(context, cfg, covered)
    if error:
        # The last good export (if any) stays, with its own coverage, and the
        # error is recorded beside it so validation reports the gap.
        record_fetch_error(out_dir, period, today, error, f"daily browser export {stamp} (failed)")
        print(f"[surface_b_browser] {period}: {error}")
        return
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "overage_spend.csv"), "wb") as fh:
        fh.write(response.body())
    write_meta(out_dir, period, covered, f"daily browser export {stamp}")
    print(f"[surface_b_browser] {period}: saved export {covered.start}..{covered.end} "
          f"({response.text().count(chr(10))} lines)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    parser.add_argument("period", nargs="?", help="YYYY-MM (default: the month containing yesterday)")
    parser.add_argument("--login", action="store_true", help="open Chrome to sign in to claude.ai once")
    args = parser.parse_args()
    if args.login:
        return login(args.root)
    today = datetime.date.today()
    return fetch(args.root, target_periods(args.root, today, args.period), today)


if __name__ == "__main__":
    sys.exit(main())
