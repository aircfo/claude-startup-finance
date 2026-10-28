"""Rebuild docs/downloads/finance-brain-starter-kit.zip from templates/finance-brain/.

Run after any change to the kit, so the download link always matches the folder on GitHub:

    python3 docs/downloads/_build_zip.py
"""
import pathlib
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
KIT = HERE.parent.parent / "templates" / "finance-brain"
OUT = HERE / "finance-brain-starter-kit.zip"

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for path in sorted(KIT.rglob("*")):
        # Skip hidden files (.DS_Store) and Office lock files (~$name.xlsx) so stray local
        # files never ship in the public download.
        if path.is_file() and not path.name.startswith((".", "~$")):
            z.write(path, pathlib.Path("finance-brain") / path.relative_to(KIT))

print(f"Wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
