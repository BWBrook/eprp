---
id: inditek-2
name: INDITEK-2.0
kind: model
domain: simulation
languages: [Python]
home: https://github.com/INDITEK-eco-evo-Model/INDITEK-2.0
repo: https://github.com/INDITEK-eco-evo-Model/INDITEK-2.0
paper: [10.1111/2041-210x.70422]
licence: "Zenodo 22079167 deposit CC BY 4.0; GitHub repository has no stated licence"
release: {version: "Zenodo 22079167; GitHub ae26596", checked: 2026-10-28}
maintenance: {state: slow, last_commit: 2026-09-17, checked: 2026-10-28}
tier: T0
validated_uses: []
environment: {route: none, lockfile: none, host: deep-server}
blockers: ["sampler initial-prior inconsistency", "saved proof chain incompatible with deposited sampler under proof settings", "no pinned production environment"]
related_sources: []
eprp_questions: [B-005, Q-007, Q-010, Q-027, Q-040]
entry: {created: 2026-10-28, updated: 2026-10-28, by: Codex, reviewed: "controlled counterexample; broader independent review pending"}
---

# INDITEK-2.0

INDITEK-2.0 is a Python spatial marine-diversification model with a
Metropolis–Hastings inverse-modelling layer. It integrates diversification
on changing palaeogeographic particles driven by environmental fields and
compares simulated modern diversity with a target. The deposited `proof`
example uses synthetic observations. It is a possible component for B-005,
but its ability to distinguish competing biological mechanisms is not yet
established.

## Source and current status

The published software and data deposit is
[Zenodo 22079167](https://zenodo.org/records/22079167), labelled CC BY 4.0.
The GitHub repository does not state a licence. Its README says Python
3.8–3.9, whereas the pinned requirements listed in the tranche-5 scope need
a newer Python; no environment has yet been built here. The full deposit
matches its provider MD5 and passes ZIP integrity checks; its SHA-256 is
recorded in the [review](../reviews/2026-10-28-inditek-sampler/README.md).

**Do not rely on its inverse sampler yet.** A deterministic
[controlled test and trace review](../reviews/2026-10-28-inditek-sampler/README.md)
found that the archived sampler initialises the Gaussian prior incorrectly;
the error affects transitions before the first acceptance. A saved proof
chain also contains a transition inconsistent with the deposited sampler's
rule and proof settings. In three additional variants, the saved traces also
contain later rejections of improved fits that are inconsistent with that
sampler's stated priors and rule. These findings leave the generating code or
settings unresolved. They do not establish the effect on published
conclusions. The forward model has not yet been independently run or
validated here.

An earlier 4 June GitHub sampler and its Q10 prior settings are compatible
with all 146,286 finite-RSS saved transitions under a necessary acceptance
check, unlike the later deposited sampler. This does not uniquely establish
which code generated the chains or validate its posterior; the earlier code
evaluates the proposed Gaussian prior at the current Q10.
In a prespecified flat-likelihood synthetic diagnostic, its four chains
departed markedly from the known Gaussian target and two stalled; this tests
the historical implementation and its adaptation together, not the published
biological conclusions. The later sampler tracked the simple target in the
same diagnostic.

## Next steps

Verify the complete deposit and its chain provenance, and determine whether
there is an author-provided source/settings combination that explains the
saved trace. Characterise the forward model with analytically controlled
cases and deposited outputs before deciding whether a larger calibration
campaign would answer a biological question. Separate reproducibility of
one run, recovery under simulated data, and suitability for real
palaeobiological inference. Author contact remains in Barry's outreach queue.

Herrero-Gascón et al. (2026), *Methods in Ecology and Evolution*,
DOI 10.1111/2041-210x.70422; software deposit DOI 10.5281/zenodo.22079167.
