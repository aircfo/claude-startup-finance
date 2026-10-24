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
# PASTE_ADMIN_KEY_HERE.txt / admin_key.txt = transient key drop (moved into .secrets/, then deleted)
# .browser-profile/ = the claude.ai login the daily export fetch uses
# dashboard/ + logs/ = per-run uploads and scheduled-job logs
.secrets/
.browser-profile/
dashboard/
logs/
PASTE_ADMIN_KEY_HERE.txt
admin_key.txt
raw/
workbooks/
artifacts/
config/
# To version only non-PII tuning, un-ignore it explicitly, e.g. add:
#   !config/thresholds.json
#   !config/models.json
"""

DROP_FILE = "PASTE_ADMIN_KEY_HERE.txt"
# Pre-created so the operator supplies the optional Admin API key by editing a file
# (secure_key.py moves it into .secrets/ and deletes it) rather than pasting it in
# chat. No literal sk-ant- token here — instructions only.
DROP_TEXT = """\
HOW TO ADD YOUR ANTHROPIC ADMIN API KEY  (optional — only for API / Console spend)

1. Get an Admin key at console.anthropic.com > Settings > Admin keys
   (you must be an Organization Owner or Admin).
2. Paste the whole key on its own line below, replacing this instruction text.
   It begins with sk-ant- and is a long string. Paste only the key — no quotes,
   no label.
3. Save and close this file.

On the next run the skill reads the key, stores it securely in .secrets/ (locked to
your user and gitignored), and DELETES this file. Your key is never written to chat,
logs, config, the workbook, or the dashboard.

Don't need API / Console spend tracked? Delete this file (or leave it as-is) — the
dashboard will simply show "Surface C not configured".

----- paste your key below this line -----
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
    drop = os.path.join(root, DROP_FILE)
    if not os.path.exists(drop) and not os.path.exists(os.path.join(root, ".secrets", "anthropic_admin_key")):
        with open(drop, "w") as fh:
            fh.write(DROP_TEXT)
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
    if os.path.exists(drop):
        print(f"  wrote {DROP_FILE} — optional: paste an Admin API key there to track API/Console spend (secured to .secrets/ + deleted on first run)")
    if seeded:
        print(f"  seeded config from templates: {', '.join(seeded)}")
    else:
        print("  config/ already populated — left untouched")
    print("  Next: your assistant walks you through setup — company, seat prices, your")
    print("  roster (bootstrapped from your first spend export), and (optionally) an API key.")
    print("  You mostly confirm; nothing here needs hand-editing or terminal commands.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
