"""Profile SahulArch: a live OCTOPUS WFS snapshot, optionally against the 2021 Zenodo shapefiles.

Usage: python3 sahularch_profile.py SNAPSHOT_DIR OUT_TSV [ZIP_2021 ...]

SNAPSHOT_DIR holds sahularch_{c14,osl,tl}.csv written by data_mirror.py wfs. Each
ZIP_2021 is a 2021 Zenodo deposit (sahularch_<method>.zip with a shapefile);
its .dbf is read to compare observation IDs and ages with the live layer.
Writes long-format rows (layer, metric, key, value). Standard library only.
"""

import csv
import io
import os
import struct
import sys
import zipfile
from collections import Counter

MISSING = {"", "ND", "NA", "-9999.99", "-9999", "null", "no data", "not specified"}
AGE_FIELD = {"c14": "C14_AGE", "osl": "OSL_AGE", "tl": "TL_AGE"}
out = []


def add(layer, metric, key, value):
    out.append((layer, metric, key, value))


def num(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return None if v <= -9999 else v


def read_dbf(data):
    n, header_len, rec_len = struct.unpack("<xxxxIHH", data[:12])
    fields, pos = [], 32
    while data[pos] != 0x0D:
        name = data[pos:pos + 11].split(b"\0")[0].decode("latin-1")
        fields.append((name, data[pos + 16]))
        pos += 32
    rows = []
    for i in range(n):
        start = header_len + i * rec_len
        rec, off, row = data[start:start + rec_len], 1, {}
        if rec[:1] == b"*":
            continue
        for name, length in fields:
            row[name] = rec[off:off + length].decode("latin-1").strip()
            off += length
        rows.append(row)
    return rows


def profile(layer, rows):
    add(layer, "rows", "", len(rows))
    add(layer, "columns", "", len(rows[0]) - 2)
    for col in ["DBVERNO", "DBDOI", "REGION_REG", "CNTRY", "DIV_ADMIN", "OPENCLOSED", "OCCUPATION", "CONTEXT",
                "AGEMTD", "MATERIAL1", "LUM_MAT", "MINERAL", "AGEMODELAB", "COL_MTD"]:
        if col in rows[0]:
            for k, v in Counter(r[col] for r in rows).most_common(15):
                add(layer, f"by:{col}", k, v)
    for col in ["SITEID", "METASITEID", "SMPID", "OBSID1", "LABID"]:
        if col in rows[0]:
            add(layer, f"distinct:{col}", "", len({r[col] for r in rows}))
    if "SMPID" in rows[0]:
        c = Counter(r["SMPID"] for r in rows)
        add(layer, "samples_with_replicate_observations", "", sum(1 for v in c.values() if v > 1))
        add(layer, "rows_in_replicated_samples", "", sum(v for v in c.values() if v > 1))
    if "LABID" in rows[0]:
        c = Counter(r["LABID"] for r in rows if r["LABID"] not in MISSING)
        add(layer, "lab_codes_on_more_than_one_row", "", sum(1 for v in c.values() if v > 1))
        add(layer, "rows_without_lab_code", "", sum(r["LABID"] in MISSING for r in rows))
    age = AGE_FIELD[layer]
    ages = [num(r.get(age)) for r in rows]
    have = [a for a in ages if a is not None]
    add(layer, "rows_without_age", age, len(ages) - len(have))
    if have:
        add(layer, "age_range", age, f"{min(have)} to {max(have)}")
        unit = 1 if layer == "c14" else 1000
        for thr in (10000, 30000, 40000, 50000):
            add(layer, f"ages_older_than_{thr}_years", age, sum(a * unit > thr for a in have))
    if layer == "c14":
        add(layer, "rows_C14_INF_flagged", "", sum(r.get("C14_INF", "") not in MISSING and r.get("C14_INF") not in ("No", "N", "0") for r in rows))
    years = [int(r["PUBYEAR1"]) for r in rows if r.get("PUBYEAR1", "").isdigit() and int(r["PUBYEAR1"]) > 1800]
    add(layer, "rows_without_first_reference_year", "", len(rows) - len(years))
    if years:
        add(layer, "first_reference_year_range", "", f"{min(years)} to {max(years)}")
    if "C13_VAL" in rows[0]:
        for k, v in Counter(r["C13_VAL"] for r in rows).most_common():
            add(layer, "by:C13_VAL (d13C method)", k, v)
    if "FEATDATED" in rows[0]:
        for k, v in Counter(r["FEATDATED"] for r in rows).most_common(8):
            add(layer, "by:FEATDATED", k, v)
    add(layer, "rows_mentioning_supersede", "AGE_COMMT", sum(("supersed" in r.get("AGE_COMMT", "").lower()) or ("superced" in r.get("AGE_COMMT", "").lower()) for r in rows))
    filled = {col: sum(r[col] not in MISSING for r in rows) / len(rows) for col in rows[0] if col not in ("FID", "geom")}
    for band, lo, hi in (("<10%", 0, 0.1), ("10-50%", 0.1, 0.5), ("50-90%", 0.5, 0.9), (">=90%", 0.9, 1.01)):
        add(layer, "columns_by_share_filled", band, sum(lo <= v < hi for v in filled.values()))
    for col in ["SMPDEPTH", "LABID", "FEATDATED", "C13_VAL", "F14C", "CHEMPREPAB", "PHYSCLEAN", "RECRYST", "SINGULAR",
                "EQUIVDOSE", "DOSERATE", "H2O_USED", "AGEMODELAB", "OD"]:
        if col in filled:
            add(layer, "share_filled", col, round(filled[col], 3))


def main():
    snap, out_path, zips = sys.argv[1], sys.argv[2], sys.argv[3:]
    live = {}
    for layer in ("c14", "osl", "tl"):
        with open(os.path.join(snap, f"sahularch_{layer}.csv"), newline="", encoding="utf-8", errors="replace") as f:
            live[layer] = list(csv.DictReader(f))
        profile(layer, live[layer])
    for z in zips:
        layer = next(m for m in ("c14", "osl", "tl") if m in os.path.basename(z))
        with zipfile.ZipFile(z) as zf:
            old = read_dbf(zf.read(next(n for n in zf.namelist() if n.lower().endswith(".dbf"))))
        key = "OBSID1"
        old_ids, new_ids = {r[key] for r in old}, {r[key] for r in live[layer]}
        add(layer, "v2021_rows", "", len(old))
        add(layer, "v2021_ids_still_live", "", len(old_ids & new_ids))
        add(layer, "v2021_ids_gone", "", len(old_ids - new_ids))
        add(layer, "live_ids_new_since_2021", "", len(new_ids - old_ids))
        age = AGE_FIELD[layer][:10]
        new_age = {r[key]: num(r.get(AGE_FIELD[layer])) for r in live[layer]}
        changed = sum(1 for r in old if r[key] in new_age and num(r.get(age)) is not None and new_age[r[key]] is not None
                      and abs(num(r.get(age)) - new_age[r[key]]) > 1e-6)
        add(layer, "v2021_shared_ids_age_changed", "", changed)
    with open(out_path, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["layer", "metric", "key", "value"])
        w.writerows(out)


if __name__ == "__main__":
    main()
