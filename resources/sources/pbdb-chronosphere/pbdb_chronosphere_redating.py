"""Date PBDB's interval re-datings from the heads of chronosphere's archived tables.

Usage: python3 pbdb_chronosphere_redating.py SURVEY_TSV FROM_VERSION TO_VERSION HEAD_BYTES JOBS CACHE_DIR OUT_TSV

Each version's pbdb_csv.zip holds one deflated CSV in occurrence-number
order. For every version from FROM_VERSION to TO_VERSION (version strings,
inclusive; listed in SURVEY_TSV, zenodo-survey.tsv), the first HEAD_BYTES of
the zip are fetched with an HTTP Range request (JOBS at once), the CSV head
is inflated, and the modal max_ma of the single-interval rows (no
late_interval) is taken for each early_interval: for those rows max_ma is
the interval's base as PBDB served it that day. Results are cached per
version in CACHE_DIR. OUT_TSV lists, for each pair of consecutive versions,
the intervals (20+ rows in both heads) whose modal max_ma changed. The heads
are partial reads, not mirrored files: they cannot be checked against
Zenodo's checksums, so an unexpected change is confirmed on the whole table.
Standard library only; no contact details are sent.
"""

import collections
import concurrent.futures
import csv
import io
import json
import os
import struct
import sys
import time
import urllib.request
import zlib

survey_tsv, v_from, v_to, head_bytes, jobs, cache_dir, out_tsv = sys.argv[1:8]
head_bytes, jobs = int(head_bytes), int(jobs)
UA = "eprp-data-mirror/4 (research data archive)"
csv.field_size_limit(1 << 30)
os.makedirs(cache_dir, exist_ok=True)
versions = sorted((r for r in csv.DictReader(open(survey_tsv, encoding="utf-8"), delimiter="\t")
                   if v_from <= r["version"] <= v_to and "pbdb_csv.zip" in r["files"]),
                  key=lambda r: (r["version"], int(r["record"])))


def head(record):
    url = f"https://zenodo.org/api/records/{record}/files/pbdb_csv.zip/content"
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Range": f"bytes=0-{head_bytes - 1}"})
            with urllib.request.urlopen(req, timeout=300) as r:
                if r.status != 206:
                    raise IOError(f"no partial content (HTTP {r.status})")
                return r.read()
        except Exception as e:
            print(f"  {record} retry {attempt + 1}: {e!r}", flush=True)
            time.sleep(10 * (attempt + 1))
    raise IOError(f"{record}: could not fetch the head")


def profile(r):
    key = f"{r['version']}_{r['record']}"
    path = os.path.join(cache_dir, key + ".json")
    if os.path.exists(path):
        return key, json.load(open(path, encoding="utf-8"))
    data = head(r["record"])
    sig, method, n, e = struct.unpack("<IH", data[:4] + data[8:10]) + struct.unpack("<HH", data[26:30])
    if sig != 0x04034B50 or method != 8:
        raise IOError(f"{key}: not a deflated zip member")
    text = zlib.decompressobj(-15).decompress(data[30 + n + e:]).decode("utf-8", "replace")
    text = text[:text.rfind("\n") + 1]  # drop the partial last line
    rows = csv.reader(io.StringIO(text, newline=""))
    h = next(rows)
    io_, iv, il, ima = (h.index(k) for k in ("occurrence_no", "early_interval", "late_interval", "max_ma"))
    tally, count, top = collections.defaultdict(collections.Counter), 0, 0
    for row in rows:
        if len(row) != len(h):
            continue  # a row cut by a quoted newline at the end
        count += 1
        top = max(top, int(float(row[io_])))
        if row[il] in ("", "NA") and row[ima] not in ("", "NA"):
            tally[row[iv]][f"{float(row[ima]):.4f}"] += 1
    res = {"rows": count, "highest_occurrence_no": top,
           "ages": {k: [c.most_common(1)[0][0], sum(c.values())] for k, c in tally.items()}}
    with open(path + ".part", "w", encoding="utf-8") as f:
        json.dump(res, f)
    os.replace(path + ".part", path)
    return key, res


with concurrent.futures.ThreadPoolExecutor(jobs) as ex:
    results = dict(ex.map(profile, versions))
keys = [f"{r['version']}_{r['record']}" for r in versions]
out = [["from", "to", "rows in heads", "intervals compared", "intervals changed", "changes (interval old->new, rows)"]]
for a, b in zip(keys, keys[1:]):
    A, B = results[a]["ages"], results[b]["ages"]
    both = [k for k in A if k in B and A[k][1] >= 20 and B[k][1] >= 20]
    changed = sorted(((min(A[k][1], B[k][1]), k) for k in both if A[k][0] != B[k][0]), reverse=True)
    out.append([a, b, f"{results[a]['rows']}/{results[b]['rows']}", len(both), len(changed),
                "; ".join(f"{k} {A[k][0]}->{B[k][0]} ({m})" for m, k in changed)])
with open(out_tsv, "w", newline="", encoding="utf-8") as f:
    csv.writer(f, delimiter="\t", lineterminator="\n").writerows(out)
print(json.dumps({"versions": len(keys), "pairs with changes": sum(1 for row in out[1:] if row[4])}))
