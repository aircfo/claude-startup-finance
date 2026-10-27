#!/usr/bin/env python3
"""The claude.ai spend export for Team plans, fetched by a fixed script on a Mac.

Usage:
  uv run --with playwright python fetch_spend_export.py <folder> --login
      Once, and whenever the login expires: opens Chrome on a profile kept in
      <folder>/.browser-profile so a claude.ai Owner can sign in.
  uv run --with playwright python fetch_spend_export.py <folder> --org <org id> --check
      Tests the saved login with the same request, saving nothing.
  uv run --with playwright python fetch_spend_export.py <folder> --org <org id>
      Daily: fetches the month that contains yesterday, from the 1st through yesterday,
      and first finishes last month if its newest saved export stops short of its end.
      Each export is handed to the engine's `save`, which checks it and files it in raw/.

The org id is in the address of claude.ai's admin pages: .../organizations/<org id>/...

Why a fixed script: Team plans have no spend API, and this runs daily with no Claude
session and nothing to approve. It makes one kind of request, the GET behind the Export
spend report button, and saves the bytes as received. That endpoint is UNDOCUMENTED and can change;
every failure says so plainly, and the export button is always the fallback.
"""
from __future__ import annotations

import argparse
import datetime
import os
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aicfo_spend  # noqa: E402

if TYPE_CHECKING:
    from playwright.sync_api import BrowserContext, Playwright

CLAUDE_URL = "https://claude.ai"
EXPORT_PATH = "/api/organizations/{org}/analytics/spend-report-export?start_date={start}&end_date={end}"
PROFILE_FOLDER = ".browser-profile"
SOURCE = "claude-spend-export"
REQUIRED_COLUMNS = ("user_email", "total_net_spend_usd")

Span = tuple[datetime.date, datetime.date]


def spans_to_fetch(folder: Path, today: datetime.date) -> list[Span]:
    """Last month first when its newest export stops short of its last day, then this month."""
    yesterday = today - datetime.timedelta(days=1)
    this_month = (yesterday.replace(day=1), yesterday)
    previous_end = this_month[0] - datetime.timedelta(days=1)
    reached = _furthest_saved_end(folder, previous_end)
    if reached is not None and reached < previous_end:
        return [(previous_end.replace(day=1), previous_end), this_month]
    return [this_month]


def looks_like_export(text: str) -> bool:
    first_line = text.split("\n", 1)[0]
    return all(column in first_line for column in REQUIRED_COLUMNS)


def export_url(org: str, span: Span) -> str:
    return CLAUDE_URL + EXPORT_PATH.format(org=org, start=span[0].isoformat(), end=span[1].isoformat())


def save_export(folder: Path, span: Span, content: bytes) -> int:
    """Hand an export to the engine's save, through a file it deletes afterwards."""
    inbox = folder / "inbox"
    inbox.mkdir(exist_ok=True)
    download = inbox / f"{SOURCE}_{span[0]}_{span[1]}.csv"
    download.write_bytes(content)
    try:
        return aicfo_spend.main(
            [str(folder), "save", SOURCE, "--start", str(span[0]), "--end", str(span[1]), "--file", str(download)]
        )
    finally:
        download.unlink(missing_ok=True)


def login(folder: Path) -> int:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        context = _open_profile(playwright, folder, headless=False)
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(f"{CLAUDE_URL}/login")
        print("Sign in to claude.ai as an Owner in the window that opened, then close the window.")
        print(f"The login is kept in {folder / PROFILE_FOLDER} for the daily fetch.")
        page.wait_for_event("close", timeout=0)
        context.close()
    return 0


def fetch(folder: Path, org: str, spans: list[Span], check_only: bool) -> int:
    if not (folder / PROFILE_FOLDER).is_dir():
        print("fetch_spend_export: no browser profile yet; run once with --login")
        return 1
    from playwright.sync_api import sync_playwright

    failures = 0
    with sync_playwright() as playwright:
        context = _open_profile(playwright, folder, headless=True)
        try:
            for span in spans:
                content, error = _request(context, org, span)
                if error:
                    failures += 1
                    print(f"fetch_spend_export: {span[0]} to {span[1]}: {error}")
                elif check_only:
                    print("fetch_spend_export: signed in, and the export answers")
                elif save_export(folder, span, content) != 0:
                    failures += 1
        finally:
            context.close()
    return 1 if failures else 0


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(description="Fetch the claude.ai spend export into an aicfo-spend folder.")
    parser.add_argument("folder", help="the company's aicfo-spend folder")
    parser.add_argument("--org", help="the claude.ai organization id")
    parser.add_argument("--login", action="store_true", help="open Chrome to sign in to claude.ai once")
    parser.add_argument("--check", action="store_true", help="test the saved login without saving anything")
    args = parser.parse_args(argv)
    folder = Path(args.folder).expanduser()
    if args.login:
        return login(folder)
    if not args.org:
        parser.error("--org is needed to fetch; it's in the address of claude.ai's admin pages")
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    spans = [(yesterday, yesterday)] if args.check else spans_to_fetch(folder, today)
    return fetch(folder, args.org, spans, check_only=args.check)


def _furthest_saved_end(folder: Path, month_end: datetime.date) -> datetime.date | None:
    """The last day any saved export for month_end's month reaches, or None if none is saved."""
    ends = []
    for path in (folder / "raw" / month_end.strftime("%Y-%m")).glob(f"{SOURCE}_*.csv"):
        # Saved names read <source>_<start>_<end>_saved-<time>.csv.
        parts = path.stem.split("_")
        try:
            ends.append(datetime.date.fromisoformat(parts[2]))
        except (IndexError, ValueError):
            continue
    return max(ends, default=None)


def _open_profile(playwright: Playwright, folder: Path, headless: bool) -> BrowserContext:
    return playwright.chromium.launch_persistent_context(
        str(folder / PROFILE_FOLDER), channel="chrome", headless=headless, accept_downloads=False
    )


def _request(context: BrowserContext, org: str, span: Span) -> tuple[bytes, str | None]:
    """The one request this script makes: the bytes, or why they can't be used."""
    response = context.request.get(export_url(org, span))
    if response.status in (401, 403):
        return b"", "signed out of claude.ai; run with --login"
    if not response.ok:
        return b"", f"HTTP {response.status} from the spend export; the endpoint may have changed"
    if not looks_like_export(response.text()):
        return b"", "the answer wasn't the spend export; signed out, or the endpoint changed"
    return response.body(), None


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
