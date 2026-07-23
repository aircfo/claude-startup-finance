#!/usr/bin/env python3
"""Build the self-contained interactive HTML artifact from /raw + /config.
Usage: python3 build_artifact.py <workspace root>
No secrets, no network calls in the output; data embedded as JSON at build time.
Company name and model-family colors/labels are read from config (pipeline.json /
models.json), so the artifact carries no hardcoded brand or model generation."""
import datetime, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_workbooks import load, family_classifier, frontier_regex, sonnet_reference_cpr


def surface_status(root, period):
    out = {}
    for s, fn in (("B", "surface_b_status.json"), ("C", "surface_c_status.json")):
        p = os.path.join(root, "raw", period, fn)
        out[s] = json.load(open(p)) if os.path.exists(p) else {"state": "unknown", "detail": "no status file"}
    return out


def main():
    root = sys.argv[1]
    org, seats, thr, keymap, periods, b_rows, c_rows, meta, models, pipeline = load(root)
    if not periods:
        print("[artifact] no raw periods found"); return 1
    os.makedirs(os.path.join(root, "artifacts"), exist_ok=True)
    latest = periods[-1]
    company = pipeline.get("company_name") or "AI Spend"
    classify = family_classifier(models)
    frx = frontier_regex(models)
    frontier_products = set(thr.get("frontier_share_products", []))

    users = {}
    for r in b_rows:
        u = users.setdefault(r["email"], {"email": r["email"], "name": r["name"], "dept": r["department"],
            "spend": {}, "tokens": {}, "products": {}, "cw_frontier_usd": 0.0, "cw_frontier_req": 0.0, "cw_total_usd": 0.0})
        u["spend"][r["period"]] = u["spend"].get(r["period"], 0) + r["net_usd"]
        u["tokens"][r["period"]] = u["tokens"].get(r["period"], 0) + r["prompt_tokens"] + r["completion_tokens"]
        pp = u["products"].setdefault(r["product"], {})
        pp[r["period"]] = pp.get(r["period"], 0) + r["net_usd"]
        if r["product"] in frontier_products:
            u["cw_total_usd"] += r["net_usd"]
            if frx.search(r["model"]):
                u["cw_frontier_usd"] += r["net_usd"]; u["cw_frontier_req"] += r["requests"]
    for s in seats:
        u = users.get(s["email"])
        if u:
            u["seat_type"], u["seat_rate"] = s["seat_type"], s["monthly_rate"]
        else:
            users[s["email"]] = {"email": s["email"], "name": s["name"], "dept": s["department"], "spend": {}, "tokens": {},
                "products": {}, "cw_frontier_usd": 0, "cw_frontier_req": 0, "cw_total_usd": 0, "seat_type": s["seat_type"], "seat_rate": s["monthly_rate"]}

    prod, model, pm = {}, {}, {}
    for r in b_rows:
        prod.setdefault(r["product"], {})[r["period"]] = prod.setdefault(r["product"], {}).get(r["period"], 0) + r["net_usd"]
        m = model.setdefault(r["model"], {"spend": 0, "req": 0}); m["spend"] += r["net_usd"]; m["req"] += r["requests"]
        fam = pm.setdefault(r["product"], {}).setdefault(classify(r["model"]), {"spend": 0.0, "req": 0.0})
        fam["spend"] += r["net_usd"]; fam["req"] += r["requests"]

    # Cost records are keyed by workspace (no api_key dimension), so attribute
    # workspace -> dept via the owners of that workspace's keys in api_key_map.csv.
    ws_depts = {}
    for kid, km in (keymap or {}).items():
        owner = (km.get("owner_email") or "").lower()
        if not owner:
            continue
        dept = org.get(owner, {}).get("department") or "(unmapped)"
        ws_depts.setdefault(km.get("workspace_id") or "default", set()).add(dept)
    api_by_dept = {}
    for r in c_rows:
        if r["record_type"] != "cost":
            continue
        ds = ws_depts.get(r.get("workspace_id") or "default", set())
        dept = list(ds)[0] if len(ds) == 1 else ("(API — mixed-owner workspace)" if ds else "(API — unassigned keys)")
        api_by_dept[dept] = api_by_dept.get(dept, 0) + r["cost_usd"]
    api = {}
    for r in c_rows:
        if r["record_type"] == "cost":
            api[r["period"]] = api.get(r["period"], 0) + r["cost_usd"]

    families = [{"name": fam.get("name", "other"), "label": fam.get("label", fam.get("name", "other")),
                 "color": fam.get("color", "#e5e7eb")} for fam in models.get("families", [])]
    data = {"generated": datetime.date.today().isoformat(), "company": company, "periods": periods,
        "meta": meta, "latest": latest, "committed": sum(s["monthly_rate"] for s in seats),
        "seat_count": len(seats), "api": api, "thr": thr, "status": surface_status(root, latest),
        "families": families, "frontierFamily": models.get("frontier_family", "frontier"),
        "sonnetFamily": models.get("sonnet_family", "sonnet"), "sonnetRefCpr": sonnet_reference_cpr(models),
        "users": sorted(users.values(), key=lambda u: -sum(u["spend"].values())),
        "products": prod, "productModel": pm, "apiByDept": api_by_dept,
        "models": [{"model": k, **v} for k, v in sorted(model.items(), key=lambda x: -x[1]["spend"])]}

    tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifact_template.html")).read()
    html = tpl.replace("/*__DATA__*/", "const DATA = " + json.dumps(data) + ";")
    out = os.path.join(root, "artifacts", f"{latest}_ai_spend.html")
    open(out, "w").write(html)
    print(f"[artifact] wrote {out} ({len(html)//1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
