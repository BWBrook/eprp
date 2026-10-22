"""Mirror every version of a Zenodo record into a read-only local archive.

Usage: python3 zenodo_mirror.py RECORD_ID DEST [--only VERSION_DIR ...] [--index-only]

Writes DEST/versions.tsv (all versions) and DEST/raw/<version>_<record>/ holding
the unchanged files plus MANIFEST.json. Files are verified against Zenodo's md5,
hashed with sha256, then made read-only. Completed versions are skipped, so an
interrupted run resumes. Standard library only.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

API = "https://zenodo.org/api/records"
UA = "eprp-zenodo-mirror/1 (research data archive)"


def get_json(url):
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or attempt == 5:
                raise
            time.sleep(int(e.headers.get("Retry-After", 0)) or 2 ** attempt * 5)
        except urllib.error.URLError:
            if attempt == 5:
                raise
            time.sleep(2 ** attempt * 5)


def all_versions(record_id):
    hits, page = [], 1
    while True:
        data = get_json(f"{API}/{record_id}/versions?size=25&page={page}")
        batch = data["hits"]["hits"]
        hits.extend(batch)
        if not batch or len(hits) >= data["hits"]["total"]:
            return sorted({h["id"]: h for h in hits}.values(), key=lambda h: (h["metadata"].get("publication_date", ""), h["id"]))
        page += 1
        time.sleep(1)


def version_dir(hit):
    v = re.sub(r"[^A-Za-z0-9._-]+", "-", str(hit["metadata"].get("version", "")).strip()).strip("-")
    return f"{v}_{hit['id']}" if v else str(hit["id"])


def write_index(hits, path):
    cols = ["version_dir", "version", "record_id", "doi", "publication_date", "license", "total_bytes", "files"]
    tmp = path + ".part"
    with open(tmp, "w") as f:
        f.write("\t".join(cols) + "\n")
        for h in hits:
            m = h["metadata"]
            files = ";".join(f"{x['key']}|{x['size']}|{x['checksum']}" for x in sorted(h["files"], key=lambda x: x["key"]))
            row = [version_dir(h), str(m.get("version", "")), str(h["id"]), h.get("doi", ""), m.get("publication_date", ""),
                   (m.get("license") or {}).get("id", ""), str(sum(x["size"] for x in h["files"])), files]
            f.write("\t".join(row) + "\n")
    os.replace(tmp, path)


def download(url, dest, size, md5_expected):
    for attempt in range(6):
        try:
            md5, sha = hashlib.md5(), hashlib.sha256()
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=300) as r, open(dest + ".part", "wb") as out:
                while chunk := r.read(1 << 20):
                    md5.update(chunk)
                    sha.update(chunk)
                    out.write(chunk)
            got = os.path.getsize(dest + ".part")
            if got != size or md5.hexdigest() != md5_expected:
                raise IOError(f"verification failed for {url}: size {got}/{size}, md5 {md5.hexdigest()}/{md5_expected}")
            os.replace(dest + ".part", dest)
            return sha.hexdigest()
        except (urllib.error.URLError, IOError, TimeoutError) as e:
            code = getattr(e, "code", None)
            if attempt == 5 or (code is not None and code not in (429, 500, 502, 503, 504)):
                raise
            wait = int(getattr(e, "headers", {}).get("Retry-After", 0) or 0) if code == 429 else 0
            print(f"  retry {attempt + 1} after {e}", flush=True)
            time.sleep(wait or 2 ** attempt * 10)


def mirror_version(hit, raw_root, tool_sha):
    vdir = os.path.join(raw_root, version_dir(hit))
    manifest_path = os.path.join(vdir, "MANIFEST.json")
    if os.path.exists(manifest_path):
        return False
    os.makedirs(vdir, exist_ok=True)
    files = []
    for x in sorted(hit["files"], key=lambda x: x["key"]):
        algo, md5 = x["checksum"].split(":", 1)
        assert algo == "md5", x["checksum"]
        dest = os.path.join(vdir, x["key"])
        sha = download(x["links"]["self"], dest, x["size"], md5)
        os.chmod(dest, 0o444)
        files.append({"key": x["key"], "size": x["size"], "md5": md5, "sha256": sha, "url": x["links"]["self"]})
        time.sleep(1)
    m = hit["metadata"]
    manifest = {
        "zenodo_record": hit["id"], "doi": hit.get("doi"), "concept_doi": hit.get("conceptdoi"),
        "version": m.get("version"), "publication_date": m.get("publication_date"), "title": m.get("title"),
        "creators": [c.get("name") for c in m.get("creators", [])], "license": (m.get("license") or {}).get("id"),
        "files": files, "retrieved_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "tool": {"name": "zenodo_mirror.py", "sha256": tool_sha},
    }
    with open(manifest_path + ".part", "w") as f:
        json.dump(manifest, f, indent=2)
    os.replace(manifest_path + ".part", manifest_path)
    os.chmod(manifest_path, 0o444)
    os.chmod(vdir, 0o555)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("record_id")
    ap.add_argument("dest")
    ap.add_argument("--only", nargs="*", default=None, help="version_dir names to fetch (default: all)")
    ap.add_argument("--index-only", action="store_true")
    a = ap.parse_args()
    with open(__file__, "rb") as f:
        tool_sha = hashlib.sha256(f.read()).hexdigest()
    os.makedirs(a.dest, exist_ok=True)
    hits = all_versions(a.record_id)
    write_index(hits, os.path.join(a.dest, "versions.tsv"))
    print(f"{len(hits)} versions indexed", flush=True)
    if a.index_only:
        return
    wanted = [h for h in hits if a.only is None or version_dir(h) in a.only]
    raw_root = os.path.join(a.dest, "raw")
    os.makedirs(raw_root, exist_ok=True)
    for i, h in enumerate(wanted, 1):
        done = mirror_version(h, raw_root, tool_sha)
        print(f"[{i}/{len(wanted)}] {version_dir(h)} {'fetched' if done else 'present'}", flush=True)
    print("complete", flush=True)


if __name__ == "__main__":
    sys.exit(main())
