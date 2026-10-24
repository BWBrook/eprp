"""Checks behind the pbdb-chronosphere entry that the profiler does not make.

Usage: python3 pbdb_chronosphere_checks.py SURVEY_TSV REGISTRY_TSV TABLES_DEST PBDB_GLOBAL_RAW OUT_TSV

SURVEY_TSV is zenodo-survey.tsv; REGISTRY_TSV is chronosphere's registry
listing (resources/software/chronosphere/pbdb_versions.tsv). Writes rows of
section, version, metric, value:
- versions: downloads per year, the longest gaps, versions on Zenodo but not
  in the registry, repeated version strings;
- index: Zenodo's version index (repeated values, the newest, inversions
  against the version dates);
- timescale: for each pair of consecutive sampled tables (and the newest
  against today's public snapshot), the intervals whose modal max_ma changed,
  with the largest examples;
- absent: occurrences public today, created before a table's access date
  but missing from it: how many are entirely Precambrian (min_ma > 538.8),
  created within 42 days before the access date, or numbered above the
  table's highest occurrence number;
- tail: each table's highest occurrence number and whether its CSV ends
  with a newline.
Standard library only.
"""

import collections
import csv
import datetime as dt
import glob
import io
import os
import re
import sys
import zipfile

survey_tsv, registry_tsv, tables_dest, pbdb, out_tsv = sys.argv[1:6]
csv.field_size_limit(1 << 30)
out = []


def put(*row):
    out.append([str(x) for x in row])


def num(x):
    return int(x) if x.isdigit() else int(float(x))


survey = list(csv.DictReader(open(survey_tsv, encoding="utf-8"), delimiter="\t"))
days = [dt.date.fromisoformat(r["publication_date"]) for r in survey]
put("versions", "", "versions on Zenodo", len(survey))
put("versions", "", "versions per year", "; ".join(f"{y} {c}" for y, c in sorted(collections.Counter(r["version"][:4] for r in survey).items())))
dates = sorted(set(days))
gaps = sorted(((b - a).days, a, b) for a, b in zip(dates, dates[1:]))[::-1][:6]
put("versions", "", "longest gaps (days, from, to)", "; ".join(f"{g} {a} {b}" for g, a, b in gaps))
reps = [v for v, c in collections.Counter(r["version"] for r in survey).items() if c > 1]
put("versions", "", "repeated version strings", "; ".join(reps) or "none")
with open(registry_tsv, encoding="utf-8") as f:
    reg = [line.split("\t") for line in f.read().splitlines() if not line.startswith("#")][1:]
reg_records = {x[5].split("zenodo.")[-1] for x in reg if x[0] != "taxa"}
put("versions", "", "registry occurrence versions", len(reg_records))
missing = [f"{r['version']}_{r['record']}" for r in survey if r["record"] not in reg_records]
put("versions", "", "on Zenodo, not in the registry", f"{len(missing)}: " + "; ".join(missing))

idx = collections.Counter(r["index"] for r in survey)
put("index", "", "distinct index values; values shared by more than one version",
    f"{len(idx)}; {sum(1 for c in idx.values() if c > 1)}")
put("index", "", "most shared index value", "%s (%d versions)" % idx.most_common(1)[0])
top = max(survey, key=lambda r: int(r["index"]))
put("index", "", "newest index; versions holding it; its version", f"{top['index']}; {idx[top['index']]}; {top['version']}_{top['record']}")
by_version = sorted(survey, key=lambda r: (r["version"], int(r["record"])))
inv = sum(1 for a, b in zip(by_version, by_version[1:]) if int(b["index"]) < int(a["index"]))
put("index", "", "inversions: a later version with a lower index", inv)

# today's public data
public, created, coll_public, today = set(), {}, collections.Counter(), {}
for p in glob.glob(os.path.join(pbdb, "occurrences__p*.csv")):
    with open(p, newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        h = next(r)
        ix = [h.index(k) for k in ("occurrence_no", "collection_no", "created", "early_interval", "max_ma", "min_ma",
                                   "late_interval")]
        for row in r:
            no = int(row[ix[0]])
            public.add(no)
            coll_public[num(row[ix[1]])] += 1
            today[no] = (row[ix[2]][:19], row[ix[3]], row[ix[4]], row[ix[5]], row[ix[6]])
coll_n = {}
for p in glob.glob(os.path.join(pbdb, "collections__p*.csv")):
    with open(p, newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        h = next(r)
        ic, ino = h.index("collection_no"), h.index("n_occs")
        for row in r:
            coll_n[num(row[ic])] = int(row[ino] or 0)

ERAS = [(2.58, "Quaternary"), (23.03, "Neogene"), (66.0, "Paleogene"), (145.0, "Cretaceous"), (201.4, "Jurassic"),
        (251.902, "Triassic"), (538.8, "Paleozoic"), (1e9, "Precambrian")]


def era(max_ma):
    try:
        x = float(max_ma)
    except ValueError:
        return "no age"
    return next(name for top_, name in ERAS if x <= top_)


def modal_ages(pairs):
    tally = collections.defaultdict(collections.Counter)
    for iv, ma in pairs:
        if iv and ma not in ("", "NA"):
            tally[iv][f"{float(ma):.4f}"] += 1
    return {iv: (c.most_common(1)[0][0], sum(c.values())) for iv, c in tally.items()}


tables = sorted(d for d in os.listdir(os.path.join(tables_dest, "raw"))
                if os.path.exists(os.path.join(tables_dest, "raw", d, "MANIFEST.json")))
prev, history = None, {}
for d in tables:
    vdir = os.path.join(tables_dest, "raw", d)
    with open(os.path.join(vdir, "metadata_occs.txt" if os.path.exists(os.path.join(vdir, "metadata_occs.txt")) else "metadata.txt"),
              encoding="utf-8") as f:
        m = re.search(r'"Access Time","\w+ (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})', f.read())
    access = f"{m.group(1)} {m.group(2)}"
    ids, pairs, eras, eras_w, top_no = set(), [], collections.Counter(), collections.Counter(), 0
    with zipfile.ZipFile(os.path.join(vdir, "pbdb_csv.zip")) as z:
        member = [x for x in z.infolist() if x.filename.endswith(".csv")][0]
        with z.open(member) as raw:
            r = csv.reader(io.TextIOWrapper(raw, encoding="utf-8", errors="replace", newline=""))
            h = next(r)
            io_, ic, iiv, ima, il = (h.index(k) for k in ("occurrence_no", "collection_no", "early_interval", "max_ma",
                                                           "late_interval"))
            for row in r:
                no = num(row[io_])
                ids.add(no)
                top_no = max(top_no, no)
                if row[il] in ("", "NA"):  # single-interval rows: max_ma is that interval's base
                    pairs.append((row[iiv], row[ima]))
                e = era(row[ima])
                eras[e] += 1
        with z.open(member) as raw:
            raw.seek(max(member.file_size - 1, 0))
            ends = raw.read(1) == b"\n"
    put("tail", d, "highest occurrence number; CSV ends with a newline", f"{top_no}; {ends}")
    absent = [no for no, t in today.items() if no not in ids and t[0] and t[0] < access]
    old = {no for no in absent if today[no][3] and float(today[no][3]) >= 635}  # wholly before the Ediacaran
    cutoff = (dt.datetime.fromisoformat(access) - dt.timedelta(days=42)).isoformat(sep=" ")
    recent = {no for no in absent if today[no][0] >= cutoff}
    above = {no for no in absent if no > top_no}
    other = [no for no in absent if no not in old and no not in recent and no not in above]
    put("absent", d, "public today, created before the access time, missing; wholly pre-Ediacaran (min_ma >= 635);"
        " created in the 42 days before; numbered above the table's highest", f"{len(absent)}; {len(old)}; {len(recent)}; {len(above)}")
    put("absent", d, "the rest: count; early intervals; creation years",
        f"{len(other)}; " + ", ".join(f"{k} {v}" for k, v in collections.Counter(today[no][1] for no in other).most_common(4))
        + "; " + ", ".join(f"{k} {v}" for k, v in collections.Counter(today[no][0][:4] for no in other).most_common(4)))
    ages = modal_ages(pairs)
    history[d] = ages
    if prev:
        changed = sorted(((n, iv, prev[1][iv][0], a) for iv, (a, n) in ages.items()
                          if iv in prev[1] and n >= 50 and prev[1][iv][0] != a), reverse=True)
        put("timescale", f"{prev[0]} to {d}", "intervals (50+ single-interval rows) whose modal max_ma changed; largest",
            f"{len(changed)}; " + "; ".join(f"{iv} {old}->{new}" for n, iv, old, new in changed[:6]))
    prev = (d, ages)
    print(d, flush=True)

ages_today = modal_ages((t[1], t[2]) for t in today.values() if not t[4])
changed = sorted(((n, iv, prev[1][iv][0], a) for iv, (a, n) in ages_today.items()
                  if iv in prev[1] and n >= 50 and prev[1][iv][0] != a), reverse=True)
put("timescale", f"{prev[0]} to today", "intervals (50+ single-interval rows) whose modal max_ma changed; largest",
    f"{len(changed)}; " + "; ".join(f"{iv} {old}->{new}" for n, iv, old, new in changed[:6]))
history["today"] = ages_today
for iv in ["Kungurian", "Roadian", "Wuchiapingian", "Changhsingian", "Olenekian", "Anisian", "Middle Oxfordian",
           "Maastrichtian", "Priabonian", "Late Pleistocene"]:
    put("timescale", iv, "modal max_ma in each sampled table, then today",
        "; ".join(f"{d[:8]} {a[iv][0]}" for d, a in history.items() if iv in a))
with open(out_tsv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["section", "version", "metric", "value"])
    w.writerows(out)
print("rows", len(out))
