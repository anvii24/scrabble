from __future__ import annotations

import random
from dataclasses import dataclass

N_WEIGHTS = 6
BOUNDS = (-5.0, 5.0)


def _clamp(value: float) -> float:
    return max(BOUNDS[0], min(BOUNDS[1], value))


def random_weights(rng: random.Random) -> list[float]:
    return [1.0] + [rng.uniform(*BOUNDS) for _ in range(N_WEIGHTS - 1)]


def neighbour(weights: list[float], rng: random.Random, step: float = 0.5) -> list[float]:
    result = list(weights)
    index = rng.randint(1, N_WEIGHTS - 1)
    result[index] = _clamp(result[index] + rng.uniform(-step, step))
    return result


@dataclass
class Result:
    technique: str
    best_weights: list[float]
    best_fitness: float
    history: list[float]
    runtime_s: float
    seed: int
    extra: dict
