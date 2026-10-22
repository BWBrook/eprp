# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib==3.9.2", "numpy==2.1.3"]
# ///
"""The vetting pipeline as practised: dated stage events for Q-012, Q-038 and Q-017 (evidence/pipeline-events.tsv).
Writes pipeline_timeline.{png,pdf}; the TSV is the table view.
    uv run --python 3.12 papers/question-first/figures/pipeline_timeline.py"""
import collections
import csv
import datetime as dt
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = pathlib.Path(__file__).resolve().parent
rows = list(csv.DictReader(open(HERE.parent / "evidence/pipeline-events.tsv"), delimiter="\t", quoting=csv.QUOTE_NONE))
STAGES = ["Seed", "Prior check", "Contract", "Support audit", "Identification design", "Finite contract",
          "Technical pilot", "Disposition", "Ranking"]
TYPES = [("entered", "o", "#2a78d6"), ("artefact", "s", "#eb6834"), ("repair", "^", "#1baf7a"),
         ("outcome", "D", "#eda100"), ("disposition", "P", "#e87ba4")]          # validated slots 1-5, shape doubles
QS = [("Q-012", "Q-012  heritable susceptibility versus intrinsic ageing"),
      ("Q-038", "Q-038  which genera die, and is it predictable?"),
      ("Q-017", "Q-017  dark extinction across scales")]
LABELS = {   # (text, vertical offset in points: + up / - down, horizontal alignment)
    ("Q-012", "2026-10-09", "gamma frailty = ageing hazard; design not decisive"): ("frailty ≡ ageing: design not decisive", -11, "left"),
    ("Q-012", "2026-10-16", "kunanyi approved by Barry; Codex GO for pilot, not campaign"): ("cluster pilot approved", -12, "center"),
    ("Q-012", "2026-10-21", "final P11 fails: 2 of 24,000 divergences"): ("sampler fails its screen (2 / 24,000)", 9, "right"),
    ("Q-038", "2026-10-11", "deferred by Barry (76/1418)"): ("deferred, then revived", -12, "left"),
    ("Q-038", "2026-10-19", "restarted after idling (Barry's 19 Oct steer)"): ("restarted", -12, "center"),
    ("Q-038", "2026-10-22", "0 of 5 fits pass the convergence screen"): ("pilot: 0 / 5 converge", 9, "right"),
    ("Q-017", "2026-10-20", "develop: analytic note, then one dual-record audit"): ("develop: analytic note", -12, "center")}
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
d0 = dt.date(2026, 10, 9)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": MUTED, "xtick.color": MUTED,
                     "ytick.color": INK})
fig, axes = plt.subplots(3, 1, figsize=(8.8, 9.0), sharex=True, constrained_layout=True)
for ax, (q, title) in zip(axes, QS):
    ev = [r for r in rows if r["question"] == q]
    slot = collections.Counter((r["date"], r["stage"]) for r in ev)
    seen = collections.Counter()
    pts = []
    for r in ev:
        key = (r["date"], r["stage"])
        n, k = slot[key], seen[key]
        seen[key] += 1
        x = (dt.date.fromisoformat(r["date"]) - d0).days + (k - (n - 1) / 2) * min(0.16, 0.8 / n)
        pts.append((x, STAGES.index(r["stage"]), r))
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=MUTED, linewidth=0.6, alpha=0.35, zorder=1)
    for name, mk, col in TYPES:
        sel = [p for p in pts if p[2]["event_type"] == name]
        ax.scatter([p[0] for p in sel], [p[1] for p in sel], marker=mk, s=34, color=col, edgecolor="#ffffff",
                   linewidth=0.8, zorder=3)
    for x, y, r in pts:
        lab = LABELS.get((q, r["date"], r["label"]))
        if lab:
            ax.annotate(lab[0], (x, y), xytext=(0, lab[1]), textcoords="offset points", ha=lab[2], va="center",
                        fontsize=7.5, color=INK, zorder=4)
    ax.set_yticks(range(len(STAGES)), STAGES)
    ax.set_ylim(len(STAGES) - 0.4, -0.6)
    ax.axhline(6.5, color=MUTED, linewidth=0.6, linestyle=(0, (2, 2)))
    ax.grid(axis="x", color=GRID, linewidth=0.6, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title(f"{title}  ({len(ev)} events)", loc="left", fontsize=9.5, color=INK, fontweight="bold")
ndays = 14
axes[-1].set_xticks(range(ndays), [str((d0 + dt.timedelta(i)).day) for i in range(ndays)])
axes[-1].set_xlim(-0.6, ndays - 0.4)
axes[-1].set_xlabel("October 2026 (events within a day are spread horizontally; the faint line joins them in record order)")
counts = collections.Counter(r["event_type"] for r in rows)
axes[0].legend([Line2D([], [], marker=mk, color=col, linestyle="", markersize=6, markeredgecolor="#ffffff")
                for _, mk, col in TYPES], [f"{n} ({counts[n]})" for n, _, _ in TYPES], frameon=False, ncol=5,
               loc="lower left", bbox_to_anchor=(0.0, 1.07), fontsize=8)
for ext in ("png", "pdf"):
    fig.savefig(HERE / f"pipeline_timeline.{ext}", dpi=200, facecolor="#ffffff")
