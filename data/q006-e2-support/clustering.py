"""Q-006 E2 data support: are stage-binned species occurrence counts plausible Poisson detections?

Uses the pinned PBDB Changhsingian marine species-level extract from Q-042 (fetched there if absent).
Per species: occurrences, distinct collections and distinct references within the stage, and the share
of repeat occurrences that add a new reference. Run from the repository root:
    python3 -I data/q006-e2-support/clustering.py
"""
import collections
import csv
import hashlib
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/raw/pbdb/q042/changhsingian_marine_species.csv"
URL = ("https://paleobiodb.org/data1.2/occs/list.csv?base_name=Animalia&interval=Changhsingian"
       "&timerule=contain&envtype=marine&idreso=species&pres=regular&show=class,ident")
SHA = "d9081350fdad36a86e0ba6da7bcc9fe13b6eeb918155e3ab9d7b5922d79ff267"


def main():
    if not RAW.exists():
        RAW.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(URL, RAW)
    digest = hashlib.sha256(RAW.read_bytes()).hexdigest()
    if digest != SHA:
        raise SystemExit(f"extract changed: sha256 {digest}; inspect before re-pinning")
    occ = collections.defaultdict(list)
    with open(RAW, newline="") as f:
        for r in csv.DictReader(f):
            if r["accepted_rank"] in ("species", "subspecies") and r["genus"]:
                name = " ".join(re.sub(r" \(.*?\)", "", r["accepted_name"]).split()[:2])
                occ[name].append((r["collection_no"], r["reference_no"]))
    n = len(occ)
    k = [len(v) for v in occ.values()]
    kc = [len({c for c, _ in v}) for v in occ.values()]
    kr = [len({rf for _, rf in v}) for v in occ.values()]
    share = lambda xs, t: round(sum(x >= t for x in xs) / n, 3)
    repeats, new_ref = sum(x - 1 for x in k), sum(x - 1 for x in kr)
    out = dict(species=n, occurrences=sum(k),
               share_ge2_occurrences=share(k, 2), share_ge2_collections=share(kc, 2),
               share_ge2_references=share(kr, 2), share_ge3_references=share(kr, 3),
               repeat_occurrences=repeats, repeats_adding_new_reference=new_ref,
               share_repeats_new_reference=round(new_ref / repeats, 3))
    with open(Path(__file__).resolve().parent / "clustering.tsv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerow(out)
    print(out)


if __name__ == "__main__":
    main()
