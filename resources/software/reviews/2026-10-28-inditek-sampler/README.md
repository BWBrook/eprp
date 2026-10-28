# INDITEK-2.0: initial-prior counterexample

28 October 2026, Codex. **Provisional source-specific finding:** the
[sampler at GitHub commit `ae26596`](https://github.com/INDITEK-eco-evo-Model/INDITEK-2.0/blob/ae26596ff82a3528f02f113e0d2465a82f5ef360/inditek_MCMC.py)
evaluates the
initial Gaussian prior differently from proposed-state priors. A controlled
test reproduces an incorrect first-step acceptance. The licensed Zenodo
deposit and its published chains were not yet checked against this source.
No claim about the published results or their practical sensitivity follows
from this counterexample alone.

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

The source SHA-256 and exact observed results are in
[`inditek_sampler_github_20261028.json`](../../bench/results/t5/inditek_sampler_github_20261028.json).
The SHA-256 of the tested source is
`ede1421d4a6db9d2883fd0f2d9152240afcaadcd730f0269602defa41cf9933c`.
It is read from GitHub for this check and is not redistributed here.
Reproduce the test with the exact source file and the pinned Python image:

```sh
docker run --rm -i --network none -v /path/to/source:/source:ro \
  eprp-sw/bench-py5:t5 python - /source/inditek_MCMC.py \
  < resources/software/bench/validate/t5_inditek_sampler_control.py
```

## Next checks

Verify whether the licensed [Zenodo deposit](https://zenodo.org/records/22079167)
contains the same code and whether its saved chains were made with it. Inspect
the proposed and accepted traces, including first acceptance and burn-in,
before assessing practical impact. A separate test of the stated adaptation
and output contracts may be warranted; this control does not test either.
Do not treat reproduction of deposited chains as posterior calibration. No
contact with the authors has been made; outreach remains Barry's decision.
