"""Profile GloNAF 2.02 (Q-047).

Usage: python3 glonaf_profile.py GLONAF_DIR OUT_TSV

Writes section, metric, value rows: taxon-by-region records, taxa, regions
and lists; status and list completeness; island and ISO-equivalent regions;
families; records per region. Standard library only.
"""

import collections
import csv
import os
import statistics
import sys

d, out_tsv = sys.argv[1:3]
out = []


def put(section, metric, value):
    out.append([section, metric, str(value)])


def counts(c, top=12):
    return "; ".join(f"{k or '(blank)'} {v}" for k, v in c.most_common(top))


def table(name):
    with open(os.path.join(d, name), newline="", encoding="utf-8-sig", errors="replace") as f:
        return list(csv.DictReader(f))


flora, region, lists, taxa = (table(f"glonaf_{t}.csv") for t in ("flora2", "region", "list", "taxon_wcvp"))
reg = {r["id"]: r for r in region}
acc = {t["id"]: t["taxa_accepted"] for t in taxa}
put("records", "taxon-by-region rows; distinct taxon ids; distinct accepted WCVP names; regions with records; lists",
    f"{len(flora)}; {len({r['taxon_wcvp_id'] for r in flora})}; {len({acc.get(r['taxon_wcvp_id']) for r in flora} - {None, ''})}; "
    f"{len({r['region_id'] for r in flora})}; {len(lists)}")
put("records", "rows by status", counts(collections.Counter(r["status"] for r in flora)))
put("records", "distinct taxon-region pairs", len({(r["taxon_wcvp_id"], r["region_id"]) for r in flora}))
put("taxa", "taxa in the WCVP table; by WCVP status; by rank",
    f"{len(taxa)}; {counts(collections.Counter(t['wcvp_taxon_status'] for t in taxa), 5)}; {counts(collections.Counter(t['wcvp_taxon_rank'] for t in taxa), 5)}")
put("taxa", "rows by family (top)", counts(collections.Counter(r["family_wcvp"] for r in flora), 10))
put("regions", "regions; islands; equivalent to an ISO country", f"{len(region)}; {sum(r['island'] == '1' for r in region)}; {sum(r['iso_equivalent'] == '1' for r in region)}")
sets = collections.defaultdict(set)
for r in flora:
    sets[r["region_id"]].add(acc.get(r["taxon_wcvp_id"]) or r["taxon_wcvp_id"])
per = {k: len(v) for k, v in sets.items()}
top = sorted(per, key=per.get, reverse=True)[:3]
put("regions", "distinct accepted taxa per region: median; largest three",
    f"{statistics.median(per.values())}; " + ", ".join(f"{reg[k]['name']} {per[k]}" for k in top))
put("lists", "lists by completeness_id", counts(collections.Counter(r["completeness_id"] for r in lists)))
put("lists", "lists listing invasives only", sum(r["invasives_only"] == "1" for r in lists))
made = [r["created"] for r in flora if r["created"]]
put("dates", "rows with a creation date; first and last; last updated",
    f"{len(made)}; {min(made)}; {max(made)}; {max(r['updated'] for r in flora)}")

with open(out_tsv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["section", "metric", "value"])
    w.writerows(out)
print(len(out), "rows")
