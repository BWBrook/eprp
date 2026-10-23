# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.1.3", "scipy==1.14.1", "cmdstanpy==1.2.4", "pandas==2.2.3"]
# ///
"""Checks for model_ctr.stan, the exact prior-preserving centring (Codex 76/2249), before any fit:
V1 Stan's sum_to_zero_vector with std_normal has covariance I - J/N (sampled); V2 the joint prior on likelihood
predictors equals the original's (exact, N = 8, 40, 87); V3 at a fixed state the likelihood (likelihood_only) and the
gradients of shared parameters agree between model.stan and model_ctr.stan. Writes ctr_checks.json.
    uv run --python 3.12 data/q038-probe/ctr_checks.py"""
import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402
from cmdstanpy import CmdStanModel, set_cmdstan_path  # noqa: E402

set_cmdstan_path(str(pathlib.Path.home() / ".cmdstan/cmdstan-2.38.0"))
out = {}
# V1
tiny = HERE / "pilot" / "_v1_stz.stan"
tiny.write_text("parameters { sum_to_zero_vector[8] z; } model { z ~ std_normal(); }\n")
fit = CmdStanModel(stan_file=str(tiny)).sample(chains=4, iter_warmup=1000, iter_sampling=10000, seed=38, show_progress=False)
Zs = fit.stan_variable("z")
P8 = np.eye(8) - 1 / 8
out["V1_max_abs_cov_minus_P"] = float(np.max(np.abs(np.cov(Zs.T) - P8)))
out["V1_mean_marginal_var"] = float(np.mean(np.var(Zs, axis=0)))
out["V1_expected_marginal_var"] = 1 - 1 / 8
out["V1_max_abs_row_sum"] = float(np.max(np.abs(Zs.sum(axis=1))))     # CSV output carries 6 significant figures
# V2: original iid effects plus intercept against centred deviations plus effective intercept, conditional on scales
v2 = 0.0
for N in (8, 40, 87):
    a2, s2 = 1.5 ** 2, 0.37 ** 2
    J = np.ones((N, N))
    orig = a2 * J + s2 * np.eye(N)
    ctr = (a2 + s2 / N) * J + s2 * (np.eye(N) - J / N)
    v2 = max(v2, float(np.max(np.abs(orig - ctr))))
out["V2_max_abs_cov_difference"] = v2
# V3: likelihood and shared-parameter gradients at a fixed truth state (checks.py C2's data and state)
D = core.load_design()
om = core.calibrate_omega(D)
rng = np.random.default_rng(7)
p = core.truth_params(rng, D, om)
gen = core.simulate(rng, D, p)
sub = gen[:400]
c2 = core.CLASSES
orig = dict(alpha1=[p["alpha"][c][1] for c in c2], s_alpha=[1.0, 1.0],
            z_alpha=[[p["alpha"][c][s] - p["alpha"][c][s - 1] for s in range(2, D["T"] + 1)] for c in c2],
            z_omega=[p["omega"][c] for c in c2], mu_omega=0.0, s_omega=1.0, beta_b=[p["beta_b"][c] for c in c2],
            beta_e=[p["beta_e"][c] for c in c2], z_delta=list(p["delta"]), tau=1.0, gam=[p["gamma"][c] for c in c2],
            z_fam=[list(p["f_fam"][c]) for c in c2], z_ord=[list(p["g_ord"][c]) for c in c2], s_fam=1.0, s_ord=1.0,
            gd0=[p["gd0"][c] for c in c2], gd=[p["gd"][c] for c in c2], z_b=[list(p["b_fam"][c]) for c in c2], s_b=1.0,
            z_nu=[list(p["nu"][c][1:]) for c in c2], s_nu=1.0)
ctr = dict(orig)
ctr["alpha1"] = [orig["alpha1"][i] + float(np.mean(orig["z_fam"][i])) + float(np.mean(orig["z_ord"][i])) for i in range(2)]
ctr["gd0"] = [orig["gd0"][i] + float(np.mean(orig["z_b"][i])) + float(np.mean(orig["z_nu"][i])) for i in range(2)]
for k in ("z_fam", "z_ord", "z_b", "z_nu"):
    ctr[k] = [list(np.array(v) - np.mean(v)) for v in orig[k]]
v3 = {}
for fold in (("full",), ("loeo", 45)):
    data = core.stan_data(sub, core.components(sub, fold, D), D, likelihood_only=1)
    m0 = CmdStanModel(stan_file=str(HERE / "model.stan"), cpp_options={"STAN_THREADS": True})
    m1 = CmdStanModel(stan_file=str(HERE / "model_ctr.stan"), cpp_options={"STAN_THREADS": True})
    a = m0.log_prob(params=orig, data=data, jacobian=False, sig_figs=18)
    b = m1.log_prob(params=ctr, data=data, jacobian=False, sig_figs=18)
    shared = [c for c in a.columns if c in b.columns and c != "lp__" and not any(       # gradient columns are g_<name>
        c.removeprefix("g_").startswith(x) for x in ("z_fam", "z_ord", "z_b", "z_nu", "s_fam", "s_ord", "s_b", "s_nu"))]
    v3[fold[0]] = dict(loglik_orig=float(a["lp__"].iloc[0]), loglik_ctr=float(b["lp__"].iloc[0]),
                       loglik_abs_diff=abs(float(a["lp__"].iloc[0]) - float(b["lp__"].iloc[0])),
                       shared_gradients=len(shared),
                       max_abs_shared_gradient_diff=float(np.max(np.abs(a[shared].values - b[shared].values))))
out["V3"] = v3
out["ok"] = bool(out["V1_max_abs_cov_minus_P"] < 0.03 and out["V1_max_abs_row_sum"] < 1e-6 and v2 < 1e-12
                 and all(x["loglik_abs_diff"] < 1e-8 * max(1, abs(x["loglik_orig"])) and x["max_abs_shared_gradient_diff"] < 1e-8
                         for x in v3.values()))
(HERE / "ctr_checks.json").write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps(out, indent=1))
