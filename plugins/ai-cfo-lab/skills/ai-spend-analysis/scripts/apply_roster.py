#!/usr/bin/env python3
"""Turn the fill-in roster into the config CSVs the pipeline reads.

Usage: apply_roster.py <workspace root>

config/roster.xlsx (or roster.csv) is the friendly, editable source of truth —
one row per person: email, name, department, seat_type. This regenerates
config/org_chart.csv and config/seats.csv from it, filling each seat's
monthly_rate from the seat_rates map in config/pipeline.json (falling back to
thresholds.standard_seat_rate_usd for a 'standard' seat).

Idempotent: fully rewrites both CSVs from the roster each run, so editing the
roster and re-running is all it takes to onboard a hire or change a seat. If no
roster file exists it exits 0 without touching anything, so a hand-maintained
org_chart.csv / seats.csv keeps working unchanged.
"""
import csv, json, os, sys

ROSTER_COLS = ["email", "name", "department", "seat_type"]
ORG_COLS = ["email", "name", "department", "team", "manager", "cost_center"]
SEAT_COLS = ["email", "seat_type", "monthly_rate"]


def read_json(path, default=None):
    return json.load(open(path)) if os.path.exists(path) else (default if default is not None else {})


def read_roster_csv(path):
    with open(path, newline="") as fh:
        return [row for row in csv.DictReader(fh)]


def read_roster_xlsx(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb["Roster"] if "Roster" in wb.sheetnames else wb.worksheets[0]
    rows = ws.iter_rows(values_only=True)
    header = [str(h).strip() if h is not None else "" for h in next(rows, [])]
    out = []
    for values in rows:
        row = {header[i]: ("" if v is None else str(v).strip()) for i, v in enumerate(values) if i < len(header)}
        out.append(row)
    return out


def load_roster(cfg):
    """Prefer roster.xlsx (needs openpyxl); fall back to roster.csv. None if neither."""
    xlsx, csv_path = os.path.join(cfg, "roster.xlsx"), os.path.join(cfg, "roster.csv")
    if os.path.exists(xlsx):
        try:
            return read_roster_xlsx(xlsx), "roster.xlsx"
        except ImportError:
            if not os.path.exists(csv_path):
                print("[roster] roster.xlsx present but openpyxl is not installed and no roster.csv fallback "
                      "exists — install openpyxl (pip install openpyxl) or provide config/roster.csv", file=sys.stderr)
                return "error", "roster.xlsx"
    if os.path.exists(csv_path):
        return read_roster_csv(csv_path), "roster.csv"
    return None, None


def seat_rate(seat_type, rates, warnings):
    if seat_type in rates:
        return rates[seat_type]
    warnings.append(f"seat_type '{seat_type}' has no price in pipeline.json seat_rates — using 0")
    return 0


def main():
    root = sys.argv[1]
    cfg = os.path.join(root, "config")
    roster, source = load_roster(cfg)
    if roster is None:
        print("[roster] no roster file found — leaving org_chart.csv / seats.csv as-is")
        return 0
    if roster == "error":
        return 1

    pipeline = read_json(os.path.join(cfg, "pipeline.json"))
    thresholds = read_json(os.path.join(cfg, "thresholds.json"))
    rates = dict(pipeline.get("seat_rates") or {})
    rates.setdefault("standard", thresholds.get("standard_seat_rate_usd", 0))

    org_rows, seat_rows, warnings, skipped = [], [], [], 0
    for row in roster:
        email = (row.get("email") or "").strip().lower()
        if "@" not in email:
            skipped += 1
            continue
        seat_type = (row.get("seat_type") or "standard").strip().lower() or "standard"
        org_rows.append({"email": email, "name": (row.get("name") or "").strip(),
                         "department": (row.get("department") or "").strip(),
                         "team": "", "manager": "", "cost_center": ""})
        seat_rows.append({"email": email, "seat_type": seat_type,
                          "monthly_rate": seat_rate(seat_type, rates, warnings)})

    with open(os.path.join(cfg, "org_chart.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=ORG_COLS, lineterminator="\n"); w.writeheader(); w.writerows(org_rows)
    with open(os.path.join(cfg, "seats.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=SEAT_COLS, lineterminator="\n"); w.writeheader(); w.writerows(seat_rows)

    premium = sum(1 for s in seat_rows if s["seat_type"] == "premium")
    no_dept = sum(1 for o in org_rows if not o["department"])
    print(f"[roster] applied {source}: {len(seat_rows)} people "
          f"({premium} premium, {len(seat_rows) - premium} standard) → org_chart.csv + seats.csv")
    if no_dept:
        print(f"  note: {no_dept} people have no department yet — they'll show as '(unmapped)' until you fill it in")
    for w in dict.fromkeys(warnings):  # de-duped, order-preserving
        print(f"  warning: {w}")
    if skipped:
        print(f"  skipped {skipped} row(s) with no valid email")
    return 0


if __name__ == "__main__":
    sys.exit(main())
