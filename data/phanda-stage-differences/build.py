# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy==2.5.3", "pandas==3.0.6", "mat-io==1.0.0"]
# ///
"""Adjacent-stage GMST differences from PhanDA under stated dependence scenarios.

PhanDA assimilates each stage separately, so no joint temporal posterior exists
(see literature/2026-10-08-phanda-ensemble-contract.md). This script reports how
much a stage-to-stage difference depends on the assumed coupling. Run from the
repository root:  uv run data/phanda-stage-differences/build.py
"""

import hashlib
import urllib.request
from pathlib import Path

import matio
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "phanda" / "PhanDA_GMST_ensemble.mat"
URL = ("https://raw.githubusercontent.com/EJJudd/PhanDA/"
       "9f06c0d9764f3da77cb0819e0ac87c01182ba341/5_Outputs/PhanDA_GMST_ensemble.mat")
SHA256 = "6213e8164af32b7e67daee1acb603f6e8a186286041b54b0897c934fa51246ce"
OUT = ROOT / "data" / "derived" / "phanda-stage-differences"
EVENT_STAGES = {"Hirnantian", "Frasnian", "Famennian", "Capitanian/Wordian", "Changhsingian",
                "Rhaetian", "Toarcian", "Cenomanian", "Turonian", "Maastrichtian", "PETM"}
N_SCENARIOS = 12
BLOCK = 1_440
N_PER_SCENARIO = 10_000
GRID = 20_000
SEED = 20261009


def load():
    if not RAW.exists():
        RAW.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": "EPRP-orientation/0.1"}), timeout=120) as r:
            RAW.write_bytes(r.read())
    digest = hashlib.sha256(RAW.read_bytes()).hexdigest()
    if digest != SHA256:
        raise SystemExit(f"checksum mismatch: {digest}")
    g = matio.load_from_mat(RAW)["GMST"]
    # ScenarioAll holds 12 scenario blocks of 1,440 (padded by resampling in combineruns.m);
    # merged slices concatenate two stages' vectors (combinestages.m), so block j is scenario j mod 12.
    # The per-scenario columns of merged rows do not reproduce ScenarioAll, so they are not used.
    samples = []
    for v in g.ScenarioAll:
        v = np.asarray(v, dtype=float).ravel()
        blocks = v.reshape(-1, BLOCK)
        samples.append([np.concatenate(blocks[s::N_SCENARIOS]) for s in range(N_SCENARIOS)])
    return g[["Stage", "UpperAge", "LowerAge"]].reset_index(drop=True), samples


# Scenario blocks within a slice have equal sizes (1,440 or 2 x 1,440), so uniform draws from the
# concatenation give equal scenario weights. An earlier version picked one older-stage scenario per
# 10,000-draw block (found by Codex, Correspondence 77/1183); see data/phanda-coupling-audit.


def pooled_quantiles(blocks, p):
    """Quantile function of the equal-weight-per-scenario mixture."""
    vals = np.concatenate(blocks)
    w = np.concatenate([np.full(b.size, 1.0 / (len(blocks) * b.size)) for b in blocks])
    order = np.argsort(vals)
    cdf = np.cumsum(w[order])
    return vals[order][np.searchsorted(cdf, p, side="left").clip(max=vals.size - 1)]


def summarise(d):
    q05, q50, q95 = np.quantile(d, [0.05, 0.5, 0.95])
    return dict(mean=d.mean(), sd=d.std(), q05=q05, q50=q50, q95=q95,
                sign_resolved=bool(q05 > 0 or q95 < 0))


def main():
    meta, samples = load()
    rng = np.random.default_rng(SEED)
    p = (np.arange(GRID) + 0.5) / GRID
    k = len(samples[0])
    rows = []
    for i in range(len(meta) - 1):
        young, old = samples[i], samples[i + 1]
        diffs = {
            "shared_label_independent": np.concatenate([
                rng.choice(young[s], N_PER_SCENARIO) - rng.choice(old[s], N_PER_SCENARIO) for s in range(k)]),
            "fully_independent": rng.choice(np.concatenate(young), k * N_PER_SCENARIO)
                                 - rng.choice(np.concatenate(old), k * N_PER_SCENARIO),
            "quantile_aligned": pooled_quantiles(young, p) - pooled_quantiles(old, p),
            "reverse_quantile": pooled_quantiles(young, p) - pooled_quantiles(old, p[::-1]),
        }
        for coupling, d in diffs.items():
            rows.append(dict(younger=meta.Stage[i], older=meta.Stage[i + 1],
                             boundary_ma=meta.LowerAge[i], coupling=coupling,
                             event_pair=bool({meta.Stage[i], meta.Stage[i + 1]} & EVENT_STAGES),
                             **summarise(d)))
    res = pd.DataFrame(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    res.to_csv(OUT / "stage_differences.tsv", sep="\t", index=False, float_format="%.4f")

    csv = pd.read_csv(ROOT / "data/raw/phanda/PhanDA_GMSTandCO2_percentiles.csv")
    med = np.array([pooled_quantiles(s, np.array([0.5]))[0] for s in samples])
    print(f"Check: equal-weight pooled median vs deposited GMST_50, max |diff| = {np.abs(med - csv.GMST_50.values).max():.3f} °C")

    wide = res.pivot_table(index=["younger", "older"], columns="coupling", values="sd", sort=False)
    ratio = wide.reverse_quantile / wide.quantile_aligned
    print(f"Adjacent pairs: {len(wide)}. SD of ΔGMST (°C), median over pairs:")
    print(wide.median().round(2).to_string())
    print(f"Reverse/aligned SD ratio: median {ratio.median():.1f}, range {ratio.min():.1f}–{ratio.max():.1f}")
    print("Pairs with sign resolved (90% interval excludes 0):")
    print(res.groupby("coupling").sign_resolved.sum().to_string())
    ev = res[res.event_pair & res.coupling.isin(["shared_label_independent", "quantile_aligned", "reverse_quantile"])]
    print("\nEvent-adjacent pairs (ΔGMST = younger − older, °C):")
    print(ev.pivot_table(index=["younger", "older"], columns="coupling",
                         values=["q05", "q50", "q95"], sort=False).round(1).to_string())


if __name__ == "__main__":
    main()
