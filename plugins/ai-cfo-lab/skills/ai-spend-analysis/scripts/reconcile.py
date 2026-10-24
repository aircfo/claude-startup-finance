#!/usr/bin/env python3
"""Check a closed month's dashboard figures against Anthropic's invoices.

Usage:
  python3 reconcile.py <workspace root> <YYYY-MM> [--seats 1540.00] [--overage 1448.69] [--api 195.28]

Pass the amounts from the invoices (before tax): --seats and --overage from the
claude.ai Team invoice (seat subscription line(s) and the extra-usage line),
--api from the Console invoice or usage page. Each surface the dashboard shows
is compared with its invoice line; any you leave out are listed but not judged.

A surface passes when it is within $1.00 or 0.5% of the invoice, whichever is
larger. Why that tolerance: seats are list price times headcount and should
match exactly unless someone was added or removed mid-month (proration);
overage comes from Anthropic's own spend export and API cost from its own cost
report, so anything beyond rounding means a real gap — a missed export, a
wrong roster, a key for the wrong organization.

Exit 0 when every judged surface passes, 1 otherwise. Read-only.
"""
from __future__ import annotations

import argparse, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_workbooks import load

ABSOLUTE_TOLERANCE = 1.00
RELATIVE_TOLERANCE = 0.005


def tolerance(invoice: float) -> float:
    return max(ABSOLUTE_TOLERANCE, abs(invoice) * RELATIVE_TOLERANCE)


def dashboard_figures(root: str, period: str) -> dict[str, float]:
    org, seats, thr, keymap, periods, b_rows, c_rows, meta, models, pipeline = load(root)
    if period not in periods:
        raise SystemExit(f"{period} isn't in the workspace (raw/{period}/ has no export or meta.json).")
    if meta[period]["partial"]:
        print(f"Note: {period} is marked partial ({meta[period]['days']} of {meta[period]['dim']} days); "
              "invoices cover whole months, so expect gaps until it is complete.")
    if period != periods[-1]:
        print("Note: seats are counted from today's roster; if seats changed since "
              f"{period}, expect a seat gap that the roster history would explain.")
    return {
        "seats": sum(s["monthly_rate"] for s in seats),
        "overage": sum(r["net_usd"] for r in b_rows if r["period"] == period),
        "api": sum(r["cost_usd"] for r in c_rows if r["period"] == period and r["record_type"] == "cost"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    parser.add_argument("period")
    parser.add_argument("--seats", type=float, help="Team invoice: seat subscription total, before tax")
    parser.add_argument("--overage", type=float, help="Team invoice: extra usage total, before tax")
    parser.add_argument("--api", type=float, help="Console: API usage total for the month, before tax")
    args = parser.parse_args()

    figures = dashboard_figures(args.root, args.period)
    invoices = {"seats": args.seats, "overage": args.overage, "api": args.api}
    labels = {"seats": "Committed seats", "overage": "Seat overage", "api": "API cost"}
    failed = False
    print(f"{'Surface':<17}{'Dashboard':>12}{'Invoice':>12}{'Gap':>10}  Result")
    for key, label in labels.items():
        mine, theirs = figures[key], invoices[key]
        if theirs is None:
            print(f"{label:<17}{mine:>12,.2f}{'—':>12}{'':>10}  not checked")
            continue
        gap = mine - theirs
        ok = abs(gap) <= tolerance(theirs)
        failed |= not ok
        print(f"{label:<17}{mine:>12,.2f}{theirs:>12,.2f}{gap:>+10,.2f}  {'pass' if ok else 'FAIL'}"
              + ("" if ok else f" (allowed ±{tolerance(theirs):,.2f})"))
    if failed:
        print("\nA failing surface usually means: seats — the roster's seat types or prices don't match billing, or "
              "someone joined or left mid-month; overage — the export for this month is incomplete; API cost — the "
              "Admin key (or Ramp's connection) is for a different Console organization.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
