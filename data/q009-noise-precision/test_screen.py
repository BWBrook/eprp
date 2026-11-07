import unittest

import numpy as np

from screen import finite_variance_factor, metric, simulate


class ObservationChecks(unittest.TestCase):
    def test_multinomial_variance_and_joint_covariance(self):
        p = np.array([.2, .3])
        x = simulate(p, 8, 500, 1, 20000, np.random.default_rng(42))
        covariance = np.cov(x.reshape(-1, 2).T)
        np.testing.assert_allclose(np.diag(covariance), p*(1-p)/500, rtol=.02)
        self.assertAlmostEqual(covariance[0, 1]/(-.2*.3/500), 1, delta=.03)
        self.assertTrue(np.all(x.sum(axis=-1) <= 1))

    def test_overdispersed_counting_variance(self):
        p = np.array([.2, 0., .3])
        x = simulate(p, 8, 500, 2, 20000, np.random.default_rng(43))
        _, v = metric(x, np.array([.2, .1, .3]))
        expected = 2/500*np.sum(p*(1-p)/np.array([.2,.1,.3])**2)
        self.assertAlmostEqual(v.mean()/expected, 1, delta=.03)
        self.assertTrue(np.all(x[..., 1] == 0))

    def test_zero_taxon_makes_cv_undefined_but_not_fixed_scale_variance(self):
        cv, v = metric(np.array([[.1, 0.], [.2, 0.], [.3, 0.]]), np.array([.2,.1]))
        self.assertTrue(np.isnan(cv))
        self.assertTrue(np.isfinite(v))

    def test_finite_ar1_covariance_includes_spacing(self):
        self.assertAlmostEqual(finite_variance_factor([1.,.5], .5), .75)
        self.assertAlmostEqual(finite_variance_factor([1.,0.], .5), .625)
        self.assertAlmostEqual(finite_variance_factor([1.,0.], 0.), .5)


if __name__ == '__main__':
    unittest.main()
