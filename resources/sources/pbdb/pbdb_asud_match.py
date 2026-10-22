"""Match PBDB collection formation, group and member names to Geoscience Australia's ASUD register.

Usage: python3 pbdb_asud_match.py PBDB_SNAPSHOT_DIR ASUD_CSV OUT_TSV OUT_EXAMPLES_TSV

Tiers: exact (case and punctuation folded, trailing rank words such as Formation or Fm
dropped), then core (trailing lithology words such as Limestone or Sands also dropped).
Units in the collection's state are preferred; a match found only in other states is
tagged _other_state (likely a homonym) and left out of the age check. For unique
matches with numeric ages, tests whether the PBDB collection's age range overlaps the
ASUD unit's. Also counts PBDB formation names that differ only in rank
or lithology words. Core extract only (Australian names). Standard library only.
"""

import csv
import re
import sys
from collections import Counter, defaultdict

csv.field_size_limit(1 << 30)
RANK = {"formation", "fm", "group", "gp", "member", "mbr", "beds", "bed", "subgroup", "supergroup", "suite", "unit"}
LITH = {"limestone", "limestones", "sandstone", "sandstones", "sand", "sands", "shale", "shales", "siltstone", "mudstone",
        "claystone", "clay", "clays", "conglomerate", "marl", "coquina", "calcarenite", "greywacke", "chert", "dolomite",
        "quartzite", "volcanics", "coal", "measures", "tuff", "basalt", "gravel", "gravels", "silt", "slate", "breccia", "chalk"}
RANK_FIELD = {"formation": "Formation, beds", "geological_group": "Group, Suite", "member": "Member, phase"}
STATES = [("queen", "QLD"), ("new s", "NSW"), ("victoria", "VIC"), ("western a", "WA"), ("west a", "WA"), ("south a", "SA"),
          ("tasman", "TAS"), ("northern t", "NT"), ("northwest t", "NT"), ("australian capital", "ACT")]
out, examples = [], []


def norm(s):
    w = re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()
    while w and w[-1] in RANK:
        w.pop()
    return " ".join(w)


def core(s):
    w = norm(s).split()
    while len(w) > 1 and w[-1] in LITH:
        w.pop()
    return " ".join(w)


def state_code(s):
    s = s.strip().lower()
    return next((code for prefix, code in STATES if s.startswith(prefix)), None)


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


pbdb, asud_csv = sys.argv[1], sys.argv[2]
with open(asud_csv, newline="", encoding="utf-8") as f:
    units = [u for u in csv.DictReader(f) if u["STATE"] != "ATA"]
by_norm, by_core = defaultdict(list), defaultdict(list)
for u in units:
    by_norm[norm(u["NAME"])].append(u)
    by_core[core(u["NAME"])].append(u)

with open(f"{pbdb}/collections.csv", newline="", encoding="utf-8") as f:
    rd = csv.reader(f)
    h = next(rd)
    first = {}
    for i, k in enumerate(h):
        first.setdefault(k, i)
    cols = [{k: r[i] for k, i in first.items()} for r in rd]
cols = [c for c in cols if c["cc"] == "AU"]
out.append(("collections", "AU_rows", "", len(cols)))

for field, rank in RANK_FIELD.items():
    tiers, occ_tiers, ages = Counter(), Counter(), Counter()
    unmatched = Counter()
    for c in cols:
        name, n_occs = c[field].strip(), int(c["n_occs"] or 0)
        if not name:
            tiers["blank"] += 1
            occ_tiers["blank"] += n_occs
            continue
        hits = by_norm.get(norm(name)) or []
        tier = "exact" if hits else ""
        if not hits:
            hits = by_core.get(core(name)) or []
            tier = "core" if hits else "unmatched"
        code = state_code(c["state"])
        same = [u for u in hits if code in u["STATE"].split(", ")]
        if same:
            hits = same
        elif hits and code and all(u["STATE"] for u in hits):
            tier += "_other_state"
        ranked = [u for u in hits if u["RANK"] == rank]
        hits = ranked or hits
        if len(hits) > 1:
            tier += "_ambiguous"
        tiers[tier] += 1
        occ_tiers[tier] += n_occs
        if tier == "unmatched":
            unmatched[name] += n_occs
            continue
        lo, hi = num(c["min_ma"]), num(c["max_ma"])
        if len(hits) != 1 or "other_state" in tier or lo is None or hi is None:
            continue
        u = hits[0]
        yng, old = num(u["NUMERICYOUNGERAGE"]), num(u["NUMERICOLDERAGE"])
        if yng is None or old is None:
            ages["asud_no_age"] += 1
            continue
        gap = max(yng - hi, lo - old, 0)
        key = "overlap" if gap == 0 else "gap_le_5myr" if gap <= 5 else "gap_5_20myr" if gap <= 20 else "gap_gt_20myr"
        ages[key] += 1
        if gap > 20 and len(examples) < 60:
            examples.append((field, c["collection_no"], name, f'{c["max_ma"]}-{c["min_ma"]}', u["NAME"], u["STATE"],
                             f'{u["NUMERICOLDERAGE"]}-{u["NUMERICYOUNGERAGE"]}', round(gap, 1)))
    for k, v in sorted(tiers.items()):
        out.append((field, "collections_by_tier", k, v))
    for k, v in sorted(occ_tiers.items()):
        out.append((field, "occurrences_by_tier", k, v))
    for k, v in sorted(ages.items()):
        out.append((field, "age_check_unique_matches", k, v))
    for k, v in unmatched.most_common(15):
        out.append((field, "top_unmatched_by_occs", k, v))

variants = defaultdict(set)
for c in cols:
    if c["formation"].strip():
        variants[core(c["formation"])].add(c["formation"].strip())
multi = {k: v for k, v in variants.items() if len(v) > 1}
out.append(("formation", "distinct_raw_names", "", sum(len(v) for v in variants.values())))
out.append(("formation", "distinct_core_keys", "", len(variants)))
out.append(("formation", "core_keys_with_multiple_raw_names", "", len(multi)))
for k in sorted(multi, key=lambda k: -len(multi[k]))[:15]:
    out.append(("formation", "variant_example", k, " | ".join(sorted(multi[k]))))

with open(sys.argv[3], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
with open(sys.argv[4], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["field", "collection_no", "pbdb_name", "pbdb_max_min_ma", "asud_name", "asud_state", "asud_older_younger_ma", "gap_myr"])
    w.writerows(examples)
