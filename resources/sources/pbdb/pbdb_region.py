"""Build the Australia and New Guinea PBDB extract from the global public snapshot.

Usage: python3 pbdb_region.py GLOBAL_RAW OUT_DIR

Regions are cut from the
global snapshot instead (pbdb_global_snapshot.sh: all records, record-level
show blocks only). Two regions, as before:
  core   collections with country code AU, PG, NF, CX, CC or HM;
  _idng  collections coded ID with longitude 129.5 to 141.1 and latitude -11 to 0
         (Indonesian New Guinea, Raja Ampat, Misool and Seram).
For each region, writes occurrences{sfx}.csv (the occurrence row with every
collection column it lacks appended, except personal-name columns),
collections{sfx}.csv, specimens{sfx}.csv (specimens of the region's
occurrences or collections), measurements{sfx}.csv (of those specimens),
references{sfx}.csv (cited by any of those records), taxa{sfx}.csv (taxa
identified or accepted for the region's occurrences), and region_counts.json.
Standard library only.
"""

import csv
import glob
import json
import os
import sys

csv.field_size_limit(1 << 30)
raw, out = sys.argv[1:3]
os.makedirs(out, exist_ok=True)
CORE = {"AU", "PG", "NF", "CX", "CC", "HM"}
PERSONAL = {"collectors", "authorizer", "enterer", "modifier", "updater", "authorizer_no", "enterer_no", "modifier_no", "updater_no"}


def read(paths):
    head = None
    for p in paths:
        with open(p, newline="", encoding="utf-8") as f:
            rd = csv.reader(f)
            h = next(rd)
            if head is None:
                head = h
                yield head
            assert h == head, f"header differs in {p}"
            yield from rd


def first_index(head):
    idx = {}
    for i, h in enumerate(head):
        idx.setdefault(h, i)
    return idx


def region_of(cc, lat, lng):
    if cc in CORE:
        return ""
    try:
        if cc == "ID" and 129.5 <= float(lng) <= 141.1 and -11 <= float(lat) <= 0:
            return "_idng"
    except ValueError:
        pass
    return None


rows = read(sorted(glob.glob(os.path.join(raw, "collections__p*.csv"))))
chead = next(rows)
ci = first_index(chead)
cols = {"": [], "_idng": []}
coll_region = {}
for r in rows:
    reg = region_of(r[ci["cc"]], r[ci["lat"]], r[ci["lng"]])
    if reg is not None:
        cols[reg].append(r)
        coll_region[r[ci["collection_no"]]] = reg

rows = read(sorted(glob.glob(os.path.join(raw, "occurrences__p*.csv"))))
ohead = next(rows)
oi = first_index(ohead)
extra = [h for h in ci if h not in set(ohead) and h not in PERSONAL]
by_coll = {}
occ_ids = {"": set(), "_idng": set()}
refs = {"": set(), "_idng": set()}
taxa_ids = {"": set(), "_idng": set()}
writers, files = {}, []
for reg in ("", "_idng"):
    f = open(os.path.join(out, f"occurrences{reg}.csv"), "w", newline="", encoding="utf-8")
    files.append(f)
    writers[reg] = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator="\n")
    writers[reg].writerow(ohead + extra)
    for c in cols[reg]:
        by_coll[c[ci["collection_no"]]] = [c[ci[h]] for h in extra]
        refs[reg].add(c[ci["reference_no"]])
for r in rows:
    reg = coll_region.get(r[oi["collection_no"]])
    if reg is None:
        continue
    writers[reg].writerow(r + by_coll[r[oi["collection_no"]]])
    occ_ids[reg].add(r[oi["occurrence_no"]])
    refs[reg].add(r[oi["reference_no"]])
    taxa_ids[reg] |= {r[oi["accepted_no"]], r[oi["identified_no"]]}
for f in files:
    f.close()
for reg in ("", "_idng"):
    with open(os.path.join(out, f"collections{reg}.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writerow(chead)
        w.writerows(cols[reg])


def subset(name, keep, reg, note=None):
    rows = read([os.path.join(raw, f"{name}.csv")])
    head = next(rows)
    idx = first_index(head)
    kept = [r for r in rows if keep(r, idx)]
    with open(os.path.join(out, f"{name}{reg}.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writerow(head)
        w.writerows(kept)
    return kept, idx


counts = {}
for reg in ("", "_idng"):
    spm, si = subset("specimens", lambda r, i: r[i["occurrence_no"]] in occ_ids[reg] or coll_region.get(r[i["collection_no"]]) == reg, reg)
    spec_ids = {r[si["specimen_no"]] for r in spm}
    refs[reg] |= {r[si["reference_no"]] for r in spm}
    mea, _ = subset("measurements", lambda r, i: r[i["specimen_no"]] in spec_ids, reg)
    ref, _ = subset("references", lambda r, i: r[i["reference_no"]] in refs[reg], reg)
    tax, _ = subset("taxa", lambda r, i: r[i["taxon_no"]] in taxa_ids[reg] or r[i["orig_no"]] in taxa_ids[reg], reg)
    counts[reg or "core"] = {"occurrences": len(occ_ids[reg]), "collections": len(cols[reg]), "specimens": len(spm),
                            "measurements": len(mea), "references": len(ref), "taxa": len(tax)}
with open(os.path.join(out, "region_counts.json"), "w") as f:
    json.dump(counts, f, indent=1)
print(json.dumps(counts))
