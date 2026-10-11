# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas==2.3.3", "numpy==2.3.3"]
# ///
"""Q-027 joint-support screen: per-stage palaeolatitudinal coverage of marine animal occurrences,
inside and outside Europe + North America, from the PBDB download deposited with Benson et al. 2025
(Zenodo 10.5281/zenodo.15269137, CC BY 4.0). Only the needed archive members are fetched, by HTTP
range requests. This is a support screen, not a replication of Benson et al.'s pipeline.
Run from the repository root:  uv run data/q027-joint-support/build.py
"""

import hashlib
import io
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "benson2025"
OUT = Path(__file__).resolve().parent
URL = ("https://zenodo.org/api/records/15269137/files/"
       "marine-lbg-ms-code-submission-2025-04-22%202.zip/content")
ARCHIVE_SIZE = 1549270962
PREFIX = "marine-lbg-ms-code-submission-2025-04-22 2/input/"
MEMBERS = {
    "occurrences.csv": PREFIX + "marine_inverts/PBDB_CSV_data_downloads/2022-05-23-14-15-24/Animalia^Chordata_data.csv",
    "marine_regions.csv": PREFIX + "marine_regions.csv",
    "country_codes.csv": PREFIX + "country-codes_csv.csv",
    "pbdb_time_int.csv": PREFIX + "pbdb_time_int.csv",
}
BANDS = [(0, 20), (20, 40), (40, 60), (60, 90)]  # absolute palaeolatitude, degrees
CELL_DEG = 5  # approximately equal-area cells: 5-degree latitude bands, longitude width scaled by cos(lat)
THRESHOLDS = (3, 10, 20)  # cells per band outside Europe + North America; screening levels, not power
COLUMNS = ["occurrence_no", "collection_no", "accepted_rank", "genus", "max_ma", "min_ma",
           "cc", "paleolat", "paleolng", "lithification1"]


class RangeFile(io.RawIOBase):
    def __init__(self, url, size):
        self.url, self.size, self.pos = url, size, 0

    def seekable(self):
        return True

    def readable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, off, whence=0):
        self.pos = off if whence == 0 else (self.pos + off if whence == 1 else self.size + off)
        return self.pos

    def readinto(self, b):
        if self.pos >= self.size or len(b) == 0:
            return 0
        end = min(self.pos + len(b), self.size) - 1
        req = urllib.request.Request(self.url, headers={"Range": f"bytes={self.pos}-{end}",
                                                        "User-Agent": "eprp-q027-support/0.1"})
        with urllib.request.urlopen(req, timeout=300) as r:
            data = r.read()
        b[:len(data)] = data
        self.pos += len(data)
        return len(data)


def fetch():
    RAW.mkdir(parents=True, exist_ok=True)
    missing = {k: v for k, v in MEMBERS.items() if not (RAW / k).exists()}
    if missing:
        zf = zipfile.ZipFile(io.BufferedReader(RangeFile(URL, ARCHIVE_SIZE), buffer_size=4 << 20))
        for local, member in missing.items():
            with zf.open(member) as src, open(RAW / local, "wb") as dst:  # zipfile checks the member CRC32
                while chunk := src.read(8 << 20):
                    dst.write(chunk)
    for local in MEMBERS:
        h = hashlib.sha256((RAW / local).read_bytes()).hexdigest()
        print(f"{local}\tsha256={h}")


def europe_north_america_codes():
    regions = pd.read_csv(RAW / "marine_regions.csv")
    codes = pd.read_csv(RAW / "country_codes.csv", keep_default_na=False)
    names = {}
    for col in ("official_name_en", "CLDR display name"):
        for name, iso in zip(codes[col], codes["ISO3166-1-Alpha-2"]):
            if name:
                names[name.strip().lower()] = iso
    names.update({"united kingdom": "GB", "moldova, republic of": "MD", "bosnia & herzegovina": "BA",
                  "united states": "US"})
    keep = regions[regions.region_name.isin(["Europe", "North America"])].country_name
    unmatched = [n for n in keep if n.strip().lower() not in names]
    if unmatched:
        print("unmatched Europe/North America names:", unmatched)
    iso = {names[n.strip().lower()] for n in keep if n.strip().lower() in names}
    return iso | {"UK"}  # PBDB writes the United Kingdom as UK


def stages():
    t = pd.read_csv(RAW / "pbdb_time_int.csv")
    s = t[(t.scale_no == 1) & (t.scale_level == 5)][["interval_name", "max_ma", "min_ma"]]
    return s.sort_values("max_ma").reset_index(drop=True)


def main():
    fetch()
    occ = pd.read_csv(RAW / "occurrences.csv", usecols=COLUMNS, low_memory=False)
    n0 = len(occ)
    occ = occ[occ.accepted_rank.isin(["genus", "subgenus", "species"]) & occ.genus.notna()]
    occ = occ[occ.lithification1.fillna("") != "unlithified"]
    occ = occ[occ.paleolat.notna() & occ.paleolng.notna()]
    st = stages()
    # assign to a stage only when the occurrence's age range lies within it
    idx = np.searchsorted(st.max_ma.values, occ.max_ma.values - 1e-9, side="left")  # first stage whose base >= occurrence max
    idx = np.clip(idx, 0, len(st) - 1)
    ok = (occ.min_ma.values >= st.min_ma.values[idx] - 1e-9) & (occ.max_ma.values <= st.max_ma.values[idx] + 1e-9)
    occ = occ[ok].copy()
    occ["stage"] = st.interval_name.values[idx[ok]]
    occ["stage_base_ma"] = st.max_ma.values[idx[ok]]
    occ["eu_na"] = occ.cc.isin(europe_north_america_codes())
    lat_i = np.floor((occ.paleolat.values + 90) / CELL_DEG).astype(int)
    lat_mid = -90 + (lat_i + 0.5) * CELL_DEG
    n_lon = np.maximum(1, np.round(360 / CELL_DEG * np.cos(np.radians(lat_mid)))).astype(int)
    lon_i = np.floor((occ.paleolng.values + 180) / 360 * n_lon).astype(int)
    occ["cell"] = lat_i * 1000 + lon_i
    occ["abslat"] = occ.paleolat.abs()
    print(f"occurrences: {n0} downloaded, {len(occ)} kept (genus-level, lithified/unknown, "
          f"palaeocoordinates, resolved to one stage)")

    rows = []
    for (stage, base), g in occ.groupby(["stage", "stage_base_ma"], sort=False):
        row = dict(stage=stage, base_ma=base, occurrences=len(g), collections=g.collection_no.nunique(),
                   genera=g.genus.nunique(), cells=g.cell.nunique(),
                   cells_eu_na_share=round(g[g.eu_na].cell.nunique() / max(g.cell.nunique(), 1), 2))
        for lo, hi in BANDS:
            band = g[(g.abslat >= lo) & (g.abslat < hi)]
            row[f"cells_{lo}_{hi}"] = band.cell.nunique()
            row[f"cells_{lo}_{hi}_outside"] = band[~band.eu_na].cell.nunique()
        out = [row[f"cells_{lo}_{hi}_outside"] for lo, hi in BANDS]
        for k in THRESHOLDS:
            row[f"three_bands_outside_ge{k}"] = out[0] >= k and out[1] >= k and (out[2] + out[3]) >= k
        rows.append(row)
    tab = pd.DataFrame(rows).sort_values("base_ma", ascending=False)
    tab.to_csv(OUT / "per_stage.tsv", sep="\t", index=False, lineterminator="\n")
    n = len(tab)
    eras = [("Palaeozoic", 541, 251.902), ("Mesozoic", 251.902, 66.0), ("Cenozoic", 66.0, 0)]
    summary = []
    for k in THRESHOLDS:
        col = f"three_bands_outside_ge{k}"
        rec = dict(threshold_cells_per_band=k, stages_total=n, stages_passing=int(tab[col].sum()))
        for name, older, younger in eras:
            sub = tab[(tab.base_ma <= older + 1e-6) & (tab.base_ma > younger + 1e-6)]
            rec[f"{name}_passing"] = f"{int(sub[col].sum())}/{len(sub)}"
        summary.append(rec)
    pd.DataFrame(summary).to_csv(OUT / "summary.tsv", sep="\t", index=False, lineterminator="\n")
    print(pd.DataFrame(summary).to_string(index=False))
    print("median share of occupied cells in Europe + North America:", tab.cells_eu_na_share.median())


if __name__ == "__main__":
    main()
