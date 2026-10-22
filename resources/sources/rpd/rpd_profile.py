"""Profile the Reading Palaeofire Database CSV bundle (rpd_csv_files.zip), globally and for Sahul.

Usage: python3 rpd_profile.py RPD_CSV_ZIP OUT_TSV

Sahul regions by coordinates: Australia (lat <= -10.6, lon 112-155, with
Tasmania), Torres Strait (lon 141-144.5, lat -10.6 to -9), New Guinea (lon
130.8-156, lat -12 to 0, with Aru and the Bismarck Archipelago). Writes
long-format counts (table, metric, key, value). Standard library only.
"""

import csv
import io
import statistics
import sys
import zipfile
from collections import Counter, defaultdict

MISSING = {"-999999", "-777777", "-888888"}
out = []


def add(*row):
    out.append(row)


def num(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return None if str(x).strip() in MISSING else v


def region(lat, lon):
    if lat is None or lon is None:
        return None
    if 141 <= lon <= 144.5 and -10.6 < lat <= -9:
        return "torres_strait"
    if lat <= -10.6 and 112 <= lon <= 155:
        return "australia"
    if 130.8 <= lon <= 156 and -12 <= lat <= 0:
        return "new_guinea"
    return None


z = zipfile.ZipFile(sys.argv[1])


def table(stem):
    name = next(n for n in z.namelist() if n.startswith("rpd_csv_files/rpd_" + stem + "_tb_") and n.endswith(".csv"))
    with z.open(name) as f:
        return list(csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")))


add("bundle", "members", "", len(z.namelist()))
add("bundle", "macos_or_ds_store_members", "", sum("__MACOSX" in n or n.endswith(".DS_Store") for n in z.namelist()))
site, entity, sample = table("site"), table("entity"), table("sample")
dates, chron, model = table("date_info"), table("chronology"), table("age_model")
units = {u["ID_UNIT"]: u["UNIT"] for u in table("unit")}
for name, rows in (("site", site), ("entity", entity), ("sample", sample), ("date_info", dates),
                   ("chronology", chron), ("age_model", model), ("unit", units)):
    add("global", "rows", name, len(rows))

reg = {e["ID_ENTITY"]: region(num(e["latitude"]), num(e["longitude"])) for e in entity}
sah = [e for e in entity if reg[e["ID_ENTITY"]]]
ids = {e["ID_ENTITY"] for e in sah}
add("sahul", "entities", "", len(sah))
add("sahul", "sites", "", len({e["ID_SITE"] for e in sah}))
for k, v in Counter(reg[e["ID_ENTITY"]] for e in sah).most_common():
    add("sahul", "entities_by_region", k, v)
for col in ("depositional_context", "measurement_method", "TYPE", "source"):
    for k, v in Counter(e[col] for e in sah).most_common(10):
        add("sahul", f"entities_by:{col}", k, v)
for k, v in Counter(units.get(e["ID_UNIT"], e["ID_UNIT"]) for e in sah).most_common(10):
    add("sahul", "entities_by:unit", k, v)
for k, v in Counter(e["last_updated"][:4] for e in sah).most_common(10):
    add("sahul", "entities_by:last_updated_year", k, v)
site_type = {s["ID_SITE"]: s["site_type"] for s in site}
for k, v in Counter(site_type.get(e["ID_SITE"]) for e in sah).most_common(10):
    add("sahul", "entities_by:site_type", k, v)

s_samples = [s for s in sample if s["ID_ENTITY"] in ids]
add("sahul", "samples", "", len(s_samples))
add("sahul", "samples_charcoal_missing_code", "", sum(s["charcoal_measurement"].strip() in MISSING for s in s_samples))
sample_entity = {s["ID_SAMPLE"]: s["ID_ENTITY"] for s in sample}
new_model = {sample_entity.get(m["ID_SAMPLE"]) for m in model}
add("global", "entities_with_new_age_model", "", len(new_model - {None}))
add("sahul", "entities_with_new_age_model", "", len(ids & new_model))
maxage = defaultdict(float)
for c in chron:
    e = sample_entity.get(c["ID_SAMPLE"])
    a = num(c["original_est_age"])
    if e in ids and a is not None:
        maxage[e] = max(maxage[e], a)
ages = list(maxage.values())
add("sahul", "entities_with_original_ages", "", len(ages))
add("sahul", "original_max_age_median_yr", "", round(statistics.median(ages)))
for thr in (2000, 20000, 50000):
    add("sahul", "entities_original_max_age_ge", thr, sum(a >= thr for a in ages))
s_dates = [d for d in dates if d["ID_ENTITY"] in ids]
add("sahul", "dates", "", len(s_dates))
for k, v in Counter(d["date_type"] for d in s_dates).most_common(8):
    add("sahul", "dates_by:date_type", k, v)
for k, v in Counter(d["age_used"] for d in s_dates).most_common(5):
    add("sahul", "dates_by:age_used", k, v)

with open(sys.argv[2], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
