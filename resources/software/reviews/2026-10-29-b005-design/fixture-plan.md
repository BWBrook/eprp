# B-005 implementation fixture declared before execution

29 October 2026, Packages Codex. No fit or production ensemble.
Use the checksum-pinned Zenodo 22079167 source and existing Python 3.12
forward environment. Call the actual `inditek_alphadiv` and `alphadiv_expo`
functions on three stationary, continuously active shelf points, time slices
541, 531 and 521 Ma, constant positive rho 0.1/Myr, initial diversity 1,
and capacities 2, 5 and 10. There is no colonisation in this fixture.
Compare each interval with independently calculated first-year Euler and
nine-year analytic logistic/exponential solutions, at absolute tolerance
1e-10. Check a zero-rate common-output control and the large-finite-K limit
(K=1e30, tolerance 1e-10). Explicitly test native K=infinity as a diagnostic,
not as the adopted zero-feedback route. Add a forced-extinction-year control
at array index 15, rho=-0.5, comparing against independent annual recurrences
for the second interval. Record finite outputs, masks, unchanged inputs and
repeat-call determinism. Exercise native endpoint gridding on synthetic
0.5-degree shelf cells shared by both branches; report an illustrative slope
of log(1+gridded diversity) against absolute latitude. This checks a downstream
calculation, not palaeobiological sampling or identification. Retain every
outcome and source hashes. No altered sampler or source is used.

## Full-history viability supplement (before its two evaluations)

Board 76/2521 authorises exactly one proof and one expo forward call using
[161,19,0.035,0.002,2], the archived full history/forcing, D0=1 and native
endpoint grid. No fit, horizon change or rescue after a failure. Use the
existing locked environment, one CPU and a one-core-hour ceiling; preserve
errors/nonfinite values. Save raw X/Y/diversity grids on deep, hashes,
finite/NaN/Inf counts and small descriptive endpoint summaries. RSS from
the existing wrapper is incidental and is not an observation law for B005.
