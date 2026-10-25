"""sha256 of every member of the given zip files, nested zips one level down.

Usage: python3 zip_members.py OUT_TSV ZIP [ZIP ...]

Writes zip, member, bytes, sha256; a nested member's zip is written as
outer::inner. __MACOSX and .DS_Store entries are skipped. Standard library only.
"""

import csv
import hashlib
import io
import sys
import zipfile

out = sys.argv[1]
fo = open(out, "w", newline="")
w = csv.writer(fo, delimiter="\t", lineterminator="\n")
w.writerow(["zip", "member", "bytes", "sha256"])


def walk(label, zf, depth=0):
    for m in zf.infolist():
        if m.is_dir() or "__MACOSX" in m.filename or m.filename.endswith(".DS_Store"):
            continue
        nested = depth == 0 and m.filename.lower().endswith(".zip") and m.file_size < 2_000_000_000
        h = hashlib.sha256()
        with zf.open(m) as f:
            data = f.read() if nested else None
            if data is None:
                for b in iter(lambda: f.read(1 << 22), b""):
                    h.update(b)
            else:
                h.update(data)
        w.writerow([label, m.filename, m.file_size, h.hexdigest()])
        if data is not None:
            try:
                walk(f"{label}::{m.filename}", zipfile.ZipFile(io.BytesIO(data)), 1)
            except zipfile.BadZipFile:
                pass


for path in sys.argv[2:]:
    walk(path, zipfile.ZipFile(path))
fo.close()
