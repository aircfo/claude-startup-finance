"""The dashboard page builder: the engine's data goes into the page whole, and can't break out of it."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_dashboard_page as builder  # noqa: E402

TEMPLATE = "<title>__TITLE__</title><main></main><script type=\"application/json\" id=\"spend-data\">__DASHBOARD_JSON__</script>"


def dashboard(company: str = "Acme", month: str = "2026-10") -> dict[str, object]:
    return {"about": {"company": company, "month": month}, "spend": {"total_cents": 53000}, "notes": []}


def embedded(page: str) -> object:
    start = page.index('id="spend-data">') + len('id="spend-data">')
    return json.loads(page[start:page.index("</script>", start)])


class BuildPageTest(unittest.TestCase):
    def test_puts_the_data_in_the_page_unchanged(self) -> None:
        data = dashboard()

        page = builder.build_page(data, TEMPLATE)

        self.assertEqual(embedded(page), data)
        self.assertIn("<title>Acme AI spend</title>", page)

    def test_a_value_cannot_close_the_script_that_holds_it(self) -> None:
        data = dashboard()
        data["notes"] = ["</script><script>alert(1)</script>"]

        page = builder.build_page(data, TEMPLATE)

        self.assertEqual(page.count("</script>"), 1)
        self.assertEqual(embedded(page), data)

    def test_the_company_name_is_text_in_the_title(self) -> None:
        page = builder.build_page(dashboard(company="Smith & Sons <West>"), TEMPLATE)

        self.assertIn("<title>Smith &amp; Sons &lt;West&gt; AI spend</title>", page)

    def test_the_shipped_template_has_one_place_for_the_data(self) -> None:
        page = builder.build_page(dashboard(), builder.TEMPLATE.read_text(encoding="utf-8"))

        self.assertNotIn(builder.DATA_SLOT, page)
        self.assertNotIn(builder.TITLE_SLOT, page)


class FolderTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name)

    def save(self, month: str) -> None:
        path = self.folder / "out" / month / "dashboard.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(dashboard(month=month)), encoding="utf-8")

    def test_writes_the_page_beside_the_newest_months_data(self) -> None:
        self.save("2026-09")
        self.save("2026-10")

        builder.main([str(self.folder)])

        page = (self.folder / "out/2026-10/dashboard.html").read_text(encoding="utf-8")
        self.assertEqual(embedded(page)["about"]["month"], "2026-10")
        self.assertFalse((self.folder / "out/2026-09/dashboard.html").exists())

    def test_says_what_to_run_when_there_is_no_data(self) -> None:
        with self.assertRaises(SystemExit) as refused:
            builder.main([str(self.folder), "2026-10"])

        self.assertIn("run the engine's `dashboard 2026-10` first", str(refused.exception))


if __name__ == "__main__":
    unittest.main()
