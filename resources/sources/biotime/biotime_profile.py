"""Profile BioTIME 2.0 for the EPRP questions (Q-025 local loss, Q-028 modern winners).

Usage: python3 biotime_profile.py RAWDATA_ZIP METADATA_CSV OUT_TSV

RAWDATA_ZIP is the St Andrews CSV export (biotime_v2_rawdata_2025.zip);
METADATA_CSV the study table from Zenodo. Writes section, metric, value rows:
study counts by realm, taxa, abundance type and licence (contact and e-mail
columns are never read into the output); records, species and years; per
study, the number of distinct years sampled; and, for studies with ten or more
sampled years, taxon names recorded in a study's first three sampled years
but in none of its last three, pooled over the study and, in a second pass,
at each site (study, latitude, longitude) sampled in both windows. BioTIME
drops zero abundances (samples record whole assemblages, so absences can be
rebuilt per sample), and effort varies between years and sites: these are
descriptive counts, neither floors nor ceilings on local loss. Standard
library only.
"""

import collections
import csv
import io
import re
import statistics
import sys
import zipfile

raw_zip, meta_csv, out_tsv = sys.argv[1:4]
csv.field_size_limit(1 << 30)
out = []


def put(section, metric, value):
    out.append([section, metric, str(value)])


def counts(c, top=12):
    return "; ".join(f"{k or '(blank)'} {v}" for k, v in c.most_common(top))


def licence(text):
    t = (text or "").upper()
    if not t.strip():
        return "blank"
    if re.search(r"\bNC\b|NON-?\s?COMMERCIAL", t):  # first: "ODbL (CC-by-NC)" is non-commercial
        return "non-commercial (CC BY-NC or ODbL with NC)"
    if "ODBL" in t:
        return "ODbL (share-alike)"
    if re.search(r"\bSA\b|SHARE-?\s?ALIKE", t):
        return "CC BY-SA"
    if re.search(r"ODC[- ]?BY", t):
        return "ODC-By"
    if re.search(r"GOVERNMENT|LICENCE OUVERTE|OPEN DATA LICENSE|\bOGL\b", t):
        return "open government or agency licence"
    if re.search(r"CC0|PUBLIC DOMAIN|PDDL|DPPL", t):
        return "CC0 or public domain"
    if re.search(r"CC[ -]*BY|ATTRIBUTION", t):
        return "CC BY"
    if "CITATION" in t:
        return "citation required, no licence named"
    if t.strip().startswith("PUBLIC"):
        return "public, no licence named"
    return "other"


with open(meta_csv, newline="", encoding="utf-8-sig", errors="replace") as f:
    meta = list(csv.DictReader(f))
meta_by_id = {m["STUDY_ID"]: m for m in meta}
put("studies", "studies in the metadata", len(meta))
for col in ("REALM", "TAXA", "AB_BIO", "CLIMATE", "PROTECTED_AREA"):
    put("studies", f"by {col}", counts(collections.Counter(m[col] for m in meta)))
put("studies", "by licence class (PERMISSIONS, classified)", counts(collections.Counter(licence(m["PERMISSIONS"]) for m in meta)))
put("studies", "PERMISSIONS as written, most common",
    counts(collections.Counter((m["PERMISSIONS"] or "")[:60] for m in meta if "@" not in (m["PERMISSIONS"] or "")), top=8))
area = sorted(float(m["AREA_SQ_KM"]) for m in meta if re.fullmatch(r"[0-9.eE+-]+", m["AREA_SQ_KM"] or ""))
if area:
    q = statistics.quantiles(area, n=4)
    put("studies", "study extent AREA_SQ_KM: n; min, quartiles, max", f"{len(area)}; {area[0]:g}, {q[0]:g}, {q[1]:g}, {q[2]:g}, {area[-1]:g}")

years_of = collections.defaultdict(set)
pres = collections.defaultdict(lambda: collections.defaultdict(set))
resolution_of = {}
rows, ab_na, bio_na, species, res, taxon, realm_rows = 0, 0, 0, set(), collections.Counter(), collections.Counter(), collections.Counter()
ymin, ymax = 9999, 0
with zipfile.ZipFile(raw_zip) as z:
    member = [m for m in z.infolist() if m.filename.endswith(".csv")][0]
    r = csv.reader(io.TextIOWrapper(z.open(member), encoding="utf-8", errors="replace", newline=""))
    h = next(r)
    ix = {k: h.index(k) for k in ("ABUNDANCE", "BIOMASS", "YEAR", "STUDY_ID", "valid_name", "resolution", "taxon")}
    for row in r:
        rows += 1
        s, y, sp = row[ix["STUDY_ID"]], row[ix["YEAR"]], row[ix["valid_name"]]
        ab_na += row[ix["ABUNDANCE"]] in ("", "NA")
        bio_na += row[ix["BIOMASS"]] in ("", "NA")
        species.add(sp)
        res[row[ix["resolution"]]] += 1
        resolution_of[(s, sp)] = row[ix["resolution"]]
        taxon[row[ix["taxon"]]] += 1
        realm_rows[meta_by_id.get(s, {}).get("REALM", "not in metadata")] += 1
        if y.isdigit():
            yi = int(y)
            ymin, ymax = min(ymin, yi), max(ymax, yi)
            years_of[s].add(yi)
            pres[s][sp].add(yi)
put("records", "rows; studies; distinct valid names", f"{rows}; {len(years_of)}; {len(species)}")
put("records", "years, first and last", f"{ymin}; {ymax}")
put("records", "rows without abundance; without biomass", f"{ab_na}; {bio_na}")
put("records", "rows by taxonomic resolution", counts(res))
put("records", "rows by taxon group", counts(taxon))
put("records", "rows by realm", counts(realm_rows))
put("records", "studies in the data but not in the metadata", sum(1 for s in years_of if s not in meta_by_id))

n_years = sorted(len(v) for v in years_of.values())
put("series", "distinct years sampled per study: median; quartiles", f"{statistics.median(n_years)}; {statistics.quantiles(n_years, n=4)}")
for k in (2, 5, 10, 20, 30):
    put("series", f"studies sampled in {k} or more distinct years", sum(1 for n in n_years if n >= k))

windows = {}
for s, ys in years_of.items():
    if len(ys) >= 10:
        order = sorted(ys)
        windows[s] = (set(order[:3]), set(order[-3:]))
pairs = gone = sp_pairs = sp_gone = 0
gone_by_realm, pairs_by_realm = collections.Counter(), collections.Counter()
for s, (first, last) in windows.items():
    realm = meta_by_id.get(s, {}).get("REALM", "not in metadata")
    for sp, spy in pres[s].items():
        if spy & first:
            pairs += 1
            pairs_by_realm[realm] += 1
            lost = not spy & last
            gone += lost
            gone_by_realm[realm] += lost
            if resolution_of.get((s, sp)) == "species":
                sp_pairs += 1
                sp_gone += lost
put("local loss", f"studies with 10+ sampled years ({len(windows)}), pooled over the study: taxon names recorded in the first three sampled years; of them, none in the last three",
    f"{pairs}; {gone} ({gone / pairs:.3f})" if pairs else "0")
put("local loss", "the same, names at species resolution only", f"{sp_pairs}; {sp_gone} ({sp_gone / sp_pairs:.3f})" if sp_pairs else "0")
put("local loss", "the same by realm (pairs; not in the last three)",
    "; ".join(f"{k} {pairs_by_realm[k]}; {gone_by_realm[k]}" for k in sorted(pairs_by_realm)))

# second pass: the same at each site (study, latitude, longitude) sampled in both windows
site_first, site_last = collections.defaultdict(set), collections.defaultdict(set)
with zipfile.ZipFile(raw_zip) as z:
    member = [m for m in z.infolist() if m.filename.endswith(".csv")][0]
    r = csv.reader(io.TextIOWrapper(z.open(member), encoding="utf-8", errors="replace", newline=""))
    h = next(r)
    ix = {k: h.index(k) for k in ("YEAR", "STUDY_ID", "valid_name", "LATITUDE", "LONGITUDE")}
    for row in r:
        s = row[ix["STUDY_ID"]]
        if s not in windows or not row[ix["YEAR"]].isdigit():
            continue
        y, site = int(row[ix["YEAR"]]), (s, row[ix["LATITUDE"]], row[ix["LONGITUDE"]])
        if y in windows[s][0]:
            site_first[site].add(row[ix["valid_name"]])
        if y in windows[s][1]:
            site_last[site].add(row[ix["valid_name"]])
both = [site for site in site_first if site in site_last]
sp_site = sum(len(site_first[site]) for site in both)
lost_site = sum(len(site_first[site] - site_last[site]) for site in both)
put("local loss", "sites (study, latitude, longitude) sampled in both windows; studies; names in the first window; of them, not recorded at that site in the last",
    f"{len(both)}; {len({site[0] for site in both})}; {sp_site}; {lost_site} ({lost_site / sp_site:.3f})" if sp_site else "0")

with open(out_tsv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["section", "metric", "value"])
    w.writerows(out)
print(len(out), "rows")
