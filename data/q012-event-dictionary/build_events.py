# /// script
# requires-python = ">=3.12"
# dependencies = ["openpyxl==3.1.5"]
# ///
"""Q-012 event dictionary from Lamyman et al. 2026 (Zenodo 21414007).

Builds two source-located tables without changing any raw value:
- lineage_edges.tsv: one row per S3 `Lineages Tree2` record (the source's
  pseudoextinction-free lineage units), with its ancestor lineage, dates, the
  date relation to the ancestor, branch style and member ecogroups;
- morphospecies_edges.tsv: one row per S1 parent -> daughter link with both
  names in S1, with its date relation, whether the daughter is named as a
  lineage's founding morphospecies, and shared lineage membership. No
  speciation mode is assigned: the source tables do not define one at this
  level (see README).

Run from the repository root:
  uv run data/q012-event-dictionary/build_events.py
"""

import collections
import csv
import hashlib
import json
import pathlib
import re

import openpyxl

ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = ROOT / "data/raw/lamyman2026"
HERE = pathlib.Path(__file__).resolve().parent
S1 = RAW / "S1. Morphospecies Key Information.xlsx"
S3 = RAW / "Supporting Data.xlsx"
SHA = {S1: "88cd9b0a054aae64c9adfeadad5ec730dddfb11d169b8100ab61f803f0e05d84",
       S3: "2412991df3ff35d9f62275a500a474feff77e2c89b24ec86289574a8f7a7366b"}
OUT_OF_SCOPE_LINEAGES = {"L_Bolivina Clade"}  # S3 Overall %Change Tree1v2 F3
OUT_OF_SCOPE_SPECIES = {"Praepararotalia cretacea", "Praepararotalia perclara"}  # S3 F2; benthic


def norm(s):
    """Derived lookup key only: strip outer whitespace including NBSP."""
    return str(s).strip().strip(" ").strip()


def table(ws):
    rows = list(ws.iter_rows(values_only=True))
    return [(i + 2, dict(zip(rows[0], r))) for i, r in enumerate(rows[1:]) if r[0] is not None]


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def relation(anc_end, d_start):
    if anc_end is None or d_start is None:
        return "undated"
    if abs(anc_end - d_start) < 1e-9:
        return "boundary"
    return "overlap" if anc_end < d_start else "gap"


def main():
    for p, h in SHA.items():
        assert hashlib.sha256(p.read_bytes()).hexdigest() == h, f"hash differs: {p.name}"
    s1 = table(openpyxl.load_workbook(S1, read_only=True, data_only=True)["Key Information"])
    wb3 = openpyxl.load_workbook(S3, read_only=True, data_only=True)
    gn = {norm(r["GenusEpithet"]): norm(r["Gn"]) for _, r in table(wb3["Gn, Genera"])}
    lin = table(wb3["Lineages Tree2"])

    sp = {norm(r["Morphospecies"]): (row, r) for row, r in s1}
    short = {}
    for name in sp:
        genus, epithet = name.split(" ", 1)
        short[gn.get(genus, genus) + " " + epithet] = name
        short[name] = name

    members, founder, unresolved = {}, {}, []
    of = re.compile(r"of (.+)$")
    for row, r in lin:
        code = norm(r["Biospecies code"])
        names = []
        for tok in str(r["MorphospeciesGnInLineage"]).split(","):
            t = norm(tok)
            if t in short:
                names.append(short[t])
            elif t:
                unresolved.append((code, t))
        members[code] = names
        m = of.search(str(r["Start Source"] or ""))
        founder[code] = (norm(m.group(1)) if m else None,
                         "end-link" if "to End of" in str(r["Start Source"]) else "start")
    in_lineages = collections.defaultdict(set)
    for code, names in members.items():
        for n in names:
            in_lineages[n].add(code)
    by_code = {norm(r["Biospecies code"]): (row, r) for row, r in lin}

    def eco(names):
        return ";".join(sorted({str(sp[n][1]["Dominant Ecogroup"]) for n in names if n in sp}))

    lrows = [["lineage", "s3_row", "ancestor", "ancestor_in_table", "branch_style", "start_Ma", "end_Ma",
              "ancestor_start_Ma", "ancestor_end_Ma", "date_relation", "founding_morphospecies",
              "founder_link", "members", "member_ecogroups", "ancestor_member_ecogroups", "in_scope"]]
    lcount = collections.Counter()
    for row, r in lin:
        code, anc = norm(r["Biospecies code"]), norm(r["Ancestor code"])
        a = by_code.get(anc, (None, {}))[1]
        rel = relation(num(a.get("End")), num(r["Start"])) if a else "ancestor_outside"
        scope = code not in OUT_OF_SCOPE_LINEAGES
        lcount[(rel, "in_scope" if scope else "out")] += 1
        lrows.append([code, row, anc, bool(a), r["BranchStyle"], r["Start"], r["End"], a.get("Start"), a.get("End"),
                      rel, founder[code][0], founder[code][1], len(members[code]), eco(members[code]),
                      eco(members.get(anc, [])), scope])

    mrows = [["parent", "daughter", "s1_row_parent", "s1_row_daughter", "daughter_edge_evidence", "date_relation",
              "daughter_founds", "founded_lineage_ancestor_lists_parent", "shared_lineages", "in_scope"]]
    mcount = collections.Counter()
    for name, (row, r) in sp.items():
        parent = norm(r["Ancestor"]) if r["Ancestor"] else None
        if parent not in sp:
            continue
        prow, pr = sp[parent]
        rel = relation(num(pr["End"]), num(r["Start"]))
        founds = sorted(c for c, (f, link) in founder.items() if f == name and link == "start")
        anc_lists = any(parent in members.get(norm(by_code[c][1]["Ancestor code"]), []) for c in founds)
        shared = sorted(in_lineages[name] & in_lineages[parent])
        scope = name not in OUT_OF_SCOPE_SPECIES and parent not in OUT_OF_SCOPE_SPECIES
        key = ("founds_lineage" if founds else "no_founding_record", "shares_lineage" if shared else "no_shared_lineage")
        mcount[(rel,) + key + ("in_scope" if scope else "out",)] += 1
        mrows.append([parent, name, prow, row, r["Ancestry evidence"], rel, ";".join(founds), anc_lists,
                      ";".join(shared), scope])

    for fn, rows in (("lineage_edges.tsv", lrows), ("morphospecies_edges.tsv", mrows)):
        with (HERE / fn).open("w", newline="") as fh:
            csv.writer(fh, delimiter="\t", lineterminator="\n").writerows(rows)
    summary = dict(
        inputs={p.name: SHA[p] for p in SHA},
        lineage_records=len(lin), unresolved_member_tokens=unresolved,
        lineage_edges={f"{k[0]}|{k[1]}": v for k, v in sorted(lcount.items())},
        morphospecies_edges={"|".join(k): v for k, v in sorted(mcount.items())},
        lineage_founders_naming_an_S1_morphospecies=sum(f in sp for f, _ in founder.values()),
        species_in_multiple_lineages=sum(len(v) > 1 for v in in_lineages.values()),
    )
    (HERE / "events_summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
