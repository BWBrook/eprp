"""Fetch checksum-pinned primary sources beside this script; no package installation."""
import hashlib
import json
import os
from pathlib import Path
import tarfile
from urllib.request import urlopen

manifest = Path(__file__).resolve().with_name("author-source-manifest.json")
out = Path(os.environ.get("Q038_AUDIT_DIR", "scratch/q038-independent-audit"))
out.mkdir(parents=True, exist_ok=True)
url = "https://cran.r-project.org/src/contrib/Archive/RMark/RMark_3.0.0.tar.gz"
b = urlopen(url, timeout=30).read()
assert hashlib.sha256(b).hexdigest() == "08a20f4246dcfe6a8bfe8acd673346b79dc1b9b42a4354d865364f577329305b"
archive = out / "RMark_3.0.0.tar.gz"
archive.write_bytes(b)
with tarfile.open(archive) as t:
    t.extractall(out, filter="data")
(out / "zenodo").mkdir(exist_ok=True)
for f in json.loads(manifest.read_text()):
    b = urlopen(f["url"], timeout=30).read()
    assert "md5:" + hashlib.md5(b).hexdigest() == f["checksum"]
    (out / "zenodo" / f["file"]).write_bytes(b)
print("Checksum-pinned sources retrieved; nothing fitted or installed.")
