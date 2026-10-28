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
tier: T2
validated_uses: ["rate and capacity formulas on specified analytic controls", "three deposited proof-proposal diversity vectors"]
environment: {route: uv, lockfile: env/uv.lock, python: "3.12", host: deep-server}
blockers: ["sampler prior inconsistency", "saved chain generating source and observations unresolved", "saved chain diagnostics poor", "deposited proposal RSS not reproduced"]
related_sources: []
eprp_questions: [B-005, Q-007, Q-010, Q-027, Q-040]
entry: {created: 2026-10-28, updated: 2026-10-28, by: Codex, reviewed: "forward and saved-chain audit; independent numerical check by GPT-6.1 Sol"}
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
3.8–3.9, whereas its pinned requirements need a newer Python. An isolated
[Python 3.12 environment](env/pyproject.toml) was locked and used for the
forward checks; its requirements match the deposit. The full deposit
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
conclusions.

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

## Forward model and retained chains

Specified analytic rate and carrying-capacity controls pass, and three
saved `proof` proposal diversity vectors reproduce within 5 × 10⁻¹⁴.
Their saved RSS values do not reproduce; the declared combined forward
replay therefore **fails**, even though an independent calculation matches
the rerun's scores. The saved residual arrays are all zero, so they cannot
resolve the difference. At nominal reference parameters the rerun also
does not reproduce the separately deposited `D_proof` reference map. The
archive's observation and generating-code provenance remains unresolved.

Analyses of all six saved chains after the notebook's 2,000-state burn-in
show poor convergence for several parameters. For example, proof Q10 has
rank-normalised split R-hat 1.623 and bulk ESS 10 out of 18,018 nominal
states. The temperature-disabled case has two chains in a different
parameter region; its trace-plot mean is calculated from four chains,
whereas the notebook's histogram pools all six. Those outputs have not
been linked definitively to specific article figures.

The [forward and claims review](../reviews/2026-10-28-inditek-forward-and-claims/README.md)
records the checks, locked environments, result receipts and limits. If
these archived chains produced the article's proof-of-concept or sensitivity
results, the posterior uncertainty and sensitivity summaries need
re-evaluation. We cannot yet quantify the impact on the article's claims.
The narrow T2 status covers the tested forward calculations, not the
inverse sampler or biological validation.

## Next steps

Identify the code, priors, observed map, seeds and chains underlying each
article figure, then re-fit those data with a verified sampler and adequate
independent-chain diagnostics. Repeated known-truth data sets can assess
coverage. Separate reproduction of one run, recovery under simulated data,
and suitability for real palaeobiological inference. Author contact remains
in Barry's outreach queue.

Herrero-Gascón et al. (2026), *Methods in Ecology and Evolution*,
DOI 10.1111/2041-210x.70422; software deposit DOI 10.5281/zenodo.22079167.
