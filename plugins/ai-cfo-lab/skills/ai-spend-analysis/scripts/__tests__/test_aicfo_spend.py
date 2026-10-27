"""The engine launcher: download once, check the fingerprint, run offline after.

Run from the skill folder: python3 -m unittest discover -s scripts/__tests__
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import aicfo_spend  # noqa: E402

# A stand-in engine: it records the command line it was given, so a test can see it ran.
FAKE_MAIN = (
    "import json, sys\n"
    "from pathlib import Path\n"
    "Path(sys.argv[2], 'ran.json').write_text(json.dumps(sys.argv[1:]))\n"
)


def fake_wheel() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as wheel:
        wheel.writestr("aicfo_spend/__init__.py", "")
        wheel.writestr("aicfo_spend/__main__.py", FAKE_MAIN)
    return buffer.getvalue()


class Downloads:
    def __init__(self, content: bytes) -> None:
        self.content = content
        self.urls: list[str] = []

    def __call__(self, url: str) -> bytes:
        self.urls.append(url)
        return self.content


class LauncherTest(unittest.TestCase):
    def setUp(self) -> None:
        self.wheel = fake_wheel()
        pinned = mock.patch.object(aicfo_spend, "WHEEL_SHA256", hashlib.sha256(self.wheel).hexdigest())
        pinned.start()
        self.addCleanup(pinned.stop)
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name) / "acme"
        self.folder.mkdir()

    def test_runs_the_command_with_the_folder_after_it(self) -> None:
        status = aicfo_spend.main([str(self.folder), "report", "2026-09"], Downloads(self.wheel))

        self.assertEqual(status, 0)
        ran = json.loads((self.folder / "ran.json").read_text())
        self.assertEqual(ran, ["report", str(self.folder), "2026-09"])

    def test_downloads_the_engine_once_then_runs_offline(self) -> None:
        downloads = Downloads(self.wheel)

        aicfo_spend.main([str(self.folder), "settings"], downloads)
        aicfo_spend.main([str(self.folder), "settings"], downloads)

        self.assertEqual(downloads.urls, [aicfo_spend.WHEEL_URL])

    def test_refuses_a_download_that_does_not_match_the_fingerprint(self) -> None:
        with self.assertRaises(SystemExit) as refused:
            aicfo_spend.main([str(self.folder), "settings"], Downloads(b"not the engine"))

        self.assertIn("doesn't match its pinned fingerprint", str(refused.exception))
        self.assertFalse((self.folder / aicfo_spend.ENGINE_FOLDER / aicfo_spend.WHEEL_NAME).exists())
        self.assertFalse((self.folder / "ran.json").exists())

    def test_replaces_an_engine_file_that_was_altered(self) -> None:
        downloads = Downloads(self.wheel)
        aicfo_spend.main([str(self.folder), "settings"], downloads)
        (self.folder / aicfo_spend.ENGINE_FOLDER / aicfo_spend.WHEEL_NAME).write_bytes(b"altered")

        aicfo_spend.main([str(self.folder), "settings"], downloads)

        self.assertEqual(len(downloads.urls), 2)
        self.assertEqual((self.folder / aicfo_spend.ENGINE_FOLDER / aicfo_spend.WHEEL_NAME).read_bytes(), self.wheel)

    def test_explains_itself_when_given_too_little(self) -> None:
        with self.assertRaises(SystemExit) as refused:
            aicfo_spend.main([str(self.folder)], Downloads(self.wheel))

        self.assertIn("Usage:", str(refused.exception))

    def test_the_pinned_release_is_the_one_the_url_names(self) -> None:
        self.assertIn(f"/v{aicfo_spend.ENGINE_VERSION}/", aicfo_spend.WHEEL_URL)
        self.assertTrue(aicfo_spend.WHEEL_URL.endswith(aicfo_spend.WHEEL_NAME))


if __name__ == "__main__":
    unittest.main()
