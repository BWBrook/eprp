# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib==3.10.*", "numpy==2.*"]
# ///
"""Draw Figures 1-3 of the infrastructure-audit article from committed, checked tables.

    uv run manuscript/figures.py        # from papers/infrastructure-audit/

Inputs are the replay receipts (evidence/replay-20261108/) and the checked panel tables
(evidence/figure-data-20261112/). Every plotted count is asserted against its claims-ledger value
before drawing, so a drifted input fails here rather than in print. Written by Claude (Anthropic).
"""

import csv
import gzip
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
REPLAY = ROOT / "evidence/replay-20261108"
PANEL = ROOT / "evidence/figure-data-20261112"
OUT = ROOT / "manuscript/figures"

FAMILY = {"DP": "#2a78d6", "CI": "#eb6834", "MS": "#1baf7a", "OI": "#eda100"}
FAMILY_NAME = {"DP": "Data provenance and transformation", "CI": "Computation and implementation",
               "MS": "Model sensitivity", "OI": "Output interpretation and calibration"}
INK, MUTED, GRID, SURFACE = "#1f1f1e", "#6b6a64", "#d9d8d2", "#ffffff"
WIDTH = 7.0

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 7.5, "axes.titlesize": 8, "axes.labelsize": 7.5,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK, "axes.spines.top": False,
    "axes.spines.right": False, "axes.linewidth": 0.6, "xtick.major.width": 0.6,
    "ytick.major.width": 0.6, "savefig.dpi": 600, "savefig.facecolor": SURFACE,
})


def load(path):
    return json.loads(path.read_text())


def tsv(path, opener=open):
    with opener(path, "rt") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def tag(ax, letter, x=-0.13):
    ax.text(x, 1.06, letter, transform=ax.transAxes, fontsize=10, fontweight="bold", va="bottom")


def grid(ax, axis="y"):
    ax.grid(axis=axis, color=GRID, linewidth=0.5)
    ax.set_axisbelow(True)


def save(fig, stem):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / f"{stem}.png", bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight")
    plt.close(fig)


def figure1():
    fig = plt.figure(figsize=(WIDTH, 3.6))
    ax = fig.add_axes([0.02, 0.46, 0.96, 0.50])
    ax.set_xlim(0, 6)
    ax.set_ylim(-1.9, 1.2)
    ax.axis("off")
    tag(ax, "A", 0.0)
    links = ["Collection", "Database\nor deposit", "Time scale\nand age model", "Plate model",
             "Analysis\npackage", "Published\nnumber"]
    cases = {1: [(1, "DP"), (3, "DP"), (10, "DP")], 2: [(2, "DP"), (4, "DP"), (5, "CI")], 3: [(9, "MS")],
             4: [(6, "CI"), (7, "OI"), (8, "OI")], 5: [(11, "CI"), (12, "CI")]}
    for i, name in enumerate(links):
        ax.add_patch(FancyBboxPatch((i + 0.08, 0.25), 0.84, 0.75, boxstyle="round,pad=0,rounding_size=0.06",
                                    fc="#f4f3ef", ec=MUTED, lw=0.6))
        ax.text(i + 0.5, 0.625, name, ha="center", va="center", fontsize=7.5)
        if i < 5:
            ax.annotate("", xy=(i + 1.08, 0.625), xytext=(i + 0.92, 0.625),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.7, mutation_scale=7))
        for j, (n, fam) in enumerate(cases.get(i, [])):
            y = -0.2 - 0.52 * j
            ax.scatter(i + 0.5, y, s=150, color=FAMILY[fam], edgecolor=SURFACE, linewidth=1.5, zorder=3)
            ax.text(i + 0.5, y, str(n), ha="center", va="center", fontsize=6.5, color=INK, zorder=4,
                    fontweight="bold")
    handles = [plt.Line2D([], [], marker="o", ls="", ms=7, color=FAMILY[k], label=FAMILY_NAME[k])
               for k in FAMILY]
    ax.legend(handles=handles, loc="lower right", bbox_to_anchor=(1.0, -0.12), frameon=False, ncol=2,
              fontsize=6.8, handletextpad=0.3, columnspacing=1.2)

    bx = fig.add_axes([0.02, 0.0, 0.96, 0.36])
    bx.set_xlim(0, 5)
    bx.set_ylim(0, 1)
    bx.axis("off")
    tag(bx, "B", 0.0)
    steps = ["189 initial candidate\nfindings, plus later\nadditions", "12 selected cases\n(8 Nov 2026)",
             "Replay from\npinned inputs", "Second check\nand wording review", "22 supported\npropositions"]
    for i, s in enumerate(steps):
        bx.add_patch(FancyBboxPatch((i + 0.06, 0.42), 0.88, 0.5, boxstyle="round,pad=0,rounding_size=0.05",
                                    fc=SURFACE, ec=INK, lw=0.7))
        bx.text(i + 0.5, 0.67, s, ha="center", va="center", fontsize=7.2)
        if i < 4:
            bx.annotate("", xy=(i + 1.06, 0.67), xytext=(i + 0.94, 0.67),
                        arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.7, mutation_scale=7))
    corrected = [1, 3, 4, 5, 7, 10]
    bx.text(2.5, 0.22, "Initial accounts corrected in replay and review: cases "
            + ", ".join(map(str, corrected)), ha="center", va="center", fontsize=7, color=INK)
    bx.annotate("", xy=(2.5, 0.42), xytext=(2.5, 0.29),
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6, ls=(0, (2, 2))))
    save(fig, "fig1_cases_workflow")


def figure2():
    fig, axes = plt.subplots(2, 2, figsize=(WIDTH, 5.2))
    fig.subplots_adjust(hspace=0.6, wspace=0.42)
    c = FAMILY["DP"]

    ax = axes[0, 0]
    d = load(REPLAY / "main/case01.json")
    present, absent = d["deposit_mollusca_present_in_snapshot"], d["deposit_mollusca_absent_from_snapshot"]
    assert (present, absent, d["deposit_mollusca_distinct_occurrences"]) == (297657, 71103, 368760)
    ax.barh([1, 0], [present, absent], color=[c, "#9ec5f4"], height=0.55, edgecolor=SURFACE, linewidth=2)
    for y, v in [(1, present), (0, absent)]:
        ax.text(v + 6000, y, f"{v:,}", va="center", fontsize=7)
    ax.set_yticks([1, 0], ["Present in\nsnapshot", "Absent from\nsnapshot"])
    ax.set_xlim(0, 360000)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v / 1000:.0f}k"))
    ax.set_xlabel("Deposited molluscan occurrences")
    grid(ax, "x")
    tag(ax, "A")

    ax = axes[0, 1]
    comps = load(REPLAY / "data/results/pbdb.json")["comparisons"]
    pairs = [(x["from"][:8], x["to"][:8], x["changed_with_later_n_ge50"]) for x in comps
             if x["changed_with_later_n_ge50"] in (460, 317, 17)]
    assert [p[2] for p in pairs] == [460, 317, 17]
    lab = [f"{a[:4]}-{a[4:6]}-{a[6:]}\nto {b[:4]}-{b[4:6]}-{b[6:]}" for a, b, _ in pairs]
    ax.bar(range(3), [p[2] for p in pairs], color=c, width=0.55)
    for i, (_, _, v) in enumerate(pairs):
        ax.text(i, v + 8, f"{v}", ha="center", fontsize=7)
    ax.set_xticks(range(3), lab, fontsize=6.5)
    ax.set_ylabel("Intervals with changed\nmodal base age")
    ax.set_xlabel("Archived snapshot pair")
    grid(ax)
    tag(ax, "B")

    ax = axes[1, 0]
    rows = tsv(PANEL / "triton/comparable.tsv")
    delta = np.array([float(r["delta_after_minus_before_deg"]) for r in rows])
    assert len(delta) == 2267 and (np.abs(delta) > 1e-9).sum() == 1388
    assert (np.abs(delta) >= 1 - 1e-9).sum() == 411
    assert len(tsv(PANEL / "triton/newly_missing.tsv")) == 4
    changed = delta[np.abs(delta) > 1e-9]
    edges = np.arange(np.floor(changed.min()), np.ceil(changed.max()) + 0.25, 0.25)
    ax.hist(changed, bins=edges, color=c, edgecolor=SURFACE, linewidth=0.4)
    ax.set_yscale("log")
    for x in (-1, 1):
        ax.axvline(x, color=INK, lw=0.6, ls=(0, (3, 2)), ymax=0.8)
    ax.set_ylim(0.7, 6000)
    ax.text(0.02, 0.97, "1,388 of 2,267 means changed;\n411 by at least 1° (dashed: ±1°)",
            transform=ax.transAxes, ha="left", va="top", fontsize=6.8)
    ax.set_xlabel("Change in mean absolute paleolatitude (°)")
    ax.set_ylabel("Changed lineage-bins")
    grid(ax)
    tag(ax, "C")

    ax = axes[1, 1]
    rows = tsv(PANEL / "nsb/nsb_signed_age_differences.tsv.gz", gzip.open)
    diff = np.array([float(r["stored_minus_interpolated_age_myr"]) for r in rows])
    over = np.abs(diff) > 0.01
    assert len(diff) == 56387 and over.sum() == 4111
    assert len({r["site_hole"] for r, o in zip(rows, over) if o}) == 56
    lim = np.max(np.abs(diff))
    pos = np.logspace(-6, np.log10(lim) + 0.05, 40)
    edges = np.concatenate([-pos[::-1], [-1e-6, 1e-6], pos])
    edges = np.unique(edges)
    ax.hist(diff, bins=edges, color=c, edgecolor=SURFACE, linewidth=0.3)
    ax.set_xscale("symlog", linthresh=1e-6)
    ax.set_yscale("log")
    for x in (-0.01, 0.01):
        ax.axvline(x, color=INK, lw=0.6, ls=(0, (3, 2)), ymax=0.8)
    ax.set_ylim(0.7, 3e6)
    ax.text(0.02, 0.97, "4,111 of 56,387 differ by more\nthan 0.01 Myr (dashed: ±0.01)", transform=ax.transAxes,
            ha="left", va="top", fontsize=6.8)
    ax.set_xticks([-1, -0.01, 0, 0.01, 1], ["−1", "−0.01", "0", "0.01", "1"])
    ax.set_xlabel("Stored minus interpolated age (Myr; symlog)")
    ax.set_ylabel("Samples")
    grid(ax)
    tag(ax, "D")
    save(fig, "fig2_data_provenance")


def figure3():
    fig, axes = plt.subplots(2, 2, figsize=(WIDTH, 5.4))
    fig.subplots_adjust(hspace=0.62, wspace=0.55)

    ax = axes[0, 0]
    rows = tsv(PANEL / "admtools/sparse_curve.tsv")
    h = np.array([float(r["height"]) for r in rows])
    e = np.array([float(r["error_myr"]) for r in rows])
    seg = np.array([r["deposition_segment"] for r in rows])
    assert len(e) == 8282 and (np.abs(e) > 1e-9).sum() == 3972 and abs(np.abs(e).max() - 2.995776523137465) < 1e-12
    for s in dict.fromkeys(seg):
        m = seg == s
        ax.plot(h[m], e[m], color=FAMILY["CI"], lw=1.2, solid_capstyle="round")
    for x in (8, 14):
        ax.axvline(x, color=INK, lw=0.6, ls=(0, (3, 2)))
    ax.text(27, -2.4, "dashed: hiatuses at\nheights 8 and 14", fontsize=6.5, va="center")
    ax.set_xlabel("Stratigraphic height (model units)")
    ax.set_ylabel("Estimated minus true time (Myr)")
    grid(ax)
    tag(ax, "A")

    ax = axes[0, 1]
    fb = load(REPLAY / "software/case06_fossilbrush.json")
    probes = fb["older_probes"]
    deltas = [round(p["delta"], 1) for p in probes]
    truth = [bool(p["numeric_expected"]) for p in probes]
    flag = [bool(p["package_flag"]) for p in probes]
    assert fb["threshold"] == 5
    assert [d for d, t, f in zip(deltas, truth, flag) if t and not f] == [10, 20, 49.9, 100, 499]
    xs = np.arange(len(deltas))
    for y, vals, name in [(1, truth, "Numeric truth"), (0, flag, "fossilbrush 1.0.6")]:
        ax.scatter(xs, [y] * len(xs), s=40, marker="o",
                   facecolor=[FAMILY["CI"] if v else SURFACE for v in vals],
                   edgecolor=FAMILY["CI"], linewidth=1.0, zorder=3)
    miss = [i for i, (t, f) in enumerate(zip(truth, flag)) if t != f]
    for i in miss:
        ax.add_patch(plt.Rectangle((i - 0.4, -0.35), 0.8, 1.7, fc="#fbe1d6", ec="none", zorder=1))
    ax.set_yticks([1, 0], ["Numeric truth", "fossilbrush 1.0.6"])
    ax.set_xticks(xs, [f"{d:g}" for d in deltas], rotation=90, fontsize=6.5)
    ax.set_ylim(-0.6, 1.6)
    ax.set_xlim(-0.6, len(xs) - 0.4)
    ax.set_xlabel("Difference from reference range (Myr)")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)

    tag(ax, "B")

    ax = axes[1, 0]
    pr = load(REPLAY / "calibration/pyrate_raw.json")["summary"]
    cl = load(REPLAY / "calibration/classical_reaggregate.json")["arms"]["A"]["methods"]
    items = [("PyRate preservation rate, arm 1", pr["high"]["parameters"]["q"]),
             ("PyRate preservation rate, arm 2", pr["low"]["parameters"]["q"]),
             ("Strauss–Sadler bound (tbea)", cl["tbea_ss_upper"]),
             ("Strauss–Sadler bound (EDE)", cl["ede_ss_upper"]),
             ("Robson–Whitlock bound (EDE 0.2.0)", cl["ede_robson_upper"])]
    got = [(x["covered"], x["n"]) for _, x in items]
    assert got == [(81, 100), (33, 50), (1895, 2000), (1899, 2000), (1909, 2000)]
    ys = [4.6, 3.6, 2.0, 1.0, 0.0]
    for y, (name, x) in zip(ys, items):
        col = FAMILY["OI"]
        ax.scatter(x["covered"] / x["n"], y, s=36, color=col, edgecolor=INK, linewidth=0.5, zorder=3)
        ax.text(x["covered"] / x["n"] - 0.012, y, f"{x['covered']:,}/{x['n']:,}", ha="right", va="center",
                fontsize=6.5)
    ax.axvline(0.95, color=INK, lw=0.7, ls=(0, (3, 2)))
    ax.text(0.945, 5.15, "nominal 95%", fontsize=6.5, va="center", ha="right")
    ax.axhline(2.8, color=GRID, lw=0.6)
    ax.set_yticks(ys, [n for n, _ in items], fontsize=6.5)
    ax.set_xlim(0.5, 1.0)
    ax.set_ylim(-0.6, 5.5)
    ax.set_xlabel("Observed coverage of the true value")
    grid(ax, "x")
    tag(ax, "C")

    ax = axes[1, 1]
    sp = load(REPLAY / "software/case09_plate_models.json")["spread_three_models"]["all_reconstructable"]
    ages = sorted(sp, key=int)
    med = [sp[a]["median_deg"] for a in ages]
    ns = [sp[a]["n"] for a in ages]
    assert [round(m, 1) for m in med] == [2.9, 5.7, 4.3, 5.5, 4.7, 13.6]
    xs = [int(a) for a in ages]
    ax.plot(xs, med, color=FAMILY["MS"], lw=2, marker="o", ms=5,
            markeredgecolor=SURFACE, markeredgewidth=1)
    for x, m in zip(xs, med):
        ax.text(x, m + 0.9, f"{m:.1f}°", ha="center", fontsize=6.5)
    for x, n in zip(xs, ns):
        ax.text(x, 0.5, f"{n}", ha="center", va="bottom", fontsize=6, color=MUTED)
    ax.text(-30, 0.5, "n", ha="center", va="bottom", fontsize=6, color=MUTED, style="italic")
    ax.set_xlabel("Age (Ma)")
    ax.set_ylabel("Median paleolatitude spread\namong three models (°)")
    ax.set_ylim(0, 17)
    ax.set_xticks(xs)
    ax.set_xlim(-45, 425)
    grid(ax)
    tag(ax, "D")
    save(fig, "fig3_computation_models_meaning")


if __name__ == "__main__":
    figure1()
    figure2()
    figure3()
    for p in sorted(OUT.glob("fig*.png")):
        print(p.relative_to(ROOT))
