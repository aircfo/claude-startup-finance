#!/usr/bin/env python3
"""Build ai_spend_sources.xlsx and ai_spend_output.xlsx from /raw + /config.

Idempotent: fully regenerates both workbooks from the raw monthly folders each
run (the /raw tree is the append-only audit trail; the sources workbook mirrors
it 1:1). Always writes workbooks/build_summary.json.

openpyxl is OPTIONAL. Without it, this script still computes every period, row,
and flag and writes build_summary.json (which the dashboard and Slack draft are
built from) — it only skips the two .xlsx files. Install it (`pip install
openpyxl`) to get the Excel workbooks.

This module also hosts load()/compute_flags() and the model-family helpers that
build_artifact.py and draft_slack.py import, so it must import cleanly even when
openpyxl is absent.

Usage: python3 build_workbooks.py <workspace root>
"""
import csv, json, os, re, sys
from calendar import monthrange

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    HAVE_OPENPYXL = True
except ImportError:
    openpyxl = None
    HAVE_OPENPYXL = False

# Number formats are plain strings (no openpyxl needed to define them).
ARIAL = "Arial"
MONEY = "$#,##0.00;($#,##0.00);-"
PCT = "0.0%"
INT = "#,##0"
# Style objects require openpyxl; they are only referenced by the workbook
# builders, which never run when openpyxl is absent.
if HAVE_OPENPYXL:
    BLUE = Font(name=ARIAL, color="0000FF")
    YELLOW = PatternFill("solid", fgColor="FFFF00")
    HDR = Font(name=ARIAL, bold=True)


# --- model-family helpers (config-driven; replaces the v1 hardcoded opus|fable) ---

def frontier_regex(models):
    """Compiled regex for the frontier family's model-name pattern."""
    name = models.get("frontier_family", "frontier")
    fam = next((f for f in models.get("families", []) if f.get("name") == name), None)
    pattern = (fam or {}).get("pattern") or r"(?!x)x"  # match nothing if unset
    return re.compile(pattern, re.I)


def family_classifier(models):
    """Return classify(model_name) -> family name. First family whose pattern
    matches wins; a family with an empty pattern is the catch-all (must be last)."""
    compiled = [
        (fam.get("name", "other"),
         re.compile(fam["pattern"], re.I) if fam.get("pattern") else None)
        for fam in models.get("families", [])
    ]

    def classify(model_name):
        for name, rx in compiled:
            if rx is None:  # catch-all family
                return name
            if rx.search(model_name or ""):
                return name
        return "other"

    return classify


def sonnet_reference_cpr(models):
    """The Sonnet-class family's reference cost/request fallback for the what-if."""
    name = models.get("sonnet_family", "sonnet")
    fam = next((f for f in models.get("families", []) if f.get("name") == name), None)
    return float((fam or {}).get("reference_cpr_usd", 0.003))


def read_csv(path):
    with open(path) as fh:
        return list(csv.DictReader(fh))


def f(v):
    try:
        return float(v or 0)
    except ValueError:
        return 0.0


def load(root):
    cfg = os.path.join(root, "config")
    org = {r["email"].lower(): r for r in read_csv(os.path.join(cfg, "org_chart.csv"))}
    seats = read_csv(os.path.join(cfg, "seats.csv"))
    thr = json.load(open(os.path.join(cfg, "thresholds.json")))
    models = json.load(open(os.path.join(cfg, "models.json")))
    pipeline_path = os.path.join(cfg, "pipeline.json")
    pipeline = json.load(open(pipeline_path)) if os.path.exists(pipeline_path) else {}
    keymap_path = os.path.join(cfg, "api_key_map.csv")
    keymap = ({r["api_key_id"]: r for r in read_csv(keymap_path)}
              if os.path.exists(keymap_path) and os.path.getsize(keymap_path) > 60 else {})
    periods, b_rows, c_rows, meta = [], [], [], {}
    rawdir = os.path.join(root, "raw")
    for p in sorted(os.listdir(rawdir)) if os.path.isdir(rawdir) else []:
        pdir = os.path.join(rawdir, p)
        bfile = os.path.join(pdir, "overage_spend.csv")
        has_b = os.path.exists(bfile)
        has_meta = os.path.exists(os.path.join(pdir, "meta.json"))
        if not (re.match(r"\d{4}-\d{2}$", p) and (has_b or has_meta)):
            continue
        periods.append(p)
        m, meta_status = {}, "missing"
        if has_meta:
            try:
                m = json.load(open(os.path.join(pdir, "meta.json")))
                meta_status = "ok"
            except (json.JSONDecodeError, OSError) as e:
                print(f"[workbooks] meta.json invalid for {p}: {e} — treating as missing")
                meta_status = f"invalid: {e}"
        y, mo = map(int, p.split("-"))
        meta[p] = {"days": m.get("days_covered", monthrange(y, mo)[1]),
                   "dim": monthrange(y, mo)[1], "partial": m.get("partial", False),
                   "meta_status": meta_status}
        for r in (read_csv(bfile) if has_b else []):
            em = r["user_email"].lower().strip()
            o = org.get(em, {})
            b_rows.append({"period": p, "email": em, "name": o.get("name", ""),
                "department": o.get("department") or "(unmapped)",
                "product": r["product"], "model": r["model"], "requests": f(r["total_requests"]),
                "prompt_tokens": f(r["total_prompt_tokens"]), "completion_tokens": f(r["total_completion_tokens"]),
                "net_usd": f(r["total_net_spend_usd"]), "gross_usd": f(r["total_gross_spend_usd"])})
        cfile = os.path.join(pdir, "api_usage_cost.csv")
        if os.path.exists(cfile):
            for r in read_csv(cfile):
                km = keymap.get(r.get("api_key_id", ""), {})
                c_rows.append({"period": p, **{k: r.get(k, "") for k in ("record_type","date","workspace_id","api_key_id","model")},
                    "owner_email": km.get("owner_email", ""), "cost_usd": f(r.get("cost_usd")), "output_tokens": f(r.get("output_tokens"))})
    for s in seats:
        s["email"] = s["email"].lower()
        o = org.get(s["email"], {})
        s["name"], s["department"] = o.get("name", ""), o.get("department") or "(unmapped)"
        s["monthly_rate"] = f(s["monthly_rate"])
    return org, seats, thr, keymap, periods, b_rows, c_rows, meta, models, pipeline


def sheet_table(ws, rows, cols, fmts=None):
    for j, c in enumerate(cols, 1):
        ws.cell(1, j, c).font = HDR
    for i, r in enumerate(rows, 2):
        for j, c in enumerate(cols, 1):
            cell = ws.cell(i, j, r.get(c, ""))
            cell.font = Font(name=ARIAL)
            if fmts and c in fmts:
                cell.number_format = fmts[c]
    ws.freeze_panes = "A2"
    for j, c in enumerate(cols, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = max(12, min(28, len(c) + 4))


def build_sources(root, seats, periods, b_rows, c_rows):
    wb = openpyxl.Workbook(); wb.remove(wb.active)
    sheet_table(wb.create_sheet("B_overage"), b_rows,
        ["period","email","name","department","product","model","requests","prompt_tokens","completion_tokens","net_usd","gross_usd"],
        {"net_usd": MONEY, "gross_usd": MONEY, "requests": INT, "prompt_tokens": INT, "completion_tokens": INT})
    sheet_table(wb.create_sheet("C_api"), c_rows,
        ["period","record_type","date","workspace_id","api_key_id","owner_email","model","output_tokens","cost_usd"],
        {"cost_usd": MONEY, "output_tokens": INT})
    sheet_table(wb.create_sheet("A_seats"), seats, ["email","name","department","seat_type","monthly_rate"], {"monthly_rate": MONEY})
    wb.save(os.path.join(root, "workbooks", "ai_spend_sources.xlsx"))


def compute_flags(thr, seats, periods, b_rows, c_rows, keymap):
    flags = []
    by_user_period, by_user_tokens = {}, {}
    for r in b_rows:
        by_user_period[(r["email"], r["period"])] = by_user_period.get((r["email"], r["period"]), 0) + r["net_usd"]
        by_user_tokens[(r["email"], r["period"])] = by_user_tokens.get((r["email"], r["period"]), 0) + r["prompt_tokens"] + r["completion_tokens"]
    with_data = {r["period"] for r in b_rows}
    fulls = [p for p in periods if p in with_data][:-1] if periods else []
    look = fulls[-thr["reclaim_months_lookback"]:] if len(fulls) >= thr["reclaim_months_lookback"] else fulls
    std_rate = thr["standard_seat_rate_usd"]
    for s in seats:
        em = s["email"]
        if look and all(by_user_tokens.get((em, p), 0) < thr["reclaim_tokens_floor"] for p in look):
            flags.append({"flag": "reclaim_candidate", "subject": em,
                "detail": f"under {thr['reclaim_tokens_floor']/1e6:.0f}M tokens in each of last {len(look)} full months",
                "est_monthly_saving_usd": s["monthly_rate"]})
        if s["seat_type"] == "premium" and fulls:
            lastfull = fulls[-1]
            util = by_user_period.get((em, lastfull), 0)
            if util < thr["premium_utilization_floor_usd"]:
                flags.append({"flag": "premium_underutilized", "subject": em,
                    "detail": f"${util:.0f} overage in {lastfull} vs ${thr['premium_utilization_floor_usd']:.0f} floor",
                    "est_monthly_saving_usd": s["monthly_rate"] - std_rate})
    n = thr["consistent_overage_months"]
    dperiods = [p for p in periods if p in with_data]
    if len(dperiods) >= n:
        lastn = dperiods[-n:]
        for em in {r["email"] for r in b_rows}:
            if all(by_user_period.get((em, p), 0) >= thr["consistent_overage_floor_usd"] for p in lastn):
                flags.append({"flag": "consistent_overage", "subject": em,
                    "detail": f">= ${thr['consistent_overage_floor_usd']:.0f} overage {n} periods running — check config/runaway automation",
                    "est_monthly_saving_usd": ""})
    seen = set()
    for r in c_rows:
        kid = r["api_key_id"]
        if kid and kid not in seen and not (keymap.get(kid, {}) or {}).get("owner_email"):
            seen.add(kid)
            name = (keymap.get(kid, {}) or {}).get("purpose", "")
            flags.append({"flag": "unowned_api_key", "subject": f"{name or kid}",
                "detail": f"API key with spend but no owner_email in api_key_map.csv ({kid}) — governance gap", "est_monthly_saving_usd": ""})
    bp = {}
    for r in b_rows:
        bp[(r["product"], r["period"])] = bp.get((r["product"], r["period"]), 0) + r["net_usd"]
    for prod in {r["product"] for r in b_rows}:
        for a, b in zip(periods, periods[1:]):
            pa, pb = bp.get((prod, a), 0), bp.get((prod, b), 0)
            if pa >= 1 and pb >= thr["spike_min_usd"] and (pb - pa) / pa * 100 >= thr["spike_mom_pct"]:
                flags.append({"flag": "product_spike", "subject": prod,
                    "detail": f"${pa:.0f} -> ${pb:.0f} ({a} -> {b})" + (" [partial month]" if b == periods[-1] else ""),
                    "est_monthly_saving_usd": ""})
    return flags


def build_output(root, org, seats, thr, keymap, periods, b_rows, c_rows, meta, company, flags):
    wb = openpyxl.Workbook(); wb.remove(wb.active)
    nb = len(b_rows) + 1
    # Config
    ws = wb.create_sheet("Config")
    ws["A1"], ws["A1"].font = "Thresholds (edit in config/thresholds.json; shown here for reference)", HDR
    row = 2
    for k, v in thr.items():
        if k.endswith("_note"):
            continue
        ws.cell(row, 1, k).font = Font(name=ARIAL)
        c = ws.cell(row, 2, v if not isinstance(v, list) else ", ".join(str(x) for x in v)); c.font = BLUE; c.fill = YELLOW
        row += 1
    ws.cell(row + 1, 1, "Period coverage").font = HDR
    ws.cell(row + 2, 1, "period").font = HDR; ws.cell(row + 2, 2, "days_covered").font = HDR
    ws.cell(row + 2, 3, "days_in_month").font = HDR; ws.cell(row + 2, 4, "partial").font = HDR
    prow = {}
    for i, p in enumerate(periods):
        rr = row + 3 + i; prow[p] = rr
        for j, v in enumerate([p, meta[p]["days"], meta[p]["dim"], str(meta[p]["partial"])], 1):
            ws.cell(rr, j, v).font = Font(name=ARIAL)
    ws.column_dimensions["A"].width = 34; ws.column_dimensions["B"].width = 16
    # FACT tabs (values = raw joined data)
    sheet_table(wb.create_sheet("FACT_B"), b_rows,
        ["period","email","name","department","product","model","requests","prompt_tokens","completion_tokens","net_usd","gross_usd"],
        {"net_usd": MONEY, "gross_usd": MONEY, "requests": INT, "prompt_tokens": INT, "completion_tokens": INT})
    sheet_table(wb.create_sheet("FACT_C"), c_rows,
        ["period","record_type","date","workspace_id","api_key_id","owner_email","model","output_tokens","cost_usd"],
        {"cost_usd": MONEY, "output_tokens": INT})
    sheet_table(wb.create_sheet("SEATS"), seats, ["email","name","department","seat_type","monthly_rate"], {"monthly_rate": MONEY})
    ns, nc = len(seats) + 1, max(len(c_rows) + 1, 2)
    # Summary (formulas)
    ws = wb.create_sheet("Summary", 0)
    ws["A1"], ws["A1"].font = f"{company} AI Spend — Summary (committed vs variable vs API cash)", HDR
    labels = ["Committed seat cost (cash)", "Variable overage (usage credits)", "API cash (Console/platform)",
              "Total", "Total MoM Δ%", "Overage run-rate forecast (full month)", "Days covered / days in month"]
    for i, lab in enumerate(labels):
        ws.cell(3 + i, 1, lab).font = Font(name=ARIAL, bold=(lab == "Total"))
    for j, p in enumerate(periods):
        col = openpyxl.utils.get_column_letter(2 + j)
        ws.cell(2, 2 + j, p + (" (partial)" if meta[p]["partial"] else "")).font = HDR
        ws[f"{col}3"] = f"=SUM(SEATS!$E$2:$E${ns})"
        ws[f"{col}4"] = f'=SUMIFS(FACT_B!$J$2:$J${nb},FACT_B!$A$2:$A${nb},"{p}")'
        ws[f"{col}5"] = f'=SUMIFS(FACT_C!$I$2:$I${nc},FACT_C!$A$2:$A${nc},"{p}",FACT_C!$B$2:$B${nc},"cost")'
        ws[f"{col}6"] = f"=SUM({col}3:{col}5)"
        if j:
            ws[f"{col}7"] = f"=IFERROR(({col}6-{openpyxl.utils.get_column_letter(1+j)}6)/{openpyxl.utils.get_column_letter(1+j)}6,\"\")"
        ws[f"{col}8"] = f"={col}4/Config!$B${prow[p]}*Config!$C${prow[p]}"
        ws[f"{col}9"] = f'=Config!$B${prow[p]}&" / "&Config!$C${prow[p]}'
        for rr, fmt in ((3, MONEY), (4, MONEY), (5, MONEY), (6, MONEY), (7, PCT), (8, MONEY)):
            ws[f"{col}{rr}"].number_format = fmt; ws[f"{col}{rr}"].font = Font(name=ARIAL, bold=(rr == 6))
    ws.column_dimensions["A"].width = 40
    note = ws.cell(11, 1, "Committed = seats.csv rates (constant until seats change). Overage = FACT_B net spend (usage credits beyond allotments; in-allotment usage is $0 by design). API cash = FACT_C cost records. Sources: raw/<period>/ exports; org_chart.csv.")
    note.font = Font(name=ARIAL, italic=True, size=9)
    # ByPerson
    ws = wb.create_sheet("ByPerson")
    emails = sorted({r["email"] for r in b_rows}, key=lambda e: -sum(r["net_usd"] for r in b_rows if r["email"] == e))
    hdrs = ["email", "name", "department", "seat_type", "seat_rate"] + periods + ["total_overage", "fully_loaded_latest_full_mo"]
    for j, h in enumerate(hdrs, 1):
        ws.cell(1, j, h).font = HDR
    lastfull = ([p for p in periods if not meta[p]["partial"]] or periods)[-1]
    for i, em in enumerate(emails, 2):
        o = org.get(em, {})
        ws.cell(i, 1, em).font = Font(name=ARIAL)
        ws.cell(i, 2, o.get("name", "")).font = Font(name=ARIAL)
        ws.cell(i, 3, o.get("department") or "(unmapped)").font = Font(name=ARIAL)
        ws.cell(i, 4, f"=IFERROR(INDEX(SEATS!$D$2:$D${ns},MATCH(A{i},SEATS!$A$2:$A${ns},0)),\"?\")").font = Font(name=ARIAL)
        ws.cell(i, 5, f"=IFERROR(INDEX(SEATS!$E$2:$E${ns},MATCH(A{i},SEATS!$A$2:$A${ns},0)),0)").number_format = MONEY
        for j, p in enumerate(periods):
            c = ws.cell(i, 6 + j, f'=SUMIFS(FACT_B!$J$2:$J${nb},FACT_B!$A$2:$A${nb},"{p}",FACT_B!$B$2:$B${nb},$A{i})')
            c.number_format = MONEY; c.font = Font(name=ARIAL)
        tc = openpyxl.utils.get_column_letter(5 + len(periods))
        ws.cell(i, 6 + len(periods), f"=SUM(F{i}:{tc}{i})").number_format = MONEY
        lcol = openpyxl.utils.get_column_letter(6 + periods.index(lastfull))
        ws.cell(i, 7 + len(periods), f"=E{i}+{lcol}{i}").number_format = MONEY
    ws.freeze_panes = "A2"

    # ByDept / ByProduct / ByModel via SUMIFS
    def dim_sheet(name, col_letter, keys, extra=None):
        ws = wb.create_sheet(name)
        hdrs = [name.replace("By", "").lower()] + periods + ["total"] + (extra or [])
        for j, h in enumerate(hdrs, 1):
            ws.cell(1, j, h).font = HDR
        for i, k in enumerate(keys, 2):
            ws.cell(i, 1, k).font = Font(name=ARIAL)
            for j, p in enumerate(periods):
                c = ws.cell(i, 2 + j, f'=SUMIFS(FACT_B!$J$2:$J${nb},FACT_B!$A$2:$A${nb},"{p}",FACT_B!${col_letter}$2:${col_letter}${nb},$A{i})')
                c.number_format = MONEY; c.font = Font(name=ARIAL)
            tc = openpyxl.utils.get_column_letter(1 + len(periods))
            ws.cell(i, 2 + len(periods), f"=SUM(B{i}:{tc}{i})").number_format = MONEY
        ws.freeze_panes = "A2"; ws.column_dimensions["A"].width = 26
        return ws

    depts = sorted({r["department"] for r in b_rows})
    dws = dim_sheet("ByDept", "D", depts, ["active_users_latest"])
    actives = {}
    for r in b_rows:
        if r["period"] == periods[-1] and (r["prompt_tokens"] or r["completion_tokens"]):
            actives.setdefault(r["department"], set()).add(r["email"])
    for i, d in enumerate(depts, 2):
        c = dws.cell(i, 3 + len(periods), len(actives.get(d, set()))); c.font = Font(name=ARIAL); c.number_format = INT
    dws.cell(1, 3 + len(periods)).value = f"active_users_{periods[-1]}"
    dim_sheet("ByProduct", "E", sorted({r["product"] for r in b_rows}))
    mws = dim_sheet("ByModel", "F", sorted({r["model"] for r in b_rows}), ["requests", "cost_per_request"])
    for i, m in enumerate(sorted({r["model"] for r in b_rows}), 2):
        rq = mws.cell(i, 3 + len(periods), f'=SUMIFS(FACT_B!$G$2:$G${nb},FACT_B!$F$2:$F${nb},$A{i})'); rq.number_format = INT; rq.font = Font(name=ARIAL)
        rc, tc = openpyxl.utils.get_column_letter(3 + len(periods)), openpyxl.utils.get_column_letter(2 + len(periods))
        cp = mws.cell(i, 4 + len(periods), f"=IFERROR({tc}{i}/{rc}{i},0)"); cp.number_format = "$0.0000"; cp.font = Font(name=ARIAL)
    # Flags
    sheet_table(wb.create_sheet("Flags"), flags, ["flag","subject","detail","est_monthly_saving_usd"], {"est_monthly_saving_usd": MONEY})
    wb["Flags"].column_dimensions["C"].width = 70
    wb.save(os.path.join(root, "workbooks", "ai_spend_output.xlsx"))


def main():
    root = sys.argv[1]
    org, seats, thr, keymap, periods, b_rows, c_rows, meta, models, pipeline = load(root)
    if not periods:
        print("[workbooks] no raw periods found"); return 1
    os.makedirs(os.path.join(root, "workbooks"), exist_ok=True)
    company = pipeline.get("company_name") or "AI Spend"
    flags = compute_flags(thr, seats, periods, b_rows, c_rows, keymap)
    summary = {"company": company, "periods": periods, "b_rows": len(b_rows), "c_rows": len(c_rows),
               "flags": len(flags), "flag_list": [{k: fl[k] for k in ("flag", "subject")} for fl in flags]}
    meta_alerts = {p: meta[p]["meta_status"] for p in periods if meta[p]["meta_status"].startswith("invalid")}
    if meta_alerts:
        summary["meta_alerts"] = meta_alerts
    if HAVE_OPENPYXL:
        build_sources(root, seats, periods, b_rows, c_rows)
        build_output(root, org, seats, thr, keymap, periods, b_rows, c_rows, meta, company, flags)
        summary["workbooks"] = "built"
    else:
        summary["workbooks"] = "skipped — openpyxl not installed (pip install openpyxl for the .xlsx workbooks)"
        print("[workbooks] openpyxl not installed — wrote build_summary.json and skipped .xlsx; dashboard/Slack draft still build")
    json.dump(summary, open(os.path.join(root, "workbooks", "build_summary.json"), "w"), indent=2)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
