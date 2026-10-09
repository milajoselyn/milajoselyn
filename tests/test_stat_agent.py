"""Regression tests for STAT.exe reference computations."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from stat_agent import describe, pearson, simple_ols


class StatAgentTests(unittest.TestCase):
    def test_describe(self):
        s = describe([1, 2, 3, 4, 5])
        self.assertEqual(s.n, 5)
        self.assertEqual(s.mean, 3)
        self.assertEqual(s.median, 3)
        self.assertAlmostEqual(s.sample_std, 2.5 ** .5)

    def test_pearson(self):
        self.assertAlmostEqual(pearson([1, 2, 3], [2, 4, 6]), 1)
        self.assertAlmostEqual(pearson([1, 2, 3], [6, 4, 2]), -1)

    def test_ols(self):
        fit = simple_ols([1, 2, 3], [3, 5, 7])
        self.assertAlmostEqual(fit.slope, 2)
        self.assertAlmostEqual(fit.intercept, 1)
        self.assertAlmostEqual(fit.r_squared, 1)

    def test_validation(self):
        with self.assertRaises(ValueError):
            pearson([1, 1, 1], [2, 3, 4])
        with self.assertRaises(ValueError):
            simple_ols([1, 2], [1])
        with self.assertRaises(ValueError):
            describe([1, float("nan")])
        with self.assertRaises(TypeError):
            describe([True, 2])


if __name__ == "__main__":
    unittest.main()
