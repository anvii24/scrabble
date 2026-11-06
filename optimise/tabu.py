"""Step 7 (optimisation): tabu search over the weights."""

from __future__ import annotations

from optimise.common import Result


def run(
    budget: int = 100, seed: int = 0, n_neighbours: int = 10, tabu_size: int = 7
) -> Result:
    """Tune the weights by tabu search.

    Inputs:
        budget: total fitness calls allowed.
        seed: seeds this run's random.Random only.
        n_neighbours: neighbours sampled per step.
        tabu_size: maximum entries in the tabu list.
    Outputs:
        A Result with technique "tabu"; `history` as in hill_climb.run.
    Rules:
        Call reset_calls(), then start from random_weights. Each step, sample
        n_neighbours neighbours and move to the best non-tabu one even if it is
        worse than the current point. That ability to go downhill is what
        distinguishes this from hill climbing.
        The tabu list is a FIFO of (weight_index, direction), direction being
        +1 or -1. After a move on weight i in direction d, add (i, -d), which
        forbids undoing it. Evict the oldest entry past tabu_size.
        Aspiration: a tabu neighbour is allowed if it beats the best ever.
        Stop as soon as CALLS reaches budget.
    Edge cases:
        neighbour() does not report what it changed, so find the index and
        direction by comparing with the current weights. A neighbour identical
        to the current point (clamped at a bound) has no direction: skip it.
        If every neighbour is tabu and none aspirates, stay put and resample.
        Since that spends budget on no move, record "stuck_steps" in extra.
    """
    raise NotImplementedError
