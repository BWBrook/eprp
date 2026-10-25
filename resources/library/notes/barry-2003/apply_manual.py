"""apply_manual.py MATCHED MANUAL OUT: override matched rows by (source, item) with hand-checked resolutions."""
import csv
import sys

rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
manual = {(r["source"], r["item"]): r for r in csv.DictReader(open(sys.argv[2]), delimiter="\t")}
for r in rows:
    m = manual.get((r["source"], r["item"]))
    if m:
        r.update({k: m[k] for k in ("doi", "openalex_id", "confidence", "matched_title", "via")})
with open(sys.argv[3], "w", newline="") as fh:
    w = csv.DictWriter(fh, list(rows[0].keys()), delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print("applied", sum((r["source"], r["item"]) in manual for r in rows), "of", len(manual), "manual rows")
