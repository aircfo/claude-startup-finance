#!/usr/bin/env python3
"""Scaffold a fresh AI-Spend workspace. Usage: python3 scaffold.py <workspace root>

Creates the folder tree (raw/ workbooks/ artifacts/ config/ .secrets/) and, only
if config/ has no files yet, seeds it from the skill's config.example/ templates
so the operator edits real values rather than starting from a blank folder.
Never overwrites an existing config file. Idempotent."""
import os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXAMPLE = os.path.join(HERE, "..", "config.example")
DIRS = ["raw", "workbooks", "artifacts", "config", ".secrets"]

# A workspace holds real per-employee spend and API keys. If the operator ever
# version-controls it, none of that must be committable. Seed a .gitignore so
# the safe default is automatic.
GITIGNORE = """# AI-Spend workspace — never commit real spend data or secrets.
# (gitignore treats a whole line as the pattern; comments must be on their own line.)
# .secrets/  = API keys
# raw/       = real monthly exports (per-person spend) + append-only audit trail
# workbooks/ + artifacts/ = regenerated every run (the dashboard names individuals)
# config/    = your roster (org_chart.csv / seats.csv are real people)
.secrets/
raw/
workbooks/
artifacts/
config/
# To version only non-PII tuning, un-ignore it explicitly, e.g. add:
#   !config/thresholds.json
#   !config/models.json
"""


def main():
    if len(sys.argv) != 2:
        print(__doc__); return 2
    root = os.path.abspath(sys.argv[1])
    for d in DIRS:
        os.makedirs(os.path.join(root, d), exist_ok=True)
    gitignore = os.path.join(root, ".gitignore")
    if not os.path.exists(gitignore):
        with open(gitignore, "w") as fh:
            fh.write(GITIGNORE)
    cfg = os.path.join(root, "config")
    seeded = []
    if os.path.isdir(EXAMPLE):
        for name in sorted(os.listdir(EXAMPLE)):
            src, dst = os.path.join(EXAMPLE, name), os.path.join(cfg, name)
            if os.path.isfile(src) and not os.path.exists(dst):
                shutil.copyfile(src, dst)
                seeded.append(name)
    print(f"✓ Workspace ready at {root}")
    print(f"  dirs: {', '.join(DIRS)}")
    print("  wrote .gitignore (keeps real spend data + secrets out of version control)")
    if seeded:
        print(f"  seeded config from templates: {', '.join(seeded)}")
        print("  → edit config/pipeline.json (company_name, plan_tier, org_id), seats.csv, org_chart.csv before the first run")
    else:
        print("  config/ already populated — left untouched")
    print("  → put the monthly seat-overage export at raw/<YYYY-MM>/overage_spend.csv, then: python3 scripts/run_pipeline.py <root> <YYYY-MM>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
