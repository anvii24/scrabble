from __future__ import annotations

import random
import time

from optimise import fitness as fit
from optimise.common import Result, neighbour, random_weights


def run(budget: int = 100, seed: int = 0, n_neighbours: int = 10) -> Result:
    start = time.perf_counter()
    rng = random.Random(seed)
    fit.reset_calls()

    best_weights: list[float] = []
    best_fitness = float("-inf")
    history: list[float] = []
    restarts = 0

    def evaluate(weights):
        nonlocal best_weights, best_fitness
        value = fit.fitness(weights, seed=seed)
        if value > best_fitness:
            best_fitness, best_weights = value, list(weights)
        history.append(best_fitness)          
        return value

    while fit.CALLS < budget:
        if restarts == 0:
            current = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        else:
            current = random_weights(rng)
        current_fit = evaluate(current)

        while fit.CALLS < budget:
            cand_weights, cand_fit = None, float("-inf")
            for _ in range(n_neighbours):
                if fit.CALLS >= budget:
                    break
                cand = neighbour(current, rng)
                value = evaluate(cand)
                if value > cand_fit:
                    cand_weights, cand_fit = cand, value

            if cand_weights is not None and cand_fit > current_fit:
                current, current_fit = cand_weights, cand_fit
            else:
                restarts += 1                  
                break

    return Result("hill_climb", best_weights, best_fitness, history,
                  time.perf_counter() - start, seed,
                  {"restarts": restarts, "n_neighbours": n_neighbours})