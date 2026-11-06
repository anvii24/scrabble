from optimise.common import BOUNDS, N_WEIGHTS
from optimise.genetic import crossover, mutate, run

TARGET = [1.0, 2.0, -1.0, -3.0, 0.5, 4.0]


def fake_fitness(weights):
    return -sum((w - t) ** 2 for w, t in zip(weights, TARGET))


def test_stays_within_budget():
    result = run(budget=50, seed=1, fitness_fn=fake_fitness)
    assert len(result.history) <= 50


def test_history_never_gets_worse():
    result = run(budget=80, seed=2, fitness_fn=fake_fitness)
    for i in range(1, len(result.history)):
        assert result.history[i] >= result.history[i - 1]


def test_improves_on_fake_problem():
    result = run(budget=300, seed=3, fitness_fn=fake_fitness)
    assert result.history[-1] > result.history[0]
    assert result.best_fitness > -5


def test_same_seed_same_result():
    a = run(budget=60, seed=4, fitness_fn=fake_fitness)
    b = run(budget=60, seed=4, fitness_fn=fake_fitness)
    assert a.best_weights == b.best_weights


def test_first_weight_fixed_and_in_bounds():
    result = run(budget=100, seed=5, fitness_fn=fake_fitness)
    assert result.best_weights[0] == 1.0
    assert len(result.best_weights) == N_WEIGHTS
    for w in result.best_weights:
        assert BOUNDS[0] <= w <= BOUNDS[1]


def test_crossover_and_mutate():
    import random
    rng = random.Random(0)
    a = [1.0, 1, 1, 1, 1, 1]
    b = [1.0, 2, 2, 2, 2, 2]
    child_a, child_b = crossover(a, b, 1.0, rng)
    assert sorted(child_a + child_b) == sorted(a + b)
    assert mutate(a, 0.0, rng) == a