"""STAT.exe: deterministic statistical tools, Python standard library only.

Educational reference. No LLM, autonomous execution, or causal inference.
Run: python examples/stat_agent.py
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from statistics import mean, median, stdev
from typing import Sequence


def _numeric(values: Sequence[float], *, min_n: int = 2) -> list[float]:
    if isinstance(values, (str, bytes)):
        raise TypeError("Expected a sequence of numeric observations")
    result = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("All observations must be numeric (not bool)")
        number = float(value)
        if not isfinite(number):
            raise ValueError("NaN and infinite values are not permitted")
        result.append(number)
    if len(result) < min_n:
        raise ValueError(f"At least {min_n} observations are required")
    return result


@dataclass(frozen=True)
class Summary:
    n: int
    mean: float
    median: float
    sample_std: float
    minimum: float
    maximum: float


def describe(values: Sequence[float]) -> Summary:
    x = _numeric(values)
    return Summary(len(x), mean(x), median(x), stdev(x), min(x), max(x))


def pearson(x_values: Sequence[float], y_values: Sequence[float]) -> float:
    x, y = _numeric(x_values), _numeric(y_values)
    if len(x) != len(y):
        raise ValueError("Paired variables must have equal lengths")
    mx, my = mean(x), mean(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    denom = sqrt(sum(v*v for v in dx) * sum(v*v for v in dy))
    if denom == 0:
        raise ValueError("Correlation undefined for constant variable")
    return sum(a*b for a, b in zip(dx, dy)) / denom


@dataclass(frozen=True)
class Regression:
    n: int
    intercept: float
    slope: float
    r_squared: float


def simple_ols(x_values: Sequence[float], y_values: Sequence[float]) -> Regression:
    x, y = _numeric(x_values), _numeric(y_values)
    if len(x) != len(y):
        raise ValueError("Paired variables must have equal lengths")
    mx, my = mean(x), mean(y)
    sxx = sum((v - mx)**2 for v in x)
    if sxx == 0:
        raise ValueError("Regression undefined for constant predictor")
    slope = sum((a-mx)*(b-my) for a, b in zip(x, y)) / sxx
    intercept = my - slope*mx
    sse = sum((b-(intercept+slope*a))**2 for a, b in zip(x, y))
    sst = sum((b-my)**2 for b in y)
    r2 = 1 - sse/sst if sst > 0 else (1.0 if sse == 0 else float("nan"))
    return Regression(len(x), intercept, slope, r2)


if __name__ == "__main__":
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 5, 4, 5]
    print("STAT.exe // ANALYSIS READY")
    print("Summary:", describe(y))
    print("Pearson r:", round(pearson(x, y), 4))
    print("OLS:", simple_ols(x, y))
