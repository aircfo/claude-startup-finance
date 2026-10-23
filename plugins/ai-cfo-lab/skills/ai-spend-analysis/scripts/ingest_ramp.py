#!/usr/bin/env python3
"""Normalize Ramp answers that Claude saved into the pipeline's own tables.

Usage: python3 ingest_ramp.py <workspace root> <YYYY-MM>

Ramp is reached through its MCP connector, which only Claude can call, so the
refresh run saves each Ramp answer verbatim and this script does the parsing:

  raw/<period>/ramp_api_cost.json         -> raw/<period>/api_usage_cost.csv (Surface C)
      ramp_get_ai_token_spend_aggregates, metric "cost", rollup "daily", group_by ["model"]
  raw/<period>/ramp_card_transactions.json -> raw/<period>/card_charges.csv
      ramp_get_transactions, merchant filter "Anthropic", every page

Which of these run is set in config/pipeline.json: `api_cost_source: "ramp"` and
`card_charges_source: "ramp"`. A configured source whose file is missing gets a
"missing" status, so the dashboard flags the gap instead of showing $0.

Each saved answer is checked for completeness, because it reaches this script
only after Claude writes it out, and a dropped page or mistyped figure must not
reach the dashboard:
  - card charges: the saved pages must hold exactly the `total_count` Ramp
    reported on the first page;
  - API cost: when raw/<period>/ramp_api_cost_total.json is saved (the same
    call with rollup "all"), each model's daily rows must sum to its total
    within a cent.
Only the fields read here need saving (period_start_at, model, total_cost; for
transactions spent_by_user, original_amount, state, transaction_time,
spend_allocation_name, plus total_count), copied exactly.
A failed check sets the status to "error" and writes no table.

Ramp's API cost is its estimate from token counts, not an Anthropic invoice; the
rows say so in `description`. Card charges are actual cash and are reported
beside the three surfaces, never added to them (a seat invoice paid by card
would otherwise be counted twice).
"""
import csv, json, os, sys

API_COLS = ["record_type", "date", "workspace_id", "api_key_id", "model", "service_tier",
            "uncached_input_tokens", "cache_read_tokens", "cache_creation_tokens",
            "output_tokens", "cost_usd", "description"]
CARD_COLS = ["date", "cardholder", "amount_usd", "allocation", "state"]


def write_status(out_dir, filename, source, state, detail, rows=0):
    with open(os.path.join(out_dir, filename), "w") as fh:
        json.dump({"source": source, "state": state, "detail": detail, "rows": rows}, fh, indent=2)
    print(f"[ramp:{source}] {state}: {detail}")


def write_csv(path, columns, rows):
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def as_responses(saved):
    """A saved file may hold one tool answer or a list of them (one per page)."""
    return saved if isinstance(saved, list) else [saved]


def api_cost_rows(saved):
    rows = []
    for response in as_responses(saved):
        for bucket in ((response.get("cost") or {}).get("data") or []):
            rows.append({
                "record_type": "cost",
                "date": (bucket.get("period_start_at") or "")[:10],
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


def transactions(saved):
    found = []
    for item in as_responses(saved):
        if isinstance(item, dict) and "transactions" in item:
            found.extend(item.get("transactions") or [])
        elif isinstance(item, dict) and "transaction_uuid" in item:
            found.append(item)
    return found


class IncompleteAnswer(Exception):
    """The saved answer doesn't match Ramp's own count or total."""


def check_card_count(saved):
    first = as_responses(saved)[0] if as_responses(saved) else {}
    expected = first.get("total_count") if isinstance(first, dict) else None
    found = len(transactions(saved))
    if expected is not None and found != expected:
        raise IncompleteAnswer(f"saved pages hold {found} of the {expected} transactions Ramp reported")


def check_api_total(out_dir, rows):
    """Per model, so two copying slips can't cancel each other out."""
    total_path = os.path.join(out_dir, "ramp_api_cost_total.json")
    if not os.path.exists(total_path):
        return
    expected = {}
    for bucket in ((json.load(open(total_path)).get("cost") or {}).get("data") or []):
        expected[bucket.get("model") or ""] = float(bucket.get("total_cost") or 0)
    found = {}
    for row in rows:
        found[row["model"]] = found.get(row["model"], 0.0) + row["cost_usd"]
    for model in sorted(set(expected) | set(found)):
        if abs(found.get(model, 0.0) - expected.get(model, 0.0)) > 0.01:
            raise IncompleteAnswer(f"{model or '(no model)'} daily rows sum to ${found.get(model, 0.0):,.2f} "
                                   f"but Ramp's total is ${expected.get(model, 0.0):,.2f}")


def card_rows(saved):
    rows = []
    for txn in transactions(saved):
        if (txn.get("state") or "").upper() == "DECLINED":
            continue
        rows.append({
            "date": (txn.get("transaction_time") or "")[:10],
            "cardholder": txn.get("spent_by_user") or "",
            "amount_usd": round(float(txn.get("original_amount") or 0), 2),
            "allocation": txn.get("spend_allocation_name") or "",
            "state": txn.get("state") or "",
        })
    return rows


def ingest(out_dir, raw_name, status_name, source, build_rows, check, out_name, columns, status_label):
    raw_path = os.path.join(out_dir, raw_name)
    if not os.path.exists(raw_path):
        write_status(out_dir, status_name, source, "missing",
                     f"{raw_name} not saved this run — {status_label} not refreshed")
        return
    try:
        saved = json.load(open(raw_path))
        rows = build_rows(saved)
        check(out_dir, saved, rows)
    except IncompleteAnswer as err:
        write_status(out_dir, status_name, source, "error", f"{raw_name} incomplete: {err} — not published")
        return
    except (ValueError, TypeError, AttributeError) as err:
        write_status(out_dir, status_name, source, "error", f"{raw_name} unreadable: {err}")
        return
    write_csv(os.path.join(out_dir, out_name), columns, rows)
    write_status(out_dir, status_name, source, "ok", f"{len(rows)} rows from Ramp", len(rows))


def main():
    root, period = sys.argv[1], sys.argv[2]
    out_dir = os.path.join(root, "raw", period)
    os.makedirs(out_dir, exist_ok=True)
    cfg_path = os.path.join(root, "config", "pipeline.json")
    cfg = json.load(open(cfg_path)) if os.path.exists(cfg_path) else {}
    if cfg.get("api_cost_source") == "ramp":
        ingest(out_dir, "ramp_api_cost.json", "surface_c_status.json", "ramp_api_cost",
               api_cost_rows, lambda out, saved, rows: check_api_total(out, rows),
               "api_usage_cost.csv", API_COLS, "API cost")
    if cfg.get("card_charges_source") == "ramp":
        ingest(out_dir, "ramp_card_transactions.json", "card_charges_status.json", "ramp_card_charges",
               card_rows, lambda out, saved, rows: check_card_count(saved),
               "card_charges.csv", CARD_COLS, "card charges")
    return 0


if __name__ == "__main__":
    sys.exit(main())
