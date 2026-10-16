# /// script
# requires-python = ">=3.12"
# dependencies = ["openpyxl==3.1.5"]
# ///
"""Source-supported name crosswalk: Triton species names -> Lamyman S1 morphospecies.

Rules, in order (fixed before use; no fuzzy matching):
1. exact: the Triton name equals an S1 name (outer whitespace stripped);
2. tree1: the Triton name equals S3 `Morphospecies Tree1v2` column
   MorphospeciesTree1 (the Aze et al. 2011 name) on a row whose status is
   "Name Changed", and that row's Morphospecies is an S1 name;
3. backticks: the Triton name equals an S1 name after removing the
   backticks S1 uses to mark informal genera (a formatting difference only);
4. otherwise unmatched, with the reason recorded (for example a Tree1 row
   whose status is "Removed"). If exactly one S1 name shares the species
   epithet under a different genus, it is recorded as a candidate in the
   note but NOT applied: genus reassignment is a taxonomic decision.
A Triton name mapping to more than one S1 name, or two Triton names mapping
to one S1 name, is recorded rather than resolved.

Run from the repository root:
  uv run data/q012-exposure-support/crosswalk.py data/q012-exposure-support/triton_names.txt
where the input lists Triton `triton.pres` species names (trim == "inc"),
one per line, as written by names.R.
"""

import collections
import csv
import hashlib
import pathlib
import sys

import openpyxl

ROOT = pathlib.Path(__file__).resolve().parents[2]
S3 = ROOT / "data/raw/lamyman2026/Supporting Data.xlsx"
S3_SHA = "2412991df3ff35d9f62275a500a474feff77e2c89b24ec86289574a8f7a7366b"
SPECIES = ROOT / "data/q012-event-dictionary/species.tsv"
OUT = pathlib.Path(__file__).resolve().parent / "name_crosswalk.tsv"


def norm(s):
    return str(s).strip().strip(" ").strip()


def main():
    assert hashlib.sha256(S3.read_bytes()).hexdigest() == S3_SHA, "S3 hash differs"
    s1 = {norm(r["morphospecies"]) for r in csv.DictReader(SPECIES.open(), delimiter="\t")
          if r["in_scope"] == "True"}
    rows = list(openpyxl.load_workbook(S3, read_only=True, data_only=True)["Morphospecies Tree1v2"]
                .iter_rows(values_only=True))
    hdr = rows[0]
    tree1 = collections.defaultdict(list)
    for i, r in enumerate(rows[1:], start=2):
        d = dict(zip(hdr, r))
        if d["MorphospeciesTree1"]:
            tree1[norm(d["MorphospeciesTree1"])].append((i, norm(d["Morphospecies"]), d["MorphospeciesStatus"]))
    triton = [norm(l) for l in pathlib.Path(sys.argv[1]).read_text().splitlines() if l.strip()]

    out = [["triton_name", "s1_name", "rule", "s3_row", "note"]]
    unticked = {n.replace("`", ""): n for n in s1}
    by_epithet = collections.defaultdict(list)
    for n in s1:
        by_epithet[n.replace("`", "").split(" ", 1)[-1]].append(n)
    for t in sorted(set(triton)):
        if t in s1:
            out.append([t, t, "exact", "", ""])
            continue
        if t in unticked:
            out.append([t, unticked[t], "backticks", "", ""])
            continue
        hits = [(i, n, st) for i, n, st in tree1.get(t, []) if st == "Name Changed" and n in s1]
        if len(hits) == 1:
            out.append([t, hits[0][1], "tree1", hits[0][0], ""])
        elif len(hits) > 1:
            out.append([t, "", "unmatched", ";".join(str(h[0]) for h in hits), "ambiguous tree1 mapping"])
        else:
            other = tree1.get(t, [])
            note = ";".join(f"row {i}: {st} -> {n}" for i, n, st in other) or "no S1 or Tree1 entry"
            cands = by_epithet.get(t.split(" ", 1)[-1], [])
            if len(cands) == 1:
                note += f"; epithet candidate (not applied): {cands[0]}"
            out.append([t, "", "unmatched", "", note])
    targets = collections.Counter(r[1] for r in out[1:] if r[1])
    for r in out[1:]:
        if r[1] and targets[r[1]] > 1:
            r[4] = (r[4] + "; " if r[4] else "") + "S1 name reached by more than one Triton name"
    with OUT.open("w", newline="") as fh:
        csv.writer(fh, delimiter="\t", lineterminator="\n").writerows(out)
    c = collections.Counter(r[2] for r in out[1:])
    print(dict(c), "| S1 names reached:", len(targets), "| collisions:", sum(v > 1 for v in targets.values()))


if __name__ == "__main__":
    main()
