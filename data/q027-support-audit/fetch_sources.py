# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas==2.3.3", "numpy==2.3.3"]
# ///
"""Retrieve checksum-pinned small source members; never run the source pipeline."""
import csv
import hashlib
import importlib.util
import io
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "screen", root / "data/q027-joint-support/build.py")
screen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(screen)
out = root / "scratch/q027-independent-audit/source"
prefix = "marine-lbg-ms-code-submission-2025-04-22 2/"
archive = None
with Path(__file__).with_name("source-member-checksums.tsv").open() as handle:
    for row in csv.DictReader(handle, delimiter="\t"):
        target = out / row["member"]
        if not target.exists():
            if archive is None:
                archive = zipfile.ZipFile(io.BufferedReader(
                    screen.RangeFile(screen.URL, screen.ARCHIVE_SIZE), buffer_size=1 << 16))
            content = archive.read(prefix + row["member"])
        else:
            content = target.read_bytes()
        assert len(content) == int(row["bytes"]), row["member"]
        assert hashlib.sha256(content).hexdigest() == row["sha256"], row["member"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
if archive is not None:
    archive.close()
print("All pinned source members verified; source pipeline was not executed.")
