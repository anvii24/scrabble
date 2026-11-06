"""Step 7 (optimisation): weight-vector helpers shared by all four techniques.

Weight index 0 multiplies the move score and is always fixed at 1.0, so only
indices 1..5 are searched.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

N_WEIGHTS = 6
BOUNDS = (-5.0, 5.0)


def _clamp(value: float) -> float:
    return max(BOUNDS[0], min(BOUNDS[1], value))


def random_weights(rng: random.Random) -> list[float]:
    """Return a random weight vector with index 0 fixed at 1.0."""
    return [1.0] + [rng.uniform(*BOUNDS) for _ in range(N_WEIGHTS - 1)]


def neighbour(weights: list[float], rng: random.Random, step: float = 0.5) -> list[float]:
    """Return a copy of `weights` with one of indices 1..5 nudged by up to `step`.

    The result is clamped to BOUNDS, so a weight already at a bound can come
    back unchanged when the nudge points outwards.
    """
    result = list(weights)
    index = rng.randint(1, N_WEIGHTS - 1)
    result[index] = _clamp(result[index] + rng.uniform(-step, step))
    return result


@dataclass
class Result:
    """Outcome of one optimiser run."""

    technique: str
    best_weights: list[float]
    best_fitness: float
    history: list[float]
    runtime_s: float
    seed: int
    extra: dict
