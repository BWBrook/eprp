"""Q-042: sharp bounds on end-Permian species loss, conditional on stated information.

Information sets (see README):
  I0  genus-loss fraction g and mean species per genus m only.
      Lower bound g/m (each lost genus has at least one species; survivors lose none).
      Upper bound 1 - (1 - g)/m (each surviving genus keeps at least one start-cohort species).
  I1  I0 plus the full genus-size distribution: the lower bound becomes the species share of the
      smallest g*G genera; the upper bound is unchanged.
  I2  the sampled cohort itself: which genera were lost (PBDB last appearance) and their sampled
      species counts. Lower bound: species in lost genera / S. Upper: 1 - surviving genera / S.
      Genera whose last appearance straddles the boundary are assigned both ways.
The sampled distribution here is PBDB's Changhsingian marine animal species-level record. It is a
labelled information set, not the true species pool: unsampled species raise the true m.

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


def sampled_cohort():
    if not RAW.exists():
        RAW.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(URL, RAW)
    species, phylum = collections.defaultdict(set), {}
    with open(RAW, newline="") as f:
        for r in csv.DictReader(f):
            if r["accepted_rank"] in ("species", "subspecies") and r["genus"]:
                name = re.sub(r" \(.*?\)", "", r["accepted_name"]).split()  # drop subgenus brackets
                genus = name[0]
                species[genus].add(" ".join(name[:2]))
                phylum[genus] = r["phylum"]
    return species, phylum


def fates(genera, phylum):
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
    i2 = dict(genera=G, species=S, lost=lost, survived=surv, ambiguous_or_unmatched=amb,
              genus_loss_min=round(lost / G, 3), genus_loss_max=round((lost + amb) / G, 3),
              species_loss_lower=round(s_lost / S, 3),
              species_loss_upper=round(1 - surv / S, 3))
    with open(OUT / "matched_cohort.tsv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(i2), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerow(i2)
    print("I2 matched sampled cohort:", i2, dict(n))


if __name__ == "__main__":
    main()
