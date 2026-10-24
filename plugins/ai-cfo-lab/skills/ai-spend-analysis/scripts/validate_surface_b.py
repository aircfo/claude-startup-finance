#!/usr/bin/env python3
"""Validate a Surface B overage_spend.csv. Usage: validate_surface_b.py <csv> <YYYY-MM>
Writes surface_b_status.json next to the file. Exit 0 = valid, 1 = invalid (fail loud).

States: ok, missing (no export), invalid (schema drift / bad rows), and stale — a
valid export exists but the latest scheduled fetch failed, so the data stops at
the last good day; the detail says why and through when."""
from __future__ import annotations

import csv, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from periods import read_meta

REQUIRED = {"user_email", "product", "model", "total_requests", "total_prompt_tokens",
            "total_completion_tokens", "total_net_spend_usd", "total_gross_spend_usd"}


def main() -> int:
    path, period = sys.argv[1], sys.argv[2]
    out = os.path.join(os.path.dirname(path), "surface_b_status.json")
    meta = read_meta(os.path.dirname(path))

    def write(state: str, detail: str, rows: int = 0) -> None:
        json.dump({"surface": "B", "state": state, "detail": detail, "rows": rows, "period": period},
                  open(out, "w"), indent=2)
        print(f"[surface_b] {state}: {detail}")

    if not os.path.exists(path) or os.path.getsize(path) == 0:
        # A scheduled fetch records why it failed; say that rather than a generic gap.
        write("missing", meta.get("fetch_error") or "overage_spend.csv absent or empty — export failed or not yet fetched")
        return 1
    with open(path) as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        write("invalid", "no data rows"); return 1
    missing = REQUIRED - set(rows[0].keys())
    if missing:
        write("invalid", f"schema drift — missing columns: {sorted(missing)}"); return 1
    bad = sum(1 for r in rows if not r["user_email"] or "@" not in r["user_email"])
    try:
        total = sum(float(r["total_net_spend_usd"] or 0) for r in rows)
    except ValueError:
        write("invalid", "non-numeric spend values"); return 1
    if bad > len(rows) * 0.05:
        write("invalid", f"{bad} rows with malformed user_email"); return 1
    if meta.get("fetch_error"):
        through = meta.get("end") or "the last good export"
        write("stale", f"{meta['fetch_error']} — showing the export through {through}", len(rows))
        return 1
    write("ok", f"{len(rows)} rows, ${total:.2f} net overage", len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
