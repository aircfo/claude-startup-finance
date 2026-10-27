#!/usr/bin/env python3
"""Turn the engine's dashboard data into one self-contained page to publish.

Usage:
  python3 build_dashboard_page.py <folder> [YYYY-MM]

Reads <folder>/out/<month>/dashboard.json, which `aicfo-spend dashboard` writes, and
writes <folder>/out/<month>/dashboard.html: the page template with that data inside it.
The page needs nothing else, and no number is retyped on the way. Without a month, it
uses the newest month that has dashboard data.
"""
from __future__ import annotations

import html
import json
import sys
from collections.abc import Sequence
from pathlib import Path

TEMPLATE = Path(__file__).with_name("dashboard_page.html")
DATA_SLOT = "__DASHBOARD_JSON__"
TITLE_SLOT = "__TITLE__"


def build_page(dashboard: object, template: str) -> str:
    """The template with the page title and the data filled in."""
    head, slot, tail = template.partition(DATA_SLOT)
    if not slot or DATA_SLOT in tail:
        raise SystemExit(f"build_dashboard_page: the template needs exactly one {DATA_SLOT}")
    about = dashboard.get("about") if isinstance(dashboard, dict) else None
    company = about.get("company") if isinstance(about, dict) else ""
    title = html.escape(f"{company} AI spend" if company else "AI spend")
    # Every "<" in the data becomes <, which JSON reads back as "<", so no value can
    # close the <script> that holds it.
    payload = json.dumps(dashboard, ensure_ascii=False).replace("<", "\\u003c")
    return head.replace(TITLE_SLOT, title, 1) + payload + tail


def dashboard_data(folder: Path, month: str | None) -> Path:
    if month:
        path = folder / "out" / month / "dashboard.json"
        if not path.is_file():
            raise SystemExit(f"build_dashboard_page: no {path}; run the engine's `dashboard {month}` first")
        return path
    found = sorted((folder / "out").glob("*/dashboard.json"))
    if not found:
        raise SystemExit(f"build_dashboard_page: no dashboard data in {folder / 'out'}; run the engine's `dashboard` first")
    return found[-1]


def main(argv: Sequence[str]) -> int:
    if not 1 <= len(argv) <= 2:
        raise SystemExit(__doc__)
    folder = Path(argv[0]).expanduser()
    source = dashboard_data(folder, argv[1] if len(argv) == 2 else None)
    page = build_page(json.loads(source.read_text(encoding="utf-8")), TEMPLATE.read_text(encoding="utf-8"))
    target = source.with_name("dashboard.html")
    target.write_text(page, encoding="utf-8")
    print(f"Wrote {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
