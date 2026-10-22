"""Profile an AusTraits release zip (austraits-X.zip from Zenodo).

Usage: python3 austraits_profile.py AUSTRAITS_ZIP OUT_TSV

Counts rows, traits, datasets and taxa; value types and basis of record; the
fire-response traits and a few vegetation traits used in modelling; taxa by
APC alignment and establishment; and invalid UTF-8 in traits.csv (decoded with
replacement, so counts are unaffected). Writes long-format (table, metric,
key, value). Standard library only.
"""

import csv
import io
import sys
import zipfile
from collections import Counter, defaultdict

csv.field_size_limit(1 << 30)
FIRE = ["resprouting_capacity", "post_fire_recruitment", "serotiny", "bud_bank_location", "seedbank_longevity_class",
        "bark_thickness", "fire_time_from_fire_to_flowering", "fire_response_on_maturity", "fire_and_establishing",
        "fire_cued_seeding", "fire_response_juvenile", "fire_time_from_fire_to_fruiting"]
OTHER = ["plant_growth_form", "plant_height", "wood_density", "leaf_mass_per_area", "seed_dry_mass", "photosynthetic_pathway"]
out = []


def add(*row):
    out.append(row)


z = zipfile.ZipFile(sys.argv[1])
names = z.namelist()
for n in sorted(names):
    add("zip", "member_bytes", n, z.getinfo(n).file_size)


def member(stem):
    return next(n for n in names if n.endswith("/" + stem) or n == stem)


raw = z.read(member("traits.csv"))
bad = 0
for line in raw.split(b"\n"):
    try:
        line.decode("utf-8")
    except UnicodeDecodeError:
        bad += 1
add("traits", "lines_with_invalid_utf8", "", bad)
rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8", errors="replace"))))
del raw
add("traits", "rows", "", len(rows))
add("traits", "columns", "", " | ".join(rows[0].keys()))
add("traits", "distinct_traits", "", len({r["trait_name"] for r in rows}))
add("traits", "distinct_datasets", "", len({r["dataset_id"] for r in rows}))
add("traits", "distinct_taxa", "", len({r["taxon_name"] for r in rows}))
for k in ("value_type", "basis_of_record"):
    if k in rows[0]:
        for v, n in Counter(r[k] for r in rows).most_common(10):
            add("traits", f"by:{k}", v, n)
by_trait = defaultdict(list)
for r in rows:
    by_trait[r["trait_name"]].append(r)
for t in FIRE + OTHER:
    rs = by_trait.get(t, [])
    add("selected_traits", t, "records_taxa_datasets", f'{len(rs)} {len({r["taxon_name"] for r in rs})} {len({r["dataset_id"] for r in rs})}')
for v, n in Counter(x for r in by_trait.get("resprouting_capacity", []) for x in r["value"].split()).most_common(6):
    add("selected_traits", "resprouting_capacity_values", v, n)
for k in ("taxa.csv", "locations.csv", "contexts.csv", "methods.csv", "contributors.csv", "excluded_data.csv", "taxonomic_updates.csv"):
    try:
        with z.open(member(k)) as f:
            data = list(csv.DictReader(io.TextIOWrapper(f, encoding="utf-8", errors="replace")))
    except StopIteration:
        continue
    add("tables", "rows", k, len(data))
    if k == "taxa.csv":
        for col in ("taxon_rank", "taxonomic_dataset", "establishment_means"):
            if col in data[0]:
                for v, n in Counter(r[col] for r in data).most_common(6):
                    add("taxa", f"by:{col}", v, n)

with open(sys.argv[2], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
