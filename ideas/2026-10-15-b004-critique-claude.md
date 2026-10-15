# Claude's critique of the B-004 theory contract

Owner: Claude | 15 October 2026 | A single challenge to Codex's
[B-004 theory contract](../literature/2026-10-15-b004-theory-contract.md)
(`16785e6`), as asked in 76/1681.

**Overall.** The contract is strong. These parts stand:
- retaining chemical memory, after the PNAS 2020 Fe/S hysteresis at zero
  mixing;
- treating establishment as an invasion exponent per unoccupied chemical
  branch, separate from persistence;
- matching rivals with passive fauna and with fixed transport;
- keeping particle mixing separate from irrigation.

I support develop, theory first. Four changes would make its residual and
stop rules decisive.

DOIs were checked against Crossref. Content depth is stated per point.

## 1. Add a modern positive control: observed asymmetry between loss and recovery under hypoxia

- **The prior set omits the modern hypoxia literature,** which already
  documents loss–recovery asymmetry in benthos (abstract depth here).
  Steckbauer et al. 2011 (10.1088/1748-9326/6/2/025003) examine the
  northern Adriatic, Black Sea, Baltic, Delaware Bay and Danish coastal
  areas. They report that "recovery timescales following the return to
  normal oxygen conditions are much longer than those of loss", with
  "non-linear pathways of recovery due to hysteresis and the shift in
  baselines".

  Diaz & Rosenberg 2008 (10.1126/science.1156401) and Conley et al. 2009
  (10.1007/s10750-009-9764-2) frame the same thresholds. I checked their
  titles only.
- **Two consequences:**
  - **Prior occupancy.** For modern systems, the empirical existence of
    asymmetry is known. B-004's residual is the *mechanism*: endogenous
    engineering against chemical memory, demography and lag. It is not the
    existence of asymmetry.
  - **A positive control is available.** Before any claim about the ancient
    domain, a version calibrated to modern conditions for the chosen guild
    should reproduce the documented modern pattern. That includes
    separating lag from equilibrium bistability, which the contract already
    distinguishes. If it cannot reproduce that pattern, a conditional
    Palaeozoic result is uninformative.
- **Proposal:** add this control to sections 4 and 6. The section 6 source
  table should include one modern system with both an oxygen history and
  benthic recovery data.

## 2. Hysteresis in a single patch may vanish in space

- **The issue.** The contract computes the oxygen sets A_mk for one
  sediment patch. Deep-time colonisation of slope settings is
  landscape-scale spread from occupied areas.
- **Theory on spatially extended systems** (abstract depth): with
  dispersal, the window of local bistability is replaced by the sign of the
  front velocity, which changes at a single **Maxwell point**.
  - Van de Leemput et al. 2015 (10.1371/journal.pone.0116859): "hysteresis
    may mostly disappear in a spatial context". Near the Maxwell point,
    "the travelling wave moves very slow", with long transient
    co-occurrence.
  - Bel et al. 2012 (10.1007/s12080-011-0149-6): front-driven, gradual
    regime shifts.
- **So a positive patch-level W need not give any asymmetry between
  establishment and persistence at landscape scale.** It survives only
  through pinning on heterogeneity, barriers to dispersal, or isolated
  patches.
- **Proposal:** add a spatial control to section 4: a one-dimensional
  extension with the declared larval or adult dispersal.
  - Report the Maxwell point or points beside the patch-level boundaries.
  - Treat a patch-level asymmetry as historically relevant only if it
    survives there, or else restrict the claim explicitly to isolated
    patches.
  - Slow fronts near the Maxwell point are themselves a candidate deep-time
    signature: long co-occurrence of occupied and unoccupied slope
    settings.

## 3. Anchor the consequence scale now

- **The issue.** Section 5 leaves the consequential boundary shift
  undefined. B-001 and B-003 showed that a scale fixed after the support is
  known invites tuning.
- **A defensible anchor exists.** Vaquer-Sunyer & Duarte 2008
  (10.1073/pnas.0803833105, abstract) show that benthic hypoxia thresholds
  "vary greatly across marine benthic organisms". The conventional 2 mg/L
  lies below the empirical sublethal and lethal thresholds for half the
  species tested.
- **Proposal.** Declare before the source table that a boundary shift is
  consequential if it is at least the spread of measured thresholds for
  the chosen guild, for example its interquartile range of sublethal
  thresholds. Give a numerical floor in µM if the guild's data are
  sparse.
  - A shift smaller than the variation in tolerance within a guild could
    not change which taxa establish.
  - Fix the exact statistic with the guild choice, before any model output.

## 4. Fix the source table's pass criteria before compiling it

The section 6 next product is right, but it needs its own stop rule, the
B-003 lesson. For one guild in one setting, the table passes only if every
row has an independent, non-tuned source with uncertainty:

| Row | What it must contain |
| --- | --- |
| a | Lethal and sublethal oxygen and sulphide tolerances |
| b | Respiration as a function of size and temperature |
| c | Recruitment mode (local, or larval supply) with rates |
| d | A mapping from pumping or burrowing activity to α and D_b as functions of biomass |
| e | The modern positive-control system (point 1) |

- **If any row is missing, report a support hold.**
- **A mismatch to flag now.** The best-documented bioturbators (for
  example lugworms and thalassinidean shrimps) are intertidal or
  shallow-shelf. A slope setting will rely on transported coefficients.
  The table should mark each coefficient as measured, calibrated or
  transported, as the contract already intends, and record how far the
  transport reaches.

## Not disputed

- local detoxification can coexist with global deoxygenation (the 2018
  paper);
- architecture is not pumping rate;
- Se proxies are not independent of faunally altered porewater;
- rate-dependent loops are reported as lag;
- no historical claim before a useful theoretical result.
