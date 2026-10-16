# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["numpy==2.1.3", "pandas==2.2.3", "cmdstanpy==1.2.4"]
# ///
"""Q-012 tiny unconditional component check (Codex 76/1709).

Subcommands, run from the repository root (config defaults to config.json):
  uv run --python 3.12 data/q012-component-check/component.py fixtures
  uv run --python 3.12 data/q012-component-check/component.py first [config]
  uv run --python 3.12 data/q012-component-check/component.py batch [config]

`fixtures` checks the closed-form cumulative hazard against quadrature,
simulator invariants, Monte Carlo extinction survival, the birth-count
distribution, the offspring kernel, the lineage cap and the compute gate,
and the Stan log density
against an independent Python implementation (as differences between two
parameter points, so dropped constants cancel). `first` fits one tree and
records its cost; `batch` fits the remaining frozen seeds within the declared
compute limit. Settings and seeds are frozen in config.json.
"""

import json
import math
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CFG_PATH = HERE / (sys.argv[2] if len(sys.argv) > 2 else "config.json")
CFG = json.loads(CFG_PATH.read_text())
OUT = ROOT / "scratch/q012-component"
CMDSTAN = pathlib.Path.home() / ".cmdstan/cmdstan-2.38.0"


def simulate(seed, truth=CFG["truth"], origins=CFG["root_origins"], H=CFG["horizon"], cap=CFG["lineage_cap"]):
    """Forward simulation; returns lineage arrays ordered parents before daughters."""
    rng = np.random.default_rng(seed)
    mu0, k, lam0, kap, sig, rho = (truth[n] for n in ("mu0", "k", "lambda0", "kappa", "sigma", "rho"))
    L = []  # dicts: parent (0-based or -1), o, x
    for o in origins:
        L.append(dict(parent=-1, o=float(o), x=sig * rng.standard_normal()))
    i = 0
    capped = False
    while i < len(L):
        lin = L[i]
        z = math.exp(lin["x"] - 0.5 * sig ** 2)
        a_ext = (rng.exponential() / (z * mu0)) ** (1.0 / k)
        end = lin["o"] + a_ext
        lin["ext"] = int(end < H)
        lin["v"] = min(end, H)
        buds, capped = bud_times(rng, lam0 * z ** kap, lin["o"], lin["v"], room=cap - len(L))
        if capped:
            return L, True  # partial history: never summarised or fitted
        lin["m"] = len(buds)
        for b in buds:
            L.append(dict(parent=i, o=b, x=rho * lin["x"] + sig * math.sqrt(1 - rho ** 2) * rng.standard_normal()))
        i += 1
    return L, False


def bud_times(rng, rate, o, v, room=math.inf):
    """Homogeneous Poisson buds on (o, v); stops (capped) if a bud would exceed `room` new lineages.
    Draw order is unchanged from the original loop, so uncapped trees reproduce exactly."""
    t, buds = o, []
    while True:
        t += rng.exponential(1.0 / rate)
        if t >= v:
            return buds, False
        if len(buds) >= room:
            return buds, True
        buds.append(t)


def stan_data(L):
    return dict(N=len(L), parent=[l["parent"] + 1 for l in L], o=[l["o"] for l in L], v=[l["v"] for l in L],
                ext=[l["ext"] for l in L], m=[l["m"] for l in L])


def python_target(d, p):
    """Independent implementation of the Stan target (normal priors without constants)."""
    mu0, k, lam0 = math.exp(p["log_mu0"]), math.exp(p["log_k"]), math.exp(p["log_lambda0"])
    sig, rho, kap = p["sigma"], p["rho"], p["kappa"]
    eps = p["eps"]
    x = []
    for i in range(d["N"]):
        par = d["parent"][i]
        x.append(sig * eps[i] if par == 0 else rho * x[par - 1] + sig * math.sqrt(1 - rho ** 2) * eps[i])
    lp = (-0.5 * (p["log_mu0"] - math.log(0.08)) ** 2 - 0.5 * (p["log_k"] / 0.5) ** 2
          - 0.5 * (p["log_lambda0"] - math.log(0.09)) ** 2 - 0.5 * kap ** 2 - 0.5 * sig ** 2
          - 0.5 * sum(e * e for e in eps))
    for i in range(d["N"]):
        dd = d["v"][i] - d["o"][i]
        logz = x[i] - 0.5 * sig ** 2
        lp += -math.exp(logz) * mu0 * dd ** k
        if d["ext"][i]:
            lp += logz + p["log_mu0"] + p["log_k"] + (k - 1) * math.log(dd)
        lp += d["m"][i] * (p["log_lambda0"] + kap * logz) - lam0 * math.exp(kap * logz) * dd
    return lp


def model():
    import cmdstanpy
    cmdstanpy.set_cmdstan_path(str(CMDSTAN))
    OUT.mkdir(parents=True, exist_ok=True)
    src = OUT / "model.stan"
    if not src.exists() or src.read_text() != (HERE / "model.stan").read_text():
        src.write_text((HERE / "model.stan").read_text())
    return cmdstanpy.CmdStanModel(stan_file=str(src))


def fixtures():
    res = {}
    # 1. closed-form cumulative hazard against quadrature
    worst = 0.0
    for z in (0.3, 1.0, 2.5):
        for k in (0.7, 1.0, 1.3):
            for D in (0.5, 7.0, 25.0):
                a = np.geomspace(1e-12, D, 200001)
                h = z * 0.08 * k * a ** (k - 1)
                num = np.trapezoid(h, a)
                exact = z * 0.08 * D ** k
                worst = max(worst, abs(num - exact) / exact)
    res["cumhaz_max_rel_err"] = float(worst)
    assert worst < 1e-3, worst
    # 2. simulator invariants on the frozen seeds
    H = CFG["horizon"]
    for s in CFG["seeds"]:
        L, capped = simulate(s)
        for i, l in enumerate(L):
            assert 0 <= l["o"] < l["v"] <= H, (s, i)
            assert (l["v"] < H) == bool(l["ext"]) or (l["v"] == H and not l["ext"])
            if l["parent"] >= 0:
                p = L[l["parent"]]
                assert l["parent"] < i and p["o"] < l["o"] < p["v"], (s, i)
        if not capped:
            kids = np.bincount([l["parent"] for l in L if l["parent"] >= 0], minlength=len(L))
            assert all(kids[i] == l["m"] for i, l in enumerate(L)), s
    res["simulator_invariants"] = "pass (20 frozen seeds)"
    # 3. Monte Carlo extinction survival against the analytic value, one lineage, fixed z
    rng = np.random.default_rng(7)
    z, mu0, k, lam0, H1 = 1.7, 0.08, 1.3, 0.09, 10.0
    E = rng.exponential(size=200000)
    a = (E / (z * mu0)) ** (1 / k)
    surv = np.mean(a > H1)
    exact = math.exp(-z * mu0 * H1 ** k)
    se = math.sqrt(exact * (1 - exact) / len(a))
    res["mc_survival"] = dict(mc=round(float(surv), 5), exact=round(exact, 5), z_score=round(float((surv - exact) / se), 2))
    assert abs(surv - exact) < 4 * se
    # 3b. birth counts: Poisson(rate * D) by mean, dispersion and chi-square
    rng = np.random.default_rng(11)
    rate, D, n = 0.09 * 1.5 ** 0.5, 10.0, 40000
    counts = np.array([len(bud_times(rng, rate, 0.0, D)[0]) for _ in range(n)])
    lamD = rate * D
    kmax = 6
    obs = np.array([np.sum(counts == j) for j in range(kmax)] + [np.sum(counts >= kmax)])
    pmf = [math.exp(-lamD) * lamD ** j / math.factorial(j) for j in range(kmax)]
    exp_ = np.array(pmf + [1 - sum(pmf)]) * n
    chi2 = float(np.sum((obs - exp_) ** 2 / exp_))
    res["birth_counts"] = dict(mean=round(float(counts.mean()), 4), expected=round(lamD, 4),
                               dispersion=round(float(counts.var() / counts.mean()), 4),
                               chi2=round(chi2, 2), df=kmax, chi2_crit_0999=22.46)
    assert abs(counts.mean() - lamD) < 4 * math.sqrt(lamD / n) and chi2 < 22.46
    # 3c. offspring kernel: regression of daughter on parent log frailty over many trees
    xp, xd, xr = [], [], []
    for s in range(5001, 5401):
        Lk, cp = simulate(s)
        if cp:
            continue
        for l in Lk:
            if l["parent"] >= 0:
                xp.append(Lk[l["parent"]]["x"]); xd.append(l["x"])
            else:
                xr.append(l["x"])
    xp, xd, xr = map(np.array, (xp, xd, xr))
    slope = float(np.cov(xp, xd)[0, 1] / np.var(xp, ddof=1))
    resid_sd = float(np.std(xd - slope * xp - (xd.mean() - slope * xp.mean()), ddof=2))
    se_slope = resid_sd / (np.std(xp, ddof=1) * math.sqrt(len(xp)))
    t = CFG["truth"]
    res["offspring_kernel"] = dict(pairs=len(xp), slope=round(slope, 4), rho=t["rho"],
                                   resid_sd=round(resid_sd, 4), expected_resid_sd=round(t["sigma"] * math.sqrt(1 - t["rho"] ** 2), 4),
                                   root_sd=round(float(np.std(xr, ddof=1)), 4), roots=len(xr), sigma=t["sigma"])
    assert abs(slope - t["rho"]) < 4 * se_slope
    assert abs(resid_sd / (t["sigma"] * math.sqrt(1 - t["rho"] ** 2)) - 1) < 0.05
    assert abs(np.std(xr, ddof=1) / t["sigma"] - 1) < 4 / math.sqrt(2 * len(xr))
    # 3d. lineage cap returns a recorded non-fit, never a partial history
    Lc, cc = simulate(CFG["seeds"][0], cap=50)
    row_c = summarise(CFG["seeds"][0], Lc, cc)
    res["cap_fixture"] = dict(capped=cc, status=row_c["status"], lineages_at_cap=row_c["N_at_cap"])
    assert cc and row_c["status"] == "capped (not fitted)"
    # 3e. compute gate: a first fit over its limit blocks the batch
    lim = CFG["compute_limit"]["max_seconds_first_fit"]
    res["gate_fixture"] = dict(over_limit_blocks=not gate_ok([dict(status="fitted", seconds=lim + 1)]),
                               within_limit_passes=gate_ok([dict(status="fitted", seconds=lim - 1)]))
    assert res["gate_fixture"]["over_limit_blocks"] and res["gate_fixture"]["within_limit_passes"]
    # 4. Stan log density against Python, as differences between two points
    import cmdstanpy  # noqa: F401
    mdl = model()
    L, _ = simulate(CFG["seeds"][0])
    d = stan_data(L)
    pts = []
    for j, (lm, lk, ll, kp, sg, rh) in enumerate([(math.log(0.07), 0.1, math.log(0.1), 0.2, 0.7, 0.4),
                                                    (math.log(0.09), -0.2, math.log(0.08), -0.3, 1.1, 0.8)]):
        eps = list(np.random.default_rng(100 + j).standard_normal(d["N"]))
        pts.append(dict(log_mu0=lm, log_k=lk, log_lambda0=ll, kappa=kp, sigma=sg, rho=rh, eps=eps))
    stan_lp = [float(mdl.log_prob(p, data=d, jacobian=False, sig_figs=15)["lp__"].iloc[0]) for p in pts]
    py_lp = [python_target(d, p) for p in pts]
    diff_stan, diff_py = stan_lp[0] - stan_lp[1], py_lp[0] - py_lp[1]
    res["logdensity_difference"] = dict(stan=round(diff_stan, 10), python=round(float(diff_py), 10),
                                        abs_err=float(abs(diff_stan - diff_py)), N=d["N"])
    assert abs(diff_stan - diff_py) < 1e-8 * max(1.0, abs(diff_py)), res["logdensity_difference"]
    (HERE / "fixtures.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps(res, indent=1))


def summarise(seed, L, capped):
    """Complete-history summaries only for uncapped trees."""
    if capped:
        return dict(seed=seed, status="capped (not fitted)", capped=True, N_at_cap=len(L))
    return dict(seed=seed, status="simulated", capped=False, N=len(L), n_ext=sum(l["ext"] for l in L),
                n_buds=sum(l["m"] for l in L), n_censored=sum(1 - l["ext"] for l in L))


def gate_ok(rows):
    """The batch may run only if the first fit completed within its declared limit."""
    return bool(rows) and rows[0].get("status") == "fitted" and \
        float(rows[0].get("seconds", math.inf)) <= CFG["compute_limit"]["max_seconds_first_fit"]


def fit_one(mdl, seed, timeout):
    L, capped = simulate(seed)
    row = summarise(seed, L, capped)
    if capped:
        return row, 0.0
    s = CFG["sampler"]
    t0 = time.time()
    try:
        fit = mdl.sample(data=stan_data(L), chains=s["chains"], parallel_chains=CFG["compute_limit"]["parallel_chains"],
                         iter_warmup=s["iter_warmup"], iter_sampling=s["iter_sampling"], adapt_delta=s["adapt_delta"],
                         max_treedepth=s["max_treedepth"], seed=seed + s["seed_offset"], show_progress=False,
                         output_dir=str(OUT / CFG.get("run_label", "v1") / f"seed{seed}"), timeout=timeout)
    except TimeoutError:
        row.update(status="timeout", seconds=round(time.time() - t0, 1))
        return row, time.time() - t0
    except RuntimeError as err:
        row.update(status=f"failed: {str(err)[:80]}", seconds=round(time.time() - t0, 1))
        return row, time.time() - t0
    secs = time.time() - t0
    draws = fit.draws_pd()  # one row per saved draw, with sampler diagnostics
    mv = fit.method_variables()
    summ = fit.summary()
    rh = [c for c in summ.columns if c.lower().startswith("r_hat")][0]
    ess = [c for c in summ.columns if c.lower() in ("ess_bulk", "n_eff")][0]
    core = summ.loc[["sigma", "rho", "eta", "kappa", "log_k", "log_mu0", "log_lambda0"]]
    div = int(mv["divergent__"].sum())
    row.update(status="fitted", seconds=round(secs, 1), divergences=div,
               max_rhat_core=round(float(core[rh].max()), 3), min_ess_core=round(float(core[ess].min()), 0))
    # where the divergent draws sit in sigma (saved states, not trajectories)
    sig = draws["sigma"].to_numpy()
    flags = draws["divergent__"].to_numpy() > 0
    if flags.any():
        lo10, hi90 = np.quantile(sig, [0.1, 0.9])
        row.update(div_sigma_median=round(float(np.median(sig[flags])), 3),
                   nondiv_sigma_median=round(float(np.median(sig[~flags])), 3),
                   div_in_bottom_sigma_decile=int(np.sum(sig[flags] <= lo10)),
                   div_in_top_sigma_decile=int(np.sum(sig[flags] >= hi90)))
    truth = CFG["truth"]
    for v, tv in (("sigma", truth["sigma"]), ("rho", truth["rho"]), ("eta", truth["rho"] * truth["sigma"]),
                  ("kappa", truth["kappa"])):
        q = np.quantile(draws[v], [0.05, 0.5, 0.95])
        row.update({f"{v}_q05": round(q[0], 3), f"{v}_q50": round(q[1], 3), f"{v}_q95": round(q[2], 3),
                    f"{v}_truth_in_90": bool(q[0] <= tv <= q[2])})
    return row, secs


def write_rows(rows):
    import pandas as pd
    pd.DataFrame(rows).to_csv(HERE / CFG.get("results_file", "component_results.tsv"), sep="\t", index=False)


def first():
    t0 = time.time()
    mdl = model()
    compile_s = time.time() - t0
    lim = CFG["compute_limit"]
    row, secs = fit_one(mdl, CFG["seeds"][0], timeout=lim.get("per_fit_timeout", lim["max_seconds_first_fit"]))
    row["compile_seconds"] = round(compile_s, 1)
    write_rows([row])
    print(json.dumps(row, indent=1))
    if not gate_ok([row]):
        print("STOP: first fit did not complete within the declared limit; rescope before extending.")
        sys.exit(2)


def batch():
    import pandas as pd
    prev = pd.read_csv(HERE / CFG.get("results_file", "component_results.tsv"), sep="\t").to_dict("records")
    if not gate_ok(prev):
        print("STOP: the first-fit gate has not passed; the batch is not run.")
        sys.exit(2)
    mdl = model()
    rows = prev
    total = sum(float(r.get("seconds", 0) or 0) for r in prev)
    done = {r["seed"] for r in prev}
    lim = CFG["compute_limit"]
    for s in CFG["seeds"]:
        if s in done:
            continue
        remaining = lim["max_seconds_total"] - total
        timeout = min(lim.get("per_fit_timeout", remaining), remaining)
        if timeout <= 1:
            rows.append(dict(seed=s, status="not run (compute budget exhausted)"))
            continue
        row, secs = fit_one(mdl, s, timeout=timeout)
        total += secs
        rows.append(row)
        write_rows(rows)
        print(s, row.get("status"), row.get("seconds"), row.get("N"))
    write_rows(rows)
    print("total fit seconds", round(total, 1))


if __name__ == "__main__":
    {"fixtures": fixtures, "first": first, "batch": batch}[sys.argv[1]]()
