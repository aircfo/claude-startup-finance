#!/usr/bin/env python3
"""Per-person Claude Code usage via the Admin API's documented Claude Code report.

Usage: python3 fetch_claude_code.py <workspace root> <YYYY-MM>

The documented per-person source for Claude Code: one row per person (or API
key) per day per model, with tokens and Anthropic's estimated cost. It covers
Claude Code only — not Chat or Cowork — and its dollars are usage at list price,
not billed overage, so it sits beside Surface B rather than replacing it.

It reports on the Admin key's own Console organization. When the claude.ai Team
workspace is a separate organization, it sees only Claude Code run on API keys
(customer_type "api") and no Team-seat users.

The report returns one UTC day per call. Each run fetches the period's days that
aren't in raw/<period>/claude_code_usage.csv yet, plus the two most recent days
(their figures can still settle), and keeps the rest — so a daily run makes a
few calls, not one per day of the month.

Uses the same Admin API key as Surface C (ANTHROPIC_ADMIN_API_KEY, or
<root>/.secrets/anthropic_admin_key). Graceful-missing: no key -> status
"not_configured", exit 0. Never prints or persists the key. Read-only.
"""
from __future__ import annotations

import csv, datetime, json, os, sys, urllib.error, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_surface_c import API, VER, read_key
from periods import coverage

REPORT_PATH = "/v1/organizations/usage_report/claude_code"
COLUMNS = ["date", "actor_type", "email", "api_key_name", "customer_type", "subscription_type",
           "is_remote", "model", "input_tokens", "output_tokens", "cache_read_tokens",
           "cache_creation_tokens", "est_cost_usd"]
SETTLING_DAYS = 2


def status(out_dir: str, state: str, detail: str, rows: int = 0, through: str = "") -> None:
    with open(os.path.join(out_dir, "claude_code_status.json"), "w") as fh:
        json.dump({"source": "claude_code", "state": state, "detail": detail, "rows": rows,
                   "through": through}, fh, indent=2)
    print(f"[claude_code] {state}: {detail}")


def days_to_fetch(period: str, today: datetime.date) -> list[datetime.date]:
    """Every completed day of the period (through yesterday). Empty for a future period."""
    covered = coverage(period, today)
    if not covered:
        return []
    return [covered.start + datetime.timedelta(days=n) for n in range((covered.end - covered.start).days + 1)]


def days_needed(days: list[datetime.date], have: set[str]) -> list[datetime.date]:
    """Days not saved yet, plus the most recent ones whose figures can still change."""
    settled_before = days[-1] - datetime.timedelta(days=SETTLING_DAYS - 1) if days else None
    return [d for d in days if d.isoformat() not in have or (settled_before and d >= settled_before)]


def fetch_day(day: datetime.date, key: str) -> list[dict]:
    records, page = [], None
    while True:
        params = {"starting_at": day.isoformat(), "limit": 1000}
        if page:
            params["page"] = page
        url = f"{API}{REPORT_PATH}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={"x-api-key": key, "anthropic-version": VER})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.load(resp)
        records.extend(data.get("data", []))
        if not data.get("has_more"):
            return records
        page = data.get("next_page")


def flatten(record: dict) -> list[dict]:
    """One output row per model in the record's model_breakdown."""
    actor = record.get("actor") or {}
    base = {
        "date": (record.get("date") or "")[:10],
        "actor_type": "user" if actor.get("type") == "user_actor" else "api_key",
        "email": (actor.get("email_address") or "").lower(),
        "api_key_name": actor.get("api_key_name") or "",
        "customer_type": record.get("customer_type") or "",
        "subscription_type": record.get("subscription_type") or "",
        "is_remote": bool(record.get("is_remote")),
    }
    rows = []
    for model in record.get("model_breakdown") or []:
        tokens = model.get("tokens") or {}
        cost = model.get("estimated_cost") or {}
        rows.append({**base,
            "model": model.get("model") or "",
            "input_tokens": tokens.get("input", 0),
            "output_tokens": tokens.get("output", 0),
            "cache_read_tokens": tokens.get("cache_read", 0),
            "cache_creation_tokens": tokens.get("cache_creation", 0),
            # The report gives cost in minor units (cents for USD).
            "est_cost_usd": round(float(cost.get("amount", 0) or 0) / 100.0, 6)})
    return rows


def main() -> int:
    root, period = sys.argv[1], sys.argv[2]
    out_dir = os.path.join(root, "raw", period)
    os.makedirs(out_dir, exist_ok=True)
    key = read_key(root)
    if not key:
        status(out_dir, "not_configured", "no Admin API key — per-person Claude Code usage skipped")
        return 0
    days = days_to_fetch(period, datetime.date.today())
    if not days:
        status(out_dir, "not_configured", f"{period} has no completed days yet")
        return 0
    out_path = os.path.join(out_dir, "claude_code_usage.csv")
    saved: list[dict] = []
    if os.path.exists(out_path):
        with open(out_path) as fh:
            saved = list(csv.DictReader(fh))
    wanted = days_needed(days, {r["date"] for r in saved})
    refetched = {d.isoformat() for d in wanted}
    rows = [r for r in saved if r["date"] not in refetched]
    try:
        for day in wanted:
            for record in fetch_day(day, key):
                rows.extend(flatten(record))
    except urllib.error.HTTPError as err:
        hint = "auth problem — check the Admin key" if err.code in (401, 403) else "request failed"
        status(out_dir, "error", f"HTTP {err.code} from the Claude Code report ({hint})")
        return 0
    except Exception as err:
        status(out_dir, "error", f"{type(err).__name__}: {err}")
        return 0
    rows.sort(key=lambda r: r["date"])
    with open(out_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    through = days[-1].isoformat()
    status(out_dir, "ok", f"{len(rows)} rows through {through}", len(rows), through)
    return 0


if __name__ == "__main__":
    sys.exit(main())
