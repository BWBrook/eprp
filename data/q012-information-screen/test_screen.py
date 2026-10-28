# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["numpy==2.1.3", "scipy==1.15.3"]
# ///
"""Independent density, selection, stationary-variance and MC-bound controls."""

import math
import unittest

import numpy as np
from numpy.polynomial.hermite import hermgauss
from scipy.stats import multivariate_normal, norm

import screen as S


class OracleControls(unittest.TestCase):
    def fixture(self):
        return [dict(parent=-1,x=0.6,cohort=True),dict(parent=-1,x=-0.3,cohort=True),
                dict(parent=1,x=-0.8,cohort=True),dict(parent=0,x=0.2,cohort=False)]

    def test_full_joint_gaussian_density_and_forced_edge(self):
        lineages = self.fixture()
        x = [l["x"] for l in lineages]
        vals = []
        for rho in (.1,.4):
            covariance = .25*np.array([[1,0,0,rho],[0,1,rho,0],
                                      [0,rho,1,0],[rho,0,0,1]])
            vals.append(multivariate_normal.logpdf(x,mean=np.zeros(4),cov=covariance))
        stat,edges = S.score(lineages)
        self.assertEqual(edges,2)
        self.assertAlmostEqual(stat,vals[1]-vals[0],places=12)
        without_forced = self.fixture()
        without_forced[2]["parent"] = -1
        with self.assertRaisesRegex(ValueError,"forced cohort"):
            S.score(without_forced)
        # Mutation control: dropping that edge is numerically wrong, not merely a flag error.
        forced_only = self.fixture()[:3]
        self.assertGreater(abs(S.score(forced_only)[0]),.05)

    def test_stationary_variance_not_fixed_innovation_variance(self):
        rng = np.random.default_rng(280800001)
        root = rng.normal(0,.5,200000)
        for rho in (.1,.4):
            daughter = rho*root+.5*math.sqrt(1-rho*rho)*rng.standard_normal(len(root))
            self.assertAlmostEqual(float(np.var(daughter)),.25,delta=.003)
        lineages=self.fixture()
        xp,xd=lineages[1]["x"],lineages[2]["x"]
        correct=norm.logpdf(xd,.4*xp,.5*math.sqrt(1-.4**2))-norm.logpdf(xd,.1*xp,.5*math.sqrt(1-.1**2))
        wrong=norm.logpdf(xd,.4*xp,.5)-norm.logpdf(xd,.1*xp,.5)
        self.assertGreater(abs(correct-wrong),.05)

    def test_cohort_selection_constant_is_required_for_normalized_ratio(self):
        nodes,weights=hermgauss(80)
        xp=.5*math.sqrt(2)*nodes[:,None]
        innovation=math.sqrt(2)*nodes[None,:]
        weight=weights[:,None]*weights[None,:]/math.pi
        def integrate(rho,weighted_lr=False):
            xd=rho*xp+.5*math.sqrt(1-rho*rho)*innovation
            survival=np.exp(-2*np.exp(xp-.125)-1.3*np.exp(xd-.125))
            value=survival
            if weighted_lr:
                loglr=norm.logpdf(xd,.4*xp,.5*math.sqrt(1-.4**2))-norm.logpdf(xd,.1*xp,.5*math.sqrt(1-.1**2))
                value=survival*np.exp(loglr)
            return float(np.sum(weight*value))
        z0,z1=integrate(.1),integrate(.4)
        weighted=integrate(.1,True)
        self.assertAlmostEqual(weighted,z1,places=12)
        self.assertGreater(abs(z1/z0-1),.01)
        self.assertAlmostEqual((weighted/z0)*(z0/z1),1,places=12)

    def test_primary_generator_cap_and_forced_edge(self):
        lineages,info=S.GEN.generate(280800002,{"lineage_cap":12,"lambda0":1.0})
        self.assertTrue(info["capped"])
        self.assertEqual(len(lineages),12)
        self.assertEqual(S.score(lineages)[1],1)
        self.assertEqual(sum(l["cohort"] and l["parent"]>=0 for l in lineages),1)
        self.assertTrue(all(l["end"]>S.GEN.C for l in lineages if l["cohort"]))
        # Conditional event/exposure/stopping density cancels at a fixed accepted X.
        changed=[dict(l) for l in lineages]
        for l in changed:
            l["E"]={0:87.0}
            l["end"]=75.0
            l["true_buds"]=123
        self.assertEqual(S.score(changed),S.score(lineages))

    def test_threshold_rank_coverage_and_binomial_endpoints(self):
        cal=norm.ppf((np.arange(2000)+.5)/2000)
        bracket=S.threshold_bracket(cal,.05,.005)
        self.assertGreaterEqual(bracket["exact_bracket_coverage"],.995)
        self.assertLess(bracket["lower"],norm.ppf(.95))
        self.assertGreater(bracket["upper"],norm.ppf(.95))
        self.assertEqual(bracket["nominal_rank"],1901)
        self.assertEqual(S.cp_interval(0,2000)[0],0)
        self.assertEqual(S.cp_interval(2000,2000)[1],1)
        self.assertTrue(math.isinf(S.threshold_bracket([0.0],.05,.005)["upper"]))

    def test_seeds_disjoint_and_frozen_variance(self):
        seen=set()
        self.assertEqual(S.PROTOCOL["hypotheses"]["sigma"],.5)
        self.assertEqual(S.GEN.CFG["generator"]["sigma"],.5)
        for ensemble in S.PROTOCOL["ensembles"]:
            for panel in S.PROTOCOL["panels"].values():
                start=ensemble["seed_base"]+panel["seed_offset"]
                seeds=set(range(start,start+panel["n"]))
                self.assertFalse(seen.intersection(seeds))
                seen.update(seeds)


if __name__=="__main__":
    unittest.main(verbosity=2)
