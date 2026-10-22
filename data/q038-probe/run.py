# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.1.3", "scipy==1.14.1", "cmdstanpy==1.2.4", "pandas==2.2.3"]
# ///
"""Q-038 five-dataset S2 pilot (contract v3 D; Codex 76/2195): runtime and convergence only, no recovery gate.
    uv run --python 3.12 data/q038-probe/run.py manifest            # calibrate omega, write manifest.json (before data)
    uv run --python 3.12 data/q038-probe/run.py generate            # datasets 38001-38005 and their truth draws
    uv run --python 3.12 data/q038-probe/run.py benchmark SEED      # short fit to forecast cost
    uv run --python 3.12 data/q038-probe/run.py fit SEED [THREADS]  # one full fit; results/fit_SEED.json
    uv run --python 3.12 data/q038-probe/run.py summarise"""
import hashlib
import json
import math
import os
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402

SEEDS = (38001, 38002, 38003, 38004, 38005)
FIT = dict(chains=4, warmup=1000, sampling=1000, adapt_delta=0.8, max_treedepth=10, rhat_max=1.01, ess_min=400)
OUT = HERE / "pilot"


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def manifest():
    D = core.load_design()
    om = core.calibrate_omega(D)
    m = dict(contract="data/q038-predictor-contract/contract.md v3 section D", scenario="S2", seeds=SEEDS,
             truth=core.TRUTH_S2, target_event_loss=core.TARGET_LOSS, omega_calibrated=om, omega_calibration_seed=38000,
             feature_transform=D["tf"], feature_convention=core.__doc__.strip(),
             families_per_class=core.N_FAM, families_per_order=core.FAM_PER_ORD, events=core.EVENTS, fit=FIT,
             inputs={p: sha(core.ROOT / p) for p in ("data/q038-predictor-contract/stages.tsv",
                                                     "data/q038-predictor-contract/exposure.tsv",
                                                     "data/q038-probe/deposit_constants.json",
                                                     "data/q038-probe/core.py", "data/q038-probe/model.stan")})
    (HERE / "manifest.json").write_text(json.dumps(m, indent=1, default=float) + "\n")
    print(json.dumps(dict(omega=om), indent=1))


def load_manifest():
    return json.loads((HERE / "manifest.json").read_text())


def generate():
    D, m = core.load_design(), load_manifest()
    OUT.mkdir(exist_ok=True)
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        p = core.truth_params(rng, D, m["omega_calibrated"])
        gen = core.simulate(rng, D, p)
        np.savez_compressed(OUT / f"data_{seed}.npz", counts=np.array([g["counts"] for g in gen]),
                            meta=np.array([[core.CLASSES.index(g["cls"]), g["fam"], g["ord"], g["entry"], g["f"], g["death"]] for g in gen]))
        truth = dict(seed=seed, delta=p["delta"], **{f"{k}_{c}": list(map(float, p[k][c])) for k in ("f_fam", "g_ord", "b_fam", "nu") for c in core.CLASSES},
                     n_genera=len(gen), n_by_class={c: sum(g["cls"] == c for g in gen) for c in core.CLASSES})
        (OUT / f"truth_{seed}.json").write_text(json.dumps(truth, default=float) + "\n")
        print(seed, truth["n_genera"], truth["n_by_class"])


def load_data(seed):
    z = np.load(OUT / f"data_{seed}.npz")
    return [dict(cls=core.CLASSES[int(r[0])], fam=int(r[1]), ord=int(r[2]), entry=int(r[3]), f=int(r[4]), death=int(r[5]), counts=c)
            for r, c in zip(z["meta"], z["counts"])]


def model(stan_file="model.stan"):
    from cmdstanpy import CmdStanModel, set_cmdstan_path
    set_cmdstan_path(str(pathlib.Path.home() / ".cmdstan/cmdstan-2.38.0"))
    return CmdStanModel(stan_file=str(HERE / stan_file), cpp_options={"STAN_THREADS": True})


DIAG = {"ad95": ("model.stan", 0.95), "stz95": ("model_stz.stan", 0.95)}     # pilot divergence diagnosis (README)


def fit(seed, threads=12, warmup=None, sampling=None, tag="fit", stan_file="model.stan", adapt_delta=None):
    D, m = core.load_design(), load_manifest()
    gen = load_data(seed)
    data = core.stan_data(gen, core.components(gen, ("full",), D), D)
    mdl = model(stan_file)
    t0 = time.time()
    f = mdl.sample(data=data, chains=FIT["chains"], parallel_chains=FIT["chains"], threads_per_chain=threads, seed=seed,
                   iter_warmup=warmup or FIT["warmup"], iter_sampling=sampling or FIT["sampling"],
                   adapt_delta=adapt_delta or FIT["adapt_delta"], max_treedepth=FIT["max_treedepth"], show_progress=False,
                   output_dir=str(OUT / f"{tag}_{seed}"))
    wall = time.time() - t0
    s = f.summary()
    mv = f.method_variables()
    div = int(np.sum(mv["divergent__"])); depth = int(np.sum(mv["treedepth__"] >= FIT["max_treedepth"]))
    rhat = float(s["R_hat"].max()); ess_b = float(s["ESS_bulk"].min()); ess_t = float(s["ESS_tail"].min())
    draws = f.stan_variables()
    be = draws["beta_e"]
    rec = dict(seed=seed, tag=tag, stan_file=stan_file, adapt_delta=adapt_delta or FIT["adapt_delta"], wall_seconds=wall, components=data["N"], rows=data["R"], threads_per_chain=threads,
               warmup=warmup or FIT["warmup"], sampling=sampling or FIT["sampling"], divergences=div, treedepth_hits=depth,
               rhat_max=rhat, ess_bulk_min=ess_b, ess_tail_min=ess_t,
               success=bool(div == 0 and rhat <= FIT["rhat_max"] and ess_b >= FIT["ess_min"] and ess_t >= FIT["ess_min"]),
               beta_e={c: dict(mean=float(be[:, i].mean()), sd=float(be[:, i].std()), q025=float(np.quantile(be[:, i], .025)),
                               q975=float(np.quantile(be[:, i], .975)), truth=core.TRUTH_S2["beta_e"],
                               contraction_vs_prior_sd1=float(be[:, i].std()) / 1.0)
                       for i, c in enumerate(core.CLASSES)},
               tau=dict(mean=float(draws["tau"].mean()), q975=float(np.quantile(draws["tau"], .975)), truth=core.TRUTH_S2["tau"]),
               worst_rhat=s["R_hat"].sort_values(ascending=False).head(5).to_dict(),
               grad_seconds_hint=None)
    (OUT / f"{tag}_{seed}.json").write_text(json.dumps(rec, indent=1, default=float) + "\n")
    print(json.dumps({k: v for k, v in rec.items() if k != "worst_rhat"}, indent=1, default=float))
    return rec


def summarise():
    """Every attempted seed is accounted for: a seed without a result file is reported as such (Codex 76/2215)."""
    att = {s: json.loads((OUT / f"fit_{s}.json").read_text()) if (OUT / f"fit_{s}.json").exists() else None for s in SEEDS}
    rows = [r for r in att.values() if r]
    out = dict(attempted=len(SEEDS), completed=len(rows), no_result=[s for s, r in att.items() if r is None],
               successes=sum(r["success"] for r in rows), failed_screen=[r["seed"] for r in rows if not r["success"]],
               wall_seconds=[r["wall_seconds"] for r in rows],
               allocated_core_hours=[r["wall_seconds"] * FIT["chains"] * r["threads_per_chain"] / 3600 for r in rows],
               divergences=[r["divergences"] for r in rows], treedepth_hits=[r["treedepth_hits"] for r in rows],
               rhat_max=[r["rhat_max"] for r in rows], ess_bulk_min=[r["ess_bulk_min"] for r in rows],
               ess_tail_min=[r["ess_tail_min"] for r in rows],
               beta_e={c: [(r["beta_e"][c]["mean"], r["beta_e"][c]["sd"]) for r in rows] for c in core.CLASSES},
               note="Runtime/convergence pilot only; five datasets cannot pass any recovery gate (contract v3 D).")
    (OUT / "summary.json").write_text(json.dumps(out, indent=1, default=float) + "\n")
    print(json.dumps(out, indent=1, default=float))


if __name__ == "__main__":
    a = sys.argv[1:]
    cmd = a[0]
    if cmd == "manifest":
        manifest()
    elif cmd == "generate":
        generate()
    elif cmd == "benchmark":
        fit(int(a[1]), int(a[2]) if len(a) > 2 else 12, warmup=100, sampling=100, tag="bench")
    elif cmd == "fit":
        fit(int(a[1]), int(a[2]) if len(a) > 2 else 12)
    elif cmd == "diag":
        fit(int(a[1]), int(a[3]), tag=f"diag_{a[2]}", stan_file=DIAG[a[2]][0], adapt_delta=DIAG[a[2]][1])
    elif cmd == "summarise":
        summarise()
