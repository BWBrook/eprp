"""Profile GRIIS: the checklists on GBIF and the 2022 Country Compendium (Q-047, Q-028).

Usage: python3 griis_profile.py CHECKLISTS_RAW DATASETS_TSV COMPENDIUM_CSV OUT_TSV

CHECKLISTS_RAW is one dated snapshot of the checklist archives (Darwin Core
Archives: taxon, distribution, species-profile files); DATASETS_TSV its
dataset index. Writes section, metric, value rows: checklists by kind and by
year last modified; taxa and distribution rows; occurrence status,
establishment, invasiveness and the share of distribution rows with an event
date; kingdoms; and the Compendium's countries and records for comparison.
Standard library only.
"""

import collections
import csv
import io
import os
import re
import sys
import zipfile

raw, datasets_tsv, compendium, out_tsv = sys.argv[1:5]
csv.field_size_limit(1 << 30)
out = []


def put(section, metric, value):
    out.append([section, metric, str(value)])


def counts(c, top=12):
    return "; ".join(f"{k or '(blank)'} {v}" for k, v in c.most_common(top))


def kind(title):
    if re.search(r"protected area|conservation area|ramsar|national park", title, re.I):
        return "protected area"
    if "Global Invasive Species Database" in title:
        return "GISD"
    return "GRIIS"


def unit(title):
    return re.sub(r"^Global Register of Introduced and Invasive Species\s*-\s*", "", title)


ds = list(csv.DictReader(open(datasets_tsv, encoding="utf-8"), delimiter="\t"))
put("checklists", "datasets; with an archive", f"{len(ds)}; {sum(1 for d in ds if d['file'])}")
put("checklists", "by kind (title)", counts(collections.Counter(kind(d["title"]) for d in ds)))
put("checklists", "by year last modified on GBIF", counts(collections.Counter(d["modified"][:4] for d in ds), 10))
def lic(url):
    m = re.search(r"licenses/([a-z-]+)/([\d.]+)", url)
    return f"CC {m.group(1).upper()} {m.group(2)}" if m else "CC0" if "publicdomain/zero" in url else url or "unspecified"


put("checklists", "by licence", counts(collections.Counter(lic(d["license"]) for d in ds)))

agg = collections.defaultdict(collections.Counter)
dated, dist_rows, taxa_rows, per_list, dated_list_rows = 0, 0, 0, [], 0
nat_taxa = nat_dist = 0
stamp_lists = stamp_rows = spread_lists = spread_rows = 0
path_lists = path_rows = doe_lists = doe_rows = intro_remarks = native_desc = 0
for d in ds:
    if not d["file"] or kind(d["title"]) != "GRIIS":
        continue
    with zipfile.ZipFile(os.path.join(raw, d["file"])) as z:
        names = z.namelist()
        for n in names:
            agg["files in the archives"][n.split("/")[-1]] += 1

        def rows(name):
            if name not in names:
                return []
            return list(csv.DictReader(io.TextIOWrapper(z.open(name), encoding="utf-8", errors="replace", newline=""),
                                       delimiter="\t", quoting=csv.QUOTE_NONE))

        tx, di, sp = rows("taxon.txt"), rows("distribution.txt"), rows("speciesprofile.txt")
        oc, de = rows("occurrence.txt"), rows("description.txt")
    intro_remarks += sum(1 for r in oc if "introduction" in (r.get("eventRemarks") or "").lower())
    native_desc += sum(1 for r in de if "native range" in (r.get("type") or "").lower())
    taxa_rows += len(tx)
    dist_rows += len(di)
    per_list.append(len(tx))
    if ", " not in unit(d["title"]):  # "Alaska, United States", "Ailuk Atoll, Marshall Islands" are nested units
        nat_taxa += len(tx)
        nat_dist += len(di)
    years = [int(m.group(0)) for r in di for m in [re.search(r"\d{4}", r.get("eventDate") or "")] if m]
    if years:
        recent = sum(1 for y in years if y >= 2015) / len(years)
        if recent >= 0.8:
            stamp_lists, stamp_rows = stamp_lists + 1, stamp_rows + len(years)
        else:
            spread_lists, spread_rows = spread_lists + 1, spread_rows + len(years)
    n_path = sum(1 for r in di if (r.get("pathway") or "").strip())
    path_lists, path_rows = path_lists + (n_path > 0), path_rows + n_path
    n_doe = sum(1 for r in di if (r.get("degreeOfEstablishment") or "").strip())
    doe_lists, doe_rows = doe_lists + (n_doe > 0), doe_rows + n_doe
    for r in tx:
        agg["kingdom"][r.get("kingdom", "")] += 1
        agg["taxonomicStatus"][r.get("taxonomicStatus", "")] += 1
    n_dated = 0
    for r in di:
        agg["occurrenceStatus"][r.get("occurrenceStatus", "").lower()] += 1
        agg["establishmentMeans"][r.get("establishmentMeans", "").lower()] += 1
        e = (r.get("eventDate") or "").strip()
        if e:
            n_dated += 1
            agg["eventDate shape"][re.sub(r"\d", "9", e)[:20]] += 1
    dated += n_dated
    dated_list_rows += len(di) if n_dated else 0
    agg["checklists with event dates"]["yes" if n_dated else "no"] += 1
    for r in sp:
        agg["isInvasive"][r.get("isInvasive", "").lower()] += 1
put("records", "GRIIS checklists read; taxon rows; distribution rows", f"{len(per_list)}; {taxa_rows}; {dist_rows}")
put("records", "the same for lists whose unit is not nested (no 'unit, country' title): lists; taxon rows; distribution rows",
    f"{sum(1 for d in ds if d['file'] and kind(d['title']) == 'GRIIS' and ', ' not in unit(d['title']))}; {nat_taxa}; {nat_dist}")
put("records", "distribution rows with an event date (share of all rows; of the rows in lists that give dates)",
    f"{dated} ({dated / dist_rows:.3f}; {dated / dated_list_rows:.3f})" if dated_list_rows else "0")
put("event dates", "lists whose dates are 80%+ from 2015 on (entry stamps, inferred): lists; dated rows",
    f"{stamp_lists}; {stamp_rows}")
put("event dates", "other dated lists (dates spread over time): lists; dated rows", f"{spread_lists}; {spread_rows}")
put("event dates", "occurrence.txt rows whose eventRemarks give an introduction date", intro_remarks)
put("other fields", "distribution pathway filled: lists; rows", f"{path_lists}; {path_rows}")
put("other fields", "distribution degreeOfEstablishment filled: lists; rows", f"{doe_lists}; {doe_rows}")
put("other fields", "description.txt rows typed native range", native_desc)
for k in ("files in the archives", "checklists with event dates", "eventDate shape", "kingdom", "taxonomicStatus",
          "occurrenceStatus", "establishmentMeans", "isInvasive"):
    put("records", k, counts(agg[k]))

with open(compendium, newline="", encoding="utf-8-sig", errors="replace") as f:
    comp = list(csv.DictReader(f))
put("compendium", "rows; countries; distinct species", f"{len(comp)}; {len({r['countryCode_alpha3'] for r in comp})}; {len({r['species'] for r in comp})}")
put("compendium", "isInvasive", counts(collections.Counter(r["isInvasive"] for r in comp)))
put("compendium", "kingdom", counts(collections.Counter(r["kingdom"] for r in comp)))

with open(out_tsv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["section", "metric", "value"])
    w.writerows(out)
print(len(out), "rows")
