#!/usr/bin/env python3
"""Write the engine's people.csv from the seats roster people edit.

Usage:
  python3 roster_to_people.py <folder> <roster rows file> [--compare <claude.ai spend export>]

The roster is a Claude Doc with one row per person: name, email, team, and a seat column
per vendor. Claude reads its table and writes the rows to a JSON file:

  {"rows": [{"name": "Pat Lee", "email": "pat@acme.com", "team": "Sales",
             "seats": {"anthropic": "Standard", "openai": "No account"}}]}

This writes <folder>/people.csv: one row per seat held. A seat type must be one the
settings file prices. Name and team are written only where the engine can't get them from
Ramp's newest people list: for someone Ramp doesn't know, or a team that differs from
Ramp's. That way a team changed in Ramp still flows through for everyone else.

With --compare, it also lists who the roster gives a Claude seat but the export doesn't
show using Claude, and who the export shows but the roster lacks. The export lists everyone
who used Claude in its period, $0 included, so no member list is needed.
"""
from __future__ import annotations

import csv
import io
import json
import os
import sys
from collections import Counter
from collections.abc import Sequence
from pathlib import Path

NO_SEAT = {"", "no account", "none", "no seat"}
PEOPLE_COLUMNS = ("email", "name", "team", "vendor", "seat_type")


class RosterError(Exception):
    """Something in the roster to fix before people.csv can be written."""


def people_rows(
    roster: object, priced: dict[str, set[str]], ramp_people: dict[str, tuple[str, str]]
) -> tuple[list[dict[str, str]], list[str]]:
    """people.csv's rows, and a plain summary of what they hold.

    priced maps each vendor to the seat types settings has prices for; ramp_people maps a
    lowercase email to (name, team) from Ramp's newest people list.
    """
    rows = roster.get("rows") if isinstance(roster, dict) else None
    if not isinstance(rows, list):
        raise RosterError('the roster file should hold {"rows": [ ... ]}')
    problems: list[str] = []
    out: list[dict[str, str]] = []
    held: Counter[tuple[str, str]] = Counter()
    seen: set[str] = set()
    for number, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            problems.append(f"row {number} isn't a person")
            continue
        email = str(row.get("email") or "").strip().lower()
        if not email or "@" not in email:
            problems.append(f"row {number} has no email")
            continue
        if email in seen:
            problems.append(f"{email} is on the roster twice")
            continue
        seen.add(email)
        name = str(row.get("name") or "").strip()
        team = str(row.get("team") or "").strip()
        seats = row.get("seats") if isinstance(row.get("seats"), dict) else {}
        for vendor, value in sorted(seats.items()):
            seat = str(value or "").strip().lower()
            if seat in NO_SEAT:
                continue
            vendor = str(vendor).strip().lower()
            if seat not in priced.get(vendor, set()):
                known = ", ".join(sorted(priced.get(vendor, set()))) or "none yet"
                problems.append(f"{email} has a {vendor} seat {value!r}, but settings price only: {known}")
                continue
            in_ramp = email in ramp_people
            ramp_team = ramp_people[email][1] if in_ramp else ""
            out.append({
                "email": email,
                "name": "" if in_ramp else name,
                "team": "" if in_ramp and team.casefold() == ramp_team.casefold() else team,
                "vendor": vendor,
                "seat_type": seat,
            })
            held[(vendor, seat)] += 1
    if problems:
        raise RosterError("fix these in the roster: " + "; ".join(problems))
    summary = [f"{vendor} {seat}: {count} held" for (vendor, seat), count in sorted(held.items())]
    missing = sorted({row["email"] for row in out if row["email"] not in ramp_people})
    if missing:
        summary.append(f"not in Ramp, so their name and team come from the roster: {', '.join(missing)}")
    return out, summary


def compare_with_export(roster: object, export_emails: set[str]) -> list[str]:
    """Lines naming roster people with a Claude seat the export doesn't show, and export people the roster lacks."""
    rows = roster.get("rows") if isinstance(roster, dict) else None
    with_seat: set[str] = set()
    on_roster: set[str] = set()
    for row in rows if isinstance(rows, list) else []:
        if not isinstance(row, dict):
            continue
        email = str(row.get("email") or "").strip().lower()
        on_roster.add(email)
        seats = row.get("seats") if isinstance(row.get("seats"), dict) else {}
        if str(seats.get("anthropic") or "").strip().lower() not in NO_SEAT:
            with_seat.add(email)
    lines = []
    idle = sorted(with_seat - export_emails)
    if idle:
        lines.append(f"Claude seat on the roster, but not in the export: {', '.join(idle)}")
    missing = sorted(export_emails - on_roster)
    if missing:
        lines.append(f"In the export, but not on the roster: {', '.join(missing)}")
    return lines or ["The roster's Claude seats match the export."]


def export_emails(path: Path) -> set[str]:
    with path.open(encoding="utf-8-sig", newline="") as export:
        return {
            row["user_email"].strip().lower()
            for row in csv.DictReader(export)
            if (row.get("user_email") or "").strip()
        }


def priced_seats(folder: Path) -> dict[str, set[str]]:
    settings = json.loads((folder / "aicfo-spend.json").read_text(encoding="utf-8"))
    seats = settings.get("seats") if isinstance(settings, dict) else None
    if not isinstance(seats, dict):
        return {}
    return {
        str(vendor).lower(): {str(seat).lower() for seat in plans}
        for vendor, plans in seats.items()
        if isinstance(plans, dict)
    }


def newest_ramp_people(folder: Path) -> dict[str, tuple[str, str]]:
    """Ramp's newest saved people list, as lowercase email -> (name, team)."""
    snapshots = sorted((folder / "raw").glob("*/ramp-people_*.json"), key=lambda path: path.name)
    if not snapshots:
        return {}
    document = json.loads(snapshots[-1].read_text(encoding="utf-8-sig"))
    people: dict[str, tuple[str, str]] = {}
    for user in document.get("users", []) if isinstance(document, dict) else []:
        if not isinstance(user, dict) or not isinstance(user.get("email"), str):
            continue
        name = " ".join(str(user.get(part) or "").strip() for part in ("first_name", "last_name")).strip()
        people[user["email"].strip().lower()] = (name, str(user.get("department_name") or "").strip())
    return people


def write_people_csv(folder: Path, rows: list[dict[str, str]]) -> Path:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=PEOPLE_COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    path = folder / "people.csv"
    # Written beside the final name, then renamed, so the engine never reads half a file.
    partial = path.with_suffix(".csv.partial")
    partial.write_text(buffer.getvalue(), encoding="utf-8")
    os.replace(partial, path)
    return path


def main(argv: Sequence[str]) -> int:
    if len(argv) not in (2, 4) or (len(argv) == 4 and argv[2] != "--compare"):
        raise SystemExit(__doc__)
    folder, roster_file = Path(argv[0]).expanduser(), Path(argv[1]).expanduser()
    roster = json.loads(roster_file.read_text(encoding="utf-8"))
    try:
        rows, summary = people_rows(roster, priced_seats(folder), newest_ramp_people(folder))
    except RosterError as error:
        raise SystemExit(f"roster_to_people: {error}") from None
    path = write_people_csv(folder, rows)
    print(f"Wrote {path} ({len(rows)} seats)")
    for line in summary:
        print(f"  {line}")
    if len(argv) == 4:
        for line in compare_with_export(roster, export_emails(Path(argv[3]).expanduser())):
            print(f"  {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
