"""Profile SISALv3 (sisalv3_database_mysql_csv.zip from ORA), globally and for Sahul and Wallacea.

Usage: python3 sisal_profile.py SISAL_CSV_ZIP OUT_TSV

Sahul regions as in rpd_profile.py; "wallacea" is lat -12 to 0, lon 115 to
130.8 (Flores, Sulawesi, Timor). Ages are years BP (1950). Writes long-format
counts (table, metric, key, value), including one row per Sahul site.
Standard library only.
"""

import csv
import io
import sys
import zipfile
from collections import Counter, defaultdict

csv.field_size_limit(1 << 30)
MODELS = ["lin_interp", "lin_reg", "Bchron", "Bacon", "OxCal", "copRa", "StalAge"]
out = []


def add(*row):
    out.append(row)


def num(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return None if v <= -999 else v


def region(lat, lon):
    if lat is None or lon is None:
        return None
    if 141 <= lon <= 144.5 and -10.6 < lat <= -9:
        return "torres_strait"
    if -45 <= lat <= -10.6 and 112 <= lon <= 155 and not (lon < 121 and lat > -17):
        return "australia"
    if 130.8 <= lon <= 156 and -12 <= lat <= 0:
        return "new_guinea"
    if 115 <= lon < 130.8 and -12 <= lat <= 0:
        return "wallacea"
    return None


z = zipfile.ZipFile(sys.argv[1])


def table(name):
    with z.open("sisalv3_database_mysql_csv/sisalv3_csv/" + name + ".csv") as f:
        return list(csv.DictReader(io.TextIOWrapper(f, encoding="utf-8", errors="replace")))


site, entity, sample, dating = table("site"), table("entity"), table("sample"), table("dating")
orig, sisal = table("original_chronology"), table("sisal_chronology")
iso = {t: {r["sample_id"] for r in table(t)} for t in ("d18O", "d13C")}
te = {t: {r["sample_id"] for r in table(t)} for t in ("Mg_Ca", "Sr_Ca", "Ba_Ca", "U_Ca", "P_Ca")}
for name, rows in (("site", site), ("entity", entity), ("sample", sample), ("dating", dating),
                   ("original_chronology", orig), ("sisal_chronology", sisal)):
    add("global", "rows", name, len(rows))
for k, v in Counter(e["entity_status"] for e in entity).most_common():
    add("global", "entities_by:status", k, v)
add("global", "samples_with_sisal_chronology", "", len({r["sample_id"] for r in sisal}))

site_reg = {s["site_id"]: region(num(s["latitude"]), num(s["longitude"])) for s in site}
site_name = {s["site_id"]: s["site_name"] for s in site}
ent_site = {e["entity_id"]: e["site_id"] for e in entity}
smp_ent = {s["sample_id"]: s["entity_id"] for s in sample}
age = defaultdict(list)
for r in orig:
    a = num(r["interp_age"])
    if a is not None:
        age[smp_ent.get(r["sample_id"])].append(a)
modelled = defaultdict(set)
for r in sisal:
    for m in MODELS:
        if num(r.get(m + "_age")) is not None:
            modelled[smp_ent.get(r["sample_id"])].add(m)

for reg in ("australia", "new_guinea", "torres_strait", "wallacea"):
    sites = [s for s, r in site_reg.items() if r == reg]
    ents = [e for e in entity if site_reg.get(e["site_id"]) == reg]
    ids = {e["entity_id"] for e in ents}
    smps = [s for s in sample if s["entity_id"] in ids]
    sids = {s["sample_id"] for s in smps}
    t = f"region:{reg}"
    add(t, "sites", "", len(sites))
    add(t, "entities", "", len(ents))
    if not ents:
        continue
    for k, v in Counter(e["entity_status"] for e in ents).most_common():
        add(t, "entities_by:status", k, v)
    add(t, "samples", "", len(smps))
    for k in ("d18O", "d13C"):
        add(t, f"samples_with_{k}", "", len(sids & iso[k]))
    for k, s in te.items():
        add(t, f"entities_with_{k}", "", len({smp_ent[x] for x in sids & s}))
    d = [r for r in dating if r["entity_id"] in ids]
    add(t, "dating_rows", "", len(d))
    for k, v in Counter(r["date_type"] for r in d).most_common(8):
        add(t, "dating_by:date_type", k, v)
    current = [e for e in ents if e["entity_status"] != "superseded"]
    add(t, "current_entities_with_any_sisal_model", "", sum(bool(modelled[e["entity_id"]]) for e in current))
    add(t, "current_entities_without_sisal_model", "", sum(not modelled[e["entity_id"]] for e in current))
    oldest = {e["entity_id"]: max(age[e["entity_id"]]) for e in current if age[e["entity_id"]]}
    for thr in (2000, 20000, 40000):
        add(t, "current_entities_oldest_age_ge", thr, sum(a >= thr for a in oldest.values()))
    add(t, "samples_aragonite", "", sum("aragonite" in s["mineralogy"] for s in smps))
    add(t, "samples_aragonite_not_corrected", "", sum("aragonite" in s["mineralogy"] and s["arag_corr"] == "no" for s in smps))
    for k, v in Counter(site_name[ent_site[s["entity_id"]]] for s in smps if "aragonite" in s["mineralogy"]).most_common(5):
        add(t, "aragonite_samples_by:site", k, v)
    cur_ids = {e["entity_id"] for e in current}
    lgm = Counter()
    for r in orig:
        e = smp_ent.get(r["sample_id"])
        a = num(r["interp_age"])
        if e in cur_ids and a is not None and 18000 <= a <= 24000:
            lgm[e] += 1
    add(t, "current_entities_with_samples_18_24ka", "", len(lgm))
    add(t, "sites_with_samples_18_24ka", "", len({ent_site[e] for e in lgm}))
    add(t, "samples_18_24ka", "", sum(lgm.values()))
    name = {e["entity_id"]: e["entity_name"] for e in ents}
    for e, n in lgm.most_common():
        add(t, "samples_18_24ka_by:entity", f'{site_name[ent_site[e]]} {name[e]}', n)
    for k, v in Counter("0-2 ka" if a < 2000 else "2-10 ka" if a < 10000 else "10-20 ka" if a < 20000 else ">=20 ka" for a in oldest.values()).most_common():
        add(t, "current_entities_by:oldest_age", k, v)
    for sid in sorted(sites, key=lambda s: site_name[s]):
        se = [e for e in current if e["site_id"] == sid]
        ages = [a for e in se for a in age[e["entity_id"]]]
        n = sum(1 for s in smps if ent_site[s["entity_id"]] == sid)
        span = f"{min(ages):.0f} to {max(ages):.0f} BP" if ages else "no ages"
        add(t, "site", site_name[sid], f"{len(se)} current entities; {n} samples; {span}")

with open(sys.argv[2], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
