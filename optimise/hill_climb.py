"""Step 7 (optimisation): random-restart hill climbing over the weights."""

from __future__ import annotations

from optimise.common import Result


def run(budget: int = 100, seed: int = 0, n_neighbours: int = 10) -> Result:
    """Tune the weights by random-restart hill climbing.

    Inputs:
        budget: total fitness calls allowed.
        seed: seeds this run's random.Random only. fitness() keeps its default
            game seed, so all candidates are compared on the same games.
        n_neighbours: neighbours sampled per step.
    Outputs:
        A Result with technique "hill_climb". `history` holds the best-so-far
        fitness after every fitness call, so len(history) == budget.
    Rules:
        Call reset_calls(), then start from random_weights. Each step, sample
        n_neighbours neighbours and move to the best if it improves on the
        current point. If none does, it is a local optimum: restart from new
        random_weights. best_weights is the best seen across all restarts.
        Stop as soon as CALLS reaches budget, even partway through a step.
    Edge cases:
        extra should record "restarts". budget=1 evaluates only the start.
    """
    raise NotImplementedError
