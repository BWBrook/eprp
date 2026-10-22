# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib==3.9.2", "numpy==2.1.3"]
# ///
"""Decision changes per day, by who made the change (A) and by the kind of evidence (B), from the WIP ledger.
Writes decision_changes_by_day.{png,pdf,tsv} (the TSV is the figure's table view).
    uv run --python 3.12 papers/question-first/figures/decision_changes_by_day.py"""
import csv
import datetime as dt
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
rows = list(csv.DictReader(open(HERE.parent / "evidence/decision-changes-draft.tsv"), delimiter="\t", quoting=csv.QUOTE_NONE))
SLOTS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]       # dataviz reference categorical slots 1-5, validated
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
WHO = [("Codex", {"Codex"}), ("Claude", {"Claude", "Claude (side session)"}), ("Barry", {"Barry"}),
       ("External (GPT-6 Pro)", {"external (GPT-6 Pro review)"}), ("Joint", {"joint"})]
KIND = [("Counterexample", {"counterexample"}), ("Computation", {"computation"}), ("Logic", {"logic"}),
        ("Source or data check", {"source-check", "data-audit", "prior-work"}), ("Human decision or other", {"human-decision", "other"})]
d0, d1 = (dt.date.fromisoformat(x) for x in (min(r["date"] for r in rows), max(r["date"] for r in rows)))
days = [d0 + dt.timedelta(i) for i in range((d1 - d0).days + 1)]


def counts(col, groups):
    m = np.zeros((len(groups), len(days)), int)
    for r in rows:
        g = next(i for i, (_, s) in enumerate(groups) if r[col] in s)
        m[g, (dt.date.fromisoformat(r["date"]) - d0).days] += 1
    return m


A, B = counts("changed_by", WHO), counts("evidence_type", KIND)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED})
fig, axes = plt.subplots(2, 1, figsize=(8.8, 5.4), sharex=True, constrained_layout=True)
x = np.arange(len(days))
for ax, m, groups, title in ((axes[0], A, WHO, "A  Who changed the judgment"), (axes[1], B, KIND, "B  What evidence changed it")):
    base = np.zeros(len(days))
    for i, (name, _) in enumerate(groups):
        ax.bar(x, m[i], 0.62, bottom=base, color=SLOTS[i], edgecolor="#ffffff", linewidth=1.0, label=f"{name} ({m[i].sum()})", zorder=3)
        base += m[i]
    for xi, tot in zip(x, base):
        if tot >= 15:
            ax.text(xi, tot + 0.8, str(int(tot)), ha="center", va="bottom", fontsize=8, color=MUTED)
    ax.set_title(title, loc="left", fontsize=10, color=INK, fontweight="bold")
    ax.set_ylabel("Decision changes")
    ax.grid(axis="y", color=GRID, linewidth=0.6, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_ylim(0, max(A.sum(0).max(), B.sum(0).max()) * 1.12)
    ax.legend(frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1.0), labelcolor=INK)
axes[1].set_xticks(x, [d.strftime("%-d") for d in days])
axes[1].set_xlabel(f"October 2026 (n = {len(rows)} ledger rows; WIP, not yet fully verified)")
for ext in ("png", "pdf"):
    fig.savefig(HERE / f"decision_changes_by_day.{ext}", dpi=200, facecolor="#ffffff")
with open(HERE / "decision_changes_by_day.tsv", "w") as fh:
    fh.write("panel\tgroup\t" + "\t".join(d.isoformat() for d in days) + "\ttotal\n")
    for panel, m, groups in (("A", A, WHO), ("B", B, KIND)):
        for (name, _), r in zip(groups, m):
            fh.write(f"{panel}\t{name}\t" + "\t".join(map(str, r)) + f"\t{r.sum()}\n")
print({n: int(r.sum()) for (n, _), r in zip(WHO, A)}, {n: int(r.sum()) for (n, _), r in zip(KIND, B)})
