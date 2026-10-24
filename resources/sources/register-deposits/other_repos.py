"""File lists and provider checksums for deposits on Harvard Dataverse, OSF and Mendeley Data.

Usage:
  python3 other_repos.py specs dataverse|osf|mendeley ID SPECS_OUT EXPECTED_OUT
  python3 other_repos.py check VERSION_DIR EXPECTED_TSV

`specs` writes NAME::URL lines for `data_mirror.py url --specs-file` and a TSV of
the provider's size and checksum per file, and prints the deposit's title,
version and licence. IDs: a Dataverse DOI (doi:10.7910/DVN/...), an OSF
project (5 characters), a Mendeley dataset with its version (ID/VERSION).
Dataverse serves ingested tables as .tab; the original upload is requested, as
that is what its MD5 describes. `check` re-hashes the mirrored files against
the TSV (md5 or sha256, as the provider gives) and exits 1 on any mismatch.
Standard library only; no contact details are sent.
"""

import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request

UA = {"User-Agent": "eprp-data-mirror/4 (research data archive)"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        return json.load(r)


def dataverse(pid):
    d = get("https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=" + urllib.parse.quote(pid, safe=":/"))["data"]
    v = d["latestVersion"]
    title = next(f["value"] for f in v["metadataBlocks"]["citation"]["fields"] if f["typeName"] == "title")
    rows = []
    for f in v["files"]:
        df = f["dataFile"]
        if f.get("restricted"):
            raise SystemExit(f"{df['filename']} is restricted")
        original = df.get("originalFileName")
        name = original or df["filename"]
        url = f"https://dataverse.harvard.edu/api/access/datafile/{df['id']}" + ("?format=original" if original else "")
        size = df.get("originalFileSize") if original else df.get("filesize")
        rows.append((name, url, size, df["checksum"]["type"].lower(), df["checksum"]["value"]))
    licence = (v.get("license") or {}).get("name") or v.get("termsOfUse") or "none stated"
    return title, f"{v['versionNumber']}.{v['versionMinorNumber']} ({v.get('releaseTime', '')[:10]})", licence, rows


def osf(node):
    a = get(f"https://api.osf.io/v2/nodes/{node}/")["data"]
    lic_rel = a["relationships"].get("license", {}).get("data")
    licence = get(f"https://api.osf.io/v2/licenses/{lic_rel['id']}/")["data"]["attributes"]["name"] if lic_rel else "none stated"
    rows, url = [], f"https://api.osf.io/v2/nodes/{node}/files/osfstorage/?page[size]=100"
    while url:
        page = get(url)
        for f in page["data"]:
            fa = f["attributes"]
            if fa["kind"] != "file":
                raise SystemExit(f"{fa['name']}: folders are not handled")
            rows.append((fa["name"], f["links"]["download"], fa["size"], "sha256", fa["extra"]["hashes"]["sha256"]))
        url = page["links"].get("next")
    return a["attributes"]["title"], f"modified {a['attributes']['date_modified'][:10]}", licence, rows


def mendeley(spec):
    ds, ver = spec.split("/")
    meta = get(f"https://data.mendeley.com/public-api/datasets/{ds}?version={ver}")
    files = get(f"https://data.mendeley.com/public-api/datasets/{ds}/files?folder_id=root&version={ver}")
    rows = [(f["filename"], f["content_details"]["download_url"], f["content_details"]["size"], "sha256",
             f["content_details"]["sha256_hash"]) for f in files]
    licence = (meta.get("data_licence") or {}).get("full_name") or (meta.get("data_licence") or {}).get("short_name") or "none stated"
    return meta["name"], f"v{ver} ({(meta.get('publish_date') or '')[:10]})", licence, rows


def check(vdir, expected):
    bad = 0
    for line in open(expected, encoding="utf-8").read().splitlines()[1:]:
        name, size, algo, value = line.split("\t")
        path = os.path.join(vdir, name)
        h = hashlib.new(algo)
        with open(path, "rb") as f:
            for b in iter(lambda: f.read(1 << 20), b""):
                h.update(b)
        ok = h.hexdigest() == value.lower() and (size in ("", "None") or os.path.getsize(path) == int(size))
        bad += not ok
        print(("ok  " if ok else "BAD ") + name)
    print(f"{bad} files failed the provider checksum")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    if sys.argv[1] == "check":
        check(sys.argv[2], sys.argv[3])
    else:
        provider, ident, specs_out, expected_out = sys.argv[2:6]
        title, version, licence, rows = {"dataverse": dataverse, "osf": osf, "mendeley": mendeley}[provider](ident)
        names = [r[0] for r in rows]
        if len(set(names)) != len(names) or any("/" in n for n in names):
            raise SystemExit("file names repeat or contain '/'")
        with open(specs_out, "w", encoding="utf-8") as f:
            f.writelines(f"{n}::{u}\n" for n, u, *_ in rows)
        with open(expected_out, "w", encoding="utf-8") as f:
            f.write("name\tsize\talgorithm\tvalue\n")
            f.writelines(f"{n}\t{s}\t{a}\t{v}\n" for n, _, s, a, v in rows)
        print(json.dumps({"title": title, "version": version, "licence": licence, "files": len(rows),
                          "bytes": sum(int(r[2] or 0) for r in rows)}))
