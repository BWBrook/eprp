"""Q-042: conditional algebra for end-Permian species loss, and a PBDB stage-union diagnostic.

Conditional algebra (valid only under its stated conditions; see README):
  I0  g = TOTAL genus loss of the start-time cohort (not event excess), m = TRUE mean species per
      genus of that cohort, and every surviving genus keeps >= 1 start-cohort species (sampled or
      not). Then species loss lies in [g/m, 1 - (1 - g)/m].
  I1  as I0, with a full genus-size distribution in place of m: the lower bound becomes the species
      share of the smallest g*G genera. The sampled distribution is used only as an illustration of
      what such a distribution does, as if it were the true one.
Diagnostic (NOT bounds):
  I2  PBDB stage union: genera with species-level occurrences anywhere in the Changhsingian, keyed
      by PBDB's accepted genus, and whether PBDB records them after the stage. A stage union is not a
      start-time cohort, and no later record is not extinction.

Run from the repository root:  python3 -I data/q042-crosswalk/bounds.py
Standard library only. Fetches the PBDB extract once into data/raw/pbdb/q042/ (git-ignored).
"""
import collections
import csv
import hashlib
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
RAW = ROOT / "data/raw/pbdb/q042/changhsingian_marine_species.csv"
URL = ("https://paleobiodb.org/data1.2/occs/list.csv?base_name=Animalia&interval=Changhsingian"
       "&timerule=contain&envtype=marine&idreso=species&pres=regular&show=class,ident")
TAXA = ROOT / "data/raw/pbdb/q042/genus_appearances.csv"
TAXA_URL = "https://paleobiodb.org/data1.2/taxa/list.csv?show=app,class&name="
BOUNDARY = 251.902  # PBDB top of the Changhsingian (GTS2020)

# Genus-loss scenarios: see README crosswalk for what each measures. They are NOT one interval.
SCENARIOS = [("g56", 0.56), ("g62", 0.62), ("g79", 0.79)]
M_VALUES = [3.0, 5.0, 9.5]  # plus the sampled mean, added at run time
TARGETS = [0.90, 0.96]


HOLD = ("PBDB data hold (76/2259, 76/2327): this legacy rebuild is disabled; the extracts were deleted at Barry's instruction on 23 October 2026. Rebuild "
        "only from public record-level data (resources/sources/pbdb/).")


def sampled_cohort():
    raise SystemExit(HOLD)                # legacy fetch disabled; see HOLD
    if not RAW.exists():
        RAW.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(URL, RAW)
    species, phylum = collections.defaultdict(set), {}
    with open(RAW, newline="") as f:
        for r in csv.DictReader(f):
            if r["accepted_rank"] in ("species", "subspecies") and r["genus"]:
                name = re.sub(r" \(.*?\)", "", r["accepted_name"]).split()  # drop subgenus brackets
                genus = re.sub(r" \(.*?\)", "", r["genus"])  # PBDB's accepted genus, not the name's first word
                species[genus].add(" ".join(name[:2]))
                phylum[genus] = r["phylum"]
    return species, phylum


def fates(genera, phylum):
    raise SystemExit(HOLD)                # legacy fetch disabled; see HOLD
    """lost / survived / ambiguous across the end-Permian, from each genus's PBDB last appearance."""
    if not TAXA.exists():
        names, lines = sorted(genera), []
        for i in range(0, len(names), 100):
            with urllib.request.urlopen(TAXA_URL + urllib.parse.quote(",".join(names[i:i + 100]))) as resp:
                text = resp.read().decode()
            body = text.splitlines()
            lines.extend(body if not lines else body[1:])
        TAXA.write_text("\n".join(lines) + "\n")
    found = collections.defaultdict(list)
    with open(TAXA, newline="") as f:
        for r in csv.DictReader(f):
            if r["taxon_rank"] == "genus":
                found[r["taxon_name"]].append(r)
    out = {}
    for gname in genera:
        rs = [r for r in found.get(gname, []) if r["phylum"] == phylum[gname]] or found.get(gname, [])
        if len(rs) != 1 or (rs[0]["is_extant"] != "extant" and not rs[0]["lastapp_max_ma"]):
            out[gname] = "unmatched"
        elif rs[0]["is_extant"] == "extant" or float(rs[0]["lastapp_max_ma"]) <= BOUNDARY + 1e-6:
            out[gname] = "survived"
        elif float(rs[0]["lastapp_min_ma"]) >= BOUNDARY - 1e-6:
            out[gname] = "lost"
        else:
            out[gname] = "ambiguous"
    return out


def main():
    species, phylum = sampled_cohort()
    sizes = sorted(len(v) for v in species.values())
    G, S = len(sizes), sum(sizes)
    m_s = S / G
    print(f"PBDB extract sha256 {hashlib.sha256(RAW.read_bytes()).hexdigest()}")
    print(f"sampled cohort: {G} genera, {S} species, mean {m_s:.3f}, "
          f"monotypic share {sum(n == 1 for n in sizes) / G:.3f}, largest genus {sizes[-1]}")

    rows = []
    for name, g in SCENARIOS:
        k = round(g * G)
        row = dict(scenario=name, genus_loss=g,
                   I1_sampled_lower=round(sum(sizes[:k]) / S, 3),
                   I1_sampled_upper=round(1 - (G - k) / S, 3))
        for m in [round(m_s, 2)] + M_VALUES:
            row[f"I0_m{m}_lower"] = round(g / m, 3)
            row[f"I0_m{m}_upper"] = round(1 - (1 - g) / m, 3)
        for e in TARGETS:
            row[f"min_m_for_{int(e * 100)}pct"] = round((1 - g) / (1 - e), 2)  # upper bound reaches e only if m >= this
        rows.append(row)
    with open(OUT / "bounds.tsv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    with open(OUT / "sampled_genus_sizes.tsv", "w", newline="") as f:
        f.write("species_per_genus\tgenera\n")
        for n, c in sorted(collections.Counter(sizes).items()):
            f.write(f"{n}\t{c}\n")
    for r in rows:
        print(r)

    fate = fates(species, phylum)
    n = collections.Counter(fate.values())
    sp = {k: sum(len(species[gn]) for gn in species if fate[gn] == k) for k in n}
    lost, surv, amb = n["lost"], n["survived"], n["ambiguous"] + n["unmatched"]
    s_lost = sp.get("lost", 0)
    i2 = dict(genera=G, species=S, no_later_record=lost, later_record=surv, ambiguous_or_unmatched=amb,
              share_genera_no_later_record_min=round(lost / G, 3),
              share_genera_no_later_record_max=round((lost + amb) / G, 3),
              share_species_in_genera_no_later_record=round(s_lost / S, 3),
              share_species_if_each_later_recorded_genus_kept_one_sampled_species=round(1 - surv / S, 3))
    with open(OUT / "stage_union_diagnostic.tsv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(i2), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerow(i2)
    print("I2 stage-union diagnostic:", i2, dict(n))


if __name__ == "__main__":
    main()
