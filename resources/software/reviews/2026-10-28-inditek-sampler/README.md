# INDITEK-2.0: initial-prior counterexample

28 October 2026, Codex. **Source-specific finding:** the
[sampler at GitHub commit `ae26596`](https://github.com/INDITEK-eco-evo-Model/INDITEK-2.0/blob/ae26596ff82a3528f02f113e0d2465a82f5ef360/inditek_MCMC.py)
evaluates the initial Gaussian prior differently from proposed-state priors.
A controlled test reproduces an incorrect first-step acceptance. The
corresponding file from the [Zenodo 22079167 deposit](https://zenodo.org/records/22079167)
has the same SHA-256 and gives the same result. Its saved chains have not
been linked to the source that generated them, and one saved proof-chain
transition is inconsistent with the deposited sampler and proof settings.
No claim about published results or their practical sensitivity follows from
the counterexample alone.

## Finding

In `inditek_MCMC.py`, initialisation sets `temp[gaus] = mu[gaus]` and
`log_prior_current = -0.5*sum(temp)`. Proposed states instead use
`((params_proposed[gaus] - mu[gaus]) / sigma[gaus])**2`. For the Q10 prior
with mean 2 and standard deviation 0.4, the two expressions generally give
different log priors for the same state. On acceptance the current posterior
is updated using the proposed-state formula; before the first acceptance it
retains the initial value. The error is therefore not evidence by itself
of an altered long-run stationary distribution.

The independent [control](../../bench/validate/t5_inditek_sampler_control.py)
loads the real sampler function, replaces the expensive forward model with a
constant residual sum of squares, and forces known proposal and uniform
random draws. These are synthetic controls, not a model fit:

- Start Q10 at 2.3, inside the documented proof initial range 1.6–2.4;
  propose 2.5 with the stated 0.08 initial proposal standard deviation and
  a standard-normal draw of 2.5. With constant likelihood, the correct
  Gaussian log-prior ratio is −0.5. A uniform draw of 0.8 should reject the
  step. The tested sampler accepts it.
- Start Q10 at 3, within its configured hard bounds, and propose changing
  only a uniform-prior parameter with constant likelihood. The prior ratio is
  one, so the proposal should be accepted; the tested sampler rejects it
  for a uniform draw of 0.5.
- An initial state at the Q10 prior mean with the same uniform-parameter
  control is accepted by both calculations.

The source SHA-256 and exact observed results for GitHub and Zenodo are in
[`inditek_sampler_github_20261028.json`](../../bench/results/t5/inditek_sampler_github_20261028.json)
and [`inditek_sampler_zenodo_20261028.json`](../../bench/results/t5/inditek_sampler_zenodo_20261028.json).
The SHA-256 of the tested source is
`ede1421d4a6db9d2883fd0f2d9152240afcaadcd730f0269602defa41cf9933c`.
The Zenodo file was extracted by HTTP byte-range reads of the archive and
passed the ZIP member's CRC check. The full archive was subsequently
downloaded, matched the provider MD5 `a1aa3deade0ddd2d57615d5064ef1c20`,
and passed `unzip -t`; its SHA-256 is
`850b86383fd8ce87511eee67524808021e2f636121ed18caa25b4321cb912b80`.
Neither source file is redistributed here.
Reproduce the test with the exact source file and the pinned Python image:

```sh
docker run --rm -i --network none -v /path/to/source:/source:ro \
  eprp-sw/bench-py5:t5 python - /source/inditek_MCMC.py \
  < resources/software/bench/validate/t5_inditek_sampler_control.py
```

## Deposited proof-chain trace

The proof output contains six chains. Reading their initial proposed,
accepted, RSS and acceptance arrays yields first accepted iterations of
1, 1, 7, 1, 1 and 4. The [trace calculation](../../bench/validate/t5_inditek_initial_trace.py)
and [receipt](../../bench/results/t5/inditek_proof_initial_trace_20261028.json)
use the saved values and the deposited sampler's proof prior, conditional
on that code and those settings actually having generated the output.

In the **third chain, iteration 4**, the saved current and proposed Q10 are
both 2.31859042; the proposed change is to Kmax, whose stated prior is
uniform. The saved RSS decreases from 3834.633639 to 3830.561523. Thus,
even using the defective initial prior, the deposited sampler's calculated
log acceptance ratio would be +2.71887, and the corrected calculation would
be +2.03606. Both imply acceptance for every possible uniform draw, yet the
saved acceptance flag is zero and the next stored parameters retain the
old state. The proposal is inside the deposited proof bounds. This is an
**incompatibility with the deposited code and settings**, not proof of which
implementation generated the chain or why it differs. In the third chain's
iteration 3, the two conditional acceptance probabilities are 0.096 and
0.190; without the uniform draw, its saved rejection cannot determine which
rule was used.

The retained NPZ is `inditekMCMCoutput_5002_proof.npz`, extracted through
byte ranges, checked against the ZIP member CRC, and confirmed identical to
the file extracted from the checksum-verified archive; its SHA-256 is
`7c47afef83c85baff6a0cddaee20a28bce926261f41e221a03f5928cea8ccd64`.
The original uniform draws, generating-source version and actual runtime
settings are not recorded in that NPZ. The trace does not establish the
effect of the initialisation bug on published conclusions or on later
sampling. Nor does matching outputs establish posterior calibration.

## Later transitions across deposited variants

The [five-file trace check](../../bench/validate/t5_inditek_trace_consistency.py)
examines only iterations **after** each chain's first recorded acceptance,
where the deposited sampler would have updated its current log posterior.
It selects finite-RSS proposals that change exactly one non-Q10 parameter,
leave Q10 unchanged, and decrease RSS by more than 1e-7. Under the deposited
sampler, only Q10 has a Gaussian prior; the other priors are uniform within
the bounds, and evaluated proposals have passed those bounds. Every selected
proposal therefore has a positive log acceptance ratio. Recorded rejections
cannot be generated by that rule, irrespective of the uniform draw.

| Archived variant | Selected improving proposals | Recorded rejections |
| --- | ---: | ---: |
| proof | 4,888 | 0 |
| open | 5,877 | 24 |
| expo | 5,741 | 1,126 |
| food | 6,275 | 205 |
| temp | 7,164 | 0 |

Across the five files, the saved next-state parameter and RSS arrays agree
with their recorded acceptance flags at all 150,000 checked transitions.
The [receipt](../../bench/results/t5/inditek_trace_consistency_20261028.json)
includes input hashes, counts and examples. For example, the first `food`
case changes only speciation minimum, with RSS 22448.5948 → 22447.0482,
yet is rejected and retains the previous state. This check treats the saved
RSS and parameter fields according to the deposited script's definitions;
it does not establish what code, priors or settings actually produced the
outputs, or whether those outputs are the precise chains used in the paper.
The inconsistency is broader than the initial-prior defect and should not be
attributed to it.

## A consistent historical candidate

The 4 June 2026 GitHub commit
[`755a08e`](https://github.com/INDITEK-eco-evo-Model/INDITEK-2.0/tree/755a08e16b253057bc15e9e364553cb425b4602a)
contains an earlier `metropolis_7param.py` and `indicios_7param.py`. The
former evaluates the proposed Gaussian prior at **current**, not proposed,
Q10; the latter specifies Q10 prior mean 2 and standard deviation **0.08**,
versus 0.4 in the deposited code. The old source also uses the incorrect
initial-prior expression. Its SHA-256 values are
`79256783eda56ae30fa653e8f1350a172cd6eb7201eefa2944347192ce4efedf`
and `40ecfcf44b01ac85aa8a2f087e4fc9c2ddc9e5bdb93464d77ce2ed565f224e90`.

The [candidate-rule replay](../../bench/validate/t5_inditek_candidate_rules.py)
tracks the evolving current prior implied by each implementation across
all five saved files. With the June rule and its 0.08 prior, **none of
146,286 finite-RSS transitions** is a rejection when its conditional log
acceptance ratio exceeds 1e-9. With the deposited rule and its 0.4 prior,
the corresponding counts are 1, 26, 1,592, 272 and 0 for proof, open,
expo, food and temp. The old rule also has no recorded acceptance with a
conditional log ratio below −30. See the
[receipt](../../bench/results/t5/inditek_candidate_rules_20261028.json).
An independently written [vectorised recount](../../bench/validate/t5_inditek_vector_crosscheck.py)
reproduces all five sets of counts
([receipt](../../bench/results/t5/inditek_vector_crosscheck_20261028.json)).
This is stronger evidence that the earlier rule and settings are compatible
with the traces; it does **not** identify the generating commit uniquely,
replay the random draws or prove that the chains are calibrated. Under the
older implementation, the stored current prior after an accepted Q10 change
lags the parameter state, so treating its chains as draws from the stated
Gaussian posterior needs a separate validity check.

A second deterministic [control](../../bench/validate/t5_inditek_old_sampler_control.py)
executes that actual historical sampler with a constant-likelihood stub. It
first accepts a uniform-prior parameter step from Q10 = 2, then proposes
Q10 = 2.2 using the historical 0.08 prior and proposal standard deviation.
The correct log acceptance ratio is −3.125, so a uniform draw of 0.5 should
reject; the historical sampler accepts because its proposed-prior expression
uses Q10 = 2. The observed result is saved in the
[receipt](../../bench/results/t5/inditek_old_sampler_control_20261028.json).
This demonstrates a wrong transition **after** the first acceptance, but
does not quantify bias in the deposited chains or establish that they used
this exact source.

## Flat-likelihood synthetic diagnostic

Prospective amendment A6 fixes a common synthetic target, initial settings,
seeds, burn-in and reporting before this run. Four chains each of the
historical and deposited implementations were run with a constant-RSS
stub. Both retained their own ongoing proposal adaptation. The target's
Q10 mean is 2, variance 0.0064, and each one-standard-deviation tail
probability is about 0.159.

The historical chain means after burn-in were 2.525, 2.777, 1.256 and
1.455. Two chains accepted no proposals in their retained 20,000
iterations; their reported zero batch standard errors are artifacts of
constant traces, not evidence of precision. The other two placed 99% or
more of their retained draws in one tail. The deposited sampler's four
means were 1.999, 2.007, 1.998 and 2.002; variances were 0.00627–0.00642,
and the individual tail proportions were 0.142–0.173. These summaries
describe this simple diagnostic, not general calibration.

The [declared test](../../bench/validate/t5_inditek_flat_prior.py) and
[receipt](../../bench/results/t5/inditek_flat_prior_20261028.json) retain all
four seed-specific summaries. A separate [post-hoc rerun](../../bench/validate/t5_inditek_flat_diagnose.py)
of historical seed 34101 reproduces its flat trace: all five proposal
standard deviations had fallen to `1e-12` by iteration 5,000 and no
proposals were accepted in the next 20,000; those proposals were evaluated,
not excluded as out of bounds ([receipt](../../bench/results/t5/inditek_flat_diagnose_20261028.json)).
This identifies a failure of the historical implementation **with its
adaptive scheme on this target**. The comparison does not isolate the prior
defect from adaptation, establish convergence of the deposited sampler in
other settings, or quantify effects on the published analysis.

## Next checks

Check the implications of the historical sampler's lagged prior and trace
the published-run code and settings before drawing an inference about the
published analyses. No contact with the authors has been made; outreach
remains Barry's decision.
