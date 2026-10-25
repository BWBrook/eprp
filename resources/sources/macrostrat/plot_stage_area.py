# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib>=3.8"]
# ///
"""Plot Macrostrat's North American column area with marine and non-marine units, by international stage.

Usage: uv run plot_stage_area.py STAGE_AREA_TSV OUT_PNG
"""

import csv
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

tsv, out_png = sys.argv[1:3]
INK, MUTED, SURFACE, GRID = "#0b0b0b", "#52514e", "#fcfcfb", "#e4e3df"
MARINE, NONMARINE = "#2a78d6", "#eb6834"
rows = list(csv.DictReader(open(tsv, encoding="utf-8"), delimiter="\t"))
x = [float(r["mid_ma"]) for r in rows]
m = [int(r["na_marine_km2"]) / 1e6 for r in rows]
n = [int(r["na_nonmarine_km2"]) / 1e6 for r in rows]

fig, ax = plt.subplots(figsize=(9, 4.2), dpi=150, facecolor=SURFACE)
ax.set_facecolor(SURFACE)
ax.plot(x, m, color=MARINE, lw=2, drawstyle="steps-mid", label="columns with a marine unit")
ax.plot(x, n, color=NONMARINE, lw=2, drawstyle="steps-mid", label="columns with a non-marine unit")
for age, label, y, va in [(443.8, "end-Ordovician", 0.2, "bottom"), (251.9, "end-Permian", 12.6, "top"),
                          (201.4, "end-Triassic", 12.6, "top"), (66.0, "end-Cretaceous", 12.6, "top")]:
    ax.axvline(age, color=GRID, lw=1, zorder=0)
    ax.text(age, y, " " + label + " ", color=MUTED, fontsize=8, va=va, rotation=90, ha="right")
ax.text(492, 8.6, "marine", color=INK, fontsize=9)
ax.text(330, 1.35, "non-marine", color=INK, fontsize=9)
ax.set_xlim(540, 0)
ax.set_ylim(0, 13)
ax.set_xlabel("Age (Ma), at each international stage's midpoint", color=MUTED)
ax.set_ylabel("Column area (million km²)", color=MUTED)
ax.grid(axis="y", color=GRID, lw=0.8)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(GRID)
ax.tick_params(colors=MUTED)
ax.legend(frameon=False, loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, fontsize=8, labelcolor=INK)
ax.set_title("Macrostrat, North America: rock record by environment", color=INK, loc="left", fontsize=11, pad=22)
fig.tight_layout()
fig.savefig(out_png, facecolor=SURFACE)
