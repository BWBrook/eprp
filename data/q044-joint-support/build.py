# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas==2.3.3", "numpy==2.3.3"]
# ///
"""Q-044 joint-support screen: per time bin, how many disjoint, adequately sampled spatial windows
of non-marine tetrapod collections exist, where are they, and do they share species?

Reads the Close et al. 2019 Dryad deposit (10.5061/dryad.3v0p84v) as data only; nothing in it is run.
Run from the repository root:  uv run data/q044-joint-support/build.py
"""
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
ZIP = ROOT / "data/raw/dryad-downloads/doi_10_5061_dryad_3v0p84v__v20190218.zip"
SRC = ROOT / ("data/raw/close2019/code-for-close-et-al-diversity-dynamics-of-phanerozoic-"
              "terrestrial-tetrapods-at-the-local-scale")
DL = SRC / "input-data/data_downloads"
OUT = Path(__file__).resolve().parent
COUNTRIES = ROOT / "data/raw/benson2025/country_codes.csv"

RADII_KM = (500, 1000)
MIN_COLLS = (5, 10, 20)
PRIMARY = (1000, 10)
COVERAGE = (0.5, 0.7)
FOCUS = ["Tr3", "Tr4", "Tr5", "J1", "J2", "J3", "J4", "J5", "J6", "K1", "K2", "K3", "K4", "K5", "K6",
         "K7", "K8", "Pg0", "Pg1", "Pg2", "Pg3", "Pg4", "Pg5", "Ng1", "Ng2", "Ng3"]  # Late Triassic to Neogene
COLS = ["occurrence_no", "collection_no", "accepted_name", "accepted_rank", "max_ma", "min_ma", "order",
        "family", "pres_mode", "cc", "geogscale", "stratscale", "environment", "lithification1",
        "paleolat", "paleolng"]


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def terms(name):
    return {t for t in (SRC / "input-data/exclude-terms" / name).read_text().split() if t}


def ids(name):
    return set(pd.read_csv(DL / name, usecols=["occurrence_no"]).occurrence_no)


def clean():
    """The deposit's occurrence and collection exclusions (01 load-alpha-data.R:85-178;
    02 calculate-local-richness.R:55-74), re-expressed here."""
    occ = pd.read_csv(DL / "alpha_tetrapodomorpha.csv", usecols=COLS, low_memory=False,
                      dtype={"cc": str}, keep_default_na=False, na_values={c: [""] for c in COLS if c != "cc"})
    n0 = len(occ)
    occ["accepted_name"] = occ.accepted_name.str.replace(r" \(.*\)", "", regex=True)
    words = occ.accepted_name.str.split()
    sp = occ.accepted_rank.isin(["species", "subspecies"]) & (words.str.len() >= 2)
    occ["genus_name"] = np.where(occ.accepted_rank.isin(["species", "subspecies", "genus"]), words.str[0], "")
    occ["binomial"] = np.where(sp, words.str[0] + " " + words.str[1], "")
    occ["ma_mid"] = (occ.max_ma + occ.min_ma) / 2

    exclude = terms("trace-terms.txt") | terms("egg-terms.txt") | terms("marine-terms.txt") | {
        "Agelaius", "Ancistrodon", "Crocodylus", "Crocodilus", "Alligator", "Lacerta",
        "Fenestrosaurus", "Ovoraptor", "Ornithoides"}
    marine = ids("alpha_cetacea.csv") | ids("alpha_pinnipedimorpha.csv") | ids("alpha_sirenia.csv")
    drop = (occ.order.isin(exclude) | occ.family.isin(exclude) | occ.genus_name.isin(exclude)
            | occ.occurrence_no.isin(marine) | occ.pres_mode.isin(["trace", "cast,trace", "mold/impression,trace"]))
    drop |= occ.occurrence_no.isin([537809, 537868, 558345, 568126, 573786, 573787, 573793, 601727, 851246,
                                    869607, 895947, 896147, 922175, 923804, 923807, 942452, 1089127, 1089130,
                                    1106821, 1178773, 1220778, 1221317, 1221321])
    dino, mamm, squa = ids("alpha_dinosauria.csv"), ids("alpha_mammaliamorpha.csv"), ids("alpha_squamata.csv")
    drop |= occ.occurrence_no.isin(dino) & ((occ.ma_mid < 66) | (occ.max_ma >= 247))
    drop |= occ.occurrence_no.isin(mamm) & (occ.max_ma >= 240)
    drop |= occ.occurrence_no.isin(squa) & (occ.max_ma >= 200)
    drop |= occ.collection_no.isin([137680, 137641, 187582, 13294, 13779, 176285, 179194, 55600, 18284])
    drop |= occ.stratscale.isin(["group", "formation"]) | (occ.geogscale == "basin")
    drop |= (occ.ma_mid <= 5.333) & occ.environment.isin(["cave", "tar", "mire/swamp", "sinkhole"])
    drop |= (occ.ma_mid <= 100) & (occ.lithification1 == "unlithified")
    occ = occ[~drop & occ.paleolat.notna() & occ.paleolng.notna()].copy()
    return occ, n0


def continents():
    c = pd.read_csv(COUNTRIES, keep_default_na=False, dtype=str)
    m = dict(zip(c["ISO3166-1-Alpha-2"], c["Continent"]))
    m.update({"UK": "EU", "AA": "AN"})  # PBDB writes the United Kingdom as UK and Antarctica as AA
    return m


def gcd(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2)
    a = np.sin((p2 - p1) / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(np.radians(lon2 - lon1) / 2) ** 2
    return 2 * 6371.0 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


def mst_length(lat, lon):
    n = len(lat)
    if n < 2:
        return 0.0
    d = gcd(lat[:, None], lon[:, None], lat[None, :], lon[None, :])
    best, done, total = d[0].copy(), np.zeros(n, bool), 0.0
    done[0] = True
    for _ in range(n - 1):
        j = np.argmin(np.where(done, np.inf, best))
        total += best[j]
        done[j] = True
        best = np.minimum(best, d[j])
    return total


def windows(colls, radius, min_colls):
    """Greedy disjoint circular windows: centres on collections, densest first, centres >= 2r apart.
    A lower bound on the number of windows that could be packed, not an optimum."""
    lat, lon = colls.paleolat.values, colls.paleolng.values
    d = gcd(lat[:, None], lon[:, None], lat[None, :], lon[None, :])
    within = d <= radius
    counts = within.sum(1)
    chosen = []
    for i in np.argsort(-counts, kind="stable"):
        if counts[i] < min_colls:
            break
        if all(d[i, j] >= 2 * radius for j in chosen):
            chosen.append(i)
    return [(i, np.flatnonzero(within[i])) for i in chosen]


def main():
    occ, n0 = clean()
    bins = pd.read_csv(SRC / "input-data/equal-length-intervals.csv")
    k = np.searchsorted(bins.FAD.values, occ.ma_mid.values, side="right")  # bins run youngest first; first FAD > ma_mid
    k = np.clip(k, 0, len(bins) - 1)
    inside = (occ.ma_mid.values < bins.FAD.values[k]) & (occ.ma_mid.values >= bins.LAD.values[k])
    inside &= ~np.isin(occ.ma_mid.values, bins.FAD.values)  # the deposit leaves midpoints on a boundary unbinned
    occ = occ[inside].copy()
    occ["bin"] = bins.bin.values[k[inside]]
    occ["spills"] = (occ.max_ma - occ.min_ma) > bins.set_index("bin").duration.reindex(occ.bin).values + 1e-6
    cont = continents()
    print(f"occurrences: {n0} downloaded, {len(occ)} after the deposit's exclusions, with palaeocoordinates and a bin")

    per_bin, per_window = [], []
    for b in FOCUS:
        g = occ[occ.bin == b]
        colls = (g.groupby("collection_no")
                 .agg(paleolat=("paleolat", "first"), paleolng=("paleolng", "first"), cc=("cc", "first"))
                 .reset_index())
        row = dict(bin=b, occurrences=len(g), collections=len(colls),
                   species_occurrences=int((g.binomial != "").sum()), species=g.loc[g.binomial != "", "binomial"].nunique(),
                   share_spilling_bin=round(g.spills.mean(), 3) if len(g) else np.nan)
        for r in RADII_KM:
            for m in MIN_COLLS:
                w = windows(colls, r, m)
                row[f"K_r{r}_n{m}"] = len(w)
                if (r, m) != PRIMARY:
                    continue
                spp_sets, gen_sets, conts, centres = [], [], [], []
                for j, (centre, members) in enumerate(w):
                    wc = colls.iloc[members]
                    wo = g[g.collection_no.isin(wc.collection_no) & (g.binomial != "")]
                    f = wo.binomial.value_counts()
                    u = 1 - (f == 1).sum() / len(wo) if len(wo) else np.nan
                    alpha = wo.groupby("collection_no").binomial.nunique()
                    cn = wc.cc.map(cont).replace("", np.nan).dropna()
                    continent = cn.mode().iloc[0] if len(cn) else "unknown"
                    spp_sets.append(set(f.index))
                    gen_sets.append(set(g.loc[g.collection_no.isin(wc.collection_no) & (g.genus_name != ""), "genus_name"]))
                    conts.append(continent)
                    centres.append((colls.paleolat.iloc[centre], colls.paleolng.iloc[centre]))
                    per_window.append(dict(bin=b, window=j + 1, centre_paleolat=round(centres[-1][0], 2),
                                           centre_paleolng=round(centres[-1][1], 2), continent=continent,
                                           collections=len(wc), species_occurrences=len(wo), species=len(f),
                                           goods_u=round(u, 3) if len(wo) else np.nan,
                                           mean_collection_species=round(alpha.mean(), 2) if len(alpha) else np.nan,
                                           mst_km=round(mst_length(wc.paleolat.values, wc.paleolng.values))))
                us = [x["goods_u"] for x in per_window if x["bin"] == b]
                for c in COVERAGE:
                    row[f"K_primary_u{int(c * 100)}"] = int(sum(1 for x in us if x >= c))
                row["primary_continents"] = ";".join(sorted(set(conts)))
                row["primary_max_windows_one_continent"] = max(pd.Series(conts).value_counts()) if conts else 0
                for level, sets in (("species", spp_sets), ("genera", gen_sets)):
                    union = set().union(*sets) if sets else set()
                    shared = sum(1 for x in union if sum(x in t for t in sets) >= 2)
                    row[f"primary_share_{level}_in_2plus_windows"] = round(shared / len(union), 3) if union else np.nan
                if len(centres) >= 2:
                    la, lo = np.array(centres).T
                    dd = gcd(la[:, None], lo[:, None], la[None, :], lo[None, :])
                    row["primary_mean_centre_distance_km"] = round(dd[np.triu_indices(len(la), 1)].mean())
                else:
                    row["primary_mean_centre_distance_km"] = np.nan
        per_bin.append(row)

    pb = pd.DataFrame(per_bin)
    pb.to_csv(OUT / "per_bin.tsv", sep="\t", index=False, lineterminator="\n")
    pd.DataFrame(per_window).to_csv(OUT / "per_window.tsv", sep="\t", index=False, lineterminator="\n")
    summary = []
    for col in [c for c in pb.columns if c.startswith("K_")]:
        summary.append(dict(measure=col, bins_with_K_ge_4=int((pb[col] >= 4).sum()),
                            bins_with_K_ge_6=int((pb[col] >= 6).sum()), bins=len(pb)))
    sm = pd.DataFrame(summary)
    sm.to_csv(OUT / "summary.tsv", sep="\t", index=False, lineterminator="\n")
    print(sm.to_string(index=False))
    print(f"outer zip sha256 {sha256(ZIP)}")
    print(f"occurrence file sha256 {sha256(DL / 'alpha_tetrapodomorpha.csv')}")


if __name__ == "__main__":
    main()
