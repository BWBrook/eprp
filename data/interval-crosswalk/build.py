# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy==2.5.3", "pandas==3.0.6", "mat-io==1.0.0"]
# ///
"""Interval crosswalk between PhanDA stage slices, Song et al. (2021) bins and PBDB stages.

Descriptive capability probe. Native intervals are kept as published; overlaps are
computed in one reference frame (PBDB stage ages, ICS chart v2024/12). Run from the
repository root:  uv run data/interval-crosswalk/build.py
"""

import hashlib
import json
import re
import urllib.request
from pathlib import Path

import matio
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
OUT = Path(__file__).resolve().parent
UA = {"User-Agent": "EPRP-orientation/0.1"}

PHANDA = "https://raw.githubusercontent.com/EJJudd/PhanDA/9f06c0d9764f3da77cb0819e0ac87c01182ba341"
SOURCES = {
    "phanda/PhanDA_GMSTandCO2_percentiles.csv": f"{PHANDA}/5_Outputs/PhanDA_GMSTandCO2_percentiles.csv",
    "phanda/PhanDA_GMST_ensemble.mat": f"{PHANDA}/5_Outputs/PhanDA_GMST_ensemble.mat",
    "song2021/R_code_extinction_rate.R": "https://zenodo.org/records/5027293/files/R%20code%20for%20extinction%20rate.R?download=1",
    "pbdb/intervals_scale1.json": "https://paleobiodb.org/data1.2/intervals/list.json?scale=1&show=class",
}

# Song bin 20/21 split the Visean at 338.8 Ma (deposited script, lines 39-40).
VISEAN_SPLIT_MA = 338.8
# PhanDA names that are not single PBDB stage names.
PHANDA_ALIASES = {
    "Holocene": ["Greenlandian", "Northgrippian", "Meghalayan"],
    "Upper Pleistocene": ["Late Pleistocene"],
}
EVENT_INTERVALS = {
    "Hirnantian": "end-Ordovician", "Frasnian": "Late Devonian", "Famennian": "Late Devonian",
    "Capitanian": "Capitanian", "Changhsingian": "end-Permian", "Rhaetian": "end-Triassic",
    "Toarcian": "Toarcian OAE", "Cenomanian": "OAE2", "Turonian": "OAE2",
    "Maastrichtian": "end-Cretaceous", "PETM": "PETM",
}


def fetch(rel, url):
    path = RAW / rel
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
            path.write_bytes(r.read())
    data = path.read_bytes()
    return {"file": f"data/raw/{rel}", "url": url, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def pbdb_stages():
    recs = json.loads((RAW / "pbdb/intervals_scale1.json").read_text())["records"]
    rows = [r for r in recs if r["itp"] == "age" or (r["itp"] == "epoch" and r["nam"] == "Pridoli")]
    return {r["nam"]: (float(r["eag"]), float(r["lag"])) for r in rows}


def song_bins():
    text = (RAW / "song2021/R_code_extinction_rate.R").read_text(encoding="utf-8", errors="replace")
    bins = {}
    for sub, num in re.findall(r"binno\[(.*?)\]\s*=\s*(\d+)", text, flags=re.S):
        bins.setdefault(int(num), []).extend(re.findall(r'stage == "([^"]+)"', sub))
    return bins


def segments(components, ref, partial=None):
    segs, missing = [], []
    for c in components:
        if partial and c in partial:
            segs.append(partial[c])
        elif c in ref:
            segs.append(ref[c])
        else:
            missing.append(c)
    return segs, missing


def overlap(a, b):
    return sum(max(0.0, min(ao, bo) - max(ay, by)) for ao, ay in a for bo, by in b)


def span(segs):
    return sum(o - y for o, y in segs)


def main():
    manifest = pd.DataFrame([fetch(rel, url) for rel, url in SOURCES.items()])
    manifest.insert(0, "retrieved", "2026-10-08")
    manifest.to_csv(OUT / "sources.tsv", sep="\t", index=False)

    ref = pbdb_stages()
    phanda = pd.read_csv(RAW / "phanda/PhanDA_GMSTandCO2_percentiles.csv")
    petm = phanda.loc[phanda.Stage == "PETM", ["LowerAge", "UpperAge"]].iloc[0]
    petm_seg = (float(petm.LowerAge), float(petm.UpperAge))

    rows = []
    for name, (o, y) in ref.items():
        rows.append(dict(source="pbdb", interval=name, components=name, native_older_ma=o,
                         native_younger_ma=y, ref_older_ma=o, ref_younger_ma=y, flags=""))
    phanda_segs = {}
    for _, r in phanda.iterrows():
        comps = PHANDA_ALIASES.get(r.Stage, r.Stage.split("/"))
        flags = []
        if r.Stage == "PETM":
            segs, missing = [petm_seg], []
            flags.append("sub-stage slice in lowermost Ypresian; native GTS2020 ages used in reference frame")
        else:
            segs, missing = segments(comps, ref)
        if r.Stage == "Ypresian":
            flags.append("PhanDA Ypresian excludes its PETM slice")
            segs = [(petm_seg[1], segs[0][1])]
        if missing:
            flags.append("unmatched components: " + ",".join(missing))
        phanda_segs[r.Stage] = segs
        rows.append(dict(source="phanda", interval=r.Stage, components="+".join(comps),
                         native_older_ma=r.LowerAge, native_younger_ma=r.UpperAge,
                         ref_older_ma=max(o for o, _ in segs) if segs else np.nan,
                         ref_younger_ma=min(y for _, y in segs) if segs else np.nan,
                         flags="; ".join(flags)))
    bins = song_bins()
    visean = ref["Visean"]
    song_segs = {}
    for b, raw in sorted(bins.items()):
        comps = list(dict.fromkeys(raw))
        flags, partial = [], {}
        if len(comps) < len(raw):
            flags.append("duplicate stage listed: " + ",".join(sorted({c for c in raw if raw.count(c) > 1})))
        if "Visean" in comps:
            partial["Visean"] = (visean[0], VISEAN_SPLIT_MA) if b == 20 else (VISEAN_SPLIT_MA, visean[1])
            flags.append("Visean split at 338.8 Ma via vector && (errors in R>=4.3; first-element semantics earlier)")
        segs, missing = segments(comps, ref, partial)
        if missing:
            flags.append("unmatched components: " + ",".join(missing))
        song_segs[b] = segs
        rows.append(dict(source="song2021", interval=f"bin{b:02d}", components="+".join(comps),
                         native_older_ma=np.nan, native_younger_ma=np.nan,
                         ref_older_ma=max(o for o, _ in segs) if segs else np.nan,
                         ref_younger_ma=min(y for _, y in segs) if segs else np.nan,
                         flags="; ".join(flags + ["bin ages not deposited (bindata2.txt)"])))
    intervals = pd.DataFrame(rows)
    intervals.to_csv(OUT / "intervals.tsv", sep="\t", index=False, float_format="%.4f")

    ov = []
    for p, psegs in phanda_segs.items():
        hits = [(b, overlap(psegs, ssegs)) for b, ssegs in song_segs.items()]
        hits = [(b, s) for b, s in hits if s > 1e-9]
        pspan = span(psegs)
        if not hits:
            ov.append(dict(phanda_slice=p, song_bin="", shared_myr=0.0, frac_of_slice=0.0,
                           frac_of_bin=0.0, relation="no Song bin"))
        for b, s in hits:
            fs, fb = s / pspan, s / span(song_segs[b])
            rel = ("one-to-one" if fs > 0.99 and fb > 0.99 else
                   "slice within bin" if fs > 0.99 else
                   "bin within slice" if fb > 0.99 else "partial")
            ov.append(dict(phanda_slice=p, song_bin=f"bin{b:02d}", shared_myr=s, frac_of_slice=fs,
                           frac_of_bin=fb, relation=rel))
    ov = pd.DataFrame(ov)
    ov["event"] = ov.phanda_slice.map(lambda s: "; ".join(sorted({EVENT_INTERVALS[c] for c in re.split(r"/", s) if c in EVENT_INTERVALS})))
    ov.to_csv(OUT / "phanda_song_overlaps.tsv", sep="\t", index=False, float_format="%.4f")

    ens = matio.load_from_mat(RAW / "phanda/PhanDA_GMST_ensemble.mat")["GMST"]
    scen = [c for c in ens.columns if c.startswith("Scenario")]
    mem = pd.DataFrame({"stage": ens.Stage, "older_ma": ens.LowerAge, "younger_ma": ens.UpperAge})
    for c in scen:
        mem[f"n_{c}"] = [np.asarray(v).size for v in ens[c]]
    adj = []
    for c in [c for c in scen if c != "ScenarioAll"]:
        for i in range(len(ens) - 1):
            a, b = np.asarray(ens[c].iloc[i]).ravel(), np.asarray(ens[c].iloc[i + 1]).ravel()
            same = a.size == b.size
            adj.append(dict(scenario=c, younger=ens.Stage.iloc[i], older=ens.Stage.iloc[i + 1],
                            equal_count=same, member_r=np.corrcoef(a, b)[0, 1] if same else np.nan))
    mem.to_csv(OUT / "phanda_ensemble_members.tsv", sep="\t", index=False)
    adj = pd.DataFrame(adj)
    adj.to_csv(OUT / "phanda_ensemble_adjacency.tsv", sep="\t", index=False, float_format="%.4f")

    print("PBDB stages:", (intervals.source == "pbdb").sum(), "| PhanDA slices:", len(phanda),
          "| Song bins:", len(bins), "(max bin", max(bins), ")")
    print("PhanDA unmatched:", intervals.loc[(intervals.source == "phanda") & intervals["flags"].str.contains("unmatched"), "interval"].tolist())
    print("Song unmatched:", intervals.loc[(intervals.source == "song2021") & intervals["flags"].str.contains("unmatched"), ["interval", "flags"]].values.tolist())
    rel = ov.groupby("phanda_slice").relation.agg(lambda s: s.iloc[0] if len(s) == 1 else "straddles bins")
    print("PhanDA slice -> Song bin relations:", rel.value_counts().to_dict())
    assigned = {c for comps in bins.values() for c in comps}
    print("PBDB stages in no Song bin:", [n for n in ref if n not in assigned])
    print("Song bins with no PhanDA overlap:", sorted(set(f"bin{b:02d}" for b in song_segs) - set(ov.song_bin)))
    print("\nEvent rows:\n", ov[ov.event != ""][["phanda_slice", "song_bin", "relation", "frac_of_slice", "frac_of_bin", "event"]].to_string(index=False))
    eq = adj.groupby("scenario").agg(pairs=("equal_count", "size"), equal=("equal_count", "sum"),
                                     median_r=("member_r", "median"))
    print("\nEnsemble members per stage, ScenarioAll:", sorted(set(mem["n_ScenarioAll"])),
          "| Scenario01 range:", mem.n_Scenario01.min(), "-", mem.n_Scenario01.max())
    print("Adjacent stages with equal member counts, and median member correlation where equal:\n", eq.to_string())


if __name__ == "__main__":
    main()
