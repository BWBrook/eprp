# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.1.3", "pandas==2.2.3", "cmdstanpy==1.2.4", "arviz==0.20.0", "matplotlib==3.9.2",
#                 "xarray==2024.9.0", "scipy==1.14.1"]
# ///
"""Q-012 bounded kunanyi pilot (Codex 76/1750): package, control tests and screening.

  uv run --python 3.12 data/q012-pilot/pilot.py build                 # hash-bound payload from the frozen seed table
  uv run --python 3.12 data/q012-pilot/pilot.py selftest              # cap, timeout, chain-failure, resume, signal and stale-hash fixtures
  uv run --python 3.12 data/q012-pilot/pilot.py diagnose DIR SCEN     # screening of one fitted attempt directory

The cluster runs only CmdStan and bash (payload/pbs/); data generation and screening run locally.
"""
import hashlib
import importlib.util
import json
import pathlib
import queue
import shutil
import subprocess
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
PAY = HERE / "payload"
PILOT = json.loads((HERE / "pilot.json").read_text())
_spec = importlib.util.spec_from_file_location("prototype", HERE.parent / "q012-prototype" / "prototype.py")
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)
CACHE = P.OUT.parent / "q012-pilot"
RUN_ENV = dict(CHAINS=4, WARMUP=PILOT["sampler"]["iter_warmup"], SAMPLING=PILOT["sampler"]["iter_sampling"],
               ADAPT_DELTA=PILOT["sampler"]["adapt_delta"], MAX_DEPTH=PILOT["sampler"]["max_treedepth"],
               STEPSIZE=PILOT["sampler"]["init_step_size"], SEED=77017, FIT_SECONDS=PILOT["resources"]["fit_seconds"],
               SMOKE_SECONDS=PILOT["resources"]["smoke_seconds"], MODEL_BIN="./model_v4",
               MODULE="HDF5/1.14.0-gompi-2023a", CMDSTAN_VERSION="2.38.0")


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def scenarios():
    lines = (HERE / PILOT["scenarios_file"]).read_text().splitlines()
    head = lines[0].split("\t")
    return [dict(zip(head, ln.split("\t"))) for ln in lines[1:] if ln.strip()]


def _generate(q, seed, overrides):
    L, ginfo = P.generate(seed, overrides)
    if ginfo["capped"]:
        q.put(("capped", None, ginfo, None))
        return
    obsd, oinfo = P.observe(L, seed)
    q.put(("ok", P.adapt(obsd), ginfo, oinfo))


def generate(seed, overrides, timeout):
    """Generate, observe and adapt one dataset in a child process under a hard time limit.
    Returns (outcome, data, generator info, observation info); outcome is ok, capped, timeout or error."""
    import multiprocessing as mp
    ctx = mp.get_context("fork")
    q = ctx.Queue()
    proc = ctx.Process(target=_generate, args=(q, seed, overrides))
    t0 = time.time()
    proc.start()
    try:
        out = q.get(timeout=timeout)
    except queue.Empty:
        out = ("timeout" if proc.is_alive() else "error", None, None, None)
    proc.join(5)
    if proc.is_alive():
        proc.terminate()
        proc.join()
    return out + (round(time.time() - t0, 2),)


def write_starts(folder, N):
    from cmdstanpy.utils import write_stan_json
    rule = P.CFG[P.CFG["active"]]["inits"]
    folder.mkdir(parents=True, exist_ok=True)
    for k, q in enumerate(P.init_points(rule, rule["seed"], 4, N, rule["perturbation"]), start=1):
        write_stan_json(str(folder / f"chain{k}.json"), q)


def log_prob_csv(exe, params_file, data_file, out_file):
    r = subprocess.run([str(exe), "log_prob", "jacobian=1", f"constrained_params={params_file}", "data", f"file={data_file}",
                        "output", f"file={out_file}", "sig_figs=15"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-500:] + r.stderr[-500:]


def start_check(exe, scen):
    """Each frozen start through Stan's own initialisation (one draw, adaptation off, depth 1) on its dataset."""
    out = {}
    work = CACHE / "start_check"
    work.mkdir(parents=True, exist_ok=True)
    for k in range(1, 5):
        r = subprocess.run([str(exe), "sample", "num_samples=1", "num_warmup=0", "adapt", "engaged=0", "algorithm=hmc",
                            "engine=nuts", "max_depth=1", f"stepsize={RUN_ENV['STEPSIZE']}", f"init={PAY / 'inits' / scen / f'chain{k}.json'}",
                            "random", f"seed={RUN_ENV['SEED']}", "data", f"file={PAY / 'data' / f'{scen}.json'}",
                            "output", f"file={work / f'{scen}_{k}.csv'}", "refresh=0"], capture_output=True, text=True, timeout=120)
        txt = r.stdout + r.stderr
        out[f"chain{k}"] = ("unrecoverable" if "Unrecoverable" in txt else "rejected" if "Rejecting initial value" in txt
                            else "initialised" if r.returncode == 0 else f"exit_{r.returncode}")
    return out


def write_manifest(root):
    files = sorted(f for f in root.rglob("*") if f.is_file() and f.name not in ("manifest.sha256", "manifest.json")
                   and not f.relative_to(root).parts[0] in ("runs", "build")
                   and not f.name.endswith((".tar.gz", ".hpp", ".o", ".d")) and f.name != RUN_ENV["MODEL_BIN"][2:])
    (root / "manifest.sha256").write_text("".join(f"{sha(f)}  {f.relative_to(root)}\n" for f in files))
    return len(files)


def cmdstan_tarball():
    """The CmdStan release tarball, downloaded once into scratch; never committed."""
    CACHE.mkdir(parents=True, exist_ok=True)
    tb = CACHE / f"cmdstan-{RUN_ENV['CMDSTAN_VERSION']}.tar.gz"
    if not tb.exists():
        subprocess.run(["curl", "-fsSL", "-o", str(tb), PILOT["runtime"]["cmdstan_url"]], check=True)
    return tb


def build():
    """Build the payload: refuse unless the prototype's checks pass and are bound to the current source and settings."""
    from cmdstanpy.utils import write_stan_json
    ver = P.CFG["active"]
    assert ver == PILOT["candidate"]["prototype_version"], f"prototype active version is {ver}"
    chk = json.loads((HERE / PILOT["candidate"]["checks_file"]).read_text())
    d_fit, _, _ = P.dataset(P.CFG["fit_seed"])
    assert chk["all_prefit_checks_pass"], "prototype checks have not passed"
    assert chk["binding"] == P.binding(d_fit), "stale prototype checks: rerun prototype.py checks"
    table_sha = sha(HERE / PILOT["scenarios_file"])
    for sub in ("data", "inits", "preflight"):
        shutil.rmtree(PAY / sub, ignore_errors=True)
        (PAY / sub).mkdir(parents=True)
    rows = []
    for s in scenarios():
        assert int(s["sampler_seed"]) == RUN_ENV["SEED"]
        ov = dict(lambda0=float(s["lambda0"]), sigma=float(s["sigma"]), rho=float(s["rho"]))
        outcome, d, ginfo, oinfo, secs = generate(int(s["gen_seed"]), ov, PILOT["generator"]["timeout_seconds"])
        row = dict(s, outcome=outcome, generator_seconds=secs, true_lineages=(ginfo or {}).get("true_lineages"))
        if outcome == "ok":
            write_stan_json(str(PAY / "data" / f"{s['id']}.json"), d)
            write_starts(PAY / "inits" / s["id"], d["N"])
            row.update(N=d["N"], observation=oinfo, cohort=d["NC"], singles=d["C1"], pairs=d["C2"])
        rows.append(row)
        print(s["id"], outcome, row.get("N"), secs)
    # The replay dataset is the prototype's cost dataset at 64 nodes, and its starts are the frozen v4/v5 files.
    d_r00 = json.loads((PAY / "data" / "R00.json").read_text())
    ref = json.loads(json.dumps(d_fit, default=float))
    assert all(np.allclose(np.asarray(d_r00[k], float), np.asarray(ref[k], float), rtol=0, atol=0) for k in ref), "R00 differs"
    for k in range(1, 5):
        assert (PAY / "inits" / "R00" / f"chain{k}.json").read_bytes() == \
            (P.HERE / P.CFG[ver]["inits"]["dir"] / f"chain{k}.json").read_bytes(), "R00 starts differ from the checked starts"
    # Preflight points and their local reference log density and gradients.
    tail, _, imax = P.v4_states(d_fit)
    sp = P.stress_points(d_fit)
    pts = dict(central0=sp["central0"], stress_s3_r09_kbm15=sp["stress_s3_r09_kbm15"], max_sigma_v4_state=tail[imax])
    exe = P.OUT / P.CFG[ver]["stan_file"].removesuffix(".stan")
    for name, q in pts.items():
        write_stan_json(str(PAY / "preflight" / f"point_{name}.json"), q)
        log_prob_csv(exe, PAY / "preflight" / f"point_{name}.json", PAY / "data" / "R00.json",
                     PAY / "preflight" / f"ref_point_{name}.csv")
    for row in rows:
        if row["outcome"] == "ok":
            row["starts_initialise"] = start_check(exe, row["id"])
    shutil.copy(P.HERE / P.CFG[ver]["stan_file"], PAY / P.CFG[ver]["stan_file"])
    shutil.copy(HERE / PILOT["scenarios_file"], PAY / "scenarios.tsv")
    (PAY / "run.env").write_text("".join(f"{k}={v}\n" for k, v in RUN_ENV.items()))
    tb = cmdstan_tarball()
    (PAY / "cmdstan.sha256").write_text(f"{sha(tb)}  {tb.name}\n")
    nfiles = write_manifest(PAY)
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=HERE).stdout.strip()
    man = dict(created=time.strftime("%Y-%m-%dT%H:%M:%S%z"), git_head_at_build=head, files=nfiles,
               manifest_sha256=sha(PAY / "manifest.sha256"), pilot_json_sha256=sha(HERE / "pilot.json"),
               scenario_table=dict(file=PILOT["scenarios_file"], sha256=table_sha, frozen_commit="c93ea58"),
               prototype_checks=dict(file=PILOT["candidate"]["checks_file"], sha256=sha(HERE / PILOT["candidate"]["checks_file"]),
                                     binding=chk["binding"], all_prefit_checks_pass=chk["all_prefit_checks_pass"]),
               cmdstan=dict(version=RUN_ENV["CMDSTAN_VERSION"], url=PILOT["runtime"]["cmdstan_url"], tarball_sha256=sha(tb)),
               run_env=RUN_ENV, scenarios=rows)
    (PAY / "manifest.json").write_text(json.dumps(man, indent=1, default=float) + "\n")
    print(json.dumps({k: v for k, v in man.items() if k != "scenarios"}, indent=1))


# ---------------------------------------------------------------- control fixtures
def _run(cmd, root, env=None, timeout=900):
    import os
    e = {k: v for k, v in os.environ.items() if not k.startswith("PBS_")}
    e.update(PILOT_ROOT=str(root), **(env or {}))
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=root, env=e, timeout=timeout)
    return r.returncode, r.stdout + r.stderr


def _receipt(path):
    return dict(ln.split("=", 1) for ln in pathlib.Path(path).read_text().splitlines() if "=" in ln)


def selftest():
    """Cheap fixtures for every control the cluster relies on; writes selftest.json. Uses the local CmdStan binary."""
    from cmdstanpy.utils import write_stan_json
    import os
    import signal
    out = {}
    # Generator controls.
    o = generate(20261017, dict(lineage_cap=30), 60)
    out["generator_cap"] = dict(outcome=o[0], expected="capped", ok=o[0] == "capped")
    o = generate(20261017, {}, 0.001)
    out["generator_timeout"] = dict(outcome=o[0], expected="timeout", ok=o[0] == "timeout")
    # Runner fixtures: the frozen-seed dataset (62 lineages), the payload's fit.sh and the local binary.
    root = CACHE / "selftest"
    shutil.rmtree(root, ignore_errors=True)
    (root / "pbs").mkdir(parents=True)
    shutil.copy(PAY / "pbs" / "fit.sh", root / "pbs" / "fit.sh")
    exe = P.OUT / P.CFG[P.CFG["active"]]["stan_file"].removesuffix(".stan")
    shutil.copy(exe, root / "model_v4")
    d, _, _ = P.dataset(P.CFG["seed"])
    (root / "data").mkdir()
    for scen in ("FX", "FY", "FB", "FT"):
        write_stan_json(str(root / "data" / f"{scen}.json"), d)
        write_starts(root / "inits" / scen, d["N"])
    bad = json.loads((root / "inits" / "FB" / "chain2.json").read_text())
    bad["sigma"] = -1.0
    (root / "inits" / "FB" / "chain2.json").write_text(json.dumps(bad))
    (root / "scenarios.tsv").write_text("id\trole\n" + "FX\treplay\nFY\tpanel\nFB\treplay\nFT\treplay\n")
    env = dict(RUN_ENV, WARMUP=10, SAMPLING=5, FIT_SECONDS=600)
    (root / "run.env").write_text("".join(f"{k}={v}\n" for k, v in env.items()))
    (root / "build").mkdir()
    (root / "build" / "receipt.txt").write_text(f"status=ok\nbinary_sha256={sha(root / 'model_v4')}\n")
    write_manifest(root)
    fit = ["bash", "pbs/fit.sh"]

    code, txt = _run(fit, root, dict(SCEN="FX"))
    rc = _receipt(root / "runs" / "FX" / "receipt.txt")
    out["complete"] = dict(exit=code, status=rc.get("status"), chains_complete=[rc.get(f"chain{k}_complete") for k in range(1, 5)],
                           maxrss_kb=[rc.get(f"chain{k}_maxrss_kb") for k in range(1, 5)],
                           ok=code == 0 and rc.get("status") == "complete")
    code, txt = _run(fit, root, dict(SCEN="FX"))
    out["resume_skip"] = dict(exit=code, said_skip="SKIP" in txt, second_attempt=(root / "runs" / "FX" / "attempt2").exists(),
                              ok=code == 0 and "SKIP" in txt and not (root / "runs" / "FX" / "attempt2").exists())
    code, txt = _run(fit, root, dict(PBS_ARRAY_INDEX="1"))
    out["array_index_maps_to_first_panel_row"] = dict(exit=code, ran=(root / "runs" / "FY" / "receipt.txt").exists(),
                                                      ok=code == 0 and (root / "runs" / "FY" / "receipt.txt").exists())
    code, txt = _run(fit, root, dict(SCEN="FB"))
    rc = _receipt(root / "runs" / "FB" / "receipt.txt")
    out["chain_failure"] = dict(exit=code, status=rc.get("status"), chain_exits=[rc.get(f"chain{k}_exit") for k in range(1, 5)],
                                ok=code == 1 and rc.get("status") == "failed" and rc.get("chain2_exit") != "0")
    # Signal: TERM the runner mid-fit; chains must stop and a receipt must say so.
    slow = dict(env, WARMUP=2000, SAMPLING=2000)
    (root / "run.env").write_text("".join(f"{k}={v}\n" for k, v in slow.items()))
    write_manifest(root)
    p = subprocess.Popen(fit, cwd=root, env=dict({k: v for k, v in os.environ.items() if not k.startswith("PBS_")},
                                                  PILOT_ROOT=str(root), SCEN="FT"),
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    time.sleep(8)
    p.send_signal(signal.SIGTERM)
    p.wait(60)
    time.sleep(3)
    rc = _receipt(root / "runs" / "FT" / "receipt.txt")
    left = subprocess.run(["pgrep", "-f", str(root / "runs" / "FT")], capture_output=True, text=True).stdout.strip()
    left = left or subprocess.run(["pgrep", "-f", "runs/FT/attempt"], capture_output=True, text=True).stdout.strip()
    out["signal_term"] = dict(exit=p.returncode, status=rc.get("status"), chains_left_running=bool(left),
                              ok=p.returncode == 3 and rc.get("status") == "terminated_TERM" and not left)
    # Timeout: a 3-second fit limit.
    (root / "run.env").write_text("".join(f"{k}={v}\n" for k, v in dict(slow, FIT_SECONDS=3).items()))
    write_manifest(root)
    code, txt = _run(fit, root, dict(SCEN="FT"))
    rc = _receipt(root / "runs" / "FT" / "receipt.txt")
    out["timeout"] = dict(exit=code, status=rc.get("status"), attempt=rc.get("attempt"),
                          chain_exits=[rc.get(f"chain{k}_exit") for k in range(1, 5)],
                          ok=code == 4 and rc.get("status") == "timeout" and rc.get("attempt") == "2")
    # Stale payload: a data file changed after the manifest; and a binary that differs from the build receipt.
    f = root / "data" / "FY.json"
    f.write_text(f.read_text() + " ")
    code, txt = _run(fit, root, dict(SCEN="FY"))
    out["stale_data_refused"] = dict(exit=code, ok=code == 2 and "REFUSED" in txt)
    write_manifest(root)
    (root / "build" / "receipt.txt").write_text("status=ok\nbinary_sha256=" + "0" * 64 + "\n")
    code, txt = _run(fit, root, dict(SCEN="FY"))
    out["binary_mismatch_refused"] = dict(exit=code, ok=code == 2 and "REFUSED" in txt)
    # Preflight on a copy of the real payload with the local binary: must pass, and a perturbed reference must fail.
    pf = CACHE / "selftest_preflight"
    shutil.rmtree(pf, ignore_errors=True)
    shutil.copytree(PAY, pf, ignore=shutil.ignore_patterns("runs", "build"))
    shutil.copy(exe, pf / "model_v4")
    code, txt = _run(["bash", "pbs/preflight.sh", "build/receipt.tmp"], pf, timeout=1200)
    out["preflight_local_binary"] = dict(exit=code, receipt=(pf / "build" / "receipt.tmp").read_text().split(),
                                         ok=code == 0)
    refs = sorted((pf / "preflight").glob("ref_point_*.csv"))
    lines = refs[0].read_text().splitlines()
    i = max(j for j, ln in enumerate(lines) if ln and not ln.startswith("#"))
    vals = lines[i].split(",")
    vals[0] = repr(float(vals[0]) * (1 + 1e-5))
    lines[i] = ",".join(vals)
    refs[0].write_text("\n".join(lines) + "\n")
    shutil.rmtree(pf / "build")
    code, txt = _run(["bash", "pbs/preflight.sh", "build/receipt.tmp"], pf, timeout=600)
    out["preflight_mismatch_detected"] = dict(exit=code, reason=(pf / "build" / "preflight_reason.txt").read_text().strip(),
                                              ok=code == 1 and "mismatch" in (pf / "build" / "preflight_reason.txt").read_text())
    out["all_pass"] = all(v["ok"] for v in out.values() if isinstance(v, dict))
    (HERE / "selftest.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


# ---------------------------------------------------------------- screening
def chain_files(folder):
    folder = pathlib.Path(folder)
    csvs = sorted(folder.glob("chain*.csv")) or sorted(folder.glob("*.csv"))
    outs = sorted(folder.glob("chain*.stdout")) or sorted(folder.glob("*-stdout.txt"))
    return csvs, outs


def stdout_record(f):
    phase, prev, rej, fatal = "init", "", {}, []
    for line in pathlib.Path(f).read_text(errors="replace").splitlines():
        if line.startswith("Iteration:"):
            phase = "sampling" if "(Sampling)" in line else "warmup"
        elif line.startswith("Exception:"):
            if prev.startswith("Informational Message") or "Error evaluating the log probability at the initial" in prev:
                key = f"{P.cause(line)}_{'init_value' if 'initial' in prev else phase}"
                rej[key] = rej.get(key, 0) + 1
            else:
                fatal.append(dict(phase=phase, cause=P.cause(line), after=prev.strip(), message=line.strip()[:240]))
        if line.strip():
            prev = line
    return rej, fatal


def ebfmi(e):
    """E-BFMI per chain as CmdStan's diagnose defines it (diagnose.cpp: mean squared successive energy difference
    over the sample variance, which equals the ratio of the two sums). A population-variance denominator gives values
    larger by n / (n - 1)."""
    return float(np.sum(np.diff(e) ** 2) / np.sum((e - e.mean()) ** 2))


def diagnose(folder, scen_id):
    """Codex's screening thresholds (76/1750) for one attempt directory; writes diagnostics.json beside the draws."""
    import arviz as az
    import pandas as pd
    S, D = PILOT["screening"], PILOT["decision"]
    max_depth = PILOT["sampler"]["max_treedepth"]
    csvs, outs = chain_files(folder)
    chains = []
    for c, o in zip(csvs, outs):
        txt = c.read_text(errors="replace")
        rej, fatal = stdout_record(o)
        chains.append(dict(csv=c.name, complete="seconds (Total)" in txt, rejections=rej, fatal=fatal))
    dfs = [pd.read_csv(c, comment="#") for c in csvs]
    n = min(len(x) for x in dfs)
    arr = lambda col: np.stack([x[col].to_numpy()[:n] for x in dfs])
    for ch, x in zip(chains, dfs):
        ch.update(draws=len(x), divergences=int(x["divergent__"].sum()), depth_hits=int((x["treedepth__"] >= max_depth).sum()),
                  ebfmi=ebfmi(x["energy__"].to_numpy()),
                  sampling_phase_rejections=sum(v for k, v in ch["rejections"].items() if k.endswith("_sampling")))
    cols = [c for c in dfs[0].columns if not c.endswith("__") or c == "lp__"]
    rhat = {c: float(az.rhat(arr(c))) for c in cols}
    ess = {c: dict(bulk=float(az.ess(arr(c), method="bulk")), tail=float(az.ess(arr(c), method="tail"))) for c in S["core"]}
    eta = arr("eta")
    q05, q95 = (float(v) for v in np.quantile(eta.ravel(), [0.05, 0.95]))
    m05, m95 = float(az.mcse(eta, method="quantile", prob=0.05)), float(az.mcse(eta, method="quantile", prob=0.95))
    worst = sorted(rhat.items(), key=lambda kv: -kv[1] if np.isfinite(kv[1]) else -np.inf)
    crit = dict(
        four_chains_complete=len(chains) == S["chains_complete"] and all(c["complete"] for c in chains),
        zero_post_warmup_divergences=sum(c["divergences"] for c in chains) == S["post_warmup_divergences"],
        no_fatal_or_sampling_phase_failures=not any(c["fatal"] or c["sampling_phase_rejections"] for c in chains),
        ebfmi_each_chain=all(c["ebfmi"] >= S["ebfmi_min_per_chain"] for c in chains),
        rhat_all=all(v < S["rhat_max"] for v in rhat.values()),
        ess_bulk_tail_core=all(v["bulk"] >= S["ess_bulk_and_tail_min_core"] and v["tail"] >= S["ess_bulk_and_tail_min_core"]
                               for v in ess.values()))
    truth = next((float(s["eta"]) for s in scenarios() if s["id"] == scen_id), None)
    res = dict(
        scenario=scen_id, folder=str(folder), draws_per_chain=n, chains=chains, screening=crit, screening_pass=all(crit.values()),
        rhat_max=worst[0], rhat_over_threshold=[(k, v) for k, v in worst if v >= S["rhat_max"]][:20],
        rhat_core={c: rhat[c] for c in S["core"]}, ess_core=ess,
        eta=dict(q05=q05, q95=q95, median=float(np.median(eta)), mcse_q05=m05, mcse_q95=m95,
                 mcse_target_met=max(m05, m95) <= D["mcse_target"], truth=truth,
                 interval_covers_truth=None if truth is None else q05 <= truth <= q95,
                 D=q05 > D["eta0"], X=q95 < D["eta1"],
                 D_numerically_uncertain=q05 - 2 * m05 < D["eta0"] < q05 + 2 * m05,
                 X_numerically_uncertain=q95 - 2 * m95 < D["eta1"] < q95 + 2 * m95))
    (pathlib.Path(folder) / "diagnostics.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k not in ("chains", "rhat_over_threshold")}, indent=1))
    return res


if __name__ == "__main__":
    {"build": build, "selftest": selftest, "diagnose": lambda: diagnose(sys.argv[2], sys.argv[3])}[sys.argv[1]]()
