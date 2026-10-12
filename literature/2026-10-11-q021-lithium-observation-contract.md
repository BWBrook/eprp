# Q-021: a lithium observation contract before model coupling

Owner: Codex | 11 October 2026 | External-review finding F-04

**Decision:** retain lithium as a candidate constraint. The algebraic contract
below is ready for challenge; the empirical comparison is **not ready**.
Neither matched native trajectories nor their lithium conversions have been
obtained. This supersedes the marginal-overlap stopping rule in
[Claude's reply 3](../ideas/2026-10-11-phase2-claude-reply-3.md), and develops
the [earlier capability check](2026-10-11-q021-lithium-and-model-capability.md).

**Later support check, 11 October:** the
[original Shangsi table](../data/q021-shangsi-support/README.md) is now obtained.
It contains only one Induan Li sample. Shangsi alone is retired as a recovery
sequence; its possible contribution to a joint comparison remains open.

**Recovery crosswalk, 12 October:** [Shanggang and all six Rauzi sections](../data/q021-recovery-support/README.md)
are now extracted. Shanggang has 16 stored Li values through the Olenekian;
Festningen and Waiheke extend into the Anisian, but Dataset S3 supplies
depths rather than numerical ages. Rauzi's SI explicitly allows authigenic
clay formation after sediment deposition. Consequently the archive mapping
below needs formation-time support as well as a depositional age model.

## One bounded comparison

Compare a terrestrial-function-loss scenario based on Xu/SCION with a
silicifier-loss/reverse-weathering scenario based on Isson. These are proposed
restricted scenarios, not mutually exclusive biological explanations. Each
must supply **both** terrestrial weathering and marine removal histories,
including an explicit reference treatment for the component it holds fixed.
One river-input history versus one burial-output history is not a complete
pair of lithium predictions.

The initial archive candidate was Cao's **Shangsi carbonate record**.
The source-table check found five Permian and one Induan Li sample, spanning
259.3818–251.4093 Ma. This rejects Shangsi alone as a sequence through Early
Triassic recovery. Measured values, both age columns and screening flags are
now preserved; age covariance and overlap with complete model histories
remain unverified. The later crosswalk identifies Festningen and Waiheke as
complementary recovery candidates, with gaps, local mixing and formation-time
limits still unresolved; it does not select a ready joint numerical series.

Published implementations also differ in forcing, reservoirs and calibration.
Comparing their unmodified predictions would compare those complete packages.
Attributing a difference to biological function needs matched external carbon
forcing and an explicit account of the remaining structural differences.

## Native output to observation

| Component | Inspected support | Required contract / present gap |
| --- | --- | --- |
| Xu continental weathering | Pinned code stores `silw`, `basw`, `granw`; `silw = basw + granw`. Their scale is tied to carbon-cycle flux parameters | Record native units and stoichiometric convention before export. They are not mol Li/yr. No time series was exported here |
| Isson marine removal | Published carbon–silica model describes dynamic clay formation and silica partitioning | Obtain the dimensional authigenic Si removal, not merely its fraction of total export; verify code version, units and time vector. Native source code/trajectories remain uninspected |
| Dissolved river Li | Neither inspected native output is this quantity | Map each lithological weathering component to mol Li/yr, including source composition, dissolution and secondary retention; jointly specify river isotope composition |
| Marine Li burial | A silica flux is insufficient | Convert mol Si/yr to mol Li/yr with mineral- and process-dependent uptake; allow associated fractionation to covary with uptake |
| Other fluxes and inventory | Required by Li balance | Supply hydrothermal input, other sinks, initial Li inventory and isotope composition for each scenario. Do not make an omitted term zero by default |
| Carbonate measurement | Cao supplies an archive interpretation and screening procedure; six Shangsi source rows are now extracted | Predict measured carbonate with an explicitly signed offset, contamination/diagenesis and analytical uncertainty. Source averaging, screening and offset-sign flags remain unresolved; no silent repairs |
| Time and evidence use | Published records and model forcings use different constraints | Freeze the numerical interval only after the sample/age and trajectory crosswalk. Preserve shared chronology; identify every datum used for forcing, priors, selection or evaluation |

For example, after checking the native weathering convention, a proposed
mapping is `F_riv = c_bas(t) basw(t) + c_gran(t) granw(t)`, where the `c`
coefficients have units mol Li per native weathering-flux unit. Similarly,
`F_sed = c_rw(t) S_rw(t)` needs a Li:Si uptake coefficient if `S_rw` is
mol Si/yr. These are dimensional placeholders, **not verified conversions**.
Unrestricted coefficients could absorb the very contrast being tested.
Fixed coefficients could create it. Their constraints and covariation must
come from evidence or declared sensitivity assumptions.

## Minimal physical and archive equations

Use forward elapsed years, not a decreasing Ma age, for the balance. Let
`N` be total oceanic Li in mol, `R = 7Li/6Li`, and `q = R/(1+R)` the heavy
isotope fraction. For input and output fluxes in mol Li/yr:

```text
dN/dt       = sum(F_in) - sum(F_out)
d(N q)/dt   = sum(F_in q_in) - sum(F_out q_out)
R_out,k     = alpha_k R_sw
delta7Li_sw = 1000 (R_sw/R_standard - 1)
```

This is a proposed exact isotope bookkeeping convention, not a reproduction
of either source implementation. Declare the isotope standard and the sign
and definition of every fractionation parameter. Do not substitute an
instantaneous steady-state balance for a transient prediction without
justifying the time-scale approximation.

For a pure carbonate component define, rather than infer from notation,
`b_i = delta7Li_carbonate - delta7Li_sw`; then its ideal value is
`delta7Li_sw(t_i) + b_i`. For mixtures, mix isotope amounts (or heavy-isotope
fractions weighted by Li amounts), not sediment mass fractions or unweighted
delta values. The measurement model must include sample age uncertainty,
section-level/shared offsets and analytical error. A shared unknown offset
can cancel in a temporal contrast; time-varying archive alteration need not.
For the siliciclastic archive, depositional age need not equal the formation
time of its authigenic component. Where formation is delayed or distributed,
the mapping must integrate over a justified formation-time distribution using
Li amounts and isotope fractions. No such distribution has yet been obtained;
assigning the seawater state at the sediment's age would impose an unsupported
instantaneous-formation assumption.

The same equation form is appropriate for both scenarios. Evidence-supported
mechanism-specific dependencies remain permitted; identical fixed priors
are not a substitute for a fair comparison. A one-way Li calculation can
test observable consequences of supplied fluxes. It does not itself establish
their climatic effect or make the source models causally comparable.

## Joint comparison and outcome-neutral gate

Before testing data, specify the measured vector, evaluation subset,
scientifically consequential contrast and a joint predictive score or
decision statistic. Propagate nuisance and shared age/measurement uncertainty
through the **whole vector**. Calibrate error and discrimination under both
scenarios at the actual sampling design; include an adequacy check so the
procedure can reject both. Average performance under a convenient prior is
insufficient if defensible nuisance settings reverse the conclusion.

The external review's two-observation fixture is a valid warning: with a
shared offset SD of 10 and independent error SD 0.25, strongly overlapping
marginal bands coexist with a contrast SD of 0.354 and classification error
7.71e-9. This is hypothetical, not a lithium power estimate. Conversely,
separation conditional on an unsupported uptake conversion is not evidence
for a mechanism.

Record three possible outcomes:

1. **Informative discrimination:** the chosen observations separate specified
   scenarios under the justified nuisance contract. Interpret only that
   conditional comparison, without allocating causal shares of recovery.
2. **Informative limit:** a calibrated result constrains a specified mechanism
   prediction or shows that this record cannot discriminate a consequential
   contrast under stated assumptions. Preserve the answer and identify which
   additional measurement would help; do not infer biological equivalence.
3. **Unresolved:** missing conversions, trajectories, age support or inadequate
   precision prevent the test. Stop this route before coupling codebases;
   Q-021 remains scientifically open.

**Present outcome: 3.** Shangsi's table is obtained but does not supply the
proposed recovery sequence. A conditional one-post-onset design check shows
an amplitude/onset ambiguity in a simple response family; it is not an
empirical power estimate. Next identify a viable recovery record, then obtain
one complete pair of unit-checked flux histories with constrained conversions.
The 12 October crosswalk advances the first step to a concrete question:
can Festningen/Waiheke supply a coarse recovery contrast with constrained
depositional and authigenesis timing, mixing and shared correlation error?
A completed source contract, a numerically runnable adapter and demonstrated
discrimination are separate checkpoints. No adapter, source-model execution
or primary analysis has started.

## Source and access record

Targeted reinspection on 11 October; no broad novelty search. Cao's main-text
Methods and equations (1–2), available in the
[institutional PDF](https://earthsciences.osu.edu/sites/default/files/2022-11/s41561-022-01009-x.pdf),
support the two-input/two-sink Li balance and archive requirements; their
steady-state model is not the transient construction above. At this note's
initial checkpoint no supplement was verified; the later linked sample check
retrieved and inspected the official workbook/SI. No new numerical calibration
was fitted.

Xu source: commit `54fdfbe92692a63cf42e948d78fa7476ad33dbfb`,
[equations](https://github.com/ZhenXuJane/SCION_Xu2025/blob/54fdfbe92692a63cf42e948d78fa7476ad33dbfb/SCION_equations.m)
lines 499–547, 581–590, 832–836 and 859–861; locally cached
`SCION_initialise.m` lines 89–102 and 270 checked for scale/time conventions.
Exact exported dimensional metadata remains required.

Isson's [primary paper](https://doi.org/10.1038/s41467-022-31128-3), Results
and carbon–silica model description, was reinspected through the existing
Europe PMC text (PMC9206662); the publisher web request failed this round.
Rauzi's archive and filtering limitations remain as documented in the
[earlier source note](2026-10-11-q021-lithium-and-model-capability.md).
No source model was run and no original author was contacted.
