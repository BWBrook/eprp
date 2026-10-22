# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.1.3", "scipy==1.14.1", "cmdstanpy==1.2.4", "pandas==2.2.3"]
# ///
"""Implementation checks for the Q-038 primary probe (Codex 76/2195), against the actual code paths in core.py and
model.stan. Writes checks.json.  uv run --python 3.12 data/q038-probe/checks.py"""
import copy
import itertools
import json
import math
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import core  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
D = core.load_design()
out = {}


def tiny_design(T, E):
    d = dict(D)
    d["T"] = T
    d["E"] = np.array([0] + list(E), dtype=int)
    return d


def tiny_params(T, seed=1):
    rng = np.random.default_rng(seed)
    om = {c: list(rng.normal(1.0, 0.5, 5)) for c in core.CLASSES}
    p = core.truth_params(rng, D, om)
    for c in core.CLASSES:
        p["alpha"][c] = rng.normal(-1.5, 0.4, T + 1)
        p["gd0"][c] = math.log(0.6)                    # tiny exposure: a larger per-reference rate
    return p


# ---- C1: total probability of the count-history likelihood (counts > 1, zeros after capture, event transition) ---------
T1, E1 = 8, (2, 1, 2, 2, 1, 2, 2, 1)                   # stage 7 -> 8 is an event transition (EVENTS contains 7)
Dt, pt = tiny_design(T1, E1), tiny_params(T1)
tot = {}
for cf in (1, 2):
    for C in (5, 8):
        s = 0.0
        for fut in itertools.product(*[range(E1[t - 1] + 1) for t in range(2, C + 1)]):
            cnt = np.zeros(T1 + 1, dtype=int); cnt[1] = cf; cnt[2:C + 1] = fut
            s += math.exp(core.component_loglik(cnt, 1, C, "Rhynchonellata", 3, 0, pt, Dt))
        tot[f"first_count_{cf}_C{C}"] = s
out["C1_total_probability"] = tot
out["C1_ok"] = all(abs(v - 1) < 1e-12 for v in tot.values())

# ---- C3: forecast q against an independent likelihood-ratio enumeration -----------------------------------------------
k, M = 7, 1
cnt = np.zeros(T1 + 1, dtype=int); cnt[1], cnt[3], cnt[4] = 2, 1, 2          # prefix up to k-1 = 6, last record at 4
h = core.history_from_counts(cnt, 1, k - 1)
q_fore = core.predict_q(h, k, M, "Rhynchonellata", 3, 0, pt, Dt, exact=True)
base = core.component_loglik(cnt, 1, k - 1, "Rhynchonellata", 3, 0, pt, Dt)
q_ratio = 0.0
for yk in range(E1[k - 1] + 1):
    c2 = cnt.copy(); c2[k] = yk; c2[k + 1:k + M + 1] = 0
    q_ratio += math.exp(core.component_loglik(c2, 1, k + M, "Rhynchonellata", 3, 0, pt, Dt) - base)
q_mc = core.predict_q(h, k, M, "Rhynchonellata", 3, 0, pt, Dt, n=200000, rng=np.random.default_rng(38))
se = math.sqrt(q_mc * (1 - q_mc) / 200000)
out["C3"] = dict(q_forecast_exact=q_fore, q_likelihood_ratio=q_ratio, abs_diff=abs(q_fore - q_ratio), q_mc=q_mc, mc_z=abs(q_mc - q_fore) / se)
out["C3_ok"] = abs(q_fore - q_ratio) < 1e-12 and abs(q_mc - q_fore) / se < 4

# ---- C4: fold builder invariance and masked old tails (real design, simulated data) -------------------------------------
om = core.calibrate_omega(D)
rng = np.random.default_rng(7)
p = core.truth_params(rng, D, om)
gen = core.simulate(rng, D, p)
res4 = {}
for kk in core.EVENTS:
    for fold in (("forward", kk), ("loeo", kk)):
        comps = core.components(gen, fold, D)
        d0 = core.stan_data(gen, comps, D)
        g2 = copy.deepcopy(gen)
        rr = np.random.default_rng(kk)
        held = {gi for gi, f, C in comps if C == kk - 1}
        for gi, g in enumerate(g2):
            if fold[0] == "forward" or gi in held:
                g["counts"][kk:] = rr.integers(0, 3, len(g["counts"]) - kk)
                if fold[0] == "loeo":
                    g["counts"][kk:] = rr.integers(0, 3, len(g["counts"]) - kk)
        d1 = core.stan_data(g2, core.components(g2, fold, D), D)
        same = all(np.array_equal(np.asarray(d0[x]), np.asarray(d1[x])) for x in d0)
        res4[f"{fold[0]}_{kk}_future_replacement_identical"] = bool(same)
    # LOEO likelihood is invariant to the held-out event's parameters, including unseen tails of old genera
    comps = core.components(gen, ("loeo", kk), D)
    ki = core.EVENTS.index(kk)
    def total(pp):
        return sum(core.component_loglik(gen[gi]["counts"], f, C, gen[gi]["cls"], gen[gi]["fam"], gen[gi]["ord"], pp, D)
                   for gi, f, C in comps)
    pa, pb = copy.deepcopy(p), copy.deepcopy(p)
    for c in core.CLASSES:
        pb["omega"][c][ki] += 3.0
    pb["delta"][ki] += 2.0
    res4[f"loeo_{kk}_loglik_change_under_event_parameters"] = abs(total(pa) - total(pb))
    old = [gi for gi, f, C in comps if C == kk and not any(gen[gi]["counts"][kk + 1:] > 0)
           and max(t for t in range(f, kk + 1) if gen[gi]["counts"][t] > 0) < kk - 3]
    res4[f"loeo_{kk}_old_unseen_tails_censored_at_k"] = len(old)
out["C4"] = res4
out["C4_ok"] = all(v for x, v in res4.items() if x.endswith("identical")) and \
    all(v < 1e-9 for x, v in res4.items() if x.endswith("event_parameters"))

# ---- C5: generator against likelihood (tiny design, first record at stage 1) ------------------------------------------
T5, E5 = 5, (2, 1, 2, 1, 2)
D5 = tiny_design(T5, E5)
D5["entries"] = {"Rhynchonellata": np.array([0, 400000, 0, 0, 0, 0]), "Bivalvia": np.zeros(T5 + 1, dtype=int)}
p5 = tiny_params(T5, seed=5)
g5 = core.simulate(np.random.default_rng(55), D5, p5)
g5 = [g for g in g5 if g["f"] == 1]
from collections import Counter
freq = {}
for fam in range(core.N_FAM):
    sub = [tuple(g["counts"][1:]) for g in g5 if g["fam"] == fam]
    freq[fam] = (len(sub), Counter(sub))
worst = 0.0
for fam in (0, 17, 33):
    n, cn = freq[fam]
    for hist, m in cn.most_common(6):
        cnt = np.array((0,) + hist)
        pr = math.exp(core.component_loglik(cnt, 1, T5, "Rhynchonellata", fam, fam // core.FAM_PER_ORD, p5, D5))
        pr_first = sum(math.exp(core.component_loglik(np.array((0,) + (hist[0],) + rest), 1, T5, "Rhynchonellata", fam,
                                                      fam // core.FAM_PER_ORD, p5, D5))
                       for rest in [hist[1:]])
        # conditional on the first count: compare with the empirical frequency among genera with the same first count
        nf = sum(v for h_, v in cn.items() if h_[0] == hist[0])
        z = abs(m / nf - pr) / math.sqrt(pr * (1 - pr) / nf)
        worst = max(worst, z)
out["C5_max_z_generator_vs_likelihood"] = worst
out["C5_ok"] = worst < 4.5

# ---- C6: LOEO restarts condition on capture but keep the observed history (Codex 76/2213) -----------------------------
res6 = {}
# (a) Codex's counterexample: records (1,2), (8,1), (9,2); k = 7; his independent alive/dead recursion gave -8.9884258733
Dc = dict(D); Dc["T"] = 10; Dc["E"] = np.array([0] + [2] * 10)
pc = core.truth_params(np.random.default_rng(913), D, json.loads((HERE / "manifest.json").read_text())["omega_calibrated"])
cc = np.zeros(11, dtype=int); cc[1], cc[8], cc[9] = 2, 1, 2
gc = [dict(cls="Rhynchonellata", fam=3, ord=0, f=1, counts=cc)]
res6["counterexample_components"] = core.components(gc, ("loeo", 7), Dc)
suf = core.component_loglik(cc, 8, 10, "Rhynchonellata", 3, 0, pc, Dc)
res6["counterexample_suffix"] = suf
res6["counterexample_vs_codex_recursion"] = abs(suf - (-8.9884258733))
pcx = copy.deepcopy(pc)
for c in core.CLASSES:
    pcx["omega"][c][0] += 10
pcx["delta"][0] += 10
res6["counterexample_change_under_event7_parameters"] = abs(
    sum(core.component_loglik(cc, f, C, "Rhynchonellata", 3, 0, pcx, Dc) for _, f, C in res6["counterexample_components"])
    - sum(core.component_loglik(cc, f, C, "Rhynchonellata", 3, 0, pc, Dc) for _, f, C in res6["counterexample_components"]))
# (b) total probability of a restarted suffix with a fixed earlier history (tiny C1 design; restart at 3, censored at 8)
for cf in (1, 2):
    s = 0.0
    for fut in itertools.product(*[range(E1[t - 1] + 1) for t in range(4, 9)]):
        cnt = np.zeros(T1 + 1, dtype=int); cnt[1], cnt[3] = 2, cf; cnt[4:9] = fut
        s += math.exp(core.component_loglik(cnt, 3, 8, "Rhynchonellata", 3, 0, pt, Dt))
    res6[f"restart_total_probability_count_{cf}"] = s
# (c) every LOEO restart on the real design (C4's simulated data): suffix = full - prefix-to-capture, and its Stan rows
# equal the full-fold rows for the same transitions
full = core.stan_data(gen, core.components(gen, ("full",), D), D)
row0 = {gi: full["c_tr0"][i] - 1 for i, (gi, f, C) in enumerate(core.components(gen, ("full",), D))}
worst_id, worst_row, n_restart = 0.0, 0.0, 0
for kk in core.EVENTS:
    comps = core.components(gen, ("loeo", kk), D)
    dk = core.stan_data(gen, comps, D)
    for i, (gi, f, C) in enumerate(comps):
        g = gen[gi]
        if f == g["f"]:
            continue
        n_restart += 1
        ll = lambda a, b: core.component_loglik(g["counts"], a, b, g["cls"], g["fam"], g["ord"], p, D)
        worst_id = max(worst_id, abs(ll(f, C) - (ll(g["f"], C) - ll(g["f"], f))))
        a, b = dk["c_tr0"][i] - 1, row0[gi] + (f - g["f"])
        for j in range(C - f):
            worst_row = max(worst_row, max(abs(u - v) for u, v in zip(dk["tr_feat"][a + j], full["tr_feat"][b + j])),
                            abs(dk["em_w"][a + j] - full["em_w"][b + j]))
res6.update(real_design_restarts=n_restart, max_suffix_identity_error=worst_id, max_restart_row_vs_full_row=worst_row)
out["C6"] = res6
out["C6_ok"] = (res6["counterexample_components"] == [(0, 1, 7), (0, 8, 10)] and res6["counterexample_vs_codex_recursion"] < 1e-9
                and res6["counterexample_change_under_event7_parameters"] < 1e-12
                and all(abs(res6[f"restart_total_probability_count_{cf}"] - 1) < 1e-12 for cf in (1, 2))
                and n_restart > 0 and worst_id < 1e-9 and worst_row == 0.0)

# ---- C7: scenario generators S0, S1, S3, S4 (redesign support; nothing is fitted) ---------------------------------------
res7 = {}
man = json.loads((HERE / "manifest.json").read_text())
same = True
for seed in man["seeds"]:                                   # (a) the S2 path is unchanged: pilot datasets regenerate exactly
    rng = np.random.default_rng(seed)
    pp = core.truth_params(rng, D, man["omega_calibrated"])
    g2 = core.simulate(rng, D, pp)
    z = np.load(HERE / f"pilot/data_{seed}.npz")
    same &= np.array_equal(np.array([g["counts"] for g in g2]), z["counts"]) and np.array_equal(
        np.array([[core.CLASSES.index(g["cls"]), g["fam"], g["ord"], g["entry"], g["f"], g["death"]] for g in g2]), z["meta"])
res7["S2_pilot_datasets_regenerated_identically"] = bool(same)
for sc_ in ("S0", "S1"):                                    # (b) calibration hits the deposit event losses on a fresh seed
    om_s = core.calibrate_omega(D, scenario=sc_)
    p_s = core.truth_params(np.random.default_rng(39000), D, om_s, sc_, draw=False)
    _, mem = core.simulate(np.random.default_rng(39001), D, p_s, record_members=True)
    err, spread = 0.0, 0.0
    for c in core.CLASSES:
        for i, k in enumerate(core.EVENTS):
            et = np.array(mem[(c, k)])
            err = max(err, abs(float(np.mean(1 / (1 + np.exp(-(et + om_s[c][i]))))) - core.TARGET_LOSS[c][i]))
            spread = max(spread, float(np.ptp(et)))
    res7[f"{sc_}_max_event_loss_error_fresh_seed"] = err
    res7[f"{sc_}_max_event_eta_spread"] = spread          # S0: eta = alpha + omega at events, so zero spread
T8 = 9                                                      # (c) S3: post-event mean count = round(E x (1 - L)) x p
D8 = tiny_design(T8, (40,) * T8)
D8["entries"] = {"Rhynchonellata": np.array([0, 60000] + [0] * (T8 - 1)), "Bivalvia": np.zeros(T8 + 1, dtype=int)}
p8 = core.truth_params(np.random.default_rng(1), D, {c: [0.0] * 5 for c in core.CLASSES}, "S0", draw=False)
for c in core.CLASSES:
    p8["alpha"][c] = np.full(T8 + 1, -3.0); p8["gd"][c] = 0.0; p8["gd0"][c] = math.log(0.02)
pr = -math.expm1(-0.02)
for obs, n_eff in ((None, 40), ("S3", int(round(40 * (1 - core.TARGET_LOSS["Rhynchonellata"][0]))))):
    g8 = core.simulate(np.random.default_rng(88), D8, p8, obs=obs)
    y8 = np.array([g["counts"][8] for g in g8 if g["f"] < 8 and g["death"] >= 8])
    res7[f"{obs or 'fitted'}_stage8_mean_count"] = float(y8.mean())
    res7[f"{obs or 'fitted'}_stage8_expected"] = n_eff * pr
    res7[f"{obs or 'fitted'}_stage8_z"] = abs(float(y8.mean()) - n_eff * pr) / (float(y8.std()) / math.sqrt(len(y8)))
T7, E7 = 3, (40, 40, 40)                                    # (d) S4: stage-2 mean count = sum_r 1 - exp(-theta e^zeta_r)
D7 = tiny_design(T7, E7)
D7["entries"] = {"Rhynchonellata": np.array([0, 60000, 0, 0]), "Bivalvia": np.zeros(T7 + 1, dtype=int)}
p7 = core.truth_params(np.random.default_rng(1), D, {c: [0.0] * 5 for c in core.CLASSES}, "S0", draw=False)
for c in core.CLASSES:
    p7["alpha"][c] = np.full(T7 + 1, -3.0); p7["gd"][c] = 0.0; p7["gd0"][c] = math.log(0.02)
g7 = core.simulate(np.random.default_rng(77), D7, p7, obs="S4")
zr = np.random.default_rng(77)
zeta7 = {t: zr.normal(0, core.S4_SD, E7[t - 1]) for t in range(1, T7 + 1)}
y2 = np.array([g["counts"][2] for g in g7 if g["f"] == 1 and g["death"] >= 2])
mu2 = float(np.sum(-np.expm1(-0.02 * np.exp(zeta7[2]))))
res7["S4_stage2_mean_count"] = float(y2.mean())
res7["S4_stage2_expected"] = mu2
res7["S4_stage2_binomial_without_zeta"] = 40 * float(-math.expm1(-0.02))
res7["S4_stage2_z"] = abs(float(y2.mean()) - mu2) / (float(y2.std()) / math.sqrt(len(y2)))
out["C7"] = res7
out["C7_ok"] = (res7["S2_pilot_datasets_regenerated_identically"] and res7["S0_max_event_eta_spread"] == 0.0
                and res7["S0_max_event_loss_error_fresh_seed"] < 0.02 and res7["S1_max_event_loss_error_fresh_seed"] < 0.03
                and res7["S3_stage8_z"] < 4 and res7["fitted_stage8_z"] < 4
                and res7["S4_stage2_z"] < 4)

# ---- C2: Stan likelihood equals the Python reference (likelihood_only, jacobian=False) ---------------------------------
from cmdstanpy import CmdStanModel, set_cmdstan_path  # noqa: E402
set_cmdstan_path(str(pathlib.Path.home() / ".cmdstan/cmdstan-2.38.0"))
model = CmdStanModel(stan_file=str(HERE / "model.stan"), cpp_options={"STAN_THREADS": True})
sub = gen[:400]
res2 = {}
for fold in (("full",), ("forward", 38), ("loeo", 45)):
    comps = core.components(sub, fold, D)
    data = core.stan_data(sub, comps, D, likelihood_only=1)
    py = sum(core.component_loglik(sub[gi]["counts"], f, C, sub[gi]["cls"], sub[gi]["fam"], sub[gi]["ord"], p, D) for gi, f, C in comps)
    c2 = core.CLASSES
    par = dict(alpha1=[p["alpha"][c][1] for c in c2], s_alpha=[1.0, 1.0],
               z_alpha=[[p["alpha"][c][s] - p["alpha"][c][s - 1] for s in range(2, D["T"] + 1)] for c in c2],
               z_omega=[p["omega"][c] for c in c2], mu_omega=0.0, s_omega=1.0, beta_b=[p["beta_b"][c] for c in c2],
               beta_e=[p["beta_e"][c] for c in c2], z_delta=list(p["delta"]), tau=1.0, gam=[p["gamma"][c] for c in c2],
               z_fam=[list(p["f_fam"][c]) for c in c2], z_ord=[list(p["g_ord"][c]) for c in c2], s_fam=1.0, s_ord=1.0,
               gd0=[p["gd0"][c] for c in c2], gd=[p["gd"][c] for c in c2], z_b=[list(p["b_fam"][c]) for c in c2], s_b=1.0,
               z_nu=[list(p["nu"][c][1:]) for c in c2], s_nu=1.0)
    lp = model.log_prob(params=par, data=data, jacobian=False, sig_figs=18)
    stan = float(lp.iloc[0, 0])
    res2[fold[0] + (f"_{fold[1]}" if len(fold) > 1 else "")] = dict(python=py, stan=stan, abs_diff=abs(py - stan), components=len(comps))
out["C2"] = res2
out["C2_ok"] = all(v["abs_diff"] < 1e-8 * max(1, abs(v["python"])) for v in res2.values())

out["all_ok"] = all(v for x, v in out.items() if x.endswith("_ok"))
(HERE / "checks.json").write_text(json.dumps(out, indent=1, default=float) + "\n")
print(json.dumps(out, indent=1, default=float))
