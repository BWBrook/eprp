"""Q-012 data-matched raw exposure-observation process (finite contract §8.2).

Fits, from the recorded raw observation pattern only (no relatives' outcomes):
- pi_L: share of lineages with any Triton coverage;
- within covered lineages after 66 Ma, a two-state Markov chain: first-bin
  observation probability, and P(observed | previous observed or missing).
Then simulates the process (seeded) over the actual lineage-bins, applying the
past-only lag rule (nearest observed older bin within 2), and compares derived
raw and lagged availability with the recorded values. Also reports the
simpler iid processes that miss. Standard library only.

Run from the repository root:  python3 -I data/q012-exposure-support/observation_process.py
"""

import collections
import csv
import json
import pathlib
import random

HERE = pathlib.Path(__file__).resolve().parent


def main():
    rows = list(csv.DictReader((HERE / "lineage_bin_E.tsv").open(), delimiter="\t"))
    cov = {r["lineage"]: int(r["n_occurrences"]) > 0
           for r in csv.DictReader((HERE / "lineage_coverage.tsv").open(), delimiter="\t")}
    seq = collections.defaultdict(list)
    for r in rows:
        seq[r["lineage"]].append((int(r["bin"]), r["observed_mean_abs_pal_lat"] not in ("NA", "")))
    bins = {l: sorted((b for b, _ in s), reverse=True) for l, s in seq.items()}  # oldest first

    first, tr = [0, 0], collections.Counter()
    for l, s in seq.items():
        obs = [o for b, o in sorted(s, key=lambda x: -x[0]) if b < 66]
        if not cov[l] or not obs:
            continue
        first[obs[0]] += 1
        for a, b in zip(obs, obs[1:]):
            tr[(a, b)] += 1
    pi_l = sum(cov.values()) / len(cov)
    p_first = first[1] / sum(first)
    p11 = tr[(1, 1)] / (tr[(1, 1)] + tr[(1, 0)])
    p01 = tr[(0, 1)] / (tr[(0, 1)] + tr[(0, 0)])

    def lagged(obs, i):
        return any(obs[max(0, i - 2):i])

    rng = random.Random(20261016)
    raw = lag = n = 0
    for _ in range(200):
        for l, bs in bins.items():
            has, prev, obs = rng.random() < pi_l, None, []
            for b in bs:
                if b >= 66 or not has:
                    o = False
                elif prev is None:
                    o = rng.random() < p_first
                else:
                    o = rng.random() < (p11 if prev else p01)
                if b < 66 and has:
                    prev = o
                obs.append(o)
            for i in range(len(bs)):
                n += 1
                raw += obs[i]
                lag += lagged(obs, i)

    def iid_lagged(p, mask):
        tot = cnt = 0
        for bs in bins.values():
            for i in range(len(bs)):
                older = [o for o in bs[max(0, i - 2):i] if not (mask and o >= 66)]
                tot += 1 - (1 - p) ** len(older)
                cnt += 1
        return tot / cnt

    recorded_raw = sum(o for s in seq.values() for _, o in s) / len(rows)
    recorded_lag = sum(1 for r in rows if r["used_value"] not in ("NA", "")) / len(rows)
    out = dict(
        fitted=dict(pi_L=round(pi_l, 4), p_first=round(p_first, 4), p_obs_given_obs=round(p11, 4),
                    p_obs_given_missing=round(p01, 4), pre_66_Ma="unobserved"),
        derived_markov=dict(raw=round(raw / n, 4), lagged=round(lag / n, 4), replicates=200, seed=20261016),
        recorded=dict(raw=round(recorded_raw, 4), lagged=round(recorded_lag, 4)),
        simpler_processes_lagged=dict(iid_p0667_no_mask=round(iid_lagged(0.667, False), 4),
                                      iid_p0667_mask=round(iid_lagged(0.667, True), 4)),
    )
    (HERE / "observation_process.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
