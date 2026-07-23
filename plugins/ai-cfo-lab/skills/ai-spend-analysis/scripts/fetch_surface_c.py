#!/usr/bin/env python3
"""Surface C: Anthropic Admin API pull (usage_report/messages + cost_report).

Usage: python3 fetch_surface_c.py <workspace root> <YYYY-MM>

Reads the Admin API key from ANTHROPIC_ADMIN_API_KEY, falling back to the file
<root>/.secrets/anthropic_admin_key (gitignored). Graceful-missing: if no key is
found, writes status to raw/<period>/surface_c_status.json and exits 0 (the
pipeline proceeds; the dashboard shows 'Surface C not configured').

Never prints or persists the key. Read-only endpoints only.
"""
import csv, json, os, sys, urllib.request, urllib.parse, urllib.error
from calendar import monthrange

API = "https://api.anthropic.com"
VER = "2023-06-01"


def read_key(root):
    key = os.environ.get("ANTHROPIC_ADMIN_API_KEY", "").strip()
    if key:
        return key
    secret_file = os.path.join(root, ".secrets", "anthropic_admin_key")
    if os.path.exists(secret_file):
        return open(secret_file).read().strip()
    return ""


def status(out_dir, state, detail, rows=0):
    with open(os.path.join(out_dir, "surface_c_status.json"), "w") as fh:
        json.dump({"surface": "C", "state": state, "detail": detail, "rows": rows}, fh, indent=2)
    print(f"[surface_c] {state}: {detail}")


def get(path, params, key):
    url = f"{API}{path}?{urllib.parse.urlencode(params, doseq=True)}"
    req = urllib.request.Request(url, headers={"x-api-key": key, "anthropic-version": VER})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def paged(path, params, key):
    items, page = [], None
    while True:
        p = dict(params)
        if page:
            p["page"] = page
        data = get(path, p, key)
        items.extend(data.get("data", []))
        if not data.get("has_more"):
            return items
        page = data.get("next_page")


def main():
    root, period = sys.argv[1], sys.argv[2]
    out_dir = os.path.join(root, "raw", period)
    os.makedirs(out_dir, exist_ok=True)
    key = read_key(root)
    if not key:
        status(out_dir, "not_configured", "no Admin API key (ANTHROPIC_ADMIN_API_KEY / .secrets/anthropic_admin_key); skipping API-platform pull")
        return 0
    y, m = map(int, period.split("-"))
    start = f"{period}-01T00:00:00Z"
    end = f"{period}-{monthrange(y, m)[1]:02d}T23:59:59Z"
    rows = []
    try:
        usage = paged("/v1/organizations/usage_report/messages",
                      {"starting_at": start, "ending_at": end, "bucket_width": "1d",
                       "group_by[]": ["api_key_id", "workspace_id", "model", "service_tier"]}, key)
        for bucket in usage:
            for r in bucket.get("results", []):
                rows.append({"record_type": "usage", "date": bucket.get("starting_at", "")[:10],
                    "workspace_id": r.get("workspace_id") or "default", "api_key_id": r.get("api_key_id") or "",
                    "model": r.get("model") or "", "service_tier": r.get("service_tier") or "",
                    "uncached_input_tokens": r.get("uncached_input_tokens", 0),
                    "cache_read_tokens": r.get("cache_read_input_tokens", 0),
                    "cache_creation_tokens": (r.get("cache_creation", {}) or {}).get("ephemeral_5m_input_tokens", 0)
                                           + (r.get("cache_creation", {}) or {}).get("ephemeral_1h_input_tokens", 0),
                    "output_tokens": r.get("output_tokens", 0), "cost_usd": "", "description": ""})
        cost = paged("/v1/organizations/cost_report",
                     {"starting_at": start, "ending_at": end, "group_by[]": ["workspace_id", "description"]}, key)
        for bucket in cost:
            for r in bucket.get("results", []):
                amt = r.get("amount", {})
                cents = float(amt.get("amount", 0)) if isinstance(amt, dict) else float(amt or 0)
                rows.append({"record_type": "cost", "date": bucket.get("starting_at", "")[:10],
                    "workspace_id": r.get("workspace_id") or "default", "api_key_id": "", "model": "",
                    "service_tier": "", "uncached_input_tokens": "", "cache_read_tokens": "",
                    "cache_creation_tokens": "", "output_tokens": "",
                    "cost_usd": round(cents / 100.0, 6), "description": r.get("description") or ""})
    except urllib.error.HTTPError as e:
        status(out_dir, "error", f"HTTP {e.code} from Admin API ({'auth problem' if e.code in (401,403) else 'request failed'})")
        return 0
    except Exception as e:
        status(out_dir, "error", f"{type(e).__name__}: {e}")
        return 0
    out = os.path.join(out_dir, "api_usage_cost.csv")
    cols = ["record_type","date","workspace_id","api_key_id","model","service_tier","uncached_input_tokens",
            "cache_read_tokens","cache_creation_tokens","output_tokens","cost_usd","description"]
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
    status(out_dir, "ok", f"pulled {len(rows)} rows for {period}", len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
