#!/usr/bin/env python3
"""Generate the synthetic AI-Spend fixture dataset (deterministic, seeded).

Usage: python3 make_fixtures.py [target_dir]   (default: this script's directory)

Produces a fake company ("Northwind Analytics", ~20 @example.com users, 5
departments) with a 3-month spend history engineered to exercise every flag and
panel the pipeline computes:

  - concentration (a few heavy users dominate overage)
  - a partial latest month (2026-06, 20/30 days) -> run-rate forecast bar
  - a zero-usage premium seat (Rosalind) -> reclaim + premium_underutilized
  - a departed user (Dennis: spend in 04/05, none in 06, seat already reclaimed)
  - frontier-heavy chat users (what-if routing panel has something to move)
  - a product spike (Agents: $30 -> $95 month over month) -> product_spike
  - a consistently-over user (Ada, >= $50 every month) -> consistent_overage
  - a synthetic Surface-C api_usage_cost.csv incl. an unmapped key -> unowned_api_key
    and an unassigned-workspace API bucket

Contains ZERO real data — every email is @example.com, every name invented.
Regenerating with the same seed reproduces byte-identical output."""
import csv, json, os, random, sys
from calendar import monthrange

HERE = os.path.dirname(os.path.abspath(__file__))
RNG = random.Random(42)

MONTHS = ["2026-04", "2026-05", "2026-06"]  # 06 is the partial latest month
PARTIAL_DAYS = {"2026-06": 20}
FRONTIER, SONNET, HAIKU = "claude-opus-4-1", "claude-sonnet-4-5", "claude-haiku-4"
CPR = {FRONTIER: 0.032, SONNET: 0.008, HAIKU: 0.0022}  # rough cost/request per family

# email, name, department, seat_type ("" = no seat), monthly overage per MONTHS,
# frontier share of that overage, products it spreads across.
USERS = [
    ("ada@example.com",       "Ada Lovelace",       "Engineering", "premium",  [220, 255, 165], 0.75, ["Chat", "Cowork"]),
    ("alan@example.com",      "Alan Turing",        "Engineering", "standard", [180, 205, 130], 0.65, ["Chat", "Cowork"]),
    ("grace@example.com",     "Grace Hopper",       "Engineering", "premium",  [150, 175, 120], 0.55, ["Chat", "Code"]),
    ("linus@example.com",     "Linus Torvalds",     "Engineering", "standard", [30, 95, 60],    0.40, ["Agents"]),        # sole "Agents" user -> clean product_spike (30 -> 95)
    ("margaret@example.com",  "Margaret Hamilton",  "Engineering", "standard", [22, 26, 17],    0.30, ["Cowork"]),
    ("dennis@example.com",    "Dennis Ritchie",     "Engineering", "",         [60, 55, 0],     0.50, ["Chat"]),          # departed: seat reclaimed, no 06 spend
    ("steve@example.com",     "Steve Wozniak",      "Product",     "premium",  [80, 92, 60],    0.60, ["Chat", "Cowork"]),
    ("radia@example.com",     "Radia Perlman",      "Product",     "standard", [30, 34, 22],    0.35, ["Cowork"]),
    ("barbara@example.com",   "Barbara Liskov",     "Product",     "standard", [45, 52, 33],    0.45, ["Chat"]),
    ("donald@example.com",    "Donald Knuth",       "Product",     "standard", [18, 20, 13],    0.25, ["Chat"]),
    ("katherine@example.com", "Katherine Johnson",  "Sales",       "premium",  [70, 60, 44],    0.50, ["Chat"]),          # premium, dips below floor in 05 windowing
    ("john@example.com",      "John von Neumann",   "Sales",       "standard", [55, 62, 40],    0.40, ["Chat"]),
    ("hedy@example.com",      "Hedy Lamarr",        "Sales",       "standard", [12, 14, 9],     0.20, ["Chat"]),
    ("claude@example.com",    "Claude Shannon",     "Sales",       "standard", [8, 10, 6],      0.20, ["Chat"]),
    ("leonhard@example.com",  "Leonhard Euler",     "Finance",     "standard", [16, 19, 12],    0.30, ["Cowork"]),
    ("carl@example.com",      "Carl Gauss",         "Finance",     "standard", [9, 11, 7],      0.20, ["Chat"]),
    ("emmy@example.com",      "Emmy Noether",       "Finance",     "standard", [14, 17, 11],    0.30, ["Cowork"]),
    ("nikola@example.com",    "Nikola Tesla",       "Operations",  "standard", [11, 13, 8],     0.25, ["Chat"]),
    ("marie@example.com",     "Marie Curie",        "Operations",  "standard", [7, 8, 5],       0.15, ["Chat"]),
    ("rosalind@example.com",  "Rosalind Franklin",  "Operations",  "premium",  [0, 0, 0],       0.00, []),                # zero-usage premium seat
]

MANAGER = {"Engineering": "grace@example.com", "Product": "steve@example.com",
           "Sales": "katherine@example.com", "Finance": "leonhard@example.com",
           "Operations": "nikola@example.com"}


def spend_rows(user, month, month_factor):
    """Emit overage_spend rows for one user in one month."""
    email, name, dept, seat, overage, frontier, products = user
    idx = MONTHS.index(month)
    total = overage[idx] * month_factor
    if total <= 0 or not products:
        return []
    rows, per_product = [], total / len(products)
    for product in products:
        # frontier portion -> opus row; remainder split sonnet/haiku 70/30
        buckets = [(FRONTIER, per_product * frontier),
                   (SONNET, per_product * (1 - frontier) * 0.7),
                   (HAIKU, per_product * (1 - frontier) * 0.3)]
        for model, net in buckets:
            if net < 0.5:
                continue
            requests = max(1, round(net / CPR[model] * RNG.uniform(0.9, 1.1)))
            prompt_tokens = requests * RNG.randint(1200, 1800)
            completion_tokens = requests * RNG.randint(300, 700)
            rows.append({
                "user_email": email, "account_uuid": "acct-northwind", "product": product,
                "model": model, "total_requests": requests,
                "total_prompt_tokens": prompt_tokens, "total_completion_tokens": completion_tokens,
                "total_net_spend_usd": round(net, 2), "total_gross_spend_usd": round(net * 1.05, 2),
                "user_id": "u_" + email.split("@")[0],
                "total_uncached_input_tokens": prompt_tokens, "total_cache_read_tokens": 0,
                "total_cache_write_5m_tokens": 0, "total_cache_write_1h_tokens": 0,
                "total_web_search_count": 0, "slack_channel_id": ""})
    return rows


OVERAGE_COLS = ["user_email", "account_uuid", "product", "model", "total_requests",
                "total_prompt_tokens", "total_completion_tokens", "total_net_spend_usd",
                "total_gross_spend_usd", "user_id", "total_uncached_input_tokens",
                "total_cache_read_tokens", "total_cache_write_5m_tokens",
                "total_cache_write_1h_tokens", "total_web_search_count", "slack_channel_id"]

API_COLS = ["record_type", "date", "workspace_id", "api_key_id", "model", "service_tier",
            "uncached_input_tokens", "cache_read_tokens", "cache_creation_tokens",
            "output_tokens", "cost_usd", "description"]

# Surface C cost per month: workspace -> cost_usd. wrkspc_main is owner-mapped
# (Engineering); wrkspc_rogue has no mapped keys (-> unassigned bucket).
API_COST = {"2026-04": {"wrkspc_main": 95.0}, "2026-05": {"wrkspc_main": 120.0, "wrkspc_rogue": 35.0},
            "2026-06": {"wrkspc_main": 60.0}}


def write_csv(path, cols, rows):
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)


def main():
    target = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else HERE
    cfg, raw = os.path.join(target, "config"), os.path.join(target, "raw")
    os.makedirs(cfg, exist_ok=True)

    # --- config ---
    write_csv(os.path.join(cfg, "org_chart.csv"),
              ["email", "name", "department", "team", "manager", "cost_center"],
              [{"email": u[0], "name": u[1], "department": u[2], "team": "",
                "manager": MANAGER.get(u[2], ""), "cost_center": "CC-" + u[2][:3].upper()} for u in USERS])
    write_csv(os.path.join(cfg, "seats.csv"), ["email", "seat_type", "monthly_rate"],
              [{"email": u[0], "seat_type": u[3], "monthly_rate": 200 if u[3] == "premium" else 30}
               for u in USERS if u[3]])
    write_csv(os.path.join(cfg, "api_key_map.csv"),
              ["api_key_id", "workspace_id", "owner_email", "purpose"],
              [{"api_key_id": "apikey_MAIN0001", "workspace_id": "wrkspc_main", "owner_email": "ada@example.com", "purpose": "Production backend"},
               {"api_key_id": "apikey_MAIN0002", "workspace_id": "wrkspc_main", "owner_email": "alan@example.com", "purpose": "Data pipeline"}])
    json.dump({
        "company_name": "Northwind Analytics", "plan_tier": "team", "org_id": "example-org-id-0000",
        "timezone": "America/New_York", "run_day": "3rd of month",
        "surface_b_endpoint": "/api/organizations/{org_id}/analytics/spend-report-export?start_date={start}&end_date={end}",
        "surface_b_method": "MANUAL EXPORT (fixture data — synthetic)",
        "surface_b_requires": "n/a for fixtures", "notes": "synthetic fixture config — not real"
    }, open(os.path.join(cfg, "pipeline.json"), "w"), indent=2)
    json.dump({
        "standard_seat_rate_usd": 30.0, "premium_utilization_floor_usd": 100.0,
        "reclaim_tokens_floor": 1000000, "reclaim_months_lookback": 2,
        "consistent_overage_months": 3, "consistent_overage_floor_usd": 50.0,
        "frontier_share_products": ["Chat", "Cowork"], "spike_mom_pct": 100, "spike_min_usd": 50.0
    }, open(os.path.join(cfg, "thresholds.json"), "w"), indent=2)
    json.dump({
        "families": [
            {"name": "frontier", "label": "Frontier (top-tier)", "pattern": "opus|fable", "color": "#1e3a8a"},
            {"name": "sonnet", "label": "Mid (Sonnet-class)", "pattern": "sonnet", "color": "#60a5fa", "reference_cpr_usd": 0.008},
            {"name": "haiku", "label": "Small (Haiku-class)", "pattern": "haiku", "color": "#bfdbfe"},
            {"name": "other", "label": "Other", "pattern": "", "color": "#e5e7eb"}],
        "frontier_family": "frontier", "sonnet_family": "sonnet"
    }, open(os.path.join(cfg, "models.json"), "w"), indent=2)

    # --- raw monthly folders ---
    for month in MONTHS:
        mdir = os.path.join(raw, month)
        os.makedirs(mdir, exist_ok=True)
        y, m = map(int, month.split("-"))
        dim = monthrange(y, m)[1]
        days = PARTIAL_DAYS.get(month, dim)
        partial = month in PARTIAL_DAYS
        factor = (days / dim) if partial else 1.0
        rows = []
        for user in USERS:
            rows.extend(spend_rows(user, month, factor))
        write_csv(os.path.join(mdir, "overage_spend.csv"), OVERAGE_COLS, rows)
        json.dump({"period": month, "start": f"{month}-01", "end": f"{month}-{days:02d}",
                   "days_covered": days, "partial": partial, "source": "synthetic fixture"},
                  open(os.path.join(mdir, "meta.json"), "w"), indent=2)

        # Surface C (synthetic): usage rows (incl. an unmapped rogue key) + cost rows
        api_rows = [
            {"record_type": "usage", "date": f"{month}-05", "workspace_id": "wrkspc_main",
             "api_key_id": "apikey_MAIN0001", "model": FRONTIER, "service_tier": "standard",
             "uncached_input_tokens": 2_000_000, "cache_read_tokens": 500_000,
             "cache_creation_tokens": 0, "output_tokens": 400_000, "cost_usd": "", "description": ""},
            {"record_type": "usage", "date": f"{month}-06", "workspace_id": "wrkspc_rogue",
             "api_key_id": "apikey_ROGUE9999", "model": SONNET, "service_tier": "standard",
             "uncached_input_tokens": 800_000, "cache_read_tokens": 0,
             "cache_creation_tokens": 0, "output_tokens": 150_000, "cost_usd": "", "description": ""},
        ]
        for wsid, cost in API_COST[month].items():
            api_rows.append({"record_type": "cost", "date": f"{month}-28", "workspace_id": wsid,
                             "api_key_id": "", "model": "", "service_tier": "", "uncached_input_tokens": "",
                             "cache_read_tokens": "", "cache_creation_tokens": "", "output_tokens": "",
                             "cost_usd": cost, "description": "API usage"})
        write_csv(os.path.join(mdir, "api_usage_cost.csv"), API_COLS, api_rows)
        # A successful Surface C fetch would have written this; the smoke test can't
        # reach the Admin API, so the fixture ships the "ok" status directly.
        json.dump({"surface": "C", "state": "ok",
                   "detail": f"synthetic fixture — {len(api_rows)} rows", "rows": len(api_rows)},
                  open(os.path.join(mdir, "surface_c_status.json"), "w"), indent=2)

    print(f"✓ fixtures written to {target} ({len(MONTHS)} months, {len(USERS)} users)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
