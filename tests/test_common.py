from __future__ import annotations

import random

from optimise.common import BOUNDS, N_WEIGHTS, neighbour, random_weights

TRIALS = 1000


def test_random_weights_shape_and_bounds():
    rng = random.Random(0)
    for _ in range(TRIALS):
        weights = random_weights(rng)
        assert len(weights) == N_WEIGHTS
        assert weights[0] == 1.0
        assert all(BOUNDS[0] <= w <= BOUNDS[1] for w in weights)


def test_neighbour_changes_exactly_one_weight():
    rng = random.Random(0)
    weights = [1.0, 0.0, 1.0, -1.0, 2.0, -2.0]
    for _ in range(TRIALS):
        changed = [i for i, (a, b) in enumerate(zip(weights, neighbour(weights, rng))) if a != b]
        assert len(changed) == 1


def test_neighbour_never_changes_index_0():
    rng = random.Random(0)
    for _ in range(TRIALS):
        assert neighbour(random_weights(rng), rng)[0] == 1.0


def test_neighbour_stays_in_bounds():
    rng = random.Random(0)
    for start in ([1.0] + [BOUNDS[1]] * 5, [1.0] + [BOUNDS[0]] * 5):
        for _ in range(TRIALS):
            result = neighbour(start, rng, step=3.0)
            assert all(BOUNDS[0] <= w <= BOUNDS[1] for w in result)


def test_neighbour_does_not_mutate_input():
    weights = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    neighbour(weights, random.Random(0))
    assert weights == [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
