#!/usr/bin/env python3
"""Ingest an Admin API key the operator dropped as a plain file.

Usage: secure_key.py <workspace root>

Instead of pasting a key into chat, the operator saves it into a visible drop file
in the workspace root — `PASTE_ADMIN_KEY_HERE.txt` (or `admin_key.txt`). This reads
that file, extracts the `sk-ant-…` key, writes it to `.secrets/anthropic_admin_key`
(chmod 600, gitignored), and deletes the drop file. The key travels file → file
only — it never appears in a command, a log, or the chat.

No-op (exit 0) when there is no drop file, so it is safe to run on every pipeline.
Prints a masked confirmation (last four characters only); never prints the key.
"""
import os, re, stat, sys

DROP_NAMES = ["PASTE_ADMIN_KEY_HERE.txt", "admin_key.txt"]
# Real Anthropic keys run ~90+ chars after the prefix; the {20,} floor keeps the
# regex from matching the literal "sk-ant-" that appears in instructional text.
KEY_RE = re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}")


def main():
    root = sys.argv[1]
    drop = next((os.path.join(root, n) for n in DROP_NAMES
                 if os.path.exists(os.path.join(root, n))), None)
    if not drop:
        return 0

    text = open(drop, encoding="utf-8", errors="ignore").read()
    match = KEY_RE.search(text)
    if not match:
        print(f"[key] found {os.path.basename(drop)} but no Anthropic key in it — "
              f"paste the whole sk-ant-… string into that file and re-run.", file=sys.stderr)
        return 0

    key = match.group(0)
    secrets_dir = os.path.join(root, ".secrets")
    os.makedirs(secrets_dir, exist_ok=True)
    dest = os.path.join(secrets_dir, "anthropic_admin_key")
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(key)
    os.chmod(dest, stat.S_IRUSR | stat.S_IWUSR)  # 0600 — owner read/write only
    os.remove(drop)
    print(f"[key] stored the Admin key in .secrets/anthropic_admin_key (600) and removed "
          f"{os.path.basename(drop)}. Key ends …{key[-4:]}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
