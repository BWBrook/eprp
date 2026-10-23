# /// script
# requires-python = ">=3.10"
# dependencies = ["openpyxl==3.1.5"]
# ///
"""Cross-check the Australian deposits against FosSahul, PBDB and SahulCHAR, and compare the two Reichgelt versions.

Usage: uv run deposits_overlap.py AU_FOSSIL_DEPOSITS_DIR FOSSAHUL_CSV PBDB_AU_NG_SNAPSHOT SAHULCHAR_SNAPSHOT OUT_TSV

Thylacine and devil dates (White et al. 2018, keyed to FosSahul IDs) against the
current FosSahul release: ID, genus, AgeID and coordinate agreement for the
linked IDs; the deposit's accept/reject decision against its own QR category
(and the A-rated rejections) and the current FosSahul Quality; coverage of
FosSahul's Thylacinus and Sarcophilus
records (linked by ID, new dates found by AgeID, the rest); creators shared by
the two Figshare records. Cloggs Cave: taxon rows, then FosSahul, PBDB and
SahulCHAR. Naracoorte (Weij et al. 2022) against SahulCHAR. The two Reichgelt et
al. versions, sheet by sheet. Writes long-format (table, metric, key, value).
"""

import collections
import csv
import glob
import json
import os
import re
import sys
import unicodedata

import openpyxl

csv.field_size_limit(1 << 30)
out = []
root, fs_csv, pbdb, sc_dir, out_path = sys.argv[1:6]


def add(table, metric, key, value):
    out.append((table, metric, key, value))


def text(v):
    return "" if v is None else str(v).strip()


def is_na(v):
    return text(v).lower() in ("", "na", "none")


def tally(items):
    return "; ".join(f"{k} {n}" for k, n in sorted(collections.Counter(items).items()))


def deposit_file(dep, pattern):
    return glob.glob(os.path.join(root, dep, "raw", "*", pattern))[0]


def sheets(dep):
    wb = openpyxl.load_workbook(deposit_file(dep, "*.xlsx"), read_only=True, data_only=True)
    return {ws.title: [list(r) for r in ws.iter_rows(values_only=True)] for ws in wb.worksheets}


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


fs = read_csv(fs_csv)
fs_by_id = {r["ID"]: r for r in fs}
units = read_csv(os.path.join(sc_dir, "sahulchar_units.csv"))

T = "thylacine_devil"
rows = sheets("thylacine-devil-dates")["Sheet1"]
head = [text(h) for h in rows[0]]
data = [dict(zip(head, r)) for r in rows[1:] if any(text(c) for c in r)]
for d in data:
    d["id"] = "" if is_na(d["Fossahul_ID"]) else text(d["Fossahul_ID"]).split(".")[0]
linked = [d for d in data if d["id"]]
new = [d for d in data if text(d["New Date"]).upper() == "Y"]
add(T, "rows", "", len(data))
add(T, "rows_with_fossahul_id", "", len(linked))
add(T, "distinct_fossahul_ids", "", len({d["id"] for d in linked}))
add(T, "ids_in_current_fossahul", "", sum(d["id"] in fs_by_id for d in linked))
add(T, "rows_by_accepted_rejected", "", tally(text(d["Accepted/Rejected"]) for d in data))
add(T, "rows_flagged_new_date", "", len(new))
add(T, "new_date_rows_by_state", "", tally(text(d["State"]) for d in new))
decisions = sorted({text(d["Accepted/Rejected"]) for d in data})
for dec in decisions:
    add(T, "qr_category_by_decision", dec, tally(text(d["QR Category"]) for d in data if text(d["Accepted/Rejected"]) == dec))
add(T, "new_date_qr_category", "", tally(text(d["QR Category"]) for d in new))
rejected_a = [d for d in data if text(d["Accepted/Rejected"]) == "Rejected" and text(d["QR Category"]) == "A"]
for column in ("DatingTechnique", "Association", "QR sub-Category"):
    add(T, "rejected_rows_rated_A", column, tally(text(d[column]) for d in rejected_a))

pairs = [(d, fs_by_id[d["id"]]) for d in linked if d["id"] in fs_by_id]
add(T, "linked_genus_identical", "", f"{sum(text(d['Genus']) == r['Genus'] for d, r in pairs)} of {len(pairs)}")
add(T, "linked_ageid_identical", "", f"{sum(text(d['AgeID']) == r['AgeID'] for d, r in pairs)} of {len(pairs)}")
add(T, "linked_ageid_deposit_na", "", f"{sum(is_na(d['AgeID']) for d, r in pairs)} (FosSahul also NA for {sum(is_na(d['AgeID']) and is_na(r['AgeID']) for d, r in pairs)})")
other = [(d, r) for d, r in pairs if text(d["AgeID"]) != r["AgeID"] and not is_na(d["AgeID"])]
add(T, "linked_ageid_different_code", "", len(other))
for d, r in other:
    add(T, "linked_ageid_different_code", d["id"], f"deposit {text(d['AgeID'])}, {text(d['State'])}, {text(d['Latitude'])}, {text(d['Longitude'])}; FosSahul {r['AgeID']}, {r['AdministrativeDivision']}, {r['Latitude']}, {r['Longitude']}")


def coordinates(d, r):
    try:
        dlat = abs(float(d["Latitude"]) - float(r["Latitude"]))
        dlon = abs(float(d["Longitude"]) - float(r["Longitude"]))
    except (TypeError, ValueError):
        return "not numeric"
    return "within 0.05 degrees" if dlat <= 0.05 and dlon <= 0.05 else "differ"


add(T, "linked_coordinates", "", tally(coordinates(d, r) for d, r in pairs))
for dec in decisions:
    add(T, "linked_decision_by_current_fossahul_quality", dec, tally(r["Quality"] for d, r in pairs if text(d["Accepted/Rejected"]) == dec))
for cat in sorted({text(d["QR Category"]) for d, r in pairs}):
    add(T, "linked_qr_category_vs_current_quality", cat, tally(r["Quality"] for d, r in pairs if text(d["QR Category"]) == cat))
add(T, "linked_qr_category_equals_current_quality", "", f"{sum(text(d['QR Category']) == r['Quality'] for d, r in pairs)} of {len(pairs)}")

two = [r for r in fs if r["Genus"] in ("Thylacinus", "Sarcophilus")]
linked_ids = {d["id"] for d in linked}
new_ageids = {text(d["AgeID"]) for d in new}
matched = [r for r in two if r["AgeID"] in new_ageids]
matched_ids = {r["ID"] for r in matched}
rest = [r for r in two if r["ID"] not in linked_ids | matched_ids]
add(T, "fossahul_thylacinus_sarcophilus_records", "", len(two))
add(T, "fossahul_records_linked_by_id", "", sum(r["ID"] in linked_ids for r in two))
add(T, "new_dates_found_in_fossahul_by_ageid", "", f"{len({r['AgeID'] for r in matched})} of {len(new_ageids)} AgeIDs in {len(matched)} records; IDs {min(int(r['ID']) for r in matched)}-{max(int(r['ID']) for r in matched)}; Year {tally(r['Year'] for r in matched)}")
add(T, "fossahul_records_not_in_deposit", "", len(rest))
for div in sorted({r["AdministrativeDivision"] for r in two}):
    group = [r for r in two if r["AdministrativeDivision"] == div]
    n_link = sum(r["ID"] in linked_ids for r in group)
    n_new = sum(r["ID"] in matched_ids for r in group)
    add(T, "coverage_by_fossahul_division", div, f"records {len(group)}; linked by ID {n_link}; new dates {n_new}; not in deposit {len(group) - n_link - n_new}")
for div in sorted({r["AdministrativeDivision"] for r in rest}):
    group = [r for r in rest if r["AdministrativeDivision"] == div]
    ids = [int(r["ID"]) for r in group]
    sites = sorted({r["Cave.Site.Deposit"].strip() for r in group})
    where = "; ".join(sites) if len(sites) <= 3 else f"{len(sites)} sites"
    add(T, "not_in_deposit", div, f"{len(group)} records; {where}; region {tally(r['SpecificRegion'].strip() for r in group)}; Year {tally(r['Year'] for r in group)}; Quality {tally(r['Quality'] for r in group)}; IDs {min(ids)}-{max(ids)}")


def surnames(manifest):
    with open(manifest) as f:
        names = json.load(f)["creators"]
    return {unicodedata.normalize("NFKD", n.split()[-1]).encode("ascii", "ignore").decode().lower() for n in names}, len(names)


dep_names, n_dep = surnames(deposit_file("thylacine-devil-dates", "MANIFEST.json"))
fs_names, n_fs = surnames(os.path.join(os.path.dirname(fs_csv), "MANIFEST.json"))
add(T, "record_creators_shared_surnames", "", f"{'; '.join(sorted(dep_names & fs_names))} ({n_dep} creators on the deposit's Figshare record, {n_fs} on the FosSahul 2.0 record)")

C = "cloggs_cave"
cl = sheets("cloggs-cave-mammals")
for label, sheet in (("xu", cl["Cloggs Cave data in XUs"]), ("su", cl["Cloggs Cave data in SUs"])):
    body = [r for r in sheet[1:] if text(r[1])]
    totals = next(r for r in sheet if text(r[0]).lower() == "totals")
    cols = range(2, len(sheet[0]))
    if label == "xu":
        add(C, "taxon_rows", "", len(body))
        indet = [r for r in body if "indet." in text(r[1])]
        add(C, "rows_identified_to_species", "", f"{len(body) - len(indet)} (of which cf. {sum(' cf. ' in text(r[1]) for r in body)})")
        add(C, "rows_indeterminate", "", len(indet))
        non_mammal = [r for r in body if text(r[1]).split()[0] in ("Agamidae", "Scincidae", "Varanus", "Anura", "Aves")]
        add(C, "non_mammal_rows", "", f"{len(non_mammal)}: {'; '.join(text(r[1]) for r in non_mammal)}; to species: {sum('indet.' not in text(r[1]) for r in non_mammal)}")
    add(C, f"{label}_totals_row_sum", "", sum(totals[j] for j in cols if isinstance(totals[j], (int, float))))
    mismatched = [j for j in cols if sum(r[j] for r in body if isinstance(r[j], (int, float))) != (totals[j] if isinstance(totals[j], (int, float)) else 0)]
    add(C, f"{label}_totals_row_equals_column_sums", "", "yes" if not mismatched else f"no: columns {', '.join(text(sheet[0][j]) for j in mismatched)}")
add(C, "fossahul_records", "", sum("clogg" in r["Cave.Site.Deposit"].lower() for r in fs))
with open(os.path.join(pbdb, "collections.csv"), newline="", encoding="utf-8") as f:
    rd = csv.reader(f)
    h = next(rd)
    n = h.index("collection_name")
    add(C, "pbdb_collections", "", sum("clogg" in r[n].lower() for r in rd))
add(C, "sahulchar_units", "", sum("clogg" in (u["SITENAME"] + u["UNITNAME"]).lower() for u in units))

W = "naracoorte_weij"
DOI = "10.1038/s43247-022-00538-y"
weij_units = [u for u in units if u["REFDOI"] == DOI]
add(W, "sahulchar_units_citing_doi", "", f"{len(weij_units)}: {'; '.join(sorted(u['UNITNAME'] for u in weij_units))}")
obs = [o for o in read_csv(os.path.join(sc_dir, "sahulchar.csv")) if DOI in (o["REFDOI1"], o["REFDOI2"], o["REFDOI3"])]
add(W, "sahulchar_observation_rows_citing_doi", "", len(obs))
add(W, "sahulchar_observation_rows_by_type", "", tally(o["WHATAMI"] for o in obs))
add(W, "sahulchar_observation_units", "", f"{len({o['UNITNAME'] for o in obs})}: {tally(o['UNITNAME'] for o in obs)}")
add(W, "sahulchar_observation_samples", "", len({o["SMPNAME"] for o in obs}))
t3 = sheets("naracoorte-charcoal-pollen")["Supplementary Data 1 Table 3"]
h3 = next(i for i, r in enumerate(t3) if text(r[1]) == "Sample ID")
charcoal_col = [text(c) for c in t3[h3]].index("charcoal conc.")
rows3 = [r for r in t3[h3 + 1 :] if text(r[1])]
dep_char = collections.Counter(float(r[charcoal_col]) for r in rows3 if isinstance(r[charcoal_col], (int, float)))
sc_char = collections.Counter(float(o["CHARVALUES"]) for o in obs if o["WHATAMI"] == "particles counted")
both = sum((dep_char & sc_char).values())
add(W, "deposit_table3_sample_rows", "", len(rows3))
add(W, "deposit_table3_rows_with_charcoal", "", sum(dep_char.values()))
add(W, "charcoal_values_in_both", "", both)
add(W, "sahulchar_charcoal_values_not_in_deposit", "", sum(sc_char.values()) - both)

R = "reichgelt_versions"
dryad, revised = sheets("reichgelt-eocene-dryad"), sheets("reichgelt-eocene-revised")


def norm(c):
    return re.sub(r"(https?://(dx\.)?doi\.org/)+", "", c) if isinstance(c, str) else c


def cells(rows):
    return {(i, j): c for i, r in enumerate(rows) for j, c in enumerate(r) if text(c)}


def doi_forms(rows):
    forms = (
        "double doi.org prefix" if x.startswith("https://doi.org/https://doi.org/") else "single doi.org prefix" if x.startswith("https://doi.org/") else "bare"
        for r in rows for x in r if isinstance(x, str) and "10.15468/" in x
    )
    return tally(forms)


add(R, "sheets", "", f"{len(dryad)} in both" if list(dryad) == list(revised) else "sheet lists differ")
for s in dryad:
    a, b = cells(dryad[s]), cells(revised[s])
    position = sum(a.get(k) != b.get(k) for k in a.keys() | b.keys())
    ca, cb = collections.Counter(norm(c) for c in a.values()), collections.Counter(norm(c) for c in b.values())
    rows_a = collections.Counter(tuple(norm(c) for c in r if text(c)) for r in dryad[s] if any(text(c) for c in r))
    rows_b = collections.Counter(tuple(norm(c) for c in r if text(c)) for r in revised[s] if any(text(c) for c in r))
    add(R, "sheet_comparison", s, f"cells differing by position {position}; cells only in Dryad copy {sum((ca - cb).values())}, only in revised {sum((cb - ca).values())} (after stripping doi.org prefixes); same rows in any order {'yes' if rows_a == rows_b else 'no'}")
    if cb - ca:
        add(R, "cells_only_in_revised", s, "; ".join(f"{k} x{n}" for k, n in (cb - ca).items()))
    if ca - cb:
        add(R, "cells_only_in_dryad_copy", s, "; ".join(f"{k} x{n}" for k, n in (ca - cb).items()))
add(R, "s6_doi_cell_forms", "dryad copy", doi_forms(dryad["S6"]))
add(R, "s6_doi_cell_forms", "revised", doi_forms(revised["S6"]))


def zipped_csv(deposit, member):
    import io
    import zipfile
    z = glob.glob(os.path.join(root, deposit, "raw", "*", "*.zip"))[0]
    with zipfile.ZipFile(z) as zf:
        name = next(n for n in zf.namelist() if n.endswith(member))
        return list(csv.DictReader(io.TextIOWrapper(zf.open(name), encoding="utf-8-sig", errors="replace")))


C = "craffey_ediacaran"
occ = zipped_csv("craffey-ediacaran-cooccurrence", "Occurrence Data.csv")
add(C, "occurrences", "", len(occ))
add(C, "collections", "", len({r["collection_no"] for r in occ}))
add(C, "genera", "", len({r["genus"] for r in occ}))


def australian(r):
    try:
        lat, lng = float(r["lat"]), float(r["lng"])
    except ValueError:
        return False
    return -45 <= lat <= -10.6 and 112 <= lng <= 155


au_occ = [r for r in occ if australian(r)]
add(C, "occurrences_in_australia", "", len(au_occ))
add(C, "collections_in_australia", "", len({r["collection_no"] for r in au_occ}))
with open(os.path.join(pbdb, "collections.csv"), newline="", encoding="utf-8") as f:
    pbdb_colls = {r["collection_no"] for r in csv.DictReader(f)}
add(C, "australian_collections_in_pbdb_au_extract", "", len({r["collection_no"] for r in au_occ} & pbdb_colls))
for k, n in collections.Counter(r["formation"] for r in au_occ).most_common(6):
    add(C, "australian_occurrences_by:formation", k, n)

K = "couzens_enamel"
main = zipped_csv("couzens-kangaroo-enamel", "data/main_data_file.csv")
add(K, "rows", "", len(main))
add(K, "specimens", "", len({r["Specimen_number"] for r in main}))
add(K, "taxa", "", len({r["Taxon"] for r in main}))
add(K, "assemblages", "", len({r["Assemblage"] for r in main if r["Assemblage"] not in ("", "NA")}))
for k, n in collections.Counter(r["Status"] for r in main).most_common():
    add(K, "rows_by:Status", k, n)
ages = [float(r["Est_age_Ma"]) for r in main if re.fullmatch(r"[\d.]+", r["Est_age_Ma"] or "")]
add(K, "est_age_ma_range", "", f"{min(ages)} to {max(ages)}" if ages else "none")
fs_genera = {r["Genus"].strip() for r in fs}
k_genera = {r["Taxon"].split("_")[0].split()[0] for r in main if r["Taxon"]}
add(K, "genera", "", len(k_genera))
add(K, "genera_in_fossahul", "", len(k_genera & fs_genera))

with open(out_path, "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
