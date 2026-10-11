#!/usr/bin/env python3
"""Independent, deterministic review fixtures; no fossil-data analysis.

Python standard library only. Run `python checks.py` from any directory.
Writes checks_results.json next to this file. All inputs are hypothetical.
"""
from __future__ import annotations
import itertools
import json
import math
from pathlib import Path


def q042_bounds() -> dict:
    genera, species, lost_genera = 100, 500, 62
    mean_size = species / genera
    g = lost_genera / genera
    lower = g / mean_size
    upper = 1 - (1 - g) / mean_size
    # Both bounds attainable with the SAME baseline allocation, when only
    # genus survival and total baseline species richness are known.
    sizes = [1] * 99 + [401]
    assert len(sizes) == genera and sum(sizes) == species
    extinct = sizes[:lost_genera]
    survivors = sizes[lost_genera:]
    assert math.isclose(sum(extinct) / species, lower)
    assert math.isclose((species - len(survivors)) / species, upper)
    uniform_min = sum([5] * lost_genera) / species
    return {
        'assumption': 'Every surviving genus retains at least one member of the t0 species cohort.',
        'genera': genera, 'baseline_species': species, 'lost_genera': lost_genera,
        'mean_species_per_genus': mean_size,
        'mean_only_sharp_lower': lower, 'mean_only_sharp_upper': upper,
        'minimum_if_every_genus_has_five_species': uniform_min,
        'baseline_allocation_attaining_both_bounds': {'one_species_genera': 99, '401_species_genera': 1},
        'replacement_counterexample': {
            'description': 'All original species replaced by newly originated species within persistent genera.',
            'g': 0, 'm': 5, 'baseline_species_loss': 1.0,
            'formula_upper_without_baseline_survivor_assumption': 0.8,
            'meaning': 'Not a refutation of the conditional bound; shows why cohort retention is necessary.'
        },
        'register_upper_bound_grid': [
            {'g': g0, 'm': m, 'upper': 1 - (1 - g0) / m}
            for g0 in (0.56, 0.62, 0.79) for m in (3, 5, 9.5)
        ]
    }


def q021_joint_information() -> dict:
    # y = mechanism_mean + common_offset + independent_error.
    # Model A mean=(-1,+1), B=(+1,-1), equally probable a priori.
    offset_sd, noise_sd = 10.0, 0.25
    marginal_sd = math.hypot(offset_sd, noise_sd)
    contrast_sd = math.sqrt(2) * noise_sd
    error = 0.5 * math.erfc((2 / contrast_sd) / math.sqrt(2))
    bands = {str(mu): [mu - 1.96 * marginal_sd, mu + 1.96 * marginal_sd]
             for mu in (-1, 1)}
    assert bands['-1'][1] > bands['1'][0]
    assert error < 1e-7
    return {
        'common_offset_sd': offset_sd, 'independent_noise_sd': noise_sd,
        'marginal_95_percent_intervals': bands,
        'contrast_means_A_B': [2, -2], 'contrast_sd': contrast_sd,
        'equal_prior_optimal_classification_error': error,
        'meaning': 'Extensive pointwise prior-predictive overlap does not imply joint observational equivalence.'
    }


def q038_conditional_score() -> dict:
    # This is one admissible model, not a claim about code in EPRP.
    odds, d = [1., 2., 3., 4.], 2
    subsets = list(itertools.combinations(range(len(odds)), d))
    def dist(scale: float) -> list[float]:
        weights = [math.prod(scale * odds[i] for i in s) for s in subsets]
        z = sum(weights)
        return [w / z for w in weights]
    probabilities = dist(1)
    scaled = dist(7)
    assert math.isclose(sum(probabilities), 1)
    assert all(math.isclose(p, q) for p, q in zip(probabilities, scaled))
    normalizer = sum(math.prod(odds[i] for i in s) for s in subsets)
    return {
        'N': len(odds), 'D': d, 'odds': odds,
        'elementary_symmetric_normalizer': normalizer,
        'probabilities': [{'victims_one_based': [i + 1 for i in s], 'p': p}
                          for s, p in zip(subsets, probabilities)],
        'common_odds_multiplier_cancels': True,
        'uniform_conditional_probability': 1 / math.comb(len(odds), d),
        'conditional_uniform_log_score': -math.log(math.comb(len(odds), d)),
        'unconditional_bernoulli_log_score_at_p_half': len(odds) * math.log(0.5),
        'meaning': 'A fixed-loss-count target requires a conditional score; intercept/severity information is removed.'
    }


def q050_mixture() -> dict:
    # Two unchanged subpopulations, common within-population covariance I,
    # means (0,0) and (2,0). Mixing alone changes mean AND covariance.
    rows = []
    for w in (0., 0.25, 0.5, 0.75, 1.):
        mean = [2*w, 0.]
        covariance = [[1 + 4*w*(1-w), 0.], [0., 1.]]
        rows.append({'second_population_weight': w, 'mean': mean, 'covariance': covariance})
    assert rows[0]['covariance'] == rows[-1]['covariance']
    assert rows[2]['covariance'][0][0] == 2
    return {'within_population_covariance': [[1, 0], [0, 1]], 'rows': rows,
            'meaning': 'Composition alone generates covariance reorganisation and mean change; no within-population evolution is present.'}


def main() -> None:
    results = {'kind': 'Independent review calculations, not empirical estimates',
               'q042': q042_bounds(), 'q021': q021_joint_information(),
               'q038': q038_conditional_score(), 'q050': q050_mixture()}
    destination = Path(__file__).resolve().with_name('checks_results.json')
    destination.write_text(json.dumps(results, indent=2) + '\n')
    print('All four independent deterministic fixtures passed.')
    print(destination)

if __name__ == '__main__':
    main()
