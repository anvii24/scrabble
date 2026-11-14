from __future__ import annotations

import random
import time
from collections import deque

from optimise import fitness as fit
from optimise.common import Result, neighbour


def _move_of(old: list[float], new: list[float]) -> tuple[int, int]:
    for i, (a, b) in enumerate(zip(old, new)):
        if a != b:
            return i, (1 if b > a else -1)
    return 1, 0


def run(
    budget: int = 100, seed: int = 0, n_neighbours: int = 10, tabu_size: int = 7
) -> Result:
    start = time.perf_counter()
    rng = random.Random(seed)
    fit.reset_calls()

    best_weights: list[float] = []
    best_fitness = float("-inf")
    history: list[float] = []
    tabu: deque[tuple[int, int]] = deque(maxlen=tabu_size)
    aspirations = 0

    def evaluate(weights):
        nonlocal best_weights, best_fitness
        value = fit.fitness(weights, seed=seed)
        if value > best_fitness:
            best_fitness, best_weights = value, list(weights)
        history.append(best_fitness)
        return value

    current = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    evaluate(current)

    while fit.CALLS < budget:
        candidates = []  
        for _ in range(n_neighbours):
            if fit.CALLS >= budget:
                break
            cand = neighbour(current, rng)
            move = _move_of(current, cand)
            is_tabu = move in tabu
            prev_best = best_fitness
            value = evaluate(cand)
            if is_tabu and value > prev_best:      
                is_tabu = False
                aspirations += 1
            candidates.append((value, cand, move, is_tabu))

        if not candidates:
            break

        allowed = [c for c in candidates if not c[3]]
        pool = allowed if allowed else candidates  
        value, current, (index, direction), _ = max(pool, key=lambda c: c[0])
        tabu.append((index, -direction))           

    return Result("tabu", best_weights, best_fitness, history,
                  time.perf_counter() - start, seed,
                  {"tabu_size": tabu_size, "n_neighbours": n_neighbours,
                   "aspirations": aspirations})