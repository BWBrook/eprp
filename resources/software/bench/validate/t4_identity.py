# Tranche-4 A5: the regenerated records must equal the run's, apart from the added count and truth columns.
# Usage: python3 t4_identity.py <old dir> <new dir> <tag> [<tag> ...]
import csv
import gzip
import sys

old, new = sys.argv[1], sys.argv[2]
ok = True
for tag in sys.argv[3:]:
    with gzip.open(f"{old}/occ_{tag}.csv.gz", "rt") as a, gzip.open(f"{new}/occ_{tag}.csv.gz", "rt") as b:
        ra, rb = list(csv.DictReader(a)), list(csv.DictReader(b))
    occ_same = len(ra) == len(rb) and all(x == {k: y[k] for k in x} for x, y in zip(ra, rb))
    with open(f"{old}/truth_{tag}.csv") as a, open(f"{new}/truth_{tag}.csv") as b:
        ta, tb = list(csv.DictReader(a)), list(csv.DictReader(b))
    truth_same = len(ta) == len(tb) and all(x == {k: y[k] for k in x} for x, y in zip(ta, tb))
    print(tag, "occurrences identical:", occ_same, "truth identical:", truth_same)
    ok = ok and occ_same and truth_same
sys.exit(0 if ok else 1)
