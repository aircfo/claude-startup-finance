#!/usr/bin/env python3
"""Surface B for ENTERPRISE plans: the documented Analytics API.

Usage: python3 fetch_surface_b_enterprise.py <workspace root> <YYYY-MM>

On Enterprise (plan_tier == "enterprise"), the seat-overage data comes from the
documented Analytics API instead of the Team plan's browser/manual export — no
browser, no 90-day window, per-user and programmatic. This fetcher pulls it and
writes raw/<period>/overage_spend.csv in the SAME schema the Team export
produces, so everything downstream (validate/workbooks/artifact) is untouched.

╔══════════════════════════════════════════════════════════════════════════╗
║  UNTESTED against a live Enterprise org. Built from the public docs        ║
║  (platform.claude.com/docs/en/manage-claude/analytics-api). Validation is  ║
║  an open roadmap work item — see references/dashboard-guide.md. The exact  ║
║  endpoint path and response field names may differ; both are overridable   ║
║  from config/pipeline.json (surface_b_enterprise_path / *_fields) WITHOUT  ║
║  editing this file. On any shape mismatch it FAILS LOUD (status "error")    ║
║  and fabricates nothing.                                                    ║
╚══════════════════════════════════════════════════════════════════════════╝

Auth: ANTHROPIC_ANALYTICS_API_KEY (an Analytics API key with the read:analytics
scope), falling back to the file <root>/.secrets/anthropic_analytics_key.
Never prints or persists the key. Read-only.
"""
import csv, json, os, sys, urllib.request, urllib.parse, urllib.error
from calendar import monthrange

API = "https://api.anthropic.com"
VER = "2023-06-01"
DEFAULT_PATH = "/v1/organizations/analytics/usage_report/spend"  # override via config if the docs differ

# Output columns — the Team spend-export schema. Downstream only reads the first
# eight (plus user_id); the rest are carried for schema fidelity when available.
OUT_COLS = ["user_email", "account_uuid", "product", "model", "total_requests",
            "total_prompt_tokens", "total_completion_tokens", "total_net_spend_usd",
            "total_gross_spend_usd", "user_id", "total_uncached_input_tokens",
            "total_cache_read_tokens", "total_cache_write_5m_tokens",
            "total_cache_write_1h_tokens", "total_web_search_count", "slack_channel_id"]

# Tolerant field resolution: each output column maps to a list of candidate
# source keys (the docs' exact names are unverified). Overridable via
# pipeline.json -> surface_b_enterprise_fields (a {out_col: [candidates]} map).
DEFAULT_FIELD_MAP = {
    "user_email": ["user_email", "actor_email", "email"],
    "user_id": ["user_id", "actor_id"],
    "account_uuid": ["account_uuid", "organization_id", "org_id"],
    "product": ["product", "surface", "app"],
    "model": ["model", "model_id"],
    "total_requests": ["total_requests", "requests", "message_count"],
    "total_prompt_tokens": ["total_prompt_tokens", "prompt_tokens", "input_tokens"],
    "total_completion_tokens": ["total_completion_tokens", "completion_tokens", "output_tokens"],
    "total_net_spend_usd": ["total_net_spend_usd", "net_spend_usd", "net_cost_usd", "cost_usd"],
    "total_gross_spend_usd": ["total_gross_spend_usd", "gross_spend_usd", "gross_cost_usd"],
}


def read_key(root):
    key = os.environ.get("ANTHROPIC_ANALYTICS_API_KEY", "").strip()
    if key:
        return key
    secret_file = os.path.join(root, ".secrets", "anthropic_analytics_key")
    if os.path.exists(secret_file):
        return open(secret_file).read().strip()
    return ""


def status(out_dir, state, detail, rows=0):
    with open(os.path.join(out_dir, "surface_b_status.json"), "w") as fh:
        json.dump({"surface": "B", "state": state, "detail": detail, "rows": rows, "source": "enterprise_analytics_api"}, fh, indent=2)
    print(f"[surface_b_enterprise] {state}: {detail}")


def pick(record, candidates):
    for k in candidates:
        if k in record and record[k] not in (None, ""):
            return record[k]
    return ""


def paged(path, params, key):
    items, page = [], None
    while True:
        p = dict(params)
        if page:
            p["page"] = page
        url = f"{API}{path}?{urllib.parse.urlencode(p, doseq=True)}"
        req = urllib.request.Request(url, headers={"x-api-key": key, "anthropic-version": VER})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.load(r)
        # Accept a few plausible container shapes without guessing beyond them.
        chunk = data.get("data") or data.get("results") or (data if isinstance(data, list) else [])
        items.extend(chunk)
        if not data.get("has_more"):
            return items
        page = data.get("next_page")


def main():
    root, period = sys.argv[1], sys.argv[2]
    out_dir = os.path.join(root, "raw", period)
    os.makedirs(out_dir, exist_ok=True)
    key = read_key(root)
    if not key:
        status(out_dir, "missing", "no Analytics API key (ANTHROPIC_ANALYTICS_API_KEY / .secrets/anthropic_analytics_key) — Enterprise Surface B not fetched")
        return 0
    cfg_path = os.path.join(root, "config", "pipeline.json")
    cfg = json.load(open(cfg_path)) if os.path.exists(cfg_path) else {}
    path = cfg.get("surface_b_enterprise_path", DEFAULT_PATH)
    field_map = {**DEFAULT_FIELD_MAP, **(cfg.get("surface_b_enterprise_fields") or {})}
    y, m = map(int, period.split("-"))
    params = {"starting_at": f"{period}-01T00:00:00Z",
              "ending_at": f"{period}-{monthrange(y, m)[1]:02d}T23:59:59Z",
              "group_by[]": ["actor", "product", "model"]}
    try:
        records = paged(path, params, key)
    except urllib.error.HTTPError as e:
        hint = "auth/scope problem (needs read:analytics)" if e.code in (401, 403) else \
               "endpoint not found — verify surface_b_enterprise_path against the current docs" if e.code == 404 else "request failed"
        status(out_dir, "error", f"HTTP {e.code} from Analytics API ({hint})")
        return 0
    except Exception as e:
        status(out_dir, "error", f"{type(e).__name__}: {e}")
        return 0

    rows = []
    for rec in records:
        if not isinstance(rec, dict):
            continue
        row = {c: "" for c in OUT_COLS}
        for out_col, candidates in field_map.items():
            row[out_col] = pick(rec, candidates)
        rows.append(row)

    # Fail loud on a shape mismatch rather than writing a plausible-but-wrong file.
    usable = [r for r in rows if r["user_email"] and "@" in str(r["user_email"])]
    if not usable:
        status(out_dir, "error",
               "Analytics API returned rows but none mapped to a user_email — the response shape likely "
               "differs from this build. Set surface_b_enterprise_fields in pipeline.json to the real field "
               "names and re-run. Nothing was written.")
        return 0

    out = os.path.join(out_dir, "overage_spend.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=OUT_COLS)
        w.writeheader(); w.writerows(rows)
    # meta.json so the period registers even before validation runs.
    json.dump({"period": period, "start": params["starting_at"], "end": params["ending_at"],
               "days_covered": monthrange(y, m)[1], "partial": False,
               "source": "enterprise analytics api"}, open(os.path.join(out_dir, "meta.json"), "w"), indent=2)
    print(f"[surface_b_enterprise] wrote {len(rows)} rows -> {out} (UNTESTED path — verify totals against the admin console)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
