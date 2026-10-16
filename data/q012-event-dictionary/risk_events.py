"""Q-012 lineage events and risk sets, from lineage_edges.tsv (standard library).

For each in-scope lineage records how it ends and how often it buds:
- end_type:
  - "present" if its end is 0 Ma (right-censored);
  - "bifurcation_candidate" if >= 2 in-scope daughters start exactly at its end;
  - "single_coincident_daughter" if exactly 1 daughter starts exactly at its end
    (equal compiled dates alone do not show a bifurcation; kept apart);
  - "extinction" otherwise.
- n_buds: in-scope daughters starting strictly before its end (budding, parent
  persists), with their start ages.
"Exactly" means equal to 0.005 Myr, the source's two-decimal precision.

Run from the repository root:  python3 -I data/q012-event-dictionary/risk_events.py
"""

import collections
import csv
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
TOL = 0.005


def main():
    rows = [r for r in csv.DictReader((HERE / "lineage_edges.tsv").open(), delimiter="\t") if r["in_scope"] == "True"]
    by = {r["lineage"]: r for r in rows}
    kids = collections.defaultdict(list)
    for r in rows:
        if r["ancestor"] in by:
            kids[r["ancestor"]].append(r)
    out = [["lineage", "start_Ma", "end_Ma", "end_type", "daughters_at_end", "n_buds", "bud_starts_Ma",
            "ancestor_in_scope", "starts_before_69Ma"]]
    count = collections.Counter()
    for r in rows:
        start, end = float(r["start_Ma"]), float(r["end_Ma"])
        at_end = [k for k in kids[r["lineage"]] if abs(float(k["start_Ma"]) - end) <= TOL]
        buds = sorted((float(k["start_Ma"]) for k in kids[r["lineage"]] if float(k["start_Ma"]) > end + TOL), reverse=True)
        if end == 0:
            et = "present"
        elif len(at_end) >= 2:
            et = "bifurcation_candidate"
        elif len(at_end) == 1:
            et = "single_coincident_daughter"
        else:
            et = "extinction"
        count[et] += 1
        out.append([r["lineage"], start, end, et, len(at_end), len(buds), ";".join(f"{b:g}" for b in buds),
                    r["ancestor"] in by, start > 69])
    with (HERE / "lineage_events.tsv").open("w", newline="") as fh:
        csv.writer(fh, delimiter="\t", lineterminator="\n").writerows(out)
    links = [r for r in rows if r["ancestor"] in by]
    print("in-scope lineages", len(rows), dict(count))
    print("links to in-scope ancestors", len(links), dict(collections.Counter(r["date_relation"] for r in links)))
    print("roots (ancestor outside scope)", sum(r["ancestor"] not in by for r in rows))
    print("starts before 69 Ma", sum(float(r["start_Ma"]) > 69 for r in rows),
          "max start", max(float(r["start_Ma"]) for r in rows))
    print("budding events", sum(int(o[5]) for o in out[1:]))


if __name__ == "__main__":
    main()
