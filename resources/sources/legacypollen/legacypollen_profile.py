"""Profile LegacyPollen 1.0, LegacyPollen 2.0 and LegacyAge 1.0 for Q-024.

Usage: python3 legacypollen_profile.py V1_DIR AGE_DIR V2_DIR OUT_TSV RECORDS_TSV

V1_DIR holds the seven regional zips (pollen_counts_<region>.csv inside),
AGE_DIR LegacyAge 1.0's tables, V2_DIR the 2.0 regional count tables
(PANGAEA tab-delimited, with a /* ... */ header). Writes section, metric, value
rows, and one row per record and version to RECORDS_TSV: samples, age span
(median ages), median spacing between samples, median pollen sum, and for
1.0 the LegacyAge dating count and mean age uncertainty. Q-024 screening
counts use the register's thresholds: series length (50, 100, 450 samples;
Dakos et al. 2008 found strong signals only above 450 points) and spacing.
Standard library only.
"""

import collections
import csv
import glob
import io
import os
import statistics
import sys
import zipfile

v1, age, v2, out_tsv, rec_tsv = sys.argv[1:6]
csv.field_size_limit(1 << 30)
out = []


def put(section, metric, value):
    out.append([section, metric, str(value)])


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def counts(c, top=10):
    return "; ".join(f"{k or '(blank)'} {v}" for k, v in c.most_common(top))


def table(stream):
    """A DictReader with the delimiter read off the header: the ".csv" files are tab- or comma-separated."""
    first = stream.readline()
    delim = max("\t,;", key=first.count)
    return csv.DictReader(io.StringIO(first + stream.read()), delimiter=delim), delim


delims = collections.Counter()


def summarise(recs):
    res = {}
    for k, rec in recs.items():
        ages = sorted(rec["ages"])
        gaps = [b - a for a, b in zip(ages, ages[1:]) if b > a]
        res[k] = {"n": len(rec["sums"]), "span": (ages[-1] - ages[0]) if ages else None,
                  "spacing": statistics.median(gaps) if gaps else None,
                  "psum": statistics.median(rec["sums"]) if rec["sums"] else None,
                  "cont": rec["cont"], "site": rec["site"], "oldest": ages[-1] if ages else None}
    return res


def screening(label, res):
    n = [r["n"] for r in res.values()]
    put(label, "records; samples; median samples per record; quartiles", f"{len(res)}; {sum(n)}; {statistics.median(n)}; {statistics.quantiles(n, n=4)}")
    aged = {k: r for k, r in res.items() if r["oldest"] is not None}
    put(label, "records with no median age on any sample", len(res) - len(aged))
    for k in (50, 100, 450):
        put(label, f"records with {k} or more samples: all; with ages", f"{sum(1 for x in n if x >= k)}; {sum(1 for r in aged.values() if r['n'] >= k)}")
    sp = [r["spacing"] for r in res.values() if r["spacing"]]
    put(label, "median gap between successive sample ages (kyr): median over records; quartiles", f"{statistics.median(sp):.3f}; {[round(q, 3) for q in statistics.quantiles(sp, n=4)]}")
    for nmin, smax in ((100, 0.1), (100, 0.2), (450, 0.05)):
        put(label, f"records with {nmin}+ samples and median gap at most {int(smax * 1000)} years; mean gap at most {int(smax * 1000)} years",
            f"{sum(1 for r in res.values() if r['n'] >= nmin and r['spacing'] and r['spacing'] <= smax)}; "
            f"{sum(1 for r in res.values() if r['n'] >= nmin and r['span'] and r['n'] > 1 and r['span'] / (r['n'] - 1) <= smax)}")
    put(label, "records by continent", counts(collections.Counter(r["cont"] for r in res.values())))
    ps = [r["psum"] for r in res.values() if r["psum"]]
    put(label, "median pollen sum per sample: median over records", f"{statistics.median(ps):.0f}")


# LegacyPollen 1.0
v1_rows, v1_taxa = [], set()
for z in sorted(glob.glob(os.path.join(v1, "*_pollen_datasets.zip"))):
    with zipfile.ZipFile(z) as zf:
        m = [n for n in zf.namelist() if n.startswith("pollen_counts_") and n.endswith(".csv")][0]
        r, d = table(io.TextIOWrapper(zf.open(m), encoding="utf-8", errors="replace", newline=""))
        delims[f"1.0 {m}: {d!r}"] += 1
        taxa = [c for c in r.fieldnames if c.endswith("(#)")]
        v1_taxa |= set(taxa)
        rows = list(r)
        for row in rows:
            row["_taxa"] = taxa
        v1_rows += rows
recs1 = collections.defaultdict(lambda: {"ages": [], "sums": [], "cont": "", "site": ""})
for row in v1_rows:
    rec = recs1[row["Dataset_ID"]]
    a = num(row["median_Age (cal. ka BP)"])
    if a is not None:
        rec["ages"].append(a)
    rec["sums"].append(sum(num(row[t]) or 0 for t in row["_taxa"]))
    rec["cont"], rec["site"] = row["Continent"], row["Site_Name"]
res1 = summarise(recs1)
put("v1", "harmonised taxa (count columns, all regions)", len(v1_taxa))
screening("v1", res1)
pct_ids, pct_src = set(), {}
for z in sorted(glob.glob(os.path.join(v1, "*_pollen_datasets.zip"))):
    with zipfile.ZipFile(z) as zf:
        m = [n for n in zf.namelist() if n.startswith("pollen_percentages_") and n.endswith(".csv")][0]
        r, _ = table(io.TextIOWrapper(zf.open(m), encoding="utf-8", errors="replace", newline=""))
        for row in r:
            pct_ids.add(row["Dataset_ID"])
            pct_src[row["Dataset_ID"]] = (row["Data_Source"], row["Continent"])
pct_only = pct_ids - set(res1)
put("v1", "records in the percentage tables; of them, not in the count tables; their sources and continents",
    f"{len(pct_ids)}; {len(pct_only)}; {counts(collections.Counter(pct_src[k] for k in pct_only))}")


def sahul(lat, lon):
    """The catalogue's Sahul region rule (Australia and New Guinea boxes; see the Sahul entries)."""
    if lat is None or lon is None:
        return False
    return (-45 <= lat <= -10.6 and 112 <= lon <= 155) or (-12 <= lat <= 0 and 130.8 <= lon <= 156)

# LegacyAge 1.0
def age_table(name):
    r, d = table(open(os.path.join(age, name), encoding="utf-8", errors="replace", newline=""))
    delims[f"LegacyAge {name}: {d!r}"] += 1
    return list(r)


s1 = age_table("Table-S1_chronological_control_points_metadata.csv")
s3 = age_table("Table-S3_bacon_parameter_settings.csv")
s5 = age_table("Table-S5_legacyage_1_0_chronology.csv")
s6 = age_table("Table-S6_chronology_comparison.csv")
put("formats", "field delimiters found", "; ".join(sorted(delims)))
dates = collections.Counter(r["Dataset_ID"] for r in s1)
measured = collections.Counter(r["Dataset_ID"] for r in s1 if not r["Dating_Method"].startswith("Dates from prior"))
widths = collections.defaultdict(list)
for r in s5:
    lo, hi = num(r["Age_Minimum"]), num(r["Age_Maximum"])
    if lo is not None and hi is not None:
        widths[r["Dataset_ID"]].append(hi - lo)
unc = {k: statistics.mean(v) for k, v in widths.items()}
rec_mean = {r["Dataset_ID"]: num(r["Uncertainty_Record.mean"]) for r in s5}
put("legacyage", "control points; records with control points; records with Bacon settings; records in the chronology table",
    f"{len(s1)}; {len(dates)}; {len({r['Dataset_ID'] for r in s3})}; {len(unc)}")
put("legacyage", "control points by dating method", counts(collections.Counter(r["Dating_Method"] for r in s1), 8))
dn = sorted(dates.values())
put("legacyage", "control points per record, incl. prior information: median; quartiles; records with fewer than 3", f"{statistics.median(dn)}; {statistics.quantiles(dn, n=4)}; {sum(1 for x in dn if x < 3)}")
mn = [measured.get(k, 0) for k in dates]
put("legacyage", "measured dates per record (prior information excluded): median; quartiles; records with fewer than 3",
    f"{statistics.median(mn)}; {statistics.quantiles(mn, n=4)}; {sum(1 for x in mn if x < 3)}")
u = sorted(unc.values())
put("legacyage", "width of the 95% age range (Age_Maximum minus Age_Minimum, yr), mean over each record's depths: median over records; quartiles",
    f"{statistics.median(u):.0f}; {[round(q) for q in statistics.quantiles(u, n=4)]}")
ratio = sorted(rec_mean[k] / unc[k] for k in unc if rec_mean.get(k) and unc[k])
put("legacyage", "Uncertainty_Record.mean divided by that mean width: median; deciles 1 and 9 (it is not the mean width)",
    f"{statistics.median(ratio):.2f}; {statistics.quantiles(ratio, n=10)[0]:.2f}; {statistics.quantiles(ratio, n=10)[-1]:.2f}")
put("legacyage", "chronology source (S6 LegacyAge 1.0_Source)", counts(collections.Counter(list(r.values())[4] for r in s6)))
put("v1", "age-model source of the count records (AgeModel_Source)", counts(collections.Counter(r["AgeModel_Source"] for r in {x["Dataset_ID"]: x for x in v1_rows}.values())))
put("legacyage", "chronology rows (depths); columns", f"{len(s5)}; {list(s5[0].keys())}")
vs = list(s6[0].keys())[2]  # "Original.chronology_VS._Newly..."
put("legacyage", f"comparison with the original chronology ({vs})", counts(collections.Counter(r[vs][:50] for r in s6), 8))
put("legacyage", "1.0 records without LegacyAge dates", sum(1 for k in res1 if k not in dates))

# LegacyPollen 2.0
rows2, fffd = [], 0
for path in sorted(glob.glob(os.path.join(v2, "PANGAEA.*_counts_*.tab"))):
    text = open(path, encoding="utf-8", errors="replace").read()
    fffd += text.count("�")
    body = text[text.find("*/") + 2:].lstrip("\n")
    r = csv.DictReader(io.StringIO(body), delimiter="\t")
    taxa = [c for c in r.fieldnames if c.endswith("[#]")]
    for row in r:
        row["_taxa"] = taxa
        rows2.append(row)
recs2 = collections.defaultdict(lambda: {"ages": [], "sums": [], "cont": "", "site": ""})
for row in rows2:
    rec = recs2[row["ID (Dataset)"]]
    a = num(row["Age [ka BP] (median)"])
    if a is not None:
        rec["ages"].append(a)
    rec["sums"].append(sum(num(row[t]) or 0 for t in row["_taxa"]))
    rec["cont"], rec["site"] = row["Cont"], row["Site"]
res2 = summarise(recs2)
screening("v2", res2)
put("v2", "replacement characters (U+FFFD) in the count tables", fffd)
text = open(os.path.join(v2, "PANGAEA.971802_overview.tab"), encoding="utf-8", errors="replace").read()
ov = list(csv.DictReader(io.StringIO(text[text.find("*/") + 2:].lstrip("\n")), delimiter="\t"))
put("v2", "overview rows; records in the count tables missing from it", f"{len(ov)}; {len(set(res2) - {r['ID (Dataset)'] for r in ov})}")
s3_ids = {r["Dataset_ID"] for r in s3}
aged2 = {k: r for k, r in res2.items() if r["oldest"] is not None}
put("v2", "records with ages; of them, with LegacyAge 1.0 Bacon settings (S3)", f"{len(aged2)}; {sum(1 for k in aged2 if k in s3_ids)}")
for nmin, smax in ((100, None), (100, 0.1), (450, None)):
    sel = [k for k, r in aged2.items() if r["n"] >= nmin and (smax is None or (r["spacing"] and r["spacing"] <= smax))]
    put("v2", f"aged records with {nmin}+ samples{'' if smax is None else ' and median gap at most 100 years'}: count; with LegacyAge settings",
        f"{len(sel)}; {sum(1 for k in sel if k in s3_ids)}")
both = set(res1) & set(res2)
all1 = set(res1) | pct_ids
put("v1 to v2", "count records in 1.0; in 2.0; in both (by dataset id); only in 1.0; only in 2.0",
    f"{len(res1)}; {len(res2)}; {len(both)}; {len(set(res1) - set(res2))}; {len(set(res2) - set(res1))}")
put("v1 to v2", "all 1.0 records (incl. percentage-only): kept in 2.0; dropped; new in 2.0; percentage-only records with counts in 2.0",
    f"{len(all1 & set(res2))}; {len(all1 - set(res2))}; {len(set(res2) - all1)}; {len(pct_only & set(res2))}")
by_depth1, by_depth2 = collections.defaultdict(dict), collections.defaultdict(dict)
for r in v1_rows:
    d, a = num(r["Depth (m)"]), num(r["median_Age (cal. ka BP)"])
    if d is not None and a is not None:
        by_depth1[r["Dataset_ID"]][round(d, 3)] = a
for r in rows2:
    d, a = num(r["Depth sed [m]"]), num(r["Age [ka BP] (median)"])
    if d is not None and a is not None:
        by_depth2[r["ID (Dataset)"]][round(d, 3)] = a
matched, same, moved = 0, 0, set()
for k in both:
    for d, a in by_depth1[k].items():
        if d in by_depth2[k]:
            matched += 1
            same += abs(by_depth2[k][d] - a) <= 0.006
            if abs(by_depth2[k][d] - a) > 0.5:
                moved.add(k)
put("v1 to v2", "samples matched by depth in shared records; with the same median age (within 0.006 ka); records with a matched sample moved by more than 0.5 kyr",
    f"{matched}; {same} ({same / matched:.3f}); {len(moved)}")


def km(a, b):
    import math
    (la1, lo1), (la2, lo2) = a, b
    p = math.pi / 180
    h = math.sin((la2 - la1) * p / 2) ** 2 + math.cos(la1 * p) * math.cos(la2 * p) * math.sin((lo2 - lo1) * p / 2) ** 2
    return 12742 * math.asin(math.sqrt(h))
coords1 = {r["Dataset_ID"]: (num(r["Latitude (DD)"]), num(r["Longitude (DD)"])) for r in v1_rows}
coords2 = {r["ID (Dataset)"]: (num(r["Latitude"]), num(r["Longitude"])) for r in rows2}
shift = [km(coords1[k], coords2[k]) for k in both if None not in coords1.get(k, (None,)) and None not in coords2.get(k, (None,))]
put("v1 to v2", "shared records whose coordinates moved more than 1 km; more than 100 km", f"{sum(1 for s in shift if s > 1)}; {sum(1 for s in shift if s > 100)}")
for label, res, coords in (("v1", res1, coords1), ("v2", res2, coords2)):
    au = [k for k in res if "Indopac" in res[k]["cont"]]
    sa = [k for k in res if sahul(*coords.get(k, (None, None)))]
    put(label, "Indopacific records; records in the Sahul region (Australia and New Guinea boxes); of them with 100+ samples",
        f"{len(au)}; {len(sa)}; {sum(1 for k in sa if res[k]['n'] >= 100)}")

with open(rec_tsv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["version", "dataset_id", "site", "continent", "samples", "span_kyr", "median_spacing_kyr", "median_pollen_sum",
                "legacyage_dates", "legacyage_mean_uncertainty_yr"])
    for label, res in (("1.0", res1), ("2.0", res2)):
        for k in sorted(res, key=lambda x: int(x) if x.isdigit() else 10 ** 9):
            r = res[k]
            w.writerow([label, k, r["site"], r["cont"], r["n"], f"{r['span']:.3f}" if r["span"] is not None else "",
                        f"{r['spacing']:.4f}" if r["spacing"] else "", f"{r['psum']:.0f}" if r["psum"] else "",
                        dates.get(k, "") if label == "1.0" else "", f"{unc[k]:.0f}" if label == "1.0" and unc.get(k) is not None else ""])
with open(out_tsv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["section", "metric", "value"])
    w.writerows(out)
print(len(out), "rows")
