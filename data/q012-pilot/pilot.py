# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.1.3", "pandas==2.2.3", "cmdstanpy==1.2.4", "arviz==0.20.0", "matplotlib==3.9.2",
#                 "xarray==2024.9.0", "scipy==1.14.1"]
# ///
"""Q-012 bounded kunanyi pilot (Codex 76/1750): package, control tests and screening.

  uv run --python 3.12 data/q012-pilot/pilot.py build                 # hash-bound payload from the frozen seed table
  uv run --python 3.12 data/q012-pilot/pilot.py selftest              # cap, timeout, chain-failure, resume, signal and stale-hash fixtures
  uv run --python 3.12 data/q012-pilot/pilot.py diagnose DIR SCEN     # screening of one fitted attempt directory
  uv run --python 3.12 data/q012-pilot/pilot.py compare A B OUT.json   # mapped comparison of two fits of one dataset

The cluster runs only CmdStan and bash (payload/pbs/); data generation and screening run locally.
"""
import hashlib
import importlib.util
import json
import math
import pathlib
import queue
import shutil
import subprocess
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
PILOT = json.loads((HERE / "pilot.json").read_text())
CAND = PILOT["candidates"][PILOT["active_candidate"]]
PAY = HERE / CAND["payload_dir"]
_spec = importlib.util.spec_from_file_location("prototype", HERE.parent / "q012-prototype" / "prototype.py")
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)
CACHE = P.OUT.parent / "q012-pilot"
RUN_ENV = dict(CHAINS=4, WARMUP=PILOT["sampler"]["iter_warmup"], SAMPLING=PILOT["sampler"]["iter_sampling"],
               ADAPT_DELTA=PILOT["sampler"]["adapt_delta"], MAX_DEPTH=PILOT["sampler"]["max_treedepth"],
               STEPSIZE=PILOT["sampler"]["init_step_size"], SEED=77017, FIT_SECONDS=PILOT["resources"]["fit_seconds"],
               SMOKE_SECONDS=PILOT["resources"]["smoke_seconds"], MODEL_BIN="./" + CAND["stan_file"].removesuffix(".stan"),
               MODULE="HDF5/1.14.0-gompi-2023a", CMDSTAN_VERSION="2.38.0")
RUN_ENV.update(CAND.get("run_env", {}))


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


def write_starts(folder, N, mapped=False):
    """The four prior-centred starts by the declared rule; for a reparameterised candidate, mapped exactly to its coordinates."""
    from cmdstanpy.utils import write_stan_json
    rule = P.CFG[P.CFG["active"]]["inits"]
    folder.mkdir(parents=True, exist_ok=True)
    for k, q in enumerate(P.init_points(rule, rule["seed"], 4, N, rule["perturbation"]), start=1):
        write_stan_json(str(folder / f"chain{k}.json"), P.to_nc(q) if mapped else q)


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
                   and not f.name.endswith((".tar.gz", ".o", ".d")) and f.name != RUN_ENV["MODEL_BIN"][2:]
                   and not (f.name.endswith(".hpp") and f.parent == root))
    (root / "manifest.sha256").write_text("".join(f"{sha(f)}  {f.relative_to(root)}\n" for f in files))
    return len(files)


def cmdstan_tarball():
    """The CmdStan release tarball, downloaded once into scratch; never committed."""
    CACHE.mkdir(parents=True, exist_ok=True)
    tb = CACHE / f"cmdstan-{RUN_ENV['CMDSTAN_VERSION']}.tar.gz"
    if not tb.exists():
        subprocess.run(["curl", "-fsSL", "-o", str(tb), PILOT["runtime"]["cmdstan_url"]], check=True)
    return tb


def data_overrides():
    """The candidate's data changes: its declared fields, and a quadrature order with its Gauss-Hermite nodes and weights."""
    ov = dict(CAND.get("data_overrides", {}))
    if "quadrature_nodes" in CAND:
        t, w = np.polynomial.hermite.hermgauss(CAND["quadrature_nodes"])
        ov.update(Q=int(CAND["quadrature_nodes"]), gh_t=[float(x) for x in t], gh_w=[float(x) for x in w])
    return ov


def build():
    """Build the payload: refuse unless the prototype's checks pass and are bound to the current source and settings."""
    from cmdstanpy.utils import write_stan_json
    ver = P.CFG["active"]
    assert ver == CAND["prototype_version"], f"prototype active version is {ver}"
    chk = json.loads((HERE / CAND["checks_file"]).read_text())
    d_fit, _, _ = P.dataset(P.CFG["fit_seed"])
    assert chk["all_prefit_checks_pass"], "prototype checks have not passed"
    assert chk["binding"] == P.binding(d_fit), "stale prototype checks: rerun prototype.py checks"
    table_sha = sha(HERE / PILOT["scenarios_file"])
    if not (PAY / "pbs").exists():  # a further candidate's package starts from a previous package's runner scripts
        shutil.copytree(HERE / CAND.get("pbs_source", "payload/pbs"), PAY / "pbs")
    if "patch" in CAND:  # observation-only sampler patch (Codex 76/2066), bound to the pinned original
        src = HERE / CAND["patch"]["dir"]
        member = f"cmdstan-{RUN_ENV['CMDSTAN_VERSION']}/{RUN_ENV['PATCH_TARGET']}"
        import tarfile
        with tarfile.open(cmdstan_tarball()) as tf:
            pinned = hashlib.sha256(tf.extractfile(member).read()).hexdigest()
        assert pinned == RUN_ENV["PATCH_ORIGINAL_SHA256"] == sha(src / "base_nuts.orig.hpp"), "patch original differs from the pinned source"
        shutil.rmtree(PAY / "patch", ignore_errors=True)
        (PAY / "patch").mkdir()
        for f in (CAND["patch"]["file"], "base_nuts.diff"):
            shutil.copy(src / f, PAY / "patch" / f)
    for sub in ("data", "inits", "preflight"):
        shutil.rmtree(PAY / sub, ignore_errors=True)
        (PAY / sub).mkdir(parents=True)
    rows = []
    for s in [s for s in scenarios() if CAND["scenarios"] == "all" or s["id"] in CAND["scenarios"]]:
        assert int(s["sampler_seed"]) == RUN_ENV["SEED"]
        ov = dict(lambda0=float(s["lambda0"]), sigma=float(s["sigma"]), rho=float(s["rho"]))
        outcome, d, ginfo, oinfo, secs = generate(int(s["gen_seed"]), ov, PILOT["generator"]["timeout_seconds"])
        row = dict(s, outcome=outcome, generator_seconds=secs, true_lineages=(ginfo or {}).get("true_lineages"))
        if outcome == "ok":
            d = dict(d, **data_overrides())
            write_stan_json(str(PAY / "data" / f"{s['id']}.json"), d)
            write_starts(PAY / "inits" / s["id"], d["N"], "noncentring" in P.CFG[ver])
            row.update(N=d["N"], observation=oinfo, cohort=d["NC"], singles=d["C1"], pairs=d["C2"])
        rows.append(row)
        print(s["id"], outcome, row.get("N"), secs)
    # The replay dataset is the prototype's cost dataset at 64 nodes, and its starts are the frozen v4/v5 files.
    d_r00 = json.loads((PAY / "data" / "R00.json").read_text())
    ref = json.loads(json.dumps(dict(d_fit, **data_overrides()), default=float))
    assert all(np.allclose(np.asarray(d_r00[k], float), np.asarray(ref[k], float), rtol=0, atol=0) for k in ref), "R00 differs"
    for k in range(1, 5):
        assert (PAY / "inits" / "R00" / f"chain{k}.json").read_bytes() == \
            (P.HERE / P.CFG[ver]["inits"]["dir"] / f"chain{k}.json").read_bytes(), "R00 starts differ from the checked starts"
    # Preflight points and their local reference log density and gradients.
    sp = P.stress_points(d_fit)
    if "tail_states" in P.CFG[ver]:
        tail, _, imax = P.v4_states(d_fit)
        pts = dict(central0=sp["central0"], stress_s3_r09_kbm15=sp["stress_s3_r09_kbm15"], max_sigma_v4_state=tail[imax])
    else:
        r00 = P.r00_states(d_fit)
        pts = dict(central0=sp["central0"], stress_s3_r09_kbm15=sp["stress_s3_r09_kbm15"],
                   max_sigma_r00_state=max(r00.values(), key=lambda q: q["sigma"]))
    if "noncentring" in P.CFG[ver]:
        pts = {k: P.to_nc(q) for k, q in pts.items()}
    exe = P.OUT / P.CFG[ver]["stan_file"].removesuffix(".stan")
    for name, q in pts.items():
        write_stan_json(str(PAY / "preflight" / f"point_{name}.json"), q)
        log_prob_csv(exe, PAY / "preflight" / f"point_{name}.json", PAY / "data" / "R00.json",
                     PAY / "preflight" / f"ref_point_{name}.csv")
    if "controls" in CAND:  # deterministic solver controls (Codex 76/1895): one admitted point, one rejected point
        C = CAND["controls"]
        pdir = HERE.parents[1] / C["probe_dir"]
        shutil.copy(pdir / f"{C['accept']}.json", PAY / "preflight" / f"point_control_{C['accept']}.json")
        log_prob_csv(exe, PAY / "preflight" / f"point_control_{C['accept']}.json", PAY / "data" / "R00.json",
                     PAY / "preflight" / f"ref_point_control_{C['accept']}.csv")
        shutil.copy(pdir / f"{C['reject']}.json", PAY / "preflight" / f"reject_control_{C['reject']}.json")
        r = subprocess.run([str(exe), "log_prob", "jacobian=1", f"constrained_params={PAY / 'preflight' / f'reject_control_{C["reject"]}.json'}",
                            "data", f"file={PAY / 'data' / 'R00.json'}", "output", f"file={CACHE / 'reject_control.csv'}", "sig_figs=15"],
                           capture_output=True, text=True)
        assert r.returncode != 0 and "algebra_solver: the norm of the algebraic function" in r.stdout + r.stderr, "reject control was not rejected"
    for row in rows:
        if row["outcome"] == "ok":
            row["starts_initialise"] = start_check(exe, row["id"])
    shutil.copy(P.HERE / P.CFG[ver]["stan_file"], PAY / P.CFG[ver]["stan_file"])
    lines = (HERE / PILOT["scenarios_file"]).read_text().splitlines(keepends=True)
    (PAY / "scenarios.tsv").write_text(lines[0] + "".join(ln for ln in lines[1:] if CAND["scenarios"] == "all"
                                                          or ln.split("\t")[0] in CAND["scenarios"]))
    (PAY / "run.env").write_text("".join(f"{k}={v}\n" for k, v in RUN_ENV.items()))
    fits = CAND.get("fits", [s["id"] for s in scenarios()] if CAND["scenarios"] == "all" else CAND["scenarios"])
    (PAY / "fits.txt").write_text("".join(f"{s}\n" for s in fits))  # the only scenarios stage.sh / submit_fit.sh may submit
    tb = cmdstan_tarball()
    (PAY / "cmdstan.sha256").write_text(f"{sha(tb)}  {tb.name}\n")
    if "same_inputs_as" in CAND:  # a diagnostic replay must use the earlier package's exact data, starts and controls
        other = HERE / PILOT["candidates"][CAND["same_inputs_as"]]["payload_dir"]
        quad = {"Q", "gh_t", "gh_w"} if "quadrature_nodes" in CAND else set()
        for sub in ("data", "inits", "preflight"):
            mine = sorted(f.relative_to(PAY) for f in (PAY / sub).rglob("*") if f.is_file())
            theirs = sorted(f.relative_to(other) for f in (other / sub).rglob("*") if f.is_file())
            assert mine == theirs, f"{sub} file lists differ from {other.name}"
            for f in mine:
                if sub == "data":  # identical apart from the declared quadrature fields
                    a, b = json.loads((PAY / f).read_text()), json.loads((other / f).read_text())
                    assert set(a) == set(b) and all(a[k] == b[k] for k in a if k not in quad), f"{f} differs beyond {sorted(quad)}"
                elif quad and f.name.startswith("ref_"):  # order-dependent references are regenerated (Codex 76/2096)
                    continue
                else:
                    body = lambda x: [ln for ln in x.read_text().splitlines() if not ln.startswith("#")] if x.suffix == ".csv" else x.read_bytes()
                    assert body(PAY / f) == body(other / f), f"{f} differs from {other.name}"
        assert (PAY / CAND["stan_file"]).read_bytes() == (other / CAND["stan_file"]).read_bytes()
    nfiles = write_manifest(PAY)
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=HERE).stdout.strip()
    man = dict(created=time.strftime("%Y-%m-%dT%H:%M:%S%z"), git_head_at_build=head, files=nfiles,
               manifest_sha256=sha(PAY / "manifest.sha256"), pilot_json_sha256=sha(HERE / "pilot.json"),
               scenario_table=dict(file=PILOT["scenarios_file"], sha256=table_sha, frozen_commit="c93ea58"),
               candidate=PILOT["active_candidate"],
               prototype_checks=dict(file=CAND["checks_file"], sha256=sha(HERE / CAND["checks_file"]),
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
    s = (f"chains {e['CHAINS']}; warmup {e['WARMUP']}; sampling {e['SAMPLING']}; adapt_delta {e['ADAPT_DELTA']}; "
         f"max_depth {e['MAX_DEPTH']}; stepsize {e['STEPSIZE']}; seed {e['SEED']}; fit_seconds {e['FIT_SECONDS']}")
    s += f"; refresh {e['REFRESH']}; log {e['LOG_FORMAT']}" if "LOG_FORMAT" in e else ""
    return s + (f"; trace {e['TRACE_SCHEMA']} caps {e['TRACE_CAP_WARMUP']}/{e['TRACE_CAP_SAMPLING']}" if "TRACE_SCHEMA" in e else "")


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


import re

LOG_RE = dict(
    grad=re.compile(r"^Gradient evaluation took [0-9.e+-]+ seconds$"),
    trans=re.compile(r"^\d+ transitions using \d+ leapfrog steps per transition would take [0-9.e+-]+ seconds\.$"),
    iteration=re.compile(r"^Iteration:\s+(\d+) / (\d+) \[\s*\d+%\]\s+\((Warmup|Sampling)\)$"),
    elapsed1=re.compile(r"^ Elapsed Time: [0-9.e+-]+ seconds \(Warm-up\)$"),
    elapsed2=re.compile(r"^\s+[0-9.e+-]+ seconds \(Sampling\)$"),
    elapsed3=re.compile(r"^\s+[0-9.e+-]+ seconds \(Total\)$"))
LOG_FIXED = dict(
    adjust="Adjust your expectations accordingly!",
    warn20a="WARNING: No variance estimation is", warn20b="         performed for num_warmup < 20",
    rej="Informational Message: The current Metropolis proposal is about to be rejected because of the following issue:",
    rej3="If this warning occurs sporadically, such as for highly constrained variable types like covariance matrices, then the sampler is fine,",
    rej4="but if this warning occurs often then your model may be either severely ill-conditioned or misspecified.",
    init="Rejecting initial value:", init_eval="  Error evaluating the log probability at the initial value.",
    init_log0="  Log probability evaluates to log(0), i.e. negative infinity.",
    init_grad="  Gradient evaluated at the initial value is not finite.",
    init_cant="  Stan can't start sampling from this initial value.")
RECOGNISED_CAUSES = {"input", "solver", "hessian", "factorisation", "solver_internal"}


def expected_header(env, scen, k, csv_rel):
    """The exact CmdStan 2.38 configuration echo of fit.sh's command line for chain k (Codex 76/2066: no free-form
    startup lines). CmdStan marks a value '(Default)' when it equals the default, whether or not it was given."""
    dflt = lambda v, default: f"{v} (Default)" if str(v) == str(default) else str(v)
    return ["method = sample (Default)", "  sample", f"    num_samples = {dflt(env['SAMPLING'], 1000)}",
            f"    num_warmup = {dflt(env['WARMUP'], 1000)}", "    save_warmup = false (Default)", "    thin = 1 (Default)",
            "    adapt", "      engaged = true (Default)", "      gamma = 0.05 (Default)",
            f"      delta = {dflt(env['ADAPT_DELTA'], 0.8)}", "      kappa = 0.75 (Default)", "      t0 = 10 (Default)",
            "      init_buffer = 75 (Default)", "      term_buffer = 50 (Default)", "      window = 25 (Default)",
            "      save_metric = false (Default)", "    algorithm = hmc (Default)", "      hmc", "        engine = nuts (Default)",
            "          nuts", f"            max_depth = {dflt(env['MAX_DEPTH'], 10)}", "        metric = diag_e (Default)",
            "        metric_file =  (Default)", f"        stepsize = {dflt(env['STEPSIZE'], 1)}",
            "        stepsize_jitter = 0 (Default)", "    num_chains = 1 (Default)", f"id = {dflt(k, 1)}", "data",
            f"  file = data/{scen}.json", f"init = inits/{scen}/chain{k}.json", "random", f"  seed = {env['SEED']}", "output",
            f"  file = {csv_rel}", "  diagnostic_file =  (Default)", f"  refresh = {dflt(env['REFRESH'], 100)}",
            "  sig_figs = 8 (Default)", "  profile_file = profile.csv (Default)", "  save_cmdstan_config = false (Default)",
            "num_threads = 1 (Default)"]


_NUM = r"-?(?:inf|nan|\d+(?:\.\d+)?(?:e[-+]?\d+)?)"


def rejection_grammar(stan_file, data_file):
    """Exact rejection-message grammar (Codex 76/2066: no keyword classifier). Each recognised message is one of the
    model's labelled reject() statements, with its declared value form, or one of the two Powell failures with the
    payload's own tolerance or step limit; the innermost source location must be that statement's line in the
    compiled model file. Returns a function line -> cause, or None when unrecognised."""
    text = pathlib.Path(stan_file).read_text().splitlines()
    name = re.escape(pathlib.Path(stan_file).name)
    data = json.loads(pathlib.Path(data_file).read_text())
    loc = rf"((?: \(in '\.\./{name}', line \d+, column \d+ to (?:line \d+, )?column \d+\))+)$"
    val = rf"(?:{_NUM}|\[{_NUM}(?:,{_NUM})*\])"
    rules = []
    for i, ln in enumerate(text, 1):
        m = re.search(r'reject\("(Q012 (input|solver|Hessian|factorisation) failure: [^"]*)"(\s*,[^;]*)?\);', ln)
        if m:
            rules.append((re.compile("^Exception: Exception: " + re.escape(m.group(1)) + (val if m.group(3) else "") + loc),
                          m.group(2).lower(), {i}, None))
    powell = {i for i, ln in enumerate(text, 1) if "solve_powell_tol(" in ln}
    rules.append((re.compile(rf"^Exception: Exception: algebra_solver: the norm of the algebraic function is {_NUM} but should "
                             rf"be lower than the function tolerance: ({_NUM})\. Consider decreasing the relative tolerance and "
                             rf"increasing max_num_steps\." + loc), "solver_internal", powell,
                  lambda g: float(g) == float(data["solver_f_tol"])))
    rules.append((re.compile(r"^Exception: Exception: algebra_solver: maximum number of iterations \((\d+)\) was exceeded in "
                             r"the solve\." + loc), "solver_internal", powell, lambda g: int(g) == int(data["solver_max_steps"])))

    def cause(line):
        for rx, c, where, check in rules:
            m = rx.match(line)
            if not m:
                continue
            first = int(re.match(r" \(in '[^']*', line (\d+)", m.group(m.lastindex)).group(1))
            if first in where and (check is None or check(m.group(1))):
                return c
        return None
    return cause


def parse_log(text, warmup, sampling, header, cause):
    """Fail-closed parse of one combined, ordered CmdStan sample log (stdout and stderr on one file, refresh = 1).
    Returns (failures, rejections). A failure is any departure from the exact expected header, any unrecognised or
    malformed line, an incomplete rejection envelope, a rejection message outside the exact grammar (cause), a missing,
    repeated, out-of-order or mislabelled iteration marker, or a missing completion block. Each rejection records its
    phase (init, stepsize_init, warmup, sampling) and transition."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    fails, rej = [], []
    total = warmup + sampling
    state, expect, cur, i = "init", 1, None, 0
    h = 0
    while i < len(lines) and h < len(header):
        if lines[i].strip():
            if lines[i] != header[h]:
                fails.append(f"line {i + 1}: header line {lines[i][:120]!r}; expected {header[h]!r}")
            h += 1
        i += 1
    if h < len(header):
        fails.append(f"header ends after {h} of {len(header)} lines")

    def phase():
        return {"init": "init", "prewarm": "stepsize_init"}.get(state, cur[1] if cur else "unknown")
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln == LOG_FIXED["init"]:
            if state != "init":
                fails.append(f"line {i + 1}: initial-value rejection after initialisation")
            state = "init"
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if nxt == LOG_FIXED["init_eval"] and i + 2 < len(lines) and lines[i + 2].startswith("Exception: "):
                c = cause(lines[i + 2])
                rej.append(dict(phase="init", transition=None, cause=c, message=lines[i + 2][:200]))
                if c not in RECOGNISED_CAUSES:
                    fails.append(f"line {i + 3}: unrecognised initial-value rejection cause: {lines[i + 2][:120]!r}")
                i += 3
            elif nxt in (LOG_FIXED["init_log0"], LOG_FIXED["init_grad"]) and i + 2 < len(lines) and lines[i + 2] == LOG_FIXED["init_cant"]:
                rej.append(dict(phase="init", transition=None, cause="init_nonfinite", message=nxt.strip()))
                i += 3
            else:
                fails.append(f"line {i + 1}: incomplete initial-value rejection envelope")
                i += 1
            continue
        if LOG_RE["grad"].match(ln) or LOG_RE["trans"].match(ln) or ln == LOG_FIXED["adjust"]:
            if state not in ("init", "prewarm"):
                fails.append(f"line {i + 1}: gradient-timing block out of place")
            state = "prewarm"
            i += 1
            continue
        if ln == LOG_FIXED["warn20a"]:
            if not (i + 1 < len(lines) and lines[i + 1] == LOG_FIXED["warn20b"] and warmup < 20 and state == "prewarm"):
                fails.append(f"line {i + 1}: unexpected low-warmup warning")
            i += 2
            continue
        m = LOG_RE["iteration"].match(ln)
        if m:
            k, n, lab = int(m.group(1)), int(m.group(2)), m.group(3)
            want = "Warmup" if k <= warmup else "Sampling"
            if state not in ("prewarm", "iter") or k != expect or n != total or lab != want:
                fails.append(f"line {i + 1}: iteration marker {k}/{n} ({lab}); expected {expect}/{total} ({want if k == expect else ''})")
            state, cur, expect = "iter", (k, lab.lower()), k + 1
            i += 1
            continue
        if ln == LOG_FIXED["rej"]:
            ok = (i + 3 < len(lines) and lines[i + 1].startswith("Exception: ") and lines[i + 2] == LOG_FIXED["rej3"]
                  and lines[i + 3] == LOG_FIXED["rej4"])
            if not ok:
                fails.append(f"line {i + 1}: incomplete rejection envelope")
                i += 1
                continue
            c = cause(lines[i + 1])
            ph = phase()
            if ph in ("init",):
                ph = "stepsize_init"
            rej.append(dict(phase=ph, transition=cur[0] if (cur and state == "iter") else None, cause=c, message=lines[i + 1][:200]))
            if c not in RECOGNISED_CAUSES:
                fails.append(f"line {i + 2}: unrecognised rejection cause: {lines[i + 1][:120]!r}")
            if state not in ("prewarm", "iter"):
                fails.append(f"line {i + 1}: rejection envelope before initialisation completed")
            i += 4
            continue
        if LOG_RE["elapsed1"].match(ln):
            if not (state == "iter" and expect == total + 1 and i + 2 < len(lines) and LOG_RE["elapsed2"].match(lines[i + 1])
                    and LOG_RE["elapsed3"].match(lines[i + 2])):
                fails.append(f"line {i + 1}: completion block out of place or malformed")
            state = "done"
            i += 3
            continue
        fails.append(f"line {i + 1}: unrecognised line {ln[:120]!r}")
        i += 1
    if state != "done":
        fails.append(f"no completion block; last marker {cur}")
    if expect != total + 1:
        fails.append(f"iteration markers end at {expect - 1}, expected {total}")
    return fails, rej


def payload_grammar(scen):
    """The rejection grammar for a scenario of the active payload."""
    return rejection_grammar(PAY / CAND["stan_file"], PAY / "data" / f"{scen}.json")


def qualify(attempt, scen, env, manifest_sha, build_receipt, grammar=None):
    """Structural qualification of one attempt, before any statistics. Returns the list of failures (empty if it qualifies).
    A diagnostic trace sidecar (TRACE_SCHEMA in run.env) is an expected file; its validity is checked separately."""
    attempt = pathlib.Path(attempt)
    fails = []
    if not (attempt / "receipt.txt").exists():
        return ["no receipt"]
    rc = _receipt(attempt / "receipt.txt")
    bh = build_receipt.get("binary_sha256") or ""
    if not (len(bh) == 64 and all(ch in "0123456789abcdef" for ch in bh)):
        fails.append(f"build receipt has no valid binary hash ({bh!r})")
    want = dict(scenario=scen, attempt=attempt.name.removeprefix("attempt"), status="complete", manifest_sha256=manifest_sha,
                binary_sha256=build_receipt.get("binary_sha256"), settings=settings_line(env))
    fails += [f"receipt {k} is {rc.get(k)!r}, expected {v!r}" for k, v in want.items() if rc.get(k) != v]
    if build_receipt.get("status") != "ok":
        fails.append(f"build receipt status is {build_receipt.get('status')!r}")
    if build_receipt.get("manifest_sha256") != manifest_sha:
        fails.append("build receipt is for a different payload manifest")
    C = int(env["CHAINS"])
    combined = env.get("LOG_FORMAT") == "combined"
    streams = ("log",) if combined else ("stdout", "stderr")
    expected = {f"chain{k}.{x}" for k in range(1, C + 1) for x in ("csv", "exit") + streams
                + (("trace.jsonl",) if "TRACE_SCHEMA" in env else ())}
    if combined:
        grammar = grammar or payload_grammar(scen)
    present = {f.name for f in attempt.iterdir()}
    fails += [f"missing {n}" for n in sorted(expected - present)]
    fails += [f"unexpected output file {n}" for n in sorted(present)
              if (n.endswith((".csv", ".stdout", ".stderr", ".log", ".exit", ".jsonl")) and n not in expected)
              or (n.endswith(".time") and n.removesuffix(".time") + ".csv" not in expected)]
    for k in range(1, C + 1):
        c = attempt / f"chain{k}"
        if not all((attempt / f"chain{k}.{x}").exists() for x in ("csv", "exit") + streams):
            continue
        if (attempt / f"chain{k}.exit").read_text().strip() != "0" or rc.get(f"chain{k}_exit") != "0":
            fails.append(f"chain {k} exit {(attempt / f'chain{k}.exit').read_text().strip()!r}")
        if combined:
            lf, _ = parse_log((attempt / f"chain{k}.log").read_text(errors="replace"), int(env["WARMUP"]), int(env["SAMPLING"]),
                              expected_header(env, scen, k, f"runs/{scen}/{attempt.name}/chain{k}.csv"), grammar)
            fails += [f"chain {k} log: {x}" for x in lf]
        else:
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
                mcse_target_met=(max(m05, m95) <= D["mcse_target"]) if ends and prec else None, truth=truth,
                interval_covers_truth=(q05 <= truth <= q95) if ends and truth is not None else None,
                D=(q05 > D["eta0"]) if ends else None, X=(q95 < D["eta1"]) if ends else None,
                D_numerically_uncertain=(q05 - 2 * m05 < D["eta0"] < q05 + 2 * m05) if ends and prec else None,
                X_numerically_uncertain=(q95 - 2 * m95 < D["eta1"] < q95 + 2 * m95) if ends and prec else None)


def statistics(csvs, outs, truth, env=None, scen=None, grammar=None):
    """Screening statistics on chain files of equal, already verified length. With a combined log format (env
    LOG_FORMAT=combined) the per-chain logs of scenario scen are parsed for phase-attributed rejections; otherwise
    stdout only."""
    import arviz as az
    import pandas as pd
    S = PILOT["screening"]
    dfs = [pd.read_csv(c, comment="#") for c in csvs]
    assert len({len(x) for x in dfs}) == 1, "unequal chain lengths"
    arr = lambda col: np.stack([x[col].to_numpy() for x in dfs])
    chains = []
    combined = bool(env) and env.get("LOG_FORMAT") == "combined"
    if combined:
        grammar = grammar or payload_grammar(scen)
    for k, (c, o, x) in enumerate(zip(csvs, outs, dfs), start=1):
        if combined:
            lf, rl = parse_log(pathlib.Path(o).read_text(errors="replace"), int(env["WARMUP"]), int(env["SAMPLING"]),
                               expected_header(env, scen, k, f"runs/{scen}/{pathlib.Path(o).parent.name}/chain{k}.csv"), grammar)
            rej = {}
            for r in rl:
                rej[f"{r['cause']}_{r['phase']}"] = rej.get(f"{r['cause']}_{r['phase']}", 0) + 1
            fatal = [dict(message=f) for f in lf]
            extra = dict(rejection_events=rl, log_parse="complete" if not lf else "failed")
        else:
            rej, fatal = stdout_record(pathlib.Path(o).read_text(errors="replace"))
            se = pathlib.Path(o).with_suffix(".stderr")
            extra = dict(log_parse="stdout only", stderr_nonempty=se.exists() and bool(se.read_text(errors="replace").strip()))
        chains.append(dict(csv=pathlib.Path(c).name, draws=len(x), divergences=int(x["divergent__"].sum()),
                           depth_hits=int((x["treedepth__"] >= PILOT["sampler"]["max_treedepth"]).sum()),
                           ebfmi=ebfmi(x["energy__"].to_numpy()), rejections=rej, fatal=fatal,
                           sampling_phase_rejections=sum(v for k, v in rej.items() if k.endswith("_sampling")), **extra))
    cols = [c for c in dfs[0].columns if not c.endswith("__") or c == "lp__"]
    rhat = {c: float(az.rhat(arr(c))) for c in cols}
    ess = {c: dict(bulk=float(az.ess(arr(c), method="bulk")), tail=float(az.ess(arr(c), method="tail"))) for c in S["core"]}
    eta = arr("eta")
    q05, q95 = (float(v) for v in np.quantile(eta.ravel(), [0.05, 0.95]))
    m05, m95 = float(az.mcse(eta, method="quantile", prob=0.05)), float(az.mcse(eta, method="quantile", prob=0.95))
    crit = dict(
        zero_post_warmup_divergences=sum(c["divergences"] for c in chains) == S["post_warmup_divergences"],
        no_fatal_or_sampling_phase_failures=(not any(c["fatal"] or c["sampling_phase_rejections"] for c in chains))
        if combined or not any(c.get("stderr_nonempty") for c in chains) else None,  # separate stderr: phase unknown
        ebfmi_each_chain=all(_finite(c["ebfmi"]) and c["ebfmi"] >= S["ebfmi_min_per_chain"] for c in chains),
        rhat_all=rhat_pass(rhat), ess_bulk_tail_core=ess_pass(ess))
    worst = sorted(rhat.items(), key=lambda kv: -kv[1] if _finite(kv[1]) else -np.inf)
    verdict = False if any(v is False for v in crit.values()) else None if any(v is None for v in crit.values()) else True
    return dict(chains=chains, screening=crit, screening_pass=verdict, rhat_max=worst[0],
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


def read_trace(path):
    """The JSON lines of one trace sidecar (non-finite numbers as NaN / Infinity tokens)."""
    return [json.loads(ln) for ln in pathlib.Path(path).read_text().splitlines()]


def trace_structure(attempt, env, k):
    """Validity of chain k's divergence trace (Codex 76/2066): header bound to run.env, every divergence recorded once in
    transition order with its phase, full records for exactly the first cap events of each phase, the summary's counts
    and write status, full-record vector lengths, and the sampling events equal to the CSV's divergent draws. Returns
    (failures, summary). Any failure invalidates the diagnostic capture, never the sampler output."""
    import pandas as pd
    attempt = pathlib.Path(attempt)
    f = attempt / f"chain{k}.trace.jsonl"
    if not f.exists():
        return [f"chain {k}: no trace file"], None
    try:
        rows = read_trace(f)
    except ValueError as e:
        return [f"chain {k}: malformed trace line ({e})"], None
    fails = []
    W, S = int(env["WARMUP"]), int(env["SAMPLING"])
    caps = dict(warmup=int(env["TRACE_CAP_WARMUP"]), sampling=int(env["TRACE_CAP_SAMPLING"]))
    df = pd.read_csv(attempt / f"chain{k}.csv", comment="#")
    cols = list(df.columns)
    dim = cols.index([c for c in cols if c.startswith("w.")][-1]) - cols.index("log_h0_1") + 1
    want = dict(type="header", schema=env["TRACE_SCHEMA"], chain=k, warmup=W, cap_warmup=caps["warmup"],
                cap_sampling=caps["sampling"], max_deltaH=1000, max_depth=int(env["MAX_DEPTH"]), dim=dim, metric="diag_e",
                config_ok=True)
    head = rows[0] if rows else {}
    fails += [f"chain {k}: header {key} is {head.get(key)!r}, expected {v!r}" for key, v in want.items() if head.get(key) != v]
    tail = rows[-1] if len(rows) > 1 else {}
    if tail.get("type") != "summary":
        fails.append(f"chain {k}: no summary line")
    events = rows[1:-1] if tail.get("type") == "summary" else rows[1:]
    seen, cap, last = dict(warmup=0, sampling=0), dict(warmup=0, sampling=0), 0
    for e in events:
        if e.get("type") != "divergence" or e.get("chain") != k:
            fails.append(f"chain {k}: unexpected trace record {str(e)[:80]}")
            continue
        t, ph = e["transition"], e["phase"]
        if not (last < t <= W + S) or ph != ("warmup" if t <= W else "sampling"):
            fails.append(f"chain {k}: event at transition {t} labelled {ph} out of order or mislabelled")
        last = t
        seen[ph] += 1
        full = all(x in e for x in ("initial", "previous", "failing", "inv_metric"))
        if e["phase_event"] != seen[ph] or e["captured"] != (seen[ph] <= caps[ph]) or full != e["captured"]:
            fails.append(f"chain {k}: capture flags wrong at transition {t}")
        cap[ph] += full
        if not e["H_effective"] - e["H0"] > e["max_deltaH"]:
            fails.append(f"chain {k}: event at transition {t} does not exceed the divergence threshold")
        if not (e["H_effective"] == e["H_raw"] or (math.isnan(e["H_raw"]) and e["H_effective"] == math.inf)):
            fails.append(f"chain {k}: effective H differs from raw H at transition {t}")
        if full and not (len(e["inv_metric"]) == dim and all(len(e[s][v]) == dim for s in ("initial", "previous", "failing")
                                                              for v in ("q", "p", "grad_V"))):
            fails.append(f"chain {k}: full record at transition {t} has wrong vector lengths")
    want_tail = dict(type="summary", transitions=W + S, seen_warmup=seen["warmup"], captured_warmup=cap["warmup"],
                     dropped_warmup=seen["warmup"] - cap["warmup"], seen_sampling=seen["sampling"],
                     captured_sampling=cap["sampling"], dropped_sampling=seen["sampling"] - cap["sampling"], write_ok=True)
    if tail.get("type") == "summary":
        fails += [f"chain {k}: summary {key} is {tail.get(key)!r}, expected {v!r}" for key, v in want_tail.items() if tail.get(key) != v]
    csv_div = [W + 1 + int(i) for i in np.flatnonzero(df["divergent__"].to_numpy() == 1)]
    trace_div = [e["transition"] for e in events if e.get("phase") == "sampling"]
    if csv_div != trace_div:
        fails.append(f"chain {k}: sampling events {trace_div[:8]} differ from CSV divergent transitions {csv_div[:8]}")
    return fails, dict(seen=seen, captured=cap, sampling_transitions=trace_div,
                       warmup_transitions=[e["transition"] for e in events if e.get("phase") == "warmup"])


def diagnose(attempt, scen, env=None, manifest_sha=None, build_receipt=None, write=True, grammar=None):
    """Pilot qualification and screening of one fetched attempt (Codex 76/1750, 76/1765). Structural failures leave the
    fit unresolved and no statistics are computed. Defaults: the local payload's run.env and manifest, and the build
    receipt fetched with the run (<fetch root>/build/receipt.txt). A traced attempt also reports its capture validity;
    a diagnostic candidate's screening is descriptive only (Codex 76/2066)."""
    attempt = pathlib.Path(attempt)
    env = env or RUN_ENV
    manifest_sha = manifest_sha or sha(PAY / "manifest.sha256")
    if build_receipt is None:
        br = attempt.parents[2] / "build" / "receipt.txt"
        build_receipt = _receipt(br) if br.exists() else {}
    fails = qualify(attempt, scen, env, manifest_sha, build_receipt, grammar)
    truth = next((float(s["eta"]) for s in scenarios() if s["id"] == scen), None)
    res = dict(scenario=scen, attempt=str(attempt), qualified=not fails, qualification_failures=fails)
    if "replay_bank" in CAND:
        res["kind"] = "instrumented diagnostic attempt: not a four-chain qualification or a dataset replicate"
    if "TRACE_SCHEMA" in env:
        cf, cs = [], {}
        for k in range(1, int(env["CHAINS"]) + 1):
            if (attempt / f"chain{k}.csv").exists():
                f, sm = trace_structure(attempt, env, k)
                cf += f
                cs[f"chain{k}"] = sm
            else:
                cf.append(f"chain {k}: no CSV")
        res["capture"] = dict(valid=not cf, failures=cf, chains=cs)
    if fails:
        res.update(status="unresolved", screening_pass=None)
    else:
        C = int(env["CHAINS"])
        st = statistics([attempt / f"chain{k}.csv" for k in range(1, C + 1)],
                        [attempt / f"chain{k}.{'log' if env.get('LOG_FORMAT') == 'combined' else 'stdout'}" for k in range(1, C + 1)],
                        truth, env, scen, grammar)
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


REF_TOL = dict(value=1e-6, derivative=1e-5)  # a reference is converged when doubling its resolution moves it less than this


def _steps(q):
    return dict(sigma=min(1e-4, q["sigma"] / 2), rho=min(1e-4, q["rho"] / 2, (1 - q["rho"]) / 2), kappa_b=1e-4, log_k=1e-4,
                log_h0_1=1e-4)


def _lse(x):
    m = float(np.max(x))
    return m + math.log(float(np.exp(x - m).sum()))


def local_reference(d, q, n=1600, L=16.0):
    """Log cohort normaliser by Simpson integration on a grid centred and scaled at each Newton mode (2-D in 64-row
    chunks). Independent of the data's quadrature nodes; resolves narrow modes the fixed-innovation reference misses."""
    sig, rho, kb = q["sigma"], q["rho"], q["kappa_b"]
    A = P.cohort_A(d, q)
    b0 = math.exp(q["log_b0"])
    s2h = 0.5 * sig * sig
    e = np.linspace(-L, L, n + 1)
    wt = np.ones(n + 1)
    wt[1:-1:2], wt[2:-1:2] = 4, 2
    lw = np.log(wt * 2 * L / (3 * n))
    ls = lambda x, a, b: -a * np.exp(x - s2h) - b * np.exp(kb * (x - s2h))

    def mode(aa, bb, inv):
        a, b, y = np.array(aa), np.array(bb), np.zeros(len(aa))
        for _ in range(200):
            ep, eb = a * np.exp(y - s2h), b * np.exp(kb * (y - s2h))
            Pm = inv + np.diag(ep + kb * kb * eb)
            dlt = np.linalg.solve(Pm, -inv @ y - ep - kb * eb)
            y = y + dlt
            if np.max(np.abs(dlt)) < 1e-14:
                break
        ep, eb = a * np.exp(y - s2h), b * np.exp(kb * (y - s2h))
        return y, np.linalg.cholesky(np.linalg.inv(inv + np.diag(ep + kb * kb * eb)))
    out = 0.0
    for ii in d["c1_lin"]:
        i = ii - 1
        a, b = A[i], b0 * (d["c"] - d["o"][i])
        m, T = mode([a], [b], np.array([[1 / sig ** 2]]))
        x = m[0] + T[0, 0] * e
        out += math.log(T[0, 0]) + _lse(lw + ls(x, a, b) - 0.5 * x * x / sig ** 2 - math.log(sig) - 0.5 * math.log(2 * math.pi))
    for ip, idd in zip(d["c2_par"], d["c2_dau"]):
        ip, idd = ip - 1, idd - 1
        aa, bb = [A[ip], A[idd]], [b0 * (d["c"] - d["o"][k]) for k in (ip, idd)]
        inv = np.linalg.inv(sig ** 2 * np.array([[1, rho], [rho, 1]]))
        m, T = mode(aa, bb, inv)
        logs = []
        for s in range(0, n + 1, 64):
            e1, e2 = e[s:s + 64, None], e[None, :]
            xp = m[0] + T[0, 0] * e1
            xd = m[1] + T[1, 0] * e1 + T[1, 1] * e2
            arr = (lw[s:s + 64, None] + lw[None, :] + ls(xp, aa[0], bb[0]) + ls(xd, aa[1], bb[1])
                   - 0.5 * (inv[0, 0] * xp * xp + 2 * inv[0, 1] * xp * xd + inv[1, 1] * xd * xd)
                   - math.log(2 * math.pi) - 2 * math.log(sig) - 0.5 * math.log(1 - rho * rho))
            logs.append(_lse(arr))
        out += math.log(T[0, 0] * T[1, 1]) + _lse(np.array(logs))
    return out


def _axes(d, extra=()):
    return ("sigma", "kappa_b") + (("rho",) if d["C2"] else ()) + tuple(extra)


def _values(d, q, f, extra=()):
    """Value and central-difference derivatives (domain-safe steps) of a normaliser function f(q), on sigma, kappa_b,
    rho (when there are pairs) and any extra axes (log_k, log_h0_1)."""
    hs = _steps(q)
    v = dict(value=f(q))
    for name in _axes(d, extra):
        h = hs[name]
        v[name] = (f(dict(q, **{name: q[name] + h})) - f(dict(q, **{name: q[name] - h}))) / (2 * h)
    return v


def _converged(a, b):
    ch = {k: b[k] - a[k] for k in a}
    return dict(value_change=float(ch["value"]), derivative_changes={k: float(v) for k, v in ch.items() if k != "value"},
                converged=bool(abs(ch["value"]) <= REF_TOL["value"]
                               and all(abs(v) <= REF_TOL["derivative"] for k, v in ch.items() if k != "value")))


def reference_convergence(d, q, extra=()):
    """Signed change of the fixed-innovation Simpson reference itself (value and derivatives), 1,600 -> 3,200 intervals."""
    ref = lambda n: (lambda p: P.log_norm_ref(d, p, P.cohort_A(d, p), n))
    return _converged(_values(d, q, ref(1600), extra), _values(d, q, ref(3200), extra))


def gate_point(d, q, extra=()):
    """The data's Q-node normaliser (order d["Q"]) against a converged reference at one joint state: value and
    derivatives on sigma, kappa_b, rho and any extra axes, with domain-safe steps. The fixed-innovation Simpson reference
    is used when it converges; otherwise the local-mode reference; if neither converges the state is unresolved, never
    passed."""
    agh = _values(d, q, lambda p: P.log_norm_agh(d, p, P.cohort_A(d, p)), extra)
    coarse = reference_convergence(d, q, extra)
    used, ref = "fixed_innovation_n1600", None
    if coarse["converged"]:
        ref = _values(d, q, lambda p: P.log_norm_ref(d, p, P.cohort_A(d, p), 1600), extra)
    else:
        a = _values(d, q, lambda p: local_reference(d, p, 800, 12.0), extra)
        b = _values(d, q, lambda p: local_reference(d, p, 1600, 12.0), extra)
        c = _values(d, q, lambda p: local_reference(d, p, 1600, 16.0), extra)
        loc = dict(resolution=_converged(a, b), domain=_converged(b, c))
        if loc["resolution"]["converged"] and loc["domain"]["converged"]:
            used, ref = "local_mode_n1600_L16", c
        coarse["local"] = loc
    res = dict(quadrature_order=int(d["Q"]), h={k: v for k, v in _steps(q).items() if k in _axes(d, extra)},
               reference=used if ref else "unresolved", reference_convergence=coarse)
    if ref is None:
        res["pass"] = None
        return res
    res["log_err"] = abs(agh["value"] - ref["value"])
    for k in agh:
        if k != "value":
            res[f"d_{k}_err"] = abs(agh[k] - ref[k])
    res["pass"] = bool(res["log_err"] <= 1e-4 and all(v <= 1e-3 for k, v in res.items() if k.startswith("d_")))
    return res


def joint_checks(fit_dir, data_file):
    """Direct checks of the data's Q-node normaliser at selected joint states of one fit (Codex 76/1855): six highest
    sigma, largest |kappa_b|, smallest and largest rho, and 40 evenly spaced draws; reference convergence at the largest
    log error; and the lower tail of sigma per chain. An unperformed check is reported as not tested."""
    import pandas as pd
    d = json.loads(pathlib.Path(data_file).read_text())
    dfs = [pd.read_csv(pathlib.Path(fit_dir) / f"chain{k}.csv", comment="#") for k in range(1, 5)]
    df = pd.concat(dfs, ignore_index=True)
    sel = list(dict.fromkeys([int(i) for i in df.nlargest(6, "sigma").index]
                             + [int(df.kappa_b.abs().idxmax()), int(df.rho.idxmin()), int(df.rho.idxmax())]
                             + [int(i) for i in np.linspace(0, len(df) - 1, 40).astype(int)]))
    states = {i: P.draw_to_params(df.iloc[i], d["N"]) for i in sel}
    gates = {str(i): dict(sigma=float(q["sigma"]), rho=float(q["rho"]), kappa_b=float(q["kappa_b"]), **gate_point(d, q))
             for i, q in states.items()}
    tested = {k: g for k, g in gates.items() if g["pass"] is not None}
    worst = max(tested, key=lambda k: tested[k]["log_err"]) if tested else None
    lower = [dict(chain=k, q001=float(x.sigma.quantile(0.001)), q01=float(x.sigma.quantile(0.01)), min=float(x.sigma.min()),
                  mass_below_0_1=float((x.sigma < 0.1).mean()), mass_below_0_01=float((x.sigma < 0.01).mean()))
             for k, x in enumerate(dfs, start=1)]
    unresolved = [k for k, g in gates.items() if g["pass"] is None]
    verdict = (None if not gates or unresolved else all(g["pass"] for g in gates.values()))
    return dict(quadrature_order=int(d["Q"]), states_selected=len(gates), states_with_converged_reference=len(tested),
                unresolved_states=unresolved,
                status="tested" if gates else "not tested", all_pass=verdict,
                max_log_err=max((g["log_err"] for g in tested.values()), default=None),
                max_derivative_err=max((v for g in tested.values() for k, v in g.items() if k.startswith("d_") and k.endswith("_err")),
                                       default=None),
                worst_state=worst, reference_convergence_at_worst=(gates[worst]["reference_convergence"] if worst else "not tested"),
                states=gates, sigma_lower_tail=lower)


def compare(dir_a, dir_b, out_file, data_file=None):
    """Mapped comparison of two qualified fits of the same dataset (Codex 76/1814): core summaries and eta endpoints with
    chain-preserving MCSEs (descriptive z under zero cross-fit covariance), per-chain cost, and direct joint-state Q = 64
    checks on B (Codex 76/1855; marginal ranges do not establish joint-state accuracy)."""
    import arviz as az
    import pandas as pd
    S = PILOT["screening"]
    load = lambda d: [pd.read_csv(pathlib.Path(d) / f"chain{k}.csv", comment="#") for k in range(1, 5)]
    A, B = load(dir_a), load(dir_b)
    arr = lambda dfs, c: np.stack([x[c].to_numpy() for x in dfs])
    rows = {}
    for c in S["core"]:
        r = {}
        for lab, dfs in (("a", A), ("b", B)):
            x = arr(dfs, c)
            r[lab] = dict(mean=float(x.mean()), sd=float(x.std()), mcse_mean=float(az.mcse(x, method="mean")),
                          q05=float(np.quantile(x, 0.05)), q50=float(np.quantile(x, 0.5)), q95=float(np.quantile(x, 0.95)),
                          mcse_q05=float(az.mcse(x, method="quantile", prob=0.05)),
                          mcse_q95=float(az.mcse(x, method="quantile", prob=0.95)))
        z = lambda k, m: (r["b"][k] - r["a"][k]) / math.hypot(r["a"][m], r["b"][m])
        r["z_mean"], r["z_q05"], r["z_q95"] = z("mean", "mcse_mean"), z("q05", "mcse_q05"), z("q95", "mcse_q95")
        rows[c] = r
    cost = {lab: [dict(step_size=float(next(ln.split("=")[1] for ln in (pathlib.Path(d) / f"chain{k}.csv").read_text().splitlines()
                                              if "Step size" in ln)),
                       treedepth_median=float(df["treedepth__"].median()), leapfrog_mean=float(df["n_leapfrog__"].mean()),
                       seconds=[float(ln.split()[-3]) for ln in (pathlib.Path(d) / f"chain{k}.csv").read_text().splitlines()
                                if "seconds (" in ln])
                  for k, df in enumerate(dfs, start=1)] for lab, d, dfs in (("a", dir_a, A), ("b", dir_b, B))}
    data_file = data_file or PAY / "data" / "R00.json"
    res = dict(a=str(dir_a), b=str(dir_b), core=rows,
               max_abs_z=max(max(abs(r["z_mean"]), abs(r["z_q05"]), abs(r["z_q95"])) for r in rows.values()),
               z_convention=("descriptive: (b - a) / sqrt(mcse_a^2 + mcse_b^2) assumes zero cross-fit Monte Carlo covariance; "
                             "the fits share seeds and chain IDs, so this is not a calibrated equality test (Codex 76/1855)"),
               cost=cost, joint_state_checks_b=joint_checks(dir_b, data_file))
    pathlib.Path(out_file).write_text(json.dumps(_clean(res), indent=1) + "\n")
    return res


def tranche_preflight():
    """For each fit of the active candidate other than the R00 build reference (Codex 76/1855): data byte-identical to the
    frozen original; starts exact a = 0.2 mappings of the original starts; finite actual-Stan v5/v6 density and AD
    identities at the mapped starts and at sigma 0.01 and 0.001; Q = 64 against the reference at the same scalar points."""
    from cmdstanpy.utils import write_stan_json
    I = P.CFG[P.CFG["active"]]["identity"]
    orig = HERE / "payload"
    mdl_old, mdl_new = P.model(P.CFG[P.CFG[P.CFG["active"]]["reference_version"]]["stan_file"]), P.model()
    work = CACHE / "tranche_preflight"
    work.mkdir(parents=True, exist_ok=True)
    out = {}
    for sc in [s for s in CAND["scenarios"] if s != "R00"]:
        r = dict(data_identical=(PAY / "data" / f"{sc}.json").read_bytes() == (orig / "data" / f"{sc}.json").read_bytes())
        starts = [json.loads((orig / "inits" / sc / f"chain{k}.json").read_text()) for k in range(1, 5)]
        same = []
        for k, q in enumerate(starts, start=1):
            write_stan_json(str(work / f"{sc}_{k}.json"), P.to_nc(q))
            same.append((work / f"{sc}_{k}.json").read_bytes() == (PAY / "inits" / sc / f"chain{k}.json").read_bytes())
        r["starts_exact_mapping"] = all(same)
        d = json.loads((PAY / "data" / f"{sc}.json").read_text())
        pts = {f"start_chain{k}": q for k, q in enumerate(starts, start=1)}
        pts.update(sigma_001=dict(starts[0], sigma=0.01), sigma_0001=dict(starts[0], sigma=0.001))
        ids = {n: P.identity_point(mdl_old, mdl_new, d, q) for n, q in pts.items()}
        worst = {k: max(x[k] for x in ids.values()) for k in ("log_identity_error", "grad_w_error", "grad_logsigma_error", "grad_other_error")}
        r["identity"] = dict(worst=worst, rows=ids, **{"pass": all(x["finite"] for x in ids.values())
                                                         and worst["log_identity_error"] <= I["log_tol"]
                                                         and max(worst[k] for k in worst if k.startswith("grad")) <= I["grad_tol"]})
        gates = {n: gate_point(d, q) for n, q in pts.items()}
        r["q64"] = dict(rows=gates, **{"pass": all(g["pass"] for g in gates.values())})
        r["pass"] = r["data_identical"] and r["starts_exact_mapping"] and r["identity"]["pass"] and r["q64"]["pass"]
        out[sc] = r
    out["all_pass"] = all(v["pass"] for v in out.values() if isinstance(v, dict))
    (HERE / f"tranche_preflight_{PILOT['active_candidate']}.json").write_text(json.dumps(_clean(out), indent=1, default=float) + "\n")
    print(json.dumps(_clean({sc: {k: v for k, v in r.items() if k in ("data_identical", "starts_exact_mapping", "pass")}
                             | dict(identity_worst=r["identity"]["worst"],
                                    q64_worst=max((g["log_err"] for g in r["q64"]["rows"].values()), default=None))
                             for sc, r in out.items() if isinstance(r, dict)} | dict(all_pass=out["all_pass"])), indent=1, default=float))


def _lp(mdl, q, d):
    """Actual-Stan log density and AD gradient (jacobian = true); None if Stan rejects the state, with the message."""
    try:
        row = mdl.log_prob(q, data=d, jacobian=True, sig_figs=15).iloc[0]
        return {k: float(v) for k, v in row.items()}, None
    except (RuntimeError, ValueError) as e:
        return None, str(e)[-400:]


def amended_preflight():
    """Preparation checks for an amended candidate with data overrides and solver controls (Codex 76/1895)."""
    import pandas as pd
    from cmdstanpy.utils import write_stan_json
    ov = CAND["data_overrides"]
    orig, prev = HERE / "payload", HERE / "payload_v6p"
    out = dict(candidate=PILOT["active_candidate"], overrides=ov)
    # 1. Data: field-level difference from the frozen originals is exactly the declared override.
    diffs = {}
    for sc in CAND["scenarios"]:
        new, old = json.loads((PAY / "data" / f"{sc}.json").read_text()), json.loads((orig / "data" / f"{sc}.json").read_text())
        diffs[sc] = sorted(k for k in set(new) | set(old) if new.get(k) != old.get(k))
    out["data_field_differences"] = diffs
    data_ok = all(v == sorted(ov) for v in diffs.values()) and all(
        json.loads((PAY / "data" / f"{sc}.json").read_text())[k] == ov[k] for sc in CAND["scenarios"] for k in ov)
    # 2. Starts identical to the previous package's exact mappings.
    starts_ok = all((PAY / "inits" / sc / f"chain{k}.json").read_bytes() == (prev / "inits" / sc / f"chain{k}.json").read_bytes()
                    for sc in CAND["scenarios"] for k in range(1, 5))
    out["starts_identical_to_v6p"] = starts_ok
    mdl_old, mdl_new = P.model(P.CFG[P.CFG[P.CFG["active"]]["reference_version"]]["stan_file"]), P.model()
    I = P.CFG[P.CFG["active"]]["identity"]
    dP = json.loads((PAY / "data" / "P11.json").read_text())
    d_old_tol = dict(dP, **{k: json.loads((orig / "data" / "P11.json").read_text())[k] for k in ov})
    starts = [json.loads((orig / "inits" / "P11" / f"chain{k}.json").read_text()) for k in range(1, 5)]
    pts = {f"start_chain{k}": q for k, q in enumerate(starts, start=1)}
    pts.update(sigma_001=dict(starts[0], sigma=0.01), sigma_0001=dict(starts[0], sigma=0.001))
    # 3. v5/v6 identities under the new data.
    ids = {n: P.identity_point(mdl_old, mdl_new, dP, q) for n, q in pts.items()}
    worst = {k: max(x[k] for x in ids.values()) for k in ("log_identity_error", "grad_w_error", "grad_logsigma_error", "grad_other_error")}
    id_ok = all(x["finite"] for x in ids.values()) and worst["log_identity_error"] <= I["log_tol"] and \
        max(worst[k] for k in worst if k.startswith("grad")) <= I["grad_tol"]
    out["identity"] = dict(worst=worst, **{"pass": id_ok})
    # 4. Old and new solver thresholds agree on accepted states: starts, small sigma, and the first P11 fit's states.
    fit = HERE.parents[1] / "scratch/q012-pilot/fetch-20261017-v6p/runs/P11/attempt1"
    df = pd.concat([pd.read_csv(fit / f"chain{k}.csv", comment="#") for k in range(1, 5)], ignore_index=True)
    sel = list(dict.fromkeys([int(i) for i in df.nlargest(6, "sigma").index]
                             + [int(df.kappa_b.abs().idxmax()), int(df.rho.idxmin()), int(df.rho.idxmax())]
                             + [int(i) for i in np.linspace(0, len(df) - 1, 40).astype(int)]
                             + [int(i) for i in np.flatnonzero(df.divergent__.to_numpy())]
                             + [int(df.iloc[k * 4000:(k + 1) * 4000].sigma.idxmin()) for k in range(4)]))
    states = dict(pts, **{f"p11_row{i}": P.draw_to_params(df.iloc[i], dP["N"]) for i in sel})
    eq = {}
    for n, q in states.items():
        a, ea = _lp(mdl_new, P.to_nc(q), d_old_tol)
        b, eb = _lp(mdl_new, P.to_nc(q), dP)
        eq[n] = dict(accepted_old=a is not None, accepted_new=b is not None,
                     max_abs_difference=(max(abs(a[k] - b[k]) for k in a) if a and b else None))
    eq_ok = all(r["accepted_old"] and r["accepted_new"] and r["max_abs_difference"] == 0.0 for r in eq.values())
    out["threshold_equivalence"] = dict(states=len(eq), all_identical=eq_ok,
                                        max_abs_difference=max((r["max_abs_difference"] or 0.0) for r in eq.values()),
                                        not_accepted=[n for n, r in eq.items() if not (r["accepted_old"] and r["accepted_new"])])
    # 5. Deterministic controls: p75 newly admitted, p53 still rejected; AD against actual-LP finite differences at p75.
    C = CAND["controls"]
    pdir = HERE.parents[1] / C["probe_dir"]
    dR = json.loads((PAY / "data" / "R00.json").read_text())
    dR_old = dict(dR, **{k: json.loads((orig / "data" / "R00.json").read_text())[k] for k in ov})
    ctl = {}
    for name in (C["accept"], C["reject"]):
        q = json.loads((pdir / f"{name}.json").read_text())
        qp = dict(q, w=q["w"][:dP["N"]])
        for sc, dn, do, qq in (("R00", dR, dR_old, q), ("P11", dP, d_old_tol, qp)):
            new, en = _lp(mdl_new, qq, dn)
            old, eo = _lp(mdl_new, qq, do)
            ctl[f"{name}_{sc}"] = dict(accepted_f10=new is not None, accepted_f11=old is not None,
                                       finite=(all(math.isfinite(v) for v in new.values()) if new else None),
                                       rejection=(en or "")[-200:] if new is None else None)
    qa = json.loads((pdir / f"{C['accept']}.json").read_text())
    qa = dict(qa, w=qa["w"][:dP["N"]])
    base, _ = _lp(mdl_new, qa, dP)
    fd = {}
    h = 1e-4
    for name, col in (("sigma", "g_sigma"), ("kappa_b", "g_kappa_b")):
        shift = (lambda s: dict(qa, sigma=qa["sigma"] * math.exp(s))) if name == "sigma" else (lambda s: dict(qa, kappa_b=qa["kappa_b"] + s))
        hi, _ = _lp(mdl_new, shift(h), dP)
        lo, _ = _lp(mdl_new, shift(-h), dP)
        g = (hi["lp__"] - lo["lp__"]) / (2 * h)
        fd[name] = dict(ad=base[col], fd=g, scaled_error=abs(base[col] - g) / max(1.0, abs(g)))
    ctl_ok = (ctl[f"{C['accept']}_R00"]["accepted_f10"] and not ctl[f"{C['accept']}_R00"]["accepted_f11"]
              and ctl[f"{C['accept']}_P11"]["accepted_f10"] and ctl[f"{C['accept']}_P11"]["finite"]
              and not ctl[f"{C['reject']}_R00"]["accepted_f10"] and not ctl[f"{C['reject']}_P11"]["accepted_f10"]
              and all(v["scaled_error"] <= 1e-6 for v in fd.values()))
    out["controls"] = dict(rows=ctl, finite_difference_at_accept=fd, **{"pass": bool(ctl_ok)})
    # 6. Q = 64 gates at the starts, small sigma and the admitted control (converged reference required).
    qa_eps = dict({k: v for k, v in qa.items() if k != "w"}, eps=list(np.asarray(qa["w"]) / qa["sigma"] ** 0.2))
    gpts = dict(pts, **{f"control_{C['accept']}_P11": qa_eps})
    gates = {n: gate_point(dP, q) for n, q in gpts.items()}
    out["q64"] = dict(rows=gates, **{"pass": all(g["pass"] is True for g in gates.values())})
    out["binding"] = {str(f.relative_to(HERE.parents[1])): sha(f) for f in
                      [PAY / "data" / "P11.json", PAY / "data" / "R00.json", PAY / "model_v6.stan", HERE / "pilot.py",
                       pdir / f"{C['accept']}.json", pdir / f"{C['reject']}.json"] + sorted((PAY / "inits").rglob("*.json"))}
    out["all_pass"] = bool(data_ok and starts_ok and id_ok and eq_ok and ctl_ok and out["q64"]["pass"])
    out["data_ok"] = bool(data_ok)
    (HERE / f"amended_preflight_{PILOT['active_candidate']}.json").write_text(json.dumps(_clean(out), indent=1, default=float) + "\n")
    print(json.dumps(_clean({k: v for k, v in out.items() if k not in ("binding",)} | dict(q64=dict(
        worst_log=max((g.get("log_err") or 0) for g in gates.values()), refs={n: g["reference"] for n, g in gates.items()},
        **{"pass": out["q64"]["pass"]}))), indent=1, default=float)[:5000])


def dispatch_test():
    """Local fixture for stage.sh and submit_fit.sh (Codex 76/1855): fake transport (local bash and cp), fake qsub/qstat that
    record every call, and a local 'remote' root. Writes dispatch_test.json."""
    import os
    root = CACHE / "dispatch_fixture"
    shutil.rmtree(root, ignore_errors=True)
    lib = root / "nectar" / "scripts" / "lib"
    lib.mkdir(parents=True)
    (lib / "common.sh").write_text('die() { echo "DIE: $*" >&2; exit 1; }\nrequire_cmd() { :; }\n')
    (lib / "tpac-expect.exp").write_text("spawn scp \\\n")
    (lib / "kunanyi.sh").write_text(
        'tpac_transport_setup() { TPAC_EXPECT_SCRIPT="$(dirname "${BASH_SOURCE[0]}")/tpac-expect.exp"; export TPAC_EXPECT_SCRIPT; }\n'
        'tpac_set_expect_timeout() { :; }\n'
        'tpac_quote() { printf "%q" "$1"; }\n'
        'tpac_expect_ssh() { bash -c "$1"; }\n'
        'tpac_expect_scp() { cp "$1" "${2#*:}"; }\n')
    log = root / "qsub.log"
    (root / "fake_qsub").write_text(f'#!/bin/bash\necho "$*" >> {log}\nn=$(wc -l < {log}); echo "9000$n.fake"\n')
    (root / "fake_qstat").write_text("#!/bin/bash\necho Job_Name = fake\n")
    for f in ("fake_qsub", "fake_qstat"):
        (root / f).chmod(0o755)
    env = {k: v for k, v in os.environ.items() if not k.startswith("PBS_")}
    env.update(NECTAR_ROOT=str(root / "nectar"), PAYLOAD_DIR=CAND["payload_dir"], QSUB=str(root / "fake_qsub"),
               QSTAT=str(root / "fake_qstat"), REMOTE_BASE=str(root / "remote"), KUNANYI_SSH_ALIAS="fixture")
    run = lambda cmd, extra: subprocess.run(cmd, capture_output=True, text=True, cwd=HERE.parents[1], env=dict(env, **extra))
    calls = lambda: log.read_text().splitlines() if log.exists() else []
    out = {}
    r = run(["bash", str(HERE / "stage.sh"), "fx"], {})
    out["no_fit_scenario_refused"] = dict(exit=r.returncode, calls=calls(), ok=r.returncode != 0 and not calls())
    r = run(["bash", str(HERE / "stage.sh"), "fx"], dict(FIT_SCEN="R00"))
    out["r00_refused"] = dict(exit=r.returncode, calls=calls(), ok=r.returncode != 0 and not calls())
    fits = CAND["fits"]
    first, later = fits[0], (fits[1] if len(fits) > 1 else None)
    others = [s["id"] for s in scenarios() if s["id"] != first]
    r = run(["bash", str(HERE / "stage.sh"), "fx"], dict(FIT_SCEN=first))
    c = calls()
    out[f"stage_{first.lower()}"] = dict(exit=r.returncode, calls=c,
                                         ok=r.returncode == 0 and len(c) == 2 and c[0] == "pbs/build.pbs"
                                         and c[1] == f"-v SCEN={first} -W depend=afterok:90001.fake pbs/fit.pbs"
                                         and not any(o in x for o in others for x in c) and not any("-J" in x for x in c))
    remote = root / "remote" / "q012-pilot-fx"
    out["remote_payload_verified"] = dict(ok=(remote / "manifest.sha256").exists() and (remote / "submitted.txt").exists(),
                                          submitted=(remote / "submitted.txt").read_text().split() if (remote / "submitted.txt").exists() else None)
    n0 = len(calls())
    r = run(["bash", str(HERE / "submit_fit.sh"), "fx", "P06"], {})
    out["p06_refused_without_build"] = dict(exit=r.returncode, ok=r.returncode != 0 and len(calls()) == n0, said=r.stdout[-120:])
    (remote / "build").mkdir(exist_ok=True)
    (remote / "build" / "receipt.txt").write_text(f"status=ok\nmanifest_sha256={sha(remote / 'manifest.sha256')}\n")
    r = run(["bash", str(HERE / "submit_fit.sh"), "fx", "R00"], {})
    out["submit_fit_r00_refused"] = dict(exit=r.returncode, ok=r.returncode != 0 and len(calls()) == n0)
    r = run(["bash", str(HERE / "submit_fit.sh"), "fx", "P06"], {})
    c = calls()
    if later:
        out[f"submit_fit_{later.lower()}_after_build"] = dict(exit=r.returncode, new_calls=c[n0:],
                                                              ok=r.returncode == 0 and c[n0:] == [f"-v SCEN={later} pbs/fit.pbs"])
    else:
        out["submit_fit_p06_refused_even_after_build"] = dict(exit=r.returncode, new_calls=c[n0:],
                                                               ok=r.returncode != 0 and c[n0:] == [])
    if "resources" in CAND:  # the PBS requests are the declared ones, and together within the released core-hours
        R = CAND["resources"]
        b, f = (PAY / "pbs" / "build.pbs").read_text(), (PAY / "pbs" / "fit.pbs").read_text()
        hours = lambda w: sum(int(x) / 60 ** i for i, x in enumerate(w.split(":")))
        ch = R["build_ncpus"] * hours(R["build_walltime"]) + R["fit_ncpus"] * hours(R["fit_walltime"])
        out["pbs_resources"] = dict(build=[ln for ln in b.splitlines() if ln.startswith("#PBS -l")],
                                    fit=[ln for ln in f.splitlines() if ln.startswith("#PBS -l")], core_hours=round(ch, 4),
                                    ok=f"#PBS -l select=1:ncpus={R['build_ncpus']}:mem={R['build_mem']}" in b
                                    and f"#PBS -l walltime={R['build_walltime']}" in b
                                    and f"#PBS -l select=1:ncpus={R['fit_ncpus']}:mem={R['fit_mem']}" in f
                                    and f"#PBS -l walltime={R['fit_walltime']}" in f and round(ch, 4) <= R["core_hours_max"])
    out["all_pass"] = all(v["ok"] for v in out.values())
    (HERE / f"dispatch_test_{PILOT['active_candidate']}.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


# ---------------------------------------------------------------- diagnostic replay (Codex 76/2066)
def trace_binary():
    """The instrumented model built locally exactly as build.pbs builds it: the pinned CmdStan tarball, the original
    header's hash verified, the patch copied over it, then CmdStan and the model (compiled as ../<model>.stan, so its
    messages carry the cluster's source path). Built once into scratch."""
    root = CACHE / "trace_build"
    exe = root / CAND["stan_file"].removesuffix(".stan")
    patch = HERE / CAND["patch"]["dir"] / CAND["patch"]["file"]
    stamp = root / "built_from.json"
    want = dict(patch_sha256=sha(patch), stan_sha256=sha(P.HERE / CAND["stan_file"]), tarball_sha256=sha(cmdstan_tarball()))
    if exe.exists() and stamp.exists() and json.loads(stamp.read_text()) == want:
        return exe
    shutil.rmtree(root, ignore_errors=True)
    root.mkdir(parents=True)
    subprocess.run(["tar", "xzf", str(cmdstan_tarball()), "-C", str(root)], check=True)
    cs = root / f"cmdstan-{RUN_ENV['CMDSTAN_VERSION']}"
    assert sha(cs / RUN_ENV["PATCH_TARGET"]) == RUN_ENV["PATCH_ORIGINAL_SHA256"]
    shutil.copy(patch, cs / RUN_ENV["PATCH_TARGET"])
    shutil.copy(P.HERE / CAND["stan_file"], root / CAND["stan_file"])
    with open(root / "build.log", "w") as log:
        subprocess.run(["make", "build", "-j8"], cwd=cs, stdout=log, stderr=subprocess.STDOUT, check=True)
        subprocess.run(["make", "-j4", f"../{exe.name}"], cwd=cs, stdout=log, stderr=subprocess.STDOUT, check=True)
    stamp.write_text(json.dumps(want) + "\n")
    return exe


def param_names(N):
    """Unconstrained coordinate names in Stan's order (the parameters block of model_v6.stan)."""
    return (["log_h0_1"] + [f"z_rw.{j}" for j in range(1, 25)]
            + ["tau", "log_k", "log_lambda0", "kappa", "log_b0", "kappa_b", "beta", "gamma", "sigma", "rho"]
            + [f"w.{j}" for j in range(1, N + 1)])


def _exp(x):
    return math.exp(x) if x < 709 else math.inf


def constrain(u, N):
    """Constrained parameters (prototype dict form, with eps = w / sigma^a) of an unconstrained vector."""
    names = param_names(N)
    v = dict(zip(names, (float(x) for x in u)))
    tau, sig = _exp(v["tau"]), _exp(v["sigma"])
    rho = 0.5 * (1 + math.tanh(0.5 * v["rho"]))
    a = P.CFG[CAND["prototype_version"]]["noncentring"]["a"]
    return dict(log_h0_1=v["log_h0_1"], z_rw=[v[f"z_rw.{j}"] for j in range(1, 25)], tau=tau,
                **{k: v[k] for k in ("log_k", "log_lambda0", "kappa", "log_b0", "kappa_b", "beta", "gamma")},
                sigma=sig, rho=rho, eps=[v[f"w.{j}"] / sig ** a for j in range(1, N + 1)])


def lp_grad(exe, u, data_file, work):
    """Log density (propto, Jacobian) and its unconstrained gradient from the model's own log_prob method, printed at
    18 significant digits. Returns (lp, grad, None) or (None, None, message) on a rejection."""
    work.mkdir(parents=True, exist_ok=True)
    (work / "u.json").write_text(json.dumps({"params_r": [float(x) for x in u]}))
    r = subprocess.run([str(exe), "log_prob", f"unconstrained_params={work / 'u.json'}", "jacobian=1", "data",
                        f"file={data_file}", "output", f"file={work / 'lp.csv'}", "sig_figs=18"], capture_output=True, text=True)
    if r.returncode:
        return None, None, next((ln for ln in (r.stdout + r.stderr).splitlines() if "Exception" in ln), "log_prob failed")[:300]
    row = [ln for ln in (work / "lp.csv").read_text().splitlines() if ln and not ln.startswith("#")][1].split(",")
    return float(row[0]), np.array([float(x) for x in row[1:]]), None


def leapfrog(exe, data_file, work, q, p, g, m, e):
    """One explicit leapfrog exactly as Stan's expl_leapfrog orders it, with g = grad V and a diagonal inverse metric m:
    p -= (e/2) g; q += e (m * p); new V, g; p -= (e/2) g. Returns (q, p, V, g, rejection)."""
    p = p - (0.5 * e) * g
    q = q + e * (m * p)
    lp, gl, err = lp_grad(exe, q, data_file, work)
    if err:
        return q, p, math.inf, None, err
    g = -gl
    return q, p - (0.5 * e) * g, -lp, g, None


def _H(V, p, m):
    return V + 0.5 * float(p @ (m * p))


def trace_check(attempt, data_file, out_file, exe=None, chains=None):
    """Checks of every full divergence record (Codex 76/2066), with a local build of the same model (default: the
    instrumented local build). Per record: the recorded V and grad V at the previous and failing states against the
    model's log_prob; one leapfrog from the previous state reproducing the failing state and H; two half steps from
    the same previous q, p and metric; actual-LP central differences against AD at the failing state when finite,
    else the previous state; the data's Q-node normaliser against a converged reference at the same state; and where the
    energy error arose (potential and kinetic parts, the coordinates with the largest momentum change)."""
    exe = pathlib.Path(exe) if exe else trace_binary()
    attempt = pathlib.Path(attempt)
    d = json.loads(pathlib.Path(data_file).read_text())
    names = param_names(d["N"])
    work = CACHE / "trace_check_work"
    res = dict(attempt=str(attempt), binary=str(exe), binary_sha256=sha(exe), data=str(data_file), records=[])
    files = sorted(attempt.glob("chain*.trace.jsonl")) if chains is None else [attempt / f"chain{k}.trace.jsonl" for k in chains]
    for f in files:
        for e in read_trace(f):
            if e.get("type") != "divergence" or not e.get("captured"):
                continue
            m = np.array(e["inv_metric"])
            st = {k: dict(q=np.array(e[k]["q"]), p=np.array(e[k]["p"]), V=e[k]["V"], g=np.array(e[k]["grad_V"]))
                  for k in ("initial", "previous", "failing")}
            rec = dict(chain=e["chain"], transition=e["transition"], phase=e["phase"], tree_depth=e["tree_depth"],
                       n_leapfrog=e["n_leapfrog"], signed_epsilon=e["signed_epsilon"], H0=e["H0"], H_raw=e["H_raw"],
                       delta=e["delta_effective"])
            for k, x in st.items():
                c = constrain(x["q"], d["N"])
                rec[f"{k}_state"] = dict(sigma=c["sigma"], rho=c["rho"], kappa_b=c["kappa_b"], V=x["V"],
                                         max_abs_w=float(np.max(np.abs(x["q"][-d["N"]:]))), max_abs_eps=float(np.max(np.abs(c["eps"]))))
            for k in ("previous", "failing"):
                lp, gl, err = lp_grad(exe, st[k]["q"], data_file, work)
                if err:
                    rec[f"{k}_recheck"] = dict(rejected=err, recorded_V_finite=math.isfinite(st[k]["V"]))
                else:
                    rec[f"{k}_recheck"] = dict(V_abs_err=abs(-lp - st[k]["V"]), V_identical=-lp == st[k]["V"],
                                               grad_max_abs_err=float(np.max(np.abs(-gl - st[k]["g"]))),
                                               grad_identical=bool(np.array_equal(-gl, st[k]["g"])))
            pv, fl = st["previous"], st["failing"]
            q1, p1, V1, g1, err = leapfrog(exe, data_file, work, pv["q"], pv["p"], pv["g"], m, e["signed_epsilon"])
            rep = dict(q_max_abs_err=float(np.max(np.abs(q1 - fl["q"]))), q_identical=bool(np.array_equal(q1, fl["q"])),
                       rejected=err)
            if err is None:
                rep.update(p_max_abs_err=float(np.max(np.abs(p1 - fl["p"]))), p_identical=bool(np.array_equal(p1, fl["p"])),
                           H=_H(V1, p1, m), H_rel_err=abs(_H(V1, p1, m) - e["H_raw"]) / max(1.0, abs(e["H_raw"])))
            rec["leapfrog_reproduction"] = rep
            q, p, g, half = pv["q"], pv["p"], pv["g"], []
            for _ in range(2):
                q, p, V, g, err = leapfrog(exe, data_file, work, q, p, g, m, 0.5 * e["signed_epsilon"])
                half.append(dict(rejected=err, deltaH=None if err else _H(V, p, m) - e["H0"],
                                 sigma=_exp(q[names.index("sigma")])))
                if err:
                    break
            rec["two_half_steps"] = half
            at = "failing" if math.isfinite(fl["V"]) else "previous"
            u = st[at]["q"]
            lp0, g0, err = lp_grad(exe, u, data_file, work)
            if err is None:
                fd = {}
                for nm in ("sigma", "rho", "kappa_b", names[len(names) - d["N"] + int(np.argmax(np.abs(g0[-d["N"]:])))]):
                    i = names.index(nm)
                    h = 1e-6 * max(1.0, abs(u[i]))
                    up, dn = u.copy(), u.copy()
                    up[i] += h
                    dn[i] -= h
                    a, _, e1 = lp_grad(exe, up, data_file, work)
                    b, _, e2 = lp_grad(exe, dn, data_file, work)
                    fd[nm] = (dict(ad=float(g0[i]), fd=(a - b) / (2 * h), scaled_error=abs(g0[i] - (a - b) / (2 * h)) / max(1.0, abs(g0[i])))
                              if not (e1 or e2) else dict(unresolved=e1 or e2))
                rec["ad_vs_fd"] = dict(state=at, **fd)
                rec["normaliser"] = dict(state=at, **gate_point(d, constrain(u, d["N"])))
            else:
                rec["ad_vs_fd"] = rec["normaliser"] = dict(state=at, unresolved=err)
            T = lambda x: 0.5 * float(x["p"] @ (m * x["p"]))
            dp = np.abs(fl["p"] - pv["p"])
            rec["energy_split"] = dict(dV=fl["V"] - st["initial"]["V"], dT=T(fl) - T(st["initial"]),
                                       largest_momentum_change=[(names[i], float(dp[i])) for i in np.argsort(-dp)[:5]])
            res["records"].append(rec)
    res["records_checked"] = len(res["records"])
    pathlib.Path(out_file).write_text(json.dumps(_clean(res), indent=1) + "\n")
    return res


def prefix_compare(attempt, bank, out_file):
    """Every saved row and column, and the adaptation output, of the diagnostic attempt against the earlier bank's
    same-numbered rows (Codex 76/2066). Reports the first mismatch per chain; an exact match supports calling the
    attempt an exact replay of the old saved path, otherwise it is an instrumented diagnostic attempt only."""
    attempt, bank = pathlib.Path(attempt), pathlib.Path(bank)
    hashes = dict(ln.split()[::-1] for ln in (HERE.parents[1] / CAND["replay_bank"]["hashes"]).read_text().splitlines())
    res = dict(attempt=str(attempt), bank=str(bank), chains={})

    def split(path):
        lines = path.read_text().splitlines()
        data = [ln for ln in lines if ln and not ln.startswith("#")]
        i = next(j for j, ln in enumerate(lines) if ln.startswith("# Adaptation terminated"))
        return data[0].split(","), data[1:], lines[i:i + 4]
    for k in range(1, int(RUN_ENV["CHAINS"]) + 1):
        b = bank / f"chain{k}.csv"
        bank_ok = sha(b) == hashes.get(f"chain{k}.csv")
        hn, rn, an = split(attempt / f"chain{k}.csv")
        hb, rb, ab = split(b)
        n = len(rn)
        first = next((i for i in range(n) if rn[i] != rb[i]), None)
        mis = None
        if first is not None:
            x, y = rn[first].split(","), rb[first].split(",")
            j = next(c for c in range(len(x)) if x[c] != y[c])
            mis = dict(row=first + 1, transition=int(RUN_ENV["WARMUP"]) + first + 1, column=hn[j], attempt=x[j], bank=y[j])
        res["chains"][f"chain{k}"] = dict(bank_hash_verified=bank_ok, header_identical=hn == hb, rows_compared=n,
                                          bank_rows=len(rb), identical_rows=(first if first is not None else n),
                                          all_rows_identical=first is None and n <= len(rb), first_mismatch=mis,
                                          adaptation_identical=an == ab)
    c = res["chains"].values()
    res["exact_replay_of_saved_path"] = all(v["bank_hash_verified"] and v["header_identical"] and v["all_rows_identical"]
                                            and v["adaptation_identical"] for v in c)
    pathlib.Path(out_file).write_text(json.dumps(res, indent=1) + "\n")
    return res


def diagnostic_preflight():
    """Local checks of the diagnostic package before staging (Codex 76/2066); writes diagnostic_preflight_<cand>.json.
    Inputs byte-identical to the earlier package and run.env changed only where declared; the patch bound to the pinned
    original, its removed lines and an audit of its added lines (no Hamiltonian, integrator, RNG, gradient or update
    call); log density and gradients at the payload's preflight points identical between the instrumented and
    uninstrumented local builds; the payload's own preflight.sh (LP/AD points, p75/p53 controls, smoke, both capture
    exercises, trace-on/off identity, the uninstrumented build as COMPARE_BIN) on the local instrumented binary; and
    every full record of those runs' traces reproduced from its previous state by the model's own log_prob."""
    out = {}
    other = HERE / PILOT["candidates"][CAND["same_inputs_as"]]["payload_dir"]
    env_other = dict(ln.split("=", 1) for ln in (other / "run.env").read_text().splitlines())
    env_mine = dict(ln.split("=", 1) for ln in (PAY / "run.env").read_text().splitlines())
    changed = sorted(k for k in set(env_other) | set(env_mine) if env_other.get(k) != env_mine.get(k))
    declared = set(CAND["run_env"]) - set(PILOT["candidates"][CAND["same_inputs_as"]]["run_env"]) | {"CHAINS", "SAMPLING", "FIT_SECONDS"}
    files = sorted(str(f.relative_to(PAY)) for sub in ("data", "inits", "preflight") for f in (PAY / sub).rglob("*") if f.is_file())
    body = lambda f: [ln for ln in f.read_text().splitlines() if not ln.startswith("#")] if f.suffix == ".csv" else f.read_bytes()
    same = all(body(PAY / f) == body(other / f) for f in files)
    out["inputs"] = dict(compared_with=other.name, files=len(files), identical=same, note="CSV references compared on data lines", model_identical=(
        (PAY / CAND["stan_file"]).read_bytes() == (other / CAND["stan_file"]).read_bytes()),
        run_env_changed={k: [env_other.get(k), env_mine.get(k)] for k in changed}, only_declared_changes=set(changed) <= declared,
        ok=same and set(changed) <= declared)
    diff = (PAY / "patch" / "base_nuts.diff").read_text().splitlines()
    removed = [ln[1:] for ln in diff if ln.startswith("-") and not ln.startswith("---")]
    added = [ln[1:] for ln in diff if ln.startswith("+") and not ln.startswith("+++")]
    forbidden = re.compile(r"hamiltonian_|integrator_|rand_|sample_p|update_|log_prob|gradient\(|\bH\(|evolve|init_stepsize")
    out["patch"] = dict(original_sha256=sha(HERE / CAND["patch"]["dir"] / "base_nuts.orig.hpp"), patched_sha256=sha(PAY / "patch" / "base_nuts.hpp"),
                        pinned_sha256=RUN_ENV["PATCH_ORIGINAL_SHA256"], removed_lines=removed, added_lines=len(added),
                        added_lines_calling_sampler_machinery=[ln for ln in added if forbidden.search(ln)])
    out["patch"]["ok"] = (out["patch"]["original_sha256"] == RUN_ENV["PATCH_ORIGINAL_SHA256"]
                          and not out["patch"]["added_lines_calling_sampler_machinery"])
    exe = trace_binary()
    plain = P.OUT / CAND["stan_file"].removesuffix(".stan")
    out["binaries"] = dict(instrumented=str(exe), instrumented_sha256=sha(exe), uninstrumented=str(plain),
                           uninstrumented_sha256=sha(plain), marker=b"Q012_TRACE_FILE" in exe.read_bytes() and b"Q012_TRACE_FILE" not in plain.read_bytes())
    work = CACHE / "diag_preflight_lp"
    work.mkdir(parents=True, exist_ok=True)
    lp = {}
    for f in sorted((PAY / "preflight").glob("point_*.json")):
        rows = []
        for b in (exe, plain):
            log_prob_csv(b, f, PAY / "data" / "R00.json", work / "lp.csv")
            rows.append([ln for ln in (work / "lp.csv").read_text().splitlines() if ln and not ln.startswith("#")])
        lp[f.stem] = rows[0] == rows[1]
    out["lp_ad_identical_instrumented_vs_uninstrumented"] = dict(points=lp, ok=all(lp.values()))
    pf = CACHE / "diag_preflight"
    shutil.rmtree(pf, ignore_errors=True)
    shutil.copytree(PAY, pf, ignore=shutil.ignore_patterns("runs", "build"))
    shutil.copy(exe, pf / RUN_ENV["MODEL_BIN"][2:])
    _write_env(pf, dict(env_mine, COMPARE_BIN=str(plain), COMPARE_BIN_SHA256=sha(plain)))
    t0 = time.time()
    code, txt = _run(["bash", "pbs/preflight.sh", "build/receipt.tmp"], pf, timeout=3600)
    rec = (pf / "build" / "receipt.tmp").read_text().splitlines() if (pf / "build" / "receipt.tmp").exists() else []
    reason = (pf / "build" / "preflight_reason.txt").read_text().strip() if (pf / "build" / "preflight_reason.txt").exists() else None
    out["payload_preflight_local"] = dict(exit=code, seconds=round(time.time() - t0), receipt=rec, reason=reason,
                                          ok=code == 0 and "preflight_compare_old_binary=identical" in rec)
    tc = {}
    for name, att in (("exercise_0.2", "s0.2"), ("exercise_0.5", "s0.5"), ("onoff", "on")):
        src = pf / "build" / ("onoff" if name == "onoff" else "exercise") / f"{att}.trace.jsonl"
        d = CACHE / "diag_preflight_tc" / name
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        shutil.copy(src, d / "chain1.trace.jsonl")
        r = trace_check(d, PAY / "data" / "P11.json", d / "trace_check.json", exe=exe)
        recs = r["records"]
        ok = bool(recs) and all(
            x["previous_recheck"].get("V_identical") and x["previous_recheck"].get("grad_identical")
            and (x["failing_recheck"].get("V_identical") if "V_identical" in x["failing_recheck"]
                 else not x["failing_recheck"]["recorded_V_finite"])
            and x["leapfrog_reproduction"]["q_identical"]
            and (x["leapfrog_reproduction"]["rejected"] is not None
                 or (x["leapfrog_reproduction"]["p_identical"] and x["leapfrog_reproduction"]["H_rel_err"] < 1e-12))
            for x in recs)
        tc[name] = dict(records=len(recs), ok=ok)
    out["trace_records_reproduced"] = dict(**tc, ok=all(v["ok"] for v in tc.values()))
    out["all_pass"] = all(v["ok"] for v in out.values() if isinstance(v, dict) and "ok" in v) and out["binaries"]["marker"]
    (HERE / f"diagnostic_preflight_{PILOT['active_candidate']}.json").write_text(json.dumps(_clean(out), indent=1) + "\n")
    print(json.dumps(_clean({k: (v if k != "payload_preflight_local" else {kk: vv for kk, vv in v.items() if kk != "receipt"})
                             for k, v in out.items()}), indent=1))
    return out


def w_to_eps(q):
    """A constrained v6 state (w = sigma^a eps) in the prototype's eps form, for the normaliser checks."""
    a = P.CFG[CAND["prototype_version"]]["noncentring"]["a"]
    return dict({k: v for k, v in q.items() if k != "w"}, eps=[float(x) / q["sigma"] ** a for x in q["w"]])


def unconstrain_w(q, N):
    """The unconstrained vector, in Stan's order, of a constrained v6 state."""
    v = dict(q, tau=math.log(q["tau"]), sigma=math.log(q["sigma"]), rho=math.log(q["rho"]) - math.log1p(-q["rho"]))
    return np.array([v["log_h0_1"]] + list(v["z_rw"]) + [v[k] for k in ("tau", "log_k", "log_lambda0", "kappa", "log_b0", "kappa_b",
                                                                       "beta", "gamma", "sigma", "rho")] + list(v["w"][:N]))


def lp_constrained(exe, q, data_file, work):
    """Actual-Stan log density and unconstrained gradient at a constrained state, or the rejection message."""
    work.mkdir(parents=True, exist_ok=True)
    (work / "c.json").write_text(json.dumps(q))
    r = subprocess.run([str(exe), "log_prob", f"constrained_params={work / 'c.json'}", "jacobian=1", "data", f"file={data_file}",
                        "output", f"file={work / 'lpc.csv'}", "sig_figs=18"], capture_output=True, text=True)
    if r.returncode:
        return None, None, next((ln for ln in (r.stdout + r.stderr).splitlines() if "Exception" in ln), "log_prob failed")[:300]
    row = [ln for ln in (work / "lpc.csv").read_text().splitlines() if ln and not ln.startswith("#")][1].split(",")
    return float(row[0]), np.array([float(x) for x in row[1:]]), None


def order_preflight():
    """Local wider finite bank before a quadrature-order candidate's fit (Codex 76/2096); writes order_preflight_<cand>.json.
    (1) Data differ from the earlier package only in Q and its exact Gauss-Hermite nodes and weights; starts identical.
    (2) The reused instrumented binary is bound through the fetched v6d build receipt to this payload's patch.
    (3) The order-Q normaliser against a converged reference, with the unchanged 1e-4 value and 1e-3 derivative gates,
        at: the 49 selected states of amended P11; the 49 of R00 v6; the eight starts; P11 start-1 at sigma 0.01 and
        0.001; Codex's 48 fixed P11 stress states; and the captured initial/previous/failing triads, with log-k and
        log-h0 derivatives added. A failed or unresolved state fails the bank.
    (4) The solver controls at order Q on both datasets: p75 admitted with finite LP/AD, p53 rejected.
    (5) Actual-Stan order binding: Stan's lp(Q) - lp(64) equals the Python normaliser change logN(64) - logN(Q).
    (6) AD against actual-LP central differences at the captured triads' finite states, on five axes."""
    import pandas as pd
    Q = int(CAND["quadrature_nodes"])
    exe = trace_binary()
    work = CACHE / "order_preflight"
    work.mkdir(parents=True, exist_ok=True)
    other = HERE / PILOT["candidates"][CAND["same_inputs_as"]]["payload_dir"]
    out = dict(candidate=PILOT["active_candidate"], quadrature_order=Q, binary=str(exe), binary_sha256=sha(exe))
    D = {sc: json.loads((PAY / "data" / f"{sc}.json").read_text()) for sc in ("P11", "R00")}
    D64 = {sc: json.loads((other / "data" / f"{sc}.json").read_text()) for sc in ("P11", "R00")}
    t, w = np.polynomial.hermite.hermgauss(Q)
    diffs = {sc: sorted(k for k in set(D[sc]) | set(D64[sc]) if D[sc].get(k) != D64[sc].get(k)) for sc in D}
    nodes = all(D[sc]["Q"] == Q and D[sc]["gh_t"] == [float(x) for x in t] and D[sc]["gh_w"] == [float(x) for x in w] for sc in D)
    starts_same = all((PAY / "inits" / sc / f"chain{k}.json").read_bytes() == (other / "inits" / sc / f"chain{k}.json").read_bytes()
                      for sc in D for k in range(1, 5))
    out["inputs"] = dict(field_differences=diffs, nodes_exact=nodes, starts_identical=starts_same,
                         ok=all(v == ["Q", "gh_t", "gh_w"] for v in diffs.values()) and nodes and starts_same)
    rec = HERE / "results" / "P11-diagnostic-20261019-v6d" / "build_receipt.txt"
    r = _receipt(rec)
    out["reused_binary"] = dict(receipt=str(rec.relative_to(HERE)), receipt_sha256=sha(rec), binary_sha256=r.get("binary_sha256"),
                                ok=sha(rec) == RUN_ENV["REUSE_BUILD_RECEIPT_SHA256"] and r.get("status") == "ok"
                                and r.get("binary_sha256") == RUN_ENV["REUSE_BIN_SHA256"] and r.get("binary_instrumented") == "yes"
                                and r.get("patch_original_sha256") == RUN_ENV["PATCH_ORIGINAL_SHA256"]
                                and r.get("patch_sha256") == sha(PAY / "patch" / "base_nuts.hpp"))
    # (3) The normaliser bank.
    bank = {}
    for name, att, sc in (("amended_P11_49", "scratch/q012-pilot/fetch-20261018-v6p2/runs/P11/attempt1", "P11"),
                          ("R00_v6_49", "scratch/q012-pilot/fetch-20261017-v6r00/runs/R00/attempt1", "R00")):
        j = joint_checks(HERE.parents[1] / att, PAY / "data" / f"{sc}.json")
        bank[name] = dict(states=j["states_selected"], converged=j["states_with_converged_reference"], unresolved=j["unresolved_states"],
                          failed=[k for k, g in j["states"].items() if g["pass"] is False], max_log_err=j["max_log_err"],
                          max_derivative_err=j["max_derivative_err"], ok=j["all_pass"] is True and j["states_selected"] == 49)
    pts = {}
    for sc in D:
        for k in range(1, 5):
            pts[f"start_{sc}_chain{k}"] = (sc, json.loads((PAY / "inits" / sc / f"chain{k}.json").read_text()), ())
    s1 = json.loads((PAY / "inits" / "P11" / "chain1.json").read_text())
    for sg in (0.01, 0.001):  # the earlier controls: start 1 with only sigma changed, at the same eps
        pts[f"P11_start1_sigma_{sg}"] = ("P11", dict(s1, sigma=sg, w=[x / s1["sigma"] ** 0.2 * sg ** 0.2 for x in s1["w"]]), ())
    stress = json.loads((HERE.parents[1] / "scratch/q012-capture-review-codex/inputs/fixed_48_stress_states.json").read_text())
    out["stress_source"] = dict(file="review-capture-20261019-codex.tar.gz:inputs/fixed_48_stress_states.json", states=len(stress["states"]),
                                source_sha256=stress["source_sha256"])
    for nm, q in stress["states"].items():
        pts[f"stress_{nm}"] = ("P11", q, ())
    trace_dir = HERE.parents[1] / "scratch/q012-pilot/fetch-20261019-v6d/runs/P11/attempt1"
    triads = {}
    for k in (1, 2):
        e = next(x for x in read_trace(trace_dir / f"chain{k}.trace.jsonl") if x.get("type") == "divergence" and x["phase"] == "sampling")
        for st in ("initial", "previous", "failing"):
            c = constrain(e[st]["q"], D["P11"]["N"])
            sig = c["sigma"]
            qw = dict({kk: v for kk, v in c.items() if kk != "eps"}, w=[x * sig ** 0.2 for x in c["eps"]])
            triads[f"capture_c{k}_{e['transition']}_{st}"] = qw
            pts[f"capture_c{k}_{e['transition']}_{st}"] = ("P11", qw, ("log_k", "log_h0_1"))
    gates = {}
    for nm, (sc, qw, extra) in pts.items():
        g = gate_point(D[sc], w_to_eps(qw), extra)
        gates[nm] = dict(dataset=sc, sigma=float(qw["sigma"]), **g)
    bad = [k for k, g in gates.items() if g["pass"] is not True]
    tested = [g for g in gates.values() if g["pass"] is not None]
    bank["points"] = dict(states=len(gates), failed_or_unresolved=bad, max_log_err=max(g["log_err"] for g in tested),
                          max_derivative_err=max(v for g in tested for kk, v in g.items() if kk.startswith("d_")), ok=not bad)
    out["normaliser_bank"] = dict(**bank, ok=all(v["ok"] for v in bank.values()))
    out["normaliser_points"] = gates
    # (4) Solver controls at order Q.
    C = CAND["controls"]
    pdir = HERE.parents[1] / C["probe_dir"]
    ctl = {}
    for name in (C["accept"], C["reject"]):
        q = json.loads((pdir / f"{name}.json").read_text())
        for sc in D:
            qq = dict(q, w=q["w"][:D[sc]["N"]])
            lp, g, err = lp_constrained(exe, qq, PAY / "data" / f"{sc}.json", work)
            ctl[f"{name}_{sc}"] = dict(accepted=lp is not None, finite=(bool(np.isfinite(lp) and np.all(np.isfinite(g))) if lp is not None else None),
                                      rejection=err, powell_residual=bool(err and "algebra_solver: the norm of the algebraic function" in err))
    a, rj = C["accept"], C["reject"]
    out["controls"] = dict(rows=ctl, ok=all(ctl[f"{a}_{sc}"]["accepted"] and ctl[f"{a}_{sc}"]["finite"] and not ctl[f"{rj}_{sc}"]["accepted"]
                                            for sc in D))
    # (5) Actual-Stan order binding at every finite point of the bank.
    ident = {}
    for nm, (sc, qw, _) in pts.items():
        u = unconstrain_w(qw, D[sc]["N"])
        lq, _, eq = lp_grad(exe, u, PAY / "data" / f"{sc}.json", work)
        l6, _, e6 = lp_grad(exe, u, other / "data" / f"{sc}.json", work)
        if eq or e6:
            ident[nm] = dict(rejected=eq or e6)
            continue
        qe = w_to_eps(qw)
        pred = P.log_norm_agh(D64[sc], qe, P.cohort_A(D64[sc], qe)) - P.log_norm_agh(D[sc], qe, P.cohort_A(D[sc], qe))
        ident[nm] = dict(stan_change=lq - l6, normaliser_prediction=pred, abs_error=abs(lq - l6 - pred))
    errs = [v["abs_error"] for v in ident.values() if "abs_error" in v]
    out["order_binding"] = dict(points=len(ident), checked=len(errs), rejected=[k for k, v in ident.items() if "rejected" in v],
                                max_abs_error=max(errs), ok=len(errs) == len(ident) and max(errs) <= 1e-9)
    # (6) AD against actual-LP central differences at the captured triads (finite states), five axes.
    names = param_names(D["P11"]["N"])
    fd = {}
    for nm, qw in triads.items():
        u = unconstrain_w(qw, D["P11"]["N"])
        lp0, g0, err = lp_grad(exe, u, PAY / "data" / "P11.json", work)
        if err:
            fd[nm] = dict(rejected=err)
            continue
        row = {}
        for ax in ("sigma", "rho", "kappa_b", "log_k", "log_h0_1"):
            i = names.index(ax)
            h = 1e-6 * max(1.0, abs(u[i]))
            up, dn = u.copy(), u.copy()
            up[i] += h
            dn[i] -= h
            hi, _, e1 = lp_grad(exe, up, PAY / "data" / "P11.json", work)
            lo, _, e2 = lp_grad(exe, dn, PAY / "data" / "P11.json", work)
            row[ax] = (dict(ad=float(g0[i]), fd=(hi - lo) / (2 * h), scaled_error=abs(g0[i] - (hi - lo) / (2 * h)) / max(1.0, abs(g0[i])))
                       if not (e1 or e2) else dict(unresolved=e1 or e2))
        fd[nm] = row
    se = [v["scaled_error"] for r in fd.values() for v in r.values() if isinstance(v, dict) and "scaled_error" in v]
    out["ad_vs_fd_captured"] = dict(rows=fd, max_scaled_error=max(se), threshold=1e-5,
                                    ok=all("rejected" not in r and all("scaled_error" in v for v in r.values()) for r in fd.values())
                                    and max(se) <= 1e-5)
    out["all_pass"] = all(out[k]["ok"] for k in ("inputs", "reused_binary", "normaliser_bank", "controls", "order_binding", "ad_vs_fd_captured"))
    (HERE / f"order_preflight_{PILOT['active_candidate']}.json").write_text(json.dumps(_clean(out), indent=1, default=float) + "\n")
    print(json.dumps(_clean({k: v for k, v in out.items() if k not in ("normaliser_points",)}), indent=1, default=float)[:6000])
    return out


# ---------------------------------------------------------------- control fixtures
def _run(cmd, root, env=None, timeout=900):
    import os
    e = {k: v for k, v in os.environ.items() if not k.startswith("PBS_") and k != "LOADEDMODULES"}
    e.update(PILOT_ROOT=str(root), **(env or {}))
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=root, env=e, timeout=timeout)
    return r.returncode, r.stdout + r.stderr


def _fixture_seal(root, binary=None):
    """Rewrite a fixture's manifest and a successful build receipt bound to it (instrumented when the binary is)."""
    binary = binary or RUN_ENV["MODEL_BIN"][2:]
    write_manifest(root)
    (root / "build").mkdir(exist_ok=True)
    inst = "binary_instrumented=yes\n" if b"Q012_TRACE_FILE" in (root / binary).read_bytes() else ""
    (root / "build" / "receipt.txt").write_text(
        f"status=ok\nmanifest_sha256={sha(root / 'manifest.sha256')}\nbinary_sha256={sha(root / binary)}\n{inst}")


def _write_env(root, env):
    (root / "run.env").write_text("".join(f"{k}={v}\n" for k, v in env.items()))


def selftest():
    """Cheap fixtures for every control the cluster relies on; writes selftest.json. Uses the local instrumented build."""
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
    exe = trace_binary()
    plain = P.OUT / CAND["stan_file"].removesuffix(".stan")
    C = int(RUN_ENV["CHAINS"])
    shutil.copy(exe, root / RUN_ENV["MODEL_BIN"][2:])
    d, _, _ = P.dataset(P.CFG["seed"])
    (root / "data").mkdir()
    (root / "fits.txt").write_text("FX\nFY\nFB\nFT\nNODATA\n")
    for scen in ("FX", "FY", "FB", "FT", "FZ"):
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
    out["complete"] = dict(exit=code, status=rc.get("status"), maxrss_kb=[rc.get(f"chain{k}_maxrss_kb") for k in range(1, C + 1)],
                           traces=[rc.get(f"chain{k}_trace") for k in range(1, C + 1)],
                           ok=code == 0 and rc.get("status") == "complete" and all(rc.get(f"chain{k}_trace") == "summary" for k in range(1, C + 1)))
    code, txt = _run(fit, root, dict(SCEN="FX"))
    out["resume_skip"] = dict(exit=code, ok=code == 0 and "SKIP" in txt and not (root / "runs" / "FX" / "attempt2").exists())
    code, txt = _run(fit, root, dict(PBS_ARRAY_INDEX="1", SCEN="FY"))
    out["array_dispatch_refused"] = dict(exit=code, ok=code == 2 and "array" in txt and not (root / "runs" / "FY").exists())
    code, txt = _run(fit, root, dict(SCEN="FZ"))
    out["scenario_not_in_fits_refused"] = dict(exit=code, ok=code == 2 and "not in fits.txt" in txt and not (root / "runs" / "FZ").exists())
    _write_env(root, {k: v for k, v in env.items() if k != "TRACE_SCHEMA"})
    _fixture_seal(root)
    code, txt = _run(fit, root, dict(SCEN="FY"))
    out["trace_settings_missing_refused"] = dict(exit=code, ok=code == 2 and "TRACE_SCHEMA" in txt)
    _write_env(root, env)
    shutil.copy(plain, root / RUN_ENV["MODEL_BIN"][2:])
    _fixture_seal(root)
    code, txt = _run(fit, root, dict(SCEN="FY"))
    out["uninstrumented_binary_refused"] = dict(exit=code, ok=code == 2 and "instrumented" in txt)
    shutil.copy(exe, root / RUN_ENV["MODEL_BIN"][2:])
    _fixture_seal(root)
    code, txt = _run(fit, root, dict(SCEN="FB"))
    rc = _receipt(root / "runs" / "FB" / "receipt.txt")
    out["chain_failure"] = dict(exit=code, status=rc.get("status"), chain_exits=[rc.get(f"chain{k}_exit") for k in range(1, C + 1)],
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
    (root / "fake_model").write_text("#!/bin/bash\n# Q012_TRACE_FILE (runner fixture only)\ntrap '' TERM\nwhile :; do sleep 1; done\n")
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
                          chain_exits=[rc.get(f"chain{k}_exit") for k in range(1, C + 1)],
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
    (root / "build" / "receipt.txt").write_text(br.replace(f"binary_sha256={sha(root / RUN_ENV['MODEL_BIN'][2:])}", "binary_sha256=" + "0" * 64))
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
    gram = rejection_grammar(PAY / CAND["stan_file"], root / "data" / "FX.json")
    q = lambda a, s="FX", e=env, m=None, b=None: qualify(a, s, e, m or rcx["manifest_sha256"],
                                                         b or dict(bld, manifest_sha256=rcx["manifest_sha256"]), gram)
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
    scr["nonzero_chain_exit"] = (q(variant("exit", lambda v: (v / f"chain{C}.exit").write_text("1\n"))), bool)
    def inject(fname, after, text):
        def f(v):
            lines = (v / fname).read_text().split("\n")
            k = next(i for i, ln in enumerate(lines) if ln.startswith(after)) + 1
            (v / fname).write_text("\n".join(lines[:k] + text.split("\n") + lines[k:]))
        return f
    scr["fatal_text_in_log"] = (q(variant("fatal", inject("chain1.log", "Iteration:  3 /", "Exception: fatal"))), bool)
    scr["separate_stderr_file"] = (q(variant("stderr", lambda v: (v / "chain1.stderr").write_text(""))), bool)
    scr["fewer_draws_than_declared"] = (q(good, e=dict(env, SAMPLING=6)), bool)

    def drop_row(v):
        lines = (v / "chain2.csv").read_text().splitlines()
        j = max(i for i, ln in enumerate(lines) if ln and not ln.startswith("#"))
        (v / "chain2.csv").write_text("\n".join(lines[:j] + lines[j + 1:]) + "\n")
    scr["unequal_chain_lengths"] = (q(variant("short", drop_row)), bool)
    scr["extra_chain_csv"] = (q(variant("extra", lambda v: shutil.copy(v / "chain1.csv", v / f"chain{C + 1}.csv"))), bool)
    scr["csv_settings_mismatch"] = (q(variant("meta", lambda v: (v / f"chain{C}.csv").write_text(
        (v / f"chain{C}.csv").read_text().replace(f"delta = {env['ADAPT_DELTA']}", "delta = 0.9", 1)))), bool)
    scr["build_receipt_other_manifest"] = (q(good, b=dict(bld, manifest_sha256="3" * 64)), bool)

    def no_hash(v):
        (v / "receipt.txt").write_text("\n".join(ln for ln in (v / "receipt.txt").read_text().splitlines()
                                                 if not ln.startswith("binary_sha256=")) + "\n")
    nb = {k: x for k, x in dict(bld, manifest_sha256=rcx["manifest_sha256"]).items() if k != "binary_sha256"}
    scr["binary_hash_absent_from_both_receipts"] = (q(variant("nohash", no_hash), b=nb), bool)
    out["screening_refusals"] = {k: dict(failures=r[:3], ok=pred(r)) for k, (r, pred) in scr.items()}
    out["screening_refusals"]["ok"] = all(v["ok"] for v in out["screening_refusals"].values())
    # Capture validity on a real trace: P11, fixed step 0.2, no adaptation, 4 warmup + 8 draws (every transition diverges).
    tr = root / "runs" / "TR" / "attempt1"
    tr.mkdir(parents=True)
    env_tr = dict(env, WARMUP=4, SAMPLING=8, MAX_DEPTH=8, TRACE_CAP_WARMUP=2, TRACE_CAP_SAMPLING=3)
    subprocess.run([str(exe), "sample", "num_samples=8", "num_warmup=4", "adapt", "engaged=0", "algorithm=hmc", "engine=nuts",
                    "max_depth=8", "stepsize=0.2", "id=1", "data", f"file={PAY / 'data' / 'P11.json'}",
                    f"init={PAY / 'inits' / 'P11' / 'chain1.json'}", "random", f"seed={RUN_ENV['SEED']}", "output",
                    f"file={tr / 'chain1.csv'}", "refresh=1"], capture_output=True, text=True, check=True,
                   env=dict(os.environ, Q012_TRACE_FILE=str(tr / "chain1.trace.jsonl"), Q012_TRACE_CHAIN="1", Q012_TRACE_WARMUP="4",
                            Q012_TRACE_CAP_WARMUP="2", Q012_TRACE_CAP_SAMPLING="3"))
    good_tr, _ = trace_structure(tr, env_tr, 1)

    def tvar(name, mutate):
        v = root / "runs" / "TRV" / name / "attempt1"
        shutil.copytree(tr, v)
        rows = (v / "chain1.trace.jsonl").read_text().splitlines()
        (v / "chain1.trace.jsonl").write_text("\n".join(mutate(rows)) + "\n")
        return trace_structure(v, env_tr, 1)[0]
    flip = lambda rows: [rows[0]] + [r.replace('"captured":false', '"captured":true', 1) if i == 4 else r
                                     for i, r in enumerate(rows[1:], 1)]
    capt = dict(
        real_trace_valid=(good_tr, lambda f: f == []),
        no_summary=(tvar("nosum", lambda r: r[:-1]), lambda f: any("no summary" in x for x in f)),
        write_failed=(tvar("wfail", lambda r: r[:-1] + [r[-1].replace('"write_ok":true', '"write_ok":false')]),
                      lambda f: any("write_ok" in x for x in f)),
        sampling_event_missing=(tvar("miss", lambda r: [x for x in r if '"transition":7,' not in x]),
                                lambda f: any("differ from CSV" in x for x in f)),
        capture_flag_beyond_cap=(tvar("flip", flip), lambda f: any("capture flags" in x for x in f)),
        header_other_chain=(tvar("chain", lambda r: [r[0].replace('"chain":1', '"chain":2', 1)] + r[1:]),
                            lambda f: any("header chain" in x for x in f)),
        malformed_line=(tvar("bad", lambda r: r[:3] + ["{not json"] + r[3:]), lambda f: any("malformed" in x for x in f)))
    out["capture_validity"] = {k: dict(failures=f[:2], ok=bool(pred(f))) for k, (f, pred) in capt.items()}
    out["capture_validity"]["ok"] = all(v["ok"] for v in out["capture_validity"].values())
    # The combined-log parser on a real fixture log (WARMUP 10, SAMPLING 5, refresh 1): phase boundaries and failure cases.
    log = (good / "chain1.log").read_text()
    W, S = int(env["WARMUP"]), int(env["SAMPLING"])
    env_text = lambda exc: "\n".join([LOG_FIXED["rej"], exc, LOG_FIXED["rej3"], LOG_FIXED["rej4"], ""])
    loc = lambda ln: f" (in '../{CAND['stan_file']}', line {ln}, column 4 to column 80) (in '../{CAND['stan_file']}', line 232, column 6 to line 233, column 86)"
    known = "Exception: Exception: Q012 input failure: 1-D initial score" + loc(39)
    ftol = json.loads((root / "data" / "FX.json").read_text())["solver_f_tol"]
    powell = lambda tol, ln: ("Exception: Exception: algebra_solver: the norm of the algebraic function is 2.18243e-11 but should be lower "
                              f"than the function tolerance: {tol}. Consider decreasing the relative tolerance and increasing max_num_steps." + loc(ln))

    def after(text, prefix, ins):
        lines = text.split("\n")
        k = next(i for i, ln in enumerate(lines) if ln.startswith(prefix)) + 1
        return "\n".join(lines[:k] + ins.split("\n") + lines[k:])

    def drop(text, prefix):
        return "\n".join(ln for ln in text.split("\n") if not ln.startswith(prefix))
    last_warm = f"Iteration: {W} / {W + S}"
    first_samp = f"Iteration: {W + 1} / {W + S}"
    cases = dict(
        clean=(log, lambda f, r: not f and not r),
        warmup_rejection=(after(log, "Iteration:  3 /", env_text(known)),
                          lambda f, r: not f and [(x["phase"], x["transition"], x["cause"]) for x in r] == [("warmup", 3, "input")]),
        boundary_last_warmup=(after(log, last_warm, env_text(known)),
                              lambda f, r: not f and [(x["phase"], x["transition"]) for x in r] == [("warmup", W)]),
        boundary_first_sampling=(after(log, first_samp, env_text(known)),
                                 lambda f, r: not f and [(x["phase"], x["transition"]) for x in r] == [("sampling", W + 1)]),
        stepsize_init_rejection=(after(log, "Adjust your expectations", env_text(known)),
                                 lambda f, r: not f and [x["phase"] for x in r] == ["stepsize_init"]),
        init_rejection=(after(log, "num_threads", "\n".join([LOG_FIXED["init"], LOG_FIXED["init_eval"], known])),
                        lambda f, r: not f and [x["phase"] for x in r] == ["init"]),
        powell_residual_recognised=(after(log, "Iteration:  3 /", env_text(powell(f"{ftol:g}", 40))),
                                    lambda f, r: not f and [(x["phase"], x["cause"]) for x in r] == [("warmup", "solver_internal")]),
        powell_other_tolerance=(after(log, "Iteration:  3 /", env_text(powell("0.001", 40))), lambda f, r: bool(f)),
        powell_other_line=(after(log, "Iteration:  3 /", env_text(powell(f"{ftol:g}", 41))), lambda f, r: bool(f)),
        keyword_newton=(after(log, "Iteration:  3 /", env_text("Exception: Exception: Newton step failed" + loc(40))), lambda f, r: bool(f)),
        guard_extra_text=(after(log, "Iteration:  3 /", env_text(known.replace("initial score", "initial score x"))), lambda f, r: bool(f)),
        guard_wrong_line=(after(log, "Iteration:  3 /", env_text(known.replace("line 39,", "line 37,"))), lambda f, r: bool(f)),
        header_extra_assignment=(after(log, "  sample", "    foo = bar"), lambda f, r: bool(f)),
        header_value_changed=(log.replace("    num_warmup = 10", "    num_warmup = 11", 1), lambda f, r: bool(f)),
        header_truncated=(drop(log, "num_threads"), lambda f, r: bool(f)),
        unknown_text=(after(log, "Iteration:  5 /", "Something unexpected happened"), lambda f, r: bool(f)),
        unrecognised_cause=(after(log, "Iteration:  5 /", env_text("Exception: Exception: cholesky_decompose: A is not symmetric")),
                            lambda f, r: bool(f)),
        incomplete_envelope=(after(log, "Iteration:  5 /", "\n".join([LOG_FIXED["rej"], known])), lambda f, r: bool(f)),
        orphan_exception=(after(log, "Iteration:  5 /", known), lambda f, r: bool(f)),
        missing_marker=(drop(log, "Iteration:  7 /"), lambda f, r: bool(f)),
        truncated=(log[:log.index(first_samp)], lambda f, r: bool(f)),
        fatal_step_size=(after(log, "Adjust your expectations", "Exception initializing step size.\n" + known), lambda f, r: bool(f)))
    pr = {}
    hdr = expected_header(env, "FX", 1, "runs/FX/attempt1/chain1.csv")
    for name, (text, ok) in cases.items():
        f, r = parse_log(text, W, S, hdr, gram)
        pr[name] = dict(failures=f[:2], rejections=[(x["phase"], x["transition"], x["cause"]) for x in r], ok=bool(ok(f, r)))
    pr["ok"] = all(v["ok"] for v in pr.values())
    out["log_parser"] = pr
    # End to end: a sampling-phase rejection leaves the attempt qualified but fails the screen.
    sv = variant("samprej", inject("chain2.log", first_samp, env_text(known)))
    rs = diagnose(sv, "FX", env=env, manifest_sha=rcx["manifest_sha256"], build_receipt=dict(bld, manifest_sha256=rcx["manifest_sha256"]),
                  write=False, grammar=gram)
    out["sampling_rejection_fails_screen"] = dict(qualified=rs["qualified"], criterion=rs.get("screening", {}).get("no_fatal_or_sampling_phase_failures"),
                                                  ok=rs["qualified"] and rs.get("screening", {}).get("no_fatal_or_sampling_phase_failures") is False)
    # Finite guards on statistics.
    nan, inf = float("nan"), float("inf")
    eb = eta_block(0.03, 0.40, 0.003, nan, 0.2)
    out["finite_guards"] = dict(
        nan_mcse_leaves_precision_unresolved=eb["mcse_target_met"] is None and eb["X_numerically_uncertain"] is None,
        raw_flags_kept=eb["D"] is False and eb["X"] is False,
        infinite_ess_fails=not ess_pass({"sigma": dict(bulk=inf, tail=500.0)}),
        nan_rhat_fails=not rhat_pass({"sigma": nan}),
        nan_endpoint_unresolved=eta_block(nan, 0.4, 0.003, 0.01, 0.2)["D"] is None,
        nan_endpoint_leaves_precision_unresolved=eta_block(nan, 0.4, 0.003, 0.01, 0.2)["mcse_target_met"] is None)
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
    real_out, chk = P.OUT, json.loads((HERE / CAND["checks_file"]).read_text())
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
    shutil.copy(exe, pf / RUN_ENV["MODEL_BIN"][2:])
    _write_env(pf, dict(RUN_ENV, COMPARE_BIN=str(plain), COMPARE_BIN_SHA256=sha(plain)))
    code, txt = _run(["bash", "pbs/preflight.sh", "build/receipt.tmp"], pf, timeout=3600)
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
    if "REUSE_BIN" in RUN_ENV:  # the preflight-only build job (Codex 76/2096), with a stub 'module' command
        bj = CACHE / "selftest_buildjob"
        shutil.rmtree(bj, ignore_errors=True)
        shutil.copytree(PAY, bj, ignore=shutil.ignore_patterns("runs", "build"))
        os.symlink(cmdstan_tarball(), bj / cmdstan_tarball().name)
        src = bj / "reused"
        src.mkdir()
        shutil.copy(exe, src / "model_v6")
        rec = src / "receipt.txt"
        rec.write_text(f"host=fixture\ngxx=fixture\nstatus=ok\nbinary_sha256={sha(exe)}\nbinary_instrumented=yes\n"
                       f"patch_original_sha256={RUN_ENV['PATCH_ORIGINAL_SHA256']}\npatch_sha256={sha(PAY / 'patch' / 'base_nuts.hpp')}\n")
        stub = bj / "stub"
        stub.mkdir()
        (stub / "module").write_text("#!/bin/bash\nexit 0\n")
        (stub / "module").chmod(0o755)

        def job(**over):
            e = dict(RUN_ENV, MODULE="fixture/1", REUSE_BIN=str(src / "model_v6"), REUSE_BIN_SHA256=sha(exe),
                     REUSE_BUILD_RECEIPT=str(rec), REUSE_BUILD_RECEIPT_SHA256=sha(rec))
            e.update(over)
            _write_env(bj, e)
            write_manifest(bj)
            shutil.rmtree(bj / "build", ignore_errors=True)
            code, txt = _run(["bash", "pbs/build.pbs"], bj, dict(PBS_O_WORKDIR=str(bj), PATH=f"{stub}:{os.environ['PATH']}"), timeout=3600)
            r = _receipt(bj / "build" / "receipt.txt") if (bj / "build" / "receipt.txt").exists() else {}
            return code, r
        code, r = job()
        bjo = dict(reuse_ok=dict(exit=code, status=r.get("status"), binary=r.get("binary_sha256"),
                                 preflight=[k for k in r if k.startswith("preflight_")],
                                 ok=code == 0 and r.get("status") == "ok" and r.get("binary_instrumented") == "yes"
                                 and r.get("binary_sha256") == sha(exe) and "preflight_exercise_0.5" in r))
        code, r = job(REUSE_BUILD_RECEIPT_SHA256="0" * 64)
        bjo["wrong_receipt_hash"] = dict(exit=code, reason=r.get("reason"), ok=code == 1 and r.get("reason") == "reuse_receipt_hash")
        rec.write_text(rec.read_text().replace(f"patch_sha256={sha(PAY / 'patch' / 'base_nuts.hpp')}", "patch_sha256=" + "4" * 64))
        code, r = job()
        bjo["patch_not_bound"] = dict(exit=code, reason=r.get("reason"), ok=code == 1 and r.get("reason") == "reuse_patch_binding")
        rec.write_text(rec.read_text().replace("patch_sha256=" + "4" * 64, f"patch_sha256={sha(PAY / 'patch' / 'base_nuts.hpp')}"))
        with open(src / "model_v6", "ab") as f:
            f.write(b"\0")
        code, r = job(REUSE_BIN_SHA256=sha(exe))
        bjo["tampered_binary"] = dict(exit=code, reason=r.get("reason"), ok=code == 1 and r.get("reason") == "reuse_binary_hash")
        bjo["ok"] = all(v["ok"] for v in bjo.values())
        out["preflight_only_build_job"] = bjo
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
    elif cmd == "compare":
        r = compare(sys.argv[2], sys.argv[3], sys.argv[4])
        print(json.dumps(_clean({k: v for k, v in r.items() if k not in ("core", "cost", "joint_state_checks_b")}), indent=1))
    elif cmd == "joint":
        r = joint_checks(sys.argv[2], sys.argv[3])
        pathlib.Path(sys.argv[4]).write_text(json.dumps(_clean(r), indent=1) + "\n")
        print(json.dumps(_clean({k: v for k, v in r.items() if k != "states"}), indent=1))
    elif cmd == "tranche-preflight":
        tranche_preflight()
    elif cmd == "dispatch-test":
        dispatch_test()
    elif cmd == "amended-preflight":
        amended_preflight()
    elif cmd == "order-preflight":
        order_preflight()
    elif cmd == "diagnostic-preflight":
        diagnostic_preflight()
    elif cmd == "trace-check":
        r = trace_check(sys.argv[2], sys.argv[3], sys.argv[4], exe=sys.argv[5] if len(sys.argv) > 5 else None)
        print(json.dumps(_clean({k: v for k, v in r.items() if k != "records"}), indent=1))
    elif cmd == "prefix-compare":
        print(json.dumps(prefix_compare(sys.argv[2], sys.argv[3], sys.argv[4]), indent=1))
    else:
        {"build": build, "selftest": selftest}[cmd]()
