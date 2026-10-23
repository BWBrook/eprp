# /// script
# requires-python = ">=3.10"
# dependencies = ["netCDF4==1.7.2", "numpy==2.2.6", "scipy==1.15.3"]
# ///
"""Profile Beyer et al. (2020) Late Quaternary climate NetCDFs for Sahul.

Usage: uv run beyer_profile.py ENVIRONMENT_NC MONTHLY_NPP_NC OUT_TSV

Reports dimensions, attributes (not the personal Contact attribute) and units;
land area from the data's own land mask (cells with BIO1) in the Sahul boxes used
by the other profilers and in sub-regions, for comparison with Pico et al. (2020);
area-weighted BIO1 and BIO12 over the Sahul boxes; land cells the main file codes
as biome 0 (water) with NPP 0; the main and monthly-NPP files compared with and
without those cells; and whether New Guinea and Australia are one landmass.
"""

import csv
import sys

import netCDF4
import numpy as np
from scipy import ndimage

TIMES = [0, -1000, -2000, -3000, -6000, -8000, -10000, -12000, -14000, -21000, -30000, -40000, -50000, -60000,
         -80000, -100000, -120000]
out = []


def add(*row):
    out.append(row)


env = netCDF4.Dataset(sys.argv[1])
npp = netCDF4.Dataset(sys.argv[2])
for k in env.ncattrs():
    if k != "Contact":
        add("attrs", "global", k, str(env.getncattr(k))[:200])
for name, d in env.dimensions.items():
    add("dims", name, "", len(d))
for name, v in env.variables.items():
    add("variables", name, str(v.dimensions), f'{getattr(v, "units", "")} | {getattr(v, "long_name", "")}'[:160])
lon, lat, time = env["longitude"][:], env["latitude"][:], env["time"][:]
add("time", "steps", "", len(time))
add("time", "range", "", f"{time.min()} to {time.max()}")
LA, LO = np.meshgrid(lat, lon, indexing="ij")
cell = (0.5 * 111.32) ** 2 * np.cos(np.radians(LA))
aus = (LA >= -45) & (LA <= -10.6) & (LO >= 112) & (LO <= 155) & ~((LO < 121) & (LA > -17))
ng = (LO >= 130.8) & (LO <= 156) & (LA >= -12) & (LA <= 0)
ts = (LO >= 141) & (LO <= 144.5) & (LA > -10.6) & (LA <= -9)
boxes = {
    "sahul_boxes": aus | ng | ts,
    "australia_box": aus,
    "new_guinea_box": ng,
    "arafura_carpentaria_torres_125-146E_20-5S": (LO >= 125) & (LO <= 146) & (LA >= -20) & (LA <= -5),
    "northern_shelf_129-146E_17-8S": (LO >= 129) & (LO <= 146) & (LA >= -17) & (LA <= -8),
    "northwest_shelf_112-129E_24-10S": (LO >= 112) & (LO <= 129) & (LA >= -24) & (LA <= -10),
    "bass_strait_tasmania_143-149E_44-38.5S": (LO >= 143) & (LO <= 149) & (LA >= -44) & (LA <= -38.5),
    "sunda_98-118E_8S-8N": (LO >= 98) & (LO <= 118) & (LA >= -8) & (LA <= 8),
}
idx = {int(t): i for i, t in enumerate(time)}
land0 = ~np.isnan(np.ma.filled(env["BIO1"][idx[0]].astype(float), np.nan))
ng_pt = (np.abs(lat - (-5.75)).argmin(), np.abs(lon - 141.75).argmin())
au_pt = (np.abs(lat - (-25.25)).argmin(), np.abs(lon - 134.75).argmin())
for t in TIMES:
    i = idx[t]
    b1 = np.ma.filled(env["BIO1"][i].astype(float), np.nan)
    b12 = np.ma.filled(env["BIO12"][i].astype(float), np.nan)
    land = ~np.isnan(b1)
    for name, m in boxes.items():
        add("land_area_km2", name, t, int(cell[land & m].sum()))
        add("land_gain_vs_0ka_km2", name, t, int(cell[land & m].sum() - cell[land0 & m].sum()))
    s = land & boxes["sahul_boxes"]
    add("sahul_boxes_area_weighted", "bio1_c", t, round(float(np.average(b1[s], weights=cell[s])), 2))
    add("sahul_boxes_area_weighted", "bio12_mm", t, round(float(np.average(b12[s], weights=cell[s])), 1))
    lab, _ = ndimage.label(land, structure=np.ones((3, 3)))
    add("connectivity", "new_guinea_joined_to_australia", t, bool(lab[ng_pt] and lab[ng_pt] == lab[au_pt]))
    bio = np.ma.filled(env["biome"][i].astype(float), np.nan)
    water_land = land & (bio == 0)
    add("main_file_land_coded_water", "cells_global", t, int(water_land.sum()))
    add("main_file_land_coded_water", "cells_sahul_boxes", t, f"{int((water_land & boxes['sahul_boxes']).sum())} of {int(s.sum())}")
    add("main_file_land_coded_water", "of_which_ocean_at_0ka_global", t, int((water_land & ~land0).sum()))
    if t in (0, -21000):
        win = (LO >= 110) & (LO <= 155) & (LA >= -45) & (LA <= 0)
        bio2 = np.ma.filled(npp["biome"][i].astype(float), np.nan)
        n1 = np.ma.filled(env["npp"][i].astype(float), np.nan)
        n2 = np.ma.filled(npp["npp"][i].astype(float), np.nan)
        both = win & ~np.isnan(bio) & ~np.isnan(bio2)
        add("files_compared_window", "biome_cells_differing", t, int((bio[both] != bio2[both]).sum()))
        add("files_compared_window", "biome_cells_differing_excluding_water_coded", t, int((bio[both & ~water_land] != bio2[both & ~water_land]).sum()))
        ok = win & ~np.isnan(n1) & ~np.isnan(n2)
        add("files_compared_window", "npp_correlation", t, round(float(np.corrcoef(n1[ok], n2[ok])[0, 1]), 3))
        ok2 = ok & ~water_land
        add("files_compared_window", "npp_correlation_excluding_water_coded", t, round(float(np.corrcoef(n1[ok2], n2[ok2])[0, 1]), 3))
        add("files_compared_window", "same_land_mask", t, bool((np.isnan(n1[win]) == np.isnan(n2[win])).all()))
        vals, counts = np.unique(bio[s], return_counts=True)
        for v, c in sorted(zip(vals, counts), key=lambda x: -x[1])[:8]:
            add("sahul_boxes_biome_cells", t, int(v), int(c))

with open(sys.argv[3], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
