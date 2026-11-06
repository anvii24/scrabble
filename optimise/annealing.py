"""Step 7 (optimisation): simulated annealing over the weights."""

from __future__ import annotations

from optimise.common import Result


def run(budget: int = 100, seed: int = 0, T0: float = 10.0, alpha: float = 0.97) -> Result:
    """Tune the weights by simulated annealing.

    Inputs:
        budget: total fitness calls allowed.
        seed: seeds this run's random.Random only.
        T0: starting temperature, in the same units as fitness (score margin).
        alpha: geometric cooling factor, 0 < alpha < 1.
    Outputs:
        A Result with technique "annealing"; `history` as in hill_climb.run.
        extra should record "final_T" and "accepted_worse".
    Rules:
        Call reset_calls(), then start from random_weights with T = T0. Each
        step, evaluate one neighbour and compute delta = new - current, so
        positive is better. Accept if delta >= 0, otherwise accept with
        probability exp(delta / T). Then T *= alpha, whether accepted or not.
        Stop when CALLS reaches budget.
    Edge cases:
        Keep the best ever separately: the final point may not be the best. All
        randomness, including the acceptance test, uses this run's Random.
    """
    raise NotImplementedError
