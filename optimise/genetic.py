"""Step 7 (optimisation): a genetic algorithm over the weights."""

from __future__ import annotations

from optimise.common import Result


def run(
    budget: int = 100,
    seed: int = 0,
    pop_size: int = 10,
    tour_k: int = 3,
    p_cross: float = 0.8,
    p_mut: float = 0.1,
    elite: int = 2,
) -> Result:
    """Tune the weights with a generational genetic algorithm.

    Inputs:
        budget: total fitness calls allowed.
        seed: seeds this run's random.Random only.
        pop_size: individuals per generation.
        tour_k: tournament size.
        p_cross: probability a pair of parents is crossed over.
        p_mut: per-gene mutation probability.
        elite: top individuals copied unchanged into the next generation.
    Outputs:
        A Result with technique "genetic"; `history` as in hill_climb.run.
        extra["avg_per_gen"] and extra["best_per_gen"] each hold one fitness
        value per fully evaluated generation.
    Rules:
        Call reset_calls(), then evaluate a population of random_weights. Each
        generation: copy the `elite` best, then fill the rest with children.
        Pick two parents by tournament (best of tour_k sampled at random). With
        probability p_cross, swap tails at a single cut point in 1..5, otherwise
        copy the parents. Mutate each of genes 1..5 with probability p_mut by
        adding gauss(0, 0.5), clamped to BOUNDS. Gene 0 stays 1.0 throughout.
        Stop as soon as CALLS reaches budget, even partway through a generation.
    Edge cases:
        Elites keep their stored fitness and are not re-evaluated: fitness is
        deterministic, so that would waste budget. Raises ValueError if
        elite > pop_size or tour_k > pop_size. If a pair of children would
        overfill the population, drop the second.
    """
    raise NotImplementedError
