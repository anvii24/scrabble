from __future__ import annotations

import math
import random
import time

from optimise.common import Result, neighbour, random_weights

def run(
    budget: int = 100, seed: int = 0, T0: float = 10.0, alpha: float = 0.97
)
    
    from optimise import fitness as fitness_module

    start = time.time()
    rng = random.Random(seed)
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

    current = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    current_fitness = evaluate(current)
    temperature = T0

    while calls_made < budget:
        candidate_weights = neighbour(current, rng)
        candidate_fitness = evaluate(candidate_weights)

        delta = candidate_fitness - current_fitness

        if delta >= 0:
            accept = True
        elif temperature <= 0:
            accept = False
        else:
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
