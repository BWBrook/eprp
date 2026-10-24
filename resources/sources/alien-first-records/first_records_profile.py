"""Profile the Alien Species First Records Database (Q-047, Q-028).

Usage: python3 first_records_profile.py V4_DIR V31_XLSX OUT_TSV

V4_DIR holds the v4.0 public files (semicolon-separated records, location
and taxonomy tables); V31_XLSX is v3.1's free-data workbook, of which only the
row count is read. Writes section, metric, value rows: records, taxa and
locations; the share with a first-record year, its range and records per
period; confidence, status, establishment and pathway fields; taxon groups
and kingdoms; records by continent. Standard library only.
"""

import collections
import csv
import os
import re
import sys
import zipfile

v4, v31, out_tsv = sys.argv[1:4]
csv.field_size_limit(1 << 30)
out = []


def put(section, metric, value):
    out.append([section, metric, str(value)])


def counts(c, top=12):
    return "; ".join(f"{k or '(blank)'} {v}" for k, v in c.most_common(top))


def table(name, delim=","):
    with open(os.path.join(v4, name), newline="", encoding="utf-8-sig", errors="replace") as f:
        return list(csv.DictReader(f, delimiter=delim))


with open(os.path.join(v4, "FirstRecords_dataset_public_v4.0.csv"), "rb") as f:
    raw_bytes = f.read()
try:
    raw_bytes.decode("utf-8")
    utf8 = "valid UTF-8"
except UnicodeDecodeError as e:
    utf8 = f"not valid UTF-8 (first bad byte at offset {e.start}; {raw_bytes.decode('utf-8', 'replace').count(chr(0xFFFD))} replacement characters)"
put("records", "records file encoding", utf8)
rec = table("FirstRecords_dataset_public_v4.0.csv", ";")
loc_rows = table("FirstRecords_location_table_public_v4.0.csv")
loc = {r["locationID"]: r for r in loc_rows}
tax = {r["taxonID"]: r for r in table("FirstRecords_taxonomy_table_public_v4.0.csv")}
blank = [r for r in rec if not r["locationID"].strip()]
put("records", "rows; distinct taxa; distinct locations (blank excluded)",
    f"{len(rec)}; {len({r['taxonID'] for r in rec})}; {len({r['locationID'] for r in rec} - {''})}")
put("records", "rows with no location identifier; their verbatim locations",
    f"{len(blank)}; {counts(collections.Counter(r['verbatimLocation'] for r in blank), 6)}")
put("records", "location table rows; distinct location ids; taxa in the taxonomy table", f"{len(loc_rows)}; {len(loc)}; {len(tax)}")
years = [int(r["firstRecordEvent"]) for r in rec if re.fullmatch(r"-?\d+", r["firstRecordEvent"].strip())]
put("years", "rows with a first-record year (share); first; last",
    f"{len(years)} ({len(years) / len(rec):.3f}); {min(years)}; {max(years)}")
put("years", "rows whose year differs from the verbatim first record (a range or text resolved to one year)",
    sum(1 for r in rec if r["firstRecordEvent"].strip() != r["verbatimFirstRecordEvent"].strip()))
spans = []
for r in rec:
    m = re.fullmatch(r"\s*(-?\d{3,4})\s*[-–/]\s*(-?\d{3,4})\s*", r["verbatimFirstRecordEvent"])
    if m and int(m.group(2)) > int(m.group(1)):
        spans.append(int(m.group(2)) - int(m.group(1)))
put("years", "verbatim year ranges (YYYY-YYYY); spanning more than 20 years; widest span",
    f"{len(spans)}; {sum(1 for s in spans if s > 20)}; {max(spans) if spans else ''}")
put("years", "rows before 1500 (incl. BCE); 1500-1799; 1800-1899; 1900-1949; 1950-1999; 2000 on",
    "; ".join(str(sum(1 for y in years if lo <= y < hi)) for lo, hi in
              ((-99999, 1500), (1500, 1800), (1800, 1900), (1900, 1950), (1950, 2000), (2000, 3000))))
for col in ("confidenceFirstRecordEvent", "occurrenceStatus", "establishmentMeans", "degreeOfEstablishment", "habitat", "accessRights"):
    put("fields", col, counts(collections.Counter(r[col].strip() for r in rec)))
put("fields", "rows with a pathway", sum(1 for r in rec if r["pathway"].strip()))
put("taxa", "rows by taxaGroup", counts(collections.Counter(tax.get(r["taxonID"], {}).get("taxaGroup", "") for r in rec), 15))
put("taxa", "rows by kingdom (GBIF)", counts(collections.Counter(tax.get(r["taxonID"], {}).get("kingdom", "") for r in rec)))
put("taxa", "taxa by GBIF match status", counts(collections.Counter(t["GBIFstatus"] for t in tax.values())))
put("locations", "rows by continent", counts(collections.Counter(loc.get(r["locationID"], {}).get("continent", "") for r in rec)))
put("sources", "rows by citation, most common", counts(collections.Counter(r["bibliographicCitation"][:50] for r in rec), 8))
with zipfile.ZipFile(v31) as z:
    sizes = {n: len(re.findall(rb"<row[ >]", z.read(n))) for n in z.namelist() if n.startswith("xl/worksheets/sheet")}
    sheet = max(sizes, key=sizes.get)
put("v3.1", "rows in the free-data workbook (its largest sheet, less the header)", f"{sizes[sheet] - 1} ({sheet.split('/')[-1]})")

with open(out_tsv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["section", "metric", "value"])
    w.writerows(out)
print(len(out), "rows")
