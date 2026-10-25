# Independent checks of the recoverability contract

These support the [Codex cross-review](../../ideas/2026-10-25-recoverability-review-codex.md)
of Claude's 25 October draft. The original files under
`data/recoverability-contract/` are preserved.

Run `OPENBLAS_NUM_THREADS=1 python data/recoverability-review/check.py`.
It writes [checks.json](checks.json). The recorded run used NumPy 1.26.4,
seed 123, and one million draws per deadline comparison; it took under a
second. Source hashes in the output identify the reviewed inputs. The
independent reviewer also replayed both original scripts to temporary files;
their JSON matched the committed results exactly.

The finite-K counterexample, zero-abundance probabilities and eventual
extinction calculation are analytic. Deadline probabilities use Monte Carlo
draws from the exact distribution of the limiting W variable, then the
**approximate** mapping from W to hitting time. They are not exact
first-passage probabilities. The import comparison uses the limiting gamma
law for immigration continuing indefinitely, with the rate rounded to 3.303;
Claude's original sampling truncates arrivals at time 60. This difference is
negligible for the displayed comparison, but the two constructions are not
identical.

For immigration rate m, individual birth b=2 and death d=1, integrating the
single-lineage survival probability over arrival times gives
`P(A(t)=0)=(1/(2*exp(t)-1))**(m/2)`. The limiting immigration contribution
has gamma shape m/2 and scale 2. With a fixed number a of standing founders,
the number with positive W is binomial with probability r/b, and their summed
W is gamma with that count as shape and b/r as scale. These mixture laws
avoid allocating a large founder-by-replicate array.

The review derives the timing-error scale and the mean/variance identity
used to distinguish structural identification from practical discrimination.
No biological parameters are estimated and no empirical conclusions follow
from these counterexamples.
