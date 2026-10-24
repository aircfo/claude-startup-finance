"""The month-coverage rule every source shares, and the period's meta.json.

Every source is a day behind, so a period is covered from its first day through
yesterday (or its last day, once it has ended). The fetchers, the Ramp importer
and the pipeline all use these helpers so that rule lives in one place.
"""
from __future__ import annotations

import datetime
import json
import os
from calendar import monthrange
from typing import NamedTuple, Optional

SELF_REGISTERED = "registered by run_pipeline (no export meta yet)"


class Coverage(NamedTuple):
    start: datetime.date
    end: datetime.date
    partial: bool


def month_of(day: datetime.date) -> str:
    return day.strftime("%Y-%m")


def previous_month(period: str) -> str:
    year, month = map(int, period.split("-"))
    return f"{year - 1}-12" if month == 1 else f"{year}-{month - 1:02d}"


def coverage(period: str, today: datetime.date) -> Optional[Coverage]:
    """First day through yesterday (or the month's last day). None before any day is complete."""
    year, month = map(int, period.split("-"))
    start = datetime.date(year, month, 1)
    last = datetime.date(year, month, monthrange(year, month)[1])
    end = min(last, today - datetime.timedelta(days=1))
    if end < start:
        return None
    return Coverage(start, end, end < last)


def read_meta(out_dir: str) -> dict:
    path = os.path.join(out_dir, "meta.json")
    try:
        with open(path) as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def write_meta(out_dir: str, period: str, covered: Coverage, source: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    meta = {"period": period, "start": covered.start.isoformat(), "end": covered.end.isoformat(),
            "days_covered": covered.end.day, "partial": covered.partial, "source": source}
    with open(os.path.join(out_dir, "meta.json"), "w") as fh:
        json.dump(meta, fh, indent=2)


def record_fetch_error(out_dir: str, period: str, today: datetime.date, error: str, source: str) -> None:
    """Note a failed fetch without pretending the window moved: the coverage of the
    last good export stays as it was, so the dashboard keeps its true age."""
    meta = read_meta(out_dir)
    if not meta:
        covered = coverage(period, today)
        meta = {"period": period, "days_covered": 0, "partial": True}
        if covered:
            meta.update(start=covered.start.isoformat(), end=None)
    meta["fetch_error"] = error
    meta["source"] = source
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "meta.json"), "w") as fh:
        json.dump(meta, fh, indent=2)


def register_period(out_dir: str, period: str, today: datetime.date) -> None:
    """Make sure a period has meta.json so it shows up, flagged, even with no export.
    A meta this function wrote earlier is refreshed, so a month first registered
    mid-month doesn't stay 'partial' after it ends; a meta written by an export
    (which knows exactly what it covers) is left alone."""
    meta = read_meta(out_dir)
    if meta and meta.get("source") != SELF_REGISTERED:
        return
    covered = coverage(period, today)
    if covered:
        write_meta(out_dir, period, covered, SELF_REGISTERED)
        return
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "meta.json"), "w") as fh:
        json.dump({"period": period, "days_covered": 0, "partial": True, "source": SELF_REGISTERED}, fh, indent=2)
