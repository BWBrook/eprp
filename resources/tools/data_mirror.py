#!/usr/bin/env python3
"""Mirror every version of a Zenodo record or Figshare collection into a read-only local archive.

Usage:
  python3 data_mirror.py zenodo RECORD_ID DEST [--latest] [--only VERSION_DIR ...] [--index-only]
  python3 data_mirror.py figshare COLLECTION_ID DEST [--latest] [--only VERSION_DIR ...] [--index-only]
  python3 data_mirror.py verify DEST [--only VERSION_DIR ...]

Writes DEST/versions.tsv (every version the provider offers) and
DEST/raw/<version_dir>/ holding the unchanged files plus MANIFEST.json for the
selected versions: --latest takes the newest version of each record (Figshare:
of each article), --only names version_dirs, and both may be combined. Zenodo
version_dirs are <version>_<record>; Figshare ones are <article-title>_v<N>_<article>,
one per version of every article in the collection. Files are verified against
the provider's size and md5, hashed with sha256, then made read-only.
Interrupted downloads resume from their .part files and completed versions are
skipped. verify re-hashes mirrored files against their manifests. Standard
library only.
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

UA = "eprp-data-mirror/3 (research data archive)"
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


def slug(text):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", str(text).strip()).strip("-")


def zenodo_versions(record_id):
    api = "https://zenodo.org/api/records"
    hits, page = {}, 1
    while True:
        data = get_json(f"{api}/{record_id}/versions?size=25&page={page}")
        total = data["hits"]["total"]
        batch = data["hits"]["hits"]
        hits.update((h["id"], h) for h in batch)
        if len(hits) >= total or not batch:
            break
        page += 1
        time.sleep(1)
    if len(hits) != total:
        raise RuntimeError(f"index incomplete: {len(hits)} of {total} versions")
    out = []
    for h in hits.values():
        m = h["metadata"]
        v = slug(m.get("version", ""))
        files = []
        for x in h["files"]:
            algo, md5 = x["checksum"].split(":", 1)
            assert algo == "md5", x["checksum"]
            files.append({"key": x["key"], "size": x["size"], "md5": md5, "url": x["links"]["self"]})
        out.append({
            "dir": f"{v}_{h['id']}" if v else str(h["id"]), "provider": "zenodo", "record": h["id"],
            "version": m.get("version"), "doi": h.get("doi"), "concept_doi": h.get("conceptdoi"),
            "publication_date": m.get("publication_date", ""), "title": m.get("title"),
            "creators": [c.get("name") for c in m.get("creators", [])],
            "license": (m.get("license") or {}).get("id", ""), "files": files,
        })
    return sorted(out, key=lambda r: (r["publication_date"], r["record"]))


def figshare_versions(collection_id):
    api = "https://api.figshare.com/v2"
    collection = get_json(f"{api}/collections/{collection_id}")
    articles = get_json(f"{api}/collections/{collection_id}/articles?page_size=1000")
    if len(articles) != collection["articles_count"]:
        raise RuntimeError(f"index incomplete: {len(articles)} of {collection['articles_count']} articles")
    out = []
    for a in articles:
        for v in get_json(f"{api}/articles/{a['id']}/versions"):
            d = get_json(f"{api}/articles/{a['id']}/versions/{v['version']}")
            time.sleep(0.3)
            files = [{"key": f["name"], "size": f["size"], "md5": f["computed_md5"], "url": f["download_url"]}
                     for f in d["files"]]
            out.append({
                "dir": f"{slug(d['title'])}_v{v['version']}_{a['id']}", "provider": "figshare", "record": a["id"],
                "version": v["version"], "doi": d.get("doi"), "concept_doi": collection.get("doi"),
                "publication_date": (d.get("published_date") or "")[:10], "title": d.get("title"),
                "creators": [x.get("full_name") for x in d.get("authors", [])],
                "license": (d.get("license") or {}).get("name", ""), "files": files,
            })
    return sorted(out, key=lambda r: (r["publication_date"], r["record"], r["version"]))


def write_index(versions, path):
    cols = ["version_dir", "version", "record_id", "doi", "publication_date", "license", "total_bytes", "files"]
    tmp = path + ".part"
    with open(tmp, "w") as f:
        f.write("\t".join(cols) + "\n")
        for r in versions:
            files = ";".join(f"{x['key']}|{x['size']}|md5:{x['md5']}" for x in sorted(r["files"], key=lambda x: x["key"]))
            row = [r["dir"], str(r["version"] or ""), str(r["record"]), r["doi"] or "", r["publication_date"],
                   r["license"], str(sum(x["size"] for x in r["files"])), files]
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


def mirror_version(r, raw_root, tool_sha):
    vdir = os.path.join(raw_root, r["dir"])
    manifest_path = os.path.join(vdir, "MANIFEST.json")
    if os.path.exists(manifest_path):
        return False
    os.makedirs(vdir, exist_ok=True)
    files = []
    for x in sorted(r["files"], key=lambda x: x["key"]):
        dest = os.path.join(vdir, x["key"])
        if os.path.exists(dest):
            got_md5, sha = hash_file(dest, "md5", "sha256")
            if got_md5 != x["md5"]:
                raise IOError(f"{dest} exists with wrong md5")
        else:
            sha = download(x["url"], dest, x["size"], x["md5"])
        os.chmod(dest, 0o444)
        files.append({**x, "sha256": sha})
        time.sleep(1)
    manifest = {k: r[k] for k in ("provider", "record", "version", "doi", "concept_doi", "publication_date",
                                  "title", "creators", "license")}
    manifest.update(files=files, retrieved_utc=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                    tool={"name": "data_mirror.py", "sha256": tool_sha})
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
    sub = ap.add_subparsers(dest="command", required=True)
    for provider in ("zenodo", "figshare"):
        p = sub.add_parser(provider)
        p.add_argument("record_id")
        p.add_argument("dest")
        p.add_argument("--only", nargs="*", default=None, help="version_dir names to fetch")
        p.add_argument("--latest", action="store_true", help="fetch the newest version of each record")
        p.add_argument("--index-only", action="store_true")
    p = sub.add_parser("verify")
    p.add_argument("dest")
    p.add_argument("--only", nargs="*", default=None)
    a = ap.parse_args()
    raw_root = os.path.join(a.dest, "raw")
    if a.command == "verify":
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
    versions = (zenodo_versions if a.command == "zenodo" else figshare_versions)(a.record_id)
    write_index(versions, os.path.join(a.dest, "versions.tsv"))
    print(f"{len(versions)} versions indexed", flush=True)
    if a.index_only:
        return 0
    if a.only is not None:
        unknown = set(a.only) - {r["dir"] for r in versions}
        if unknown:
            sys.exit(f"unknown version_dir: {' '.join(sorted(unknown))}")
    chosen = set(a.only or [])
    if a.latest:
        group = (lambda r: "all") if a.command == "zenodo" else (lambda r: r["record"])
        newest = {}
        for r in versions:
            key = group(r)
            if key not in newest or (r["publication_date"], str(r["version"])) > (newest[key]["publication_date"], str(newest[key]["version"])):
                newest[key] = r
        chosen |= {r["dir"] for r in newest.values()}
    wanted = [r for r in versions if r["dir"] in chosen] if (a.only is not None or a.latest) else versions
    for i, r in enumerate(wanted, 1):
        done = mirror_version(r, raw_root, tool_sha)
        print(f"[{i}/{len(wanted)}] {r['dir']} {'fetched' if done else 'present'}", flush=True)
    print("complete", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
