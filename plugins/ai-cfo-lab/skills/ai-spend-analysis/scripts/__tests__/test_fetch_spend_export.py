"""The export script's choices that don't need a browser: which days to fetch, and what counts as an export."""
from __future__ import annotations

import datetime
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import fetch_spend_export as export  # noqa: E402

day = datetime.date


class SpansTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name)

    def saved(self, start: str, end: str) -> None:
        month = self.folder / "raw" / start[:7]
        month.mkdir(parents=True, exist_ok=True)
        (month / f"{export.SOURCE}_{start}_{end}_saved-20261101T090000Z.csv").write_text("user_email\n")

    def test_fetches_this_month_from_the_1st_through_yesterday(self) -> None:
        self.saved("2026-09-01", "2026-09-30")

        self.assertEqual(export.spans_to_fetch(self.folder, day(2026, 10, 15)), [(day(2026, 10, 1), day(2026, 10, 14))])

    def test_on_the_1st_it_fetches_the_whole_month_just_ended(self) -> None:
        self.saved("2026-10-01", "2026-10-30")

        self.assertEqual(export.spans_to_fetch(self.folder, day(2026, 11, 1)), [(day(2026, 10, 1), day(2026, 10, 31))])

    def test_finishes_last_month_first_when_its_newest_export_stops_short(self) -> None:
        self.saved("2026-10-01", "2026-10-29")

        self.assertEqual(
            export.spans_to_fetch(self.folder, day(2026, 11, 4)),
            [(day(2026, 10, 1), day(2026, 10, 31)), (day(2026, 11, 1), day(2026, 11, 3))],
        )

    def test_a_folder_with_no_saved_export_starts_with_this_month(self) -> None:
        self.assertEqual(export.spans_to_fetch(self.folder, day(2026, 11, 4)), [(day(2026, 11, 1), day(2026, 11, 3))])


class ExportTest(unittest.TestCase):
    def test_an_export_has_the_email_and_net_spend_columns(self) -> None:
        self.assertTrue(export.looks_like_export("user_email,account_uuid,model,total_net_spend_usd\nx,y,z,1\n"))
        self.assertFalse(export.looks_like_export("<!DOCTYPE html><html>Sign in</html>"))

    def test_the_request_names_the_org_and_both_days(self) -> None:
        url = export.export_url("org-123", (day(2026, 10, 1), day(2026, 10, 14)))

        self.assertEqual(
            url,
            "https://claude.ai/api/organizations/org-123/analytics/spend-report-export"
            "?start_date=2026-10-01&end_date=2026-10-14",
        )


if __name__ == "__main__":
    unittest.main()
