"""Turn the matched citation table into seed tiers and a review list.
Usage: python3 build_seeds.py MATCHED.tsv LIBRARY_DIR"""
import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

matched, lib = sys.argv[1], Path(sys.argv[2])
rows = list(csv.DictReader(open(matched), delimiter="\t"))


def write(path, data, fields):
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fields, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(data)


resolved = [r for r in rows if r["confidence"]]
key = lambda r: r["doi"] or r["openalex_id"]

# the 2003 list: one row per list item, in list order
listed = [{"item": r["item"], "openalex_id": r["openalex_id"], "doi": r["doi"], "confidence": r["confidence"],
           "citation": r["raw"]} for r in rows if r["source"] == "list" and r["confidence"]]
write(lib / "seeds" / "barry-2003-list.tsv", listed, ["item", "openalex_id", "doi", "confidence", "citation"])

# the EndNote libraries and the RTF bibliography: one row per distinct work, with every holding listed
groups = defaultdict(list)
for r in resolved:
    if r["source"] != "list":
        groups[key(r)].append(r)
held = []
for k, rs in groups.items():
    best = max(rs, key=lambda r: r["confidence"] == "exact")
    held.append({"openalex_id": best["openalex_id"], "doi": best["doi"],
                 "confidence": "exact" if any(r["confidence"] == "exact" for r in rs) else "probable",
                 "items": "; ".join(r["item"] for r in rs),
                 "libraries": "; ".join(sorted({r["source"].split(":", 1)[-1] for r in rs})),
                 "citation": best["raw"]})
held.sort(key=lambda r: r["items"])
write(lib / "seeds" / "barry-2003-endnote.tsv", held,
      ["openalex_id", "doi", "confidence", "items", "libraries", "citation"])

unresolved = [r for r in rows if not r["confidence"]]
write(lib / "review" / "barry-2003-unresolved.tsv", unresolved,
      ["source", "item", "first_author", "year", "title", "journal", "volume", "pages", "raw", "via"])

list_keys = {key(r) for r in resolved if r["source"] == "list"}
print("rows:", len(rows), "| by grade:", dict(Counter(r["confidence"] or "unresolved" for r in rows)))
print("list:", len(listed), "of", sum(1 for r in rows if r["source"] == "list"), "items resolved,",
      len(list_keys), "distinct works;", dict(Counter(r["confidence"] for r in listed)))
print("libraries + RTF:", len(held), "distinct works from", sum(len(v) for v in groups.values()), "resolved records;",
      "list works also held there:", sum(1 for k in list_keys if k in groups), "of", len(list_keys),
      "| list items:", sum(1 for r in listed if key(r) in groups), "of", len(listed))
print("unresolved by source:", dict(Counter(r["source"] for r in unresolved)))
print("via:", dict(Counter(r["via"] for r in rows)))
