#!/usr/bin/env python3
"""Write the Claude Dashboard's datasets from /raw + /config.

Usage: python3 build_dashboard_datasets.py <workspace root> [--only id,id,...]

Writes one JSON file per dataset to <root>/dashboard/<id>.json (shaped
{"rows": [...]}, the Dashboard type's attached-file format) plus
<root>/dashboard/manifest.json, which lists each dataset's title, description,
refresh schedule and — for Ramp-sourced data — the connector call behind it.
The refresh run uploads each file and points the dashboard's dataset at it
(see references/daily-refresh.md); this script never touches the network.

Visibility (config/pipeline.json `dashboard_visibility`):
  "department" (default) — no names or emails leave the workspace; people roll
                           up to their department before the file is written.
  "person"               — per-person rows, for orgs that chose to share them.
The filter runs here, not in the page: anyone who can open the dashboard can
download a dataset's rows, so data the page hides would still be readable.

--only limits the run to the named datasets, so a job that refreshed one source
(the cloud job pulls only Ramp API cost) uploads only what it changed.

A dataset whose source failed this run (status error, missing, stale or
invalid for the latest month) is left out of the manifest, under "skipped":
re-uploading the previous data with a fresh timestamp would make stale numbers
look current. The dashboard keeps its last good file, shows its true age, and
the status dataset says what went wrong.
"""
from __future__ import annotations

import argparse, datetime, json, os, sys
from typing import Callable

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_workbooks import compute_flags, f, family_classifier, load, read_csv

Row = dict
Context = dict

UNMAPPED = "(unmapped)"

# Each dataset's metadata for the dashboard's Sources panel. `schedule` and
# `stale_after_hours` say how it stays current; staleness is about twice the cadence.
DATASETS = {
    "periods": {
        "title": "Months covered",
        "description": "Each month in the workspace, how many of its days the data covers, and whether it is still in progress.",
        "schedule": "Each daily refresh", "stale_after_hours": 48,
    },
    "seats": {
        "title": "Committed seats",
        "description": "The seat roster times each seat type's list price (Surface A). Changes only when seats change.",
        "schedule": "Each daily refresh, from the roster", "stale_after_hours": 48,
    },
    "overage": {
        "title": "Seat overage (claude.ai)",
        "description": "Usage-credit spend beyond seat allowances, from the claude.ai spend export (Surface B). Usage inside an allowance costs $0 and shows only as tokens. One day behind.",
        "schedule": "Daily, from the claude.ai spend export", "stale_after_hours": 48,
    },
    "api_cost": {
        "title": "API cost by day",
        "description": "Developer-platform (Console) API cost per day and model (Surface C).",
        "schedule": "Daily, from the API cost source", "stale_after_hours": 48,
    },
    "claude_code": {
        "title": "Claude Code usage",
        "description": "Claude Code usage per day and model from Anthropic's Claude Code usage report, with Anthropic's estimated cost at list price (not billed overage).",
        "schedule": "Daily, from the Admin API", "stale_after_hours": 48,
    },
    "card_charges": {
        "title": "Anthropic card charges",
        "description": "Actual card charges at Anthropic recorded in Ramp. Shown beside the totals, not added to them: a seat invoice paid by card is already in committed seats.",
        "schedule": "Daily, from Ramp", "stale_after_hours": 48,
    },
    "flags": {
        "title": "Savings and risk flags",
        "description": "Reclaim candidates, under-used premium seats, steady overage, product spikes and unowned API keys, using the thresholds in config/thresholds.json.",
        "schedule": "Each daily refresh", "stale_after_hours": 48,
    },
    "status": {
        "title": "Source status",
        "description": "Whether each source refreshed cleanly for the latest month, and what to do when one didn't.",
        "schedule": "Each daily refresh", "stale_after_hours": 48,
    },
}

# The Ramp connector calls behind Ramp-sourced datasets, kept with the file so an
# editor can see the query behind the numbers. `{start}`/`{end}` are filled per run.
RAMP_REQUESTS = {
    "api_cost": {"connector": "Ramp", "tool": "ramp_get_ai_token_spend_aggregates",
                 "args": {"metric": "cost", "providers": ["ANTHROPIC"], "group_by": ["model"],
                          "rollup": "daily", "start_at": "{start}", "end_at": "{end}"}},
    "card_charges": {"connector": "Ramp", "tool": "ramp_get_transactions",
                     "args": {"transactions_to_retrieve": "all_transactions_across_entire_business",
                              "filters": {"filters": [{"filter_type": "merchant", "filter": "Anthropic"}]},
                              "from_date": "{start}", "to_date": "{end}", "page_size": 200}},
}


def period_files(root: str, periods: list[str], filename: str) -> list[Row]:
    """Rows of raw/<period>/<filename> for every period that has it, tagged with the period."""
    rows: list[Row] = []
    for period in periods:
        path = os.path.join(root, "raw", period, filename)
        if os.path.exists(path):
            rows.extend({**row, "period": period} for row in read_csv(path))
    return rows


def month_of(date: str, folder_period: str) -> str:
    """A daily row's month comes from its own date: one Ramp pull can span several months."""
    return date[:7] if date else folder_period


def roll_up(rows: list[Row], key_fields: list[str], sum_fields: list[str]) -> list[Row]:
    """Group rows by key_fields and sum sum_fields — how people collapse to departments."""
    grouped: dict[tuple, Row] = {}
    for row in rows:
        key = tuple(row[field] for field in key_fields)
        bucket = grouped.setdefault(key, {**{f: row[f] for f in key_fields}, **{f: 0.0 for f in sum_fields}})
        for field in sum_fields:
            bucket[field] += row[field]
    for bucket in grouped.values():
        for field in sum_fields:
            bucket[field] = round(bucket[field], 6)
    return list(grouped.values())


def build_periods(ctx: Context) -> list[Row]:
    return [{"period": p, "days_covered": ctx["meta"][p]["days"], "days_in_month": ctx["meta"][p]["dim"],
             "partial": bool(ctx["meta"][p]["partial"])} for p in ctx["periods"]]


def build_seats(ctx: Context) -> list[Row]:
    rows = [{"email": s["email"], "name": s["name"], "department": s["department"],
             "seat_type": s["seat_type"], "monthly_rate": s["monthly_rate"], "seats": 1.0} for s in ctx["seats"]]
    if ctx["per_person"]:
        return [{k: v for k, v in r.items() if k != "seats"} for r in rows]
    return roll_up(rows, ["department", "seat_type"], ["seats", "monthly_rate"])


def build_overage(ctx: Context) -> list[Row]:
    rows = [{"period": r["period"], "email": r["email"], "name": r["name"], "department": r["department"],
             "product": r["product"], "model": r["model"], "family": ctx["classify"](r["model"]),
             "net_usd": r["net_usd"], "gross_usd": r["gross_usd"], "requests": r["requests"],
             "tokens": r["prompt_tokens"] + r["completion_tokens"]} for r in ctx["b_rows"]]
    keys = ["period", "department", "product", "model", "family"]
    sums = ["net_usd", "gross_usd", "requests", "tokens"]
    return roll_up(rows, (["email", "name"] if ctx["per_person"] else []) + keys, sums)


def build_api_cost(ctx: Context) -> list[Row]:
    rows = [{"period": month_of(r["date"], r["period"]), "date": r["date"], "model": r["model"] or "(not broken out)",
             "family": ctx["classify"](r["model"]), "cost_usd": r["cost_usd"]}
            for r in ctx["c_rows"] if r["record_type"] == "cost"]
    return roll_up(rows, ["period", "date", "model", "family"], ["cost_usd"])


def build_claude_code(ctx: Context) -> list[Row]:
    rows = []
    for r in period_files(ctx["root"], ctx["periods"], "claude_code_usage.csv"):
        person = ctx["org"].get(r["email"], {})
        is_user = r["actor_type"] == "user"
        rows.append({"period": month_of(r["date"], r["period"]), "date": r["date"],
                     "email": r["email"] if is_user else "",
                     "name": person.get("name", "") if is_user else f"API key: {r['api_key_name']}",
                     "department": (person.get("department") or UNMAPPED) if is_user else "(API keys)",
                     "model": r["model"], "family": ctx["classify"](r["model"]),
                     "est_cost_usd": f(r["est_cost_usd"]),
                     "tokens": sum(f(r[c]) for c in ("input_tokens", "output_tokens",
                                                          "cache_read_tokens", "cache_creation_tokens"))})
    keys = ["period", "date", "department", "model", "family"]
    return roll_up(rows, (["email", "name"] if ctx["per_person"] else []) + keys, ["est_cost_usd", "tokens"])


def build_card_charges(ctx: Context) -> list[Row]:
    # Ramp names the cardholder, not their email, so the roster is matched by name.
    by_name = {(o.get("name") or "").strip().lower(): o for o in ctx["org"].values() if o.get("name")}
    rows = []
    for r in period_files(ctx["root"], ctx["periods"], "card_charges.csv"):
        person = by_name.get(r["cardholder"].strip().lower(), {})
        rows.append({"period": month_of(r["date"], r["period"]), "date": r["date"], "cardholder": r["cardholder"],
                     "department": person.get("department") or UNMAPPED,
                     "allocation": r["allocation"], "amount_usd": f(r["amount_usd"]), "charges": 1.0})
    keys = ["period", "date", "department", "allocation"]
    return roll_up(rows, (["cardholder"] if ctx["per_person"] else []) + keys, ["amount_usd", "charges"])


def build_flags(ctx: Context) -> list[Row]:
    flags = compute_flags(ctx["thr"], ctx["seats"], ctx["periods"], ctx["b_rows"], ctx["c_rows"], ctx["keymap"])
    rows = []
    for flag in flags:
        saving = flag.get("est_monthly_saving_usd")
        subject = flag["subject"]
        if not ctx["per_person"] and "@" in subject:
            subject = ctx["org"].get(subject, {}).get("department") or UNMAPPED
        rows.append({"flag": flag["flag"], "subject": subject, "detail": flag["detail"],
                     "est_monthly_saving_usd": float(saving) if saving not in ("", None) else 0.0})
    return rows


STATUS_FILES = [
    ("Seat overage (claude.ai export)", "surface_b_status.json"),
    ("API cost", "surface_c_status.json"),
    ("Claude Code usage", "claude_code_status.json"),
    ("Anthropic card charges", "card_charges_status.json"),
]


def build_status(ctx: Context) -> list[Row]:
    latest = ctx["periods"][-1]
    rows = []
    for label, filename in STATUS_FILES:
        path = os.path.join(ctx["root"], "raw", latest, filename)
        if os.path.exists(path):
            state = json.load(open(path))
            rows.append({"source": label, "period": latest, "state": state.get("state", "unknown"),
                         "detail": state.get("detail", "")})
    return rows


BUILDERS: dict[str, Callable[[Context], list[Row]]] = {"periods": build_periods, "seats": build_seats, "overage": build_overage,
            "api_cost": build_api_cost, "claude_code": build_claude_code,
            "card_charges": build_card_charges, "flags": build_flags, "status": build_status}


RAMP_SOURCE_SETTINGS = {"api_cost": "api_cost_source", "card_charges": "card_charges_source"}


def ramp_request(dataset_id: str, rows: list[Row], periods: list[str]) -> dict:
    """The call that produced this file. It starts at the first month in the rows,
    since the cloud job pulls months of history into a one-month workspace."""
    dates = sorted(r["date"] for r in rows if r.get("date"))
    start = f"{dates[0][:7]}-01" if dates else f"{periods[0]}-01"
    end = datetime.date.today().isoformat()
    text = json.dumps(RAMP_REQUESTS[dataset_id]).replace("{start}", start).replace("{end}", end)
    return json.loads(text)


# The status file that says whether each sourced dataset refreshed cleanly.
SOURCE_STATUS = {"overage": "surface_b_status.json", "api_cost": "surface_c_status.json",
                 "claude_code": "claude_code_status.json", "card_charges": "card_charges_status.json"}
NOT_PUBLISHABLE = {"error", "missing", "stale", "invalid"}


def failed_source(root: str, period: str, dataset_id: str) -> str:
    """Why this dataset's source failed for the period, or "" when it is fine to publish."""
    filename = SOURCE_STATUS.get(dataset_id)
    path = os.path.join(root, "raw", period, filename) if filename else ""
    if not path or not os.path.exists(path):
        return ""
    with open(path) as fh:
        status = json.load(fh)
    if status.get("state") in NOT_PUBLISHABLE:
        return f"{status.get('state')}: {status.get('detail', '')}"
    return ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    parser.add_argument("--only", default="", help="comma-separated dataset ids")
    args = parser.parse_args()

    org, seats, thr, keymap, periods, b_rows, c_rows, meta, models, pipeline = load(args.root)
    if not periods:
        print("[dashboard] no raw periods found"); return 1
    visibility = (pipeline.get("dashboard_visibility") or "department").lower()
    if visibility not in ("department", "person"):
        print(f"[dashboard] dashboard_visibility must be 'department' or 'person', got {visibility!r}"); return 1
    wanted = [d.strip() for d in args.only.split(",") if d.strip()] or list(BUILDERS)
    unknown = [d for d in wanted if d not in BUILDERS]
    if unknown:
        print(f"[dashboard] unknown dataset ids: {unknown}"); return 1

    ctx = {"root": args.root, "org": org, "seats": seats, "thr": thr, "keymap": keymap, "periods": periods,
           "b_rows": b_rows, "c_rows": c_rows, "meta": meta, "classify": family_classifier(models),
           "per_person": visibility == "person"}
    out_dir = os.path.join(args.root, "dashboard")
    os.makedirs(out_dir, exist_ok=True)
    published: dict[str, dict] = {}
    skipped: dict[str, str] = {}
    for dataset_id in wanted:
        problem = failed_source(args.root, periods[-1], dataset_id)
        if problem:
            skipped[dataset_id] = problem
            print(f"[dashboard] {dataset_id}: not published — source {problem}")
            continue
        rows = BUILDERS[dataset_id](ctx)
        filename = f"{dataset_id}.json"
        with open(os.path.join(out_dir, filename), "w") as fh:
            json.dump({"rows": rows}, fh)
        entry = {**DATASETS[dataset_id], "file": filename, "rows": len(rows)}
        if pipeline.get(RAMP_SOURCE_SETTINGS.get(dataset_id, "")) == "ramp":
            entry["request"] = ramp_request(dataset_id, rows, periods)
        published[dataset_id] = entry
        print(f"[dashboard] {dataset_id}: {len(rows)} rows -> dashboard/{filename}")
    manifest = {"generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                "company": pipeline.get("company_name") or "AI Spend", "visibility": visibility,
                "dashboard_url": pipeline.get("dashboard_url") or "", "datasets": published, "skipped": skipped}
    with open(os.path.join(out_dir, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
