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


# ---------------------------------------------------------------- screening
def _receipt(path):
    return dict(ln.split("=", 1) for ln in pathlib.Path(path).read_text().splitlines() if "=" in ln)


def settings_line(env):
    """The settings line fit.sh writes into every receipt, for the given run.env values."""
    e = {k: str(v) for k, v in env.items()}
    return (f"chains {e['CHAINS']}; warmup {e['WARMUP']}; sampling {e['SAMPLING']}; adapt_delta {e['ADAPT_DELTA']}; "
            f"max_depth {e['MAX_DEPTH']}; stepsize {e['STEPSIZE']}; seed {e['SEED']}; fit_seconds {e['FIT_SECONDS']}")


def csv_meta(path):
    """CmdStan CSV header settings; 'file' is qualified by its section (data.file, output.file)."""
    meta, section = {}, ""
    with open(path, errors="replace") as f:
        for line in f:
            if not line.startswith("#"):
                break
            s = line[1:].strip()
            if "=" in s:
                k, v = (x.strip() for x in s.split("=", 1))
                v = v.replace("(Default)", "").strip()
                meta.setdefault(f"{section}.file" if k == "file" else k, v)
            elif s:
                section = s
    return meta


def csv_draws(path):
    with open(path, errors="replace") as f:
        rows = [ln for ln in f if ln.strip() and not ln.startswith("#")]
    return len(rows) - 1


def stdout_record(text):
    phase, prev, rej, fatal = "init", "", {}, []
    for line in text.splitlines():
        if line.startswith("Iteration:"):
            phase = "sampling" if "(Sampling)" in line else "warmup"
        elif line.startswith("Exception:"):
            if prev.startswith("Informational Message") or "Error evaluating the log probability at the initial" in prev:
                key = f"{P.cause(line)}_{'init_value' if 'initial' in prev else phase}"
                rej[key] = rej.get(key, 0) + 1
            else:
                fatal.append(dict(phase=phase, cause=P.cause(line), after=prev.strip(), message=line.strip()[:240]))
        elif "Unrecoverable" in line or "Exception initializing" in line:
            fatal.append(dict(phase=phase, cause="unrecoverable", after=prev.strip(), message=line.strip()[:240]))
        if line.strip():
            prev = line
    return rej, fatal


def qualify(attempt, scen, env, manifest_sha, build_receipt):
    """Structural qualification of one attempt, before any statistics. Returns the list of failures (empty if it qualifies)."""
    attempt = pathlib.Path(attempt)
    fails = []
    if not (attempt / "receipt.txt").exists():
        return ["no receipt"]
    rc = _receipt(attempt / "receipt.txt")
    want = dict(scenario=scen, attempt=attempt.name.removeprefix("attempt"), status="complete", manifest_sha256=manifest_sha,
                binary_sha256=build_receipt.get("binary_sha256"), settings=settings_line(env))
    fails += [f"receipt {k} is {rc.get(k)!r}, expected {v!r}" for k, v in want.items() if rc.get(k) != v]
    if build_receipt.get("status") != "ok":
        fails.append(f"build receipt status is {build_receipt.get('status')!r}")
    if build_receipt.get("manifest_sha256") != manifest_sha:
        fails.append("build receipt is for a different payload manifest")
    C = int(env["CHAINS"])
    expected = {f"chain{k}.{x}" for k in range(1, C + 1) for x in ("csv", "stdout", "stderr", "exit")}
    present = {f.name for f in attempt.iterdir()}
    fails += [f"missing {n}" for n in sorted(expected - present)]
    fails += [f"unexpected output file {n}" for n in sorted(present)
              if (n.endswith((".csv", ".stdout", ".stderr", ".exit")) and n not in expected)
              or (n.endswith(".time") and n.removesuffix(".time") + ".csv" not in expected)]
    for k in range(1, C + 1):
        c = attempt / f"chain{k}"
        if not all((attempt / f"chain{k}.{x}").exists() for x in ("csv", "stdout", "stderr", "exit")):
            continue
        if (attempt / f"chain{k}.exit").read_text().strip() != "0" or rc.get(f"chain{k}_exit") != "0":
            fails.append(f"chain {k} exit {(attempt / f'chain{k}.exit').read_text().strip()!r}")
        err = (attempt / f"chain{k}.stderr").read_text(errors="replace").strip()
        if err:
            fails.append(f"chain {k} stderr not empty: {err.splitlines()[0][:160]!r}")
        _, fatal = stdout_record((attempt / f"chain{k}.stdout").read_text(errors="replace"))
        if fatal:
            fails.append(f"chain {k} fatal: {fatal[0]['message'][:160]!r}")
        if "seconds (Total)" not in pathlib.Path(f"{c}.csv").read_text(errors="replace"):
            fails.append(f"chain {k} CSV incomplete")
        m = csv_meta(f"{c}.csv")
        for key, val in (("num_samples", env["SAMPLING"]), ("num_warmup", env["WARMUP"]), ("delta", env["ADAPT_DELTA"]),
                         ("max_depth", env["MAX_DEPTH"]), ("stepsize", env["STEPSIZE"]), ("seed", env["SEED"]), ("id", k)):
            try:
                ok = float(m.get(key, "nan")) == float(val)
            except ValueError:
                ok = False
            if not ok:
                fails.append(f"chain {k} CSV {key} is {m.get(key)!r}, expected {val!r}")
        for key, val in (("data.file", f"data/{scen}.json"), ("init", f"inits/{scen}/chain{k}.json")):
            if m.get(key) != val:
                fails.append(f"chain {k} CSV {key} is {m.get(key)!r}, expected {val!r}")
        n = csv_draws(f"{c}.csv")
        if n != int(env["SAMPLING"]):
            fails.append(f"chain {k} has {n} retained draws, expected {env['SAMPLING']}")
    return fails


def ebfmi(e):
    """E-BFMI per chain as CmdStan's diagnose defines it (diagnose.cpp: mean squared successive energy difference
    over the sample variance, which equals the ratio of the two sums). A population-variance denominator gives values
    larger by n / (n - 1)."""
    return float(np.sum(np.diff(e) ** 2) / np.sum((e - e.mean()) ** 2))


def _finite(x):
    return x is not None and bool(np.isfinite(x))


def rhat_pass(rhat):
    return bool(rhat) and all(_finite(v) and v < PILOT["screening"]["rhat_max"] for v in rhat.values())


def ess_pass(ess):
    T = PILOT["screening"]["ess_bulk_and_tail_min_core"]
    return bool(ess) and all(_finite(v["bulk"]) and _finite(v["tail"]) and v["bulk"] >= T and v["tail"] >= T for v in ess.values())


def eta_block(q05, q95, m05, m95, truth):
    """Endpoints, raw D/X flags and Monte Carlo precision. Non-finite endpoints or MCSE leave the affected items unresolved
    (None), never passed."""
    D = PILOT["decision"]
    ends = _finite(q05) and _finite(q95)
    prec = _finite(m05) and _finite(m95) and m05 >= 0 and m95 >= 0
    return dict(q05=q05, q95=q95, mcse_q05=m05, mcse_q95=m95, endpoints_finite=ends, mcse_finite=prec,
                mcse_target_met=(max(m05, m95) <= D["mcse_target"]) if prec else None, truth=truth,
                interval_covers_truth=(q05 <= truth <= q95) if ends and truth is not None else None,
                D=(q05 > D["eta0"]) if ends else None, X=(q95 < D["eta1"]) if ends else None,
                D_numerically_uncertain=(q05 - 2 * m05 < D["eta0"] < q05 + 2 * m05) if ends and prec else None,
                X_numerically_uncertain=(q95 - 2 * m95 < D["eta1"] < q95 + 2 * m95) if ends and prec else None)


def statistics(csvs, outs, truth):
    """Screening statistics on chain files of equal, already verified length."""
    import arviz as az
    import pandas as pd
    S = PILOT["screening"]
    dfs = [pd.read_csv(c, comment="#") for c in csvs]
    assert len({len(x) for x in dfs}) == 1, "unequal chain lengths"
    arr = lambda col: np.stack([x[col].to_numpy() for x in dfs])
    chains = []
    for c, o, x in zip(csvs, outs, dfs):
        rej, fatal = stdout_record(pathlib.Path(o).read_text(errors="replace"))
        chains.append(dict(csv=pathlib.Path(c).name, draws=len(x), divergences=int(x["divergent__"].sum()),
                           depth_hits=int((x["treedepth__"] >= PILOT["sampler"]["max_treedepth"]).sum()),
                           ebfmi=ebfmi(x["energy__"].to_numpy()), rejections=rej, fatal=fatal,
                           sampling_phase_rejections=sum(v for k, v in rej.items() if k.endswith("_sampling"))))
    cols = [c for c in dfs[0].columns if not c.endswith("__") or c == "lp__"]
    rhat = {c: float(az.rhat(arr(c))) for c in cols}
    ess = {c: dict(bulk=float(az.ess(arr(c), method="bulk")), tail=float(az.ess(arr(c), method="tail"))) for c in S["core"]}
    eta = arr("eta")
    q05, q95 = (float(v) for v in np.quantile(eta.ravel(), [0.05, 0.95]))
    m05, m95 = float(az.mcse(eta, method="quantile", prob=0.05)), float(az.mcse(eta, method="quantile", prob=0.95))
    crit = dict(
        zero_post_warmup_divergences=sum(c["divergences"] for c in chains) == S["post_warmup_divergences"],
        no_fatal_or_sampling_phase_failures=not any(c["fatal"] or c["sampling_phase_rejections"] for c in chains),
        ebfmi_each_chain=all(_finite(c["ebfmi"]) and c["ebfmi"] >= S["ebfmi_min_per_chain"] for c in chains),
        rhat_all=rhat_pass(rhat), ess_bulk_tail_core=ess_pass(ess))
    worst = sorted(rhat.items(), key=lambda kv: -kv[1] if _finite(kv[1]) else -np.inf)
    return dict(chains=chains, screening=crit, screening_pass=all(crit.values()), rhat_max=worst[0],
                rhat_over_threshold=[(k, v) for k, v in worst if not _finite(v) or v >= S["rhat_max"]][:20],
                rhat_core={c: rhat[c] for c in S["core"]}, ess_core=ess, eta=eta_block(q05, q95, m05, m95, truth))


def _clean(x):
    if isinstance(x, float) and not np.isfinite(x):
        return repr(x)
    if isinstance(x, dict):
        return {k: _clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_clean(v) for v in x]
    return x


def diagnose(attempt, scen, env=None, manifest_sha=None, build_receipt=None, write=True):
    """Pilot qualification and screening of one fetched attempt (Codex 76/1750, 76/1765). Structural failures leave the
    fit unresolved and no statistics are computed. Defaults: the local payload's run.env and manifest, and the build
    receipt fetched with the run (<fetch root>/build/receipt.txt)."""
    attempt = pathlib.Path(attempt)
    env = env or RUN_ENV
    manifest_sha = manifest_sha or sha(PAY / "manifest.sha256")
    if build_receipt is None:
        br = attempt.parents[2] / "build" / "receipt.txt"
        build_receipt = _receipt(br) if br.exists() else {}
    fails = qualify(attempt, scen, env, manifest_sha, build_receipt)
    truth = next((float(s["eta"]) for s in scenarios() if s["id"] == scen), None)
    res = dict(scenario=scen, attempt=str(attempt), qualified=not fails, qualification_failures=fails)
    if fails:
        res.update(status="unresolved", screening_pass=None)
    else:
        C = int(env["CHAINS"])
        st = statistics([attempt / f"chain{k}.csv" for k in range(1, C + 1)],
                        [attempt / f"chain{k}.stdout" for k in range(1, C + 1)], truth)
        res.update(status="screened", **st)
        res["precision"] = ("met" if st["eta"]["mcse_target_met"] else "not met" if st["eta"]["mcse_target_met"] is False
                            else "unresolved")
    res = _clean(res)
    if write:
        (attempt / "diagnostics.json").write_text(json.dumps(res, indent=1) + "\n")
    return res


def summarise(folder):
    """Historical summary of older output (for example the v4 fit). Not pilot qualification: no receipts are checked."""
    folder = pathlib.Path(folder)
    csvs = sorted(folder.glob("chain*.csv")) or sorted(folder.glob("*.csv"))
    outs = sorted(folder.glob("chain*.stdout")) or sorted(folder.glob("*-stdout.txt"))
    assert len(csvs) == len(outs) and csvs, "unpaired chain files"
    res = dict(kind="historical summary; not pilot qualification", folder=str(folder), **statistics(csvs, outs, None))
    print(json.dumps(_clean({k: v for k, v in res.items() if k != "chains"}), indent=1))
    return res


# ---------------------------------------------------------------- control fixtures
def _run(cmd, root, env=None, timeout=900):
    import os
    e = {k: v for k, v in os.environ.items() if not k.startswith("PBS_") and k != "LOADEDMODULES"}
    e.update(PILOT_ROOT=str(root), **(env or {}))
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=root, env=e, timeout=timeout)
    return r.returncode, r.stdout + r.stderr


def _fixture_seal(root, binary="model_v4"):
    """Rewrite a fixture's manifest and a successful build receipt bound to it."""
    write_manifest(root)
    (root / "build").mkdir(exist_ok=True)
    (root / "build" / "receipt.txt").write_text(
        f"status=ok\nmanifest_sha256={sha(root / 'manifest.sha256')}\nbinary_sha256={sha(root / binary)}\n")


def _write_env(root, env):
    (root / "run.env").write_text("".join(f"{k}={v}\n" for k, v in env.items()))


def selftest():
    """Cheap fixtures for every control the cluster relies on; writes selftest.json. Uses the local CmdStan binary."""
    from cmdstanpy.utils import write_stan_json
    import os
    import signal
    out = {}
    # Generator controls.
    o = generate(20261017, dict(lineage_cap=30), 60)
    out["generator_cap"] = dict(outcome=o[0], ok=o[0] == "capped")
    o = generate(20261017, {}, 0.001)
    out["generator_timeout"] = dict(outcome=o[0], ok=o[0] == "timeout")
    # Runner fixtures: the frozen-seed dataset (62 lineages), the payload's scripts and the local binary.
    root = CACHE / "selftest"
    shutil.rmtree(root, ignore_errors=True)
    shutil.copytree(PAY / "pbs", root / "pbs")
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
    env = dict(RUN_ENV, WARMUP=10, SAMPLING=5, FIT_SECONDS=600, MODULE="")
    _write_env(root, env)
    _fixture_seal(root)
    fit = ["bash", "pbs/fit.sh"]

    code, txt = _run(fit, root, dict(SCEN="FX"))
    rc = _receipt(root / "runs" / "FX" / "receipt.txt")
    out["complete"] = dict(exit=code, status=rc.get("status"), maxrss_kb=[rc.get(f"chain{k}_maxrss_kb") for k in range(1, 5)],
                           ok=code == 0 and rc.get("status") == "complete")
    code, txt = _run(fit, root, dict(SCEN="FX"))
    out["resume_skip"] = dict(exit=code, ok=code == 0 and "SKIP" in txt and not (root / "runs" / "FX" / "attempt2").exists())
    code, txt = _run(fit, root, dict(PBS_ARRAY_INDEX="1"))
    out["array_index_maps_to_first_panel_row"] = dict(exit=code, ok=code == 0 and (root / "runs" / "FY" / "receipt.txt").exists())
    code, txt = _run(fit, root, dict(SCEN="FB"))
    rc = _receipt(root / "runs" / "FB" / "receipt.txt")
    out["chain_failure"] = dict(exit=code, status=rc.get("status"), chain_exits=[rc.get(f"chain{k}_exit") for k in range(1, 5)],
                                ok=code == 1 and rc.get("status") == "failed" and rc.get("chain2_exit") != "0")
    # Module: a declared module that is not loaded is refused; when loaded, the runner proceeds (here to the skip).
    _write_env(root, dict(env, MODULE=RUN_ENV["MODULE"]))
    _fixture_seal(root)
    code, txt = _run(fit, root, dict(SCEN="FX"))
    out["module_not_loaded_refused"] = dict(exit=code, ok=code == 2 and "module" in txt)
    code, txt = _run(fit, root, dict(SCEN="NODATA", LOADEDMODULES=f"GCCcore/12.3.0:{RUN_ENV['MODULE']}"))
    out["module_loaded_passes_module_check"] = dict(exit=code, ok=code == 2 and "no data or starts" in txt)
    _write_env(root, env)
    _fixture_seal(root)
    # Signal, cooperative model: TERM the runner mid-fit.
    slow = dict(env, WARMUP=2000, SAMPLING=2000)
    _write_env(root, slow)
    _fixture_seal(root)

    def term_test(scen, wait):
        p = subprocess.Popen(fit, cwd=root, env=dict({k: v for k, v in os.environ.items() if not k.startswith("PBS_")},
                                                      PILOT_ROOT=str(root), SCEN=scen),
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        time.sleep(wait)
        p.send_signal(signal.SIGTERM)
        p.wait(60)
        rc = _receipt(root / "runs" / scen / "receipt.txt")
        left = subprocess.run(["pgrep", "-f", f"runs/{scen}/attempt"], capture_output=True, text=True).stdout.split()
        left += subprocess.run(["pgrep", "-f", "fake_model"], capture_output=True, text=True).stdout.split()
        return p.returncode, rc, left
    code, rc, left = term_test("FT", 8)
    out["signal_term"] = dict(exit=code, status=rc.get("status"), cleanup=rc.get("cleanup"), left_running=left,
                              ok=code == 3 and rc.get("status") == "terminated_TERM" and not left)
    # Signal, TERM-ignoring model: the runner must escalate to KILL and leave nothing behind before the receipt.
    (root / "fake_model").write_text("#!/bin/bash\ntrap '' TERM\nwhile :; do sleep 1; done\n")
    (root / "fake_model").chmod(0o755)
    _write_env(root, dict(slow, MODEL_BIN="./fake_model"))
    _fixture_seal(root, "fake_model")
    code, rc, left = term_test("FY", 3)
    for pid in left:
        subprocess.run(["kill", "-KILL", pid])
    out["signal_term_ignoring_model"] = dict(exit=code, status=rc.get("status"), cleanup=rc.get("cleanup"), left_running=left,
                                             ok=code == 3 and rc.get("status") == "terminated_TERM" and not left
                                             and "kill_escalated yes" in rc.get("cleanup", "") and "survivors no" in rc.get("cleanup", ""))
    # Timeout: a 3-second fit limit.
    _write_env(root, dict(slow, FIT_SECONDS=3))
    _fixture_seal(root)
    code, txt = _run(fit, root, dict(SCEN="FT"))
    rc = _receipt(root / "runs" / "FT" / "receipt.txt")
    out["timeout"] = dict(exit=code, status=rc.get("status"), attempt=rc.get("attempt"),
                          chain_exits=[rc.get(f"chain{k}_exit") for k in range(1, 5)],
                          ok=code == 4 and rc.get("status") == "timeout" and rc.get("attempt") == "2")
    _write_env(root, env)
    _fixture_seal(root)
    # Refusals: stale data, a binary differing from the build receipt, and a build receipt for another manifest.
    f = root / "data" / "FY.json"
    f.write_text(f.read_text() + " ")
    code, txt = _run(fit, root, dict(SCEN="FX"))
    out["stale_data_refused"] = dict(exit=code, ok=code == 2 and "manifest mismatch" in txt)
    _fixture_seal(root)
    br = (root / "build" / "receipt.txt").read_text()
    (root / "build" / "receipt.txt").write_text(br.replace(f"binary_sha256={sha(root / 'model_v4')}", "binary_sha256=" + "0" * 64))
    code, txt = _run(fit, root, dict(SCEN="FX"))
    out["binary_mismatch_refused"] = dict(exit=code, ok=code == 2 and "binary hash" in txt)
    (root / "build" / "receipt.txt").write_text(br.replace(f"manifest_sha256={sha(root / 'manifest.sha256')}", "manifest_sha256=" + "1" * 64))
    code, txt = _run(fit, root, dict(SCEN="FX"))
    out["build_manifest_mismatch_refused"] = dict(exit=code, ok=code == 2 and "different payload manifest" in txt)
    (root / "build" / "receipt.txt").write_text(br)
    # Screening refuses failed, mismatched or malformed output before any statistics.
    good = root / "runs" / "FX" / "attempt1"
    man, bld = sha(root / "manifest.sha256"), _receipt(root / "build" / "receipt.txt")
    # The FX receipt predates later reseals; requalify it against the manifest and binary it was produced under.
    rcx = _receipt(good / "receipt.txt")
    q = lambda a, s="FX", e=env, m=None, b=None: qualify(a, s, e, m or rcx["manifest_sha256"],
                                                         b or dict(bld, manifest_sha256=rcx["manifest_sha256"]))
    scr = {}
    scr["good_attempt_qualifies"] = (q(good), lambda r: r == [])

    def variant(name, mutate):
        v = root / "runs" / "DX" / name / "attempt1"
        shutil.copytree(good, v)
        mutate(v)
        return v
    scr["no_receipt"] = (q(variant("norec", lambda v: (v / "receipt.txt").unlink())), bool)
    scr["receipt_for_other_scenario_failed_and_stale"] = (q(variant("other", lambda v: (v / "receipt.txt").write_text(
        (v / "receipt.txt").read_text().replace("scenario=FX", "scenario=P12").replace("status=complete", "status=failed")
        .replace(rcx["manifest_sha256"], "2" * 64)))), bool)
    scr["nonzero_chain_exit"] = (q(variant("exit", lambda v: (v / "chain3.exit").write_text("1\n"))), bool)
    scr["fatal_stderr"] = (q(variant("stderr", lambda v: (v / "chain1.stderr").write_text("Exception: fatal\n"))), bool)
    scr["fewer_draws_than_declared"] = (q(good, e=dict(env, SAMPLING=6)), bool)

    def drop_row(v):
        lines = (v / "chain2.csv").read_text().splitlines()
        j = max(i for i, ln in enumerate(lines) if ln and not ln.startswith("#"))
        (v / "chain2.csv").write_text("\n".join(lines[:j] + lines[j + 1:]) + "\n")
    scr["unequal_chain_lengths"] = (q(variant("short", drop_row)), bool)
    scr["fifth_csv"] = (q(variant("fifth", lambda v: shutil.copy(v / "chain1.csv", v / "chain5.csv"))), bool)
    scr["csv_settings_mismatch"] = (q(variant("meta", lambda v: (v / "chain3.csv").write_text(
        (v / "chain3.csv").read_text().replace("delta = 0.995", "delta = 0.9", 1)))), bool)
    scr["build_receipt_other_manifest"] = (q(good, b=dict(bld, manifest_sha256="3" * 64)), bool)
    out["screening_refusals"] = {k: dict(failures=r[:3], ok=pred(r)) for k, (r, pred) in scr.items()}
    out["screening_refusals"]["ok"] = all(v["ok"] for v in out["screening_refusals"].values())
    # Finite guards on statistics.
    nan, inf = float("nan"), float("inf")
    eb = eta_block(0.03, 0.40, 0.003, nan, 0.2)
    out["finite_guards"] = dict(
        nan_mcse_leaves_precision_unresolved=eb["mcse_target_met"] is None and eb["X_numerically_uncertain"] is None,
        raw_flags_kept=eb["D"] is False and eb["X"] is False,
        infinite_ess_fails=not ess_pass({"sigma": dict(bulk=inf, tail=500.0)}),
        nan_rhat_fails=not rhat_pass({"sigma": nan}),
        nan_endpoint_unresolved=eta_block(nan, 0.4, 0.003, 0.01, 0.2)["D"] is None)
    out["finite_guards"]["ok"] = all(out["finite_guards"].values())
    # Retrieval after the earliest failure: a failed build and no run directory.
    fx = CACHE / "selftest_fetch"
    shutil.rmtree(fx, ignore_errors=True)
    (fx / "build").mkdir(parents=True)
    shutil.copytree(PAY / "pbs", fx / "pbs")
    (fx / "build" / "receipt.txt").write_text("status=failed\nreason=cmdstan_build\n")
    (fx / "build" / "cmdstan_build.log").write_text("make: *** [error] 2\n")
    (fx / "submitted.txt").write_text("BUILD_JOB=1.kunanyi FIT_JOB=2.kunanyi\n")
    (fx / "q012_build.o1").write_text("BUILD FAILED: cmdstan_build\n")
    code, txt = _run(["bash", "pbs/pack.sh", "R00"], fx)
    listing = subprocess.run(["tar", "tzf", str(fx / "fetch-R00.tar.gz")], capture_output=True, text=True).stdout.split()
    out["fetch_after_failed_build"] = dict(exit=code, archived=listing,
                                           ok=code == 0 and "build/receipt.txt" in listing and "q012_build.o1" in listing)
    # Provenance: mutating a consumed saved-draw bank changes the prototype binding (on a copy of the banks).
    banks = CACHE / "selftest_banks"
    shutil.rmtree(banks, ignore_errors=True)
    for b in P.SAVED_BANKS:
        (banks / b).mkdir(parents=True)
        for f in (P.OUT / b).glob("*.csv"):
            shutil.copy(f, banks / b / f.name)
    d_fit, _, _ = P.dataset(P.CFG["fit_seed"])
    real_out, chk = P.OUT, json.loads((HERE / PILOT["candidate"]["checks_file"]).read_text())
    try:
        P.OUT = banks
        before = P.binding(d_fit) == chk["binding"]
        tgt = sorted((banks / "fit_v4").glob("*_3.csv"))[0]
        tgt.write_text(tgt.read_text().replace("2.9932533", "3.0932533", 1))
        after = P.binding(d_fit) == chk["binding"]
    finally:
        P.OUT = real_out
    out["bank_mutation_breaks_binding"] = dict(copy_matches_checks=before, matches_after_mutation=after, ok=before and not after)
    # Preflight on a copy of the real payload with the local binary: must pass, and a perturbed reference must fail.
    pf = CACHE / "selftest_preflight"
    shutil.rmtree(pf, ignore_errors=True)
    shutil.copytree(PAY, pf, ignore=shutil.ignore_patterns("runs", "build"))
    shutil.copy(exe, pf / "model_v4")
    code, txt = _run(["bash", "pbs/preflight.sh", "build/receipt.tmp"], pf, timeout=1200)
    out["preflight_local_binary"] = dict(exit=code, receipt=(pf / "build" / "receipt.tmp").read_text().split(), ok=code == 0)
    refs = sorted((pf / "preflight").glob("ref_point_*.csv"))
    lines = refs[0].read_text().splitlines()
    i = max(j for j, ln in enumerate(lines) if ln and not ln.startswith("#"))
    vals = lines[i].split(",")
    vals[0] = repr(float(vals[0]) * (1 + 1e-5))
    lines[i] = ",".join(vals)
    refs[0].write_text("\n".join(lines) + "\n")
    shutil.rmtree(pf / "build")
    code, txt = _run(["bash", "pbs/preflight.sh", "build/receipt.tmp"], pf, timeout=600)
    reason = (pf / "build" / "preflight_reason.txt").read_text().strip()
    out["preflight_mismatch_detected"] = dict(exit=code, reason=reason, ok=code == 1 and "mismatch" in reason)
    out["all_pass"] = all(v["ok"] for v in out.values() if isinstance(v, dict))
    (HERE / "selftest.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "diagnose":
        r = diagnose(sys.argv[2], sys.argv[3])
        print(json.dumps({k: v for k, v in r.items() if k not in ("chains", "rhat_over_threshold")}, indent=1))
    elif cmd == "summarise":
        summarise(sys.argv[2])
    else:
        {"build": build, "selftest": selftest}[cmd]()
