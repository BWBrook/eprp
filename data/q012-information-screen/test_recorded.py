# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["numpy==2.1.3", "scipy==1.15.3"]
# ///
"""Controls for the prospectively fixed recorded-only detector."""

import copy
import tempfile
import unittest
from pathlib import Path

import numpy as np

import recorded as R


class RecordedControls(unittest.TestCase):
    def fixture(self):
        return dict(ids=[0,1,2],par={0:-1,1:0,2:0},tO={0:70,1:68,2:67},
                    tE={0:0,1:20,2:5},label={0:"present",1:"ext",2:"bif"})

    def test_hazard_integration_boundaries_and_pre_cut(self):
        self.assertEqual(R.cumulative_hazard(5,2,np.array([2,3])),8)
        self.assertEqual(R.cumulative_hazard(3,0,np.array([2,3])),6)
        self.assertEqual(R.cumulative_hazard(4,4,np.array([2,3])),0)
        self.assertAlmostEqual(R.cumulative_hazard(72.44,66.05),.065*(72.44-66.05),places=12)
        with self.assertRaises(ValueError):
            R.cumulative_hazard(2,3)

    def test_quadrature_control_and_analytic_limits(self):
        controls=R.P["quadrature_control"]
        nodes,weights=np.polynomial.hermite.hermgauss(controls["comparison_nodes"])
        for extinct in (0,1):
            hazard=np.array(controls["hazards"])
            delta=np.full(len(hazard),extinct)
            difference=np.abs(R.risk_proxy(hazard,delta)-R.risk_proxy(hazard,delta,nodes,weights))
            self.assertLess(float(difference.max()),controls["absolute_tolerance"])
        self.assertAlmostEqual(float(R.risk_proxy([0],[0])[0]),0,places=12)
        self.assertAlmostEqual(float(R.risk_proxy([0],[1])[0]),R.P["sigma"],places=12)

    def test_recorded_only_inputs_and_arbitrary_identifiers(self):
        observed=self.fixture()
        baseline=R.features(observed)
        polluted=copy.deepcopy(observed)
        polluted.update(x={0:1e6,1:-1e6},true_parent={0:2,1:-1},capped=True,
                        cohort_attempts=99999,used={0:{1:-1e9}})
        np.testing.assert_array_equal(R.features(polluted),baseline)
        remap={0:56,1:23,2:77}
        permuted=dict(ids=[77,56,23],par={remap[i]:remap.get(p,-1) for i,p in observed["par"].items()})
        for key in ("tO","tE","label"):
            permuted[key]={remap[i]:v for i,v in observed[key].items()}
        np.testing.assert_allclose(R.features(permuted),baseline,atol=1e-12)

    def test_sister_pair_identity_and_empty_history(self):
        observed=self.fixture()
        q=R.risk_proxy(np.array([R.cumulative_hazard(observed["tO"][i],observed["tE"][i]) for i in observed["ids"]]),[0,1,0])
        self.assertAlmostEqual(R.features(observed)[2],q[1]*q[2]/np.sqrt(2),places=12)
        np.testing.assert_array_equal(R.features(dict(ids=[])),np.zeros(8))

    def test_linear_fit_development_only_and_threshold_isolation(self):
        rng=np.random.default_rng(280920001)
        null=rng.normal(size=(50,8))
        alt=rng.normal(size=(50,8))+.2
        fit=R.fit_discriminant(null,alt)
        self.assertGreater(np.mean([R.score(x,fit) for x in alt]),np.mean([R.score(x,fit) for x in null]))
        frozen=copy.deepcopy(fit)
        cal={"calibration_null":list(range(2000)),"calibration_zero":list(range(2000,4000))}
        chosen=R.choose_threshold(cal)
        self.assertEqual(chosen["threshold"],chosen["calibration"]["calibration_zero"]["upper_threshold"])
        self.assertEqual(fit,frozen)
        with self.assertRaisesRegex(ValueError,"only both endpoint-null"):
            R.choose_threshold(dict(**cal,evaluation_alternative=[9999]*2000))
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"coefficients.json"
            path.write_text("{}")
            with self.assertRaisesRegex(ValueError,"SHA256 mismatch"):
                R.run("evaluate",Path(folder)/"evaluation",path,"wrong-hash")

    def test_all_panel_seeds_independent_from_oracle_and_each_other(self):
        seen=set()
        for protocol in (R.O.PROTOCOL,R.P):
            for ensemble in protocol["ensembles"]:
                for panel in protocol["panels"].values():
                    seeds=set(range(ensemble["seed_base"]+panel["seed_offset"],
                                    ensemble["seed_base"]+panel["seed_offset"]+panel["n"]))
                    self.assertFalse(seen.intersection(seeds))
                    seen.update(seeds)


if __name__=="__main__":
    unittest.main(verbosity=2)
