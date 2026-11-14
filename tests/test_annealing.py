from __future__ import annotations

import math

import pytest

from optimise import fitness as fitness_module
from optimise.annealing import run
from optimise.common import BOUNDS, N_WEIGHTS

TARGET = [1.0, 2.0, -1.0, -3.0, 0.5, 4.0]


def fake_fitness(weights, n_games=6, seed=0):
    return -sum((w - t) ** 2 for w, t in zip(weights, TARGET))


@pytest.fixture(autouse=True)
def _patch_fitness(monkeypatch):
    monkeypatch.setattr(fitness_module, "fitness", fake_fitness)


def test_spends_exactly_budget():
    result = run(budget=50, seed=1)
    assert len(result.history) == 50


def test_history_never_decreases():
    result = run(budget=80, seed=2)
    for i in range(1, len(result.history)):
        assert result.history[i] >= result.history[i - 1]


def test_is_seeded():
    a = run(budget=60, seed=4)
    b = run(budget=60, seed=4)
    assert a.best_weights == b.best_weights
    assert a.best_fitness == b.best_fitness
    assert a.history == b.history


def test_always_accepts_improvement(monkeypatch):
    calls = {"n": 0}

    def always_improving(weights, n_games=6, seed=0):
        calls["n"] += 1
        return float(calls["n"])

    monkeypatch.setattr(fitness_module, "fitness", always_improving)
    result = run(budget=30, seed=0, T0=0.001, alpha=0.5)
    assert result.history == sorted(result.history)
    assert result.best_fitness == max(result.history)


def test_accepts_worse_when_hot(monkeypatch):
    import optimise.annealing as annealing_module

    sequence = [0.0, -0.01] * 100

    def tiny_step_fitness(weights, n_games=6, seed=0):
        return sequence.pop(0)

    monkeypatch.setattr(fitness_module, "fitness", tiny_step_fitness)
    monkeypatch.setattr(annealing_module.random.Random, "random", lambda self: 0.0)
    result = run(budget=10, seed=0, T0=1e6, alpha=0.9999999)
    assert len(result.history) == 10


def test_rejects_worse_when_cold(monkeypatch):
    values = [10.0] + [1.0] * 50

    def dropping_fitness(weights, n_games=6, seed=0):
        return values.pop(0) if values else 1.0

    monkeypatch.setattr(fitness_module, "fitness", dropping_fitness)
    result = run(budget=20, seed=0, T0=1.0, alpha=0.0)
    assert result.best_fitness == 10.0
    assert all(value == 10.0 for value in result.history[1:])


def test_temperature_cools_geometrically():
    result = run(budget=10, seed=0, T0=10.0, alpha=0.97)
    expected_final_T = 10.0 * (0.97 ** 9)
    assert math.isclose(result.extra["final_temperature"], expected_final_T, rel_tol=1e-9)


def test_weight_0_stays_fixed():
    result = run(budget=100, seed=3)
    assert result.best_weights[0] == 1.0
    assert len(result.best_weights) == N_WEIGHTS
    for w in result.best_weights:
        assert BOUNDS[0] <= w <= BOUNDS[1]


def test_zero_budget_returns_empty_result():
    result = run(budget=0, seed=0)
    assert result.history == []
    assert result.best_weights is None


def test_runs_with_tiny_budget():
    result = run(budget=1, seed=0)
    assert len(result.history) == 1
    assert result.best_weights is not None
