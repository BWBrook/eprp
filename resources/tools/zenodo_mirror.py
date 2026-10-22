#!/usr/bin/env python3
"""Mirror every version of a Zenodo record into a read-only local archive.

Usage: python3 zenodo_mirror.py RECORD_ID DEST [--only VERSION_DIR ...] [--index-only | --verify]

Writes DEST/versions.tsv (all versions) and DEST/raw/<version>_<record>/ holding
the unchanged files plus MANIFEST.json. Files are verified against Zenodo's size
and md5, hashed with sha256, then made read-only. Interrupted downloads resume
from their .part files and completed versions are skipped. --verify re-hashes
mirrored files against their manifests. Standard library only.
"""

import argparse
import datetime as dt
import email.utils
import fcntl
import hashlib
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

API = "https://zenodo.org/api/records"
UA = "eprp-zenodo-mirror/2 (research data archive)"
RETRYABLE = (429, 500, 502, 503, 504)
TRANSIENT = (urllib.error.URLError, http.client.HTTPException, TimeoutError, ConnectionError)


def retry_wait(err, attempt):
    after = getattr(err, "headers", None) and err.headers.get("Retry-After")
    if after:
        if after.isdigit():
            return int(after)
        when = email.utils.parsedate_to_datetime(after)
        return max(0, (when - dt.datetime.now(dt.timezone.utc)).total_seconds())
    return 2 ** attempt * 5


def get_json(url):
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except TRANSIENT as e:
            if attempt == 5 or (isinstance(e, urllib.error.HTTPError) and e.code not in RETRYABLE):
                raise
            time.sleep(retry_wait(e, attempt))


def all_versions(record_id):
    hits, page = {}, 1
    while True:
        data = get_json(f"{API}/{record_id}/versions?size=25&page={page}")
        total = data["hits"]["total"]
        batch = data["hits"]["hits"]
        hits.update((h["id"], h) for h in batch)
        if len(hits) >= total or not batch:
            break
        page += 1
        time.sleep(1)
    if len(hits) != total:
        raise RuntimeError(f"index incomplete: {len(hits)} of {total} versions")
    return sorted(hits.values(), key=lambda h: (h["metadata"].get("publication_date", ""), h["id"]))


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


def hash_file(path, *algos):
    hs = [hashlib.new(a) for a in algos]
    with open(path, "rb") as f:
        while chunk := f.read(1 << 20):
            for h in hs:
                h.update(chunk)
    return [h.hexdigest() for h in hs]


def download(url, dest, size, md5_expected):
    part = dest + ".part"
    for attempt in range(8):
        have = os.path.getsize(part) if os.path.exists(part) else 0
        if have > size:
            os.remove(part)
            have = 0
        try:
            if have < size:
                headers = {"User-Agent": UA}
                if have:
                    headers["Range"] = f"bytes={have}-"
                with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=300) as r:
                    mode = "ab" if have and r.status == 206 else "wb"
                    with open(part, mode) as out:
                        while chunk := r.read(1 << 20):
                            out.write(chunk)
            md5, sha = hash_file(part, "md5", "sha256")
            got = os.path.getsize(part)
            if got == size and md5 == md5_expected:
                os.replace(part, dest)
                return sha
            if got >= size:
                os.remove(part)
            print(f"  incomplete or mismatched ({got}/{size} bytes); attempt {attempt + 1}", flush=True)
        except TRANSIENT as e:
            if attempt == 7 or (isinstance(e, urllib.error.HTTPError) and e.code not in RETRYABLE):
                raise
            print(f"  retry {attempt + 1} after {e!r}", flush=True)
            time.sleep(retry_wait(e, attempt))
    raise IOError(f"could not fetch {url} intact")


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
        if os.path.exists(dest):
            got_md5, sha = hash_file(dest, "md5", "sha256")
            if got_md5 != md5:
                raise IOError(f"{dest} exists with wrong md5")
        else:
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


def verify(raw_root, only):
    bad = 0
    for v in sorted(os.listdir(raw_root)):
        manifest = os.path.join(raw_root, v, "MANIFEST.json")
        if (only and v not in only) or not os.path.exists(manifest):
            continue
        for f in json.load(open(manifest))["files"]:
            ok = hash_file(os.path.join(raw_root, v, f["key"]), "sha256")[0] == f["sha256"]
            bad += not ok
            print(f"{'ok ' if ok else 'BAD'} {v}/{f['key']}", flush=True)
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("record_id")
    ap.add_argument("dest")
    ap.add_argument("--only", nargs="*", default=None, help="version_dir names to fetch or verify (default: all)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--index-only", action="store_true")
    mode.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    raw_root = os.path.join(a.dest, "raw")
    if a.verify:
        bad = verify(raw_root, a.only)
        print(f"{bad} files failed verification", flush=True)
        return 1 if bad else 0
    with open(__file__, "rb") as f:
        tool_sha = hashlib.sha256(f.read()).hexdigest()
    os.makedirs(raw_root, exist_ok=True)
    lock = open(os.path.join(a.dest, ".mirror.lock"), "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        sys.exit(f"another mirror run holds {a.dest}/.mirror.lock")
    hits = all_versions(a.record_id)
    write_index(hits, os.path.join(a.dest, "versions.tsv"))
    print(f"{len(hits)} versions indexed", flush=True)
    if a.index_only:
        return 0
    if a.only is not None:
        unknown = set(a.only) - {version_dir(h) for h in hits}
        if unknown:
            sys.exit(f"unknown version_dir: {' '.join(sorted(unknown))}")
    wanted = [h for h in hits if a.only is None or version_dir(h) in a.only]
    for i, h in enumerate(wanted, 1):
        done = mirror_version(h, raw_root, tool_sha)
        print(f"[{i}/{len(wanted)}] {version_dir(h)} {'fetched' if done else 'present'}", flush=True)
    print("complete", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
