#!/usr/bin/env python3
"""Draft the short Slack summary (never sends). Usage: draft_slack.py <workspace root>
Writes artifacts/<latest>_slack_draft.txt and prints it. The operator delivers it
themselves — this script has no Slack access and sends nothing."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_workbooks import load, compute_flags


def main():
    root = sys.argv[1]
    org, seats, thr, keymap, periods, b_rows, c_rows, meta, models, pipeline = load(root)
    if not periods:
        print("[slack] no raw periods found"); return 1
    os.makedirs(os.path.join(root, "artifacts"), exist_ok=True)
    latest = periods[-1]
    committed = sum(s["monthly_rate"] for s in seats)
    ov = sum(r["net_usd"] for r in b_rows if r["period"] == latest)
    api = sum(r["cost_usd"] for r in c_rows if r["period"] == latest and r["record_type"] == "cost")
    total = committed + ov + api
    prev = periods[-2] if len(periods) > 1 else None
    lines = []
    # line 1: fetch failures first (per spec — fail loud, never a silent gap)
    fails = []
    for sname, fn in (("Surface B (seat overage)", "surface_b_status.json"), ("Surface C (API platform)", "surface_c_status.json")):
        sp = os.path.join(root, "raw", latest, fn)
        st = json.load(open(sp)) if os.path.exists(sp) else {"state": "unknown"}
        if st["state"] not in ("ok",):
            fails.append(f"{sname}: {st['state']}")
    if fails:
        lines.append("⚠️ Data gaps this cycle — " + "; ".join(fails))
    if prev:
        pt = committed + sum(r["net_usd"] for r in b_rows if r["period"] == prev) + sum(r["cost_usd"] for r in c_rows if r["period"] == prev and r["record_type"] == "cost")
        delta = f" ({'+' if total >= pt else ''}{(total - pt) / pt * 100:.0f}% vs {prev})" if pt else ""
    else:
        delta = ""
    partial = " (partial month)" if meta[latest]["partial"] else ""
    lines.append(f"AI spend {latest}{partial}: ${total:,.0f} total — ${committed:,.0f} seats + ${ov:,.0f} overage + ${api:,.0f} API{delta}.")
    flags = compute_flags(thr, seats, periods, b_rows, c_rows, keymap)
    savers = sorted([fl for fl in flags if fl.get("est_monthly_saving_usd")], key=lambda fl: -fl["est_monthly_saving_usd"])[:3]
    for fl in savers:
        lines.append(f"• {fl['flag']}: {fl['subject']} — {fl['detail']} (~${fl['est_monthly_saving_usd']:,.0f}/mo)")
    lines.append(f"Full breakdown: artifacts/{latest}_ai_spend.html")
    txt = "\n".join(lines)
    open(os.path.join(root, "artifacts", f"{latest}_slack_draft.txt"), "w").write(txt)
    print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
