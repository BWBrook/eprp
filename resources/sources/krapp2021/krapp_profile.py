# /// script
# requires-python = ">=3.10"
# dependencies = ["netCDF4==1.7.2", "numpy==2.2.6", "scipy==1.15.3"]
# ///
"""Profile the Krapp et al. (2021) 800 ka climate files mirrored from OSF.

Usage: uv run krapp_profile.py SNAPSHOT_DIR OSF_FILES_TSV OUT_TSV

Verifies every file's size and md5 against the OSF listing; reads the
land/ice/ocean mask (0 ocean, 1 land, 2 ice) for the land area of the Sahul boxes
(as in the other profilers) and New Guinea-Australia connectivity at selected times; reads annual temperature and precipitation for
units and Sahul-window means; counts the documented 15000 precipitation
placeholder in the window. Writes long-format (table, metric, key, value).
"""

import csv
import hashlib
import os
import sys

import netCDF4
import numpy as np
from scipy import ndimage

TIMES = [0, -2000, -3000, -6000, -8000, -10000, -12000, -21000, -60000, -120000, -400000, -799000]
out = []


def add(*row):
    out.append(row)


snap = sys.argv[1]
with open(sys.argv[2], newline="") as f:
    listing = list(csv.DictReader(f, delimiter="\t"))
bad = 0
for r in listing:
    p = os.path.join(snap, r["name"])
    h = hashlib.md5()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    ok = os.path.getsize(p) == int(r["bytes"]) and h.hexdigest() == r["md5"]
    bad += not ok
    if not ok:
        add("md5", "mismatch", r["name"], "")
add("md5", "files_checked", "", len(listing))
add("md5", "files_failed", "", bad)

m = netCDF4.Dataset(os.path.join(snap, "data__icesheets_000-800_cru.nc"))
lat, lon, time = m["lat"][:], m["lon"][:], m["time"][:]
LA, LO = np.meshgrid(lat, lon, indexing="ij")
sahul = (((LA >= -45) & (LA <= -10.6) & (LO >= 112) & (LO <= 155) & ~((LO < 121) & (LA > -17))) | ((LO >= 130.8) & (LO <= 156) & (LA >= -12) & (LA <= 0))
         | ((LO >= 141) & (LO <= 144.5) & (LA > -10.6) & (LA <= -9)))
cell = (0.5 * 111.32) ** 2 * np.cos(np.radians(LA))
ng_pt = (np.abs(lat - (-5.75)).argmin(), np.abs(lon - 141.75).argmin())
au_pt = (np.abs(lat - (-25.25)).argmin(), np.abs(lon - 134.75).argmin())
add("mask", "values", "", str(np.unique(m["mask"][-1])))
for t in TIMES:
    i = int(np.where(time == t)[0][0])
    mk = np.ma.filled(m["mask"][i], -1)
    for v in np.unique(mk[sahul]):
        add("mask", f"sahul_area_km2_by_value_at_{t}", int(v), int(cell[sahul & (mk == v)].sum()))
    lab, _ = ndimage.label(mk == 1, structure=np.ones((3, 3)))
    a, b = lab[ng_pt], lab[au_pt]
    add("connectivity", "new_guinea_joined_to_australia", t, bool(a and a == b))

win = (LA >= -45) & (LA <= 0) & (LO >= 110) & (LO <= 155)
for name, var in (("data__temperature__temp_800ka_ann.nc", None), ("data__precipitation__prec_800ka_ann.nc", None)):
    d = netCDF4.Dataset(os.path.join(snap, name))
    v = [k for k in d.variables if k not in ("lon", "lat", "time")][0]
    add(name, "variable", v, f'{getattr(d[v], "units", "")} | {getattr(d[v], "long_name", "")}')
    tt = d["time"][:]
    for t in (0, -21000, -120000):
        i = int(np.where(tt == t)[0][0])
        x = np.ma.filled(d[v][i].astype(float), np.nan)
        w = x[win]
        add(name, "sahul_window_mean_land", t, round(float(np.nanmean(w[w != 15000])), 2))
        add(name, "sahul_window_cells_equal_15000", t, int((w == 15000).sum()))

with open(sys.argv[3], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
