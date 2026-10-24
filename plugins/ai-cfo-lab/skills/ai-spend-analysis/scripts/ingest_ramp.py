#!/usr/bin/env python3
"""Normalize Ramp answers that Claude saved into the pipeline's own tables.

Usage: python3 ingest_ramp.py <workspace root> <YYYY-MM>

Ramp is reached through its MCP connector, which only Claude can call, so the
refresh run saves each Ramp answer and this script does the parsing:

  raw/<period>/ramp_api_cost.json          -> raw/<month>/api_usage_cost.csv (Surface C),
      ramp_get_ai_token_spend_aggregates,     one file per month the pull covers
      metric "cost", rollup "daily", group_by ["model"]
  raw/<period>/ramp_card_transactions.json -> raw/<period>/card_charges.csv
      ramp_get_transactions, merchant filter "Anthropic", every page

Which of these run is set in config/pipeline.json: `api_cost_source: "ramp"` and
`card_charges_source: "ramp"`. API cost is skipped when `api_cost_refreshed_by`
is "cloud" (a cloud routine owns it, so this workspace never saves it). A
configured source whose file is missing gets a "missing" status, so the
dashboard flags the gap instead of showing $0.

An API-cost pull can span several months (the cloud job pulls history): each
row is filed under its own date's month, and each month's table is replaced
whole by the newest pull that covers it, so months never mix or double count.

Each saved answer is checked before anything is written, because it reaches
this script only after Claude writes it out, and a dropped page or mistyped
figure must not reach the dashboard:
  - card charges: the saved pages must hold exactly the `total_count` Ramp
    reported on the first page (which therefore must be saved);
  - API cost: when raw/<period>/ramp_api_cost_total.json is saved (the same
    call with rollup "all"), each model's daily rows must sum to its total
    within a cent.
A failed check sets the status to "error" and writes no table.

Each saved answer is used once: after it is read (whatever the outcome) it is
renamed `<name>.imported.json`, so a day when Claude saved nothing new reports
"missing" instead of quietly re-importing yesterday's answer as fresh.

Only the fields read here need saving, copied exactly: for API cost
period_start_at, model, total_cost; for transactions spent_by_user, amount,
original_amount, original_currency, state, transaction_time,
spend_allocation_name, plus each page's total_count.

Ramp's API cost is its estimate from token counts, not an Anthropic invoice; the
rows say so in `description`. Card charges are actual cash, in US dollars, and
are reported beside the three surfaces, never added to them (a seat invoice
paid by card would otherwise be counted twice).
"""
from __future__ import annotations

import csv, datetime, json, os, sys
from typing import Callable, Optional, Union

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from periods import register_period

API_COLS = ["record_type", "date", "workspace_id", "api_key_id", "model", "service_tier",
            "uncached_input_tokens", "cache_read_tokens", "cache_creation_tokens",
            "output_tokens", "cost_usd", "description"]
CARD_COLS = ["date", "cardholder", "amount_usd", "allocation", "state"]

Saved = Union[dict, list]
Row = dict


class IncompleteAnswer(Exception):
    """The saved answer doesn't match Ramp's own count or total, or can't be read as dollars."""


def write_status(out_dir: str, filename: str, source: str, state: str, detail: str, rows: int = 0) -> None:
    with open(os.path.join(out_dir, filename), "w") as fh:
        json.dump({"source": source, "state": state, "detail": detail, "rows": rows}, fh, indent=2)
    print(f"[ramp:{source}] {state}: {detail}")


def write_csv(path: str, columns: list[str], rows: list[Row]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def as_responses(saved: Saved) -> list:
    """A saved file may hold one tool answer or a list of them (one per page)."""
    return saved if isinstance(saved, list) else [saved]


# ---- API cost ----

def api_cost_rows(saved: Saved) -> list[Row]:
    rows = []
    for response in as_responses(saved):
        for bucket in ((response.get("cost") or {}).get("data") or []):
            date = (bucket.get("period_start_at") or "")[:10]
            if len(date) != 10:
                raise IncompleteAnswer("a saved API-cost bucket has no period_start_at date")
            rows.append({
                "record_type": "cost",
                "date": date,
                "workspace_id": "(via Ramp)",
                "api_key_id": "",
                "model": bucket.get("model") or "",
                "service_tier": "",
                "uncached_input_tokens": "", "cache_read_tokens": "",
                "cache_creation_tokens": "", "output_tokens": "",
                "cost_usd": round(float(bucket.get("total_cost") or 0), 6),
                "description": "Ramp estimate from token usage",
            })
    return rows


def check_api_total(out_dir: str, rows: list[Row]) -> None:
    """Per model, so two copying slips can't cancel each other out."""
    total_path = os.path.join(out_dir, "ramp_api_cost_total.json")
    if not os.path.exists(total_path):
        return
    with open(total_path) as fh:
        buckets = (json.load(fh).get("cost") or {}).get("data") or []
    expected = {(b.get("model") or ""): float(b.get("total_cost") or 0) for b in buckets}
    found: dict[str, float] = {}
    for row in rows:
        found[row["model"]] = found.get(row["model"], 0.0) + row["cost_usd"]
    for model in sorted(set(expected) | set(found)):
        if abs(found.get(model, 0.0) - expected.get(model, 0.0)) > 0.01:
            raise IncompleteAnswer(f"{model or '(no model)'} daily rows sum to ${found.get(model, 0.0):,.2f} "
                                   f"but Ramp's total is ${expected.get(model, 0.0):,.2f}")


def file_by_month(root: str, rows: list[Row], today: datetime.date) -> list[str]:
    """Write each month's rows to that month's folder, replacing its table."""
    by_month: dict[str, list[Row]] = {}
    for row in rows:
        by_month.setdefault(row["date"][:7], []).append(row)
    for month, month_rows in sorted(by_month.items()):
        month_dir = os.path.join(root, "raw", month)
        register_period(month_dir, month, today)
        write_csv(os.path.join(month_dir, "api_usage_cost.csv"), API_COLS, month_rows)
    return sorted(by_month)


# ---- card charges ----

def transactions(saved: Saved) -> list[dict]:
    found: list[dict] = []
    for item in as_responses(saved):
        if isinstance(item, dict) and "transactions" in item:
            found.extend(item.get("transactions") or [])
        elif isinstance(item, dict) and "transaction_uuid" in item:
            found.append(item)
    return found


def check_card_count(saved: Saved) -> None:
    pages = as_responses(saved)
    first = pages[0] if pages else {}
    expected = first.get("total_count") if isinstance(first, dict) else None
    if expected is None:
        raise IncompleteAnswer("the saved pages don't include Ramp's total_count, so completeness can't be checked")
    found = len(transactions(saved))
    if found != expected:
        raise IncompleteAnswer(f"saved pages hold {found} of the {expected} transactions Ramp reported")


def usd_amount(txn: dict) -> float:
    """The charge in US dollars. Ramp's original_amount is in the merchant's currency,
    so a non-USD charge uses Ramp's settled `amount` (shown as "$1,234.56")."""
    if (txn.get("original_currency") or "USD").upper() == "USD":
        if txn.get("original_amount") in (None, ""):
            raise IncompleteAnswer("a saved charge has no original_amount")
        return round(float(txn["original_amount"]), 2)
    settled = str(txn.get("amount") or "").strip()
    if not settled.startswith("$"):
        raise IncompleteAnswer(f"a {txn.get('original_currency')} charge was saved without its US-dollar `amount`")
    return round(float(settled.lstrip("$").replace(",", "")), 2)


def card_rows(saved: Saved) -> list[Row]:
    rows = []
    for txn in transactions(saved):
        if (txn.get("state") or "").upper() == "DECLINED":
            continue
        rows.append({
            "date": (txn.get("transaction_time") or "")[:10],
            "cardholder": txn.get("spent_by_user") or "",
            "amount_usd": usd_amount(txn),
            "allocation": txn.get("spend_allocation_name") or "",
            "state": txn.get("state") or "",
        })
    return rows


# ---- shared ----

def mark_imported(out_dir: str, *names: str) -> None:
    for name in names:
        path = os.path.join(out_dir, name)
        if os.path.exists(path):
            os.replace(path, path[: -len(".json")] + ".imported.json")


def read_saved(out_dir: str, raw_name: str, status_name: str, source: str, label: str) -> Optional[Saved]:
    raw_path = os.path.join(out_dir, raw_name)
    if not os.path.exists(raw_path):
        write_status(out_dir, status_name, source, "missing", f"{raw_name} not saved this run — {label} not refreshed")
        return None
    try:
        with open(raw_path) as fh:
            saved: Saved = json.load(fh)
        return saved
    except ValueError as err:
        write_status(out_dir, status_name, source, "error", f"{raw_name} unreadable: {err}")
        mark_imported(out_dir, raw_name)
        return None


def ingest(out_dir: str, raw_name: str, status_name: str, source: str, label: str,
           build: Callable[[Saved], list[Row]], check: Callable[[Saved, list[Row]], None],
           write: Callable[[list[Row]], str]) -> None:
    saved = read_saved(out_dir, raw_name, status_name, source, label)
    if saved is None:
        return
    try:
        rows = build(saved)
        check(saved, rows)
        where = write(rows)
    except IncompleteAnswer as err:
        write_status(out_dir, status_name, source, "error", f"{raw_name} incomplete: {err} — not published")
        return
    except (TypeError, AttributeError, ValueError) as err:
        write_status(out_dir, status_name, source, "error", f"{raw_name} unreadable: {err}")
        return
    finally:
        mark_imported(out_dir, raw_name, raw_name.replace(".json", "_total.json"))
    write_status(out_dir, status_name, source, "ok", f"{len(rows)} rows from Ramp{where}", len(rows))


def main() -> int:
    root, period = sys.argv[1], sys.argv[2]
    out_dir = os.path.join(root, "raw", period)
    os.makedirs(out_dir, exist_ok=True)
    cfg_path = os.path.join(root, "config", "pipeline.json")
    cfg: dict = {}
    if os.path.exists(cfg_path):
        with open(cfg_path) as fh:
            cfg = json.load(fh)
    today = datetime.date.today()

    if cfg.get("api_cost_source") == "ramp" and cfg.get("api_cost_refreshed_by", "mac") != "cloud":
        def write_api(rows: list[Row]) -> str:
            months = file_by_month(root, rows, today)
            return f" ({', '.join(months)})" if months else ""
        ingest(out_dir, "ramp_api_cost.json", "surface_c_status.json", "ramp_api_cost", "API cost",
               api_cost_rows, lambda saved, rows: check_api_total(out_dir, rows), write_api)

    if cfg.get("card_charges_source") == "ramp":
        def write_cards(rows: list[Row]) -> str:
            write_csv(os.path.join(out_dir, "card_charges.csv"), CARD_COLS, rows)
            return ""
        ingest(out_dir, "ramp_card_transactions.json", "card_charges_status.json", "ramp_card_charges",
               "card charges", card_rows, lambda saved, rows: check_card_count(saved), write_cards)
    return 0


if __name__ == "__main__":
    sys.exit(main())
