from __future__ import annotations

import math
import random
import time

from optimise.common import Result, neighbour, random_weights


def run(
    budget: int = 100, seed: int = 0, T0: float = 10.0, alpha: float = 0.97
) -> Result:
    """Optimise the evaluation weights with simulated annealing.

    Args:
        budget: maximum number of calls to the shared fitness function.
            The initial evaluation of the starting weights counts towards
            this budget, so for ``budget <= 0`` no evaluation is made at
            all.
        seed: seeds both the search's own randomness (the starting weights,
            the neighbour moves, and the acceptance draws) and the games
            played inside the fitness function, so a run is fully
            reproducible.
        T0: starting temperature. Higher means the search is more willing
            to accept worsening moves early on.
        alpha: geometric cooling rate applied after every iteration,
            ``T <- T * alpha``. Must be in (0, 1) for the temperature to
            cool towards zero.

    Returns:
        A `Result` with ``technique="annealing"``, the best weights and
        fitness found, the best-so-far fitness after every fitness call,
        the run's wall-clock time, the seed used, and an ``extra`` dict
        with the final temperature and number of fitness calls spent.
    """
    # Imported lazily so that importing this module does not require the
    # fitness module (and, through it, the lexicon file) to be importable --
    # useful for tests that inject their own fitness function indirectly by
    # monkeypatching `optimise.fitness.fitness`.
    from optimise import fitness as fitness_module

    start = time.time()
    rng = random.Random(seed)
    # Zero the shared counter so it reports this run's own call count
    # (used by experiments/run_all.py and reported in `extra` below). The
    # budget itself is tracked with a local counter rather than this
    # global one, so that a fitness function which forgets to bump `CALLS`
    # (e.g. a fake used in a unit test) cannot leave this loop spinning
    # forever.
    fitness_module.reset_calls()
    calls_made = 0

    history: list[float] = []
    best_weights: list[float] | None = None
    best_fitness = float("-inf")

    if budget < 1:
        return Result(
            technique="annealing",
            best_weights=best_weights,
            best_fitness=best_fitness,
            history=history,
            runtime_s=time.time() - start,
            seed=seed,
            extra={"final_temperature": T0, "calls": 0},
        )

    def evaluate(weights: list[float]) -> float:
        nonlocal best_weights, best_fitness, calls_made
        value = fitness_module.fitness(weights, seed=seed)
        calls_made += 1
        if value > best_fitness:
            best_fitness = value
            best_weights = list(weights)
        history.append(best_fitness)
        return value

    current_weights = random_weights(rng)
    current_fitness = evaluate(current_weights)
    temperature = T0

    while calls_made < budget:
        candidate_weights = neighbour(current_weights, rng)
        candidate_fitness = evaluate(candidate_weights)

        delta = candidate_fitness - current_fitness

        if delta >= 0:
            accept = True
        elif temperature <= 0:
            accept = False
        else:
            # Guard against floating-point overflow in exp() for very
            # negative delta / very low (but still positive) temperature:
            # such moves would be accepted with ~0 probability anyway.
            exponent = delta / temperature
            probability = math.exp(exponent) if exponent > -700 else 0.0
            accept = rng.random() < probability

        if accept:
            current_weights = candidate_weights
            current_fitness = candidate_fitness

        temperature *= alpha

    return Result(
        technique="annealing",
        best_weights=best_weights,
        best_fitness=best_fitness,
        history=history,
        runtime_s=time.time() - start,
        seed=seed,
        extra={"final_temperature": temperature, "calls": calls_made},
    )
